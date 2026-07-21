#!/usr/bin/env python3
"""
glyph_invent.py — invent 256/1024/4096/16384-glyph languages by deterministic BPE,
train the vocab on the head of the corpus, then MEASURE over the FULL corpus:
  - byte-exact restore (glyphs -> bytes == original sha256)
  - order-0 (unigram) and order-1 (previous-glyph) empirical entropy over glyphs
  - merge TABLE charged into the total; bpc over ORIGINAL bytes
Deterministic: merge tie-break = lowest (a,b); table sha256 is reproducible.

usage: glyph_invent.py <corpus> <train_bytes> <out_prefix>
"""
import sys, os, re, time, math, json, hashlib, struct, heapq
from collections import Counter

CORPUS      = sys.argv[1]
TRAIN_BYTES = int(sys.argv[2]) if len(sys.argv) > 2 else 50_000_000
OUT         = sys.argv[3] if len(sys.argv) > 3 else "glyph_out"
TIERS       = [256, 1024, 4096, 16384]     # number of INVENTED glyphs (merges)
MAXM        = max(TIERS)
LOG2        = math.log2

def log(m): print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)

WORD_RE = re.compile(rb"\s+|\S+")

# ───────────────────────── TRAIN (efficient incremental BPE) ─────────────────
def train(sample):
    log(f"train: pretokenize {len(sample):,} B")
    freqs = Counter(m.group() for m in WORD_RE.finditer(sample))
    # words as mutable lists of symbol-ids; keep parallel freq
    words = [list(w) for w in freqs.keys()]
    wfreq = list(freqs.values())
    log(f"train: {len(words):,} unique words")

    pair_cnt = Counter()
    pair_where = {}   # pair -> set(word_idx)
    for wi, w in enumerate(words):
        f = wfreq[wi]
        for a, b in zip(w, w[1:]):
            p = (a, b)
            pair_cnt[p] += f
            s = pair_where.get(p)
            if s is None: pair_where[p] = s = set()
            s.add(wi)

    # max-heap via (-count, a, b): pops highest count, tie-break lowest (a,b). lazy-invalidated.
    heap = [(-c, p[0], p[1]) for p, c in pair_cnt.items()]
    heapq.heapify(heap)

    def push(p):
        c = pair_cnt.get(p, 0)
        if c > 0: heapq.heappush(heap, (-c, p[0], p[1]))

    merges = []
    for k in range(MAXM):
        # pop until a non-stale top (count matches current)
        best = None
        while heap:
            nc, a0, b0 = heap[0]
            p = (a0, b0)
            if pair_cnt.get(p, 0) == -nc and -nc > 0:
                best = p; break
            heapq.heappop(heap)
        if best is None: break
        new_id = 256 + k
        merges.append(best)
        a, b = best
        touched = set()
        for wi in list(pair_where.get(best, ())):
            w = words[wi]; f = wfreq[wi]
            # remove this word's old pair contributions
            for x, y in zip(w, w[1:]):
                p = (x, y); pair_cnt[p] -= f
                if pair_cnt[p] <= 0: pair_cnt.pop(p, None); pair_where.pop(p, None)
                else:
                    s = pair_where.get(p)
                    if s is not None: s.discard(wi)
            # merge all occurrences of (a,b) in w
            nw = []; i = 0; L = len(w)
            while i < L:
                if i < L-1 and w[i] == a and w[i+1] == b:
                    nw.append(new_id); i += 2
                else:
                    nw.append(w[i]); i += 1
            words[wi] = nw
            # add new pair contributions
            for x, y in zip(nw, nw[1:]):
                p = (x, y); pair_cnt[p] += f
                s = pair_where.get(p)
                if s is None: pair_where[p] = s = set()
                s.add(wi)
                touched.add(p)
        pair_cnt.pop(best, None); pair_where.pop(best, None)
        for p in touched: push(p)
        if (k+1) in (256,1024,4096,16384) or (k+1) % 4000 == 0:
            log(f"train: {k+1} merges done")
    return merges

# ───────────────────────── APPLY (bpe tokenize a word) ───────────────────────
def make_ranks(merges):
    return {pair: i for i, pair in enumerate(merges)}

def tokenize_word(wb, ranks, cache):
    t = cache.get(wb)
    if t is not None: return t
    sym = list(wb)
    while len(sym) >= 2:
        best = None; br = 1 << 30
        for i in range(len(sym)-1):
            r = ranks.get((sym[i], sym[i+1]))
            if r is not None and r < br: br = r; best = i
        if best is None: break
        nid = 256 + br
        sym[best:best+2] = [nid]
    tt = tuple(sym); cache[wb] = tt; return tt

# expand a glyph id back to bytes (for restore)
def build_expand(merges):
    exp = {}
    def ex(sid):
        if sid < 256: return bytes([sid])
        v = exp.get(sid)
        if v is not None: return v
        a, b = merges[sid-256]
        v = ex(a) + ex(b); exp[sid] = v; return v
    for k in range(len(merges)): ex(256+k)
    return exp

# ───────────────────────── MEASURE one tier over full corpus ─────────────────
def measure_tier(n_glyphs, merges_full, data, byte_sha):
    merges = merges_full[:n_glyphs]
    ranks  = make_ranks(merges)
    expand = build_expand(merges)
    cache  = {}
    uni = Counter()             # order-0
    bi  = Counter()             # order-1 (prev,cur)
    ntok = 0
    prev = -1
    resh = hashlib.sha256()
    # single streaming pass over words in corpus order (lazy finditer, no giant list)
    for m in WORD_RE.finditer(data):
        wb = m.group()
        toks = tokenize_word(wb, ranks, cache)
        # restore bytes
        for sid in toks:
            resh.update(expand[sid] if sid >= 256 else bytes([sid]))
        # counts
        for sid in toks:
            uni[sid] += 1
            if prev >= 0: bi[(prev, sid)] += 1
            prev = sid
        ntok += len(toks)
    restore_ok = (resh.hexdigest() == byte_sha)

    N = ntok
    # order-0 entropy bits
    h0 = 0.0
    for c in uni.values():
        p = c / N; h0 -= c * LOG2(p)
    # order-1 conditional entropy bits: sum -log2 p(cur|prev)
    ctx = Counter()
    for (pv, cu), c in bi.items(): ctx[pv] += c
    h1 = 0.0
    for (pv, cu), c in bi.items():
        h1 -= c * LOG2(c / ctx[pv])
    # first token has no context -> charge order-0 self-info (uni)
    # (negligible; add its unigram cost)
    # table cost: serialize merges as 2x uint32 each
    tbl = b"".join(struct.pack("<II", a, b) for (a, b) in merges)
    tbl_bytes = len(tbl)
    tbl_sha = hashlib.sha256(tbl).hexdigest()[:16]

    orig_bytes = len(data)
    bpc0 = (h0 + tbl_bytes*8) / orig_bytes
    bpc1 = (h1 + tbl_bytes*8) / orig_bytes
    return {
        "invented_glyphs": n_glyphs,
        "distinct_symbols_used": len(uni),
        "n_tokens": N,
        "bytes_per_token": round(orig_bytes / N, 4),
        "restore_ok": restore_ok,
        "order0_bpc": round(bpc0, 4),
        "order1_bpc": round(bpc1, 4),
        "table_bytes": tbl_bytes,
        "table_sha16": tbl_sha,
    }

# ───────────────────────── byte baseline (order-0/1 over bytes) ──────────────
def byte_baseline(data):
    N = len(data)
    uni = Counter(data)
    h0 = -sum(c*LOG2(c/N) for c in uni.values())
    bi = Counter(zip(data, data[1:]))
    ctx = Counter()
    for (p, c), n in bi.items(): ctx[p] += n
    h1 = -sum(n*LOG2(n/ctx[p]) for (p, c), n in bi.items())
    return {"order0_bpc": round(h0/N, 4), "order1_bpc": round(h1/N, 4)}

def main():
    t0 = time.time()
    log(f"reading {CORPUS}")
    with open(CORPUS, "rb") as f: data = f.read()
    byte_sha = hashlib.sha256(data).hexdigest()
    log(f"corpus {len(data):,} B  sha={byte_sha[:16]}")

    base = byte_baseline(data)
    log(f"byte baseline: order0={base['order0_bpc']} order1={base['order1_bpc']}")

    sample = data[:TRAIN_BYTES]
    merges = train(sample)
    log(f"invented {len(merges)} glyphs total; measuring tiers {TIERS}")

    results = {"corpus": CORPUS, "corpus_bytes": len(data), "corpus_sha": byte_sha,
               "train_bytes": TRAIN_BYTES, "byte_baseline": base, "tiers": []}
    # smallest tier first: bank results progressively; a late-tier OOM can't wipe earlier tiers
    for n in sorted(TIERS):
        if n > len(merges):
            log(f"skip tier {n}: only {len(merges)} merges invented"); continue
        log(f"── measuring tier {n} glyphs over full corpus ──")
        try:
            r = measure_tier(n, merges, data, byte_sha)
        except Exception as e:
            log(f"tier {n} FAILED: {type(e).__name__}: {e}")
            results["tiers"].append({"invented_glyphs": n, "error": f"{type(e).__name__}: {e}"})
            with open(OUT + ".json", "w") as f: json.dump(results, f, indent=2)
            continue
        results["tiers"].append(r)
        log(f"tier {n}: order1_bpc={r['order1_bpc']} order0_bpc={r['order0_bpc']} "
            f"restore={r['restore_ok']} tok={r['n_tokens']:,} table={r['table_bytes']}B")
        with open(OUT + ".json", "w") as f: json.dump(results, f, indent=2)
        log(f"snapshot written -> {OUT}.json")
    results["elapsed_sec"] = round(time.time()-t0, 1)
    results["tiers"].sort(key=lambda r: r["invented_glyphs"])
    with open(OUT + ".json", "w") as f: json.dump(results, f, indent=2)
    log(f"DONE in {results['elapsed_sec']}s -> {OUT}.json")

if __name__ == "__main__":
    main()
