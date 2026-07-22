#!/usr/bin/env python3
"""
rime_creation_tower.py — THE LAST LEVEL OF THE RIME CREATION.
Operator: Jesse Daniel Brown, 2026-07-22.

The tower, exactly as spoken:  256  ->  x3  ->  x27  ->  rime sphere.

  level 0: 256          = 2^8        the byte (binary world, imported whole)
  level 1: 256 x 3      = 768        one trime of bytes  (-,0,+ each a full byte-space)
  level 2: 768 x 27     = 20736      one rime dimension of trimes of bytes
  level 3: the rime sphere           a prime p with 20736 | p-1, so the WHOLE tower
                                     sits inside (Z/pZ)* as an exact chain of
                                     nested subgroups:  H_256 < H_768 < H_20736 < sphere

This is the NESTED answer (subgroup tower), the one the CRT answer (729 x 1024,
coprime axes) does not give: here every level is INSIDE the next, and one
generator g reaches all of them (w_L = g^((p-1)/L) generates exactly level L).
Constructive smoothness (Law 14 inverted): we CHOOSE p so the tower divides p-1.

Address = (byte b, trime t, glyph d)  ->  k = b + 256*t + 768*d  in 0..20735
        ->  point = w^k on the sphere. Inverted byte-exact by the Fischer.

HONEST GATES: this is the ADDRESSING axis (~0 bpc over generated structure,
Law 6/15) — a relabeling tower, rate 1.0, no compression claimed. The cofactor
(p-1)/20736 is the part of the sphere the tower does NOT reach — named, not hidden.
"""
from rime_sphere import is_prime, primitive_root

TOWER = [256, 768, 20736]                       # 256 -> x3 -> x27

def main():
    print("=== THE RIME CREATION TOWER: 256 -> x3 -> x27 -> rime sphere ===\n")
    print(f"  256 x 3  = {256*3}     (one trime of bytes: -,0,+ each holding a byte-space)")
    print(f"  768 x 27 = {768*27}   (one rime dimension of trimes of bytes)")
    print(f"  20736    = 2^8 * 3^4 = 12^4   (the binary byte and the trime tower, fused)\n")

    # find the smallest prime p == 1 (mod 20736): the sphere the tower fits inside
    n = 20736; k = 1
    while not is_prime(n * k + 1): k += 1
    p = n * k + 1
    g = primitive_root(p)
    print(f"  candidate 20737 = 89 x 233  — NOT prime (and both factors are Fibonacci; a smile, not a law)")
    print(f"  the sphere: smallest prime p = {n}*{k}+1 = {p}   g = {g}")
    print(f"  cofactor (p-1)/20736 = {k}   <- the part of the sphere the tower does not reach (named)\n")

    # nested subgroup chain: one generator reaches every level
    w = {L: pow(g, (p - 1) // L, p) for L in TOWER}
    for L in TOWER:
        # w[L] has exact order L; each level's generator is a power of the next level's
        assert pow(w[L], L, p) == 1 and pow(w[L], L // 2 if L % 2 == 0 else 1, p) != 1
    assert pow(w[768], 3, p) == w[256]           # byte level = cube of trime level
    assert pow(w[20736], 27, p) == w[768]        # trime level = 27th power of rime level
    print("  nested chain verified:  H_256 < H_768 < H_20736 < (Z/pZ)*")
    print("    w768^3 = w256   (the trime level folds 3-to-1 onto the byte level)")
    print("    w20736^27 = w768 (the rime level folds 27-to-1 onto the trime level)\n")

    # address (byte, trime, glyph) -> sphere point -> back, byte-exact
    W = w[20736]
    table = {}                                   # the frozen Fischer for this level
    x = 1
    for e in range(20736):
        table[x] = e; x = x * W % p
    ok = True
    demo = [(0, 0, 0), (255, 2, 26), (77, 1, 13), (42, 0, 22), (128, 2, 4)]
    for (b, t, d) in demo:
        kk = b + 256 * t + 768 * d
        pt = pow(W, kk, p)
        e = table[pt]
        ok &= (e % 256, (e // 256) % 3, e // 768) == (b, t, d)
    print(f"  address (byte, trime, glyph) -> point -> Fischer -> back: byte-exact = {ok}")
    print(f"  {len(demo)} demo addresses of 20,736; every level readable from one exponent:")
    print(f"    k mod 256 = the byte | (k/256) mod 3 = the trime | k/768 = the glyph\n")

    print("VERDICT (honest): the tower is real and nested — one sphere, one generator,")
    print("four levels, each folding exactly onto the one below; byte-exact addressing")
    print("of GENERATED structure (~0 bpc, Law 6/15). It relabels; it does not compress.")

if __name__ == "__main__":
    main()
