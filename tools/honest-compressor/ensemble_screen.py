#!/usr/bin/env python3
# 8-view ensemble screen + isomorphism probe (third-seat independent run).
# Question: do the omega-cube corner views, feeding the model SIMULTANEOUSLY,
# beat the single-view baseline? And WHY — are the view predictions new
# information or the same predictions relabeled?
#
# Causal views only: N (nibble-swap), Q (bit-reverse), NQ. The R-family views
# reverse the sequence — a streaming model would need the FUTURE — so they
# cannot join a causal ensemble (they were tested earlier as preprocessors:
# all worse than identity).
import sys, time
import numpy as np

def bitrev8(x): return int(f"{x:08b}"[::-1], 2)
BR = np.array([bitrev8(i) for i in range(256)], dtype=np.uint8)          # Q
NS = np.array([((i << 4) | (i >> 4)) & 0xFF for i in range(256)], dtype=np.uint8)  # N
NQ = NS[BR]                                                               # N∘Q

def run_model(stream):
    """Context-mixing model, orders 0-2, count-based, weights 1/3/9.
    Returns per-position probability assigned to the ACTUAL next byte."""
    n = len(stream)
    f0 = np.ones(256, dtype=np.uint32)
    f1 = np.ones((256, 256), dtype=np.uint32)
    f2 = np.ones((65536, 256), dtype=np.uint32)
    probs = np.empty(n - 2, dtype=np.float64)
    W0, W1, W2 = 1.0, 3.0, 9.0
    for i in range(2, n):
        c1 = stream[i - 1]
        c2 = (int(stream[i - 2]) << 8) | int(stream[i - 1])
        b = stream[i]
        r0 = f0; r1 = f1[c1]; r2 = f2[c2]
        t0 = r0.sum(); t1 = r1.sum(); t2 = r2.sum()
        p = (W0 * (r0[b] / t0) + W1 * (r1[b] / t1) + W2 * (r2[b] / t2)) / (W0 + W1 + W2)
        probs[i - 2] = p
        r0[b] += 32; r1[b] += 32; r2[b] += 32
        if t0 > 60000: f0[:] = (f0 >> 1) | 1
        if t1 > 60000: f1[c1] = (r1 >> 1) | 1
        if t2 > 60000: f2[c2] = (r2 >> 1) | 1
    return probs

def main():
    N = 300_000
    data = np.frombuffer(open("enwik8", "rb").read(N), dtype=np.uint8)
    print(f"slice: first {N:,} bytes of real enwik8")
    t0 = time.time()
    base = run_model(data)
    print(f"baseline arm      : {(-np.log2(base)).mean():.6f} bpc   ({time.time()-t0:.0f}s)")

    views = {"N": NS[data], "Q": BR[data], "NQ": NQ[data]}
    view_probs = {}
    for name, vstream in views.items():
        t0 = time.time()
        vp = run_model(vstream)      # prob assigned to actual TRANSFORMED byte
        view_probs[name] = vp
        dmax = np.max(np.abs(vp - base))
        print(f"view {name:3} arm      : {(-np.log2(vp)).mean():.6f} bpc   "
              f"max|dp vs baseline| = {dmax:.2e}   ({time.time()-t0:.0f}s)")

    ens = (base + sum(view_probs.values())) / (1 + len(view_probs))
    bpc_base = (-np.log2(base)).mean()
    bpc_ens = (-np.log2(ens)).mean()
    gain = bpc_base - bpc_ens
    print(f"\nensemble (4 models, equal mix): {bpc_ens:.6f} bpc")
    print(f"gain vs baseline              : {gain:+.6f} bpc")
    v = "REAL (>0.010)" if gain > 0.010 else "MARGINAL (0.001-0.010)" if gain > 0.001 else "CLOSED (<=0.001)"
    print(f"pre-registered verdict        : {v}")
    print("\nR-family views (R, RN, RQ, RNQ): NON-CAUSAL for streaming — excluded;")
    print("previously measured as preprocessors: all worse than identity.")

if __name__ == "__main__":
    main()
