#!/usr/bin/env python3
"""
rime_backoff_test.py — does depth REALLY level off at order 5, or is that "the wave"
(an artifact of a no-backoff estimator)? Test: build order-k counts up to K on a
slice, then measure held-out bpc TWO ways per order:
  (a) NO BACKOFF  : unseen context -> uniform 1/256 (what the 6h run did)
  (b) WITH BACKOFF: unseen context -> fall back to deepest seen shorter context (PPM-ish)
If (a) ticks up at 5 but (b) keeps dropping, Jesse is right: depth never stops;
the level-off was the measurement giving up, not the information running out.
"""
import time, math
from collections import defaultdict

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
CORPUS = f"{S}/enwik9"
NTRAIN = 12_000_000
NHELD  = 1_000_000
KMAX   = 7

raw = open(CORPUS, 'rb').read(NTRAIN + NHELD)
train = raw[:NTRAIN]; held = raw[NTRAIN:NTRAIN+NHELD]
t0 = time.time()

# build counts for orders 0..KMAX: counts[k][context_bytes] -> {byte: n, total}
# memory-bounded: use dict of dict; contexts as bytes keys of length k
print(f"training orders 0..{KMAX} on {NTRAIN:,} B ...", flush=True)
counts = [defaultdict(lambda: defaultdict(int)) for _ in range(KMAX+1)]
tot = [defaultdict(int) for _ in range(KMAX+1)]
for i in range(KMAX, NTRAIN):
    b = train[i]
    for k in range(KMAX+1):
        ctx = train[i-k:i]
        counts[k][ctx][b] += 1
        tot[k][ctx] += 1
    if i % 20_000_000 == 0 and i: print(f"  trained {i:,} ({time.time()-t0:.0f}s)", flush=True)
print(f"trained ({time.time()-t0:.0f}s)\n", flush=True)

def bpc_no_backoff(K):
    bits = 0.0
    for i in range(K, NHELD):
        b = held[i]; ctx = held[i-K:i]
        d = counts[K].get(ctx)
        if d is not None:
            p = (d.get(b,0) + 1) / (tot[K][ctx] + 256)
        else:
            p = 1/256                      # GIVE UP -> 8 bits (the artifact)
        bits += -math.log2(p)
    return bits/(NHELD-K)

def bpc_backoff(K):
    bits = 0.0
    for i in range(K, NHELD):
        b = held[i]
        # use deepest order <= K whose context was actually seen
        p = None
        for k in range(K, -1, -1):
            ctx = held[i-k:i]
            d = counts[k].get(ctx)
            if d is not None:
                p = (d.get(b,0) + 1) / (tot[k][ctx] + 256)
                break
        if p is None: p = 1/256
        bits += -math.log2(p)
    return bits/(NHELD-K)

print(f"{'order':>5} | {'NO backoff':>11} | {'WITH backoff':>12}")
print("-"*34)
prev_nb = prev_bo = None
for K in range(1, KMAX+1):
    nb = bpc_no_backoff(K); bo = bpc_backoff(K)
    fnb = "" if prev_nb is None else ("  UP" if nb>prev_nb else "")
    fbo = "" if prev_bo is None else ("  UP" if bo>prev_bo else "")
    print(f"{K:>5} | {nb:>11.4f}{fnb:<4} | {bo:>12.4f}{fbo:<4}", flush=True)
    prev_nb, prev_bo = nb, bo
print(f"\n({time.time()-t0:.0f}s total)")
