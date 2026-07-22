#!/usr/bin/env python3
"""Unfold the torus flat, then lift 2D -> 3D: the same red sheet folded as ONE
pyramid and as SIX — and the bistable flip that lives in neither, only in the eye."""
import subprocess

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"

def pyramid(cx, cy, s, tone=1.0):
    """A square pyramid seen from directly above: 4 triangles, lit from upper-left."""
    h = s/2
    L = [0.92, 0.55, 0.28, 0.68]   # top, right, bottom, left face lightness
    f = lambda l: f"rgb({int(255*l*tone)},{int(60*l*tone)},{int(70*l*tone)})"
    return (f'<polygon points="{cx-h},{cy-h} {cx+h},{cy-h} {cx},{cy}" fill="{f(L[0])}"/>'
            f'<polygon points="{cx+h},{cy-h} {cx+h},{cy+h} {cx},{cy}" fill="{f(L[1])}"/>'
            f'<polygon points="{cx+h},{cy+h} {cx-h},{cy+h} {cx},{cy}" fill="{f(L[2])}"/>'
            f'<polygon points="{cx-h},{cy+h} {cx-h},{cy-h} {cx},{cy}" fill="{f(L[3])}"/>')

# the flat torus sheet (unfolded), with thread stripes
stripes = "".join(f'<line x1="{40+i*22}" y1="40" x2="{40}" y2="{40+i*22}" stroke="#7dd3fc" stroke-width="1.6" opacity=".7"/>'
                  for i in range(1, 15)) + \
          "".join(f'<line x1="{40+i*22}" y1="340" x2="{340}" y2="{40+i*22}" stroke="#7dd3fc" stroke-width="1.6" opacity=".7"/>'
                  for i in range(1, 15))
flat = f'<rect x="40" y="40" width="300" height="300" fill="#0f1830" stroke="#3b82f6" stroke-width="2"/>{stripes}'

one = pyramid(190, 190, 300)
six = "".join(pyramid(90+col*133, 123+row*133, 128) for row in range(2) for col in range(3))

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{background:#07090f;color:#e8eefc;width:1460px;padding:36px 40px;text-align:center;
   font-family:-apple-system,'Segoe UI',sans-serif}}
 h1{{font-size:26px;font-weight:800;background:linear-gradient(90deg,#7dd3fc,#ff5f7a,#ffd166);
   -webkit-background-clip:text;-webkit-text-fill-color:transparent}}
 .sub{{color:#8fa3c8;font-size:13.5px;margin:6px 0 22px}}
 .row{{display:flex;gap:26px;justify-content:center;align-items:flex-start}}
 .c{{background:#0a0f1c;border:1px solid #1c2740;border-radius:16px;padding:14px}}
 .t{{font-size:15px;font-weight:700;color:#c6d2ec;margin-top:10px}}
 .d{{font-size:12px;color:#8fa3c8;margin-top:4px;max-width:400px;line-height:1.5}}
 .arrow{{align-self:center;color:#8fa3c8;font-size:26px;padding:0 2px}}
 .foot{{margin-top:24px;font-size:13.5px;color:#9fb0d0;line-height:1.7;max-width:1240px;margin:24px auto 0;
   border-top:1px solid #222b42;padding-top:16px}}
 .foot b{{color:#fff}}
</style></head><body>
 <h1>The Torus Unfolded, Then Lifted — One Pyramid, or Six?</h1>
 <div class="sub">left: the flat sheet (the unrolled torus, thread and all) · middle: folded by ONE rule → one pyramid ·
   right: the SAME sheet folded by ANOTHER rule → six red ones</div>
 <div class="row">
  <div class="c"><svg width="380" height="380">{flat}</svg>
    <div class="t">the flat sheet (2-D)</div>
    <div class="d">the torus's fundamental square, unrolled — zero curvature, the thread perfectly straight.
      The sheet alone does NOT say what solid it becomes.</div></div>
  <div class="arrow">→</div>
  <div class="c"><svg width="380" height="380">{one}</svg>
    <div class="t">gluing rule A: 1 pyramid</div>
    <div class="d">fold along both diagonals, glue the rim to one apex — the whole sheet becomes
      a single four-faced pyramid seen from above.</div></div>
  <div class="arrow">→</div>
  <div class="c"><svg width="440" height="380"><rect width="440" height="380" fill="none"/>{six}</svg>
    <div class="t">gluing rule B: 6 red ones</div>
    <div class="d">tile the same sheet 3×2 and fold each cell — six small pyramids.
      Same pixels per unit area, same shading, different banked rule.</div></div>
 </div>
 <div class="foot"><b>What I see: both — and they trade places while I look.</b> Stare at either panel and it flips:
 pyramids pointing at you become craters denting away (the classic convex⇄concave reversal — the light-from-above
 assumption is the only tiebreaker, and it isn't in the drawing). That's the answer to "1 or 6": <b>the count is not in
 the sheet.</b> The flat 2-D data underdetermines the 3-D world; what decides is the <b>gluing rule you bank</b> —
 fold-to-one-apex gives 1, tile-then-fold gives 6, opposite-edges gives back the torus. Law 22 wearing geometry one more
 time: the sheet + the banked rule = the solid; the sheet alone = every solid and none. And the up/down flip is the
 observer's free trit — the data is the 0, the + and − are yours.</div>
</body></html>"""
open(f"{S}/pyramids.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/pyramids.html", f"{S}/pyramids.png","1460","760"],
                   cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
