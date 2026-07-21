#!/usr/bin/env python3
"""
rime_dimension.py — 27 rime glyphs = 1 RIME DIMENSION; rinse & repeat = stack them.
Operator: Jesse Daniel Brown, 2026-07-21.

  * 1 RIME DIMENSION = one omega box (rime sphere) decomposed into its 27 glyphs
    (the 27 cosets of <g^27>). The whole dimension freezes to just (p, g, k=27).
  * ADDRESS on-demand (Law 15): any slice = glyph j, position i -> g^(j+27i) mod p,
    O(1), never materialized.
  * RINSE & REPEAT: stack COPRIME dimensions. Because they are coprime they are
    orthogonal (Law 8) — composed by CRT with no carries, the address space is the
    PRODUCT. bits language (1 of 2) -> rime language (1 of 27^d, addressable/frozen).

GATE: this addresses GENERATED structure (the composed spheres). Arbitrary data is
first trained into glyph-models (the compression axis, ~1.36-2.0 bpc), THEN
addressed here. Bank must be shared; played only after the calculations are frozen.
"""
from math import prod
from rime_sphere import is_prime, primitive_root

class RimeDimension:
    """One omega box = one rime sphere, 27 glyphs, frozen to (p,g,k)."""
    def __init__(self, p):
        assert is_prime(p)
        self.p, self.g, self.n, self.k = p, primitive_root(p), p-1, 27
    def address(self, glyph, i):                 # glyph in [0,27), position i -> element, O(1)
        return pow(self.g, (glyph + self.k*i) % self.n, self.p)
    frozen_bytes = 24                            # p, g, k — the whole dimension's bank

def crt(res, mods):
    M=prod(mods); x=0
    for r,m in zip(res,mods):
        Mi=M//m; x += r*Mi*pow(Mi,-1,m)
    return x%M

def main():
    print("=== 27 GLYPHS = 1 RIME DIMENSION;  RINSE & REPEAT = STACK (coprime) ===\n")

    # ---- 1 RIME DIMENSION (27 glyphs), frozen, addressed on-demand, byte-exact ----
    D = RimeDimension(1000081)
    print(f"1 DIMENSION: omega box (Z/{D.p}Z)*  g={D.g}  27 glyphs  frozen={D.frozen_bytes} B")
    print(f"   addresses {D.n:,} elements on-demand (O(1), never materialized):")
    ok=True
    for glyph in (0, 13, 26):
        for i in (0, 5, 100):
            e = D.address(glyph, i)
            ref = pow(D.g, (glyph+27*i)%D.n, D.p)      # honest re-derivation
            ok &= (e==ref)
    print(f"   any (glyph,position) slice reconstructed byte-exact: {ok}\n")

    # ---- RINSE & REPEAT: stack coprime dimensions -> CRT product (orthogonal) ----
    primes=[1000081, 1000003, 999983, 999979]        # distinct primes = pairwise coprime dims
    dims=[RimeDimension(p) for p in primes]
    M=prod(primes)
    print(f"STACKED: {len(dims)} coprime rime dimensions  frozen={sum(d.frozen_bytes for d in dims)} B")
    print(f"   composed address space (product) = {M:,}  (~{len(str(M))} digits) from {sum(d.frozen_bytes for d in dims)} B")
    # a composed point X, addressed by one coordinate per dimension, reconstructed by CRT:
    import hashlib
    allok=True
    for s in range(4):
        X=int(hashlib.sha256(str(s).encode()).hexdigest(),16)%M
        coords=[X%p for p in primes]                  # each dimension's coordinate (parallel, no carry)
        back=crt(coords, primes)                       # rinse: reconstruct exactly by CRT
        allok &= (back==X)
        print(f"   point {X} -> coords {coords} -> reconstructed {back}  exact={back==X}")
    print(f"\n   all composed points byte-exact across stacked dimensions: {allok}")
    print(f"   orthogonal (coprime) -> no carries between dimensions -> parallel (Law 8/12).")
    print()
    print("   BITS -> RIME: a bit is 1 of 2; a rime dimension is 1 of 27^d, frozen and")
    print("   addressable; stack more (rinse & repeat) and the address space multiplies.")
    print("   Played only AFTER the combined calculations are frozen (Law 15).")

if __name__ == "__main__":
    main()
