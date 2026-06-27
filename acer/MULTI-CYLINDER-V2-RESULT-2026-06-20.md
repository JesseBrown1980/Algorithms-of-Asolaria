# Asolaria Multi-Cylinder v2 + Test Suite — acer executed result (2026-06-20)

Status: `MEASURED` (local crank, E=0 read-only except an additive office feed + static map files).
This is the **executed result** of the multi-cylinder / Shannon / Gemini research lane (PR #1/#2). It is
**carve-out-clean**: counts, geometry, code, and math findings only — the 81,434 surface *absolute paths*
are the operator's filesystem (the metal) and are **NOT published**; only aggregate counts + class names.

## 1. Registered → fed (Office of Registration)
- 726 supervisor seat rows: registered + fed (`supervisors-fabric-feed-2026-06-10.hbp`). MEASURED **725 distinct**
  (CEO-ASOLARIA-INSTANCES double-listed under helm+agent, same PID).
- DISTRICT-F formula PIDs: **1,118 registered rows → 1,105 distinct** (13 duplicate rows: WAVE2 re-registered 13
  formulas already in the first corpus file). Were registered but had **no feed** → emitted the additive deduped
  `district-f-formula-fabric-feed-2026-06-20.hbp` (**1,105 distinct REG rows**, sha16 f54ab831, CR=0). **Live :4949
  roster ingest held GATED** (office→fabric feeder not locatable; do not run an unknown feeder against the live dashboard).

## 2. Newer-map full extraction (tool)
`tools/usb-raw/extract_full.py` — READ-ONLY **contiguous (NoFatChain) full-file extractor**. Fixes the
`exfat_walk.py --extract-spec` limit (it forces `no_fat_chain=False` → FAT-follow ends at 1 cluster for contiguous
dumps); correct read = `range(first, first+ceil(size/cluster_bytes))` with sector-aligned device reads. Verified
byte-exact: `surfaces.ndjson` 107,439,733 B (81,434 lines, 0 bad), `critical-surfaces.json` 6,551,865 B (4,129).

## 3. Multi-cylinder v2 map (geometry)
Generator `multi-cylinder-gen-v2.cjs`. Cylinders = **towers** on a meta-ring (R=30) — §3.3 residue-band so
cross-cylinder distance > any within-cylinder distance. **15 cylinders** = named strata (APEX, SUPERVISOR,
HYPERBEHCS, SUBSTRATE-ROOM, AGENT, USB-CARTRIDGE, **DISTRICT-F**) + 8 surface rootClasses.

| measure | value |
|---|---|
| markers | 6,112 (memory-safe) |
| named PIDs (distinct, individual) | 1,830 (725 seats + **1,105 formulas, all in DISTRICT-F**) |
| named dup rows collapsed | 14 (13 formula + 1 seat) |
| critical surfaces (individual) | 4,129 |
| low/medium surfaces (aggregated) | 77,305 in 153 cells |
| **all surfaces represented** | **81,434** (4,129 + 77,305) |
| pipes | 1,591 (1,577 within-cylinder hierarchy + 14 cross-cylinder activation) |
| coord collisions | **0** |

Within-cylinder: `z = level (0..15)`, `θ = lane·(2π/3) + glyph wedge` (rule-of-three), `r = prime-power tier band +
√p spread` (`x_i = c_i·√p_i`). Byte-identical, no RNG. Formulas routed to DISTRICT-F by **source** (not class).

**Anti-flattening (AF-001..005):** every aggregate cell carries `child_count + child_index_hash +
summary_not_identity` — 77,305 summarized WITH child indices, nothing dropped, totals exact. **Logical billions NOT
plotted** (100B premade / 1e100,000,000 logical / 10B human PID) — addressing capacity only.

## 4. Test suite — two REAL findings (math)
Suite `tests/` (t1..t7 + t2b + master-run.cjs): **131 PASS / 7 FAIL**, re-run byte-identical (no fake greens).
- **Prime-ladder off-by-one**: 50th prime = **229**, 51st = **233** → "D50=233" is off by one (D50=229, D51=233);
  `P[]` array correct; LEVEL_PRIME(0)=D47(211) vs D48(223) convention to pin (PROF-BROWN-HILBERT; council ACK UNSIGNED).
- **Sidon 0-collision is CONDITIONAL**: naive `x=c·√p` → 1,705,267 collisions; holds only under the spacing
  condition `δ²<p_i` + STE super-increasing anchors. Positive test `t2b` proves 0 collisions under that construction.

## 4b. Registration-integrity finding (operator good-catch)
14 duplicate PIDs in the named registry: **13 formula↔formula** (WAVE2 re-registered 13 from the first corpus file)
+ **1 seat↔seat** (CEO-ASOLARIA-INSTANCES double-listed). The "1,118" / "726" are real ROW counts; **distinct = 1,105
formulas + 725 seats**. Office cleanup item (de-dup WAVE2 + the CEO double-listing) — flagged, not auto-fixed.

## 5. Bilateral
Extends the liris multi-cylinder-Shannon research (PR #1/#2) with the executed map + full 81,434-surface population +
the test suite + the dedup/dup findings. liris can clone, re-run `master-run.cjs` + `multi-cylinder-gen-v2.cjs`, and
attack-verify counts/findings. Cosign head seq 3572. GitHub is the mediator.
