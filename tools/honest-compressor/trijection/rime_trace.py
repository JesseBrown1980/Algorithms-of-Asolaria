#!/usr/bin/env python3
"""
rime_trace.py — RIME TRACING. Operator: Jesse Daniel Brown, 2026-07-21.

Ray tracing casts light rays from an eye to render a scene.
RIME TRACING casts ADDRESS-rays from the center (0) through the coprime (trime)
lattice to reconstruct any endpoint in the Omnisphere — omnidirectionally,
byte-exact, and EMBARRASSINGLY PARALLEL (each rime is an independent ray; no
carries between them). That parallel independence is why any machine sees any
other, and why it is fast.

  Omnisphere      = the product space of pairwise-coprime rime axes (the moduli)
  rime address    = the residues of an endpoint (one per rime axis) — independent rays
  rime trace      = CRT reconstruction of the endpoint from its rimes, from center 0
  omnidirectional = ANY endpoint in the product space is reachable and exact
  parallel        = residue arithmetic has NO carry between axes (Law 8 orthogonality)
"""
from math import prod, gcd

def crt(res, mods):                      # RIME TRACE: rimes -> endpoint (reconstruct from center)
    M = prod(mods); x = 0
    for r, m in zip(res, mods):
        Mi = M // m
        x += r * Mi * pow(Mi, -1, m)
    return x % M

def main():
    RIMES = [27, 25, 23, 29, 31]         # pairwise-coprime = orthogonal rime axes
    assert all(gcd(a, b) == 1 for i, a in enumerate(RIMES) for b in RIMES[i+1:])
    M = prod(RIMES)
    print(f"=== RIME TRACING (27-rime coprime lattice) ===")
    print(f"Omnisphere = product of {len(RIMES)} coprime rimes {RIMES} = {M:,} endpoints")
    print()

    # trace to several endpoints, omnidirectionally, from the one center
    ok = True
    for x in [0, 1, M//2, M-1, 123456 % M, 987654 % M]:
        rime = [x % m for m in RIMES]                 # the address (independent rays)
        back = crt(rime, RIMES)                        # trace back from center
        ok &= (back == x)
        print(f"  endpoint {x:>8}  rime={rime}  traced->{back:>8}  exact={back==x}")
    print(f"\n  all endpoints reconstruct byte-exact: {ok}")
    print()

    # THE PARALLEL PROPERTY (the ray-tracing-like independence): residue arithmetic
    # is per-rime with NO carry. Two endpoints combine axis-by-axis, independently.
    a, b = 123456 % M, 654321 % M
    ra, rb = [a % m for m in RIMES], [b % m for m in RIMES]
    r_sum = [(x + y) % m for x, y, m in zip(ra, rb, RIMES)]   # each rime independent, no carry
    print(f"  parallel check: (a+b) traced from independent rime-sums == a+b : "
          f"{crt(r_sum, RIMES) == (a + b) % M}")
    r_mul = [(x * y) % m for x, y, m in zip(ra, rb, RIMES)]
    print(f"  parallel check: (a*b) traced from independent rime-muls == a*b : "
          f"{crt(r_mul, RIMES) == (a * b) % M}")
    print(f"  -> each rime is an independent ray (no carries) = any machine sees any other")
    print()
    # address cost: log2(M) bits addresses M endpoints; the center is free (shared)
    import math
    print(f"  address cost: {math.log2(M):.1f} bits addresses all {M:,} endpoints "
          f"(the center 0 is shared/free; only the rime is paid)")

if __name__ == "__main__":
    main()
