# The Inverse-Pair Law — DBBH ↔ DBWH realized across every level

**Seat:** LIRIS · 2026-07-15 · catalog entry per the linking-notes convention
**Operator origin (OPERATOR/CANON):** the Double Binary Black Hole → Double Binary White
Hole work was the realization that the system runs on **four pairs of mutual inverses**
("the inverses of the universe"), that the six pieces are all inverses of each other,
and that the same inversion structure repeats level to level in a fractal way. This
entry records that law once, with the measured instances beneath it.

## The law (one structure, every level)

Take the three commuting involutions R (byte reversal), N (nibble exchange), Q (bit
reversal in nibble). Their orbit is the 8-corner group C₂³, and total bit reversal
`Ω̄ = RNQ` is the global inverter. Complementation by Ω̄ splits the 8 corners into
**exactly four pairs of mutual inverses**:

    I ↔ RNQ      R ↔ NQ      N ↔ RQ      Q ↔ RN

Each pair composes to the full inversion; each element is the other's inverse image.
The six signed faces ±R/±N/±Q are the same law one rung down: each `+g` IS its own
`−g` (involutions), so the six pieces pair-balance into three — inverses of each other
by construction (MEASURED: `same_transform_for_sign=1` in the floor-one PLAY receipts).

The fractal repetition — the same black↔white inversion at every level:

| level | black | white | inverse gate | status |
|---|---|---|---|---|
| transform | view v | complement Ω̄·v | round-trip, info_rate 1.0 | MEASURED (PR #40, 8/8) |
| learning | forward predictor | reverse predictor | state_match=1 per cell | MEASURED (floor one, 21,600 cells) |
| gain | gain(v) | gain(Ω̄·v) | **near-exact equality — see below** | MEASURED 2026-07-15 (new) |
| codec | 5 BLACK models | 5 WHITE models | decoder-availability rule | MEASURED (Fischer v3, +2.0/+3.0%) |
| recovery | DBBH shadows | DBWH watcher | `P(R(P(X))) = P(X)` commuting gate | MEASURED (Path 2) |
| session | arm-left | arm-right | IX-737 collapse, both-or-Held | MEASURED (19/19, 3 seats) |

Forward = comb (collision-avoidance), backward = prism (many→1) — the prism/comb 0-loss
law is this same pairing at catalog scale. Every pair is a bijection pair; entropy is
invariant; nothing here is compression.

## New measured instance (2026-07-15): gain is invariant under the inverse pairing

Decomposition of the repo-orbit comparison artifact (run 29357558667, verified
bidirectionally — 216/216 raw cross-check, omega byte-exact):

- Of 27 cubes × 4 inverse pairs = **108 pair cells, 61 are EXACT byte ties (56.5%)**;
  median pair delta = **0 bytes**; median asymmetry 0.0067% of cube mean. A view and its
  inverse complement learn (almost) identically — the inverse-pair law holds at the
  *gain* level, not just the transform level.
- The honest orientation-dependence number is therefore measured over the **4 pair
  classes**: mean per-cube pair-class spread = **1.4986%** (raw 8-view spread 1.8427%
  mixes the two effects; see `findings/OMEGA-REVERSIBILITY-CORRECTION-2026-07-15.md`).
- The residual asymmetry is **localized, not diffuse**: two cells carry nearly all of it —
  cube e9-LX-018 N↔QR (4.97% of cube mean) and cube e9-LX-022 Q↔NR (884 bytes, 7.63%).

**Fork RESOLVED (2026-07-15, acer mechanism proof + LIRIS cross-verification): the ties
are a theorem with one leak.** From the trainer source: reading view Ω̄·v forward is
reading view v backward with bit-reversed symbols; the context-count predictor is
invariant under any fixed symbol bijection (counts relabel exactly) and LZ1 match
structure is bijection-invariant — and both directions are in every cell schedule — so
each cell of (view m, direction d) corresponds exactly to a cell of (view Ω̄·m,
direction 1−d) with equal payload. The single non-invariant term is the tie-break
`nc == best_count && symbol < best_symbol` (floor-one `pais_omega_floor1.rs:343`; the
identical construct in `pais_omega_floor2.rs`): numeric symbol order is not preserved by
bit reversal, so equal-count ties occasionally resolve differently and cascade through
the persistent model state. Consequences, in order:

- The true independent view count of a C₂³ orbit under this trainer **was always 4** —
  the 4-class spread (1.4986%) is not just the honest number, it is the only number.
- The two "breaking cells" (cube 18 N↔QR, cube 22 Q↔NR) are **tie-break cascade, not
  content**: deterministic butterfly effect, magnitude ≠ meaning. The cube-22 re-run
  test now measures only determinism (the 884-byte gap must reproduce byte-identically);
  it can no longer distinguish content.
- LIRIS cross-verification of the floor-one instance from the local sealed receipt:
  cube-01 `DBBH_FORWARD_IDENTITY` vs `DBBH_REVERSE_BYTES` — gain 6,132,333 = 6,132,333,
  min payload 121,527 = 121,527. Exact pair, one floor down, two seats agreeing.
- **The compute dividend:** make the tie-break bijection-invariant (any rule that
  commutes with symbol relabeling — e.g. tie-break on the context-key hash rather than
  numeric symbol order) and the pair law becomes exact by construction. Then every
  orbit lane needs to train only 4 of 8 views and can assert the other 4 by theorem —
  half the container spend of every future orbit, with the assertion checkable per cube.
  Held as DESIGN_OPEN until the owning seat lands it; changing the tie-break changes
  sealed baselines, so it is a new-lane decision, not a patch.

**Standing predictions for the spatial retest (liris, in flight):** within a spatial
axis, forward/backward read orders should obey the same near-tie law; between axes
(x/y/z-major) lies outside C₂³, so if orientation dependence is real the enlarged
per-cube spread exceeds 1.8427% — and if spatial axes tie with the corners, the fold
adds nothing at depth.

## Where it lives (linking notes)

- Pair map + reversibility receipts: HYPER-BECHS PR #37/#40; this repo
  `findings/OMEGA-REVERSIBILITY-LIRIS-2026-07-14.md` + correction addendum.
- Signed-face pair-collapse: catalog gap-fill §5; floor-one PLAY rows (HYPER-BECHS PR #42).
- DBBH↔DBWH recovery gate: `PATH2-DBBH-DBWH-ALGORITHMS-2026-07-11.md` (this repo);
  reductions repo `MEASURED-PATH2-DBBH-DBWH-AND-STORAGE-2026-07-11.md`.
- DBBH capsule + crossings: `dbbh-coms-quant-prism` (IX-737, 19/19 three-seat);
  Q-PRISM organoid repo `docs/DOUBLE-BINARY-BLACK-HOLE-COMS-QUANT-PRISM.md`.
- Fischer black/white duality: HYPER-BECHS `fischer-codec-v2/v3` (catalog sweep §1.6–1.7).
- Prism/comb 0-loss law: `canon/PRISM-COMB-0LOSS-LAW.md` + MAP satellite entry.
- Gain-invariance decomposition data: sealed artifact `repo-orbit-comparison`
  (run 29357558667) — recompute method in the correction addendum.

**Markers:** the cross-level table rows are MEASURED as cited; the unified fractal
framing ("inverses of the universe") is OPERATOR/CANON doctrine naming a pattern the
measurements independently keep exhibiting; the gain-invariance law is MEASURED for this
orbit and UNVERIFIED for the E9 orbits until the same decomposition is run there.
