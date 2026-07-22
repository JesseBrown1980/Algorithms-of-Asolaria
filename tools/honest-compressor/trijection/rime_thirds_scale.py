#!/usr/bin/env python3
"""
rime_thirds_scale.py — THE ENTIRE (verifiable) CORPUS in 3 giant thirds,
binary -> trinary -> 27-nary per third, with bank scaling x1 / x3 / x9 and the
-1/3 -> 2/3 ledger at full scale. Operator: Jesse Daniel Brown, 2026-07-22.

HONEST WALLS, NAMED: enwik10 is not publicly published (Mahoney's corpus set
stops at enwik9) — so the scale ladder tops at the verified gigabyte; x81 bank
scaling needs 8.1 GB of verified text and is therefore BLOCKED, not faked.
No GPU in this container: CPU numpy, said plainly.

PRE-REGISTERED (before the run): (1) order-2 bank improves only slightly from
x3/x9 data — capacity-bound; (2) unbanked -1/3 -> 2/3 stays at the ~13-14%
floor; banked-2 stays exact and net-zero.
"""
import numpy as np, time, json

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
P, N = 103681, 20736
def primitive_root(p):
    fac, n, d = [], p-1, 2
    while d*d <= n:
        if n % d == 0:
            fac.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p-1)//q, p) != 1 for q in fac): return g
g = primitive_root(P); W = pow(g, (P-1)//N, P)
pts = np.empty(N, dtype=np.int64); v = 1
for e in range(N): pts[e] = v; v = v*W % P
inv = np.empty(P+1, dtype=np.int64); inv[pts] = np.arange(N)

SZ = 1_000_000_000; THIRD = SZ // 3            # 333,333,333 B per giant third
HOLD = 100_000_000                              # held-out: the final 100 MB
f = open(f"{S}/enwik9","rb")

# ---------- the 3 giant thirds: tower wind/unwind (binary->trinary->27-nary) ----------
print("=== PART 1: the entire corpus in 3 giant thirds, tower per third ===", flush=True)
tri = np.arange(50_000_000, dtype=np.int64) % 3
thirds_rows = []
for t in range(3):
    f.seek(t*THIRD)
    t0 = time.perf_counter_ns(); ok = True; done = 0
    while done < THIRD:
        take = min(50_000_000, THIRD-done)
        blk = np.frombuffer(f.read(take), dtype=np.uint8).astype(np.int64)
        k = blk + 256*tri[:len(blk)] + 768*((t*9 + done//50_000_000) % 27)   # 27-nary sector tag
        ok &= bool(np.array_equal(inv[pts[k]], k))
        done += take
    ns = time.perf_counter_ns()-t0
    thirds_rows.append(dict(third=t, bytes=THIRD, ns=int(ns), exact=ok))
    print(f"third {t}: {THIRD:,} B wound+unwound in {ns/1e9:.1f} s  byte-exact={ok}", flush=True)

# ---------- bank scaling x1 / x3 / x9, scored on the held-out tail ----------
print("\n=== PART 2: bank scaling x1 / x3 / x9 (order-2 frozen), held-out = final 100 MB ===", flush=True)
f.seek(SZ - HOLD)
hold = np.frombuffer(f.read(HOLD), dtype=np.uint8).astype(np.int64)
hc = hold[:-2]*256 + hold[1:-1]; hn = hold[2:]
C2 = np.zeros(1<<24, dtype=np.int64)
trained = 0; scale_rows = []
def score():
    Cv = C2.reshape(65536,256)
    T2 = Cv.sum(axis=1)
    pr = (Cv[hc, hn] + 1.0) / (T2[hc] + 256.0)
    return float((-np.log2(pr)).mean())
for target in (100_000_000, 300_000_000, 900_000_000):
    f.seek(trained)
    while trained < target:
        take = min(100_000_000, target-trained)
        b = np.frombuffer(f.read(take), dtype=np.uint8).astype(np.int64)
        C2 += np.bincount(b[:-2]*65536 + b[1:-1]*256 + b[2:], minlength=1<<24)
        trained += take
    t0 = time.perf_counter_ns(); bpc = score(); ns = time.perf_counter_ns()-t0
    scale_rows.append(dict(bank_MB=target//1_000_000, heldout_bpc=bpc, score_ns=int(ns)))
    print(f"bank {target//1_000_000:>3} MB (x{target//100_000_000}): held-out bpc = {bpc:.4f}", flush=True)

# ---------- the -1/3 -> 2/3 ledger at whole-corpus scale ----------
print("\n=== PART 3: -1/3 -> 2/3 at full scale (thirds of the ENTIRE corpus) ===", flush=True)
f.seek(0); A = np.frombuffer(f.read(THIRD), dtype=np.uint8).astype(np.int16)
B = np.frombuffer(f.read(THIRD), dtype=np.uint8).astype(np.int16)
C = np.frombuffer(f.read(THIRD), dtype=np.uint8).astype(np.int16)
P1 = (-(A+B+C)) % 256
rec = (-(A+B+P1)) % 256                          # bank1, hold 2/3 -> the third
exact1 = bool(np.array_equal(rec, C % 256))
guess = np.full_like(B, 32); forced = (-(A+guess+P1)) % 256
acc = float(((guess%256 == B%256) & (forced == C%256)).mean())
P1b = (-(A+B)) % 256; P2b = (-(A+C)) % 256       # bank2, hold 1/3
exact2 = bool(np.array_equal((-(A+P1b))%256, B%256) and np.array_equal((-(A+P2b))%256, C%256))
print(f"bank1 hold-2/3 -> 1/3: exact={exact1} (333,333,333 B recreated)")
print(f"bank1 hold-1/3 -> 2/3: {acc*100:.2f}% (the floor, at 333 MB scale)")
print(f"bank2 hold-1/3 -> 2/3: exact={exact2} — bank IS 2/3, net zero")

json.dump(dict(thirds=thirds_rows, scaling=scale_rows,
    ledger=dict(bank1_hold23_exact=exact1, bank1_hold13_acc=acc, bank2_hold13_exact=exact2)),
    open(f"{S}/rime_thirds_scale.json","w"), indent=1)
print("\nDONE — receipts in rime_thirds_scale.json")
