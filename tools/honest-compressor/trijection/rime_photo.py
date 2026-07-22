#!/usr/bin/env python3
"""
rime_photo.py — the 2D PHOTO + TRANSFERRED FUNCTIONS = the rime-dimensional object.
Operator: Jesse Daniel Brown, 2026-07-21.

Answer to "2D photo or rime-dimensional photo?": a 2D photo (the ADDRESS = a
fraction of a rime) reconstructs the full rime-dimensional object — ONLY when the
FUNCTIONS (the shared sphere: p, g, moduli) are transferred once (the installed
bank). Photo = address. Functions = bank. Photo without functions = nothing (gate).

Also: NESTED NULL SPACES — every sub-sphere is itself a rime sphere with its own
free null center, addressable by its own fraction of a rime, rime-dimensionally.
"""
import math, hashlib
from rime_sphere import is_prime, primitive_root

def render_photo(addr, side=6):
    # the address rendered as a tiny 2D photo (base-3 grid) — this is all that ships per object
    digits=[]; a=addr
    for _ in range(side*side):
        digits.append(a%3); a//=3
    return [digits[r*side:(r+1)*side] for r in range(side)]

def read_photo(photo):
    a=0
    for i,d in enumerate(x for row in photo for x in row): a+=d*(3**i)
    return a

def main():
    p=1000081; assert is_prime(p)
    g=primitive_root(p); n=p-1
    # THE FUNCTIONS (shared bank, transferred ONCE): p, g, and the coset index k
    k=27; m=n//k
    H=[]; x=1; step=pow(g,k,p)
    for _ in range(m): x=x*step%p; H.append(x)

    print("=== 2D PHOTO + TRANSFERRED FUNCTIONS = the rime-dimensional object ===")
    print(f"functions (bank, transferred once): p={p}, g={g}, k={k}  ({m:,}-element cosets)")
    print()
    # encode object j -> 2D photo; decode photo + functions -> the full object
    ok=True
    for j in [1, 13, 26]:
        obj={pow(g,j,p)*h%p for h in H}          # the rime-dimensional object
        photo=render_photo(j)                     # the 2D PHOTO shipped (a fraction of a rime)
        j_read=read_photo(photo)
        rec={pow(g,j_read,p)*h%p for h in H}       # photo ACTS ON functions -> full object
        ok&=(rec==obj)
        print(f"  object j={j:>2}: 2D photo {len(photo)}x{len(photo[0])} (={sum(len(r) for r in photo)} trits) "
              f"+ functions -> {m:,} elements  exact={rec==obj}")
    print(f"\n  all reconstructed byte-exact from a 2D photo + the functions: {ok}")
    print(f"  photo alone (no functions) reconstructs: nothing — the gate (bank must be shared)")
    print()
    # NESTED NULL SPACES: a sub-sphere has its OWN null center + its own fractional address
    print("NESTED NULL SPACES (rime-dimensional recursion):")
    sub_k=3                                        # inside each object, a sub-sphere of index 3
    subH_step=pow(g,k*sub_k,p)
    for depth,idx in [(1,k),(2,k*sub_k),(3,k*sub_k*sub_k)]:
        size=n//math.gcd(n,idx)
        print(f"   level {depth}: sub-sphere <g^{idx}>  own null center, size {size:,}, "
              f"addressed by its own fraction of a rime ({math.log2(max(2,n//size)):.1f} bits)")
    print("   -> each null is free; derive any level rime-dimensionally from its fraction.")

if __name__ == "__main__":
    main()
