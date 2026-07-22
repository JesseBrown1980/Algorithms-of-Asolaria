#!/usr/bin/env python3
"""
rime_fanout27.py — enwik9 divided into 27 pieces, one per RIME SECTOR of the
sphere p=103681; each sector populated, timed in exact nanoseconds, and run
through the CLOSURE LEDGER — the three bankings, measured:

  bank 0 closures, hold 2/3 -> recover 0 thirds      (nothing banked, nothing owed)
  bank 1 closure,  hold 2/3 -> recover 1/3 EXACT     (one equation, one unknown)
  bank 1 closure,  hold 1/3 -> recover 2/3 FAILS     (one equation, TWO unknowns)
  bank 2 closures, hold 1/3 -> recover 2/3 EXACT     (two equations, two unknowns)
                                but the bank IS 2/3  (net ledger: zero)

The MDS law under Law 22: you recover exactly as many thirds as you banked
closures. -1/3 gets the 2/3 only by paying the 2/3 up front. Measured, per
sector, on the real gigabyte.
"""
import numpy as np, time, json, hashlib

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
P, N = 103681, 20736
SECTORS = 27

# frozen sphere engine (same as rime_feed: Law 15)
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
g = primitive_root(P); W = pow(g, (P-1)//N, P)
pts = np.empty(N, dtype=np.int64); v = 1
for e in range(N): pts[e] = v; v = v*W % P
inv = np.empty(P+1, dtype=np.int64); inv[pts] = np.arange(N)

SZ = 1_000_000_000
SEC = SZ // SECTORS                       # 37,037,037 B per sector
f = open(f"{S}/enwik9", "rb")

def sha8(a): return hashlib.sha256(a.tobytes()).hexdigest()[:8]

sector_rows = []
t_all = time.perf_counter_ns()
mode_hits_1of3 = 0; mode_n_1of3 = 0
for d in range(SECTORS):
    t0 = time.perf_counter_ns()
    f.seek(d * SEC)
    sec = np.frombuffer(f.read(SEC), dtype=np.uint8)
    third = len(sec) // 3
    A = sec[:third].astype(np.int16)
    B = sec[third:2*third].astype(np.int16)
    C = sec[2*third:3*third].astype(np.int16)

    # ---- bank ONE closure (cost: 1/3) ----
    P1 = (-(A + B + C)) % 256
    # hold 2/3 (delete the rotating trime channel d%3), recover the 1
    lost = [A, B, C][d % 3]
    kept = [x for i, x in enumerate([A, B, C]) if i != d % 3]
    rec = (-(kept[0] + kept[1] + P1)) % 256
    exact_1 = bool(np.array_equal(rec % 256, lost % 256))

    # hold 1/3 (keep only A), attempt the 2/3: one equation, two unknowns
    guess_B = np.full_like(B, 32)                     # best order-0 guess (space)
    forced_C = (-(A + guess_B + P1)) % 256            # forced by the single equation
    hits = int(np.count_nonzero((guess_B % 256 == B % 256) & (forced_C == C % 256)))
    mode_hits_1of3 += hits; mode_n_1of3 += third

    # ---- bank TWO closures (cost: 2/3) ----
    P1b = (-(A + B)) % 256; P2b = (-(A + C)) % 256
    B2 = (-(A + P1b)) % 256; C2 = (-(A + P2b)) % 256
    exact_2 = bool(np.array_equal(B2, B % 256) and np.array_equal(C2, C % 256))

    # ---- populate this rime sector on the sphere (tower round-trip sample) ----
    samp = sec[:100000].astype(np.int64) + 256*(np.arange(100000) % 3) + 768*d
    sphere_ok = bool(np.array_equal(inv[pts[samp]], samp))

    ns = time.perf_counter_ns() - t0
    sector_rows.append(dict(sector=d, bytes=int(len(sec)), ns=int(ns),
        sha=sha8(sec), recover_1of3_exact=exact_1, pair_hits_1of3=hits,
        recover_2of3_banked2_exact=exact_2, sphere_ok=sphere_ok))
    print(f"sector {d:2d}: {len(sec):,} B  {ns/1e6:8.1f} ms  sha={sha8(sec)}  "
          f"1-closure/hold-2/3: exact={exact_1}  1-closure/hold-1/3: {hits/third*100:5.2f}%  "
          f"2-closures/hold-1/3: exact={exact_2}  sphere={sphere_ok}", flush=True)

total_ns = time.perf_counter_ns() - t_all
acc = mode_hits_1of3 / mode_n_1of3
summary = dict(sectors=SECTORS, total_bytes=int(SEC*SECTORS), total_ns=int(total_ns),
    all_1of3_exact=all(r['recover_1of3_exact'] for r in sector_rows),
    all_2of3_banked2_exact=all(r['recover_2of3_banked2_exact'] for r in sector_rows),
    all_sphere_ok=all(r['sphere_ok'] for r in sector_rows),
    hold_1of3_bank1_accuracy=acc)
json.dump(dict(summary=summary, sectors=sector_rows), open(f"{S}/rime_fanout27.json","w"), indent=1)
print(f"\nFAN-OUT COMPLETE: {SEC*SECTORS:,} B in {total_ns/1e9:.2f} s "
      f"({SEC*SECTORS/(total_ns/1e9)/1e6:.0f} MB/s)")
print(f"  bank 1, hold 2/3 -> 1/3 recovered : 27/27 sectors byte-exact = {summary['all_1of3_exact']}")
print(f"  bank 1, hold 1/3 -> 2/3 attempted : {acc*100:.2f}% (pair-exact; the guessing floor)")
print(f"  bank 2, hold 1/3 -> 2/3 recovered : 27/27 byte-exact = {summary['all_2of3_banked2_exact']}"
      f"  — but the bank IS 2/3: net zero, named")
print(f"  all 27 sectors populated on the sphere, tower round-trip = {summary['all_sphere_ok']}")
