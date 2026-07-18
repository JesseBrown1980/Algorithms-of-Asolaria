# Honest Compressor — Measured Results (2026-07-18)

Seat: Anthropic cloud container (Cowork session), Python 3.11, numpy.
Every number below is byte-exact and total-counted (payload + decoder + dictionary).
Every row passed the SHA-256 restore gate; a failed restore invalidates the row.
The measurement is the referee.

## Corpus

| item | value |
|---|---|
| source | enwik8 (mattmahoney.net), first 1,000,000 bytes |
| slice SHA-256 | `369b688978f649681136198fb96db14c1616756260c55fb4b65e9bc049552cad` |
| N | 1,000,000 bytes |
| order-0 entropy H₀(X) | 5.0589 bits/byte (195 distinct bytes) |
| order-0 floor N·H₀/8 | 632,357 bytes |

Floor note (spec formula 5): `total_bits ≥ N·H(X)` where H(X) is the **source**
entropy (the entropy rate, ≈1.0–1.5 bpc for English text), not the order-0 byte
entropy. Context models legitimately code below H₀ because they exploit conditional
structure; nothing here codes below the source entropy rate, and no row claims to.
No decode step reads any external data: the decoder file + shipped dictionary +
payload are the complete decode inputs, and all three are counted.

## Baselines (identical slice, standard tools)

Baseline sizes are the emitted stream only — their decoders (gzip ~100 KB binary,
xz ~700 KB, etc.) are **not** charged, while the Asolaria totals below **do** charge
the full decoder source. The comparison is therefore tilted against us; it is kept
anyway because it is the honest convention of the field.

| tool | bytes | bpc | restore |
|---|---|---|---|
| gzip -9 | 355,362 | 2.8429 | OK (SHA match) |
| zstd -19 | 300,067 | 2.4005 | OK (SHA match) |
| xz -9 | 290,692 | 2.3255 | OK |
| bzip2 -9 | 281,323 | 2.2506 | OK |

## Stock compressor (asolaria_cube_compressor.py, unmodified)

| merges | cube | V | glyphs | payload | dict | decoder | total | bpc_total | restore |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 256 | 1,000,000 | 473,959 | 0 | 5,441 | 479,400 | 3.8352 | OK |
| 512 | 0 | 768 | 446,900 | 339,794 | 1,481 | 5,441 | 346,716 | 2.7737 | OK |
| 1024 | 0 | 1280 | 375,164 | 323,508 | 3,175 | 5,441 | 332,124 | 2.6570 | OK |
| 1024 | 1 | 1280 | 375,040 | 323,449 | 3,170 | 5,441 | 332,060 | 2.6565 | OK |

Rung: **at gzip** (2.66–2.77 vs gzip 2.84), below bzip2/xz — exactly as the spec
states. The cube involution changes the result by 0.02% — noise, as the spec states.

## Context-mixing model (cm_asolaria.py, new — the one real lever)

Orders 0..k blended with per-context adaptive weights (Bayes mixture + fixed-share
per order-1 bucket), carryless range coder, optional BPE glyph layer. Decoder charge
is the full cm_asolaria.py source (9,138 bytes).

| merges | k | V | glyphs | payload | dict | decoder | total | bpc_total | restore |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 256 | 1,000,000 | 486,547 | 0 | 9,138 | 495,685 | 3.9655 | OK |
| 0 | 2 | 256 | 1,000,000 | 389,428 | 0 | 9,138 | 398,566 | 3.1885 | OK |
| 0 | 3 | 256 | 1,000,000 | 330,477 | 0 | 9,138 | 339,615 | 2.7169 | OK |
| 512 | 2 | 768 | 446,900 | 300,465 | 1,481 | 9,138 | 311,084 | 2.4887 | OK |
| **512** | **3** | **768** | **446,900** | **296,564** | **1,481** | **9,138** | **307,183** | **2.4575** | **OK** |
| 512 | 4 | 768 | 446,900 | 296,723 | 1,481 | 9,138 | 307,342 | 2.4587 | OK |
| 1024 | 3 | 1280 | 375,164 | 296,810 | 3,175 | 9,138 | 309,123 | 2.4730 | OK |
| 1024 | 4 | 1280 | 375,164 | 297,014 | 3,175 | 9,138 | 309,327 | 2.4746 | OK |

## Ladder (identical 1M slice, total-counted bpc)

```
stock merges=0        3.8352
stock merges=1024     2.6570
gzip -9               2.8429   <- stock compressor passes gzip at 1024 merges
cm 512,3              2.4575   <- new best, lossless, total-counted
zstd -19              2.4005
xz -9                 2.3255
bzip2 -9              2.2506
source entropy est    ~1.0-1.5 (GPU-model region, out of scope for this run)
```

## Findings

1. The context-mixing lever works exactly as the spec predicts: k=1→2→3 on raw
   bytes gives 3.97 → 3.19 → 2.72 bpc, the same trend as the spec's earlier
   measurement (4.52 → 3.77 → 3.38), and our implementation lands lower at each k.
2. Best measured config: **BPE-512 + orders 0–3 mixing = 2.4575 bpc total** —
   from the gzip rung (2.77 stock) to 0.057 bpc above zstd -19, closing 61% of the
   stock→zstd gap. Payload-only it is 2.3725 bpc, already below zstd's stream and
   0.047 above xz's — but the honest number charges the decoder, so 2.4575 stands.
3. k=4 is past the knee on 1M bytes (2.4587 > 2.4575): order-4 contexts are too
   sparse to pay for their dilution at this corpus size. More corpus, context
   hashing (bounded tables), and SSE/APM stages are the next CPU-honest steps
   toward xz; ~1.0 bpc still requires a GPU-trained predictor, out of scope here.
4. Nothing below entropy, no external data at decode, every restore SHA-verified.
   The cube involution remains a no-op (0.02%), confirming formula-5 discipline.

## Repro

```
head -c 1000000 enwik8 > slice1M.txt          # sha 369b6889...
python3 asolaria_cube_compressor.py slice1M.txt
python3 cm_asolaria.py slice1M.txt 0,1 0,2 0,3 512,2 512,3 512,4 1024,3 1024,4
```
