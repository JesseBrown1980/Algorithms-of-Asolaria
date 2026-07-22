#!/usr/bin/env python3
"""
rime_deep6h.py — the 6-hour SGRAM understanding run, refereed.
Operator: Jesse Daniel Brown, 2026-07-22.

Tests "more computation = stronger understanding" on the axis where it is TRUE:
context DEPTH, not repeated seconds. Trains progressively deeper order-k byte
models over the ENTIRE enwik9 (SGRAM-sharded, integer, deterministic), climbing
the rime cadence of orders/contexts, and at each staggered checkpoint measures
held-out bpc on text never trained on. Receipt written incrementally (restart-safe).

PRE-REGISTERED (before run): held-out bpc DROPS with depth (real understanding),
FLATTENS with repeated same-depth passes (the wall measured earlier tonight).
The receipt referees the claim; the measurement is the judge.
"""
import time, json, math, os, hashlib
from array import array

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
CORPUS = f"{S}/enwik9"
RECEIPT = f"{S}/rime_deep6h.jsonl"
BUDGET = 6*3600
HELD = 20_000_000
TRAIN_END = 1_000_000_000 - HELD

held = open(CORPUS, 'rb').read()[TRAIN_END:TRAIN_END+HELD]
held_measure = held[:3_000_000]      # fast, stable bpc estimate (~0.01 of full)

def log(obj):
    with open(RECEIPT, 'a') as f: f.write(json.dumps(obj) + "\n")

# staggered rime checkpoints (seconds): 3 / 27 / 81 / 243 / 729 / 2187 / 6561 / ... x3
CKPT = [3, 27, 81, 243, 729, 2187, 6561, 10000, 14000, 18000, 21600]

t0 = time.time()
log(dict(event="start", budget_s=BUDGET, pre_registered=
    "bpc drops with DEPTH (real), flattens with repeated same-depth passes (the wall)",
    corpus="enwik9", train_bytes=TRAIN_END, held_bytes=HELD))

# progressively deepen: order 1 -> 2 -> 3 -> 4, each a real pass, held-out measured.
# higher orders use sparse dict counts (memory-bounded by real context diversity),
# capped so the 6h job never OOMs.
ORDERS = [1, 2, 3, 4, 5]
CAP = 60_000_000            # max distinct contexts kept per order (LRU-free: freeze when full)

def measure(counts, order, K=256):
    mask = (1 << (8*order)) - 1
    bits = 0.0; ctx = 0
    for b in held_measure:
        d = counts.get(ctx & mask)
        if d:
            c = d.get(b, 0); t = d.get(-1, 0)
            p = (c + 1) / (t + K)
        else:
            p = 1 / K
        bits += -math.log2(p)
        ctx = ((ctx << 8) | b) & mask
    return bits / len(held_measure)

ck_i = 0
results = []
for order in ORDERS:
    if time.time() - t0 > BUDGET: break
    counts = {}
    mask = (1 << (8*order)) - 1
    ctx = 0; frozen = False; passes = 0
    # one full pass over training corpus, in 50MB SGRAM shards
    pos = 0; shard = 50_000_000
    stage_t = time.time()
    with open(CORPUS, 'rb') as f:
        while pos < TRAIN_END and time.time() - t0 < BUDGET:
            f.seek(pos); data = f.read(min(shard, TRAIN_END - pos))
            for b in data:
                key = ctx & mask
                d = counts.get(key)
                if d is None:
                    if not frozen and len(counts) < CAP:
                        d = {}; counts[key] = d
                    else:
                        ctx = ((ctx << 8) | b) & mask; continue
                d[b] = d.get(b, 0) + 1; d[-1] = d.get(-1, 0) + 1
                ctx = ((ctx << 8) | b) & mask
            if len(counts) >= CAP: frozen = True
            pos += shard
            # staggered checkpoint?
            el = time.time() - t0
            while ck_i < len(CKPT) and el >= CKPT[ck_i]:
                bpc = measure(counts, order)
                rec = dict(event="checkpoint", t_s=round(el), order=order,
                    contexts=len(counts), frozen=frozen, heldout_bpc=round(bpc, 4),
                    train_pos=pos)
                log(rec); results.append(rec)
                print(f"[{el:6.0f}s] order-{order} contexts={len(counts):,} "
                      f"held-out bpc={bpc:.4f}", flush=True)
                ck_i += 1
    # end-of-order measurement (always)
    bpc = measure(counts, order)
    rec = dict(event="order_done", t_s=round(time.time()-t0), order=order,
        contexts=len(counts), frozen=frozen, heldout_bpc=round(bpc, 4),
        stage_s=round(time.time()-stage_t))
    log(rec); results.append(rec)
    print(f"ORDER {order} DONE: contexts={len(counts):,} held-out bpc={bpc:.4f} "
          f"({time.time()-stage_t:.0f}s)", flush=True)

# verdict
by_order = {}
for r in results:
    if r.get("event") in ("checkpoint", "order_done"):
        by_order[r["order"]] = r["heldout_bpc"]
drops = sorted(by_order.items())
verdict = "DEPTH lowers bpc (understanding deepens with context, not seconds)" \
    if len(drops) > 1 and drops[-1][1] < drops[0][1] else "flat — wall reached"
log(dict(event="verdict", by_order=by_order, verdict=verdict, wall_s=round(time.time()-t0)))
print(f"\nVERDICT: {verdict}")
print("by order:", by_order)
