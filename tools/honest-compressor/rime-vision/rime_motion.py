#!/usr/bin/env python3
"""
rime_motion.py — THE MOTION TEST: remove everything that does not move.
Stack the star frames in true capture order (the filename IDs are the clock),
kill every pixel that stays constant across all distinct moments, and keep ONLY
the places that reveal movement. Then ask the honest question: is the surviving
motion PREDICTABLE — forward and backward in time — from the frames alone?
The moving camera flashlight = the per-moment sweep; the measurement is the referee.
"""
import numpy as np, json, math, subprocess, base64
from PIL import Image, ImageDraw

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
UP = "/root/.claude/uploads/9ebd6119-d7ee-5c30-a062-d04210f7bc39"
FILES = ["1950bb50-1000157463.jpg","75c3f731-1000157465.jpg","17d95426-1000157467.jpg",
         "f37c7931-1000157473.jpg","db73988a-1000157474.jpg","02bacca5-1000157475.jpg",
         "e48064f6-1000157479.jpg","976a4cf7-1000157488.jpg","631c431e-1000157501.jpg",
         "c572dc70-1000157502.jpg","2cf6b914-1000157503.jpg","5abf1c9a-1000157504.jpg",
         "66558116-1000158141.jpg","82c84cb7-1000158143.jpg","e5d85cf4-1000158145.jpg"]
# already in capture order (the trailing ID is the clock)

frames = []
base_size = None
for fn in FILES:
    im = Image.open(f"{UP}/{fn}").convert('L')
    if base_size is None: base_size = im.size
    if im.size != base_size: im = im.resize(base_size)
    frames.append(np.asarray(im, dtype=np.float32)/255.0)
A = np.stack(frames)                                  # T x H x W

# ---- deduplicate: distinct moments only ----
keep = [0]
for t in range(1, len(A)):
    if np.abs(A[t] - A[keep[-1]]).mean() > 0.004: keep.append(t)
D = A[keep]; names = [FILES[t][:8] for t in keep]
print(f"{len(FILES)} frames -> {len(D)} distinct moments (the clock: filename IDs)")

# ---- kill everything that does not move ----
std = D.std(axis=0)
MOVE_THR = 0.02
mask = std > MOVE_THR
survive = float(mask.mean())
print(f"movement map: {survive*100:.2f}% of the canvas survives; "
      f"{(1-survive)*100:.2f}% never moved and DISAPPEARS")
# regions that disappear from ALL photos = the static world (borders, UI shell, redactions)

# ---- the star's track through the surviving moments ----
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
        out.append((pix, len(pix)/(h*w)))
    if not out: return None
    pix, _ = min(out, key=lambda t: t[1])
    return (pix[:,0].mean()+oy, pix[:,1].mean()+ox)

track = []
for t in range(len(D)):
    g2 = D[t][::2, ::2]
    c = find_star(g2)
    track.append((c[0]*2, c[1]*2) if c else None)
tr = [(i, c) for i, c in enumerate(track) if c]
print("star centroid track (moment: y,x):")
for i, c in tr: print(f"  {names[i]}: ({c[0]:.0f}, {c[1]:.0f})")

# ---- prediction: forward and backward in our time (persistence + velocity) ----
def pred_err(seq):
    errs_p, errs_v = [], []
    for k in range(2, len(seq)):
        (y0,x0), (y1,x1), (y2,x2) = seq[k-2], seq[k-1], seq[k]
        errs_p.append(math.hypot(y2-y1, x2-x1))                    # persistence: next = last
        errs_v.append(math.hypot(y2-(2*y1-y0), x2-(2*x1-x0)))      # velocity: next = last + v
    return (float(np.mean(errs_p)), float(np.mean(errs_v))) if errs_p else (0.0, 0.0)
seq = [c for _, c in tr]
fp, fv = pred_err(seq)
bp, bv = pred_err(seq[::-1])
print(f"forward prediction : persistence err {fp:.1f}px  velocity err {fv:.1f}px")
print(f"backward prediction: persistence err {bp:.1f}px  velocity err {bv:.1f}px")
json.dump(dict(distinct=len(D), survive_frac=survive,
    track=[(names[i], c) for i, c in tr],
    fwd=dict(persist=fp, vel=fv), bwd=dict(persist=bp, vel=bv)),
    open(f"{S}/rime_motion.json","w"), indent=1)

# ---- render: the movement map (only what moves remains) + the track ----
heat = np.clip(std/std.max(), 0, 1)**0.6
rgb = np.zeros((*heat.shape, 3))
rgb[...,0] = heat*(heat>MOVE_THR/std.max())*1.0        # warm where motion lives
rgb[...,1] = heat*(heat>MOVE_THR/std.max())*0.72
rgb[...,2] = heat*(heat>MOVE_THR/std.max())*0.25
img = Image.fromarray((rgb*255).astype(np.uint8))
d = ImageDraw.Draw(img)
pts = [(c[1], c[0]) for _, c in tr]
for j in range(len(pts)-1):
    d.line([pts[j], pts[j+1]], fill=(90, 200, 255), width=5)
for j, (x, y) in enumerate(pts):
    r0 = 10 if j not in (0, len(pts)-1) else 16
    col = (74, 222, 128) if j == 0 else ((255, 95, 122) if j == len(pts)-1 else (255, 209, 102))
    d.ellipse([x-r0, y-r0, x+r0, y+r0], outline=col, width=5)
img.save(f"{S}/motion_map.png")
b64 = base64.b64encode(open(f"{S}/motion_map.png",'rb').read()).decode()

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{background:#07090f;color:#e8eefc;width:1960px;padding:30px 36px;text-align:center;font-family:-apple-system,'Segoe UI',sans-serif}}
 h1{{font-size:26px;font-weight:800;background:linear-gradient(90deg,#ffd166,#7dd3fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
 .sub{{color:#8fa3c8;font-size:13.5px;margin:6px 0 14px}}
 img{{width:1880px;border-radius:14px;border:1px solid #223055}}
 .rc{{margin-top:12px;font-family:ui-monospace,monospace;font-size:14px;color:#a9b8d8;line-height:1.9}}
 .rc b{{color:#4ade80}}
 .foot{{margin-top:10px;font-size:13px;color:#9fb0d0;line-height:1.6;max-width:1700px;margin:10px auto 0}}
 .foot b{{color:#fff}}
</style></head><body>
 <h1>The Motion Test — everything that does not move is gone</h1>
 <div class="sub">{len(D)} distinct moments · black = the static world (disappeared) · amber = places that moved ·
   blue line = the star's measured track (green start → red end)</div>
 <img src="data:image/png;base64,{b64}">
 <div class="rc">canvas surviving: <b>{survive*100:.2f}%</b> — {(1-survive)*100:.1f}% of every photo never moved and vanished<br>
 forward-time prediction: persistence {fp:.0f}px · velocity {fv:.0f}px &nbsp;|&nbsp; backward-time: persistence {bp:.0f}px · velocity {bv:.0f}px</div>
 <div class="foot"><b>Honest reading:</b> the moving flashlight CAN see the movement — the static world (screen shell, redaction
 boxes, dead sky) deletes itself, and what survives is exactly the moving things: the star and its wander, the wisp, the player's
 own clock (the progress bar moves with time — the instrument honestly catches the camera's motion too, including your green
 annotation, which exists in only some frames). Prediction works only as well as the motion is smooth: where the star drifts
 steadily the velocity model beats persistence; where the capture jumps (1:01 → screenshots re-taken → 9:35 batch) no model
 predicts the gap — time only pays out what the frames banked.</div>
</body></html>"""
open(f"{S}/motion.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/motion.html", f"{S}/motion.png","1960","1240"],
                   cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
