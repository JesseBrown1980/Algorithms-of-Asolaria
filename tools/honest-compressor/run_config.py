#!/usr/bin/env python3
# Foreground runner for one (merges,k) config with BPE caching.
import sys, os, pickle, time, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cm_asolaria as cm

path, nm, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
data = open(path, "rb").read()
N = len(data); sha_in = hashlib.sha256(data).hexdigest()

if nm > 0:
    cache = f"bpe{nm}.pkl"
    if os.path.exists(cache):
        seq, merges = pickle.load(open(cache, "rb"))
    else:
        t0 = time.time()
        seq, merges = cm.bpe_train(data, nm)
        pickle.dump((seq, merges), open(cache, "wb"))
        print(f"# bpe_train({nm}) took {time.time()-t0:.0f}s, cached", flush=True)
else:
    seq, merges = list(data), []

V = 256 + len(merges)
t0 = time.time()
comp = cm.cm_compress(seq, V, k)
enc_s = time.time() - t0
t1 = time.time()
seq2 = cm.cm_decompress(comp, len(seq), V, k)
body = cm.bpe_decode(seq2, merges)
dec_s = time.time() - t1
ok = hashlib.sha256(body).hexdigest() == sha_in
dict_b = cm.merges_bytes(merges)
decoder_b = os.path.getsize(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cm_asolaria.py"))
payload = len(comp); total = payload + dict_b + decoder_b
line = (f"merges={nm:5d} k={k}  V={V:5d} glyphs={len(seq):7d} "
        f"payload={payload:7d} dict={dict_b:6d} decoder={decoder_b} "
        f"total={total:7d}  bpc_total={total*8/N:.4f}  "
        f"restore={'OK' if ok else 'FAIL'}  enc={enc_s:.0f}s dec={dec_s:.0f}s")
print(line, flush=True)
with open("cm-sweep.log", "a") as f:
    f.write(line + "\n")
