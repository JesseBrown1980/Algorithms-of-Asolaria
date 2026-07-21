#!/usr/bin/env python3
"""
njection.py — THE DIRECT N-JECTION (one center, N-1 separations, the Nth FREE),
head-to-head against the NESTED 3-cascade. Operator: Jesse Daniel Brown, 2026-07-21.

Direct N-jection: given N aligned values,
    c0  = floor(sum / N)          # ONE center (grand mean)
    rem = sum - N*c0              # remainder in [0, N-1]
    sep_i = v_i - c0  (i<N-1)     # N-1 separations
    v_{N-1} = c0 + rem - sum(sep) # the Nth point is FREE
Integer-only, restore=OK or invalid.

Question this settles: does a FLAT 27-jection reduce as much as the NESTED
27->9->3->1 cascade? (Answer decides whether the 3x3x3 nesting structure matters.)
"""
import numpy as np
from nested_cascade import H_bits, bal_ternary_zero_frac, cascade, uncascade

def njection_forward(streams):
    N = len(streams)
    s = sum(streams)
    c0 = np.floor_divide(s, N)
    rem = s - N * c0
    seps = [streams[i] - c0 for i in range(N - 1)]
    return c0, rem, seps

def njection_inverse(c0, rem, seps, N):
    out = [c0 + seps[i] for i in range(N - 1)]
    tot = seps[0].copy() if seps else np.zeros_like(c0)
    for sp in seps[1:]: tot = tot + sp
    out.append(c0 + rem - tot)     # the free Nth
    return out

def measure_direct(streams, label):
    N = len(streams); L = streams[0].size
    c0, rem, seps = njection_forward(streams)
    rec = njection_inverse(c0, rem, seps, N)
    ok = all(np.array_equal(a, b) for a, b in zip(rec, streams))
    raw = sum(H_bits(s) for s in streams)
    nj = H_bits(c0) + H_bits(rem) + sum(H_bits(sp) for sp in seps)
    zf = bal_ternary_zero_frac([c0] + seps)
    print(f"[DIRECT {N}-jection · {label}]  restore={'OK' if ok else 'FAIL'}")
    print(f"   raw={raw/(N*L):.4f}  njection={nj/(N*L):.4f} bpc  reduction={raw/nj:.2f}x  zero-trit={zf:.3f}")
    return raw, nj

def measure_nested(streams, label):
    N = len(streams); L = streams[0].size
    grand, levels = cascade([s.copy() for s in streams])
    rec = uncascade(grand, levels)
    ok = all(np.array_equal(a, b) for a, b in zip(rec, [s for s in streams]))
    raw = sum(H_bits(s) for s in streams)
    nb = H_bits(grand)
    for seps in levels:
        for sa, sb, rem in seps: nb += H_bits(sa) + H_bits(sb) + H_bits(rem)
    print(f"[NESTED {N}->..->1 cascade · {label}]  restore={'OK' if ok else 'FAIL'}")
    print(f"   raw={raw/(N*L):.4f}  cascade={nb/(N*L):.4f} bpc  reduction={raw/nb:.2f}x")
    return raw, nb

if __name__ == "__main__":
    L = 50000; idx = np.arange(L, dtype=np.int64)
    sig = (128 + 100 * np.sin(idx * 0.01)).astype(np.int64)   # the omniverse center
    print("=== 27-JECTION (flat) vs NESTED 27->9->3->1 — head to head ===\n")
    for N in (3, 9, 27, 81):
        streams = [sig + ((idx * (7 + 2*m)) % 5) - 2 for m in range(N)]
        rd, nd = measure_direct(streams, f"{N} shared-center")
        rn, nn = measure_nested(streams, f"{N} shared-center")
        print(f"   --> flat {N}-jection {rd/nd:.2f}x   vs   nested {rn/nn:.2f}x   "
              f"({'NESTED wins' if nn<nd else 'flat wins' if nd<nn else 'tie'})\n")
    print("--- CONTROL: 27 independent (no shared center) ---")
    rng = np.random.RandomState(12345)
    indep = [rng.randint(0, 256, size=L).astype(np.int64) for _ in range(27)]
    measure_direct(indep, "27 independent")
    measure_nested(indep, "27 independent")
