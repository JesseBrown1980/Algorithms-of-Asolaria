#!/usr/bin/env python3
"""
rime_darkstatic.py — remove ALL white and ALL movement. What remains is the
TIMELESS DARK: the skeleton every moment shares (elementwise minimum of the
dark residue across all distinct moments). The mover is then each moment's
difference from the skeleton. Red pass and blue pass run SEPARATELY (agreement
checked), the moving areas are tracked, and the rime explanation is MEASURED
in real bytes: skeleton paid once (the free center), movers paid per frame
(the separations) — Law 0/3 tested on real video with zlib as the accountant.
"""
import numpy as np, json, math, zlib, subprocess, base64
from PIL import Image, ImageDraw

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
UP = "/root/.claude/uploads/9ebd6119-d7ee-5c30-a062-d04210f7bc39"
FILES = ["dce7436d-1000157457.jpg","a6afc323-1000157459.jpg","7e56c453-1000157461.jpg",
         "0f20abcd-1000157463.jpg","bde2a191-1000157465.jpg","d2de0a6f-1000157467.jpg",
         "c59eeaf4-1000157473.jpg","09512ae3-1000157474.jpg","7fe74aa5-1000157475.jpg",
         "bd18db16-1000157479.jpg","ecf640f4-1000157488.jpg","47145577-1000157501.jpg",
         "a2c6c3ea-1000157502.jpg","cb2c4720-1000157503.jpg","5c80d84d-1000157504.jpg",
         "9888f968-1000157505.jpg"]                     # capture-order (the ID clock)

imgs = []; base = None
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

H, W = D.shape[1], D.shape[2]
vy, vx = slice(int(.13*H), int(.80*H)), slice(int(.22*W), int(.78*W))

out = {}
for cname, ci in (('RED', 0), ('BLUE', 2)):
    darks = []
    for t in range(len(D)):
        ch = D[t][vy, vx, ci]
        bg = np.median(ch)
        dk = np.clip(bg - ch, 0, 1); dk[dk < 0.06] = 0   # white removed
        darks.append(dk)
    darks = np.stack(darks)
    skeleton = darks.min(axis=0)                          # movement removed: the timeless dark
    movers = darks - skeleton                             # each moment's separation
    sk_mass = float(skeleton.sum())
    mv_mass = float(movers.sum(axis=(1,2)).mean())
    # the accountant: pay skeleton once + residuals, vs pay every frame whole
    q = lambda a: (np.clip(a, 0, 1)*255).astype(np.uint8).tobytes()
    naive = sum(len(zlib.compress(q(darks[t]), 6)) for t in range(len(darks)))
    center = len(zlib.compress(q(skeleton), 6)) + sum(len(zlib.compress(q(movers[t]), 6)) for t in range(len(darks)))
    # track the moving areas (mover centroid per moment)
    track = []
    for t in range(len(darks)):
        m = movers[t]
        if m.sum() < 50: track.append(None); continue
        ys, xs = np.nonzero(m > 0.10)
        if len(ys) < 40: track.append(None); continue
        w_ = m[ys, xs]
        track.append((float((ys*w_).sum()/w_.sum()), float((xs*w_).sum()/w_.sum())))
    out[cname] = dict(skeleton_mass=sk_mass, mover_mass=mv_mass,
        naive_bytes=naive, center_bytes=center, amortization=naive/center,
        skeleton=skeleton, movers=movers, track=track)
    print(f"{cname}: skeleton {sk_mass:,.0f} mass (shared, paid once)  mover {mv_mass:,.0f}/moment")
    print(f"{cname}: naive pay-per-frame {naive:,} B  vs  center+separations {center:,} B  "
          f"-> amortization x{naive/center:.3f}")

# channel agreement on the mover track
spread = []
for t in range(len(D)):
    r, b = out['RED']['track'][t], out['BLUE']['track'][t]
    if r and b: spread.append(math.hypot(r[0]-b[0], r[1]-b[1]))
print(f"RED vs BLUE mover-track agreement: mean {np.mean(spread):.2f}px max {np.max(spread):.2f}px "
      f"over {len(spread)} moments")
json.dump(dict(moments=names,
    red=dict(am=out['RED']['amortization'], track=out['RED']['track']),
    blue=dict(am=out['BLUE']['amortization'], track=out['BLUE']['track']),
    agree_mean=float(np.mean(spread)), agree_max=float(np.max(spread))),
    open(f"{S}/rime_darkstatic.json","w"), indent=1)

# ---- render: the timeless skeleton + the mover trail ----
sk = out['BLUE']['skeleton']
comp = np.zeros((*sk.shape, 3))
comp[..., 2] = np.clip(sk*4.0, 0, 1)*0.85                 # skeleton in deep blue
comp[..., 1] = np.clip(sk*4.0, 0, 1)*0.35
trail = np.zeros_like(sk)
for t in range(len(out['RED']['movers'])):
    trail = np.maximum(trail, out['RED']['movers'][t])
comp[..., 0] = np.clip(trail*4.0, 0, 1)                    # everything that EVER moved, in red
img = Image.fromarray((np.clip(comp, 0, 1)*255).astype(np.uint8)).resize((sk.shape[1]*2, sk.shape[0]*2))
d = ImageDraw.Draw(img)
pts = [( (p[1])*2, (p[0])*2 ) for p in out['BLUE']['track'] if p]
for j in range(len(pts)-1): d.line([pts[j], pts[j+1]], fill=(255, 255, 255), width=3)
for (x, y) in pts: d.ellipse([x-7, y-7, x+7, y+7], outline=(255, 209, 102), width=3)
img.save(f"{S}/darkstatic.png")
b64 = base64.b64encode(open(f"{S}/darkstatic.png",'rb').read()).decode()
am_r, am_b = out['RED']['amortization'], out['BLUE']['amortization']
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{background:#04060c;color:#e8eefc;width:1960px;padding:30px 36px;text-align:center;font-family:-apple-system,'Segoe UI',sans-serif}}
 h1{{font-size:26px;font-weight:800;background:linear-gradient(90deg,#5aa0ff,#ff5f7a);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
 .sub{{color:#8fa3c8;font-size:13.5px;margin:6px 0 14px}}
 img{{width:1860px;border-radius:14px;border:1px solid #223055}}
 .rc{{margin-top:12px;font-family:ui-monospace,monospace;font-size:14px;color:#a9b8d8;line-height:1.9}}
 .rc b{{color:#4ade80}}
</style></head><body>
 <h1>White Removed · Movement Removed — the Timeless Dark, and the Trail</h1>
 <div class="sub">blue = the skeleton (dark in EVERY moment: redactions, horizon, contrail, the wisp's core) ·
   red = every place that ever moved (the star's whole trail at once) · gold rings = the mover's tracked stations</div>
 <img src="data:image/png;base64,{b64}">
 <div class="rc">the accountant's verdict (Law 0/3 on real video): pay-per-frame vs center+separations —
 RED x{am_r:.3f} · BLUE x{am_b:.3f} amortization<br>
 RED and BLUE mover tracks agree to mean {np.mean(spread):.2f}px (max {np.max(spread):.2f}px) — the mover is real in both lights</div>
</body></html>"""
open(f"{S}/darkstatic.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/darkstatic.html", f"{S}/darkstatic_shot.png","1960","1120"],
                   cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
