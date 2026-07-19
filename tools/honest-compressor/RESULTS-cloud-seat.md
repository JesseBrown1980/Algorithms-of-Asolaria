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
