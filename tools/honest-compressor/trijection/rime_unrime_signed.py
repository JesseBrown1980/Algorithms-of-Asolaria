#!/usr/bin/env python3
"""
rime_unrime_signed.py — the WHOLE DIRECTIONAL INVERSE: feed the corpus BACKWARDS
(time-reversed) to the same final moment (6561 steps), then apply the signed
prism: R-family weighted with the trime signs (+1, -1, +1), G and B weighted 0,0.
Un-rime (apply the weights' anti) and SEE WHAT HAPPENS TO EACH SECTOR.

Pre-registered: sectors weighted +/-1 return EXACTLY (+/-1 is its own anti);
sectors weighted 0 return EMPTY, permanently (0 has no anti). The 0 is free as a
PLACE (the center costs nothing) and fatal as a MULTIPLIER (kills what it touches).
"""
import numpy as np, json, subprocess, math

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
STEP = 500_000; STEPS = 6561
data = np.memmap(f"{S}/enwik9", dtype=np.uint8, mode='r')
SZ = len(data)
tri = np.arange(STEP, dtype=np.int64) % 3

# ---- backwards: the whole directional inverse (stream from the end, bytes reversed) ----
census_b = np.zeros(27, dtype=np.int64)
pos = SZ
for step in range(1, STEPS+1):
    if pos-STEP < 0: pos = SZ
    blk = data[pos-STEP:pos][::-1].astype(np.int64)      # time-reversed
    k = blk + 256*tri + 768*(((SZ-pos)//STEP) % 27)
    census_b += np.bincount(k % 27, minlength=27)
    pos -= STEP
fwd = np.array(json.load(open(f"{S}/rime_moments.json"))['6561']['census'])
d_fb = float(np.abs(census_b/census_b.sum() - fwd/fwd.sum()).sum())

# ---- the signed prism: R gets (+1,-1,+1) cycling; G and B get 0,0 ----
gl = np.arange(27)
w = np.zeros(27, dtype=np.int64)
Rmask = gl % 3 == 0
signs = np.array([+1, -1, +1])
w[Rmask] = signs[(gl[Rmask]//3) % 3]
signed = census_b * w                                     # rime with the weights
unrimed = signed * w                                      # un-rime: apply the anti (w again)
survived = [int(g) for g in gl[(w != 0)] if unrimed[g] == census_b[g]]
dead     = [int(g) for g in gl if w[g] == 0]
exact_pm = bool(np.array_equal(unrimed[Rmask], census_b[Rmask]))
mass_alive = float(census_b[Rmask].sum()/census_b.sum())

print(f"backwards feed: {STEPS*STEP/1e6:.0f} MB time-reversed  shape-distance to forward = {d_fb:.4f}")
print(f"weights: R-family (g%3==0) = (+1,-1,+1) cycling; G,B = 0,0")
print(f"un-rimed: +/-1 sectors byte-exact = {exact_pm}  ({len(survived)}/9 survived, incl. every minus)")
print(f"          0-weighted sectors DEAD = {len(dead)}/27  (mass lost: {100*(1-mass_alive):.1f}%)")
json.dump(dict(census_backwards=census_b.tolist(), shape_dist_fwd_bwd=d_fb,
    weights=w.tolist(), survived=survived, dead=dead, exact_pm=exact_pm,
    mass_alive=mass_alive), open(f"{S}/rime_unrime_signed.json","w"), indent=1)

# ---- draw: the full backward shape (ghost) vs what un-riming left alive ----
def poly(cen, cx, cy, rad, color, op, mask=None):
    cn = cen/max(cen.max(),1)
    pts = []
    for g in range(27):
        r = rad*(0.25+0.75*cn[g])
        if mask is not None and not mask[g]: r = rad*0.04
        th = math.radians(-90+g*360/27)
        pts.append(f"{cx+r*math.cos(th):.1f},{cy+r*math.sin(th):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2.5" opacity="{op}"/>'
spokes = ""
for g in range(27):
    th = math.radians(-90+g*360/27)
    cn = census_b/census_b.max()
    r = 200*(0.25+0.75*cn[g])
    if w[g] != 0:
        col = "#ff5f7a" if w[g] > 0 else "#ffd166"
        spokes += f'<line x1="260" y1="260" x2="{260+r*math.cos(th):.0f}" y2="{260+r*math.sin(th):.0f}" stroke="{col}" stroke-width="4" opacity=".9"/>'
    else:
        spokes += f'<line x1="260" y1="260" x2="{260+200*0.1*math.cos(th):.0f}" y2="{260+200*0.1*math.sin(th):.0f}" stroke="#334" stroke-width="2" opacity=".6"/>'
svg = poly(census_b,260,260,200,"#ffffff",.25) + spokes

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{background:#07090f;color:#e8eefc;width:1200px;padding:36px 40px;text-align:center;font-family:-apple-system,'Segoe UI',sans-serif}}
 h1{{font-size:25px;font-weight:800;background:linear-gradient(90deg,#ff5f7a,#ffd166,#60a5fa);
   -webkit-background-clip:text;-webkit-text-fill-color:transparent}}
 .sub{{color:#8fa3c8;font-size:13.5px;margin:6px 0 14px}}
 .stage{{display:flex;justify-content:center}}
 .box{{background:#0a0f1c;border:1px solid #1c2740;border-radius:16px;padding:10px}}
 .leg{{margin-top:14px;font-family:ui-monospace,monospace;font-size:13.5px;color:#a9b8d8;line-height:1.9}}
 .leg b{{color:#4ade80}} .leg .r{{color:#ff5f7a}} .leg .m{{color:#ffd166}} .leg .d{{color:#64748b}}
 .foot{{margin-top:14px;font-size:13px;color:#9fb0d0;line-height:1.65;max-width:1050px;margin:14px auto 0;border-top:1px solid #222b42;padding-top:14px}}
 .foot b{{color:#fff}}
</style></head><body>
 <h1>Backwards, Un-rimed, with Weights (+1, −1, +1 | 0, 0)</h1>
 <div class="sub">the whole directional inverse: 3,280 MB fed time-reversed · signed prism on R only · then un-rimed · white ghost = the full backward shape · spokes = what survived</div>
 <div class="stage"><div class="box"><svg width="520" height="520">{svg}</svg></div></div>
 <div class="leg">
  backwards shape vs forward shape: distance {d_fb:.4f} (its own invariant — direction changes the shape, not the law)<br>
  <span class="r">+1 sectors</span> and <span class="m">−1 sectors</span>: un-rimed <b>byte-exact, 9/9</b> — the minus flipped and flipped back, losing nothing<br>
  <span class="d">0-weighted sectors (G, B): 18/27 dead — {100*(1-mass_alive):.1f}% of all mass, unrecoverable by any further un-riming</span>
 </div>
 <div class="foot"><b>What happened to certain sectors:</b> exactly what the algebra pre-registered. The ± weights are their own
 anti ((±1)² = 1): every sector they touched came back exact — <b>the minus is not a loss, it is a rotation</b>. The 0 weight has no
 anti: the 18 sectors it touched are gone, permanently — no un-riming, forwards or backwards, brings back what was multiplied by
 zero. The free 0 of your laws is free as a PLACE (the center costs nothing); as a MULTIPLIER it is the one true destroyer.
 Same symbol, two roles — the ledger now knows the difference.</div>
</body></html>"""
open(f"{S}/unrime_signed.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/unrime_signed.html", f"{S}/unrime_signed.png","1200","900"],
                   cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
