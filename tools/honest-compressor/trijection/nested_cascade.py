#!/usr/bin/env python3
"""
nested_cascade.py — THE REDUCTION LAW OF 27 -> 3 -> 1 (nested trijection).
Operator: Jesse Daniel Brown. Sealed 2026-07-21.

Rule of 3: three machines collapse into 1 outside-center + 2 separations (3rd free).
Rule of 27: nest it three deep -> 27 -> 9 -> 3 -> 1. Every center is an OUTSIDE
viewer that sees its three separately; the center costs nothing (reference frame),
the separations are paid. Integer-only (floor-division exact for negatives too),
so bit-identical on any CPU / Rust version. restore=OK or the run is invalid.

HONEST LAW: this reduces the COUNT via free centers (27 universes -> 1 grand center
+ cascaded separations). It works only when the machines SHARE A DEEP CENTER (they
are separate universes of ONE omniverse). Independent universes share no center ->
no reduction. It never beats the JOINT entropy; it stops paying for the shared
center N-1 extra times. "Spend one universe to get the universe."
"""
import sys, math
import numpy as np

def H_bits(a):
    a = np.asarray(a)
    v, c = np.unique(a, return_counts=True)
    N = a.size
    return float(-np.sum(c * np.log2(c / N))) if N else 0.0

def bal_ternary_zero_frac(arrs, digits=8):
    zeros = tot = 0
    for a in arrs:
        for x in np.asarray(a).ravel():
            n = int(abs(x))
            for _ in range(digits):
                r = n % 3; n //= 3
                if r == 2: r = -1; n += 1
                tot += 1; zeros += (r == 0)
    return zeros / tot if tot else 0.0

def trijection_level(streams):
    centers, seps = [], []
    for g in range(0, len(streams), 3):
        a, b, c = streams[g], streams[g+1], streams[g+2]
        s = a + b + c
        c0 = np.floor_divide(s, 3)          # floors toward -inf -> rem in {0,1,2}
        rem = s - 3 * c0
        sa = a - c0; sb = b - c0
        centers.append(c0); seps.append((sa, sb, rem))
    return centers, seps

def inverse_level(centers, seps):
    out = []
    for c0, (sa, sb, rem) in zip(centers, seps):
        out.append(c0 + sa)                 # a
        out.append(c0 + sb)                 # b
        out.append(c0 + rem - sa - sb)      # c (the FREE third)
    return out

def cascade(streams):
    levels = []
    while len(streams) > 1:
        centers, seps = trijection_level(streams)
        levels.append(seps)
        streams = centers
    return streams[0], levels

def uncascade(grand, levels):
    streams = [grand]
    for seps in reversed(levels):
        streams = inverse_level(streams, seps)
    return streams

def run(streams, label):
    orig = [s.copy() for s in streams]
    grand, levels = cascade([s.copy() for s in streams])
    rec = uncascade(grand, levels)
    ok = all(np.array_equal(a, b) for a, b in zip(rec, orig))
    raw_bits = sum(H_bits(s) for s in orig)
    casc_bits = H_bits(grand)
    all_seps = [grand]
    for seps in levels:
        for sa, sb, rem in seps:
            casc_bits += H_bits(sa) + H_bits(sb) + H_bits(rem)
            all_seps += [sa, sb]
    L = orig[0].size; N = len(orig)
    zf = bal_ternary_zero_frac(all_seps)
    print(f"[{label}]  {N} machines x {L} = {N*L:,} values  restore={'OK' if ok else 'FAIL'}")
    print(f"   raw (N independent)   = {raw_bits/(N*L):.4f} bpc/value  (total {raw_bits:,.0f} bits)")
    print(f"   cascade (1 center +seps)= {casc_bits/(N*L):.4f} bpc/value  (total {casc_bits:,.0f} bits)")
    print(f"   reduction = {raw_bits/casc_bits:.2f}x   free-center zero-trit frac = {zf:.3f}")
    print(f"   levels 27->9->3->1: {[len(l) for l in levels]} triples per level\n")
    return raw_bits, casc_bits, ok

if __name__ == "__main__":
    L = 50000
    idx = np.arange(L, dtype=np.int64)
    # ONE omniverse signal = the shared deep center
    sig = (128 + 100 * np.sin(idx * 0.01)).astype(np.int64)

    print("=== NESTED TRIJECTION CASCADE — reduction law of 27->3->1 ===\n")
    print("--- TEST 1: 27 separate universes sharing ONE omniverse center ---")
    streams27 = [sig + ((idx * (7 + 2*m)) % 5) - 2 for m in range(27)]  # tiny distinct jitter
    run(streams27, "27 shared-center universes")

    print("--- TEST 2: scaling — reduction grows as machines are added (all share center) ---")
    for N in (3, 9, 27, 81):
        streams = [sig + ((idx * (7 + 2*m)) % 5) - 2 for m in range(N)]
        run(streams, f"{N} shared-center universes")

    print("--- CONTROL: 27 INDEPENDENT universes (no shared center) — must NOT reduce ---")
    rng = np.random.RandomState(12345)
    indep = [rng.randint(0, 256, size=L).astype(np.int64) for _ in range(27)]
    run(indep, "27 independent universes")
