#!/usr/bin/env python3
"""
rime_cm.py — a REAL context-mixing predictor (mini-PAQ), the honest path toward
the frontier below the order-k wall. Operator: Jesse Daniel Brown, 2026-07-22.

Bit-level. Several order-k byte-context models + a match model, combined by an
adaptive logistic mixer (context-selected weights). Reports cross-entropy bpc =
the size a matched arithmetic coder achieves. Integer count tables (fixed-size
hashed), deterministic. This is the technique that crosses order-k plateaus; it
does NOT ride waves (waves are rate-1.0 addressing) — it PREDICTS better.

Honest: below-1 bpc is the Hutter frontier (SOTA ensembles, huge). This measures
how far a compact honest CM gets, with a real receipt. Never below Shannon.

usage: rime_cm.py <nbytes> [orders csv]
"""
import sys, time, json, math
from array import array

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
CORPUS = f"{S}/enwik9"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
ORDERS = [int(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1,2,3,4,6]

data = open(CORPUS, 'rb').read(N)

# stretch/squash tables (fixed-point domain [-2047,2047] <-> prob)
SQ = array('H', [0]*4096)
for i in range(4096):
    x = (i-2048)/256.0
    SQ[i] = min(4095, max(1, int(4096/(1+math.exp(-x)))))
def squash(x):
    x = 2047 if x > 2047 else (-2047 if x < -2047 else x)
    return SQ[int(x)+2048]
ST = array('h', [0]*4096)
for p in range(1,4096):
    ST[p] = int(round(256*math.log(p/(4096-p))))
ST[0] = ST[1]

TBITS = 22; TSIZE = 1 << TBITS; TMASK = TSIZE-1
# each model: count table, 2 bytes per node (n0,n1)
tabs = [bytearray(2*TSIZE) for _ in ORDERS]
# match model
MHBITS = 22; MH = 1 << MHBITS; MHMASK = MH-1
matchpos = array('i', [-1])*0
matchtab = array('i', [-1]*MH)

wordtab = bytearray(2*TSIZE)     # word-context model (rolling hash of current alnum run)
# mixer: weights[selctx][model], selctx small
NM = len(ORDERS) + 2     # + match model + word model
NSEL = 256*8             # selected by order-0 byte high bits + bit position-ish
W = array('f', [0.3]*(NSEL*NM))
LR = 0.0009

def run():
    t0 = time.time()
    hist = data
    o_hash = [0]*len(ORDERS)
    bitctx = 1
    c0 = 0                    # partial current byte (with leading 1)
    loss = 0.0
    mlen = 0; mptr = -1
    wordhash = 0
    for i in range(len(hist)):
        # word context: rolling hash of the current run of letters/digits
        prevb = hist[i-1] if i > 0 else 0
        if (65 <= prevb <= 90) or (97 <= prevb <= 122) or (48 <= prevb <= 57):
            wordhash = (wordhash*0x9E3779B1 + prevb + 1) & 0xFFFFFFFF
        else:
            wordhash = 0
        # per-byte: compute order context hashes from preceding bytes
        for oi, k in enumerate(ORDERS):
            h = 0
            for j in range(1, k+1):
                if i-j >= 0: h = (h*0x9E3779B1 + hist[i-j] + 1) & 0xFFFFFFFF
            o_hash[oi] = h
        # match model: predicted byte from current match pointer
        pred_byte = hist[mptr] if (0 <= mptr < i) else -1
        bitctx = 1; c0 = 1
        for bp in range(8):
            # gather model predictions (fixed point stretch)
            sts = []
            idxs = []
            for oi in range(len(ORDERS)):
                idx = ((o_hash[oi]*0x2545F491 + c0) & TMASK)
                idxs.append(idx)
                n0 = tabs[oi][2*idx]; n1 = tabs[oi][2*idx+1]
                p = int(4096*(n1+0.4)/(n0+n1+0.8))
                p = 1 if p < 1 else (4095 if p > 4095 else p)
                sts.append(ST[p])
            # word-context count model
            widx = ((wordhash*0x2545F491 + c0) & TMASK)
            wn0 = wordtab[2*widx]; wn1 = wordtab[2*widx+1]
            wp = int(4096*(wn1+0.4)/(wn0+wn1+0.8)); wp = 1 if wp<1 else (4095 if wp>4095 else wp)
            sts.append(ST[wp])
            # match model prediction for this bit
            if pred_byte >= 0 and mlen > 0:
                exp_bit = (pred_byte >> (7-bp)) & 1
                # confidence grows with match length
                conf = min(1800, 200 + mlen*140)
                sts.append(conf if exp_bit else -conf)
            else:
                sts.append(0)
            # mix
            sel = (((hist[i-1] if i>0 else 0) >> 5) * 8 + bp) % NSEL
            base = sel*NM
            dot = 0.0
            for m in range(NM):
                dot += W[base+m]*sts[m]     # sts already in 256-fixed-point stretch
            p = squash(dot)          # squash clamps to +/-2047; 1..4095 out
            # actual bit
            bit = (hist[i] >> (7-bp)) & 1
            pf = p/4096.0
            loss += -math.log2(pf if bit else 1-pf)
            # update mixer
            err = ((bit<<12) - p) / 4096.0
            g = LR*err
            for m in range(NM):
                W[base+m] += g*sts[m]*(1/256.0)
            # update count models
            for oi in range(len(ORDERS)):
                idx = idxs[oi]
                n0 = tabs[oi][2*idx]; n1 = tabs[oi][2*idx+1]
                if bit:
                    n1 = n1+1
                    if n0>2: n0=(n0>>1)
                else:
                    n0 = n0+1
                    if n1>2: n1=(n1>>1)
                if n0>255 or n1>255: n0>>=1; n1>>=1
                tabs[oi][2*idx]=n0; tabs[oi][2*idx+1]=n1
            # update word model counts
            wn0 = wordtab[2*widx]; wn1 = wordtab[2*widx+1]
            if bit:
                wn1 += 1
                if wn0>2: wn0>>=1
            else:
                wn0 += 1
                if wn1>2: wn1>>=1
            if wn0>255 or wn1>255: wn0>>=1; wn1>>=1
            wordtab[2*widx]=wn0; wordtab[2*widx+1]=wn1
            c0 = (c0<<1)|bit
            bitctx = c0
        # update match model after full byte
        if pred_byte == hist[i] and mptr>=0:
            mlen = min(28, mlen+1); mptr += 1
        else:
            mlen = 0; mptr = -1
        if i >= 4:
            hh = 0
            for j in range(1,5): hh = (hh*0x9E3779B1 + hist[i-j+1]) & 0xFFFFFFFF  # last 4 incl current
            key = hh & MHMASK
            cand = matchtab[key]
            if mlen == 0 and cand >= 0:
                mptr = cand+1 if cand+1 <= i else -1
                mlen = 1 if mptr>=0 else 0
            matchtab[key] = i
        if (i & 0x3FFFF) == 0 and i>0:
            bpc = loss/(i*8)*8
            print(f"  {i:,}/{len(hist):,}  bpc so far {loss/(i)/1:.4f}  "
                  f"({i/(time.time()-t0)/1e3:.1f} KB/s)", flush=True)
    bpc = loss/len(hist)
    dt = time.time()-t0
    print(f"CM orders={ORDERS}+match  N={len(hist):,}  bpc={bpc:.4f}  ({dt:.0f}s)")
    json.dump(dict(N=len(hist), orders=ORDERS, bpc=bpc, seconds=dt),
              open(f"{S}/rime_cm_{len(hist)}.json","w"))
    return bpc

if __name__ == "__main__":
    run()
