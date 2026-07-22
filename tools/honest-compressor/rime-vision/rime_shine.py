#!/usr/bin/env python3
"""
rime_shine.py — SHINE the 13 uploaded frames at the trimes, reverted to the
3-sided triangle level, for 27 seconds of rime-time winds.
Per frame: extract the bright points (the stars), fit the LEVEL-3 triangle
(three brightest), draw every line of the constellation, measure angles/ratios.
The 27 s of winds = repeated deterministic passes; identical results each pass
(sha receipt) or the run is void. Honest scope: geometry of the lights only —
this measures shapes and lines; it does not and cannot identify the object.
"""
import numpy as np, time, json, hashlib, math, os, subprocess, base64, zlib, struct
from PIL import Image, ImageDraw

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
UP = "/root/.claude/uploads/9ebd6119-d7ee-5c30-a062-d04210f7bc39"
FILES = ["58b7ff86-1000157276.jpg","7f251ffa-1000157272.jpg","a40f7e29-1000157270.jpg",
         "bfa3c3a2-1000157274.jpg","5c6f8351-1000157280.jpg","2049a08b-1000157262.jpg",
         "a711c694-1000157258.jpg","fb65b77a-1000157256.jpg","95511f79-1000157254.jpg",
         "702cac7d-1000157230.jpg","9ea1076e-1000157228.jpg","2d2d2a12-1000157222.jpg",
         "1728d892-1000157218.jpg"]

def blobs(gray):
    """Bright connected components on black; returns [(cy,cx,area,peak)] sorted by mass."""
    thr = max(float(gray.mean() + 3*gray.std()), 0.55*float(gray.max()))
    m = gray > thr
    lab = np.zeros(gray.shape, dtype=np.int32); nxt = 0; out = []
    idx = np.argwhere(m)
    for (y, x) in idx:
        if lab[y, x]: continue
        nxt += 1; stack = [(y, x)]; lab[y, x] = nxt; pix = []
        while stack:
            a, b = stack.pop(); pix.append((a, b))
            for da, db in ((1,0),(-1,0),(0,1),(0,-1)):
                p, q = a+da, b+db
                if 0 <= p < gray.shape[0] and 0 <= q < gray.shape[1] and m[p, q] and not lab[p, q]:
                    lab[p, q] = nxt; stack.append((p, q))
        pix = np.array(pix)
        if len(pix) < 6: continue
        w = gray[pix[:,0], pix[:,1]]
        out.append((float((pix[:,0]*w).sum()/w.sum()), float((pix[:,1]*w).sum()/w.sum()),
                    int(len(pix)), float(w.max())))
    return sorted(out, key=lambda b: -b[2])

def tri_metrics(P):
    (y1,x1),(y2,x2),(y3,x3) = P
    a = math.hypot(x2-x3, y2-y3); b = math.hypot(x1-x3, y1-y3); c = math.hypot(x1-x2, y1-y2)
    sides = sorted([a,b,c])
    def ang(o, p, q):
        v1 = (p[1]-o[1], p[0]-o[0]); v2 = (q[1]-o[1], q[0]-o[0])
        cosv = (v1[0]*v2[0]+v1[1]*v2[1])/(math.hypot(*v1)*math.hypot(*v2)+1e-12)
        return math.degrees(math.acos(max(-1,min(1,cosv))))
    A = sorted([ang(P[0],P[1],P[2]), ang(P[1],P[0],P[2]), ang(P[2],P[0],P[1])])
    return dict(ratio=[1.0, sides[1]/sides[0], sides[2]/sides[0]], angles=A)

# ---- 27 seconds of rime-time winds: repeat the whole pass, demand identical shas ----
t0 = time.perf_counter_ns(); passes = 0; sha_prev = None; results = None
while time.perf_counter_ns() - t0 < 27_000_000_000:
    res = []
    for fn in FILES:
        im = Image.open(f"{UP}/{fn}").convert('L')
        g = np.asarray(im, dtype=np.float32)/255.0
        g = g[::2, ::2]                                   # wind down (2x)
        bl = blobs(g)
        r = dict(file=fn[:8], n=len(bl), blobs=[(round(b[0]*2,1), round(b[1]*2,1), b[2]) for b in bl[:6]])
        if len(bl) >= 3:
            P = [(bl[i][0]*2, bl[i][1]*2) for i in range(3)]
            r.update(tri_metrics(P))
        res.append(r)
    sha = hashlib.sha256(json.dumps(res, sort_keys=True).encode()).hexdigest()[:12]
    assert sha_prev is None or sha == sha_prev, "non-deterministic pass!"
    sha_prev = sha; results = res; passes += 1
el = time.perf_counter_ns() - t0
print(f"27 s of rime-time winds: {passes} full passes over {len(FILES)} frames, "
      f"every pass identical (sha {sha_prev})  elapsed {el/1e9:.1f}s")
for r in results:
    line = f"  {r['file']}: {r['n']} stars"
    if 'angles' in r:
        line += f"  L3-triangle angles {[round(a) for a in r['angles']]}  side-ratios {[round(x,2) for x in r['ratio']]}"
    print(line)
json.dump(dict(passes=passes, sha=sha_prev, frames=results), open(f"{S}/rime_shine.json","w"), indent=1)

# ---- draw the shapes and their lines (overlay contact sheet) ----
COLS, TH_W = 4, 470
rows = math.ceil(len(FILES)/COLS)
sheet = Image.new('RGB', (COLS*TH_W, rows*260), (7, 9, 15))
for i, (fn, r) in enumerate(zip(FILES, results)):
    im = Image.open(f"{UP}/{fn}").convert('RGB')
    W0, H0 = im.size
    d = ImageDraw.Draw(im)
    pts = [(b[1], b[0]) for b in r['blobs']]              # (x,y)
    for j, (x, y) in enumerate(pts):                       # all lines of the constellation
        for (x2, y2) in pts[j+1:]:
            d.line([(x, y), (x2, y2)], fill=(90, 200, 255), width=3)
    if len(pts) >= 3:                                      # the LEVEL-3 triangle, bold
        tri = pts[:3] + [pts[0]]
        d.line(tri, fill=(255, 210, 80), width=6)
    for (x, y) in pts:
        rr = 16
        d.ellipse([x-rr, y-rr, x+rr, y+rr], outline=(255, 95, 122), width=5)
    th = im.resize((TH_W, int(TH_W*H0/W0)))
    sheet.paste(th, ((i % COLS)*TH_W, (i//COLS)*260))
sheet.save(f"{S}/shine_sheet.png")

def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
angset = [r['angles'] for r in results if 'angles' in r]
med = np.median(np.array(angset), axis=0) if angset else [0,0,0]
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{background:#07090f;color:#e8eefc;width:1960px;padding:30px 36px;text-align:center;font-family:-apple-system,'Segoe UI',sans-serif}}
 h1{{font-size:26px;font-weight:800;background:linear-gradient(90deg,#ffd166,#7dd3fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
 .sub{{color:#8fa3c8;font-size:13.5px;margin:6px 0 16px}}
 img{{width:1890px;border-radius:14px;border:1px solid #223055}}
 .foot{{margin-top:14px;font-size:13px;color:#9fb0d0;line-height:1.65;max-width:1700px;margin:14px auto 0}}
 .foot b{{color:#fff}}
</style></head><body>
 <h1>The Shapes and Their Lines — 13 frames, triangle level, {passes} winds in 27 s</h1>
 <div class="sub">red rings = the stars found · blue = every line of the constellation · gold = the level-3 triangle (three brightest) ·
   every pass identical, sha {sha_prev}</div>
 <img src="data:image/png;base64,{b64(f'{S}/shine_sheet.png')}">
 <div class="foot"><b>Measured:</b> median level-3 triangle angles ≈ {[round(float(a)) for a in med]}° · the constellation is
 3–5 warm stars on a dark angular hull · <b>honest scope:</b> this measures the geometry of the lights and their lines — it does
 not identify the object; the horizontal scanline weave in every frame says these are frames re-filmed from a video screen.</div>
</body></html>"""
open(f"{S}/shine.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/shine.html", f"{S}/shine.png","1960", str(140+rows*260+90)],
                   cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
