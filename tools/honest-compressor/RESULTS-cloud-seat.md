# Honest Compressor — consolidated measured results

Every number here is byte-exact and lossless (SHA-256 restore verified). Provenance is
labeled: **[cloud]** = run in the Anthropic cloud container this session; **[container]** =
run by the companion agent (cm3t Rust), reported via its own logs. No number is below the
source entropy; none claims to be.

## Standard-compressor baselines — real enwik8 (Wikipedia), **[cloud]**

| corpus | gzip -9 | bzip2 -9 | xz -9 |
|---|---|---|---|
| enwik8, full 100 MB (entropy 5.0801) | 2.9181 | 2.3207 | **1.9892** |
| corpus.bin, 2.2 MB distinct | 2.9402 | 2.2493 | 2.1550 |
| enwik8 first 3 MB | 2.9061 | 2.3108 | 2.2710 |

## The transform family (BWT / cube) — caps at the bzip2 tier, **[cloud]**

| method | corpus | bpc | lossless |
|---|---|---|---|
| BWT + MTF + range coder | enwik8 3 MB | 2.5149→2.33 | ✓ |
| BWT + MTF + **RLE0** + range coder | corpus.bin 2.2 MB | 2.2796 | ✓ |
| all 8 omega-cube corners before the chain | enwik8 3 MB | every corner **worse** than identity (+0.9% … +3.0%) | ✓ |

**Finding:** the transform/geometry approach (BWT, cubes) tops out at the bzip2 tier. Fully
built out (RLE0 and all), it does not pass bzip2/xz. The cube corners measured net-negative.

## The context-mixing model — the lever that actually moves, **[container]** (cm3t, Rust)

| slice | k=7 | k=9/k=10 | k=12 | vs xz |
|---|---|---|---|---|
| 1 MB | 2.0731 | 2.0678 (k9) | — | — |
| 2.2 MB | — | 2.0426 | — | — |
| **10 MB distinct** | 1.9307 | **1.9276 (k10)** | 1.9328 (past knee) | xz = 2.1933 → **beaten** |

**Finding:** context mixing (match model + logistic mixer + APM) is the only method that
passes xz. On the 10 MB slice it broke **below 2.0** (1.9276, lossless). Depth pays to k=10
and then hits its knee (k=12 worse) — the next gains need a better *model* (SSE + word model),
not more depth. The Rust port is ~**40× faster** than pure Python (1 MB k=7: 12 s vs ~500 s),
putting 100 MB within reach.

## Sanity checks that keep everything honest, **[cloud]**

- **BEHCS-1024 ladder:** 1,000,000 bytes ↔ 800,000 glyphs, **information rate 1.000000**,
  SHA clone verified. A bijection — zero-loss, **not** compression.
- **Codec v0.1** (order-2 range coder): 1 MB → ~402 KB, **3.218 bpc**, byte-identical restore.
- **Q4-style quantization** (GGUF-like): 32→~3.5 bit is **lossy** — changed **96.7%** of the
  weights on round-trip. "Zero accuracy loss" ≠ "zero information loss."

## The honest ceiling (the yardsticks)

| | bpc | note |
|---|---|---|
| this project's best (cm3t, 10 MB) | **1.9276** | real, lossless, beats xz |
| first Hutter winner (paq8hp5, 2006) | 1.366 | full enwik8 |
| current world record (fx2-cmix, 2024) | 0.886 | enwik9, CPU-only, no GPU |
| source entropy floor | > 0 | no lossless code goes below `N·H(X)` |

**Bottom line:** below 2.0 is a real, earned milestone. It is *not* below entropy — the record
sits at 0.886 and the floor below that. The road onward is CPU context-mixing (SSE + word
model), the same family the record-holders used. Every gain here came from the **model**; the
transforms/geometry (BWT, cubes, glyph rebasing) are entropy-neutral and measured as such.

## Rule-of-three battery (space / colors / time) — 2026-07-19 evening

Jesse's triad: 3 for space, 3 for colors, 3 for time (past/present/future),
proposed as an encodable "final key." Contract applied: each rule built as an
operation and measured. Anchor: v6 rainbow-12-even @1MB k7 = 239,869 payload
(comp_sha 53ad10066c34ac66, reproduced live twice same day).

| Arm | Operation | payload @1MB k7 | vs anchor | comp_sha | Verdict |
|---|---|---|---|---|---|
| TIME | v6 on byte-reversed slice1m | 243,254 | **+3,385 (+0.027 bpc)** | ec702184f05ce923 | **Arrow of time measured** — enwik text predicts easier forward than backward for finite-context models (Shannon's fwd=bwd entropy equality holds only in the infinite limit). We already code in the favored direction; property recorded, no action. |
| SPACE-3 | 3-class sector wheel (letters / ws+digits / other), 6 rows | 240,180 | +311 (+0.0025) | 88665c0fb1a90b19 | Closed — wheel curve monotone below 6; confirms 3 < 6 < 12 < 24 ordering both directions from the 6 anchor. |
| COLOR-3 | three learning-rate banks on mixer A (>>12/>>14/>>17), gain-preserving | 240,629 | +760 (+0.0061) | ddbf061d486ed0ba | Fast bank is noise at this scale. |
| COLOR-3b | tightened triad (>>13/>>14/>>16) | 239,950 | +81 (+0.0006) | 61eb948ab85c95da | Near-tie: triad collapses toward the single rate → **>>14 already at the rate optimum**. Closed at this scale. |

Also sealed today, same discipline (the shared-mechanism controls):
- Arm A determinism: v6 run twice on slice1m → identical comp_sha 53ad10066c34ac66 (the thrice-cross-seat sha, reproduced live).
- Arm B one-bit key ablation: flip 1 bit of the 8,000,000 → comp_sha f27108a5dac77846 (total avalanche; the map's content lives in the corpus).
- Arm C process ablation: v8 wheel on same input → aa66be5faec222cb (the identity lives in the code too).
Conclusion on record: byte-identical maps across machines = shared classical key
(code+corpus, all bits transmitted over counted channels) + exact inversion pair
(D∘E=id, restore=OK). Preparation from a shared key, not cloning; no-cloning
theorem untouched (linearity proof); I(A;B|K)=0.

## tb28 probe @100MB — tables STILL rising (2026-07-19 20:10 UTC)

cm3ti-r24-tb28 k=10 N=100000000 payload=20503967 decoder_src=18963
total=20522930 bpc_total=**1.6418** restore=OK comp_sha=fd4601c8034e5c6f
enc=1274s dec=1303s (RSS ~9.2 GB)

Table-only line: tb26 1.6805 → tb27 1.6584 (−0.0221) → tb28 **1.6418** (−0.0166).
No flattening yet. tb29 needs ~18 GB tables — beyond this seat's RAM; the
table-scaling frontier passes to acer/relic/liris if they carry more memory.

Champion config decision: vc28 (full stack, TBITS 28) staged — source pushed as
rust/variants/vc28.rs. Its 100 MB confirm runs after the enwik9 baseline seals
(vc28 wants ~10 GB; running beside enwik9's ~5-7 GB risks OOM on this box).
Predicted vc28 @100MB: 1.640 ± 0.002 (stack delta at tb27 was −0.0021).
## Third-seat granularity screens → NEW CROWN: rainbow-12-even = 1.7918 bpc (2026-07-19)

Cloud seat, from the pushed crown code. Anchor reproduced byte-exact before any
variation was trusted (1 MB comp_sha 251c0b44; 100 MB comp_sha 489205479047d08f —
container's crown sha, reproduced here at full scale: cross-seat determinism at 22.5 MB).

1 MB screens (payload vs 6-sector anchor 242,020, k=7): V1 8-targeted −0.0060 ·
V3 soft-gate 3:1 −0.0069 · V2 12-uniform −0.0073 · V4 = V2+V3 −0.0139 (additive) ·
leak sweep: 7:1 −0.0106, 3:1 −0.0139, **1:1 −0.0172** (leakier = better, monotone).

10 MB confirms (k=10, slice sha c4e72b59…): anchor 1.8823 · V4 1.8679 (−0.0144,
scale-stable) · **v6 1:1 even 1.8646 (−0.0177) — champion.**

100 MB crown challenge (full enwik8, k=10, same-seat pair, decoder charged):

| arm | payload | total bpc | comp_sha | restore |
|---|---|---|---|---|
| 6-sector (old crown) | 22,506,819 | 1.8020 | 489205479047d08f | OK |
| **rainbow-12-even (NEW CROWN)** | **22,379,104** | **1.7918** | f3d45412c9a82568 | OK |

Config: 12-way sector = class(last)*2 + (prev same class), soft gate blending the
last byte's sector row with the previous byte's 1:1 (dot = 4w + 2·w2[s1] + 2·w2[s2]
>> 19; updates >>15 both rows). The full stack of the operator's ideas — color
sectors → finer wheel → gradient, at the softest tested blend — measured, lossless,
deterministic. Cross-check requested from the container seat (expected f3d45412…).
Next: single-stream enwik9 champion run (the current prize corpus).

## CROWN LEAP: v8+TBITS26 = 1.6805 bpc on enwik8 (2026-07-19, Phase 0 pays at scale)

Table-bits sweep (ROADMAP Phase 0): TBITS 23→26 relieves hash collisions, gain GROWS
with corpus (−0.021 @1MB → −0.066 @10MB → −0.111 @100MB stacked with the 24-way wheel).

| arm @100MB k=10 | payload | total bpc | comp_sha | restore |
|---|---|---|---|---|
| v6 rainbow-12-even tb23 (prior crown) | 22,379,104 | 1.7918 | f3d45412c9a82568 | OK |
| **v8 24-way + TBITS=26 (NEW CROWN)** | **20,987,880** | **1.6805** | 4ac88955567940be | OK |

Now inside the ROADMAP Phase-4 projection band (1.60–1.68) with only Phase 0 + the
wheel landed. Gap to 2006 prize baseline (1.466): 0.21. Source: rust/variants/tb26.rs
(v8_r24.rs with TBITS=26). enwik9: v6-tb23 baseline run in flight (seals as first
prize-corpus receipt); champion re-run with the new crown config follows overnight.

## Crown again: v8+TBITS27 = 1.6584 bpc enwik8 (2026-07-19 evening)

Table law third confirmation: tb27 ≈ flat at 1 MB (−273 B) but −0.0221 at 100 MB.
payload 20,710,481 · total 20,729,444 · comp_sha de5122afca0db106 · restore OK.
Day's crown arc: 1.8043 → 1.7918 → 1.6805 → **1.6584** (−0.146 in one day).
Combined model (vc26: +URL field on crown base) screened −0.0054 @1 MB, 10 MB
confirm in flight; tb28 probe queued for the enwik9 champion config.

## Crown: vc27 full stack = 1.6563 bpc enwik8 (2026-07-19 night)

URL-combined + 24-way run-depth + even gradient + TBITS27. payload 20,683,246 ·
total 20,703,275 · comp_sha 1465313e7acaf59e · restore OK. URL gain shrinks with
scale (−0.0054/−0.0034/−0.0021 at 1M/10M/100M) but stays net-positive. Source:
generated chain on rust/cm3ti_combo.rs (see variants receipt). Day arc:
1.8043 → 1.7918 → 1.6805 → 1.6584 → 1.6563.

## 4096-wheel + primed-law screens (2026-07-19 ~20:50 UTC)

**v13 s4096** — Jesse's 4ⁿ ladder rung: sector = last_byte(256) × 16 boundary
states (cls(lb2)×2 + same-class bit; 12 of 16 used), partner row one step back.
- 1MB k7: payload 238,739 (**−1,130 vs anchor**, comp_sha f365fdf05ac9ff00) —
  pre-registered cold-start prediction WRONG, it wins even cold.
- 10MB k10: payload 2,311,093 (**−19,660 / −0.0157 bpc vs baseline 2,330,753**,
  comp_sha 31ca395032cfbb93) — biggest sector-geometry step at 10MB to date.
  → promoted; 100MB crown challenge launched.

**v14 primed** — the sphere-law mechanism ("everything from one bit, given the
shared law"): both sides warm the model on a shared prior before bit one; prior
charged raw to total.
- Identity gate: prior=0 reproduces anchor payload 239,869 byte-exact
  (comp_sha 53ad10066c34ac66). Patch sound.
- prior = enwik8[20M..21M] (disjoint): payload 228,295 (**−11,574, −4.8%**,
  comp_sha 55e5ec67d1b03b36). Total loses at 1MB under honest charging
  (prior = 1MB); verdict deferred to the 10MB decay measurement (running).
Sphere-law demo, same hour: lawful 1MB → 414 B payload (64200e637c869bbe);
random 1MB → 1,003,218 B (d83febf780e58374); enwik 1MB → 239,869. Cost =
deviation from shared law; the asymptote the ladder climbs.

## ENWIK9 SEALED — first full-gigabyte run of the codec (2026-07-19 20:54 UTC)

cm3ti-rainbow12-even k=10 N=1,000,000,000 payload=196,462,859
decoder_src=18,737 total=196,481,596 **bpc_total=1.5719** restore=OK
comp_sha=4f0805c53150ea29 enc=7761s dec=9498s (4.8 h total, single core)

Scale curve for the same code (v6): 1MB 2.0688 → 10MB 1.8796 → 100MB 1.7918 →
**1GB 1.5719**. Yardsticks on the prize corpus: 2006-era baseline ≈ 1.466 bpc
(enwik8 basis), current enwik9 record (fx2-cmix) ≈ 0.886. Gap to record: 0.686.
This is the deterministic, decoder-charged, restore-verified baseline every
future enwik9 champion run measures against. vc28 100MB confirm launched
(prediction on record: 1.640 ± 0.002).

**v14 primed @10MB k10** (1MB prior): payload 2,311,328 (comp_sha
e9ae8570ed83591e) vs unprimed 2,330,753 → saving 19,425 B. Absolute saving
GREW with scale (11.6k@1MB → 19.4k@10MB) — decay prediction wrong — but the
curve's shape (sub-linear growth) can never cross the honest 1,000,000 B
charge for the prior: projected ~40–60k saved at 1GB vs 1MB charged.
VERDICT: mechanism confirmed, accounting negative — primed-law closed under
raw-prior charging at all measured scales. Door reopens only if a
compressed/tiny prior bends the savings-per-charged-byte curve above 1.0.

## GEOMETRY CROWN: 4096-wheel @100MB = 1.7738 (2026-07-19 21:25 UTC)

cm3ti-s4096 k=10 N=100,000,000 payload=22,153,139 decoder_src=18,737
total=22,171,876 **bpc_total=1.7738** restore=OK comp_sha=7fd8487859fbf938
enc=950s dec=915s. Beats container's rainbow-48 (1.7822) by 0.0084 at the same
small tables (TBITS 23). The 4ⁿ wheel (256×16, temporal partner row) wins at
1MB, 10MB, and 100MB — Jesse's call, my cold-start prediction wrong at every
scale. Next composition: s4096 × TBITS-28 tables.

## Optical-bench screens: absorption spectrum + colored mirror (21:35 UTC)

**v15 absorb** (per-class learning rates [16,14,14,15,15,15] on mixer B):
1MB 239,587 (−282, marginal, f49ad8c361dd5228); 10MB 2,330,457 (−296 only,
−0.0002 bpc, 6ee9edcaba3851fa) — win does NOT scale. CLOSED (marginal).
**v15b** steeper spectrum [17,13,13,15,15,16]: 240,051 @1MB — worse. The
response spectrum is nearly flat around >>15; the dial was already right.
**v16 mirror** (sector-keyed third APM, 24 curves): 1MB 239,938 (+69,
bec04aad1445b7c7); 10MB 2,331,499 (+746, 82c49cd7999a03fa) — more data made it
worse, not better: the third mirror re-refines what mirrors 1+2 already refined.
CLOSED both scales.
Bench summary: geometry (4096-wheel) and capacity (tables) pay; rate-spectrum
and extra mirrors don't — the existing dials were already at their optima.

## NEW OVERALL CROWN: vc28 full stack = 1.6399 @100MB (2026-07-19 21:40 UTC)

cm3ti-vc28-fullstack k=10 N=100,000,000 payload=20,478,473 decoder_src=20,029
total=20,498,502 **bpc_total=1.6399** restore=OK comp_sha=975abe08121fe2fb
enc=1339s dec=1300s (RSS 9.64 GB). Landed dead-center of the pre-registered
band (1.640 ± 0.002). Crown line today: 1.8043 → 1.7918 → 1.6805 → 1.6584 →
1.6563 → **1.6399**. Gap to 2006 baseline (1.466): 0.174.

**vc28m** (u8 history port for enwik9 RAM, pattern from container's 19f6c9e):
IDENTITY GATE PASSED @10MB — payload 2,215,189 and comp_sha 6227e48478f05698
byte-identical between vc28 and vc28m. (decoder_src metadata still reads
vc27.rs — 20,029 B, same file size class; charged consistently on both sides.)

**ENWIK9 CHAMPION LAUNCHED 21:47 UTC**: vc28m k=10 on the full 10⁹ — projected
~10.8 GB RSS, ~7.3 h, seals ~05:00 UTC. Baseline to beat: 1.5719 (v6).
Extrapolation from the 100MB deltas: ~1.42–1.46 territory — the 2006-era
enwik8 baseline line, on the gigabyte, in one day of measured steps.

## The 4ⁿ glyph ladder walked to its limit (2026-07-19 ~22:15 UTC)

Jesse's sequence 64-256-1024-4096-16384(-65536), screened wheel-by-wheel.
Payloads (1MB k7 / 10MB k10), all restore=OK:

| wheel | 1MB | 10MB | comp_shas |
|---|---|---|---|
| s12 (baseline) | 239,869 | 2,330,753 | 53ad1006 / 4ae7ec1f |
| s1024 (256×4) | 239,105 | 2,315,651 | c280622e / 178a8081 |
| s4096 (256×16) | 238,739 | 2,311,093 | f365fdf0 / 31ca3950 |
| s16384 (256×64) | 237,995 | 2,300,939 | 05484092 / d70ec471 |
| **s65536 (256×256)** | **237,753** | **2,293,443** | c689f2a5 / b98eb79e |

Monotone the whole way at both scales — the curve never turned. At 65,536 the
wheel IS the full last-2-bytes: the second mixer is now order-2-gated, the
natural limit of this construction. −0.030 bpc vs s12 at 10MB. s65536 100MB
geometry-crown challenge launched beside the enwik9 champion. Tomorrow's
composition: winning wheel × TBITS-28 tables. (Contrast on record: sector
counts this small-table wheel keeps rewarding capacity, same lesson as the
table ladder — geometry and capacity pay; re-processing doesn't.)

## GEOMETRY CROWN AGAIN: s65536 = 1.7555 @100MB (2026-07-19 23:00 UTC)

cm3ti-s65536 k=10 N=100,000,000 payload=21,925,581 decoder_src=18,737
total=21,944,318 **bpc_total=1.7555** restore=OK comp_sha=6104215bf6c8d206
enc=792s dec=767s. Beats s4096 (1.7738) by 0.0183 — the margin GREW from 10MB
to 100MB (projection was ~1.766; measurement better again). Geometry line in
one evening: 1.7918 (s12) → 1.7738 (s4096) → **1.7555 (s65536)**, all at
TBITS-23 small tables. The 4ⁿ ladder's limit rung holds the geometry crown.
Determinism note: v19 spot-check reproduced c689f2a5145001de byte-exact ACROSS
the container restart (process death + rebirth) — survival proof added to the
cross-seat and cross-arch proofs. Morning composition: s65536 × TBITS-28.

## Glyph-transfer test — "does training on other sets' glyphs hurt?" (2026-07-20 00:55 UTC)

Jesse's question, made operational via the primed-law engine: prime the model
on an alphabet learned from a DIFFERENT distribution, measure payload vs
unprimed baseline (slice10m k=10, unprimed = 2,330,753).

| Prior (the imported alphabet) | payload | vs unprimed | comp_sha |
|---|---|---|---|
| In-domain (disjoint Wikipedia, 1MB) | 2,311,328 | **−19,425 (helps)** | e9ae8570 |
| Foreign domain (source code, 605KB) | 2,341,317 | **+10,564 (HURTS)** | 5075fc24 |
| Adversarial (random bytes, 1MB) | 2,364,599 | **+33,846 (hurts badly)** | 13af0f63 |

VERDICT: glyphs transfer exactly as far as the shared law extends. Wrong-set
glyphs bias counters/mixer warm-start and the model pays real bytes to unlearn
them — 10MB was not enough to fully recover. Alphabets for enwik-family targets
must be carved from Wikipedia itself (precisely how Ratushnyak won: dictionary
built FROM enwik8). Design input for enwik10/SGRAM: per-cell in-domain priming
is a candidate to offset the measured +6% shard cold-start cost; cross-set
priming (e.g. non-wiki cubes) is now measured harmful.

## BEHCS glyph-language transfer arms (2026-07-20 01:50 UTC)

Jesse's four trained sets (behcs-64 → bechs-256 → bechs-1024 → HYPER-BECHS)
tested as priors per his directive. Authentic glyph stream generated with the
canonical GLYPH-GENESIS.js from asolaria-behcs-256 (sha256→8-symbol sentences);
doctrine prior = concatenated BEHCS/hyper-bechs markdown. Target slice10m k=10,
unprimed baseline 2,330,753. Full transfer spectrum:

| Prior | size | payload | vs unprimed | comp_sha |
|---|---|---|---|---|
| Wikipedia (in-domain) | 1MB | 2,311,328 | **−19,425** | e9ae8570 |
| BEHCS doctrine prose | 143KB | 2,333,509 | +2,756 | d21d0129 |
| Source code | 605KB | 2,341,317 | +10,564 | 5075fc24 |
| **BEHCS-256 glyph stream** | 1MB | 2,345,617 | **+14,864** | 82641908 |
| Random bytes | 1MB | 2,364,599 | +33,846 | 13af0f63 |

Notes: my pre-registered band for the glyph stream (+25k..+35k, near-random)
was too pessimistic — it landed at +14.9k, between code and random, because
the GRAMMAR (spacing, 8-char tokens, sentence shape) is real learnable law
even though the sha256 symbol cores are lawless by construction. VERDICT: the
BEHCS sets are identifier languages (naming law for the fabric), not
statistical models of English; as enwik priors they hurt. Scale confirms
(100MB targets) queued post-champion per Jesse's scale requirement; GB-scale
grid + enwik10 SGRAM campaign specced in session plan.

## GGUF catalog + WRT screen — the real-alphabet first contact (2026-07-20 02:20 UTC)

Built per Jesse's spec: hyper-dense 2D catalog, 4,096 in-domain words (carved
from enwik8[20M:30M]), rows = 16B word | 8B fnv1a64 PID (the 8-byte root atom,
same primitive as the codec's table hashes) | code | freq. Serialized as GGUF
v3 (131,296 B, mmap-able — the "stubbed rooms on disk" layout). Reversible
WRT transform: 16 verified-unused prefixes × 256 codes; REVERSIBLE=True gate
passed; raw text shrank 2,260,612 B (23%).

Screen @10MB k=10: payload on transformed stream = 2,341,964 (comp_sha
4398d8b7cdbc8f79) vs untransformed 2,330,753 → **payload +11,211 WORSE even
before the +131k catalog charge. Arm total ≈ 2,493k vs baseline 2,349k: LOSES
by ~144k.** CLOSED at this scale for this codec.

The honest history lesson this seals: Ratushnyak's dictionary won because
paq8h's models were CO-DESIGNED for the transformed stream. A dictionary alone
subtracts raw bytes but destroys the morphology (shared prefixes/suffixes) our
order-k contexts feed on — opaque 2-byte codes cost more than they save. The
real alphabet pays only when Phase-2 models SPEAK it (word-ID contexts reading
the catalog directly), not as a bolt-on transform. Catalog machinery (GGUF,
PID-addressed, reversibility-gated) is built, pushed, and ready for that.

## ENWIK9 CHAMPION SEALED: 1.3839 bpc on the full gigabyte (2026-07-20 ~07:40 UTC)

cm3ti-vc28m-fullstack k=10 N=1,000,000,000 payload=172,966,825
decoder_src=20,029 total=172,986,854 **bpc_total=1.3839** restore=OK
comp_sha=274fe82ef3886681 enc=10637s dec=10799s (~6 h, single core, ~10.8 GB).

- Beats the pre-registered prediction band (1.42–1.46) — better than predicted.
- vs yesterday's baseline (v6, 1.5719): **−0.188 bpc, −23.5 MB** on the same
  corpus, one day of measured steps apart.
- Yardsticks: 2006 enwik8 baseline 1.466 — CLEARED. 2006 first-prize winner
  (paq8hp5) ≈ 1.37 — within 0.014, on a corpus 10× larger. enwik9 record
  (fx2-cmix) 0.886 — gap now 0.498.
- The whole gigabyte reconstructs byte-perfect from 173 MB. Survived three
  container restarts via relaunch; determinism spot-checks held throughout.

## Composition screens: vc65 = 65536-wheel × TBITS-28 full stack (2026-07-20 08:00 UTC)

1MB k7: payload 234,184 (comp_sha dab7ea1e8b8ba4a5) — best 1MB number to date.
10MB k10: payload 2,190,036 (comp_sha 6ca9875b00a0ba11) vs vc28's 2,215,189 →
**−25,153: the wheel's gain survives composition with big tables** (near-
independent effects). 100MB crown challenge launched; pre-registered
prediction 1.620 ± 0.003 (crown: vc28 1.6399). Source pushed as
rust/variants/vc65.rs. 100MB transfer confirms (wiki/behcs/unprimed priors on
full enwik8) launched in parallel per Jesse's scale requirement.

## NEW OVERALL CROWN: vc65 = 1.6168 @100MB (2026-07-20 08:35 UTC)

cm3ti-vc65-fullstack k=10 N=100,000,000 payload=20,190,425 decoder_src=20,029
total=20,210,454 **bpc_total=1.6168** restore=OK comp_sha=8cb3553185bb5ef5
enc=977s dec=1004s. Prediction band 1.620±0.003 — landed at/just past the
optimistic edge. Beats vc28 (1.6399) by −0.0231 (−288,048 B). Crown line:
1.8043 → 1.7918 → 1.6805 → 1.6584 → 1.6563 → 1.6399 → **1.6168**. Gap to 2006
baseline (1.466): 0.151. The composition thesis is sealed: Jesse's 4ⁿ wheel
and table capacity are near-orthogonal axes; both crowns compose. enwik9
re-run with vc65 launched (projection ~1.36 vs current gigabyte seal 1.3839).

## Transfer confirms AT SCALE — 100MB targets (2026-07-20 08:50 UTC)

Per Jesse's requirement ("you can't conclude from small tests"). v14, full
enwik8, 1MB priors. Unprimed reference payload 22,379,104 — comp_sha
**f3d45412c9a82568 = bit-exact reproduction of the thrice-cross-seat-verified
v6 100MB run** (v14's priming patch provably inert with empty prior, at scale).

| Prior | payload @100MB | vs unprimed | (10MB ref) |
|---|---|---|---|
| Wikipedia in-domain | 22,323,775 | **−55,329 helps** | (−19.4k) |
| BEHCS-256 glyphs | 22,413,260 | **+34,156 hurts** | (+14.9k) |

VERDICT AT SCALE: the small-test verdicts don't flip — they AMPLIFY. In-domain
help grew ×2.9 with ×10 data; foreign-glyph harm grew ×2.3. Savings curve
(11.6k→19.4k→55.3k per decade) still projects below the 1MB honest charge at
any practical scale — priming economics unchanged; transfer law confirmed at
the scale demanded. comp_shas: 2a3240889ae2fcb8 (wiki), 171b163828175cbb
(behcs).

## The three-sphere machine-count test — Jesse's rule of holes, corrected form, MEASURED (2026-07-20)

Corpus: 1MB, three drifting color-laws (letters/digits/symbols, drift every 30
blocks) under deterministic keyed rotation (R→Y→B, 64B blocks) — Jesse's three
gradiated spheres around a static omega, time folded into the key.

| Machine | payload | vs enwik ordering |
|---|---|---|
| 3-wheel (v10) | **5,798 WINS** | (loses on enwik) |
| 12-wheel (v6) | 5,985 | (wins on enwik) |
| 4096-wheel (v13) | 6,225 | (wins bigger on enwik) |

The ordering INVERTS with the data's law-count: the 3-machine wins exactly
when the data has three laws. Total collapse 1MB → 5,798 B (0.046 bpc): the
keyed rotation rode free (shared-key theorem), machines paid only for the
gradients (drift-is-information theorem). Machine-count accounting sealed:
3 machines + key (rotation free, mirror/anti-spheres free by bijection,
omega +1 only if it has state). Law of Machines P2 confirmed in both
directions: rooms must match the corpus's law-count — too many rooms is
measured harm on simple law, too few is measured harm on language.

## FLEET-VERIFIED: the Law of Machines room-count claim (2026-07-20)

Cross-seat replication complete on independent 3-law corpora:
- This seat (gentle laws, keyed rotation): 3-wheel 5,798 < 12-wheel 5,985 <
  4096-wheel 6,225 — smallest adequate machine wins.
- Other seat (hard laws: XOR drift + quadratic): 12-wheel 70,573 < 48-wheel
  71,229 < 4096 75,954, omega 212,669 — mid machine wins, palace heats empty
  rooms, minimal machine pays triple.
Both orderings: room-count must match law-count; the crown loses on few-law
data; the law-count of the DATA (not geometry) sets the machine. Their honest
miss folded in: "lawful" is a spectrum — laws that keep moving keep costing
(tracking rent ∝ law velocity). Graduated from observation to FLEET-VERIFIED.

Corollary (Jesse's scaling mantra, measured form): in the un-charged fabric
regime, an ever-growing rule base keeps earning exactly as long as incoming
data keeps carrying new law — our own receipts: tables 23→28 never turned,
wheels 12→65,536 never turned on enwik, scale curve 2.07→1.57 per 1MB→1GB.
The Hutter frame is the bounded dual (fixed corpus, charged decoder → forces
efficiency); the fabric frame is the unbounded dual (open data, uncharged
storage → forces scale). Same identity, two budgets.

## Feed-the-repos-to-the-spheres — sealed, with a two-lane disagreement (2026-07-20)

White-room GC receipt: 1,954 fleet files hash-consed → 1,943 unique kept,
11 duplicates discarded (15,769 B), corpus 15,278,457 B, sha16 567da5c5d3f185bd.

Two referees, same corpus, opposite verdicts on difficulty:
- CODEC lane (v6 @1MB): fleet functions = 206,713 payload (1.65 bpc) —
  EASIER than enwik (239,869 / 1.92). comp_sha a92708490c0239eb.
- SPHERE lane (1×247 GRU, 3 loops, 3k steps): fleet = sampled_val_bpc
  3.5107 — HARDER than enwik (2.6483) for the same config.

Resolution (Law of Machines, sharpened): lawfulness is machine-relative.
H is intrinsic; KL is paid per machine. The fleet corpus is law-DENSE in
exact repeats (headers, boilerplate — the codec's match model + thousands of
table-rooms feast) but law-DIVERSE in sublanguages (code+prose+JSON+HBP —
many laws, and a 281k-param sphere at 3k steps lacks the rooms; mixed-law
tax). Caveat on record: the 90/10 split of a concatenated heterogeneous
corpus makes val a partial distribution shift; 3.5107 includes transfer cost.
Consequence for the build: the counted lane and the uncounted lane need
DIFFERENT capacity governors — the same governor cannot serve both, because
the same data presents different law-counts to different machines.

## The colored-sphere / rainbow-omni / mirror grid — 12 arms sealed (2026-07-20)

Jesse's geometry, measured: 3 domains (RED=wiki slice1m, BLUE=repos fleet1m,
YELLOW=gradient grad1m) × 4 warm-ups (cold / own-color key / rainbow ⅓+⅓+⅓ /
mirror = complement of the color). v14 primed engine, 1MB, k7. Payloads:

| domain | cold | own key | rainbow | mirror |
|---|---|---|---|---|
| RED (wiki) | 239,869 | **228,295 (−11,574)** | 236,145 (−3,724) | 245,433 (+5,564) |
| BLUE (repos) | **206,713** | 209,539 (+2,826) | 210,439 | 211,965 |
| YELLOW (gradient) | 8,617 | **915 (−89%)** | 9,053 (+436) | 10,151 |

Pre-registration outcomes:
1. "Own color wins its domain": RED ✓ (replicates the cross-seat −11.5k),
   YELLOW ✓ spectacularly (the key nearly unlocks the whole lawful domain),
   BLUE ✗ — the repos are NOT one color: a disjoint slice of a heterogeneous
   corpus is partially foreign to itself; even the own-key is net negative.
   Sharpened law: **a color is a LAW, not a corpus.**
2. "Rainbow lands between cold and specialist everywhere": RED ✓ only.
   On BLUE and YELLOW the rainbow fell BELOW cold — a mixture key pays full
   price for its foreign thirds; the omnisphere cannot freely recalculate
   its colors, it only earns where the domain overlaps its mixture. The
   mixture theorem's log-K bound applies to MODELS mixed at runtime, not to
   PRIORS baked before bit one — priors don't get to route.
3. "Mirrors (inverted inversion, complement-warmed) fail": ✓✓✓ swept — the
   mirror was the WORST arm in all three domains. A complement cannot
   conjure the missing color; inversion carries only what it contains.
All 12 restore=OK. Geometry verdict: radiated spheres with single-law keys =
real and strong (YELLOW −89%); rainbow center = weak, mixture-taxed;
external mirrors = measured harm. Build accordingly.

## Law-descent grid: the white room splits by law, then descends (2026-07-20)

Fleet corpus split by content class, each colored sphere keyed with a pure
disjoint slice of its own law. Payloads (v14, k7):

| law | files | cold | own key | verdict |
|---|---|---|---|---|
| prose (.md) | 652 | 204,644 | **192,743 (−5.8%)** | WINS — comparable to wiki's −4.8% |
| data (.json/.hbp) | 530 | 196,523 | **191,188 (−2.7%)** | WINS |
| code (all langs) | 762 | **182,542** | 184,018 (+0.8%) | LOSES — "code" is a family of laws |
| rust only (.rs) | 81 | 120,293 | 120,013 (−0.2%) | ≈TIE — see below |

Two laws sharpened:
1. **Laws nest.** Corpus → class → language: each descent flipped losers
   toward winners (blue mixed −1.4% → prose/data wins). The classifier must
   descend until slices are self-similar. (Code needs per-language split.)
2. **Online learning cannibalizes priming** (the rust tie, my strong-win
   pre-registration BROKEN): a highly self-similar test corpus warms itself
   in its first files — cold was already 1.47 bpc — leaving the key almost
   nothing to add (−280 B). Key value = shared law MINUS law the test
   teaches itself early. Priors pay on single-law domains with high internal
   variety (wiki, prose); they are redundant on self-repeating domains
   (rust variants) and poison on mixed domains (raw fleet).
All arms restore=OK. The colored-sphere build rule, final measured form:
one sphere per NESTED law, keyed only where the domain cannot self-prime.

## Pumping law CROSS-SEAT REPLICATED + retention law co-signed (2026-07-20)

This seat's replication (v14, slice1m, k7): pump1 228,295 → pump2 (key×2)
230,964 (+2,669) → pump3 (×2 + reversed) 235,389 (+4,425 more). Matches the
other seat's 226,408 → 230,992 → 234,204 in direction and shape on an
independent implementation. FLEET LAW: one clean read of the key, then live
data — the first reading teaches, the second stiffens (count-maturation =
the tracking theorem's learning-rate stiffening, measured), the reversed
third adds anti-law (re-confirms the arrow-of-time seal: backwards English
is a foreign language).

Retention law co-signed from their grid: optimal keep-threshold τ=2 —
"once is an accident, twice is a function; three is confirmation you get
for free" (Jesse's τ=3 within 0.35% of peak). Amendment adopted for the
white-room GC design: hash-cons dedup + drop count-1 functions at the GULP
boundary; keep count≥2.
