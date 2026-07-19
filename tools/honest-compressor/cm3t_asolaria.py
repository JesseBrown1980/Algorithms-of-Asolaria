#!/usr/bin/env python3
# cm3: cm2 + word model + SSE chain (two chained APM stages).
# The CPU road called by RESULTS.md finding 5: secondary estimation + word-level
# context, not more order depth. Same honesty gates as cm2.
#
# The next rung past cm_asolaria.py, still the ONLY real lever (the model):
#   - each glyph is coded MSB-first as B = ceil(log2 V) binary decisions
#   - hashed context models of glyph-orders 1..k, each predicting the next bit
#     at the current tree node, with adaptive 12-bit probabilities
#   - a match model (longest recent order-M match predicts the next glyph's bits)
#   - logistic mixing: p = squash(sum w_i * stretch(p_i)), weights selected per
#     (bit-position, quantized last glyph), trained online by gradient descent
#   - one APM/SSE stage refining the mixed p against (quantized p, order-1 ctx)
#   - carryless binary arithmetic coder (exact, no rounding loss)
#   - optional BPE glyph layer; dictionary varint-shipped and counted
#
# Honesty gates: total = payload + decoder(self) + dictionary, byte-exact;
# SHA-256 restore or the run is invalid; nothing below entropy is claimed.
import hashlib, os, pickle, sys, time
import numpy as np
T1 = float(os.environ.get('CM3_T1','0.6'))
T2 = float(os.environ.get('CM3_T2','0.7'))

# ---------- BPE layer (identical conventions to cm_asolaria.py, inlined so the
# ---------- decoder is this single self-contained file) ----------
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
    for s in seq:
        stack = [s]
        while stack:
            t = stack.pop()
            if t < 256: acc.append(t)
            else:
                a, b = table[t]; stack.append(b); stack.append(a)
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

PSCALE = 4096
TBITS = 23
TSIZE = 1 << TBITS
TMASK = TSIZE - 1

def _build_stretch():
    st = np.zeros(PSCALE, dtype=np.float64)
    for i in range(PSCALE):
        p = (i + 0.5) / PSCALE
        st[i] = np.log(p / (1 - p))
    return st
STRETCH = _build_stretch()

def squash(x):
    if x > 20: x = 20.0
    elif x < -20: x = -20.0
    return 1.0 / (1.0 + np.exp(-x))

class Model:
    def __init__(self, V, k, match_order=5, lr=0.02):
        self.V = V; self.k = k; self.mo = match_order; self.lr = lr
        self.B = max(1, (V - 1).bit_length())
        self.nin = k + 4                     # k orders + order0 + match + 2 word models
        # hashed bit-probability tables per order (uint16 prob in [0,4096))
        self.t = [np.full(TSIZE, PSCALE // 2, dtype=np.uint16) for _ in range(k)]
        self.tn = [np.zeros(TSIZE, dtype=np.uint8) for _ in range(k)]
        self.t0 = np.full(1 << (self.B + 1), PSCALE // 2, dtype=np.uint16)
        self.t0n = np.zeros(1 << (self.B + 1), dtype=np.uint8)
        # count-adaptive rates: fast when a context is young, 1/32 when mature
        self.RATE = [1.0 / (n + 1.5) if n < 30 else 1.0 / 32.0 for n in range(256)]
        # mixer weights: (B bit positions x 256 last-glyph buckets) sets
        self.w = np.zeros((self.B * 256, self.nin), dtype=np.float64)
        self.w[:, :] = 0.3
        # APM: (33 p-bins x 1024 ctx buckets)
        self.apm = np.tile((np.arange(33, dtype=np.float64) / 32.0), (1024, 1)).copy()
        # word model tables (share TSIZE hashing)
        self.tw = [np.full(TSIZE, PSCALE // 2, dtype=np.uint16) for _ in range(2)]
        self.twn = [np.zeros(TSIZE, dtype=np.uint8) for _ in range(2)]
        self.wh = 0                          # hash of current (partial) word
        self.pwh = 0                         # hash of previous word
        # second APM stage (SSE chain), keyed by (match-len bucket, node byte)
        self.apm2 = np.tile((np.arange(33, dtype=np.float64) / 32.0), (1024, 1)).copy()
        # match model state
        self.hist = []                       # full glyph history
        self.mpos = {}                       # hash(last mo glyphs) -> position
        self.match_ptr = -1; self.match_len = 0
        self.ctx_h = [0] * (k + 1)           # rolling hashes for orders 1..k

    # ----- per-symbol setup: compute context hashes, refresh match -----
    def begin_symbol(self):
        h = self.hist; k = self.k
        for o in range(1, k + 1):
            v = 0
            if len(h) >= o:
                for g in h[-o:]:
                    v = (v * 0x9E3779B1 + g + 1) & 0xFFFFFFFF
                v = (v ^ (o * 0x85EBCA6B)) & 0xFFFFFFFF
            self.ctx_h[o] = v
        # match model: find/extend candidate
        if self.match_ptr >= 0 and self.match_ptr < len(h):
            pass  # still valid, extended in update_symbol
        if self.match_ptr < 0 and len(h) >= self.mo:
            key = 0
            for g in h[-self.mo:]:
                key = (key * 0x01000193 + g + 1) & 0xFFFFFFFF
            p = self.mpos.get(key, -1)
            if p >= 0 and p < len(h):
                self.match_ptr = p; self.match_len = self.mo
        self.pred_glyph = self.hist[self.match_ptr] if 0 <= self.match_ptr < len(self.hist) else -1
        self.bucket_base = ((self.hist[-1] & 0xFF) if self.hist else 0)
        self.wctx1 = (self.wh ^ 0x8DA6B343) & 0xFFFFFFFF
        self.wctx2 = ((self.wh * 0x01000193) ^ (self.pwh * 0x9E3779B1)) & 0xFFFFFFFF

    # ----- predict probability that next bit is 1, at tree node c (bit j) -----
    def predict_bit(self, c, j):
        k = self.k
        idxs = self.idxs = []
        x = self.x = np.empty(self.nin, dtype=np.float64)
        for o in range(1, k + 1):
            idx = ((self.ctx_h[o] ^ (c * 0xB5297A4D)) & TMASK)
            idxs.append(idx)
            x[o - 1] = STRETCH[self.t[o - 1][idx]]
        self.o0idx = c & ((1 << (self.B + 1)) - 1)
        x[k] = STRETCH[self.t0[self.o0idx]]
        # match input
        if self.pred_glyph >= 0:
            pb = (self.pred_glyph >> (self.B - 1 - j)) & 1
            strength = min(self.match_len, 28) * 0.18
            x[k + 1] = strength if pb else -strength
            self.match_bit = pb
        else:
            x[k + 1] = 0.0; self.match_bit = -1
        wi1 = ((self.wctx1 ^ (c * 0xB5297A4D)) & TMASK)
        wi2 = ((self.wctx2 ^ (c * 0xB5297A4D)) & TMASK)
        self.widx = (wi1, wi2)
        x[k + 2] = STRETCH[self.tw[0][wi1]]
        x[k + 3] = STRETCH[self.tw[1][wi2]]
        wrow = self.wrow = j * 256 + self.bucket_base
        dot = float(np.dot(self.w[wrow], x))
        p1 = squash(dot)
        # SSE chain: stage 1 keyed by order-1 ctx, stage 2 by (match-len, last byte)
        def _bin(p):
            pf = min(max(p, 1e-6), 1 - 1e-6)
            z = np.log(pf / (1 - pf))
            b = (z + 8.0) * 2.0
            b = min(max(b, 0.0), 31.999)
            b0 = int(b); return b0, b - b0
        actx = ((self.ctx_h[1] ^ (c * 0x2545F491)) & 1023) if self.k >= 1 else (c & 1023)
        b0, frac = _bin(p1)
        a = self.apm[actx]
        pa = a[b0] * (1 - frac) + a[b0 + 1] * frac
        self.apm_state = (actx, b0, frac)
        p_s1 = T1 * pa + (1-T1) * p1
        mlb = min(self.match_len, 3)
        actx2 = (mlb * 256 + self.bucket_base) & 1023
        b02, frac2 = _bin(p_s1)
        a2 = self.apm2[actx2]
        pa2 = a2[b02] * (1 - frac2) + a2[b02 + 1] * frac2
        self.apm2_state = (actx2, b02, frac2)
        p = T2 * pa2 + (1-T2) * p_s1
        p = min(max(p, 1.0 / PSCALE), 1 - 1.0 / PSCALE)
        self.p1_pre = p1
        return p

    # ----- after coding the actual bit -----
    def update_bit(self, c, j, bit):
        k = self.k; err = bit - self.p1_pre
        wrow = self.wrow
        self.w[wrow] += self.lr * err * self.x
        RATE = self.RATE
        for o in range(1, k + 1):
            t = self.t[o - 1]; tn = self.tn[o - 1]; idx = self.idxs[o - 1]
            n = int(tn[idx]); v = int(t[idx])
            t[idx] = min(PSCALE - 1, max(0, v + int((bit * PSCALE - v) * RATE[n])))
            if n < 255: tn[idx] = n + 1
        idx = self.o0idx
        n = int(self.t0n[idx]); v = int(self.t0[idx])
        self.t0[idx] = min(PSCALE - 1, max(0, v + int((bit * PSCALE - v) * RATE[n])))
        if n < 255: self.t0n[idx] = n + 1
        for wi_t, wi_n, wi in ((self.tw[0], self.twn[0], self.widx[0]),
                                (self.tw[1], self.twn[1], self.widx[1])):
            n = int(wi_n[wi]); v = int(wi_t[wi])
            wi_t[wi] = min(PSCALE - 1, max(0, v + int((bit * PSCALE - v) * RATE[n])))
            if n < 255: wi_n[wi] = n + 1
        actx, b0, frac = self.apm_state
        a = self.apm[actx]
        tgt = float(bit)
        a[b0] += 0.02 * (1 - frac) * (tgt - a[b0])
        a[b0 + 1] += 0.02 * frac * (tgt - a[b0 + 1])
        actx2, b02, frac2 = self.apm2_state
        a2 = self.apm2[actx2]
        a2[b02] += 0.02 * (1 - frac2) * (tgt - a2[b02])
        a2[b02 + 1] += 0.02 * frac2 * (tgt - a2[b02 + 1])
        if self.match_bit >= 0 and self.match_bit != bit:
            self.match_ptr = -1; self.match_len = 0   # match broken mid-symbol

    # ----- after the full symbol is known -----
    def update_symbol(self, s):
        # word tracking: letters/digits extend the word, else word boundary
        if (48 <= (s & 0xFF) <= 57) or (65 <= (s & 0xFF) <= 90) or (97 <= (s & 0xFF) <= 122):
            self.wh = (self.wh * 0x01000193 + (s | 0x20) + 1) & 0xFFFFFFFF
        else:
            if self.wh: self.pwh = self.wh
            self.wh = 0
        h = self.hist
        # advance/validate match
        if self.match_ptr >= 0:
            if self.hist[self.match_ptr] == s:
                self.match_ptr += 1; self.match_len += 1
            else:
                self.match_ptr = -1; self.match_len = 0
        h.append(s)
        if len(h) >= self.mo:
            key = 0
            for g in h[-self.mo:]:
                key = (key * 0x01000193 + g + 1) & 0xFFFFFFFF
            self.mpos[key] = len(h)          # position AFTER the context

# ---------- carryless binary arithmetic coder ----------
class Encoder:
    def __init__(self):
        self.x1 = 0; self.x2 = 0xFFFFFFFF; self.out = bytearray()
    def encode(self, bit, p1):
        x1, x2 = self.x1, self.x2
        xmid = x1 + int((x2 - x1) * p1)
        if xmid < x1: xmid = x1
        if xmid >= x2: xmid = x2 - 1
        if bit: x2 = xmid
        else: x1 = xmid + 1
        while (x1 ^ x2) & 0xFF000000 == 0:
            self.out.append((x2 >> 24) & 0xFF)
            x1 = (x1 << 8) & 0xFFFFFFFF; x2 = ((x2 << 8) | 0xFF) & 0xFFFFFFFF
        self.x1, self.x2 = x1, x2
    def flush(self):
        for _ in range(4):
            self.out.append((self.x1 >> 24) & 0xFF)
            self.x1 = (self.x1 << 8) & 0xFFFFFFFF
        return bytes(self.out)

class Decoder:
    def __init__(self, data):
        self.data = data; self.pos = 4
        self.x1 = 0; self.x2 = 0xFFFFFFFF
        self.x = int.from_bytes(data[:4], "big")
    def decode(self, p1):
        x1, x2 = self.x1, self.x2
        xmid = x1 + int((x2 - x1) * p1)
        if xmid < x1: xmid = x1
        if xmid >= x2: xmid = x2 - 1
        bit = 1 if self.x <= xmid else 0
        if bit: x2 = xmid
        else: x1 = xmid + 1
        while (x1 ^ x2) & 0xFF000000 == 0:
            x1 = (x1 << 8) & 0xFFFFFFFF; x2 = ((x2 << 8) | 0xFF) & 0xFFFFFFFF
            nxt = self.data[self.pos] if self.pos < len(self.data) else 0
            self.x = ((self.x << 8) | nxt) & 0xFFFFFFFF; self.pos += 1
        self.x1, self.x2 = x1, x2
        return bit

# ---------- symbol codec ----------
def compress(seq, V, k):
    m = Model(V, k); B = m.B
    enc = Encoder()
    for s in seq:
        m.begin_symbol()
        c = 1
        for j in range(B):
            bit = (s >> (B - 1 - j)) & 1
            p1 = m.predict_bit(c, j)
            enc.encode(bit, p1)
            m.update_bit(c, j, bit)
            c = (c << 1) | bit
        m.update_symbol(s)
    return enc.flush()

def decompress(data, n, V, k):
    m = Model(V, k); B = m.B
    dec = Decoder(data)
    out = []
    for _ in range(n):
        m.begin_symbol()
        c = 1
        for j in range(B):
            p1 = m.predict_bit(c, j)
            bit = dec.decode(p1)
            m.update_bit(c, j, bit)
            c = (c << 1) | bit
        s = c - (1 << B)
        m.update_symbol(s)
        out.append(s)
    return out

# ---------- driver ----------
def run(path, nm, k):
    data = open(path, "rb").read()
    N = len(data); sha_in = hashlib.sha256(data).hexdigest()
    if nm > 0:
        cache = f"bpe{nm}.pkl"
        if os.path.exists(cache):
            seq, merges = pickle.load(open(cache, "rb"))
        else:
            seq, merges = bpe_train(data, nm)
            pickle.dump((seq, merges), open(cache, "wb"))
    else:
        seq, merges = list(data), []
    V = 256 + len(merges)
    t0 = time.time(); comp = compress(seq, V, k); enc_s = time.time() - t0
    t1 = time.time()
    seq2 = decompress(comp, len(seq), V, k)
    body = bpe_decode(seq2, merges); dec_s = time.time() - t1
    ok = hashlib.sha256(body).hexdigest() == sha_in
    dict_b = merges_bytes(merges)
    decoder_b = os.path.getsize(os.path.abspath(__file__))  # self-contained decoder
    payload = len(comp); total = payload + dict_b + decoder_b
    return dict(N=N, V=V, k=k, glyphs=len(seq), payload=payload, dict_b=dict_b,
                decoder=decoder_b, total=total, bpc_total=total * 8 / N,
                ok=ok, enc_s=enc_s, dec_s=dec_s)

if __name__ == "__main__":
    path = sys.argv[1]
    for arg in sys.argv[2:]:
        nm, k = (int(v) for v in arg.split(","))
        r = run(path, nm, k)
        line = (f"cm3t[{T1},{T2}] merges={nm:5d} k={k}  V={r['V']:5d} glyphs={r['glyphs']:7d} "
                f"payload={r['payload']:7d} dict={r['dict_b']:6d} decoder={r['decoder']} "
                f"total={r['total']:7d}  bpc_total={r['bpc_total']:.4f}  "
                f"restore={'OK' if r['ok'] else 'FAIL'}  enc={r['enc_s']:.0f}s dec={r['dec_s']:.0f}s")
        print(line, flush=True)
        with open("cm3t-sweep.log", "a") as f:
            f.write(line + "\n")
