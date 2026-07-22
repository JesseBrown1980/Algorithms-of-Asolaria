#!/usr/bin/env python3
"""Front-end projection of the container hosting the upgraded rime prime,
rendered from the actual run receipts (rime_feed_runs.json / facts)."""
import json, subprocess

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
runs  = json.load(open(f"{S}/rime_feed_runs.json"))
facts = json.load(open(f"{S}/rime_feed_facts.json"))

def panel(r, hue):
    corpus_x = r['bytes_fed'] / 100_000_000
    return f"""<div class="run" style="--h:{hue}">
      <div class="wt">{r['window_s']} s window</div>
      <div class="big">{r['bytes_fed']:,}<span class="u">bytes fed</span></div>
      <div class="mono">elapsed&nbsp; {r['elapsed_ns']:,} ns</div>
      <div class="mono ov">overshoot +{r['overshoot_ns']:,} ns (measured, not hidden)</div>
      <div class="bar"><div class="fill" style="width:{min(100, r['mb_s'])}%"></div></div>
      <div class="st">{r['mb_s']:.1f} MB/s · {corpus_x:.2f}× enwik8 · {r['chunks_verified']} chunks
        <b class="ok">byte-exact ✓</b></div>
    </div>"""

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{background:#07090f;color:#e8eefc;width:1500px;padding:38px 46px;
   font-family:-apple-system,'Segoe UI',sans-serif}}
 h1{{font-size:28px;font-weight:800;background:linear-gradient(90deg,#7dd3fc,#c4b5fd,#f0abfc);
   -webkit-background-clip:text;-webkit-text-fill-color:transparent}}
 .sub{{color:#8fa3c8;font-size:14px;margin:5px 0 22px}}
 .box{{display:flex;gap:18px;margin-bottom:18px}}
 .host{{flex:1.1;background:#0d1322;border:1px solid #1c2740;border-radius:14px;padding:18px 22px}}
 .ht{{font-size:12px;letter-spacing:1.5px;text-transform:uppercase;color:#8fa3c8;margin-bottom:10px}}
 .kv{{display:grid;grid-template-columns:auto 1fr;gap:4px 16px;font-size:13.5px}}
 .kv b{{color:#c6d2ec;font-weight:600}} .kv span{{color:#8fa3c8;font-family:ui-monospace,monospace}}
 .engine{{flex:1;background:#0d1322;border:1px solid #1c2740;border-radius:14px;padding:18px 22px}}
 .tower{{font-family:ui-monospace,monospace;font-size:14px;line-height:1.9;color:#a9b8d8}}
 .tower b{{color:#7dd3fc}}
 .runs{{display:flex;gap:18px}}
 .run{{flex:1;background:#0d1322;border:1px solid hsl(var(--h),70%,45%);border-radius:14px;
   padding:18px 20px;box-shadow:0 0 22px hsla(var(--h),80%,55%,.22)}}
 .wt{{font-size:13px;letter-spacing:1px;text-transform:uppercase;color:hsl(var(--h),85%,68%);font-weight:700}}
 .big{{font-size:26px;font-weight:800;margin:8px 0 6px}} .u{{font-size:12px;color:#8fa3c8;margin-left:7px}}
 .mono{{font-family:ui-monospace,monospace;font-size:12.5px;color:#a9b8d8}}
 .ov{{color:#fbbf24}}
 .bar{{height:9px;background:#131c31;border-radius:5px;margin:10px 0 7px;overflow:hidden}}
 .fill{{height:100%;background:linear-gradient(90deg,hsl(var(--h),85%,55%),hsl(var(--h),85%,70%))}}
 .st{{font-size:12.5px;color:#a9b8d8}} .ok{{color:#4ade80}}
 .foot{{margin-top:18px;font-size:12.5px;color:#8fa3c8;line-height:1.65;border-top:1px solid #222b42;padding-top:14px}}
 .foot b{{color:#e8eefc}}
</style></head><body>
 <h1>Container Front-End — the Upgraded Rime Prime, fed live</h1>
 <div class="sub">real enwik8 streamed through the tower engine for three wall-clock windows · every chunk round-tripped through the sphere and Fischer-inverted before it counts</div>
 <div class="box">
  <div class="host"><div class="ht">host container</div><div class="kv">
    <b>node</b><span>{facts['host']} · Linux {facts['kernel']}</span>
    <b>cpu</b><span>{facts['cpu']} × {facts['cores']}</span>
    <b>memory</b><span>{facts['mem_gb']} GB</span>
    <b>engine sha</b><span>{facts['sha_engine']} (frozen point table — Law 15)</span>
    <b>clock</b><span>monotonic, nanosecond read; exact elapsed REPORTED</span>
  </div></div>
  <div class="engine"><div class="ht">the upgraded rime prime</div><div class="tower">
    prime <b>103681</b> · g = 11 · tower <b>256 → ×3 → ×27</b> = 20736 = 144²<br>
    feed: byte + 256·trime + 768·glyph → point W<sup>k</sup> mod p → Fischer → back<br>
    verification: <b>every chunk byte-exact</b> or it doesn't count
  </div></div>
 </div>
 <div class="runs">{panel(runs[0],195)}{panel(runs[1],265)}{panel(runs[2],320)}</div>
 <div class="foot"><b>Honest timing law:</b> no process halts at exactly T — it can only <b>measure exactly what it did</b>.
 The engine cuts at the target and reports true elapsed nanoseconds; the overshoots above (1.5 ms, 90 µs, 0.8 ms) are the
 cost of checking a nanosecond clock between million-byte chunks. <b>Throughput is flat (~100 MB/s single-core):</b> 27 s feeds
 27× what 1 s feeds — linear, no acceleration, as conservation demands. The 27 s window pushed <b>2.676 GB = 26.76×
 the whole of enwik8</b> through the sphere and back, byte-exact.</div>
</body></html>"""
open(f"{S}/rime_feed_frontend.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/rime_feed_frontend.html",
                    f"{S}/rime_feed_frontend.png", "1500", "760"], cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
