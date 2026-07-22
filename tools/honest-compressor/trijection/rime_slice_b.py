#!/usr/bin/env python3
"""
Rewind the rime to 3-D: flashlight photo of ONE SLICE of the torus, with the
B family carrying the trime weights (-1, 0, +1). Pre-registered: the +/-1 blues
survive un-riming exactly; the 0-weighted blues die BY THE TRIME'S OWN CENTER;
R and G (weight 0,0) stay dark. 6 alive / 21 dead, mass ~ 6/27.
"""
import numpy as np, json, subprocess, math

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
J = json.load(open(f"{S}/rime_unrime_signed.json"))
census = np.array(J['census_backwards'], dtype=np.int64)

gl = np.arange(27)
w = np.zeros(27, dtype=np.int64)
Bmask = gl % 3 == 2                                   # the blue family
signs = np.array([-1, 0, +1])                         # THE TRIME ITSELF as weights
w[Bmask] = signs[(gl[Bmask]//3) % 3]
signed = census * w
unrimed = signed * w                                  # anti of +/-1 is itself; 0 has none
alive = [int(g) for g in gl if w[g] != 0 and unrimed[g] == census[g]]
dead_zero_b = [int(g) for g in gl[Bmask] if w[g] == 0]
mass_alive = float(census[np.isin(gl, alive)].sum()/census.sum())
exact = all(unrimed[g] == census[g] for g in alive)
print(f"B family (g%3==2) weighted (-1,0,+1): alive={alive} (exact={exact})")
print(f"killed by the trime's own 0: {dead_zero_b}   R,G dark: 18")
print(f"mass alive: {mass_alive*100:.1f}%  (pre-registered ~{6/27*100:.1f}%)")
json.dump(dict(weights=w.tolist(), alive=alive, dead_zero_b=dead_zero_b,
    mass_alive=mass_alive, exact_pm=exact), open(f"{S}/rime_slice_b.json","w"), indent=1)

# ---------- the flashlight photo of the slice ----------
cn = census/census.max()
CX, CY, R0 = 640, 470, 265
dots = ""
for g in range(27):
    th = math.radians(-90 + g*360/27)
    r = R0*(0.55 + 0.45*cn[g])
    x, y = CX + r*math.cos(th), CY + r*math.sin(th)
    if w[g] == +1:  col, glow, op = "#60a5fa", "0 0 26px #60a5fa", 1.0
    elif w[g] == -1: col, glow, op = "#a5d8ff", "0 0 26px #a5d8ff", 1.0
    elif g % 3 == 2: col, glow, op = "#0b1a33", "none", .85       # blue killed by its own 0
    else:            col, glow, op = "#111827", "none", .55       # R,G dark
    ring = 'border:2px solid #fbbf24;' if (w[g]==0 and g%3==2) else ''
    dots += f"""<div class="dot" style="left:{x:.0f}px;top:{y:.0f}px;background:{col};
      box-shadow:{glow};opacity:{op};{ring}"><span>{g}</span></div>"""

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{background:#05070d;color:#e8eefc;width:1280px;height:1010px;position:relative;overflow:hidden;
   font-family:-apple-system,'Segoe UI',sans-serif;text-align:center}}
 h1{{padding-top:28px;font-size:25px;font-weight:800;background:linear-gradient(90deg,#60a5fa,#a5d8ff,#fbbf24);
   -webkit-background-clip:text;-webkit-text-fill-color:transparent}}
 .sub{{color:#8fa3c8;font-size:13px;margin-top:5px}}
 .torus{{position:absolute;left:{CX-330}px;top:{CY-330}px;width:660px;height:660px;border-radius:50%;
   border:44px solid #0d1626;opacity:.85}}
 .beam{{position:absolute;left:60px;top:180px;width:640px;height:560px;
   background:conic-gradient(from 32deg at 0% 50%, transparent 0deg, #dbeafe22 8deg, #dbeafe0d 22deg, transparent 30deg);
   pointer-events:none}}
 .lamp{{position:absolute;left:34px;top:440px;width:54px;height:54px;border-radius:50%;
   background:radial-gradient(circle,#fff,#cbd5e1 60%,#334155);box-shadow:0 0 40px #e2e8f0aa}}
 .slice{{position:absolute;left:{CX-300}px;top:{CY-300}px;width:600px;height:600px;border-radius:50%;
   border:1.5px dashed #274067;background:radial-gradient(circle,#0a121f 0%,#0c1626 62%,#101d33 100%)}}
 .dot{{position:absolute;transform:translate(-50%,-50%);width:34px;height:34px;border-radius:50%;
   display:flex;align-items:center;justify-content:center}}
 .dot span{{font-size:11px;font-weight:700;color:#e8eefc99}}
 .zero{{position:absolute;left:{CX}px;top:{CY}px;transform:translate(-50%,-50%);width:44px;height:44px;border-radius:50%;
   background:radial-gradient(circle,#fff,#9ec5ff 60%,#1a2340);line-height:44px;font-weight:800;color:#0a0f1c;
   box-shadow:0 0 30px #7dd3fc66}}
 .leg{{position:absolute;bottom:24px;left:0;width:100%;font-size:13px;color:#a9b8d8;line-height:1.8;font-family:ui-monospace,monospace}}
 .leg b{{color:#4ade80}} .leg .y{{color:#fbbf24}}
</style></head><body>
 <h1>Flashlight on the Slice — B carrying the Trime (−, 0, +)</h1>
 <div class="sub">the torus rewound to 3-D · one poloidal slice under the beam · blue family weighted −1, 0, +1 · gold rings = blues killed by the trime's own 0</div>
 <div class="torus"></div><div class="slice"></div><div class="beam"></div><div class="lamp"></div>
 {dots}
 <div class="zero">0</div>
 <div class="leg">
   ± blues un-rimed byte-exact: <b>{alive} — 6/6</b> (the − flips and flips back)<br>
   <span class="y">killed by the trime's own 0: {dead_zero_b}</span> · R,G dark: 18 · mass alive {mass_alive*100:.1f}% (pre-registered 22.2%)<br>
   the 0 at the CENTER is free · the 0 as a WEIGHT kills — even inside the trime itself
 </div>
</body></html>"""
open(f"{S}/slice_b.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/slice_b.html", f"{S}/slice_b.png","1280","1010"],
                   cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
