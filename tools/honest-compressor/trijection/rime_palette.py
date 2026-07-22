#!/usr/bin/env python3
"""
rime_palette.py — THE RIME PALETTE FILES (red / green / blue) with rime references.
Operator: Jesse Daniel Brown, 2026-07-21.

Builds the three color rooms on the hard drive as RIME REFERENCES (Law 15: the file
holds the FRACTION — p, g, seed, order, length, sha — never the content; the slice
is derived on demand and verified byte-exact). Then the trijection closure:

    CENTER room = R + G + B (the grand center, Law 0 — the free center).
    ANY TWO colors + the center recover the THIRD, byte-exact.

That is "any two of the three points derive the third" made physical on disk —
honest erasure-closure (parity), measured, no magic: 2-of-3 + center = whole.
"""
import os, json, math, hashlib
from collections import defaultdict
from rime_sphere import is_prime, primitive_root

ROOM="/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad/palette_room"
ENWIK="/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad/enwik8"
LEN=2000; ORDER=4

def train(data, order):
    m=defaultdict(lambda:[0]*256); ctx=b"\x00"*order
    for b in data: m[ctx][b]+=1; ctx=(ctx+bytes([b]))[-order:]
    return dict(m)

def derive(model, order, g, p, n, seed, length):
    out=bytearray(); ctx=b"\x00"*order; x=seed%n
    for _ in range(length):
        cnts=model.get(ctx) or [1]*256; tot=sum(cnts)
        x=(x+1)%n; r=(pow(g,x,p)/p)*tot; acc=0; sym=0
        for s in range(256):
            acc+=cnts[s]
            if r<acc: sym=s; break
        out.append(sym); ctx=(ctx+bytes([sym]))[-order:]
    return bytes(out)

def main():
    p=1000081; assert is_prime(p); g=primitive_root(p); n=p-1
    os.makedirs(ROOM, exist_ok=True)
    data=open(ENWIK,'rb').read(3_000_000); model=train(data,ORDER)
    base=271828%n
    seeds={'red':pow(g,base%n,p), 'green':pow(g,(base+n//3)%n,p), 'blue':pow(g,(base+2*(n//3))%n,p)}

    print("=== RIME PALETTE FILES (red/green/blue) — references on disk, derived on demand ===\n")
    streams={}
    for color,seed in seeds.items():
        s=derive(model,ORDER,g,p,n,seed,LEN); streams[color]=s
        ref={'color':color,'p':p,'g':g,'seed':seed,'order':ORDER,'length':LEN,
             'sha256':hashlib.sha256(s).hexdigest()}
        path=os.path.join(ROOM,f"palette_{color}.rime")
        json.dump(ref,open(path,'w'))
        print(f"  {color:5s}: reference file {os.path.getsize(path):3d} B  addresses a {LEN:,}-B slice  "
              f"sha={ref['sha256'][:16]}…")

    # PLAY the references back (Law 15): re-derive from the file alone, verify byte-exact
    print("\nPLAY (address on demand from the reference files only):")
    allok=True
    for color in seeds:
        ref=json.load(open(os.path.join(ROOM,f"palette_{color}.rime")))
        s2=derive(model,ref['order'],ref['g'],ref['p'],ref['p']-1,ref['seed'],ref['length'])
        ok=hashlib.sha256(s2).hexdigest()==ref['sha256']; allok&=ok
        print(f"  {color:5s}: re-derived from {os.path.getsize(os.path.join(ROOM,f'palette_{color}.rime'))} B reference -> byte-exact={ok}")

    # CENTER room (the grand center, Law 0) + trijection closure: any 2 + center -> the 3rd
    center=bytes((streams['red'][i]+streams['green'][i]+streams['blue'][i])%256 for i in range(LEN))
    open(os.path.join(ROOM,"palette_center.room"),'wb').write(center)
    print(f"\nCENTER room written: {LEN:,} B  (R+G+B mod 256 — the free center)")
    print("TRIJECTION CLOSURE — delete any one color; recover it from the other two + center:")
    for lost in ('red','green','blue'):
        others=[c for c in seeds if c!=lost]
        rec=bytes((center[i]-streams[others[0]][i]-streams[others[1]][i])%256 for i in range(LEN))
        ok=(rec==streams[lost])
        print(f"  lost {lost:5s} -> recovered from {others[0]}+{others[1]}+center: byte-exact={ok}")

    print(f"\nHONEST LEDGER: each palette file is a FRACTION ({os.path.getsize(os.path.join(ROOM,'palette_red.rime'))} B) that addresses its")
    print(f"slice against the shared bank (the frozen model) — Law 15. The center is the")
    print(f"grand center (Law 0); any two colors + center determine the third — the")
    print(f"trijection closure, physical on disk. 2-of-3 recovery is parity (erasure code):")
    print(f"real, byte-exact, and information-conserving (the center room paid for it).")

if __name__=="__main__":
    main()
