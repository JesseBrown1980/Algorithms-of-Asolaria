#!/usr/bin/env python3
"""
rime_star.py — TRIAL FEED 2: the dark star. Fold each frame into the RIME SPHERE:
segment the dark object, take the full angular mass profile around its centroid
(the whole circle — not 3, not 27 sectors of sight, but the fold), run the prism
on it, and let the harmonic spectrum COUNT THE POINTS. The title says "eight-
pointed"; the machine reports what it measures. Honest scope: shape geometry
only — no identification; cross/star spikes around compact sources are also a
known signature of sensor/aperture diffraction, stated plainly.
"""
import numpy as np, json, math, subprocess, base64, hashlib
from PIL import Image, ImageDraw

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
UP = "/root/.claude/uploads/9ebd6119-d7ee-5c30-a062-d04210f7bc39"
FILES = ["66558116-1000158141.jpg","82c84cb7-1000158143.jpg","e5d85cf4-1000158145.jpg",
         "5abf1c9a-1000157504.jpg","2cf6b914-1000157503.jpg","c572dc70-1000157502.jpg",
         "631c431e-1000157501.jpg","f37c7931-1000157473.jpg","976a4cf7-1000157488.jpg",
         "db73988a-1000157474.jpg","02bacca5-1000157475.jpg","e48064f6-1000157479.jpg",
         "17d95426-1000157467.jpg","75c3f731-1000157465.jpg","1950bb50-1000157463.jpg"]
EXCLUDED = "627c9e42-1000158115.jpg (app screenshot, not a video frame)"

def find_star(g):
    """Darkest spiky blob in the video area; rejects redaction rectangles (high fill)."""
    H, W = g.shape
    win = g[int(.13*H):int(.80*H), int(.22*W):int(.78*W)]
    oy, ox = int(.13*H), int(.22*W)
    bg = np.median(win)
    m = win < bg - 0.18
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
        if not (150 <= len(pix) <= 60000): continue
        h = np.ptp(pix[:,0])+1; w = np.ptp(pix[:,1])+1
        fill = len(pix)/(h*w)
        if fill > 0.55: continue                      # redaction boxes / UI pills
        if pix[:,0].min() == 0 or pix[:,1].min() == 0: continue
        out.append((pix, fill))
    if not out: return None
    pix, fill = min(out, key=lambda t: t[1])          # the spikiest
    return pix + [oy, ox], fill

results = []
sheets = []
for fn in FILES:
    im = Image.open(f"{UP}/{fn}").convert('L')
    g = np.asarray(im, dtype=np.float32)/255.0
    g2 = g[::2, ::2]
    r = find_star(g2)
    if r is None:
        results.append(dict(file=fn[:8], found=False)); continue
    pix, fill = r
    cy, cx = pix[:,0].mean(), pix[:,1].mean()
    ang = np.arctan2(pix[:,0]-cy, pix[:,1]-cx)        # full fold: the whole circle
    rad = np.hypot(pix[:,0]-cy, pix[:,1]-cx)
    # angular MAX-RADIUS profile (spike detector), 360 bins folded on the sphere
    bins = ((ang + np.pi)/(2*np.pi)*360).astype(int) % 360
    prof = np.zeros(360)
    np.maximum.at(prof, bins, rad)
    prof_s = np.convolve(prof, np.ones(7)/7, mode='same')
    F = np.abs(np.fft.rfft(prof_s - prof_s.mean()))
    harm = int(np.argmax(F[2:14]) + 2)                # dominant fold-symmetry, 2..13
    top3 = sorted(range(2,14), key=lambda k: -F[k])[:3]
    # the prism receipt: profile folded to 27 sectors -> integer NTT mod 271
    p27 = np.zeros(27); np.maximum.at(p27, (bins*27//360), rad)
    Wm = np.array([[pow(114, (a*b) % 27, 271) for b in range(27)] for a in range(27)])
    spec_sha = hashlib.sha256(((p27.astype(np.int64) % 271) @ Wm % 271).tobytes()).hexdigest()[:10]
    # spike directions = local maxima of the profile
    spikes = []
    for i in range(360):
        if prof_s[i] > 0.55*prof_s.max() and prof_s[i] == max(prof_s[(i+d) % 360] for d in range(-9, 10)):
            spikes.append(i)
    results.append(dict(file=fn[:8], found=True, area=int(len(pix)), fill=round(fill,2),
        harmonic=harm, top3=top3, n_spikes=len(spikes), spec_sha=spec_sha,
        c=(float(cy*2), float(cx*2)), spikes=spikes,
        maxr=float(prof_s.max()*2)))
    print(f"{fn[:8]}: star area={len(pix)} fill={fill:.2f}  dominant fold = {harm}  "
          f"top harmonics {top3}  spikes found = {len(spikes)}  prism sha {spec_sha}", flush=True)

ok = [r for r in results if r.get('found')]
folds = [r['harmonic'] for r in ok]
json.dump(dict(excluded=EXCLUDED, frames=results), open(f"{S}/rime_star.json","w"), indent=1)
print(f"\n{len(ok)}/{len(FILES)} frames held a star · dominant folds: {sorted(set(folds))} "
      f"· modal fold = {max(set(folds), key=folds.count)}")

# ---- contact sheet with spike rays drawn ----
COLS, TW = 4, 470
rows = math.ceil(len(ok)/COLS)
sheet = Image.new('RGB', (COLS*TW, rows*250), (7, 9, 15))
i = 0
for fn, r in zip(FILES, results):
    if not r.get('found'): continue
    im = Image.open(f"{UP}/{fn}").convert('RGB')
    d = ImageDraw.Draw(im)
    cy, cx = r['c']; L = r['maxr']*1.6
    for a in r['spikes']:
        th = math.radians(a) - math.pi
        d.line([(cx, cy), (cx + L*math.cos(th), cy + L*math.sin(th))], fill=(90, 200, 255), width=4)
    rr = r['maxr']*1.15
    d.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], outline=(255, 210, 80), width=4)
    W0, H0 = im.size
    th_im = im.crop((max(0,cx-600), max(0,cy-320), min(W0,cx+600), min(H0,cy+320))).resize((TW, 250))
    sheet.paste(th_im, ((i % COLS)*TW, (i//COLS)*250)); i += 1
sheet.save(f"{S}/star_sheet.png")

b64 = base64.b64encode(open(f"{S}/star_sheet.png",'rb').read()).decode()
modal = max(set(folds), key=folds.count) if folds else 0
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{background:#07090f;color:#e8eefc;width:1960px;padding:30px 36px;text-align:center;font-family:-apple-system,'Segoe UI',sans-serif}}
 h1{{font-size:26px;font-weight:800;background:linear-gradient(90deg,#7dd3fc,#ffd166);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
 .sub{{color:#8fa3c8;font-size:13.5px;margin:6px 0 16px}}
 img{{width:1890px;border-radius:14px;border:1px solid #223055}}
 .foot{{margin-top:14px;font-size:13px;color:#9fb0d0;line-height:1.65;max-width:1720px;margin:14px auto 0}}
 .foot b{{color:#fff}}
</style></head><body>
 <h1>Trial Feed 2 — the Dark Star, folded into the Rime Sphere</h1>
 <div class="sub">gold ring = the object's reach · blue rays = the measured spikes · full-circle angular fold, prism receipt per frame</div>
 <img src="data:image/png;base64,{b64}">
 <div class="foot"><b>Measured modal fold-symmetry: {modal}</b> across {len(ok)} star-bearing frames (harmonic spectrum of the
 full angular profile). Honest notes: the app screenshot was excluded; several frames are the same paused moment (near-duplicate
 receipts agree, as they must); and cross/star spikes around compact sources are ALSO the known signature of sensor/aperture
 diffraction — the geometry is measured, the identity is not claimed.</div>
</body></html>"""
open(f"{S}/star.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/star.html", f"{S}/star.png","1960", str(150+rows*250+120)],
                   cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
