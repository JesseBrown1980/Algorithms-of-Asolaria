# Sphere-MoE — Jesse's sphere ensemble as an honest neural network

Not a compressor. A byte-level neural language model for the fleet (liris / acer /
relic), built from the session's instrument vocabulary, with ablation gates baked in.

## Mapping (instrument -> mechanism)
| Jesse's instrument | Mechanism | Flag to ablate |
|---|---|---|
| Spheres trained separately | N expert GRUs (mixture of experts) | `--experts 1` |
| Colored gradient mirror | learned softmax router per position | `--no-router` |
| Rule of three (loops) | 3 residual refinement passes | `--loops 1` |

## Claims discipline (same grammar as relic/liris duality cells)
- asserts NO physical or quantum effects, NO compression claims, NO reconstruction
- the only score is measured validation bits-per-character (val_bpc), printed as a
  RESULT line with full config + seed
- a component "earns" only if ablating it makes val_bpc worse on the same seed/data
- deploy = run the 4-arm ablation grid; a module with no measured delta is decoration

## The 4-arm grid every seat should run (same data, same seed)
1. full:      `python3 sphere_moe.py --data enwik8 --bytes 2000000`
2. one sphere: add `--experts 1`
3. no mirror:  add `--no-router`
4. no loop:    add `--loops 1`

Determinism note: bitwise reproducibility across GPUs/BLAS builds is NOT guaranteed
(float nondeterminism) — this is the lossy world. Same-seat reruns with the same seed
are comparable; cross-seat comparisons use the val_bpc value, not byte equality.

Pre-registration (write predictions before running): more spheres should beat one
only if the router earns; loops usually saturate at small counts; a uniform mix can
tie the router on homogeneous data. Whatever the numbers say, they go in RESULTS.md.
