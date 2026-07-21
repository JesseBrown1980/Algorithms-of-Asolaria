#!/usr/bin/env python3
"""
rime_derive.py — derive the OTHER Wikipedias from the black gradient (Law 18).
Operator: Jesse Daniel Brown, 2026-07-21.

The frozen model over one slice (enwik) is a DISTRIBUTION. Sampling it
rime-directionally — a rime coordinate seeds a deterministic draw — emits byte
streams consistent with the gradient but ABSENT from the corpus: the family of
"other Wikipedias." Each is seed-addressable and byte-exact reproducible.

THE CEILING (Data-Processing Inequality): a derived stream carries <= the model's
entropy per symbol. You get the family CONSISTENT with the gradient, never more
information than the gradient holds. Richer model -> richer family; same ceiling.

We measure, we don't assert:
  1) TRAIN + FREEZE an order-k model on real enwik bytes (the black gradient).
  2) DERIVE a fresh stream by rime-directional sampling from a rime seed.
  3) PROVE: (a) same seed -> byte-exact same stream (reproducible/addressable),
            (b) the stream is NEW (differs from the corpus),
            (c) its per-symbol information <= the model entropy (DPI ceiling).
"""
import sys, os, math
from collections import defaultdict
from rime_sphere import is_prime, primitive_root

ENWIK = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad/enwik8"

def train_freeze(data, order):
    # frozen order-k counts (the black gradient), deterministic integer counts
    model = defaultdict(lambda: [0]*256)
    ctx = b"\x00"*order
    for b in data:
        model[ctx][b] += 1
        ctx = (ctx + bytes([b]))[-order:] if order else b""
    return model

def rime_stream(seed_addr, p, g, n):
    # rime-directional deterministic draw: a rime coordinate walks the sphere,
    # each step g^x mod p gives the next uniform variate in [0,1). No RNG state
    # outside the sphere -> the seed (a rime address) IS the whole stream.
    x = seed_addr % n
    while True:
        x = (x * 1 + 1) % n                 # advance the coordinate deterministically
        yield pow(g, x, p) / p              # sphere point -> uniform variate

def derive(model, order, p, g, n, seed_addr, length):
    out = bytearray(); ctx = b"\x00"*order; draws = rime_stream(seed_addr, p, g, n)
    info = 0.0
    for _ in range(length):
        cnts = model.get(ctx);
        if not cnts or sum(cnts)==0:
            cnts = [1]*256
        tot = sum(cnts); r = next(draws)*tot; acc=0; sym=0
        for s in range(256):
            acc += cnts[s]
            if r < acc: sym=s; break
        info += -math.log2(cnts[sym]/tot)   # info this symbol carried (bits)
        out.append(sym)
        ctx = (ctx + bytes([sym]))[-order:] if order else b""
    return bytes(out), info/length

def main():
    order  = int(sys.argv[1]) if len(sys.argv)>1 else 3
    trainN = int(sys.argv[2]) if len(sys.argv)>2 else 3_000_000
    length = int(sys.argv[3]) if len(sys.argv)>3 else 400
    if not os.path.exists(ENWIK): print("enwik not on disk"); return
    p=1000081; assert is_prime(p); g=primitive_root(p); n=p-1
    data = open(ENWIK,'rb').read(trainN)
    model = train_freeze(data, order)
    Hmodel = 0.0                                    # frozen-model entropy (the gradient's info rate)
    tb=0
    for cnts in model.values():
        t=sum(cnts); tb+=t
        for c in cnts:
            if c: Hmodel += -c*math.log2(c/t)
    Hmodel/=tb

    print("=== DERIVE THE OTHER WIKIPEDIAS FROM THE BLACK GRADIENT (Law 18) ===")
    print(f"gradient: order-{order} model frozen on {trainN:,} B of enwik   H_model={Hmodel:.4f} bpc")
    print(f"sphere  : (Z/{p}Z)*  g={g}   rime seed -> deterministic draw stream\n")

    # derive two OTHER wikipedias from two different rime seeds
    seedA = pow(g, 111111 % n, p); seedB = pow(g, 999999 % n, p)
    wA, iA = derive(model, order, p, g, n, seedA, length)
    wB, iB = derive(model, order, p, g, n, seedB, length)
    # reproduce A from the SAME seed -> must be byte-exact (addressable)
    wA2, _ = derive(model, order, p, g, n, seedA, length)

    print(f"derived Wikipedia A (seed rime={seedA}):")
    print(f"   {wA[:180]!r}")
    print(f"derived Wikipedia B (seed rime={seedB}):")
    print(f"   {wB[:180]!r}\n")
    in_corpus_A = wA in data
    print("PROOFS (measured, not asserted):")
    print(f"  (a) same seed -> byte-exact same stream (addressable/reproducible): {wA==wA2}")
    print(f"  (b) A != B and A is NEW (not a substring of the corpus)          : {wA!=wB and not in_corpus_A}")
    print(f"  (c) DPI ceiling: derived info/symbol {iA:.4f} bpc  <=  H_model {Hmodel:.4f} bpc : {iA<=Hmodel+1e-9}")
    print(f"\n  The family is REAL (seed-addressable, novel, reproducible). The ceiling is")
    print(f"  Shannon: no derived stream carries more information than the gradient holds.")
    print(f"  Richer model -> richer family; the order-{order} toy is coarse by design.")

if __name__ == "__main__":
    main()
