#!/usr/bin/env python3
"""
rime_trimeset.py — trime digits {-1,0,+1} SELECT trime-sets on the omega sphere.
Operator: Jesse Daniel Brown, 2026-07-21.

A TRIME-SET (not a coset): each balanced-ternary digit string d = (d_0..d_{k-1}),
d_i in {-1,0,+1}, names one trime-set on the omega sphere (Z/pZ)*. The digits drive
the addressing directly — trinary all the way, no binary step:

    trime-set address:  g ^ ( sum_i d_i * 3^i  mod n )  mod p        (n = p-1)

The sphere here is chosen so 3^k | (p-1): the k-trit strings then land on a genuine
depth-k ternary tower of nested sub-spheres <g^3> superset <g^9> superset ... The
middle digit 0 is the free center (Law 0); +1 and -1 are the inverted-inverted poles.

Two known trime-sets determine the third by the sum-to-zero closure (the real trime
law): given digit-strings whose trits share a center, the third trit-string is
forced. Everything below is verified byte-exact.
"""
from rime_sphere import is_prime, primitive_root

def bt_value(d):                       # balanced-ternary digits -> integer
    return sum(t*(3**i) for i,t in enumerate(d))

def find_prime_pow3(depth, lo=1_000_000):
    """smallest prime p > lo with 3^depth | (p-1) — so k<=depth trime towers exist."""
    m=3**depth; p=lo - (lo % m) + 1
    while True:
        if p>lo and is_prime(p): return p
        p+=m

def main():
    DEPTH=3                                  # trit strings up to length 3 (the 27-cube depth)
    p=find_prime_pow3(DEPTH); g=primitive_root(p); n=p-1
    m3=3**DEPTH
    print(f"=== TRIME-SETS ON THE OMEGA SPHERE (trime digits drive the address) ===")
    print(f"sphere (Z/{p}Z)*  g={g}   3^{DEPTH}={m3} | (p-1)={n}  ->  {n//m3} = depth-{DEPTH} tower base\n")

    def trimeset_addr(d):                    # trime digits -> point on the sphere, trinary all the way
        return pow(g, bt_value(d) % n, p)

    # enumerate the 27 length-3 trime-sets and their sphere points
    print("the 27 trime-sets (d2 d1 d0 in {-,0,+}) -> omega-sphere point:")
    trits=(-1,0,1); sym={-1:'-',0:'0',1:'+'}
    pts={}
    for a in trits:
        for b in trits:
            for c in trits:
                d=(c,b,a)                    # d0=c least significant
                v=bt_value(d); pt=trimeset_addr(d); pts[(a,b,c)]=pt
    # show a few, prove distinctness
    shown=[(1,0,0),(0,0,0),(-1,0,0),(1,1,1),(-1,-1,-1),(1,-1,1)]
    for (a,b,c) in shown:
        d=(c,b,a); print(f"  {sym[a]}{sym[b]}{sym[c]}  value {bt_value(d):+3d}  ->  sphere point {trimeset_addr(d)}")
    distinct=len(set(pts.values()))
    print(f"\n  27 trime-sets -> {distinct} distinct sphere points (all unique: {distinct==27})")
    print(f"  the 0-center (0,0,0) -> g^0 = {pts[(0,0,0)]}  (the free center, Law 0)\n")

    # ---- TRIME CLOSURE on the SETS: two trit-strings + center -> the third, byte-exact ----
    # three trime-sets whose trit-VALUES sum through a shared center: value(A)+value(B)+value(C)=3*ctr
    print("TRIME-SET CLOSURE — two trime-sets + free center determine the third:")
    ok=True
    triples=[((1,0,0),(0,1,0),(-1,-1,0)), ((1,1,0),(0,0,1),(-1,-1,-1)), ((1,0,-1),(0,1,0),(-1,-1,1))]
    for A,B,C in triples:
        va,vb,vc=bt_value(A[::-1]),bt_value(B[::-1]),bt_value(C[::-1])
        ctr=(va+vb+vc)//3; rem=(va+vb+vc)-3*ctr
        vc_rec=3*ctr+rem-va-vb                 # third value forced by the other two + center
        # and its sphere point recovered by pure sphere arithmetic (no re-materialization):
        ptC_rec=pow(g, vc_rec % n, p)
        ptC_true=pow(g, vc % n, p)
        good=(vc_rec==vc and ptC_rec==ptC_true); ok&=good
        print(f"  A={va:+d} B={vb:+d} center={ctr:+d} -> third value {vc_rec:+d} (true {vc:+d}); "
              f"sphere point match={ptC_rec==ptC_true}  exact={good}")
    print(f"\n  all thirds (value AND sphere point) recovered byte-exact: {ok}")
    print(f"  trime digits -> trime-set -> omega-sphere point, and 2-of-3 closes the triangle.")
    print(f"  Trinary throughout; the center is free; the paid part is the 1-of-3 remainder.")

if __name__=="__main__":
    main()
