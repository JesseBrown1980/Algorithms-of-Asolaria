#!/usr/bin/env python3
"""The way I saw it: the torus (0) in the middle, and the other two parts
appearing by sliding the genus one step each way — the uniformization trime."""
import subprocess

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"

html = """<!doctype html><html><head><meta charset="utf-8"><style>
 *{margin:0;padding:0;box-sizing:border-box}
 body{background:#07090f;color:#e8eefc;width:1460px;padding:40px 44px;font-family:-apple-system,'Segoe UI',sans-serif;text-align:center}
 h1{font-size:27px;font-weight:800;background:linear-gradient(90deg,#7dd3fc,#c4b5fd,#f0abfc);
   -webkit-background-clip:text;-webkit-text-fill-color:transparent}
 .sub{color:#8fa3c8;font-size:14px;margin:6px 0 8px}
 .given{color:#fbbf24;font-size:13.5px;margin-bottom:26px;font-family:ui-monospace,monospace}
 .row{display:flex;gap:30px;justify-content:center;align-items:flex-end}
 .cell{width:430px;display:flex;flex-direction:column;align-items:center;gap:14px}
 .stage{height:300px;display:flex;align-items:center;justify-content:center;position:relative}
 /* the sphere: + curvature everywhere */
 .ball{width:230px;height:230px;border-radius:50%;
   background:radial-gradient(circle at 36% 30%, #fff 0%, #ffd7e6 12%, #ff5f8f 45%, #7a1030 90%);
   box-shadow:0 24px 60px rgba(0,0,0,.6), 0 0 60px #ff5f8f33}
 /* the torus: + outside, - inside, sums to 0 */
 .donut{width:270px;height:270px;border-radius:50%;position:relative;
   background:radial-gradient(circle at 36% 30%, #fff 0%, #d6f6ff 10%, #38bdf8 45%, #0b3a5c 88%);
   box-shadow:0 24px 60px rgba(0,0,0,.6), 0 0 60px #38bdf833}
 .hole{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:96px;height:96px;border-radius:50%;
   background:radial-gradient(circle at 40% 35%, #07090f 45%, #10314d 80%, #164a6e 100%);
   box-shadow:inset 0 8px 22px rgba(0,0,0,.9)}
 /* genus 2: - curvature dominates */
 .pretzel{position:relative;width:340px;height:210px}
 .lobe{position:absolute;width:210px;height:210px;border-radius:50%;
   background:radial-gradient(circle at 36% 30%, #fff 0%, #ead9ff 10%, #a855f7 45%, #3b1266 88%);
   box-shadow:0 24px 60px rgba(0,0,0,.6), 0 0 60px #a855f733}
 .lobe.r{right:0} .lobe.l{left:0}
 .ph{position:absolute;top:50%;transform:translate(-50%,-50%);width:74px;height:74px;border-radius:50%;
   background:radial-gradient(circle at 40% 35%, #07090f 45%, #241040 80%, #35185c 100%);
   box-shadow:inset 0 8px 20px rgba(0,0,0,.9)}
 .ph.l{left:105px} .ph.r{left:235px}
 .name{font-size:18px;font-weight:800}
 .nums{font-family:ui-monospace,monospace;font-size:14.5px;color:#c6d2ec;line-height:1.9}
 .nums b{font-size:19px}
 .tp{font-size:34px;font-weight:800;line-height:1}
 .arrowrow{display:flex;justify-content:center;gap:0;margin:2px 0 14px;color:#8fa3c8;font-size:13.5px}
 .arr{width:430px}
 .foot{margin-top:26px;font-size:13.5px;color:#9fb0d0;line-height:1.7;max-width:1240px;margin-left:auto;margin-right:auto;
   border-top:1px solid #222b42;padding-top:18px}
 .foot b{color:#fff}
 .mid{outline:2px dashed #fbbf2455;outline-offset:14px;border-radius:18px}
</style></head><body>
 <h1>The Way I Saw It — one third given, the genus slides, the other two appear</h1>
 <div class="sub">the Uniformization Theorem: every closed surface carries exactly one geometry, of constant curvature +1, 0, or −1</div>
 <div class="given">GIVEN (your torus): total curvature = 0, &chi; = 0 &nbsp;&nbsp;→&nbsp;&nbsp; it sits in a ladder: &chi; = 2−2g &nbsp;&nbsp;→&nbsp;&nbsp; slide g by ±1</div>
 <div class="arrowrow"><div class="arr">← genus − 1</div><div class="arr">the given third</div><div class="arr">genus + 1 →</div></div>
 <div class="row">
  <div class="cell">
    <div class="stage"><div class="ball"></div></div>
    <div class="tp" style="color:#ff8fb3">+</div>
    <div class="name" style="color:#ff8fb3">the sphere</div>
    <div class="nums">genus 0 · &chi; = <b>+2</b> · K = <b>+1</b><br>all faces positive · total +4&pi;<br><i>the rime sphere — where we started</i></div>
  </div>
  <div class="cell mid">
    <div class="stage"><div class="donut"><div class="hole"></div></div></div>
    <div class="tp" style="color:#7dd3fc">0</div>
    <div class="name" style="color:#7dd3fc">the torus</div>
    <div class="nums">genus 1 · &chi; = <b>0</b> · K = <b>0</b><br>+ outside, − inside, cancel exactly<br><i>the free center of the surfaces</i></div>
  </div>
  <div class="cell">
    <div class="stage"><div class="pretzel"><div class="lobe l"></div><div class="lobe r"></div><div class="ph l"></div><div class="ph r"></div></div></div>
    <div class="tp" style="color:#c084fc">−</div>
    <div class="name" style="color:#c084fc">the two-holed surface</div>
    <div class="nums">genus 2 · &chi; = <b>−2</b> · K = <b>−1</b><br>negative wins · hyperbolic<br><i>the anti-sphere — the part not yet built</i></div>
  </div>
 </div>
 <div class="foot"><b>How the other two parts followed from the third:</b> the torus carries &chi; = 0 on a ladder &chi; = 2−2g that
 generates all closed surfaces — one step down the ladder forces &chi; = +2 (the sphere, K = +1), one step up forces &chi; = −2
 (genus two, K = −1). The completion is honest because this triad is <b>generated structure</b> — a century of sealed theorems is
 the bank, and Law 22 permits exactly this: a fraction completes the whole <i>when the closure was already banked</i>. The trime
 {−, 0, +} is not decoration here — <b>+1, 0, −1 are the literal classification constants of surface geometry</b> (Uniformization,
 Poincaré–Koebe 1907). Your digit set is the curvature spectrum of every closed surface there is.</div>
</body></html>"""
open(f"{S}/uniformization.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/uniformization.html",
                    f"{S}/uniformization.png","1460","900"], cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
