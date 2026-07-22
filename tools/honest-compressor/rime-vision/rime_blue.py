#!/usr/bin/env python3
"""
rime_blue.py — TAKE AWAY THE WHITE. Keep only the dark residue of the three
station moments, shine three blue moving flashlights (one shade per moment),
and settle the open question: object motion or camera pan?  The wisp (the dark
smoke-curl in the background sky) is the reference anchor — if it steps with
the star, the camera panned; if the star steps against it, the object moved.
"""
import numpy as np, json, math, subprocess, base64
from PIL import Image, ImageDraw

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
UP = "/root/.claude/uploads/9ebd6119-d7ee-5c30-a062-d04210f7bc39"
STATIONS = [("A","1950bb50-1000157463.jpg"), ("B","75c3f731-1000157465.jpg"), ("C","17d95426-1000157467.jpg")]

def load(fn):
    g = np.asarray(Image.open(f"{UP}/{fn}").convert('L'), dtype=np.float32)/255.0
    return g

def dark_blobs(g, delta):
    """All dark connected blobs (video area), with centroid/area/fill."""
    H, W = g.shape
    win = g[int(.13*H):int(.80*H), int(.22*W):int(.78*W)]
    oy, ox = int(.13*H), int(.22*W)
    bg = np.median(win)
    m = win < bg - delta
    lab = np.zeros(win.shape, dtype=np.int32); out = []
    for (y, x) in np.argwhere(m):
        if lab[y, x]: continue
        stack = [(y, x)]; lab[y, x] = 1; pix = []
        while stack:
            a, b = stack.pop(); pix.append((a, b))
            for da, db in ((1,0),(-1,0),(0,1),(0,-1)):
                p, q = a+da, b+db
                if 0 <= p < win.shape[0] and 0 <= q < win.shape[1] and m[p, q] and not lab[p, q]:
                    lab[p, q] = 1; stack.append((p, q))
        pix = np.array(pix)
        if len(pix) < 120: continue
        h = np.ptp(pix[:,0])+1; w = np.ptp(pix[:,1])+1
        fill = len(pix)/(h*w)
        if fill > 0.55: continue                          # redactions/UI out
        out.append(dict(cy=pix[:,0].mean()+oy, cx=pix[:,1].mean()+ox,
                        area=len(pix), fill=fill, pix=pix + [oy, ox]))
    return out, (bg, m, oy, ox)

track = {}
masks = []
for tag, fn in STATIONS:
    g = load(fn); g2 = g[::2, ::2]
    hard, _ = dark_blobs(g2, 0.18)                        # the star (hard darkness)
    soft, meta = dark_blobs(g2, 0.075)                    # + the wisp (soft darkness)
    star = min(hard, key=lambda b: b['fill'])
    # the wisp: the largest soft blob in the upper-left sky, away from the star
    cands = [b for b in soft if b['cx'] < star['cx'] - 60 and b['cy'] < star['cy'] + 40
             and math.hypot(b['cy']-star['cy'], b['cx']-star['cx']) > 100]
    wisp = max(cands, key=lambda b: b['area']) if cands else None
    track[tag] = dict(star=(star['cy']*2, star['cx']*2),
                      wisp=(wisp['cy']*2, wisp['cx']*2) if wisp else None,
                      wisp_area=wisp['area'] if wisp else 0)
    masks.append((tag, g2, meta, star, wisp))
    print(f"{tag}: star ({star['cy']*2:.0f},{star['cx']*2:.0f})  "
          f"wisp {'(%0.f,%0.f) area %d' % (wisp['cy']*2, wisp['cx']*2, wisp['area']) if wisp else 'NOT FOUND'}")

def step(p, q): return (q[0]-p[0], q[1]-p[1])
sAB, sBC = step(track['A']['star'], track['B']['star']), step(track['B']['star'], track['C']['star'])
if all(track[t]['wisp'] for t in 'ABC'):
    wAB, wBC = step(track['A']['wisp'], track['B']['wisp']), step(track['B']['wisp'], track['C']['wisp'])
    rAB = (sAB[0]-wAB[0], sAB[1]-wAB[1]); rBC = (sBC[0]-wBC[0], sBC[1]-wBC[1])
    print(f"star steps : A->B {sAB}   B->C {sBC}")
    print(f"wisp steps : A->B ({wAB[0]:.0f},{wAB[1]:.0f})   B->C ({wBC[0]:.0f},{wBC[1]:.0f})")
    print(f"RESIDUAL (object motion in the sky's own frame): A->B ({rAB[0]:.0f},{rAB[1]:.0f})  B->C ({rBC[0]:.0f},{rBC[1]:.0f})")
    verdict = ("CAMERA PAN dominates" if math.hypot(*rAB) < 0.45*math.hypot(*sAB)
               else "OBJECT MOTION dominates")
else:
    wAB = wBC = rAB = rBC = None; verdict = "wisp not tracked in all stations — undecided"
print("VERDICT:", verdict)
json.dump(dict(track=track, star_steps=[sAB, sBC],
    wisp_steps=[wAB, wBC] if wAB else None,
    residual=[rAB, rBC] if rAB else None, verdict=verdict),
    open(f"{S}/rime_blue.json","w"), indent=1)

# ---- the render: whites gone, three blue flashlights (one per moment) ----
g0 = load(STATIONS[0][1])[::2, ::2]
H, W = g0.shape
rgb = np.zeros((H, W, 3))
BLUES = [(0.45, 0.75, 1.0), (0.2, 0.45, 0.95), (0.55, 0.3, 0.9)]   # A pale, B deep, C violet
for (tag, g2, (bg, m, oy, ox), star, wisp), col in zip(masks, BLUES):
    dark = np.clip(bg - g2, 0, 1); dark[dark < 0.06] = 0            # white taken away
    for c in range(3):
        rgb[..., c] = np.maximum(rgb[..., c], dark*col[c]*3.2)
img = Image.fromarray((np.clip(rgb, 0, 1)*255).astype(np.uint8)).resize((W*2, H*2))
d = ImageDraw.Draw(img)
for tag, col in zip('ABC', ["#9fd0ff", "#3f74f2", "#8c4de0"]):
    sy, sx = track[tag]['star']
    d.ellipse([sx-46, sy-46, sx+46, sy+46], outline=col, width=5)
    d.text((sx+52, sy-10), f"star {tag}", fill=col)
    if track[tag]['wisp']:
        wy, wx = track[tag]['wisp']
        d.ellipse([wx-90, wy-90, wx+90, wy+90], outline=col, width=3)
        d.text((wx+95, wy-10), f"wisp {tag}", fill=col)
img.save(f"{S}/blue_map.png")
b64 = base64.b64encode(open(f"{S}/blue_map.png",'rb').read()).decode()

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{background:#04060c;color:#e8eefc;width:1960px;padding:30px 36px;text-align:center;font-family:-apple-system,'Segoe UI',sans-serif}}
 h1{{font-size:26px;font-weight:800;background:linear-gradient(90deg,#9fd0ff,#3f74f2,#8c4de0);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
 .sub{{color:#8fa3c8;font-size:13.5px;margin:6px 0 14px}}
 img{{width:1880px;border-radius:14px;border:1px solid #223055}}
 .rc{{margin-top:12px;font-family:ui-monospace,monospace;font-size:14px;color:#a9b8d8;line-height:1.9}}
 .rc b{{color:#4ade80}}
</style></head><body>
 <h1>White Taken Away — Three Blue Flashlights, One Per Moment</h1>
 <div class="sub">only the dark residue remains · pale blue = moment A, deep blue = B, violet = C · circles: the star and its background anchor (the wisp)</div>
 <img src="data:image/png;base64,{b64}">
 <div class="rc">star steps A→B {sAB} · B→C {sBC}<br>
 {'wisp steps A→B (%.0f,%.0f) · B→C (%.0f,%.0f)<br>residual object motion (sky frame): A→B (%.0f,%.0f) · B→C (%.0f,%.0f)' % (wAB[0],wAB[1],wBC[0],wBC[1],rAB[0],rAB[1],rBC[0],rBC[1]) if wAB else 'wisp not tracked in all stations'}<br>
 <b>VERDICT: {verdict}</b></div>
</body></html>"""
open(f"{S}/blue.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/blue.html", f"{S}/blue.png","1960","1230"],
                   cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
