#!/usr/bin/env python3
"""
rime_rgb_predict.py — TRIAL 3, the channel-blind cross-check. White removed;
then the ENTIRE measurement (dark-star track + forward/backward prediction)
is run THREE separate times — once per color channel, each its own moving
flashlight: 1 red pass, 1 green pass, 1 blue pass. Real motion must return
IDENTICAL tracks in all three; artifacts are allowed to disagree. Where the
channels agree the composite renders neutral; disagreement shows as fringes.
"""
import numpy as np, json, math, subprocess, base64
from PIL import Image, ImageDraw

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
UP = "/root/.claude/uploads/9ebd6119-d7ee-5c30-a062-d04210f7bc39"
FILES = ["db538e8e-1000157399.jpg","221217c5-1000157403.jpg","5cbcc489-1000157407.jpg",
         "d313495a-1000157411.jpg","7c402ae6-1000157413.jpg","d8dcc4a2-1000157419.jpg",
         "5b606c67-1000157423.jpg","405a3290-1000157427.jpg","262fd48d-1000157431.jpg",
         "3784c5c9-1000157435.jpg","e3628016-1000157439.jpg","a272a61c-1000157441.jpg",
         "126d215d-1000157445.jpg","a381c4d0-1000157451.jpg","f7c646c5-1000157455.jpg",
         "6fb45441-1000157457.jpg"]                       # capture order (the ID clock)

def find_star(g):
    H, W = g.shape
    win = g[int(.13*H):int(.80*H), int(.22*W):int(.78*W)]
    oy, ox = int(.13*H), int(.22*W)
    bg = np.median(win); m = win < bg - 0.18
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
        if len(pix)/(h*w) > 0.55: continue
        if pix[:,0].min() == 0 or pix[:,1].min() == 0: continue
        out.append((pix, len(pix)/(h*w)))
    if not out: return None
    pix, _ = min(out, key=lambda t: t[1])
    return (pix[:,0].mean()+oy)*2, (pix[:,1].mean()+ox)*2

# load RGB, dedup to distinct moments
imgs = []
base = None
for fn in FILES:
    im = Image.open(f"{UP}/{fn}").convert('RGB')
    if base is None: base = im.size
    if im.size != base: im = im.resize(base)
    imgs.append(np.asarray(im, dtype=np.float32)/255.0)
A = np.stack(imgs)
keep = [0]
for t in range(1, len(A)):
    if np.abs(A[t] - A[keep[-1]]).mean() > 0.004: keep.append(t)
D = A[keep]; names = [FILES[k][:8] for k in keep]
print(f"{len(FILES)} frames -> {len(D)} distinct moments")

# the three flashlight passes, fully independent
CH = {'R': 0, 'G': 1, 'B': 2}
tracks = {c: [] for c in CH}
for c, ci in CH.items():
    for t in range(len(D)):
        tracks[c].append(find_star(D[t][::2, ::2, ci]))
    found = [p for p in tracks[c] if p]
    print(f"{c} flashlight: star found in {len(found)}/{len(D)} moments")

def pred(seq):
    ep, ev = [], []
    for k in range(2, len(seq)):
        if not (seq[k-2] and seq[k-1] and seq[k]): continue
        (y0,x0),(y1,x1),(y2,x2) = seq[k-2], seq[k-1], seq[k]
        ep.append(math.hypot(y2-y1, x2-x1))
        ev.append(math.hypot(y2-(2*y1-y0), x2-(2*x1-x0)))
    return (float(np.mean(ep)), float(np.mean(ev))) if ep else (None, None)

report = {}
for c in CH:
    fp, fv = pred(tracks[c]); bp, bv = pred(tracks[c][::-1])
    report[c] = dict(fwd=(fp, fv), bwd=(bp, bv))
    print(f"{c}: fwd persist {fp:.1f}px vel {fv:.1f}px | bwd persist {bp:.1f}px vel {bv:.1f}px")

# cross-channel agreement per moment
spreads = []
for t in range(len(D)):
    ps = [tracks[c][t] for c in CH if tracks[c][t]]
    if len(ps) == 3:
        sp = max(math.hypot(ps[i][0]-ps[j][0], ps[i][1]-ps[j][1])
                 for i in range(3) for j in range(i+1, 3))
        spreads.append(sp)
agree = float(np.max(spreads)) if spreads else None
print(f"cross-channel agreement: max spread {agree:.2f}px over {len(spreads)} moments "
      f"(mean {np.mean(spreads):.2f}px)")
# geometry: heading per step from the channel-mean track
mean_track = []
for t in range(len(D)):
    ps = [tracks[c][t] for c in CH if tracks[c][t]]
    if len(ps) == 3: mean_track.append((t, np.mean([p[0] for p in ps]), np.mean([p[1] for p in ps])))
headings = []
for k in range(1, len(mean_track)):
    _, y0, x0 = mean_track[k-1]; _, y1, x1 = mean_track[k]
    d = math.hypot(y1-y0, x1-x0)
    if d > 6: headings.append(math.degrees(math.atan2(-(y1-y0), x1-x0)))
print("step headings (deg):", [round(h,1) for h in headings])
json.dump(dict(moments=names, tracks={c: tracks[c] for c in CH}, report=report,
    max_spread=agree, mean_spread=float(np.mean(spreads)) if spreads else None,
    headings=headings), open(f"{S}/rime_rgb_predict.json","w"), indent=1)

# ---- composite: each channel's dark residue in its own color; agreement = neutral ----
g_ref = D[len(D)//2]
comp = np.zeros_like(g_ref)
for c, ci in CH.items():
    ch = g_ref[..., ci]
    bg = np.median(ch)
    dark = np.clip(bg - ch, 0, 1); dark[dark < 0.06] = 0
    comp[..., ci] = dark*3.0
img = Image.fromarray((np.clip(comp, 0, 1)*255).astype(np.uint8))
d = ImageDraw.Draw(img)
COLS = {'R': (255, 95, 122), 'G': (74, 222, 128), 'B': (90, 160, 255)}
for c in CH:
    pts = [(p[1], p[0]) for p in tracks[c] if p]
    for j in range(len(pts)-1): d.line([pts[j], pts[j+1]], fill=COLS[c], width=3)
    for (x, y) in pts: d.ellipse([x-8, y-8, x+8, y+8], outline=COLS[c], width=3)
img.save(f"{S}/rgb_predict.png")
b64 = base64.b64encode(open(f"{S}/rgb_predict.png",'rb').read()).decode()
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{background:#04060c;color:#e8eefc;width:1960px;padding:30px 36px;text-align:center;font-family:-apple-system,'Segoe UI',sans-serif}}
 h1{{font-size:26px;font-weight:800;background:linear-gradient(90deg,#ff5f7a,#4ade80,#5aa0ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
 .sub{{color:#8fa3c8;font-size:13.5px;margin:6px 0 14px}}
 img{{width:1880px;border-radius:14px;border:1px solid #223055}}
 .rc{{margin-top:12px;font-family:ui-monospace,monospace;font-size:14px;color:#a9b8d8;line-height:1.9}}
 .rc b{{color:#4ade80}}
</style></head><body>
 <h1>Trial 3 — One Flashlight Per Channel, Predictions Cross-Checked</h1>
 <div class="sub">white removed · R, G, B measured independently · where all three agree the residue renders neutral; fringes = disagreement · three tracks drawn in their own colors</div>
 <img src="data:image/png;base64,{b64}">
 <div class="rc">cross-channel max spread: <b>{agree:.2f}px</b> · the three flashlights walked the same line or they didn't — see fringes<br>
 headings per step: {[round(h,1) for h in headings]}</div>
</body></html>"""
open(f"{S}/rgb_trial.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/rgb_trial.html", f"{S}/rgb_trial.png","1960","1230"],
                   cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
