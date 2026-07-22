# Shadow extractor — a lens, not a codec

**This is an analysis/visualization tool. It selects and surfaces information that is
already in the data; it creates none. By the data-processing inequality a view cannot
contain more than its source. It makes NO compression claims. A beautiful shadow is
never a result — it only aims effort.**

## What it does
Instruments the deterministic `cm3ti` codec to log per-byte coding cost (centibits,
u16, behind `--costmap` — flag OFF is byte-identical to the canonical crown, comp_sha
`101c86ae…`, so instrumentation never perturbs the stream), then renders the byte
stream as 2D Hilbert-curve images under four color functions and reports where the
model spends its bits.

## The four lenses (enwik8, 10 MB distinct slice, 2048×2048 Hilbert tile)
- `shadow_a_loss.png` — prediction-loss: cm3ti bits/byte (bright = model struggles)
- `shadow_b_entropy.png` — local order-0 entropy (256-byte window)
- `shadow_c_class.png` — byte class (letter/digit/whitespace/markup/high-byte)
- `shadow_d_match.png` — log2 distance to most recent 8-byte match

## The deliverable: hot content → candidate context model
Measured (see `shadow_report.txt`): mean 1.895 b/B, median 0.870 — most text is cheap,
but a heavy tail burns. Hottest content, in order, and where the two-layer mixer should
aim:

| hot content (measured) | why it burns | CANDIDATE context to add | priority |
|---|---|---|---|
| **URLs / query strings** (loc.gov, base64 paths, yahoo redirects) | long, high-entropy, low-repeat, punctuation-delimited | **URL/path word model** — tokenize on `/ . : ? & =`, context on path segments | 1 |
| **foreign / UTF-8 multibyte spans** (Old Norse, Greek translit) | byte model can't see multibyte structure | **high-byte / UTF-8 sequence context** | 2 |
| **digits / numbers** (mean 3.42 b/B, hottest class) | weak numeric structure model | **digit-position / numeric-run context** | 3 |
| markup `<>&[]{}` and proper nouns / caps | tag depth, capitalization boundaries | markup-depth + case context | 4 |

The mixer screen should test candidates 1–3 first — that is the extractor doing its
job: turning "where should modeling effort go?" from a guess into a measured picture.

## Run
```
rustc -O cm3ti_instrumented.rs -o cm3ti_instr
./cm3ti_instr <file> <k> --costmap cost.bin   # dumps u16 centibits/byte
python3 render_shadows.py                      # renders the four PNGs
```
