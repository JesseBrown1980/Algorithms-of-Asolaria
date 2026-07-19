#!/usr/bin/env python3
# Phase 1 v0 — word-replacing transform (the language layer), reversibility-gated.
# Codes: two-byte (u, i) where u = byte values UNUSED in the corpus (verified),
# i = 0..255. Top-N frequent words -> codes. Dictionary shipped and charged.
# GATE: inverse(transform(x)) must equal x byte-exact, or everything halts.
import sys, re, hashlib, collections

def build(data, max_prefixes=16):
    used = set(data)
    unused = [b for b in range(256) if b not in used]
    prefixes = unused[:max_prefixes]
    cap = len(prefixes) * 256
    # words: space+lowercase-run (the " the" trick: fold the leading space in)
    words = collections.Counter(m.group() for m in re.finditer(rb' [a-z]{2,20}', data))
    top = [w for w, c in words.most_common(cap) if c * (len(w) - 2) > len(w) + 3]
    return prefixes, top

def transform(data, prefixes, top):
    code = {w: bytes([prefixes[i >> 8], i & 255]) for i, w in enumerate(top)}
    pat = re.compile(rb' [a-z]{2,20}')
    return pat.sub(lambda m: code.get(m.group(), m.group()), data)

def inverse(tdata, prefixes, top):
    dec = {}
    for i, w in enumerate(top):
        dec[(prefixes[i >> 8], i & 255)] = w
    out = bytearray(); i = 0; n = len(tdata); pset = set(prefixes)
    while i < n:
        b = tdata[i]
        if b in pset and i + 1 < n and (b, tdata[i+1]) in dec:
            out += dec[(b, tdata[i+1])]; i += 2
        else:
            out.append(b); i += 1
    return bytes(out)

def dict_bytes(prefixes, top):
    # shipped dictionary: prefix list + newline-joined words
    return len(prefixes) + 2 + sum(len(w) for w in top) + len(top)

if __name__ == "__main__":
    path = sys.argv[1]
    data = open(path, "rb").read()
    sha_in = hashlib.sha256(data).hexdigest()
    prefixes, top = build(data)
    t = transform(data, prefixes, top)
    r = inverse(t, prefixes, top)
    ok = hashlib.sha256(r).hexdigest() == sha_in
    print(f"corpus={len(data)}  transformed={len(t)}  ({100*len(t)/len(data):.1f}%)")
    print(f"prefixes={len(prefixes)}  words={len(top)}  dict_charge={dict_bytes(prefixes, top)}")
    print(f"REVERSIBILITY GATE: {'PASS — byte-exact' if ok else 'FAIL — HALT PHASE'}")
    if ok:
        open(path + ".wrt", "wb").write(t)
