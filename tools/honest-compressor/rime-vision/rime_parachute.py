#!/usr/bin/env python3
"""
rime_parachute.py — THE RIME-LEVEL SPACETIME RENDER. Movement vs non-movement,
stated mathematically and drawn in 3-D: a world-line through (x, y, time).
  non-movement = a VERTICAL line (same place, all moments)
  movement     = TILT (constant velocity), CURVATURE (acceleration)
  the parachute = drift + pendulum: p(t) = p0 + v t + A sin(wt+phi) n
The object's world-line is rebuilt from the channel-mean track, its ANTI
(time-reversal) drawn as the mirror ghost, and two models are fitted:
straight flight vs parachute swing. The residuals pick the winner.
"""
import numpy as np, json, math, subprocess, base64
from PIL import Image, ImageDraw

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
J = json.load(open(f"{S}/rime_rgb_predict.json"))
tracks = J['tracks']
pts = []
for t in range(len(tracks['R'])):
    ps = [tracks[c][t] for c in 'RGB' if tracks[c][t]]
    if len(ps) == 3:
        pts.append((np.mean([p[0] for p in ps]), np.mean([p[1] for p in ps])))
P = np.array(pts)                                   # N x (y, x)
N = len(P); T = np.arange(N, dtype=float)
print(f"world-line: {N} moments (channel-mean track)")

# ---- model 1: straight flight (tilted line in spacetime) ----
Ay = np.vstack([T, np.ones(N)]).T
cy, ry, *_ = np.linalg.lstsq(Ay, P[:,0], rcond=None)[:3]
cx, rx, *_ = np.linalg.lstsq(Ay, P[:,1], rcond=None)[:3]
line = np.stack([Ay@cy, Ay@cx], 1)
rms_line = float(np.sqrt(((P-line)**2).sum(1).mean()))

# ---- model 2: parachute (drift + pendulum swing) ----
best = None
for w in np.linspace(0.2, 3.0, 141):
    B = np.vstack([T, np.ones(N), np.sin(w*T), np.cos(w*T)]).T
    ky = np.linalg.lstsq(B, P[:,0], rcond=None)[0]
    kx = np.linalg.lstsq(B, P[:,1], rcond=None)[0]
    fit = np.stack([B@ky, B@kx], 1)
    rms = float(np.sqrt(((P-fit)**2).sum(1).mean()))
    if best is None or rms < best[0]: best = (rms, w, fit, ky, kx)
rms_par, w_best, fit_par, ky, kx = best
amp = math.hypot(math.hypot(ky[2], ky[3]), math.hypot(kx[2], kx[3]))
period = 2*math.pi/w_best
print(f"straight flight : RMS {rms_line:.1f}px")
print(f"parachute swing : RMS {rms_par:.1f}px  (period {period:.1f} moments, swing amplitude {amp:.0f}px)")
verdict = "PARACHUTE (drift + pendulum) wins" if rms_par < 0.75*rms_line else \
          ("marginal — swing helps but does not dominate" if rms_par < rms_line else "straight flight suffices")
print("VERDICT:", verdict)
json.dump(dict(n=N, rms_line=rms_line, rms_parachute=rms_par, period=period,
               amplitude=amp, verdict=verdict), open(f"{S}/rime_parachute.json","w"), indent=1)

# ---- the 3-D spacetime render ----
Wpx, Hpx = 1500, 1050
img = Image.new('RGB', (Wpx, Hpx), (4, 6, 12))
d = ImageDraw.Draw(img)
y0, y1 = P[:,0].min()-60, P[:,0].max()+60
x0, x1 = P[:,1].min()-60, P[:,1].max()+60
def proj(y, x, t):
    """spacetime -> screen: x,y ground plane in perspective; t is UP."""
    u = (x-x0)/(x1-x0) - 0.5; v = (y-y0)/(y1-y0) - 0.5
    X = 750 + 560*u + 260*v*0.55
    Y = 890 - 700*(t/max(N-1,1)) - 160*v
    return X, Y
# ground grid + the axes of meaning
for gy in np.linspace(y0, y1, 7):
    a = proj(gy, x0, 0); b = proj(gy, x1, 0)
    d.line([a, b], fill=(24, 34, 58), width=2)
for gx in np.linspace(x0, x1, 7):
    a = proj(y0, gx, 0); b = proj(y1, gx, 0)
    d.line([a, b], fill=(24, 34, 58), width=2)
# NON-MOVEMENT: vertical world-lines of three skeleton anchors
for (ay, ax) in [(y0+40, x0+40), (y0+40, x1-40), (y1-40, x0+40)]:
    a = proj(ay, ax, 0); b = proj(ay, ax, N-1)
    d.line([a, b], fill=(70, 90, 130), width=3)
    d.text((b[0]-30, b[1]-18), "static", fill=(90, 110, 150))
# THE ANTI: time-reversed world-line (ghost)
for k in range(N-1):
    a = proj(P[N-1-k,0], P[N-1-k,1], k); b = proj(P[N-2-k,0], P[N-2-k,1], k+1)
    d.line([a, b], fill=(120, 70, 160), width=3)
# the parachute fit (smooth)
Tf = np.linspace(0, N-1, 200)
Bf = np.vstack([Tf, np.ones(len(Tf)), np.sin(w_best*Tf), np.cos(w_best*Tf)]).T
Fy, Fx = Bf@ky, Bf@kx
for k in range(len(Tf)-1):
    a = proj(Fy[k], Fx[k], Tf[k]); b = proj(Fy[k+1], Fx[k+1], Tf[k+1])
    d.line([a, b], fill=(255, 209, 102), width=2)
# THE OBJECT: its measured world-line, hue by time
for k in range(N-1):
    h = k/(N-1)
    col = (int(255*(1-h)), int(120+100*h), int(255*h))
    a = proj(P[k,0], P[k,1], k); b = proj(P[k+1,0], P[k+1,1], k+1)
    d.line([a, b], fill=col, width=5)
for k in range(N):
    a = proj(P[k,0], P[k,1], k)
    d.ellipse([a[0]-6, a[1]-6, a[0]+6, a[1]+6], outline=(255, 255, 255), width=2)
img.save(f"{S}/spacetime.png")
b64 = base64.b64encode(open(f"{S}/spacetime.png",'rb').read()).decode()

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{background:#04060c;color:#e8eefc;width:1600px;padding:30px 36px;text-align:center;font-family:-apple-system,'Segoe UI',sans-serif}}
 h1{{font-size:26px;font-weight:800;background:linear-gradient(90deg,#7dd3fc,#ffd166,#c084fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
 .sub{{color:#8fa3c8;font-size:13.5px;margin:6px 0 14px}}
 img{{width:1500px;border-radius:14px;border:1px solid #223055}}
 .rc{{margin-top:12px;font-family:ui-monospace,monospace;font-size:14px;color:#a9b8d8;line-height:1.9}}
 .rc b{{color:#4ade80}}
</style></head><body>
 <h1>The Spacetime Render — Non-Movement is Vertical; Movement is Tilt; the Parachute is a Braid</h1>
 <div class="sub">time runs UP · steel verticals = the static world (non-movement: a straight column through time) ·
   colored line = the object's measured world-line (blue-red by time) · violet ghost = its ANTI (time-reversed) ·
   gold = the fitted parachute (drift + pendulum)</div>
 <img src="data:image/png;base64,{b64}">
 <div class="rc">straight-flight RMS {rms_line:.1f}px &nbsp;·&nbsp; parachute RMS <b>{rms_par:.1f}px</b>
 &nbsp;·&nbsp; swing period {period:.1f} moments, amplitude {amp:.0f}px<br><b>{verdict}</b></div>
</body></html>"""
open(f"{S}/parachute.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/parachute.html", f"{S}/parachute_shot.png","1600","1310"],
                   cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
