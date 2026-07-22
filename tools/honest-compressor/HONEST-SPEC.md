# Honest Compressor Spec — the real formulas, the real code, the real ceiling

This is the complete, honest specification of the Asolaria cube compressor. Everything
here is real, buildable, and measured byte-exact (SHA-256 verified). Nothing is withheld.
It is written so that any agent — Claude Code Cloud or otherwise — can read it and run the
exact same experiment and get the exact same result.

It is also honest about what it does **not** do, because a spec that overpromises would
waste whoever runs it. Read the "Ceiling" section before spending compute on it.

## The whole engine, in five formulas

1. **Model prediction** (this is the only lever that lowers the size):
   For the next symbol `s` given context `ctx`:

       p(s | ctx) = freq[ctx][s] / Σ_k freq[ctx][k]

   A better predictor (higher order, context mixing, or a trained neural model) makes
   `p(s | ctx)` sharper for the true symbol, which lowers formula 2. That is where all real
   compression comes from.

2. **Cost of coding a symbol** (Shannon information content):

       bits(s) = −log₂ p(s | ctx)

3. **Range coder** (turns those probabilities into bytes, losslessly, no rounding loss):

       low   ← low + (Σ_{k<s} f_k) · (range / Σf)
       range ← f_s · (range / Σf)
       # renormalize: while range < 2^16, emit top byte of low, shift low and range left 8 bits

   Carryless variant constants used in the code: TOP = 1<<24, BOT = 1<<16, MASK = 0xFFFFFFFF.

4. **Glyph / BPE layer** ("recalculate the next layer"):
   Repeatedly replace the most frequent adjacent symbol pair `(a,b)` with a new symbol id.
   The dictionary of merges must be **shipped and counted** (varint-encoded pairs).

5. **The floor** (the boundary no configuration crosses):

       total_bits ≥ N · H(X),   where   H(X) = −Σ p log₂ p

   `H(X)` is the source entropy. This is the Shannon source-coding bound. It is a theorem,
   not a tuning limit.

## Why there is no sixth formula

There is no additional formula that gets below line 5, and this spec does not hide one.
The reasons, each independently sufficient:

- **Pigeonhole / counting.** A lossless code is injective. Strings shorter than `n` bits
  number `2^n − 1 < 2^n`. So no lossless code can shorten *every* input; gains on some
  inputs are exactly paid back by losses on others.
- **Bijections conserve entropy.** The "cube" transform is `x → reverse(x)` (an involution).
  For any bijection `f`, `H(f(X)) = H(X)`. Measured effect of the cube here: **0.46%**,
  i.e. noise. The full "omega cube" (the C₂³ group, 8 corners) adds exactly **7 bytes**
  (one recompute flag per extra face), not 8× anything.
- **Data-processing inequality.** For any function chain, `I(f(X); Y) ≤ I(X; Y)`. Stacking
  transforms, cascades, or extra "depth" of reversible geometry cannot manufacture
  information. This covers every multi-axis / multi-projection variant.

## Ceiling (read before spending compute)

- The engine is **correct and lossless** — restore equals input byte-for-byte or the run is
  invalid (SHA-256 gate in the code).
- On real text, the current model (BPE + order-1) lands **near gzip, below bzip2/xz**.
- The number goes **down only when the predictive model gets stronger** (higher order,
  context mixing, or a neural predictor). Measured with a context-mixing model: orders 0-1 →
  4.52 bpc, 0-2 → 3.77, 0-3 → 3.38. The trend is real and it points at the record region
  (~1.0 bpc, where cmix/nncp neural models sit — the estimated entropy of English).
- Reaching ~1.0 bpc requires **training a large predictive model on GPU compute**
  (GPU-hours), then shipping/using it. That is a GPU budget, separate from any agent plan.
  Agents can parallelize the *engineering* (a Rust port, config sweeps, the measurement
  harness) — they cannot substitute for GPU training, because an agent is not a GPU.
- **No configuration in this repo, or any repo, goes below `N · H(X)`.** If a run reports
  a size below the byte-exact total (payload + decoder + dictionary), it is a measurement
  bug, not a discovery. Trust the SHA gate and the total byte count.

## How to run it

    python3 asolaria_cube_compressor.py <path-to-a-real-text-file>
    python3 omega_cube.py <path-to-a-file>

Both print byte-exact totals and a restore check. The measurement is the referee: no claim
is accepted without a byte-exact, total-counted number.

## What is honest to say about this work

- "A real, lossless compressor implementing the glyph + cube ideas, measured byte-exact,
  competitive with gzip, bounded below by the source entropy." — true, defensible.
- "Beats the competition once the predictive model is trained up." — true *as a goal*, and
  legitimate; it means climbing toward the Hutter-record region, which is hard but allowed.
- "Compresses below entropy / stores arbitrary data in a fixed small key / reproduces
  physics from a cube." — not true, and this spec will not claim it. The measurements say
  information is conserved.
