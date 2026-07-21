#!/usr/bin/env python3
"""
rime_prism.py — THE RIME PRISM: a 3->9->27 nested, integer, byte-exact spectral
split over the rime sphere. Operator: Jesse Daniel Brown, 2026-07-21.

Newton used TWO prisms (split white light, recombine to white) — a 1-D transform
and its inverse; reversible. The RIME PRISM generalizes to 27 coordinates: a radix-3
Number-Theoretic Transform using a primitive 27th root of unity w = g^((p-1)/27) on
the sphere (Z/pZ)*. Nesting thirds 3->9->27 (Cooley-Tukey radix 3; 1+w+w^2=0).

Each of the 27 outputs is a RIME GLYPH — one spectral coordinate ("rime gradient")
of the whole signal. The transform is LOSSLESS and REVERSIBLE to the byte (integer;
no float), so it is RATE 1.0: it re-addresses the same information into 27 rime
coordinates. A glyph is ONE coordinate; the full 27 (or, for generated structure,
the seed) reconstruct the whole. More prisms = finer decomposition, not more info.
"""
from rime_sphere import is_prime, primitive_root

def ntt(x, w, p):
    N=len(x); return [sum(x[j]*pow(w,(j*k)%N,p) for j in range(N))%p for k in range(N)]
def intt(X, w, p):
    N=len(X); wi=pow(w,-1,p); Ninv=pow(N,-1,p)
    return [(Ninv*sum(X[k]*pow(wi,(j*k)%N,p) for k in range(N)))%p for j in range(N)]

def main():
    p=1000081; assert is_prime(p); g=primitive_root(p); n=p-1; N=27
    assert n%N==0, "need 27 | (p-1) for a 27th root"
    w=pow(g,n//N,p)                                   # primitive 27th root of unity on the sphere
    assert pow(w,N,p)==1 and pow(w,9,p)!=1 and pow(w,3,p)!=1
    print("=== THE RIME PRISM (3->9->27 NTT over the rime sphere; integer, byte-exact) ===")
    print(f"sphere (Z/{p}Z)*  g={g}   primitive 27th root w=g^{n//N} mod p = {w}")
    print(f"radix-3 nested: 27 = 3^3   (Newton: 2 prisms 1-D; rime: 27 coordinates)\n")

    # roots-of-unity identity (the trime/trianti closure): sum of all 27 powers = 0
    s=sum(pow(w,k,p) for k in range(N))%p
    print(f"  1 + w + w^2 + ... + w^26  (mod p) = {s}   (roots-of-unity closure, like 1+w+w^2=0)")

    # PRISM a real signal: 27 bytes of enwik -> 27 rime-glyph coordinates -> recombine
    import os
    path="/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad/enwik8"
    sig=list(open(path,'rb').read(27)) if os.path.exists(path) else [ (i*i+7)%251 for i in range(27) ]
    X=ntt(sig,w,p)                                     # split into 27 glyphs (rime gradients)
    rec=intt(X,w,p)                                    # recombine (the second prism, rewound)
    exact = (rec==sig)
    print(f"\n  signal (27 bytes)      : {sig}")
    print(f"  27 rime glyphs (coords): {X[:6]} ... (27 spectral coordinates)")
    print(f"  DC / center glyph X[0]  = {X[0]}  =  sum(signal) mod p = {sum(sig)%p}  (the FREE CENTER, Law 0)")
    print(f"  recombined (inverse)    : {rec}")
    print(f"  BYTE-EXACT round-trip   : {exact}   (lossless, reversible -> RATE 1.0)")
    print(f"\n  Each glyph is ONE rime gradient of the whole; the 27 together are the whole,")
    print(f"  re-addressed, information conserved. Any rime glyph can carry a gradient of the")
    print(f"  signal — but one glyph is one coordinate, not the whole universe (the gate).")

if __name__=="__main__":
    main()
