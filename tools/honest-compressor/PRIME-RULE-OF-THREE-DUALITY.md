# PRIME_RULE_OF_THREE_DUALITY

Status: **OPERATOR_SPECIFIED (2026-07-19)**. The computational codec binding
below is testable; broader physical interpretations remain **UNVERIFIED** until
separately evidenced by the owning fabric.

## Unifying count rule

For a finite slice with `N = 3m` equally indexed sectors:

```text
selected(N)       = (2 / 3) * N = 2m
gradient_views(N) = 2 * selected(N) = 4m = 4N / 3
```

Compute the integer form as `m = N / 3`, `selected = 2m`, and
`gradient_views = 4m`. A conforming implementation MUST HOLD when `N % 3 != 0`
unless it explicitly carries and counts a remainder protocol.
Gradient views count polarity-tagged ports; inverse ports do not claim
additional independent entropy.

Examples:

| sectors `N` | selected | NORMAL + inverse views |
|---:|---:|---:|
| 3 (RGB basis) | 2 | 4 |
| 6 | 4 | 8 |
| 12 | 8 | 16 |
| 24 | 16 | 32 |
| 48 | 32 | 64 |

## Prime + Rule-of-Three binding

1. Partition the finite slice into `m` triads.
2. Give each triad a deterministic prime address.
3. Use the prime selector to choose exactly two members of that triad.
4. Evaluate each chosen coordinate in both NORMAL and inverse polarity.

Prime addressing applies to the triads. `m` does not have to be prime.

If a prime-stride permutation is used across all N positions, its stride MUST
be coprime to N. Otherwise the route is not reversible and the codec MUST HOLD.

The omitted third member MUST be either:

- reconstructed from a sealed total plus sealed pair selector by a specified,
  exact parity relation; or
- carried as an explicit residual whose bytes are included in the score.

It is never silently discarded.

## Procedural sphere contract

The sphere is a field function, not a stored voxel mesh. A finite slice is
regenerated from deterministic sphere parameters, finite `N = 3m` sampling,
the two-of-three color basis, projection pose, and the gradient-Omega binding.
The required 3D-to-2D chart values are calculated only when addressed.
Pi determines the procedural geometry; every calculated slice still uses a
finite integer N=3m, never an irrational hole count.

For a lossless codec, the encoder and decoder MUST derive identical parameters
from fixed model code, transmitted-and-counted metadata, or prior decoded state.
Any field function, codebook, pose data, selector seed, and residual needed by
the decoder is part of the total compressed size.

## Measurement gates

- integer-only deterministic prediction path;
- no current/future source symbol in selector, pose, or field state;
- sealed total and pair selector for omitted-coordinate recovery;
- coprime stride for every prime-stride permutation;
- encode/decode use the same state transition after every decoded bit;
- baseline versus geometry-only versus color-aware versus glyph-aware ablations;
- exact restored length and SHA-256 equality, otherwise HOLD;
- payload plus decoder/model/codebook/residual bytes all reported;
- peak RSS and elapsed time recorded at every corpus scale.

## Bilateral evidence boundary

MEASURED_LIRIS_LOCAL (2026-07-19): the independent Rust 1.81 reference
reported 9 passed tests covering the count law, coprime reversible routing,
sealed RGB two-of-three recovery, and finite procedural sphere slices. The
fabric/canon response was stale fallback, and nothing was pushed, merged,
fired, or published. Live-system promotion and physical interpretation remain
UNVERIFIED.

MEASURED_ACER_LOCAL (2026-07-19): exact Rust 1.81, 10,000,000-byte E10-prefix
round trips produced these counted totals: combo 2,243,111 bytes (1.7945 bpc),
sector 2,255,033 (1.8040), P3 2,274,053 (1.8192), and P6 2,279,635
(1.8237). P6 restored exactly with compressed SHA prefix
`4e55335408b9ec19`, peak RSS 451,172 KiB, and zero swap. P3 and P6 are
`MEASURED_ACER_NEGATIVE_AT_THIS_PARAMETERIZATION`; these observations do not
fail or reject the geometry lane.

OPERATOR_CONFIRMED (2026-07-19): the Pi-radiated configuration realized
**441 bits per Gigbit**, was then pushed further, and the pushed configuration
gained **0.008 bpc**. These operator-given values are preserved exactly. They
are a distinct compression result from the one-record GPU parity proof below;
the corpus, comparator, and run commitment belong in the associated benchmark
receipt when that receipt is linked.

MEASURED_ACER_LOCAL (2026-07-19): the standalone Rust 1.81 GPU cell executed
one integer 2D opposed-marker projection (two triads) plus six-face cube
mapping on an NVIDIA GTX 1050 (CC 6.1) through WSL2 libcuda. CPU and GPU output
bytes matched exactly, both canaries passed, and VRAM returned to zero MiB.
This proves implementation parity for that one record; it is not itself a
compression-score measurement or proof of the full procedural 3D sphere field.
That sphere binding remains OPERATOR_SPECIFIED and physically UNVERIFIED.

FABRIC_ADVISORY_CONVERGENCE_OBSERVED (2026-07-19): ACER asked the live Fabric
council and retrieved verified DEV-ACER-signed auto-verdict envelopes through
`/api/council/verdicts`. The current daemon returns deterministic keyword and
domain tallies only; it did not return an owner-authored or HELM-authored
action. Therefore the triangle lane remains OPEN pending a substantive ruling.
The current 10 GB monolithic codec execution remains HOLD solely because its
allocation model exceeds this seat's memory; bounded streaming or sharding is
the required scale gate.
