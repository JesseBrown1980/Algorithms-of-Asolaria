#!/usr/bin/env python3
"""The Crank Constellation — 3 cycles x 27 glyph-stars, from crank_s300 receipts."""
import json, math, subprocess
import numpy as np

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
J = json.load(open(f"{S}/crank_s300/receipt.json"))
CX, CY = 620, 560
RADII = [180, 320, 460]
stars = []
for cyc, c in enumerate(J['cycles']):
    cen = np.array(c['census'], dtype=float)
    lum = np.log1p(cen); lum = lum/lum.max() if lum.max() else lum
    for gld in range(27):
        th = math.radians(-90 + gld*360/27 + cyc*4.4)
        x = CX + RADII[cyc]*math.cos(th); y = CY + RADII[cyc]*math.sin(th)
        h = int(360*gld/27); l = lum[gld]
        sz = 6 + 16*l
        top = gld in c['top_glyphs']
        stars.append(f"""<div class="st{' tp' if top else ''}" style="left:{x:.0f}px;top:{y:.0f}px;
          width:{sz:.0f}px;height:{sz:.0f}px;--h:{h};opacity:{0.25+0.75*l:.2f}"></div>""")
rings = "".join(f'<div class="ring" style="left:{CX-r}px;top:{CY-r}px;width:{2*r}px;height:{2*r}px"></div>' for r in RADII)
legend = "".join(f"""<div class="lg"><b>cycle {c['cycle']}</b> · {c['bytes_fed']//1_000_000} MB ·
  census {c['census_sha'][:8]} · prism {c['prism_sha'][:8]} · top {c['top_glyphs']} ·
  keep/compact {c['whiteroom']['kept']}/{c['whiteroom']['compacted']} · PID {c['pids'][0]}</div>""" for c in J['cycles'])

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{background:radial-gradient(circle at 50% 46%, #0b1020 0%, #05070d 70%);color:#e8eefc;
   width:1240px;height:1180px;font-family:-apple-system,'Segoe UI',sans-serif;position:relative;overflow:hidden}}
 h1{{position:absolute;top:24px;width:100%;text-align:center;font-size:25px;font-weight:800;
   background:linear-gradient(90deg,#7dd3fc,#c4b5fd,#f0abfc);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
 .sub{{position:absolute;top:58px;width:100%;text-align:center;color:#8fa3c8;font-size:13px}}
 .ring{{position:absolute;border:1px dashed #223055;border-radius:50%}}
 .st{{position:absolute;transform:translate(-50%,-50%);border-radius:50%;
   background:radial-gradient(circle,#fff 0%,hsl(var(--h),90%,65%) 45%,transparent 75%);
   box-shadow:0 0 12px hsla(var(--h),90%,60%,.8)}}
 .st.tp{{box-shadow:0 0 22px hsla(var(--h),95%,65%,1), 0 0 40px hsla(var(--h),90%,60%,.5)}}
 .zero{{position:absolute;left:{CX}px;top:{CY}px;transform:translate(-50%,-50%);width:56px;height:56px;
   border-radius:50%;background:radial-gradient(circle,#fff,#9ec5ff 55%,#1a2340 100%);
   box-shadow:0 0 40px #7dd3fc99;text-align:center;line-height:56px;font-weight:800;color:#0a0f1c}}
 .leg{{position:absolute;bottom:70px;left:0;width:100%;text-align:center;font-size:12px;color:#a9b8d8;line-height:1.7}}
 .lg{{font-family:ui-monospace,monospace}}
 .foot{{position:absolute;bottom:18px;width:100%;text-align:center;font-size:11.5px;color:#66779c}}
</style></head><body>
 <h1>The Crank Constellation — 300 s, 3 cycles, scored by the trained GNNs</h1>
 <div class="sub">each ring = one cycle · each star = one glyph-sector (hue = glyph, brightness = census mass) ·
   1,188,000,000 bytes cranked · every chunk 9-tuple bijective · GNN fwd/rev = real gslgnn_w9_3_seq47_v2.pt outputs</div>
 {rings}{''.join(stars)}
 <div class="zero">0</div>
 <div class="leg">{legend}</div>
 <div class="foot">honest: GNN scores are the real checkpoint's outputs on out-of-domain input (trained on the BEHCS fabric, not Wikipedia) —
   receipts of what the model says, not validated judgments · −1/3 slices banked with closures, 3 per cycle · the 2700 s crank is running now</div>
</body></html>"""
open(f"{S}/constellation.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/constellation.html",
                    f"{S}/constellation.png", "1240", "1180"], cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
