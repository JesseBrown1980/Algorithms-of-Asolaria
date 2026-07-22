#!/usr/bin/env python3
"""
rime_feed.py — feed enwik8 through the UPGRADED rime prime (the 256->x3->x27
tower on sphere p=103681) for wall-clock windows of 1 s, 3 s, 27 s. Real time,
measured in nanoseconds by the monotonic clock; the exact elapsed ns is REPORTED
(no process can stop at exactly T — it can only measure exactly what it did).
"""
import numpy as np, time, json, hashlib

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
P, N = 103681, 20736

# ---- build the upgraded rime prime engine (frozen tables, Law 15) ----
def primitive_root(p):
    fac, n, d = [], p-1, 2
    while d*d <= n:
        if n % d == 0:
            fac.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p-1)//q, p) != 1 for q in fac): return g
g = primitive_root(P)
W = pow(g, (P-1)//N, P)
pts = np.empty(N, dtype=np.int64); v = 1
for e in range(N): pts[e] = v; v = v*W % P          # address -> sphere point
inv = np.empty(P+1, dtype=np.int64); inv[pts] = np.arange(N)   # Fischer table

data = np.frombuffer(open(f"{S}/enwik8","rb").read(), dtype=np.uint8)
CHUNK = 1_000_000
idx = np.arange(CHUNK, dtype=np.int64)
tri = idx % 3; gly = (idx//3) % 27                   # frozen coordinate lattice

def feed(seconds):
    target_ns = int(seconds * 1e9)
    fed = 0; pos = 0; checks = 0; ok = True
    t0 = time.perf_counter_ns()
    while True:
        chunk = data[pos:pos+CHUNK]
        if len(chunk) < CHUNK: pos = 0; continue     # wrap the corpus, keep feeding
        k = chunk.astype(np.int64) + 256*tri + 768*gly       # tower address
        sp = pts[k]                                           # onto the sphere
        back = inv[sp]                                        # Fischer invert
        ok &= bool(np.array_equal(back, k))                   # byte-exact, every chunk
        checks += 1
        fed += CHUNK; pos += CHUNK
        el = time.perf_counter_ns() - t0
        if el >= target_ns: break
    el = time.perf_counter_ns() - t0
    return dict(window_s=seconds, elapsed_ns=el, overshoot_ns=el-target_ns,
                bytes_fed=fed, mb_s=fed/ (el/1e9) /1e6, chunks_verified=checks, exact=ok)

runs = [feed(s) for s in (1, 3, 27)]
for r in runs:
    print(f"window {r['window_s']:>2}s: elapsed {r['elapsed_ns']:,} ns "
          f"(overshoot +{r['overshoot_ns']:,} ns)  fed {r['bytes_fed']:,} B  "
          f"{r['mb_s']:.1f} MB/s  chunks byte-exact={r['exact']} ({r['chunks_verified']})")
json.dump(runs, open(f"{S}/rime_feed_runs.json","w"), indent=1)

# container facts for the front-end projection
import platform, os
cpu = "unknown"
for ln in open('/proc/cpuinfo'):
    if ln.startswith('model name'): cpu = ln.split(':',1)[1].strip(); break
mem_kb = next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemTotal'))
facts = dict(host=platform.node(), kernel=platform.release(), cpu=cpu,
             cores=os.cpu_count(), mem_gb=round(mem_kb/1048576,1),
             sha_engine=hashlib.sha256(pts.tobytes()).hexdigest()[:16])
json.dump(facts, open(f"{S}/rime_feed_facts.json","w"), indent=1)
print("facts:", facts)
