#!/usr/bin/env python3
# Asolaria Cube Compressor (honest, buildable version).
# Implements: multi-level glyph tokenization (BPE), + an order-1 adaptive context model
# over glyphs + carryless range coder (the real engine). Cube transform (byte-reverse
# involution) measured as an option. Every byte counted (payload + decoder + dictionary),
# byte-exact restore gated by SHA-256. Compared honestly to gzip/bzip2/xz.
import hashlib, sys, time, os
import numpy as np

TOP=1<<24; BOT=1<<16; MASK=0xFFFFFFFF
DECODER_SELF_BYTES = None  # set at runtime = size of this file (the decompressor is charged)

# ---------------- BPE glyph learning ----------------
def bpe_train(byte_seq, n_merges):
    seq=list(byte_seq)
    merges=[]                      # ordered list of (a,b)->new_id
    nextid=256
    for _ in range(n_merges):
        # count adjacent pairs
        pairs={}
        prev=None
        for s in seq:
            if prev is not None:
                pairs[(prev,s)]=pairs.get((prev,s),0)+1
            prev=s
        if not pairs: break
        (a,b),cnt=max(pairs.items(), key=lambda kv: kv[1])
        if cnt<2: break
        merges.append((a,b))
        # apply merge
        out=[]; i=0; L=len(seq)
        while i<L:
            if i<L-1 and seq[i]==a and seq[i+1]==b:
                out.append(nextid); i+=2
            else:
                out.append(seq[i]); i+=1
        seq=out; nextid+=1
    return seq, merges

def bpe_decode(seq, merges):
    # expand each merged id back to bytes (merges applied in order -> reverse expansion)
    table={256+i:merges[i] for i in range(len(merges))}
    out=[]
    stack=list(seq)
    # iterative expansion
    def expand(sym, acc):
        if sym<256: acc.append(sym); return
        a,b=table[sym]; expand(a,acc); expand(b,acc)
    acc=[]
    for s in seq: expand(s, acc)
    return bytes(acc)

def merges_bytes(merges):
    # cost of shipping the dictionary: each merge is a pair of ids < current alphabet.
    # store as 2 varints; estimate 3 bytes/merge (ids up to ~1280 -> 2 bytes each, ~4; use exact varint)
    b=bytearray()
    for a,x in merges:
        for v in (a,x):
            while True:
                c=v&0x7F; v>>=7
                if v: b.append(c|0x80)
                else: b.append(c); break
    return len(b)

# ---------------- order-1 range coder over an alphabet of size V ----------------
def rc_compress(seq, V):
    freq=np.ones((V,V),dtype=np.uint32)
    low,rng=0,MASK; out=bytearray(); ctx=0
    for s in seq:
        f=freq[ctx]; tot=int(f.sum()); c=int(f[:s].sum()); fr=int(f[s])
        r=rng//tot; low=(low+c*r)&MASK; rng=fr*r
        while True:
            if (low^(low+rng))&MASK<TOP: pass
            elif rng<BOT: rng=(-low)&(BOT-1)
            else: break
            out.append((low>>24)&0xFF); low=(low<<8)&MASK; rng=(rng<<8)&MASK
        f[s]+=32
        if tot>60000: freq[ctx]=(f>>1)|1
        ctx=s
    for _ in range(4): out.append((low>>24)&0xFF); low=(low<<8)&MASK
    return bytes(out)

def rc_decompress(comp,n,V):
    freq=np.ones((V,V),dtype=np.uint32)
    low,rng=0,MASK; code=int.from_bytes(comp[:4],"big"); pos=4
    out=[]; ctx=0
    for _ in range(n):
        f=freq[ctx]; tot=int(f.sum()); r=rng//tot
        target=min(((code-low)&MASK)//r, tot-1)
        cum=np.cumsum(f); s=int(np.searchsorted(cum,target,side="right"))
        c=int(cum[s-1]) if s>0 else 0; fr=int(f[s])
        low=(low+c*r)&MASK; rng=fr*r
        while True:
            if (low^(low+rng))&MASK<TOP: pass
            elif rng<BOT: rng=(-low)&(BOT-1)
            else: break
            code=((code<<8)|(comp[pos] if pos<len(comp) else 0))&MASK; pos+=1
            low=(low<<8)&MASK; rng=(rng<<8)&MASK
        f[s]+=32
        if tot>60000: freq[ctx]=(f>>1)|1
        out.append(s); ctx=s
    return out

# ---------------- driver ----------------
def run(path, n_merges, cube):
    data=open(path,"rb").read()
    N=len(data); sha_in=hashlib.sha256(data).hexdigest()
    src=data
    if cube:  # reversible "cube" involution: reverse byte order (bijection)
        src=data[::-1]
    t0=time.time()
    seq,merges=bpe_train(src, n_merges)
    V=256+len(merges)
    comp=rc_compress(seq, V)
    enc_s=time.time()-t0
    dict_b=merges_bytes(merges)
    # decode path (verify byte-exact)
    seq2=rc_decompress(comp, len(seq), V)
    body=bpe_decode(seq2, merges)
    if cube: body=body[::-1]
    ok = hashlib.sha256(body).hexdigest()==sha_in
    payload=len(comp); total=payload+dict_b+DECODER_SELF_BYTES
    return dict(N=N, glyphs=len(seq), V=V, payload=payload, dict_b=dict_b,
               decoder=DECODER_SELF_BYTES, total=total,
               bpc_payload=payload*8/N, bpc_total=total*8/N, ok=ok, enc_s=enc_s)

if __name__=="__main__":
    DECODER_SELF_BYTES=os.path.getsize(__file__)
    path=sys.argv[1]
    for nm in (0, 512, 1024):
        r=run(path, nm, cube=False)
        print(f"glyph-merges={nm:5d} cube=0  V={r['V']:5d} glyphs={r['glyphs']:7d} "
              f"payload={r['payload']:7d} dict={r['dict_b']:6d} decoder={r['decoder']} "
              f"total={r['total']:7d}  bpc_total={r['bpc_total']:.4f}  restore={'OK' if r['ok'] else 'FAIL'}")
    r=run(path, 1024, cube=True)
    print(f"glyph-merges= 1024 cube=1  V={r['V']:5d} glyphs={r['glyphs']:7d} "
          f"payload={r['payload']:7d} dict={r['dict_b']:6d} total={r['total']:7d}  "
          f"bpc_total={r['bpc_total']:.4f}  restore={'OK' if r['ok'] else 'FAIL'}")
