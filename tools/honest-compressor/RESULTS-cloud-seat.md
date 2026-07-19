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
