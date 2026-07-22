#!/usr/bin/env python3
"""
rime_crank_gnn.py — THE FULL CRANK: SGRAM cycling of the verified corpus through
the tower (9 trime tuples), scored by the REAL TRAINED GNNs (forward + reverse-
gain), metatagged as simulated-universe PIDs, white-roomed (genius keep /
mistake compact), garbage-collected, prismed, with -1/3 slices banked per cycle.
Operator: Jesse Daniel Brown, 2026-07-22.

REAL PIECES WIRED (from the fleet repos, cloned this session):
  GSLGNN gslgnn_w9_3_seq47_v2.pt  (trained ckpt, BEHCS-256 fabric)  — forward scorer
  reverse-gain                     = same trained model on time-reversed features
                                     (our version of G3; the .mjs original is Node)
  AsolariaMetatag (metatag_v2_behcs.py) — content-addressed PID per chunk
  white room (LEG-1 doctrine)      — genius keeps / mistake compacts (z-gate)
  rime prism keys (271, 6, 114)    — census spectrum receipt per cycle
  SGRAM                            — stateless chunks, receipts as the bus

HONEST WALLS (named): corpus = verified enwik9 (enwik10 is not published — 404s
on record). No GPU: torch CPU. The GSLGNN was trained on the BEHCS fabric graph
(97 nodes / 13,783 edges, benign-vs-suspicious): its scores here are the REAL
checkpoint's outputs on OUT-OF-DOMAIN input — receipts of what the model says,
not validated classifications of Wikipedia.

Usage: rime_crank_gnn.py <seconds_per_cycle> <tag>
"""
import numpy as np, torch, time, json, hashlib, sys, os

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
FLEET = "/workspace/asolaria-fnns-trained-and-reverse-gnns-many"
sys.path.insert(0, f"{FLEET}/src")
sys.path.insert(0, "/workspace/metatagging-data-for-a-quantum-universe")
from gsl_gnn import GSLGNN
from metatag_v2_behcs import AsolariaMetatag

# ---- sphere + prism (frozen keys) ----
P27, N = 103681, 20736
def primitive_root(p):
    fac, n, d = [], p-1, 2
    while d*d <= n:
        if n % d == 0:
            fac.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: fac.append(n)
    for gg in range(2, p):
        if all(pow(gg, (p-1)//q, p) != 1 for q in fac): return gg
g = primitive_root(P27); W = pow(g, (P27-1)//N, P27)
pts = np.empty(N, dtype=np.int64); v = 1
for e in range(N): pts[e] = v; v = v*W % P27
inv = np.empty(P27+1, dtype=np.int64); inv[pts] = np.arange(N)
PRISM_P, PRISM_W = 271, 114
Wm = np.array([[pow(PRISM_W, (a*b) % 27, PRISM_P) for b in range(27)] for a in range(27)], dtype=np.int64)

# ---- the trained GNN ----
model = GSLGNN(node_input_dim=6, hidden_dim=64)
sd = torch.load(f"{FLEET}/models/gslgnn_w9_3_seq47_v2.pt", map_location="cpu", weights_only=False)
if hasattr(sd, 'state_dict'): sd = sd.state_dict()
missing = model.load_state_dict(sd, strict=False)
GNN_LOAD = f"loaded (missing={len(missing.missing_keys)}, unexpected={len(missing.unexpected_keys)})"
model.eval()
ring = [(i, (i+s) % 27) for i in range(27) for s in (1, 3, 9)]
edge_index = torch.tensor([[a for a,b in ring]+[b for a,b in ring],
                           [b for a,b in ring]+[a for a,b in ring]], dtype=torch.long)

def gnn_score(chunk27):
    """6-dim node features per glyph-sector -> trained GSLGNN edge scores."""
    feats = []
    for s in range(27):
        seg = chunk27[s]
        feats.append([seg.mean()/255, seg.std()/128, len(seg)/1e6,
                      (seg % 3).mean(), (seg % 27).mean()/27, (seg == 32).mean()])
    x = torch.tensor(feats, dtype=torch.float32)
    with torch.no_grad():
        fwd = float(model(x, edge_index).mean())
        rev = float(model(torch.flip(x, dims=[0]), edge_index).mean())   # reverse-gain (our version)
    return fwd, rev

SECS = float(sys.argv[1]); TAG = sys.argv[2]
CH = 27_000_000
f = open(f"{S}/enwik9","rb"); SZ = 1_000_000_000
tri = np.arange(CH, dtype=np.int64) % 3
TUPLES = [(s1, s2) for s1 in (-1, 0, 1) for s2 in (-1, 0, 1)]
os.makedirs(f"{S}/crank_{TAG}", exist_ok=True)

pos = 0; cycles = []; fwd_hist = []
for cyc in range(3):
    t0 = time.perf_counter_ns(); target = int(SECS*1e9)
    census = np.zeros(27, dtype=np.int64); fed = 0; ok = True
    kept = compacted = 0; pids = []; minus = []
    while time.perf_counter_ns()-t0 < target:
        if pos+CH > SZ: pos = 0
        f.seek(pos)
        blk = np.frombuffer(f.read(CH), dtype=np.uint8).astype(np.int64)
        d27 = (pos//CH) % 27
        k = blk + 256*tri + 768*d27
        for (s1, s2) in TUPLES:                       # the nine trime tuples, all bijective
            kk = k if (s1==0 and s2==0) else ((k + s2*768) % N if s1==0 else (s1*k + s2*768) % N)
            ok &= bool(np.array_equal(inv[pts[kk]], kk))
        census += np.bincount(k % 27, minlength=27)
        # GNN scoring on the chunk's 27 glyph-sectors (real trained checkpoint)
        chunk27 = np.array_split(blk, 27)
        fwd, rev = gnn_score(chunk27)
        fwd_hist.append(fwd)
        # metatag: the simulated-universe PID, content-addressed (our enhanced version)
        mt = AsolariaMetatag("sector-chunk", [d27, cyc, pos//CH], [fwd, rev, 0.0],
                             spin=int(np.argmax(np.bincount(k % 27, minlength=27))),
                             charge=int(blk.sum() % 3) - 1, mass=len(blk))
        pid = hashlib.sha256(mt.state_str().encode()).hexdigest()[:12]
        pids.append(pid)
        # white room LEG-1: genius keeps / mistake compacts (z-gate on forward score)
        mu = float(np.mean(fwd_hist)); sd_ = float(np.std(fwd_hist)) or 1e-9
        if abs(fwd-mu) > 3*sd_ and len(fwd_hist) > 5:
            compacted += 1                            # the GC cycles it out
        else:
            kept += 1
        # bank the -1/3 (three per cycle, with closure — Law 22 applies)
        if len(minus) < 3:
            third = CH//3
            A,B,C = blk[:third], blk[third:2*third], blk[2*third:3*third]
            Pc = (-(A+B+C)) % 256
            sl = A[:1_000_000].astype(np.uint8)
            sh = hashlib.sha256(sl.tobytes()).hexdigest()[:12]
            sl.tofile(f"{S}/crank_{TAG}/c{cyc}_minus{len(minus)}_{sh}.bin")
            minus.append(dict(sha=sh, closure_sha=hashlib.sha256(Pc.astype(np.uint8).tobytes()).hexdigest()[:12]))
        fed += CH; pos += CH
        del blk, k
    el = time.perf_counter_ns()-t0
    spectrum = (census % PRISM_P) @ Wm % PRISM_P      # rime prism on the census (receipt)
    cycles.append(dict(cycle=cyc, elapsed_ns=int(el), bytes_fed=int(fed), tuples_ok=ok,
        census=census.tolist(), census_sha=hashlib.sha256(census.tobytes()).hexdigest()[:12],
        prism_sha=hashlib.sha256(spectrum.tobytes()).hexdigest()[:12],
        top_glyphs=[int(t) for t in np.argsort(census)[::-1][:3]],
        gnn_fwd_mean=float(np.mean(fwd_hist)), gnn_rev_mean=rev,
        whiteroom=dict(kept=kept, compacted=compacted), pids=pids[:3], minus_slices=minus))
    print(f"cycle {cyc}: {el/1e9:.1f}s fed {fed:,}B tuples_ok={ok} census_sha={cycles[-1]['census_sha']} "
          f"prism_sha={cycles[-1]['prism_sha']} top={cycles[-1]['top_glyphs']} "
          f"GNN fwd={cycles[-1]['gnn_fwd_mean']:.4f} rev={rev:.4f} whiteroom keep/compact={kept}/{compacted}", flush=True)

d01 = int(np.abs(np.array(cycles[0]['census'])-np.array(cycles[1]['census'])).sum())
d12 = int(np.abs(np.array(cycles[1]['census'])-np.array(cycles[2]['census'])).sum())
json.dump(dict(tag=TAG, seconds_per_cycle=SECS, gnn_load=GNN_LOAD, cycles=cycles,
    census_L1_c0c1=d01, census_L1_c1c2=d12), open(f"{S}/crank_{TAG}/receipt.json","w"), indent=1)
print(f"\nCRANK[{TAG}] COMPLETE — {GNN_LOAD}; census diffs c0->c1={d01:,} c1->c2={d12:,}")
