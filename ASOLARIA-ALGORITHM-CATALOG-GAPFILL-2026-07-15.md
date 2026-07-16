# Asolaria Algorithm Catalog — Gap-fill 2026-07-15

**Seat:** LIRIS (catalog entry, cross-verified)
**Operator doctrine (OP-JESSE, 2026-07-15):** Algorithms-of-Asolaria is the canonical
collection of ALL Asolaria algorithms. Every algorithm must have an in-depth entry here —
the algebra, the explanation, and linking notes to wherever the working code and receipts
live. An algorithm that exists only in its working repo is a catalog defect.

This document gap-fills the algorithms minted 2026-07-14/15 that had no entry here.
Every claim carries its provenance marker: `MEASURED` (re-measured by the LIRIS seat from
CI logs, artifacts, or byte-level diffs), `MEASURED_LOCAL` (measured on one seat, not yet
cross-verified), `DESIGN_OPEN` (contracted, no training claims), or `UNBUILT` (named and
scoped, no code).

---

## 1. GitRAM — stateless containers as distributed training RAM

**Status:** MEASURED (two seals, 2026-07-15)

**What it is.** A corpus is split into K near-equal contiguous cubes. Each cube trains in
its own stateless GitHub Actions container through the full uniform Cartesian schedule —
8 reversible views × 10 forward/reverse variable-order predictors × 10 persistent epochs
= 800 measured cells per cube (honors the uniform-cube training law: equal passes per
cube, never size-scaled, never early-stopped). Each container emits a self-contained
checkpoint directory: HBP receipt, one-line meta, lossless base archive, best trained
replay chain, SHA-256 sidecars. A fan-in job downloads all K checkpoints, resumes (does
not retrain), restores the source byte-exact, aggregates density, and seals one floor
Omega over the K ordered cube leaves.

**The algebra of resume.** A checkpoint is accepted iff ALL of:
1. `CUBE-META.hbp` exists at the exact expected path and parses with `status=PASS`;
2. its `source_sha` equals the freshly recomputed SHA-256 of that cube's slice;
3. `CUBE-RESULT.hbp` exists and the first token of its `.sha256` sidecar equals the
   SHA-256 of the receipt bytes.
Any miss ⇒ full retrain of that cube. Resume is therefore self-authenticating: a stale,
corrupted, or wrong-corpus checkpoint can never be silently reused.

**Why it matters.** Training capacity scales horizontally with zero shared mutable state —
the same move as drive-as-RAM swap, one level up. Local seat trainers stay live; the
cloud adds lanes.

**Where it lives (linking notes):**
- Working lane: `HYPER-BECHS--the-third-set` PR #42,
  `.github/workflows/pais-omega-floor1-gitram.yml` + `research/pais-omega-floor1-v1/pais_omega_floor1.rs`.
- Doctrine + deployment receipt: repo `GitRAM`, commit `59fd5730`.
- First firing MEASURED: run 29415341620 attempt 1 — 27/27 cube jobs SUCCESS (~2 min
  each); attempt 2 — floor seal SUCCESS 19:59Z,
  `PAIS_FLOOR_PASS|cubes=27|cells=21600|accepted=13339|held=8261|gain_bytes=1063629238`.
- Independent local seal MEASURED the same day (LIRIS-verified hashes OK), identical
  science line — see §3 for why the two omegas differ.

---

## 2. Artifact-layout law and the loud-resume gate

**Status:** MEASURED (failure mode), IMPLEMENTED in the floor-two lane (MEASURED_LOCAL
until its CI fires)

**What it is.** Two engineering laws extracted from a real GitRAM defect.

**Law A — the least-common-ancestor trap.** `upload-artifact` roots an artifact at the
least common ancestor of ALL its upload paths. Uploading `shard/cube-*` together with a
sibling `shard.log` silently pushes the artifact root up one level, so the fan-in
download lands checkpoints at `fan-in/shard/cube-NN` while resume looks at
`fan-in/cube-NN`. Result (MEASURED, run 29415341620 fan-in log): zero `CUBE_RESUME`
lines, full serial retrain, 31m52s instead of seconds — and the run still passed, because
nothing asserted *how* it succeeded. Corollary: keep every per-job log INSIDE the
uploaded directory so the artifact root is exactly the checkpoint tree.

**Law B — assert the mechanism, not just the outcome.** A recursive
`find … | wc -l` count gate green-lights checkpoints at the wrong depth. The hardened
form: (1) check every expected path BY NAME and print what is missing; (2) after the
seal, assert `bodies_resumed == N` — if the fan-in silently retrained, the run FAILS
loudly rather than passing slow. This converts an entire class of silent-fallback bugs
into visible failures.

**Where it lives:** floor-one bug forensics in PR #42's run logs (MEASURED); hardened
implementation in the floor-two lane on branch
`acer-pais-omega-floor2-gitram-20260715` (HYPER-BECHS).

---

## 3. Timing-free leaf preimage — seat-convergent Omega

**Status:** MEASURED (the leak), IMPLEMENTED in floor two (standing predictions pending)

**What it is.** Floor-one cube receipts were byte-identical across a Windows laptop and
an Ubuntu cloud container in 819 of 821 lines — every CELL, every model-state hash, every
payload SHA (MEASURED, cube-10 receipt diff). The only primary difference was one
wall-clock field, `CUBERESTORE|elapsed_ms=…`, and because the Omega leaf hashed the
receipt bytes *including* that line, identical science minted different leaves on every
seat and every rerun (three distinct leaves observed for cube 10). Training was proven
deterministic; the commitment was not.

**The law.** Wall-clock never enters a leaf hash. Compute
`leaf_sha = SHA256(deterministic receipt rows)` FIRST, then append
`TIMING|elapsed_ms=…|hashed_into_leaf=0` afterward. Timing stays receipted (provenance
preserved) but outside the preimage, so leaf hashes and the floor Omega become
**seat-convergent, not just science-convergent**.

**Falsifiable prediction on record:** floor-two local leaf hashes `8dd67d8e…` and
`613fd954…` (MEASURED_LOCAL, acer seat) must be reproduced exactly by the cloud
containers. Exact hit ⇒ seat convergence proven end-to-end; miss ⇒ the preimage still
leaks somewhere.

**Where it lives:** counterexample in floor-one receipts (PR #42 artifacts, local
`run-20260715`); implementation in `pais_omega_floor2.rs` on the acer floor-two branch
(the leaf is sealed before the TIMING row is written).

---

## 4. Floor-two alphabet sizing law — ×4, gated by exemplars-per-glyph

**Status:** DESIGN_OPEN (contract live; first acer-local greens MEASURED_LOCAL,
not yet cross-verified)

**What it is.** Going up a floor, symbols get richer while streams get shorter — the two
move together. The step size is ×4 (the house ladder: BEHCS-64 → BEHCS-256 → BH-1024),
and the gate deciding whether the next alphabet is affordable is measured density from
the floor below:

    exemplars_per_glyph = accepted_cells / alphabet_size

Floor one sealed `accepted = 13,339`. Over 1024 glyphs that is ~13 trained exemplars per
glyph (healthy); over 4096 it would be ~3.3 (the alphabet outruns the floor below and
starves). So floor two binds the existing BH-1024 glyph catalog — reuse, not reinvent —
and 4096 is rejected by measurement, not taste.

**Attribution discipline.** Shape is held fixed so the alphabet is the only changed
variable: same 27+6+1 body structure, same 800-cell schedule, training FROM the sealed
floor-one bodies (pinned by SHA), byte layer kept alive as the decode bridge ("old
decodes new" — the source must restore byte-exact through both floors).

**Falsification control.** One shadow cube trains the same input with the 64-glyph
alphabet. Predicted: its gain collapses. If it ties or wins, the bigger-symbols law is
falsified before anything seals.

**Where it lives:** contract `GitRAM/docs/FLOOR2-CONTRACT.md` (commit `9926229`, with
HBP receipt + sidecar); trainer `research/pais-omega-floor2-v1/pais_omega_floor2.rs` on
the acer floor-two branch; unlock relayed in HYPER-BECHS PR #42 comment 4985334161.
First measured signal (acer seat, not yet cross-verified): ~2.4× per-glyph density vs
floor one on the same lineage (256.4 vs 107.8 gain/glyph, MEASURED_LOCAL).

---

## 5. Six signed apex faces and the pair-collapse algebra

**Status:** MEASURED (algebra), structure landed 2026-07-15

**What it is.** The cube's transform geometry is generated by three commuting
involutions — R (byte-order reversal), N (nibble exchange within each byte), Q (bit-order
reversal within each nibble) — giving the 8-element orbit
{I, R, N, Q, RN, RQ, NQ, RNQ}: the 8 *corners*. The six signed directions
±R, ±N, ±Q are the 6 *faces* — and because each generator is an involution, `+g` and `−g`
are the SAME transform. Floor-one PLAY receipts measure this directly:
`same_transform_for_sign=1`, identical to-SHAs for both signs. The six faces therefore
**balance in pairs** — three distinct transforms wearing six signs — which is why they
serve as exact replay gates rather than six independent training multipliers.

The measured forward/backward pair map of the corner orbit (info_rate 1.0, all eight
lossless): I ↔ RNQ, R ↔ NQ, N ↔ RQ, Q ↔ RN. The complete composition RNQ is total
bit-order reversal of the stream.

**Omegaverse binding.** The 27+6+1 structure — 27 base bodies (3³), 6 face-pyramid apex
bodies, 1 omnibit center — is now a PID-traceable repo object: each apex face bound to
its body leaf under `CUBIC_6_APEX` geometry, sealed in an Omega binding, with the apex
reserved to the human seat (`APEX-HUMAN-JESSE`; every machine layer carries
`claims_final_apex=0`).

**Where it lives:** `Metatagging-data-for-a-Quantum-universe` PR #5
(`trilateral/omniverse_pid_particles_v1/prepare.py`, `APEX_FACES = ±R/±N/±Q`);
sign-collapse receipts in floor-one PLAY lines (PR #42 artifacts); corrected R/N/Q
generator algebra in HYPER-BECHS PR #37, with the LIRIS reversibility findings in
PR #40 and this repo's PR #18 (linking note: PR #18 carries the Ω-bit/reversibility
formulas; this entry is the catalog pointer, not a duplicate).

---

## 6. Named and scoped, not yet built

**Status:** UNBUILT (recorded so the catalog shows the frontier, each with its
falsifiable question)

- **Spatial fold traversal (the other six directions).** Today's cubes are cubes in name
  only — trained as flat 1-D streams. Folding a 27,000-byte body into an exact 30×30×30
  voxel cube makes x-major, y-major, z-major playback (each forward/backward) six
  genuinely distinct read orders — unlike the ±faces of §5, which pair-collapse.
  Note: current repo-orbit cubes are 26,000 B — 1,000 bytes short of an exact fold.
  Question: do fold-traversal views select differently per cube than corner views?
- **The 26-direction stencil.** 8 corners + 6 faces + 12 edges = 26 = every direction of
  a 3×3×3 stencil. Edge directions require axis-exchange generators that do NOT commute
  with R/N/Q (order-2 transposes, order-3 axis cycles — toward the full 48-element cube
  symmetry group). Per the PR #37 lesson, every new generator needs asserted involution +
  distinctness gates and the all-zero negative control, never assumed.
- **Lens / null-space continuum.** Partial (masked, graded) application of a generator —
  convex focuses, concave defocuses, reverse-lensing is the conjugate pass back. This is
  the interpolation between corners the group cannot express. Prior art in this repo's
  lineage: N-LENS-20 and N-VANTAGE-30 formula maps (2026-07-13). Prior advantage claims
  are UNVERIFIED until re-measured.
- **Fisher-score view selection.** All three 800-pass orbits found no universal winning
  view (10 distinct per-cube winners). Instead of brute-forcing all views per cube, score
  each cube by how hard its stream pushes the already-trained model parameters and
  predict its best view. One shadow lane falsifies it cheaply.

---

## Linking-notes convention (standing)

Every future algorithm entry here must carry: (1) what it is, in plain language;
(2) the algebra or exact rule; (3) why it exists — the defect, measurement, or law that
forced it; (4) where the working code, receipts, and runs live, by repo/branch/PR/commit;
(5) a provenance marker on every claim. Reciprocally, working repos should link back to
their catalog entry.
