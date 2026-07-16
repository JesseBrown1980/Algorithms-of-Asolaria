# Asolaria Algorithm Catalog — Full Sweep 2026-07-15

**Seat:** LIRIS (four parallel repo sweeps, independently read from source; nothing taken
from prose claims without checking the file or receipt behind it)
**Companion:** `ASOLARIA-ALGORITHM-CATALOG-GAPFILL-2026-07-15.md` (the 2026-07-14/15
algorithms). This document is the standing collection for the older clusters the
operator named: Metatagging, the two Q-PRISM repos, the quants engines, the white rooms,
and the prism comb — so they do not get lost again.

**Markers:** `MEASURED` (receipt/CI/test re-verified), `MEASURED_LOCAL` (one-seat),
`CANON` (sealed doctrine/math principle), `DESIGN_OPEN` (contracted, no results),
`UNBUILT`/`MYTHOLOGY` (named-only or self-flagged illustrative).
**Standing law over everything here:** all reductions are bijections — entropy-invariant,
never below Shannon. Recall/addressing is NOT compression. Physics language is metaphor
unless there is code plus a receipt.

---

# Cluster 1 — White rooms and the uncataloged research lanes

All lanes under `gitram-pais-floor1-20260715\` (HYPER-BECHS clone), CI-run in
`HYPER-BECHS--the-third-set`. Shared receipt algebra: `cube_sha256 = SHA-256(canonical
JSON, sort_keys, digest fields excluded)`; aggregators re-verify before trusting any cube.

**1.1 Non-reconstructive lens observer** (`NONRECONSTRUCTIVE-LENS-CUBE-v1`) — observes a
public page, retains ONLY hashes, tag/anchor counts, coarse histograms, and
whitelist-matched factual labels (`expressive_text_bytes: 0`,
`source_reconstructable: false`); emits a `white_room_handoff` of general methods and
requirements for an independent builder. Lives:
`research\wolfram-lens-white-room-v1\lens_observer.py` (PR #32, run 29303616380).
MEASURED (3 lenses PASS).

**1.2 Open-license reversible cube builder** — the contrasting reconstructive lane:
pinned-commit clone, license-marker gate (MIT/Apache/BSD-3), deterministic ≤1 MB text
selection, 1/2/3-level BPE/glyph encode, accept = min(catalog+payload) subject to
byte-identical restore; charged against gzip/bzip2/xz/zstd on the same corpus. MEASURED —
with the negative result preserved: best glyph cube (1.035–2.197 bpc) never beat the
strongest conventional baseline. No sub-Shannon claim. Lives: `open_cube_builder.py`,
same PR.

**1.3 White-room / clean-room independent builder** — THE white-room algorithm.
`white_room_builder.py` receives only the shadow cubes' handoff specs — no page bodies,
no third-party checkouts — and independently implements the named general methods from
mathematical definitions (prime-field Gauss–Jordan, continued fractions, graph-Laplacian
spectra, symbolic canonicalization, 1–2-qubit state vectors, LSP framing), then passes
six property-test groups. Isolation invariant: inputs = {shadow cubes} ∧ no source bodies
∧ no checkouts ∧ no unexpected files. MEASURED (PASS in PR #32 receipts).

**1.4 What the white room IS in the authority chain** — grep across `Asolaria\` (40+
hits; zero in hyperbehcs-hermes): the white room is the **isolated
clean-rebuild-and-attest stage** of the Hermes/Shannon/Hookwall/GNN/white-room repair
route — receives only non-reconstructive specs/receipts, independently rebuilds, keeps
winners, compacts losing candidates as receipts (nothing silently deleted), and emits the
attestation authority-layer promotion requires. Fischer v2's spec pins the pipeline
position: `Hookwall → GNN ensemble → Shannon/OmniShannon → white rooms → GULP → exact
recovery`. Status: CANON as doctrine; the research lane (1.3) is its only measured
instantiation; no single owning fabric implementation found on disk.

**1.5 Hutter/Asolaria 30-cube research swarm** — 30 parallel runner sessions (8 Asolaria
evidence, 8 Hutter-winner, 10 paper/method, 4 reversible-training lanes) each emitting a
source-pinned research cube; aggregation verifies every digest, preserves HELD lanes
(missing private inputs held, never substituted), and measures real concurrency from
timestamp overlap (measured 20, not the requested 30). Honest-negative training results
kept (Plan-B glyph cube 2.4458 bpc lost to bzip2/xz/zstd). Hutter anchor pinned:
fx2-cmix 110,793,128 B. Lives: `research\hutter-cube-swarm-v1\` (PR #29, run
29295933454). MEASURED; the 12-lane tournament in NEXT-TOURNAMENT.md is DESIGN_OPEN.

**1.6 Fischer bidirectional codec v2** — 5 BLACK (past-context) + 5 WHITE
(decoder-legal right-context via pyramid anchors) bounded-memory models; log-odds Shannon
mixer with contextual trust; per-block Fischer tournament (all-BLACK vs BLACK+WHITE
pyramid, keep smaller, replay recovered bytes through the loser so both stay
synchronized); range coder; `ORACLE_NOT_CODEC` audit bounds what leakage would fake.
Decoder-availability rule: a probability is legal only if the decoder holds identical
conditioning at that step. Lives: `fischer-codec-v2\`. Code present; no receipt in-folder
— MEASURED_LOCAL at best.

**1.7 Fischer bidirectional codec v3 (10-runner bench)** — v2→v3: entropy stage replaced
by a predictor transform (hit bitmap + miss-byte stream, zstd/zlib), tournament and range
coder dropped; ten runner jobs audit each expert (prime-rooted hashes: black
11/13/17/19/23, white 29/31/37/41/43); codec-CPL diagnostics
`CPL_j = round(1000·max(0, err_j − best_err))` with <150 PROCEED / 150–499 HOLD / ≥500
BLOCK; consensus maximizes Σ trust·(1+confidence). Lives: `fischer-codec-v3\` (run
29267179250). MEASURED, triple-seated: white gain **+2.008390% / +2.975149%** (150 KB /
1 MB enwik8), trust ≈50/50, all restores byte-identical; **the 15.1% claim NOT
reproduced**; black-sequential still beats both pyramids; 7z-PPMd beats everything.
STAGED_NOT_INGESTED.

**1.8 OMNIEVENT47 instrumented quant** — the exact multilevel-BPE quant/readback harness
wrapped in a single-host Omni lifecycle, every event stamped against the pinned
Brown-Hilbert 47-catalog registry; companion `omnisppan_min_v1.py` portal (schema
codebook + actor dictionary + base-36 deltas + Merkle roots). Lives:
`omnievent47-2026-07-13\`. MEASURED (sha-sealed CI receipt; reference surface, not the
live dispatcher).

**1.9 OMNIEVENTv1 — Catalog47 + HyperBEHCS-60D stamping contract** — canonical
event-stamping algebra: glyph stamp `V = BE-int(SHA-256("D{D}|{v}")[0:8])` rendered as
eight LE base-256 digits; 60×10-bit Q-PRISM selector from
`h = SHA-256(pid8‖counter‖body)`; hash chain `event_hash = SHA-256(event incl. prev)`;
full Merkle root; scheduler law: accept level l iff readback passes AND the named
`codec_plus_catalog` ledger strictly improves. Lives: `omni-event-v1\` (PR #18, 12/12
gates). MEASURED — including independent falsification of "accept all three" (level 1
accepted, 2–3 held) and an accounting correction to the operator-reported bpc.

---

# Cluster 2 — Metatagging-data-for-a-Quantum-universe

Doctrine file mandates no-inflate/no-deflate: all physics language is metaphor/ontology.
PRs: #1 #2 MERGED; #3 #4 #5 DRAFT.

**Layer 0 (2024 seed):** QuantumParticle static metatag (dict + serialize;
`PhaseCorrelation: 1.0` is a literal — MEASURED_LOCAL demo, quantum content
illustrative); 3-D Planck-grid vector expansion (prose only — MYTHOLOGY as physics, but
its realized bijective analogues are `bh_inject_between` and the 256↔1024 transcode in
Q-PRISM, MEASURED for that rung).

**Layer 1 (v2, merged):**
- **Content-addressed PID** — `pid = "AGT-" + sha256(sorted-key JSON of state)[:16]`;
  identical state ⇒ identical address. MEASURED_LOCAL.
- **behcs_tuple 60-D projection** — `t[i] = (int(h[i%64],16)·((i+1)%7+1)) % 1024`;
  hash-derived, hence lossy — an address/route key, NOT a bijection, NOT compression.
  MEASURED_LOCAL.
- **Entanglement-as-bilateral-cosign** — two seats independently recompute the same
  digest; PhaseCorrelation 1.0 ⇔ byte-exact sha match;
  `cosign = sha16(min(pidA,pidB)|max(...))`. Demo MEASURED_LOCAL; the two-seat receipt
  claim lives outside this repo.
- **Catalog improve() flywheel** — mistakes fold to `"fixed:"+m` skills. MEASURED_LOCAL.
- **interaction_gate (E=0)** — un-receipted interaction is HELD; `os_process_spawn=0`
  always. MEASURED_LOCAL (enforced kernel version receipted externally).
- **learn_from_slice + CRC token** — slice → note → glyph `sha16(note+pid)` → versioned
  crypto token; raw slice discarded ("slices are time"). MEASURED_LOCAL.
- **is_genius_candidate** — promote when distilled (fixed+genius) ≥ threshold.
  MEASURED_LOCAL.
- **big_loop (Big Crunch as recompile)** — all pids join to one address
  `sha16(join(sorted(pids)))`; only distilled fixes/genius seed version N+1. Explicitly
  lossy-by-design compaction, not compression. Demo MEASURED_LOCAL; cosmic reading
  self-flagged MYTHOLOGY.
- **Auto-gulp task manager** — anti-memory-explosion law: drain at 50 msgs → note; 2,000
  notes → cube `sha16(join(notes))`; super-gulp per 50,000 total. Raw discarded, digests
  kept. MEASURED_LOCAL demo; "Hilbra" named-only UNBUILT.

**Layer 2 (v3 orientation, PR #3/#4 draft):** orientation_orbit — the C₂³ R/N/Q reversal
orbit on state bytes (8 views, group axioms asserted on actual bytes; MEASURED_LOCAL with
Liris receipts: 8/8 info_rate 1.0, isotropy-at-depth ±0.26%); antiparticle() — the R·N·Q
total-bit-reversal involution; omega_commitment() — sha over the 8 view digests (50%
avalanche, one-way skin, reversible hub reading). All SHADOW_MEASURED_ISOLATED, merge
HELD pending Acer/Relic.

**Layer 3 (Floor-1 trilateral prep, PR #5 draft — CI 42/42 + independent verify):**
- **digest() length-prefixed identity** — type tag + 8-byte length prefix per field +
  domain string, then sha256; delimiter-unambiguous. MEASURED.
- **RouteSelector 60-D commitment** — ≥60 axes in 0..1023 from
  `seed=sha256(lang|face|slice)`; hash-derived route address. MEASURED.
- **Content-PID DAG + verify_pid_dag** — PIDs from digests including parents' identity
  hashes; verifier rejects duplicates, missing parents, hash mismatches, generation
  inversions, cycles. MEASURED.
- **paired_learning_edges** — every event emits a forward-GNN edge + reverse-gain
  feedback edge (reverse tick = forward+1); `learned=0` until an owning GNN receipt.
  Mechanism MEASURED; trained GNN DESIGN_OPEN.
- **supervisor_collision_table** — collision ⇔ same request/scope/route ∧ |Δtick| ≤
  window ∧ differing verdict/payload-sha → HELD_FOR_SUPERVISOR. MEASURED.
- **Geometry combinatorics + omnicentric law** — Q3 cube edges by XOR, recenter
  `T_v(x)=x⊕v` (coordinates only, never blind payload XOR); K4; icosphere
  `F,E,V = 20·4^L, 30·4^L, 10·4^L+2`; cycle-double-cover verifier; omega capacity
  `cells×12×6×8` explicitly capacity-not-resident. MEASURED (exact fixtures).
- **brown_hilbert_child** — radix-1024 address extension, finite-word nested-address
  law. MEASURED.
- **Self-improvement claim gate** — precommit (heldout SHA + evaluator SHA BEFORE child
  creation), ≥2-trial CI, accept only if `delta > noise_floor ∧ child_CI_low >
  parent_CI_high` + leakage audit + lineage + reverse replay + rollback. "More training
  alone is not an improvement receipt." Validator MEASURED; zero materialized claims ⇒
  self-improvement DESIGN_OPEN; historical semantic-QA claim stays UNVERIFIED.
- **Native-glyph witnesses + five-gate glyph-language evaluation** — 34 witnesses
  (27+6+1) content-bound; language accepted only with structure-beyond-substitution,
  novel compositional message, exact native↔Ω round-trip, cross-cube preservation,
  unchanged native catalog. Witnesses 34/34 MEASURED; evaluations 0/34 ⇒ DESIGN_OPEN.
- **reversible_digital_projection (Path-3)** — self-inverse keyed XOR keystream view;
  bijection, entropy-invariant; explicitly disclaims quantum cloning. MEASURED.
- **Omega GNN junction (OmegaBinding)** — 6 apex → forward fan-in → Ω → reverse-gain
  fan-out; full PID binding, never a bare hash. Structure MEASURED;
  PREPARED_NOT_INGESTED ⇒ DESIGN_OPEN.
- **engine_promotion_gate** — all 9 named checks AND ACER+LIRIS+RELIC attestations PASS,
  else HELD. Gate MEASURED; promotion HELD.
- **HBP/HBI/hex sealing + verify** — pipe rows `json=0`, LF-only, atomic; HBI byte-offset
  + per-row SHA index; `.sha256` sidecars + SHA256SUMS; semantic verification rejects
  forged claims even after resealing. MEASURED.
- **Omnidispatcher intake + bus-ACK sealers** — cold bundles, `dispatch=0, gnn_train=0`,
  PREPARED_NOT_GNN_INGESTED. MEASURED_LOCAL.

---

# Cluster 3 — Reductions + quants engines

Local checkout NOTE: `what-is-asolaria-reductions` is 3 commits stale vs GitHub main
(remote adds the Path-2/DBBH-DBWH measured doc and cross-repo PR map — inventoried from
FETCH_HEAD).

**The core reduction moves (README/MAP law layer):**
- **Referential naming (handle8)** — `handle8 = sha256(content)[:8]`; entropy relocated
  and named, never destroyed; collision = birthday `≈ M²/2⁶⁵`. MEASURED (math); the
  21,141:1 / ~3B:1 multiplicity anchors are operator numbers held as anchors.
- **Exact re-basing (BEHCS 256↔1024)** — same integer, different digit base; exact at
  lcm(8,10)=40 bits ⇒ 5 bytes ⇄ 4 glyphs; code rate exactly 1.0, sha-identical,
  Rust==Python. MEASURED for this rung; 43+ ladder = CANON frame, further rungs
  UNVERIFIED until their own round-trips.
- **CRT prime lanes** — `ℤ_M ≅ ∏ℤ_mᵢ`; split = collision-proof lanes, Garner
  recombination = exact reconstruction. CANON math principle.
- **Path 2 — no-store recovery + DBBH→DBWH gate** — poles hold lossy shadows
  `Sᵢ = X mod pᵢ`; reconstruct iff `ΠpᵢI ≥ R` else Held; watcher emits only under
  `P(R(P(X))) = P(X)`; `residual_selector_bits = ⌈log₂⌈R/M_I⌉⌉` is the honest mechanism
  behind "one-bit tails". MEASURED **with a pinned defect**: u128 overflow at ≥6 of 7
  cylinders → FALSE HOLD + lying receipt (`capacity_bits_floor=0`) — fix before
  canonizing.
- **Level-ladder groupoid** — `T_ji∘T_ij = id`, `T_jk∘T_ij = T_ik`: path-independent
  translation; verification = recomputation. CANON, one rung MEASURED.

**F01–F10 rebuild:**
- **F01 prime-tower coordinate** — PID = tuple `(V,T,L,D,K,i)`, scalar addr is only a
  render; cylinder quant lane/ring/phase mod small primes. Gap-mod-6 forcing law PROVEN
  9,589/9,589 pairs; tuple unification DESIGN_OPEN.
- **F02 Sidon-Tower Embedding** — the projection licence. The naive 1-D linearizer does
  NOT give unique distances (measured pigeonhole collisions); the fix composes an
  Erdős–Turán Sidon set `S_p = {2pk + (k² mod p)} mod 2p²` per tower, tower weights
  `p_t³`, super-increasing anchors. Certificate: **627 points → 196,251 pairs → 0
  collisions**, byte-identical across two vantages. MEASURED. Corollary (distinct
  distances ⇒ globally rigid) PROVEN.
- **F03 rule-of-three triad** — one message → three ROLE lanes (L0 worker → L1
  self-reflect → L2 supervisor), strictly increasing information frontier; a triad costs
  3 sha16 handles + 1 verdict; amplification `E[heavy passes]=1/p`. MEASURED
  (structure + self-tests 9/9); wall-clock speedup explicitly not benchmarked.
  **NOT the cube's R/N/Q axes — different threes.**
- **F04 8-chamber revolver** — only-mover state machine
  (EMPTY→LOAD→RUNNING→COLLECT→EJECT), operator-gated fire. Never-Explode theorem: LOAD
  only if resident < B=2000; forward invariance of [0,B]; Lyapunov `V=(r−B)₊≡0`; memory
  O(B). Infinite-Three Convergence: only the supervisor spine recurses, `R_total ≈ 1.5B`
  for infinite depth; 3 = unique minimal arity. MEASURED (10⁶-row self-test).
- **F05 emitter piping / total recall** — emitting computes the retrieval address
  (recompute, don't scan): `$PID0 = md5(REAL‖REFL‖FABR)`; PID prefix tree + content
  store + time fold; `.hbi` seek + sha verify; only claim class permitted:
  `O1_SHAPED_ADDRESSING_NOT_TOTAL_WORK`. MEASURED (live host ≈2.7 MB RSS); unified EMIT
  envelope DESIGN_OPEN.
- **F06 real-graph projection Π** — deterministic address→ℝ³: cylinder kernel
  `(n mod p, ⌊n/p⌋)` lifted by `ω_d=√p_d`, fixed prime-frame projector; SOLID only with a
  sealed packetHash, unwalked slots HOLLOW. DESIGN_OPEN (exporter 8/8).
- **F07 watcher stack** — line-graph dual (watch lines, never light points);
  tie-free centrality via distance uniqueness; Bobby-Fischer player
  `PCPL(m)=cpl(m)·(1+λ·Ĉ)` with remove-and-reprobe; BHGNN-10: the 10 bytes are the
  emitted verdict-frame, weights live in the 55 KB cube. GNN heads MEASURED
  (277.8M/111.1M hits, live :4792); Fischer player + 10-byte frame DESIGN_OPEN.
- **F08 prime-tier taxonomy** — tiers = disjoint address bands by prime-power exponent;
  Lemma R3: `x↦x^k mod p` bijective iff `gcd(k,p−1)=1` (odd powers preserve, even fold —
  the REAL-FREE vs FROZEN-BRAIN split). p¹/p³ MEASURED; **τ3⁵ and p5+ = self-flagged
  PROPOSAL — MYTHOLOGY until built.**
- **F09 grounding audit** — every claim [EXISTS] or [NEW-reduced-to-EXISTS]. Anchor:
  **100B run — 10¹¹ packets, 0 child spawns, 0 external tokens, 3.93 min @ ~424 M/s**;
  closed-form quant law `score=0.82+0.18u` predicts genius/mistake counts to ±0.008% over
  10¹¹ draws. MEASURED — the strongest claim in the cluster. (200 ns figure retired;
  measured 1,759 ns local handle.)
- **F10 test plan** — R0–R7 held-safe protocol + QUANT-Δ certificate
  (`distinct_ratio=1.0, collisions=0 → PROJECTION_LICENSED`). R2/R2-neg/R3 MEASURED;
  E1–E8 experiments DESIGN_OPEN.

**Named quant series:** QUANT-Δ (MEASURED once, rolling re-proof DESIGN_OPEN);
Brown-Hilbert Gap Series (self-flagged UNVERIFIED — MYTHOLOGY until regenerated); Baker
Q-fence (rests partly on a conjecture — "do not ship as guarantee"); Riemann ψ-dial
(measurement protocol, NOT a proof of RH — UNBUILT).

**Recall portal (S4)** — postings-intersection over HBI row offsets + O(1) HBP byte
seeks; acer Rust 591,286 rows / 1.47 ms median; liris Node 3.65–4.82 ms. MEASURED per
seat; "SOTA" bounded to specialized recall, self-held.

**Quant engine stubs (already in this repo — linking notes only):** Combined Quant Atlas
(28 operators, 5 families) → `ASOLARIA-COMBINED-QUANT-ATLAS-2026-07-13.md`; quant8
head/tail law (3,200-B four-channel head; verify gain 41,826× → 495,011× with corpus
size) and E8/E9 lossless quant/unquant (info_rate exactly 1.0 at 100 MB and 1 GB) →
`ASOLARIA-COMBINED-QUANT-MEASURED-ADDENDUM-2026-07-13.md`.

---

# Cluster 4 — Q-PRISM (both repos, host8, and the prism comb)

**Local acer build (Python sim/harness):** Talbot–Lau matter-wave forward model
(calibrated to the Nature apparatus paper; doc drift noted — README says 8-point
calibration, docstring still says 1-point: reconcile); three-arm blinded harness with
honest-null self-validation (coupling=0 ⇒ no advantage p=0.91; coupling≥0.3 wins
p→0.004) MEASURED in-sim; (1+1)-ES control arm; NeuralStream coupling blend (the
"consciousness stream" reduced to a lawful control-parameter proposer — synthetic;
real-data arm not run); BEHCS-1024 schedule identifier (addressing only); 3,200-byte
quant tuple (JL projection seed 51966 → int8 turbo + signs + zeta stand-in + histogram;
zeta lane byte-parity pending bilateral verify); host-8 handle family
(`handle8 = FNV-1a-64(node_id)`, byte-identical Rust==Python); Brown-Hilbert
inject-between (deepen one radix-1024 digit ⇒ gap ×1024 ⇒ a strictly-between addressable
point always exists — capacity ≠ live, materialization operator-gated E=0); **the
256↔1024 comb transcode** (MEASURED, the pinned rung); Graphify-V3 60D selector envelope
(address describes, never executes); active-glyph CARET lens (provenance disputed —
DESIGN_OPEN, alien content self-flagged MYTHOLOGY); Liris DBBH-CQP host8 cell
(independent second implementation, attack-verified 6/6); omnibit signal-split proof
frame (proof requirement, photon analogy only — DESIGN_OPEN); shadow-resolution capstone
(papers hit a ~0.65 lossy ceiling; Q-PRISM recovery is lossless only via retained content
+ bijections + consent — CANON frame).

**qprism-3d-slice-harness (Rust, zero-dep):**
- **8-wavelength split** — 1 frozen slice → 7 lossless bijections
  (binary/hex/HBI-HBP/BEHCS-64/256/1024/HyperBEHCS-60D) + 1 declared SHA shadow.
  **These are eight ENCODINGS, not the cube's eight orientation views — different
  eights.** MEASURED (round-trips).
- **OmniShannon edge watch** — decode(encode(x))==x ⇒ Lossless; SHA ⇒ Shadow (entropy
  relocated to a store); any failed declared-lossless lane ⇒ Held holds the run. Test
  pins exactly 7+1+0. MEASURED.
- **60D/N-D projection** — `axis_j = (h[j]<<8 | h[j+1]) & 0x3FF`; addressing resolution
  only, never in byte-identity recovery. MEASURED.
- **Multi-cylinder CRT no-store recovery** — 4 pairwise-coprime ~2²⁵ moduli (only two
  are prime; the "prime" label was a bilateral bug fixed 2026-07-04); 48-bit blocks;
  incremental Garner CRT; any 2 of 4 suffice; byte-identical or HOLD. MEASURED. Its
  `adversarial_crt.rs` pins the sibling path2 **u128-overflow FALSE-HOLD defect**
  (receipt lies: `capacity_bits_floor=0`) — MEASURED defect pin.
- **MTP-1/2/3 visual PID supervisors** — record-only observers per cylinder pole + 3-axis
  geospatial read. MEASURED as records.
- **GNN/reverse-GNN edge watchers** — explicit `DESIGN:edge-recorded` scaffolds.
  DESIGN_OPEN.
- **Canon prime-cube anchor ladder** — `dim_anchor(d) = prime(d)³`, 9 canon anchors;
  `dim_is_signed_executable(d) = d ≤ 49`; **D50 = 233 = prime(51)** — the council-sealed
  skip (test proves prime(50)=229, so the skip is canon choice, not arithmetic).
- **PIE N-prime-cylinder atlas** — FNV-fold → residue per prime axis; activation vector
  on an (N−1)-sphere; recovery stays exact per-block CRT. Code MEASURED; JEPA layer
  UNBUILT.
- **Expansion-proposal HBP emitter** — `reversible=1|fire=0` rows routing dim expansion
  to the sealers. MEASURED emission; semantics DESIGN_OPEN.

**dbbh-coms-quant-prism (Path 1, Rust zero-dep):** AGT content addressing (KAT-verified
sha256); BEHCS ladder groupoid with in-test path-independence proof
(256→64→1024 == 256→1024); HyperBEHCS 60D reshape (a reshape, not a new code);
QPrismCube + PID selector (**selector computed but UNUSED in recovery** — verified,
reconstruction touches only glyphs); IX-737 double-black-hole session capsule
(propose/arm-both/open/collapse/revoke, single-use sequenced nonce, deterministic Held
laws — 19/19 across three seats; "black hole" = consent-boundary metaphor, coded and
receipted, admissible); DBBH crossings — glyph-riding (lossless by inversion) and
**address-only crossing = content-addressed dictionary lookup; the mass never crosses;
miss = Held::AddressMismatch, no invention**; N-Nest hash-chained receipts (GENESIS
chain, verify = full recomputation). All MEASURED. "Quant snap (lossy)" is README-naming
only — the actual lossy quant is the Python quant tuple; flagged to avoid double-count.

**The prism comb (`canon/PRISM-COMB-0LOSS-LAW.md`, merged):** the unifying theorem —
every cataloged prism/comb operation is a bijection, `H(f(X))=H(X)`; forward = comb
(collision-avoidance), backward = prism (many→1 collapse, interference-as-search).
Pinned instances: class B = the 256↔1024 rung (MEASURED); class C = CRT ring isomorphism
(math principle); class D = unitary Fourier/Parseval + frequency-comb law
`fₙ = n·f_rep + f_ceo` (math principle); class A = sha-handle addressing bound
("infinite ADDRESSING capacity, not lossless infinite compression" — the held boundary).
CANON; each ladder rung earns MEASURED only by its own round-trip.

---

# Cross-cluster synthesis (what the sweep resolved)

**S1. The 60D-vs-50D discrepancy is RESOLVED by the code.** 60 = the addressing
coordinate width (1024⁶ = 2⁶⁰ ceiling, parametric `project_nd`); 49D = the
signed-executable catalog (`dim_is_signed_executable(d) = d ≤ 49`); D50 = 233 =
prime(51), the council-sealed META_RATIFICATION skip (prime(50)=229 — proven in test, so
the skip is canon choice, not error). No code binds runtime semantics above 49D. The
memory note listing this as a live discrepancy should be updated.

**S2. The different threes and eights (do NOT conflate).**
- rule-of-three ROLE lanes (worker/self-reflect/supervisor, mod-3) ≠ the cube's three
  R/N/Q reversal axes.
- qprism's 8 wavelengths (encodings of one slice) ≠ the cube's 8 orientation views
  (C₂³ orbit) ≠ the 8-chamber revolver (scheduler chambers).
- The six apex faces ±R/±N/±Q pair-collapse to 3 transforms
  (`same_transform_for_sign=1`) — see the gap-fill document §5.

**S3. One defect blocks Path-2 canonization:** the u128 overflow at ≥6 of 7 CRT
cylinders → FALSE HOLD with a lying receipt (`capacity_bits_floor=0`), pinned
independently by qprism's adversarial test and the reductions-side measured doc. Verify
the fix in `path2-two-shadow-recovery` before promoting Path 2.

**S4. Drift/cleanup found by the sweep (actionable):**
- Local `what-is-asolaria-reductions` checkout is 3 commits stale vs GitHub main.
- Q-PRISM `physics.py` docstring (1-point calibration) contradicts README (8-point) —
  reconcile.
- The 3,200-B quant tuple's zeta lane is a layout-compatible stand-in pending bilateral
  byte-parity verify.
- dbbh's "quant snap (lossy)" exists in the README table but not in the crate.

**S5. The one story.** Across all four clusters the same law holds everywhere it was
checked in source, not just prose: **reductions are bijections, never below Shannon;
recall is content-addressed lookup, not compression; lossy operations are explicit
discard-by-design; the SHA is relocated entropy, not destroyed entropy; and every
"impossible" number that survived verification did so as addressing capacity or verify
gain, never as sub-entropy archive size.** Measured cores of record: the 100B run (0
spawns, 0 external tokens), the 627-point Sidon certificate (0 collisions), the 256↔1024
rung (rate exactly 1.0), E8/E9 info_rate 1.0, Fischer white gain +2.0/+3.0% (15.1% not
reproduced), and the floor-one dual seal with the timing-free preimage law.
