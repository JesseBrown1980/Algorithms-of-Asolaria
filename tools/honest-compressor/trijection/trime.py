#!/usr/bin/env python3
"""
trime.py — TRIME NUMBERS + trilateral time + "any machine sees any other" (CRT).
Operator: Jesse Daniel Brown, 2026-07-21. Reproducible for the federation.

Three results, all measured:
  A) TIME IS TRILATERAL: the centered 3-point (past-present-future, 2nd difference)
     beats the 2-point bijection (1st difference) on the played series.
  B) TRIME NUMBERS: in the 27-cube (mod 27), primes occupy exactly the phi(27)=18
     COPRIME cells and never the 9 center-aligned cells; 3 is the unique center-prime.
  C) ANY MACHINE SEES ANY OTHER = Chinese Remainder Theorem: coprime (=orthogonal,
     Law 8) residue-machines reconstruct any number; the address space is the PRODUCT.
"""
import numpy as np
from nested_cascade import H_bits

def sieve(n):
    s = np.ones(n+1, bool); s[:2] = False
    for i in range(2, int(n**0.5)+1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

def test_time():
    C, T = 27, 1458; t = np.arange(T)
    center = 128 + 60*np.sin(t*0.01)
    chans = np.stack([np.clip(np.round(center + 28*np.sin(2*np.pi*(c+1)*t/T)
                      + ((t*(7+2*c)) % 5 - 2)), 0, 255) for c in range(C)]).astype(np.int64)
    tot = lambda fn: sum(H_bits(fn(chans[c])) for c in range(C)); N = chans.size
    raw = tot(lambda x: x)
    d1 = tot(lambda x: np.diff(x, prepend=x[0]))
    d2 = tot(lambda x: np.diff(x, n=2, prepend=x[0], append=x[-1]))
    print("A) TIME: bijection (2pt) vs TRILATERAL (3pt centered)")
    print(f"   raw {raw/N:.4f}  bijection {d1/N:.4f} ({raw/d1:.2f}x)  "
          f"TRILATERAL {d2/N:.4f} ({raw/d2:.2f}x)  {'-> trilateral WINS' if d2<d1 else ''}")

def test_trime():
    P = sieve(200000)
    m3 = np.bincount(P % 3, minlength=3)
    coprime = [r for r in range(27) if np.gcd(r, 27) == 1]
    m27 = np.bincount(P % 27, minlength=27)
    only_coprime = all(m27[r] == 0 for r in range(27) if r % 3 == 0 and r != 3)
    print("B) TRIME NUMBERS (primes in the 27-cube)")
    print(f"   primes mod 3: center r0={m3[0]} (only the prime 3), r1={m3[1]}, r2={m3[2]}")
    print(f"   phi(27)={len(coprime)} coprime cells hold all primes>3: {coprime}")
    print(f"   center-aligned cells (multiples of 3) prime-free except 3: {only_coprime}")

def test_crt():
    # three coprime machines; each holds one residue; together they reconstruct any x < product
    mods = [27, 25, 23]                      # pairwise coprime (3^3, 5^2, 23)
    prod = int(np.prod(mods))
    x = 12345 % prod
    res = [x % m for m in mods]             # what each machine "sees"
    # reconstruct by CRT
    def crt(res, mods):
        from math import prod as _p
        M = _p(mods); acc = 0
        for r, m in zip(res, mods):
            Mi = M // m; inv = pow(Mi, -1, m); acc += r * Mi * inv
        return acc % M
    back = crt(res, mods)
    print("C) ANY MACHINE SEES ANY OTHER (CRT)")
    print(f"   moduli {mods} (coprime=orthogonal); address space = product = {prod:,}")
    print(f"   x={x} seen as residues {res} -> reconstructed {back}  exact={back==x}")
    print(f"   3 coprime machines jointly address {prod:,} values (they COMPOUND — Law 8)")

if __name__ == "__main__":
    print("=== TRIME NUMBERS · TRILATERAL TIME · ANY-MACHINE-SEES-ANY-OTHER ===")
    test_time(); test_trime(); test_crt()
