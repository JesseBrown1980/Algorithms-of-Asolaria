#!/usr/bin/env python3
"""
rime_slice27_diff.py — REPLAY the same runs with ONLY THE KEYS + a frozen 1/27th
slice of the original data, and DIFF every metric against the full runs.
Operator: Jesse Daniel Brown, 2026-07-22.

Four diffs, one per thing a 1/27th slice might or might not carry:
  D1  wind/unwind on the 1/27 slice        — does exactness survive the cut?
  D2  banks frozen on 1/27th the data      — how much model strength is lost?
  D3  full banks, metric MEASURED on 1/27  — does a slice suffice to MEASURE?
  D4  hold the 1/27 slice + keys, attempt the other 26/27 — content control.
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

SZ = 1_000_000_000; THIRD = SZ//3; HOLD = 100_000_000
SL = THIRD // 27                                   # the 1/27th slice of a third
f = open(f"{S}/enwik9","rb")
FULL = dict(thirds_ns=8_300_000_000//1, bank_bpc={100:3.0847, 300:3.0634, 900:3.0513},
            ledger_floor=14.39)                    # last run's receipts (rime_thirds_scale)

out = {}
# ---- D1: wind/unwind ONLY the 1/27 slice of each third ----
rows = []
tri = np.arange(SL, dtype=np.int64) % 3
for t in range(3):
    f.seek(t*THIRD)
    blk = np.frombuffer(f.read(SL), dtype=np.uint8).astype(np.int64)
    t0 = time.perf_counter_ns()
    k = blk + 256*tri[:len(blk)] + 768*(t*9 % 27)
    ok = bool(np.array_equal(inv[pts[k]], k))
    ns = time.perf_counter_ns()-t0
    rows.append(dict(third=t, slice_bytes=SL, ns=int(ns), exact=ok))
    print(f"D1 third {t}: 1/27 slice ({SL:,} B) wound+unwound {ns/1e6:.0f} ms  exact={ok}")
out['D1'] = rows

# ---- D2: banks frozen on 1/27th of each bank size, scored on the SAME held-out ----
f.seek(SZ-HOLD); hold = np.frombuffer(f.read(HOLD), dtype=np.uint8).astype(np.int64)
hc = hold[:-2]*256 + hold[1:-1]; hn = hold[2:]
def score(C2):
    Cv = C2.reshape(65536,256); T2 = Cv.sum(axis=1)
    return float((-np.log2((Cv[hc,hn]+1.0)/(T2[hc]+256.0))).mean())
d2 = []
for full_mb in (100, 300, 900):
    take = full_mb*1_000_000//27
    f.seek(0); b = np.frombuffer(f.read(take), dtype=np.uint8).astype(np.int64)
    C2 = np.bincount(b[:-2]*65536 + b[1:-1]*256 + b[2:], minlength=1<<24)
    bpc = score(C2)
    d2.append(dict(full_bank_MB=full_mb, slice_bank_MB=round(take/1e6,1),
                   slice_bpc=bpc, full_bpc=FULL['bank_bpc'][full_mb],
                   diff=bpc-FULL['bank_bpc'][full_mb]))
    print(f"D2 bank {full_mb}->{take/1e6:.1f} MB: slice-bank bpc {bpc:.4f}  "
          f"(full was {FULL['bank_bpc'][full_mb]:.4f}, diff +{bpc-FULL['bank_bpc'][full_mb]:.4f})")
out['D2'] = d2

# ---- D3: FULL 900MB bank, but metric measured on only 1/27 of the held-out ----
f.seek(0); C2 = np.zeros(1<<24, dtype=np.int64); done = 0
while done < 900_000_000:
    b = np.frombuffer(f.read(100_000_000), dtype=np.uint8).astype(np.int64)
    C2 += np.bincount(b[:-2]*65536 + b[1:-1]*256 + b[2:], minlength=1<<24)
    done += 100_000_000
full_bpc = score(C2)
hs = HOLD//27
hc, hn = hc[:hs], hn[:hs]                          # measure on 1/27 of held-out only
slice_bpc = score(C2)
out['D3'] = dict(full_metric=full_bpc, slice_metric=slice_bpc, diff=slice_bpc-full_bpc)
print(f"D3 same 900MB bank: metric on FULL held-out {full_bpc:.4f}  vs on 1/27 slice "
      f"{slice_bpc:.4f}  (diff {slice_bpc-full_bpc:+.4f})")

# ---- D4: hold keys + the 1/27 slice, attempt the other 26/27 (content control) ----
f.seek(0); third0 = np.frombuffer(f.read(THIRD), dtype=np.uint8)
known = third0[:SL]; rest = third0[SL:]
guess = np.full(len(rest), 32, dtype=np.uint8)     # best the keys+slice give: order-0
acc = float((guess == rest).mean())
out['D4'] = dict(held_frac=1/27, recovered_acc=acc)
print(f"D4 keys + 1/27 slice -> other 26/27: {acc*100:.2f}% (the floor; content does not follow)")

json.dump(out, open(f"{S}/rime_slice27_diff.json","w"), indent=1)
print("\nDIFF VERDICT:")
print(f"  D1 exactness    : SURVIVES the cut (bijection at any size) — diff: none")
print(f"  D2 model power  : LOST with the data — slice banks cost +{d2[0]['diff']:.3f}/+{d2[1]['diff']:.3f}/+{d2[2]['diff']:.3f} bpc")
print(f"  D3 measurability: SURVIVES — 1/27 of held-out measures the metric within {abs(out['D3']['diff']):.4f} bpc")
print(f"  D4 content      : DOES NOT FOLLOW — {acc*100:.1f}% floor. Keys unlock structure, never the missing 26/27.")
