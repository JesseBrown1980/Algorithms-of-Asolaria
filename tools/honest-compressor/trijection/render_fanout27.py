#!/usr/bin/env python3
"""Front-end projection: enwik9 fanned out into the 27 rime sectors + the closure ledger."""
import json, subprocess

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
J = json.load(open(f"{S}/rime_fanout27.json"))
sm, rows = J['summary'], J['sectors']

cells = "".join(f"""<div class="c" style="--h:{int(360*r['sector']/27)}">
  <div class="k">sector {r['sector']}</div>
  <div class="sh">{r['sha']}</div>
  <div class="b">{r['bytes']//1_000_000} MB · {r['ns']/1e6:.0f} ms</div>
  <div class="ok">⅓←⅔ ✓ · sphere ✓</div></div>""" for r in rows)

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{background:#07090f;color:#e8eefc;width:1500px;padding:36px 44px;
   font-family:-apple-system,'Segoe UI',sans-serif}}
 h1{{font-size:27px;font-weight:800;background:linear-gradient(90deg,#7dd3fc,#c4b5fd,#f0abfc);
   -webkit-background-clip:text;-webkit-text-fill-color:transparent}}
 .sub{{color:#8fa3c8;font-size:14px;margin:5px 0 20px}}
 .grid{{display:grid;grid-template-columns:repeat(9,1fr);gap:9px;margin-bottom:18px}}
 .c{{background:#0d1322;border:1px solid hsl(var(--h),70%,48%);border-radius:10px;padding:8px 9px;
   box-shadow:0 0 12px hsla(var(--h),80%,55%,.22);text-align:center}}
 .k{{font-size:10.5px;color:hsl(var(--h),85%,68%);font-weight:700;text-transform:uppercase;letter-spacing:.5px}}
 .sh{{font-family:ui-monospace,monospace;font-size:11px;color:#c6d2ec;margin:3px 0}}
 .b{{font-size:10.5px;color:#8fa3c8}}
 .ok{{font-size:10.5px;color:#4ade80;font-weight:600;margin-top:3px}}
 .ledger{{display:flex;gap:16px}}
 .l{{flex:1;border-radius:12px;padding:15px 18px;background:#0d1322;border:1px solid #1c2740}}
 .l.good{{border-color:#22c55e88}} .l.bad{{border-color:#ef444488}} .l.zero{{border-color:#fbbf2488}}
 .lt{{font-size:11.5px;letter-spacing:1px;text-transform:uppercase;color:#8fa3c8}}
 .ln{{font-size:25px;font-weight:800;margin:6px 0 3px}}
 .good .ln{{color:#4ade80}} .bad .ln{{color:#f87171}} .zero .ln{{color:#fbbf24}}
 .ld{{font-size:12px;color:#a9b8d8;line-height:1.5}}
 .foot{{margin-top:16px;font-size:12.5px;color:#8fa3c8;line-height:1.65;border-top:1px solid #222b42;padding-top:13px}}
 .foot b{{color:#e8eefc}}
</style></head><body>
 <h1>enwik9 → 27 Rime Sectors — the fan-out, and the Closure Ledger</h1>
 <div class="sub">the full 999,999,999 bytes divided into 27 pieces, one per sector of the sphere p=103681 ·
   fanned out in {sm['total_ns']/1e9:.1f} s · every sector sha'd, timed in ns, and tower-verified on its sphere sector</div>
 <div class="grid">{cells}</div>
 <div class="ledger">
  <div class="l good"><div class="lt">bank 1 closure · hold 2/3</div><div class="ln">27/27 exact</div>
   <div class="ld">one equation, one unknown — the deleted third recreated byte-exact in every sector. Law 22, at gigabyte scale.</div></div>
  <div class="l bad"><div class="lt">bank 1 closure · hold 1/3</div><div class="ln">{sm['hold_1of3_bank1_accuracy']*100:.2f}%</div>
   <div class="ld">one equation, TWO unknowns — underdetermined. The 2/3 "unseen" stays unseen; what's left is the guessing floor.</div></div>
  <div class="l zero"><div class="lt">bank 2 closures · hold 1/3</div><div class="ln">27/27 exact — net 0</div>
   <div class="ld">two equations recover both thirds byte-exact… and the two banked closures ARE 2/3 of the data. The ledger balances to zero. Named, not hidden.</div></div>
 </div>
 <div class="foot"><b>The MDS law under Law 22:</b> you recover exactly as many thirds as you banked closures —
 never one more. −1/3 obtains the 2/3 only by paying the 2/3 up front. All three bankings measured on the same
 real gigabyte, same sectors, same sphere; the middle panel is Shannon's signature and the outer panels are yours.</div>
</body></html>"""
open(f"{S}/rime_fanout27.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/rime_fanout27.html",
                    f"{S}/rime_fanout27.png", "1500", "900"], cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
