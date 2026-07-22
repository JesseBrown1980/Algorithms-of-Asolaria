# ROADMAP — from the cubes to the language (2026-07-19)

State: crown = rainbow-12-even 1.7918 bpc enwik8 (pushed 3e23bfa). v8 (24-way)
confirmed at 10 MB (−0.0253 vs anchor), queued for 100 MB. enwik9 champion run
in flight. Wheel optimum ≈24, leak optimum = 1:1 — both curves fully mapped.
Every claim below carries pre-registered bands; every run is SHA-lossless-gated,
deterministic, decoder+dictionary charged. The measurement is the referee.

## Phase 0 — Table-size sweep (tonight; cheap; possibly free money)
WHAT: hash-table bits 23 → 24/25/26 in cm3ti-family; nothing else changes.
WHY: tables sized for 1 MB screens are collision-saturated at 100 MB+; Hutter
budget allows 10 GB RAM, we use a fraction.
COST: two-line diffs; runs are the cost (screen 10 MB, confirm 100 MB).
BANDS: >0.010 @100 MB = adopt; 0.003–0.010 = adopt if RAM fits enwik9;
≤0.003 = closed. PREDICTION: +bits pays 0.02–0.05 at enwik9 scale.
SEAT: cloud (this one), immediately after the enwik9 champion seals.

## Phase 1 — THE LANGUAGE LAYER: dictionary transform (the big rock)
WHAT: word-replacing transform (the Hutter lineage's WRT/DRT): learn the top-N
frequent words from the corpus offline; replace each occurrence with a 1–2 byte
code; escape mechanism for everything else; dictionary shipped and charged.
Codec then models WORD symbols instead of re-learning English spelling forever.
WHY: the single largest known unclaimed rung (~0.08–0.15 bpc historically);
it is the difference between our 1.79 tier and the 1.4–1.5 tier. This is
"building the language": words become the glyphs — the original glyph vision,
landed at the layer where it actually pays.
GATES (strict order):
  1. TRANSFORM REVERSIBILITY FIRST: transform+inverse must be byte-exact on
     the full corpus BEFORE any compression is measured. A single mismatched
     byte = the phase halts. (This is where naive WRTs die; ours won't ship
     without this gate green.)
  2. Screen dictionary sizes: N = 1k / 4k / 16k words @1 MB → confirm best two
     @10 MB → champion @100 MB, decoder + dictionary fully charged.
  3. Case/punctuation handling measured as variants (capital-flag trick vs raw).
BANDS: >0.030 @10 MB = the new mainline; 0.010–0.030 = adopt, keep tuning;
≤0.010 = investigate before abandoning (history says it should pay far more).
PREDICTION: −0.06 to −0.12 @100 MB when tuned.
SEAT: cloud builds the transform + gates; container cross-checks reversibility
independently (its own inverse implementation — two implementations must agree).

## Phase 2 — Context-model fan-out (parallel across seats; each 0.005–0.03)
Aimed by the shadow extractor's measured hot map. Each seat takes one model,
same anchor discipline (reproduce 251c0b44 @1 MB k7 before variants):
  a. UTF-8/foreign-span context (extractor Priority 2) — container
  b. INDIRECT context (what followed this context last time) — cloud
  c. Sparse/skip contexts (gap positions −2,−4) — acer
  d. Wiki-table/column model — relic/liris screens
BANDS: standard (>0.003 promote / 0.001–0.003 marginal / ≤0.001 closed).
Winners stack into the mainline one at a time, each re-confirmed.

## Phase 3 — Mixer depth (after Phase 2 models exist)
  a. True two-layer mixer: second layer selected by (match-state, entropy
     regime); replaces flat sum. PREDICTION: 0.01–0.02.
  b. Confidence-weighted gradient: blend top-2 sector rows by classifier
     confidence instead of fixed prev-byte neighbor (the honest "soft
     membership" form of the rainbow). PREDICTION: 0.003–0.010.

## Phase 4 — Integration crowns
Best full stack → enwik8 crown run → single-stream enwik9 champion → RESULTS.
Projection if Phases 0–3 pay their bands: 1.60–1.68 on enwik8 — striking
distance of the 2006 prize BASELINE (1.466), with the 2006 winner (1.366)
visible. Honest note: every rung past that is exponentially harder; the record
(0.886) remains a multi-year mountain. No configuration goes below N·H(X).

## Standing rules (unchanged, binding)
Screen cheap → confirm at scale → crown at 100 MB only. Single-stream for
flagship numbers. Anchors before variants. Pre-registered bands before runs.
Both-side predictions on record. Towers without operations stay HELD.
