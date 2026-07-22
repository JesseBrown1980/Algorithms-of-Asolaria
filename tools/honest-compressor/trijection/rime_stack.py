import math
from math import prod
# The honest stacking calculation: fractions multiply DOWN as dimensions stack.
primes=[1000081,1000003,999983,999979,999961,999959]
print("d | frozen B | address space (elements)          | 1/27^d (fraction of a rime) | bits/element (amortized)")
M=1
for d in range(1,7):
    M=prod(primes[:d])
    frozen_bits = d*24*8                     # 24 B per dimension
    space_bits  = math.log2(M)               # bits to name one composed point
    frac = 1/(27**d)                          # the selecting fraction: 1 of 27^d glyph-slots
    bpe = frozen_bits/M                        # amortized bits per addressed element (goes ->0)
    print(f"{d} | {d*24:7d}  | {M:>30,d} | {frac:.12f}  = 1/{27**d:<12d} | {bpe:.3e}")
print()
print("fraction shrinks x1/27 each stack:", " -> ".join(f"1/{27**d}" for d in range(1,7)))
print("as decimals:", " -> ".join(f"{1/27**d:.2e}" for d in range(1,7)))
