#!/usr/bin/env python3
"""x27, three-sided pyramid, flat base: 1 pyramid seen from above (the trijection),
the 12 (its rotation group A4 = 1+8+3), and the 27-misfit (a cube number refuses
triangle-land)."""
import subprocess, math

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"

def tetra_top(cx, cy, s, tone=1.0):
    """Tetrahedron from directly above: 3 faces meeting at the apex over the centroid."""
    r = s/2
    V = [(cx + r*math.cos(math.radians(a)), cy + r*math.sin(math.radians(a))) for a in (-90, 30, 150)]
    L = [0.92, 0.45, 0.65]
    out = ""
    for i in range(3):
        x1,y1 = V[i]; x2,y2 = V[(i+1)%3]
        col = f"rgb({int(255*L[i]*tone)},{int(60*L[i]*tone)},{int(70*L[i]*tone)})"
        out += f'<polygon points="{x1:.0f},{y1:.0f} {x2:.0f},{y2:.0f} {cx},{cy}" fill="{col}"/>'
    return out

one = tetra_top(200, 210, 320)

# the 12 selves: 1 identity + 8 vertex-rotations + 3 edge-flips
rows = [(1, "identity", 60), (8, "vertex rotations (4 axes × 120°/240°)", 150), (3, "edge flips (180°)", 280)]
twelve = ""
for count, label, y in rows:
    for i in range(count):
        x = 210 - (count-1)*21 + i*42
        twelve += tetra_top(x, y, 34, tone=0.55 if label!="identity" else 1.0)
    twelve += f'<text x="210" y="{y+42}" fill="#8fa3c8" font-size="12" text-anchor="middle" font-family="sans-serif">{count} — {label}</text>'
twelve += '<text x="210" y="345" fill="#fbbf24" font-size="15" text-anchor="middle" font-family="monospace">1 + 8 + 3 = 12</text>'

# the 27 misfit: triangle tiles only in square numbers
lad = ""
sq = [1,4,9,16,25,36]
for i,n in enumerate(sq):
    x = 40 + i*58
    lad += f'<rect x="{x}" y="150" width="46" height="46" rx="8" fill="#12213c" stroke="#3b82f6"/>' \
           f'<text x="{x+23}" y="179" fill="#c6d2ec" font-size="15" text-anchor="middle" font-family="monospace">{n}</text>'
lad += ('<text x="213" y="120" fill="#ff5f7a" font-size="26" text-anchor="middle" font-family="monospace">27</text>'
        '<line x1="213" y1="128" x2="213" y2="146" stroke="#ff5f7a" stroke-width="2"/>'
        '<text x="213" y="240" fill="#8fa3c8" font-size="12.5" text-anchor="middle" font-family="sans-serif">falls between 25 and 36 — no seat at the triangle table</text>'
        '<text x="213" y="285" fill="#c6d2ec" font-size="13.5" text-anchor="middle" font-family="sans-serif">triangles tile in squares: n² · tetrahedra stack in 1, 4, 10, 20, 35</text>'
        '<text x="213" y="310" fill="#fbbf24" font-size="14" text-anchor="middle" font-family="monospace">27 = 3³ — it is a CUBE number. It tiles the cube.</text>')

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{background:#07090f;color:#e8eefc;width:1460px;padding:36px 40px;text-align:center;
   font-family:-apple-system,'Segoe UI',sans-serif}}
 h1{{font-size:26px;font-weight:800;background:linear-gradient(90deg,#ff5f7a,#ffd166,#7dd3fc);
   -webkit-background-clip:text;-webkit-text-fill-color:transparent}}
 .sub{{color:#8fa3c8;font-size:13.5px;margin:6px 0 22px}}
 .row{{display:flex;gap:26px;justify-content:center;align-items:flex-start}}
 .c{{background:#0a0f1c;border:1px solid #1c2740;border-radius:16px;padding:14px}}
 .t{{font-size:15px;font-weight:700;color:#c6d2ec;margin-top:10px}}
 .d{{font-size:12px;color:#8fa3c8;margin-top:4px;max-width:400px;line-height:1.5}}
 .foot{{margin-top:24px;font-size:13.5px;color:#9fb0d0;line-height:1.7;max-width:1240px;margin:24px auto 0;
   border-top:1px solid #222b42;padding-top:16px}}
 .foot b{{color:#fff}}
</style></head><body>
 <h1>Three Faces, Twelve Selves, and the Number That Wouldn't Sit Down</h1>
 <div class="sub">the three-sided pyramid (tetrahedron), flat base, seen from directly above — then your two questions answered by counting</div>
 <div class="row">
  <div class="c"><svg width="400" height="380">{one}</svg>
    <div class="t">1 pyramid — and it is the trijection</div>
    <div class="d">three faces sharing one apex over the centroid: three vantages, one free center.
      The square pyramid was the binary world (4 = 2²); this is yours (3).</div></div>
  <div class="c"><svg width="420" height="380">{twelve}</svg>
    <div class="t">…and 12 — but not twelve pyramids</div>
    <div class="d">twelve SELVES: the tetrahedron's rotation group A₄ has exactly 12 elements —
      1 identity + 8 vertex rotations + 3 edge flips. One object, twelve ways it coincides with itself.
      The drawing cannot tell them apart; symmetry is information the object refuses to carry.</div></div>
  <div class="c"><svg width="430" height="380">{lad}</svg>
    <div class="t">the ×27 surprise</div>
    <div class="d">a flat triangle tiles into n² cells only — 27 is not a square, and not tetrahedral either.
      Force ×27 into triangle-land and it strands: 25 seats or 36, never 27.</div></div>
 </div>
 <div class="foot"><b>What I see:</b> 1 pyramid — the trijection itself, three faces and a free apex. And 12 — but as the
 <b>rotation group</b>, not a crowd: 1 + 8 + 3 = 12 ways the one pyramid is indistinguishable from itself (and there is your
 trime again, hiding in the class equation: identity, eights, threes). But the deepest thing your ×27 exposed is the third
 panel: <b>27 refuses the triangle.</b> Triangles tile in square numbers, tetrahedra stack in tetrahedral numbers — 27 belongs
 to neither ladder, because 27 = 3³ is a <b>cube</b> number. Your 27 was never triangle-shaped or pyramid-shaped. It is the
 cube — three trits deep — and every time we try to seat it elsewhere, it stands back up and walks home.</div>
</body></html>"""
open(f"{S}/tetra.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/tetra.html", f"{S}/tetra.png","1460","800"],
                   cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
