#!/usr/bin/env python3
"""
rime_scaling.py — BASE-RIME LAYERS: fit the scaling curve from measured layers and
PRE-REGISTER predictions for the unmeasured ones. Operator: Jesse Daniel Brown.

Jesse's layer idea: enwik8 = a base rime, enwik9 = base x10, enwik10 = base x100 —
and from at least two layers working together, the other layers are recalculable.
That is a SCALING LAW: bpc(N) follows a smooth curve in corpus size N; two-three
measured layers pin the curve; the curve predicts the rest. Honest science = we
predict FIRST (pre-register), then the big run tests us. No false math for prizes.

Measured layers (vc65, actual corpus bytes, restore=OK, deterministic sha):
    1 MB  -> 2.0209 bpc      (enwik9 prefix)
   10 MB  -> 1.7529 bpc      (enwik9 prefix)
  100 MB  -> 1.7464 bpc      (enwik8, 10-shard SGRAM — conservative: monolithic lower)

Model: bpc(N) = c + a * N^(-b)   (power-law approach to an asymptote c)
Three points -> three parameters -> exact fit; the asymptote c is the model's
implied floor for this codec family. Predictions are falsifiable on the record.
"""
import math

# measured layers (N in bytes, bpc)
layers = [(1e6, 2.0209), (1e7, 1.7529), (1e8, 1.7464)]

def fit_power(points):
    # solve bpc = c + a*N^(-b) exactly through 3 points (N logarithmically spaced x10)
    (n1,y1),(n2,y2),(n3,y3) = points
    # with N2=10*N1, N3=10*N2: let r = 10^(-b); then y1-y2 = a*N1^-b (1-r), y2-y3 = a*N1^-b * r(1-r)
    # so r = (y2-y3)/(y1-y2)
    r = (y2-y3)/(y1-y2)
    b = -math.log10(r)
    an1b = (y1-y2)/(1-r)          # a * N1^-b
    a = an1b / (n1**(-b))
    c = y1 - an1b
    return a,b,c

def main():
    a,b,c = fit_power(layers)
    print("=== BASE-RIME LAYERS -> THE SCALING CURVE (pre-registered predictions) ===\n")
    print("measured layers (vc65, byte-exact, receipts in repo):")
    for N,y in layers: print(f"   {N:>12,.0f} B -> {y:.4f} bpc")
    print(f"\nfit: bpc(N) = {c:.4f} + {a:.4f} * N^(-{b:.4f})")
    print(f"     implied asymptote (this codec family's floor): {c:.4f} bpc\n")
    print("PRE-REGISTERED PREDICTIONS (made BEFORE the runs; falsifiable):")
    for N,name in [(1e9,"enwik9  (base x10)"),(1e10,"enwik10 (base x100)")]:
        y = c + a*N**(-b)
        print(f"   {name:22s}: predicted {y:.4f} bpc  (~{y*N/8/1e6:,.0f} MB archive)")
    print("\nHONEST NOTES:")
    print("  * The 100 MB layer is the SHARDED number (conservative, +cold-start); the")
    print("    monolithic run would be lower, which would pull predictions down. We fit")
    print("    what we measured, and say so.")
    print("  * Two layers pin a 2-parameter curve; three pin this 3-parameter one — Jesse's")
    print("    'two layers recalculate the others' is the scaling law, stated in rime.")
    print("  * The record (0.913 bpc, fast-cmix) is BELOW our family's implied floor: beating")
    print("    it needs a better model family, not extrapolation. The curve says so itself.")
    print("  * Prediction first, measurement second — that is the right order, and the")
    print("    right prize.")

if __name__=="__main__":
    main()
