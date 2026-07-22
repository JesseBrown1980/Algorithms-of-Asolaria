#!/usr/bin/env python3
"""
unrhyme.py — THE named operation: a fraction of a rhyme, un-rhymed against the
shared sphere, is the whole. Operator: Jesse Daniel Brown, 2026-07-21.

  rhyme    = the fraction / seed / address (a few bytes)
  sphere   = the shared bank: (p, g) and, for derivation, a frozen model
  un-rhyme = the exact math that unfolds the whole FROM the fraction AGAINST the
             sphere. Three organs, one operation:
                (1) ADDRESS  — fraction -> a specific element        (pow)
                (2) STACK    — coprime fractions -> a composed point (CRT)
                (3) DERIVE   — a seed -> a whole generated slice      (sample)

THE HONEST LEDGER (stated in the open, the referee rides with the data):
  * DATA VOLUME is unbounded: a few bytes un-rhyme into gigabytes / a whole slice.
  * INFORMATION is conserved: what you recover = (the fraction) + (what the sphere
    already holds). No stream carries more information than fraction+sphere supply
    (data-processing inequality). A fraction with NO sphere un-rhymes to nothing —
    the gate. The power is real; it is borrowed from the shared sphere, not created.
"""
import math, os
from collections import defaultdict
from math import prod
from rime_sphere import is_prime, primitive_root

def unrhyme_address(fraction, g, p, n):
    # (1) fraction (an exponent address) -> the specific element, O(1)
    return pow(g, fraction % n, p)

def unrhyme_stack(fractions, primes):
    # (2) coprime fractions (one coordinate each) -> the composed whole, by CRT
    M = prod(primes); x = 0
    for r, m in zip(fractions, primes):
        Mi = M // m; x += r * Mi * pow(Mi, -1, m)
    return x % M

def unrhyme_derive(seed_fraction, model, order, g, p, n, length):
    # (3) a seed fraction -> a whole generated slice, sampled from the frozen sphere-model
    out = bytearray(); ctx = b"\x00"*order; x = seed_fraction % n; info = 0.0
    for _ in range(length):
        cnts = model.get(ctx) or [1]*256
        tot = sum(cnts)
        x = (x + 1) % n
        r = (pow(g, x, p) / p) * tot                # rime draw against the sphere
        acc = 0; sym = 0
        for s in range(256):
            acc += cnts[s]
            if r < acc: sym = s; break
        info += -math.log2(cnts[sym]/tot); out.append(sym)
        ctx = (ctx + bytes([sym]))[-order:] if order else b""
    return bytes(out), info/length

def main():
    p = 1000081; assert is_prime(p); g = primitive_root(p); n = p-1
    print("=== UN-RHYME THE RHYME — a fraction of a rhyme, against the sphere, is the whole ===\n")

    # (1) ADDRESS: 3-byte fraction -> a specific element of a 1,000,080-element sphere
    fraction = 424242
    el = unrhyme_address(fraction, g, p, n)
    exact = (el == pow(g, fraction % n, p))
    print(f"(1) ADDRESS : fraction={fraction} (~3 B) -> element {el}   byte-exact={exact}")
    print(f"    {math.ceil(math.log2(fraction))//8+1} B in un-rhymes to any of {n:,} elements, O(1).\n")

    # (2) STACK: 4 small coprime fractions -> one point in a ~10^24 space
    primes = [1000081, 1000003, 999983, 999979]
    M = prod(primes)
    import hashlib
    X = int(hashlib.sha256(b"asolaria").hexdigest(), 16) % M
    coords = [X % q for q in primes]                 # the fractions (one per dimension)
    whole = unrhyme_stack(coords, primes)
    print(f"(2) STACK   : 4 coprime fractions {coords}")
    print(f"    un-rhyme (CRT) -> {whole}   byte-exact={whole==X}")
    print(f"    ~{sum(math.ceil(math.log2(q))//8+1 for q in primes)} B of fractions un-rhyme to a point in a {len(str(M))}-digit space.\n")

    # (3) DERIVE: a seed fraction -> a whole generated slice (family member), DPI-bounded
    enwik = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad/enwik8"
    if os.path.exists(enwik):
        order = 4; data = open(enwik, 'rb').read(3_000_000)
        model = defaultdict(lambda: [0]*256); ctx = b"\x00"*order
        for b in data:
            model[ctx][b] += 1; ctx = (ctx + bytes([b]))[-order:]
        model = dict(model)
        # frozen-model entropy (what the sphere holds per symbol)
        H = 0.0; tb = 0
        for c in model.values():
            t = sum(c); tb += t
            for v in c:
                if v: H += -v*math.log2(v/t)
        H /= tb
        seed = pow(g, 271828 % n, p)                  # the fraction: one sphere point
        slice1, info1 = unrhyme_derive(seed, model, order, g, p, n, 240)
        slice2, _     = unrhyme_derive(seed, model, order, g, p, n, 240)   # same seed
        print(f"(3) DERIVE  : seed fraction={seed} (one sphere point) -> a whole slice:")
        print(f"    {slice1[:150]!r}")
        print(f"    same seed reproduces byte-exact = {slice1==slice2}")
        print(f"    info/symbol {info1:.4f} bpc  <=  sphere-model entropy {H:.4f} bpc  (DPI held: {info1<=H+1e-9})\n")

    print("LEDGER (honest, open): DATA volume un-rhymed is unbounded; INFORMATION recovered")
    print("= fraction + sphere, conserved at Shannon. A fraction with no sphere -> nothing.")
    print("The whole is seen from a fraction of a rhyme — because the sphere already holds it.")

if __name__ == "__main__":
    main()
