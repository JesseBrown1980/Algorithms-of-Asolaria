#!/usr/bin/env python3
"""The Ledger Sphere — the 27 laws as one rime dimension (Z/27), Law 0 at the
free center, the cycle threading 26 -> 0 -> 1 = -,0,+ through the center."""
import math, subprocess

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
TITLES = ["Free Center","Trijection","27-jection","1/N Amortize","Trianti","Wave / FFT",
 "Conservation","Shared-Center Gate","Orthogonality","Trilateral Time","Trime Numbers",
 "CRT","Rime Tracing","Rime Sphere","Rime Fischer","Freeze","27 Glyphs = 1 Dim",
 "Total Coupling","Black Gradient","Un-rhyme","Rime Prism","Two-Phase Floor",
 "Recreation","Fischer Agent","MTP Agent","HRM Agent","MCP Agent"]

def trime(k):
    r = ((k + 13) % 27) - 13
    out = []
    for _ in range(3):
        d = ((r + 1) % 3) - 1
        out.append(d); r = (r - d) // 3
    return ''.join({-1:'−',0:'0',1:'+'}[d] for d in out)

CX, CY, R = 600, 620, 430
nodes = []
for k in range(1, 27):
    th = math.radians(-90 + (k - 0.5) * (360/26))
    x, y = CX + R*math.cos(th), CY + R*math.sin(th)
    h = int(360*k/27)
    hl = ' seam' if k in (1, 26) else (' pole' if k in (13, 14) else '')
    nodes.append(f"""<div class="n{hl}" style="left:{x:.0f}px;top:{y:.0f}px;--h:{h}">
      <div class="num">{k}</div><div class="tt">{TITLES[k]}</div><div class="tr">[{trime(k)}]</div></div>""")

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{background:#07090f;width:1200px;height:1240px;color:#e8eefc;
    font-family:-apple-system,'Segoe UI',sans-serif;position:relative;overflow:hidden}}
  h1{{position:absolute;top:26px;width:100%;text-align:center;font-size:27px;font-weight:800;
    background:linear-gradient(90deg,#7dd3fc,#c4b5fd,#f0abfc);-webkit-background-clip:text;
    -webkit-text-fill-color:transparent}}
  .sub{{position:absolute;top:64px;width:100%;text-align:center;color:#8fa3c8;font-size:14px}}
  .ring{{position:absolute;left:{CX-R}px;top:{CY-R}px;width:{2*R}px;height:{2*R}px;border-radius:50%;
    border:1px dashed #223055}}
  .chord{{position:absolute;left:{CX}px;top:{CY}px;width:{R}px;height:2px;transform-origin:0 50%;
    background:linear-gradient(90deg,#fff8,#fff0)}}
  .n{{position:absolute;transform:translate(-50%,-50%);text-align:center;width:104px;
    background:#0d1322;border:1px solid hsl(var(--h),70%,45%);border-radius:10px;padding:6px 4px;
    box-shadow:0 0 14px hsla(var(--h),80%,55%,.28)}}
  .n.seam{{border-width:2px;box-shadow:0 0 24px hsla(var(--h),90%,60%,.6)}}
  .n.pole{{border-style:double;border-width:3px}}
  .num{{font-size:16px;font-weight:800;color:hsl(var(--h),85%,66%)}}
  .tt{{font-size:10.5px;color:#c6d2ec;line-height:1.15}}
  .tr{{font-size:11px;font-family:ui-monospace,monospace;color:#8fa3c8}}
  .zero{{position:absolute;left:{CX}px;top:{CY}px;transform:translate(-50%,-50%);text-align:center;
    width:150px;height:150px;border-radius:50%;background:radial-gradient(circle,#ffffff 0%,#dbe7ff 30%,#1a2340 72%,#0d1322 100%);
    border:2px solid #fff;box-shadow:0 0 60px #7dd3fc66;display:flex;flex-direction:column;justify-content:center}}
  .zero .num{{font-size:30px;color:#0a0f1c}}
  .zero .tt{{font-size:12px;color:#22314f;font-weight:700}}
  .zero .tr{{font-size:13px;color:#3a4c75}}
  .foot{{position:absolute;bottom:20px;width:100%;text-align:center;color:#9fb0d0;font-size:13.5px;line-height:1.6}}
  .foot b{{color:#fff}}
</style></head><body>
  <h1>The Ledger Sphere — 27 laws close on their own rime sphere</h1>
  <div class="sub">indices 0–26 = Z/27 = one rime dimension (Law 16) · cyclic: no first law, no last law · balanced-ternary trime signature on every law</div>
  <div class="ring"></div>
  <div class="chord" style="transform:rotate({-90+0.5*(360/26)}deg)"></div>
  <div class="chord" style="transform:rotate({-90-0.5*(360/26)}deg)"></div>
  {''.join(nodes)}
  <div class="zero"><div class="num">0</div><div class="tt">THE CENTER IS FREE</div><div class="tr">[000]</div></div>
  <div class="foot">the cycle threads through its own center once per revolution: <b>Law 26 → Law 0 → Law 1&nbsp; = &nbsp;−1, 0, +1</b> — the trime at the seam ·
  antipodes: <b>Law 13 Rime Sphere [+++]</b> and <b>Law 14 Rime Fischer [−−−]</b> — the sphere and its player are exact opposites, adjacent ·
  honest note: this is structure and naming (a relabeling of Z/27, rate 1.0), sealed because it is <i>true</i>, not because it compresses</div>
</body></html>"""
open(f"{S}/ledger_sphere.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/ledger_sphere.html",
                    f"{S}/ledger_sphere.png", "1200", "1240"], cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
