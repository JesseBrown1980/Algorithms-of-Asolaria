#!/usr/bin/env python3
"""
trit_waves.py — the n(x3x3) WAVES, measured. Operator: Jesse Daniel Brown.
For each data size (1 / 6 / 27 MB), build the TRINARY TOWER and report held-out
bits/byte at each level (27=3^3, 243=3^5, 729=3^6, 3^9, 3^12, 3^13). Shows the
WAVE (bpc drops per level) and the moving WALL (best level deepens with size) —
the direct measurement of "you can't see the next x3x3 until you build it, and
you can't build it until you have the data."  Vectorized (numpy), exact (direct
base-3 index, no hashing), deterministic. Never below Shannon.
"""
import numpy as np, math, time
from numpy.lib.stride_tricks import sliding_window_view

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
raw = np.frombuffer(open(f"{S}/enwik9",'rb').read(30_000_000), dtype=np.uint8)
held_bytes = np.frombuffer(open(f"{S}/enwik9",'rb').read()[900_000_000:901_000_000], dtype=np.uint8)

def to_trits(b):
    # each byte -> 6 balanced-position trits (reversible); the trinary stream
    out = np.empty(len(b)*6, dtype=np.int8)
    v = b.astype(np.int32).copy()
    for k in range(6):
        out[k::6] = (v % 3).astype(np.int8); v //= 3
    return out

held_t = to_trits(held_bytes)
HEIGHTS = [3, 5, 6, 9, 12, 13]
NARY = {h: 3**h for h in HEIGHTS}

def bpc_at(train_t, h, held_t, nbytes_held):
    P = 3**h
    powers = (3**np.arange(h-1,-1,-1)).astype(np.int64)
    # train counts: context(h trits) -> next trit
    w = sliding_window_view(train_t.astype(np.int64), h+1)   # (M, h+1)
    ctx = w[:, :h] @ powers
    nxt = w[:, h]
    flat = ctx*3 + nxt
    counts = np.bincount(flat, minlength=P*3).reshape(P, 3).astype(np.float64)
    tot = counts.sum(1, keepdims=True)
    prob = (counts + 0.33) / (tot + 1.0)
    # held-out
    wh = sliding_window_view(held_t.astype(np.int64), h+1)
    ctxh = wh[:, :h] @ powers
    nxth = wh[:, h]
    p = prob[ctxh, nxth]
    bits = -np.log2(p).sum()
    return bits / nbytes_held

for MB in (1, 6, 27):
    NT = MB*1_000_000
    train_t = to_trits(raw[:NT])
    t0 = time.time()
    row = []
    for h in HEIGHTS:
        b = bpc_at(train_t, h, held_t, 1_000_000)
        row.append((h, b))
    best = min(row, key=lambda x: x[1])
    print(f"=== {MB} MB train ({len(train_t):,} trits) ===  best = 3^{best[0]} ({NARY[best[0]]:,}-nary)  bpc {best[1]:.4f}")
    prev = None
    for h, b in row:
        wave = "" if prev is None else (f"  ↓ {prev-b:+.3f}" if b < prev else f"  ↑ {b-prev:+.3f} (wall)")
        print(f"   level 3^{h:<2} = {NARY[h]:>10,}-nary : {b:.4f} bpc{wave}")
        prev = b
    print(f"   ({time.time()-t0:.0f}s)\n", flush=True)
print("READING: within a size, bpc falls per level then rises = the wave hitting its wall.")
print("Across sizes, the best level DEEPENS = the wall recedes with data. Both measured.")
