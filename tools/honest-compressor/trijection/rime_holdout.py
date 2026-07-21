#!/usr/bin/env python3
"""
rime_holdout.py — the DIRECT test of "a fraction predicts everything".
Train on a FRACTION; then try to reproduce an UNSEEN part byte-exact from a small
reference. Pre-registered prediction: prediction is good, EXACT reproduction costs
the unseen part's entropy; a tiny seed cannot pin it. Let the bytes referee.
"""
import os, math
from collections import defaultdict
E="/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad/enwik8"
def train(data,order):
    m=defaultdict(lambda:[0]*256); ctx=b"\x00"*order
    for b in data: m[ctx][b]+=1; ctx=(ctx+bytes([b]))[-order:]
    return dict(m)
def main():
    order=4; data=open(E,'rb').read(6_000_000)
    known=data[:2_000_000]                  # the FRACTION we train on
    unseen=data[5_000_000:5_003_000]        # 3000 bytes the model has NEVER seen
    model=train(known,order)
    # bits to reproduce the UNSEEN part EXACTLY under the model = the residual you must store
    ctx=b"\x00"*order; bits=0.0; correct=0
    for b in unseen:
        cnts=model.get(ctx) or [1]*256; tot=sum(cnts)
        p=(cnts[b]+1)/(tot+256); bits+=-math.log2(p)
        if cnts and cnts[b]==max(cnts): correct+=1   # would top-1 prediction have been right?
        ctx=(ctx+bytes([b]))[-order:]
    bpc=bits/len(unseen)
    print("=== 'A FRACTION PREDICTS EVERYTHING' — direct test on UNSEEN Wikipedia ===")
    print(f"trained on: {len(known):,} B (a fraction)   |   test: {len(unseen):,} UNSEEN bytes\n")
    print(f"PRE-REGISTERED: prediction good, but EXACT reproduction costs ~entropy (~1.8 bpc),")
    print(f"                and a tiny seed cannot pin the exact unseen bytes.\n")
    print(f"MEASURED:")
    print(f"  top-1 prediction correct on unseen : {correct/len(unseen)*100:.1f}% of bytes  (the model DOES predict well)")
    print(f"  bits to reproduce unseen EXACTLY   : {bits:,.0f} bits = {bits/8:,.0f} B   ({bpc:.4f} bpc)")
    print(f"  a 'fraction of a rhyme' seed is     : ~4 bytes")
    print(f"  4 bytes can address at most         : 2^32 outcomes; the unseen chunk is 1 of 2^{len(unseen)*8:,}")
    print(f"\nVERDICT: the model predicts the unseen text well (~{correct/len(unseen)*100:.0f}%), which LOWERS the")
    print(f"  cost — but to get it back EXACTLY you must still store {bits/8:,.0f} B of residual")
    print(f"  ({bpc:.2f} bpc). That residual IS the information the fraction did not contain.")
    print(f"  A 4-byte seed indexes 2^32 things; the exact unseen chunk is one of 2^{len(unseen)*8:,}.")
    print(f"  Prediction: yes. Exact reproduction from a fraction: no — by the count itself.")
if __name__=="__main__": main()
