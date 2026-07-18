#!/usr/bin/env python3
# Context-mixing compressor for the Asolaria honest-compressor lane.
#
# Implements the ONLY real lever per HONEST-SPEC.md: a stronger predictive model.
#   - Blends orders 0..k (dense tables for orders 0-1, sparse dicts for >=2)
#   - Per-context adaptive weights: a (k+1)-weight vector per order-1 bucket,
#     updated by the Bayes mixture rule with fixed-share (Herbster-Warmuth),
#     so the mix tracks whichever order predicts best in each local context.
#   - Carryless range coder (same constants as asolaria_cube_compressor.py).
#   - Optional BPE glyph layer; the merge dictionary is varint-shipped and counted.
#
# Honesty gates (non-negotiable):
#   - total = payload + decoder(self) + dictionary, byte-exact.
#   - SHA-256 restore check; a failed restore invalidates the run.
#   - No claim below N*H(X). The measurement is the referee.
import hashlib, sys, os, time
import numpy as np

TOP = 1 << 24; BOT = 1 << 16; MASK = 0xFFFFFFFF
K = 1 << 14          # coder total (integer probability resolution)
ALPHA_SHARE = 0.02   # fixed-share mixing floor
W_MIN = 1e-8

# ---------------- BPE (same conventions as asolaria_cube_compressor.py) ----------------
def bpe_train(byte_seq, n_merges):
    seq = list(byte_seq); merges = []; nextid = 256
    for _ in range(n_merges):
        pairs = {}; prev = None
        for s in seq:
            if prev is not None:
                pairs[(prev, s)] = pairs.get((prev, s), 0) + 1
            prev = s
        if not pairs: break
        (a, b), cnt = max(pairs.items(), key=lambda kv: kv[1])
        if cnt < 2: break
        merges.append((a, b))
        out = []; i = 0; L = len(seq)
        while i < L:
            if i < L - 1 and seq[i] == a and seq[i + 1] == b:
                out.append(nextid); i += 2
            else:
                out.append(seq[i]); i += 1
        seq = out; nextid += 1
    return seq, merges

def bpe_decode(seq, merges):
    table = {256 + i: merges[i] for i in range(len(merges))}
    acc = []
    def expand(sym):
        stack = [sym]
        while stack:
            t = stack.pop()
            if t < 256: acc.append(t)
            else:
                a, b = table[t]; stack.append(b); stack.append(a)
    for s in seq: expand(s)
    return bytes(acc)

def merges_bytes(merges):
    b = bytearray()
    for a, x in merges:
        for v in (a, x):
            while True:
                c = v & 0x7F; v >>= 7
                if v: b.append(c | 0x80)
                else: b.append(c); break
    return len(b)

# ---------------- context-mixing model ----------------
class CMModel:
    """Deterministic online model. Encoder and decoder run the exact same updates,
    so both sides always hold identical integer frequency tables."""
    def __init__(self, V, k):
        self.V = V; self.k = k
        self.c0 = np.zeros(V, dtype=np.float64); self.t0 = 0.0
        self.c1 = np.zeros((V, V), dtype=np.float64); self.t1 = np.zeros(V, dtype=np.float64)
        self.hi = [dict() for _ in range(max(0, k - 1))]   # orders 2..k: ctx-tuple -> (dict sym->cnt, total)
        # per-context adaptive weights: one weight vector per order-1 bucket (last symbol)
        self.w = np.full((V + 1, k + 1), 1.0 / (k + 1), dtype=np.float64)
        self.uni = np.full(V, 1.0 / V, dtype=np.float64)
        self.hist = []

    def _order_p(self, o):
        V = self.V
        if o == 0:
            return (self.c0 + 1.0 / V) / (self.t0 + 1.0)
        h = self.hist
        if len(h) < o:
            return self.uni
        if o == 1:
            ctx = h[-1]
            t = self.t1[ctx]
            return (self.c1[ctx] + 1.0 / V) / (t + 1.0)
        ctx = tuple(h[-o:])
        entry = self.hi[o - 2].get(ctx)
        if entry is None:
            return self.uni
        d, t = entry
        p = np.full(V, (1.0 / V) / (t + 1.0))
        ks = list(d.keys())
        p[ks] += np.fromiter(d.values(), dtype=np.float64, count=len(ks)) / (t + 1.0)
        return p

    def predict(self):
        bucket = (self.hist[-1] + 1) if self.hist else 0
        w = self.w[bucket]
        ps = [self._order_p(o) for o in range(self.k + 1)]
        pm = np.zeros(self.V)
        for o in range(self.k + 1):
            pm += w[o] * ps[o]
        pm /= pm.sum()
        # integer frequencies, deterministic
        f = np.maximum((pm * K).astype(np.int64), 1)
        diff = K - int(f.sum())
        if diff != 0:
            j = int(np.argmax(f))
            if f[j] + diff >= 1: f[j] += diff
            else:
                # spread removal deterministically over largest entries
                order = np.argsort(-f)
                i = 0
                while diff < 0:
                    j = int(order[i % len(order)])
                    take = min(-diff, int(f[j]) - 1)
                    f[j] -= take; diff += take; i += 1
        return f, ps, pm, bucket

    def update(self, s, ps, pm, bucket):
        k = self.k
        # per-context weight update: Bayes mixture + fixed share
        w = self.w[bucket]
        like = np.fromiter((max(ps[o][s], 1e-12) for o in range(k + 1)), dtype=np.float64, count=k + 1)
        w = w * like
        w /= w.sum()
        w = (1.0 - ALPHA_SHARE) * w + ALPHA_SHARE / (k + 1)
        np.maximum(w, W_MIN, out=w)
        self.w[bucket] = w / w.sum()
        # count updates
        self.c0[s] += 1; self.t0 += 1
        h = self.hist
        if h:
            self.c1[h[-1], s] += 1; self.t1[h[-1]] += 1
        for o in range(2, k + 1):
            if len(h) >= o:
                ctx = tuple(h[-o:])
                entry = self.hi[o - 2].get(ctx)
                if entry is None:
                    self.hi[o - 2][ctx] = ({s: 1.0}, 1.0)
                else:
                    d, t = entry
                    d[s] = d.get(s, 0.0) + 1.0
                    self.hi[o - 2][ctx] = (d, t + 1.0)
        h.append(s)
        if len(h) > k: del h[0]

# ---------------- range coder (carryless, repo constants) ----------------
def cm_compress(seq, V, k):
    m = CMModel(V, k)
    low, rng = 0, MASK; out = bytearray()
    for s in seq:
        f, ps, pm, bucket = m.predict()
        cum = np.cumsum(f)
        c = int(cum[s - 1]) if s > 0 else 0
        fr = int(f[s])
        r = rng // K
        low = (low + c * r) & MASK; rng = fr * r
        while True:
            if (low ^ (low + rng)) & MASK < TOP: pass
            elif rng < BOT: rng = (-low) & (BOT - 1)
            else: break
            out.append((low >> 24) & 0xFF); low = (low << 8) & MASK; rng = (rng << 8) & MASK
        m.update(s, ps, pm, bucket)
    for _ in range(4):
        out.append((low >> 24) & 0xFF); low = (low << 8) & MASK
    return bytes(out)

def cm_decompress(comp, n, V, k):
    m = CMModel(V, k)
    low, rng = 0, MASK
    code = int.from_bytes(comp[:4], "big"); pos = 4
    out = []
    for _ in range(n):
        f, ps, pm, bucket = m.predict()
        cum = np.cumsum(f)
        r = rng // K
        target = min(((code - low) & MASK) // r, K - 1)
        s = int(np.searchsorted(cum, target, side="right"))
        c = int(cum[s - 1]) if s > 0 else 0
        fr = int(f[s])
        low = (low + c * r) & MASK; rng = fr * r
        while True:
            if (low ^ (low + rng)) & MASK < TOP: pass
            elif rng < BOT: rng = (-low) & (BOT - 1)
            else: break
            code = ((code << 8) | (comp[pos] if pos < len(comp) else 0)) & MASK; pos += 1
            low = (low << 8) & MASK; rng = (rng << 8) & MASK
        m.update(s, ps, pm, bucket)
        out.append(s)
    return out

# ---------------- driver ----------------
def run(path, n_merges, k):
    data = open(path, "rb").read()
    N = len(data); sha_in = hashlib.sha256(data).hexdigest()
    t0 = time.time()
    if n_merges > 0:
        seq, merges = bpe_train(data, n_merges)
    else:
        seq, merges = list(data), []
    V = 256 + len(merges)
    comp = cm_compress(seq, V, k)
    enc_s = time.time() - t0
    dict_b = merges_bytes(merges)
    t1 = time.time()
    seq2 = cm_decompress(comp, len(seq), V, k)
    body = bpe_decode(seq2, merges)
    dec_s = time.time() - t1
    ok = hashlib.sha256(body).hexdigest() == sha_in
    decoder_b = os.path.getsize(__file__)
    payload = len(comp); total = payload + dict_b + decoder_b
    return dict(N=N, glyphs=len(seq), V=V, k=k, merges=len(merges),
                payload=payload, dict_b=dict_b, decoder=decoder_b, total=total,
                bpc_total=total * 8 / N, ok=ok, enc_s=enc_s, dec_s=dec_s)

if __name__ == "__main__":
    path = sys.argv[1]
    configs = []
    for arg in sys.argv[2:]:
        nm, k = arg.split(",")
        configs.append((int(nm), int(k)))
    if not configs:
        configs = [(0, 1), (0, 2), (0, 3)]
    for nm, k in configs:
        r = run(path, nm, k)
        print(f"merges={nm:5d} k={k}  V={r['V']:5d} glyphs={r['glyphs']:7d} "
              f"payload={r['payload']:7d} dict={r['dict_b']:6d} decoder={r['decoder']} "
              f"total={r['total']:7d}  bpc_total={r['bpc_total']:.4f}  "
              f"restore={'OK' if r['ok'] else 'FAIL'}  enc={r['enc_s']:.0f}s dec={r['dec_s']:.0f}s",
              flush=True)
