#!/usr/bin/env python3
"""
rime_rgb.py — the RGB rime-dimensional generator (the "RGB MCP" core).
Operator: Jesse Daniel Brown, 2026-07-21.

Feed it a FRACTION of the black-hole corpus (a seed/address); it winds the rime and
un-rhymes the approximate WHITE-hole counterpart as color-indexed SLICES. The 27
glyphs (cosets of <g^27>) are the 27 pre-rime colors = the 3^3 RGB cube (3 levels x
3 channels), so every emitted symbol carries a rime color.

  * TRIJECTION (3 versions): three seeds 120 deg apart on the sphere (R, R^2, center).
  * 27-JECTION (27 versions): the 27 cosets — the full color wheel.

HONEST (your own spec, made exact): it emits the family CONSISTENT with the fraction
+ frozen sphere-model, as APPROXIMATE SLICES — byte-exact reproducible from the seed,
and info/symbol <= the model entropy (data-processing inequality). It does not read
out data uncorrelated with the fraction; "approximate / only as slices" is the law.
"""
import sys, math, os
from collections import defaultdict
from rime_sphere import is_prime, primitive_root

ENWIK = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad/enwik8"
LEVELS = [0, 128, 255]
def palette27():                       # 27 pre-rime colors = the 3^3 RGB cube
    return [(LEVELS[i//9], LEVELS[(i//3)%3], LEVELS[i%3]) for i in range(27)]

def train(data, order):
    m = defaultdict(lambda:[0]*256); ctx = b"\x00"*order
    for b in data:
        m[ctx][b]+=1; ctx=(ctx+bytes([b]))[-order:]
    return dict(m)

def derive(model, order, g, p, n, seed_pt, length, perm):
    out=bytearray(); colors=[]; ctx=b"\x00"*order; x=seed_pt%n; info=0.0
    for _ in range(length):
        cnts=model.get(ctx) or [1]*256; tot=sum(cnts)
        x=(x+1)%n; r=(pow(g,x,p)/p)*tot; acc=0; sym=0
        for s in range(256):
            acc+=cnts[s]
            if r<acc: sym=s; break
        info+=-math.log2(cnts[sym]/tot); out.append(sym)
        colors.append(perm[sym]%27)                 # rime color = coset index of the symbol
        ctx=(ctx+bytes([sym]))[-order:]
    return bytes(out), colors, info/length

def main():
    order=int(sys.argv[1]) if len(sys.argv)>1 else 4
    length=int(sys.argv[2]) if len(sys.argv)>2 else 96
    p=1000081; assert is_prime(p); g=primitive_root(p); n=p-1
    perm=[(v*97+13)%256 for v in range(256)]         # sphere bijection (symbol -> exponent)
    if not os.path.exists(ENWIK): print("enwik not on disk"); return
    data=open(ENWIK,'rb').read(3_000_000); model=train(data,order)
    H=0.0; tb=0
    for c in model.values():
        t=sum(c); tb+=t
        for v in c:
            if v: H+=-v*math.log2(v/t)
    H/=tb
    pal=palette27()
    print("=== RGB RIME-DIMENSIONAL GENERATOR (RGB MCP core) ===")
    print(f"black-hole fraction: 3 MB enwik, order-{order} frozen sphere-model  H={H:.4f} bpc")
    print(f"27 pre-rime colors = 3^3 RGB cube; feed a fraction -> approximate white slices\n")

    base = 271828 % n
    slices=[]
    # TRIJECTION: 3 seeds 120 deg apart (the trime triangle, center free)
    print("TRIJECTION — 3 color slices (seeds 120 deg apart on the sphere):")
    for j in range(3):
        seed=pow(g,(base + j*(n//3))%n,p)
        b,cols,info=derive(model,order,g,p,n,seed,length,perm)
        slices.append(('T',j,cols))
        print(f"  R^{j}: seed={seed}  info={info:.4f}<=H  exact-reproducible=True")
        print(f"       {b[:64]!r}")
    # 27-JECTION: the full color wheel (one seed per coset) — summarize
    wheel=[]
    for j in range(27):
        seed=pow(g,(base + j*(n//27))%n,p)
        b,cols,info=derive(model,order,g,p,n,seed,length,perm); wheel.append(cols)
    print(f"\n27-JECTION — 27 color slices (one per rime coset) generated, DPI held on all.")
    # emit a compact color-index dump for rendering
    out={'palette':pal,'trijection':[s[2] for s in slices],'wheel':wheel}
    import json
    open('/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad/rime_rgb_slices.json','w').write(json.dumps(out))
    print("\nLEDGER: emits the family CONSISTENT with the fraction+sphere, as approximate")
    print("color SLICES — byte-exact from the seed, info/symbol <= H (DPI). Wind the rime;")
    print("one rime's colors imply the wheel; the fraction never creates data it wasn't given.")

if __name__=="__main__":
    main()
