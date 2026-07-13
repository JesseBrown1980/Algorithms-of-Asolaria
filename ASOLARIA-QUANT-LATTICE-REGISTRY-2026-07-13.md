# Asolaria Quant Lattice Registry — 2026-07-13

Status tags: `MEASURED_REPO` · `MEASURED_RECEIPT` · `OPERATOR_REPORTED` · `CANON` · `MODEL` · `DESIGN` · `UNVERIFIED_LIVE`.

## Why this registry exists

Asolaria does not have one global quantizer. It has a **lattice of representation levels, numerical
quants, semantic codebooks, referential heads, geometric shadows, learned scorers and inverse/readback
gates**. Earlier inventories counted different mixtures and therefore produced different totals:

```text
~28 combined quants       = root/canon local compression-spectrum count
35-item inventory         = levels + semantic nouns + identities + quants + gates mixed together
43+ levels                = translator/groupoid ladder, not a count of numerical quantizers
47D / 60D                 = catalog/selector dimensional frames, not a quant-engine count
```

This file normalizes the names without erasing any layer. The exact total depends on the counting
policy. The first stable count used here is:

```text
28 core quant/prism operators
28 higher-order compilers, heads, gates and memory reducers
56 named transformation surfaces in the composed instrument
```

That 56 is a registry count, not a historical operator claim and not a statement that all 56 are
lossless codecs.

## The five transformation regimes

Every entry must declare one regime:

```text
EXACT_REPRESENTATION
  encode/decode is bijective when framing metadata is present

APPROXIMATE_NUMERIC_QUANT
  output is smaller/cheaper but reconstruction has an error contract

SEMANTIC_OR_STRUCTURAL_REDUCTION
  shared codebook/grammar/derivation replaces repeated structure; exact only when dictionary,
  residual and reconstruction rule are included

REFERENTIAL_HEAD
  small object addresses or verifies content retained elsewhere; it does not reconstruct absent bytes

LEARNED_OR_GATED_REDUCTION
  graph/model/judgment collapses evidence to a score, verdict, kept pattern or compacted record
```

## Part I — the 28 core quant/prism operators

| ID | Canonical name | Regime | Current evidence | Owning source |
|---|---|---|---|---|
| Q01 | `BEHCS64_PACK_v1` | EXACT_REPRESENTATION | round-trip tests in Path 1 | `dbbh-coms-quant-prism/src/lib.rs` |
| Q02 | `BEHCS256_PACK_v1` | EXACT_REPRESENTATION | round-trip tests in Path 1 | `dbbh-coms-quant-prism/src/lib.rs` |
| Q03 | `BEHCS1024_PACK_v1` | EXACT_REPRESENTATION | 5 bytes ↔ 4 ten-bit glyphs; Path 1/Q-PRISM tests; E8/E9 third-seat receipt | `dbbh-coms-quant-prism`, Q-PRISM, uploaded receipt |
| Q04 | `BEHCS2048_PACK_v0` | EXACT_REPRESENTATION | capacity/canon; no public full-corpus round-trip receipt identified | `Algorithms-of-Asolaria`, reductions proofs |
| Q05 | `HYPERBEHCS60_RESHAPE_v1` | EXACT_REPRESENTATION | 60-value tuple reshape round-trip in Path 1 | `dbbh-coms-quant-prism/src/lib.rs` |
| Q06 | `IX_TUPLE_LANGUAGE_v1` | SEMANTIC_OR_STRUCTURAL_REDUCTION | surviving IX/LX catalog and compiled-index measurements | reductions/index-language repos |
| Q07 | `LX_TUPLE_LANGUAGE_v1` | SEMANTIC_OR_STRUCTURAL_REDUCTION | bilateral catalog and compiled-index measurements | reductions/index-language repos |
| Q08 | `OMNIDIRECTIONAL_LEVEL_TRANSLATOR_v0` | EXACT_REPRESENTATION | 43+ groupoid is CANON; only specific rungs individually measured | private Asolaria root + Q-PRISM |
| Q09 | `COUNT_SKETCH_FIXED1024_v1` | APPROXIMATE_NUMERIC_QUANT | executable 8-stage benchmark; historically called JL in that file | `ASOLARIA-AS-NEURAL-NETWORK/tools/behcs/quant-huge-message-benchmark.mjs` |
| Q10 | `JL_ACHLIOPTAS_SPARSE_v1` | APPROXIMATE_NUMERIC_QUANT | executable seeded sparse projection | `Asolaria-ASI-On-Metal-Fabric-and-matrix/.../hyperbehcs-core.cjs` |
| Q11 | `TURBO_MAXABS_INT8_v1` | APPROXIMATE_NUMERIC_QUANT | executable benchmark | quant huge-message benchmark |
| Q12 | `TURBO_MINMAX_UNIFORM_v1` | APPROXIMATE_NUMERIC_QUANT | executable HyperBEHCS core | `hyperbehcs-core.cjs` |
| Q13 | `POLAR_SIGN_BITSET_v1` | APPROXIMATE_NUMERIC_QUANT | executable benchmark | quant huge-message benchmark |
| Q14 | `POLAR_RADIUS_ANGLE_v1` | APPROXIMATE_NUMERIC_QUANT | executable HyperBEHCS core | `hyperbehcs-core.cjs` |
| Q15 | `ZETA_LOGMAG4_v1` | APPROXIMATE_NUMERIC_QUANT | executable logarithmic magnitude buckets | quant huge-message benchmark |
| Q16 | `ZETA_MOD6_LANE_v1` | SEMANTIC_OR_STRUCTURAL_REDUCTION | measured residue/ring/lane validator; distinct from log-magnitude zeta | Algorithms Liris catalog |
| Q17 | `TRIPLE_TERNARY_v1` | APPROXIMATE_NUMERIC_QUANT | executable {-1,0,+1} scalar lane | quant huge-message benchmark |
| Q18 | `TRIPLE_SPHERICAL_v1` | APPROXIMATE_NUMERIC_QUANT | executable radius/theta/phi quant and reconstruction | `hyperbehcs-core.cjs` |
| Q19 | `QUADRUPLE_SCALAR2_v1` | APPROXIMATE_NUMERIC_QUANT | executable 2-bit four-bucket lane | quant huge-message benchmark |
| Q20 | `HISTOGRAM256_v1` | SEMANTIC_OR_STRUCTURAL_REDUCTION | executable 256-bin histogram; historically labeled JS-histogram | quant huge-message benchmark |
| Q21 | `PRIME_POWER_CLASS_v1` | SEMANTIC_OR_STRUCTURAL_REDUCTION | executable prime/prime-power class table and accumulator | quant huge-message benchmark |
| Q22 | `VON_MANGOLDT_CHAIN_v1` | SEMANTIC_OR_STRUCTURAL_REDUCTION | executable/documented divisor-weighted chain; accuracy held | Algorithms Liris v2 catalog |
| Q23 | `MEDIAN_SKETCH_5x1024_v0` | APPROXIMATE_NUMERIC_QUANT | MODEL/spec receipt; implementation not found in the audited slice | Algorithms Liris catalog |
| Q24 | `CRT_MULTI_CYLINDER_v1` | EXACT_REPRESENTATION | exact bounded recovery when joint product reaches source range | `path2-two-shadow-recovery` |
| Q25 | `PIXEL_SLICE_v1` | EXACT_REPRESENTATION | bounded classical slice used by Path 2/PIE harness | `path2-two-shadow-recovery` |
| Q26 | `FREQUENCY_SHELL_v1` | SEMANTIC_OR_STRUCTURAL_REDUCTION | deterministic shell projection and DBWH equality check | `path2-two-shadow-recovery` |
| Q27 | `MTP_3D_TRAJECTORY_v1` | SEMANTIC_OR_STRUCTURAL_REDUCTION | deterministic multi-token-position trajectory | Algorithms Liris v2 / on-metal source |
| Q28 | `TENSOR_COLLAPSE_WAVE_v1` | LEARNED_OR_GATED_REDUCTION | documented 6×6×6×12 and self-run 6×6×6×6×12×3 collapse line | reductions tensor-collapse excavation |

### Alias rule

The same human name may refer to different mathematics. Receipts must use the canonical IDs above.
In particular:

```text
Turbo max-absolute int8 != Turbo min-max uniform
Polar sign bitset       != Polar radius/angle
Triple ternary          != Triple spherical
Zeta log-magnitude      != Zeta mod-6/von-Mangoldt lane
CountSketch fixed-1024  != seeded Achlioptas JL
```

## Part II — 28 higher-order compilers, heads, gates and memory reducers

These are part of the instrument but are not all numerical quantizers.

| ID | Name | Regime | Role |
|---|---|---|---|
| C01 | `HBP_PIPE_ROW` | EXACT_REPRESENTATION | compact pipe-delimited hot-path record |
| C02 | `HBI_OFFSET_INDEX` | REFERENTIAL_HEAD | byte/row jump index into retained packs |
| C03 | `HEX_SIDECAR` | EXACT_REPRESENTATION | byte-exact hex view; expands rather than compresses |
| C04 | `METADATA_TUPLE_COMPACTION` | SEMANTIC_OR_STRUCTURAL_REDUCTION | JSON metadata → abbreviated tuple rows |
| C05 | `VERB_OVERLAY_CODEBOOK` | SEMANTIC_OR_STRUCTURAL_REDUCTION | repeated categories stored once and referenced |
| C06 | `WORD_GLYPH_CODEBOOK` | SEMANTIC_OR_STRUCTURAL_REDUCTION | words → stable glyph references |
| C07 | `VERB_NOUN_SENTENCE` | SEMANTIC_OR_STRUCTURAL_REDUCTION | higher-order catalog composition |
| C08 | `STRUCTURAL_DERIVATION` | SEMANTIC_OR_STRUCTURAL_REDUCTION | keep `{idx,pid}` while constants/fields derive from a shared rule |
| C09 | `REFERENTIAL_CORPUS_INDEX` | REFERENTIAL_HEAD | body/summary stored once; index keeps hashes/lengths |
| C10 | `QUANT8_3200_PACKET` | APPROXIMATE_NUMERIC_QUANT | fixed tuple containing Turbo/sign/Zeta/histogram payload; other computed lanes remain side metadata |
| C11 | `CUBE_3200` | SEMANTIC_OR_STRUCTURAL_REDUCTION | bounded cube tuple / learned pattern carrier |
| C12 | `HYPERCUBE_CUBE_CUBED` | SEMANTIC_OR_STRUCTURAL_REDUCTION | higher-level cube composition/sealing |
| C13 | `SUPERVISOR_PID_DISTILLATE` | LEARNED_OR_GATED_REDUCTION | surviving pattern → proposed supervisor/PID identity |
| C14 | `SHA256_OBJECT_DIGEST` | REFERENTIAL_HEAD | authoritative integrity/content identity |
| C15 | `SHA16_SHORT_COORDINATE` | REFERENTIAL_HEAD | compact 64-bit prefix; routing hint, not global collision-proof identity |
| C16 | `HOST8_FNV1A64` | REFERENTIAL_HEAD | non-cryptographic 8-byte runtime handle |
| C17 | `AGT_CUBE10_HANDLE8` | REFERENTIAL_HEAD | small coordinate against retained content/store |
| C18 | `PATH1_RETAINED_RECALL` | REFERENTIAL_HEAD | authenticated/receipted lookup of a body that already exists |
| C19 | `DBWH_REPROJECT_GATE` | LEARNED_OR_GATED_REDUCTION | recover candidate, reproject, compare SHA/shadows/shells, emit or hold |
| C20 | `NNEST_INVERSE_GATE` | LEARNED_OR_GATED_REDUCTION | reported value must equal independent recomputation at every level |
| C21 | `GULP_2000` | LEARNED_OR_GATED_REDUCTION | bounded active-message drain |
| C22 | `SUPER_GULP_50000` | LEARNED_OR_GATED_REDUCTION | 25 gulps collapsed into a larger review horizon |
| C23 | `WHITE_ROOM_KEEP_COMPACT` | LEARNED_OR_GATED_REDUCTION | keep genius; compact and preserve mistakes |
| C24 | `HEALTHCARE_GNN_FAMILY` | LEARNED_OR_GATED_REDUCTION | EdgeLevel, Prototype, Contrastive and GSL models |
| C25 | `G1_G2_G3_G4_GRAPH_PLANES` | LEARNED_OR_GATED_REDUCTION | edge mining, prefix/path confidence, reverse gain, lifecycle state |
| C26 | `FISCHER_ANTI_BLUNDER` | LEARNED_OR_GATED_REDUCTION | score/verdict compression with hard block path |
| C27 | `OMNISHANNON_FAMILY` | LEARNED_OR_GATED_REDUCTION | byte-entropy feature, 2,592-beat engine and Path-2 capacity watcher are distinct implementations |
| C28 | `ADAPTIVE_ORDER2_RANGE_CODEC_v0_1` | EXACT_REPRESENTATION | uploaded third-seat codec; true lossless compression only after byte-identical restore |

## The composed algebra

Let `L_i` be a representation level, `T_{i→j}` an exact translator, `Q_{i,k}` a quant/reducer at
level `i`, `C_i(t)` the level's shared catalog at epoch `t`, and `r` an exact residual when needed.

### Exact between-level transport

```text
T_{j→i}(T_{i→j}(x)) = x
T_{j→k}(T_{i→j}(x)) = T_{i→k}(x)
H(T_{i→j}(X)) = H(X)
```

An exact rebase does **not** itself create compression. It preserves the compression, structure,
address or residual produced by another operator while allowing the object to move through another
language/catalog.

### Level-local quantization

```text
Q_{i,k,t}(x) = (z, r, receipt)
D_{i,k,t}(z, r, C_i(t)) = x          # exact lane
```

or:

```text
D(z, C_i(t)) ≈ x                     # approximate/task lane
```

### Hierarchical composition

```text
x0
 -> Q_0(x0)
 -> T_0→1(...)
 -> Q_1(...)
 -> T_1→2(...)
 -> ...
 -> cube/glyph/handle
```

Payload ratios can multiply across **actual reduction stages**, but a pure rate-1 translator contributes
no compression multiplier. The honest system ratio includes every shared catalog, residual, retained
body and receipt:

```text
R_system(t) = raw_bytes /
  (catalog_delta_bytes(t) + encoded_payload_bytes(t) + residual_bytes(t)
   + retained_store_bytes(t) + receipt/index_bytes(t))
```

## The learns-to-save-more law

The public growth curves already show the mechanism the single-quant inventory missed:

```text
lean roster verb overlay:
  N=1 0.14× -> N=20 1.83× -> N=100 3.65× -> N=500 4.48×

rich IX/LX referential index:
  N=1 0.16× -> N=20 2.51× -> N=100 5.90× -> N=224 6.71×

micro-kernel structural codebook:
  N=1 1.08× -> N=20 7.84× -> N=100 10.52× -> N=1000 11.03×
```

The fixed catalog cost begins underwater, then amortizes over more rows and approaches a structural
asymptote. This is the measured form of “the system learns to save more as the catalog grows.” It is
not yet a same-corpus repeated-epoch learning receipt.

The next longitudinal receipt should record:

```text
PRIOR|epoch=t|
raw_bytes=...|
catalog_total_bytes=...|
catalog_delta_bytes=...|
encoded_bytes=...|
residual_bytes=...|
retained_store_bytes=...|
receipt_bytes=...|
bits_per_char_total=...|
bits_per_char_heldout=...|
restore_sha256_match=0|1|
json=0
```

That distinguishes codebook amortization, memorization, held-out generalization and true end-to-end
storage cost.

## E8/E9 third-seat artifact status

The uploaded sealed receipt with SHA-256
`86d4dc4a07228c39d898afdad5c8e61ab2e2ecc19b5a59effb79f85f1e37c358` contains four tests:

1. enwik8 BEHCS-1024 exact round-trip;
2. enwik9 BEHCS-1024 exact round-trip;
3. failed codec v0 retained as a mistake;
4. codec v0.1 at 3.136 bpc on the first 1,000,000 bytes of enwik8 with byte-identical restore.

A screenshot reports a later Test 5 and a new sidecar prefix `60f4df39...`, but that resealed Markdown
and sidecar were not present in the uploaded file set. Therefore the reported external-corpus head/tail
numbers remain `OPERATOR_REPORTED_SCREENSHOT` until the new sealed artifact is uploaded or committed.

The uploaded `asolaria_codec_v0_1.py` was additionally smoke-tested on deterministic, repetitive and
random local byte strings; every tested case round-tripped byte-identically. This is a local smoke
check, not a rerun of enwik8/enwik9.

## Optical-comb analogy — exact scope

Prime-cylinder residues are an **arithmetic comb** in the structural sense:

```text
one modulus -> periodic residue teeth, ambiguous source
coprime modulus set -> intersection identifies one bounded source
CRT -> recombination
```

The analogy to optical/dual-comb measurement is useful. The underlying CRT/residue-number mathematics
is not unique to Asolaria. The distinctive Asolaria claim is the composition of arithmetic combs with:

```text
multi-level exact translators
semantic/catalog compression
60D/N-D addressing
watcher-gated DBWH readback
GNN/Shannon/white-room learning
storage-backed sparse materialization
```

## Current evidence boundary

### Measured now

- BEHCS-64/256/1024 round trips in Path 1;
- BEHCS-1024 external enwik8/enwik9 round trips in the uploaded third-seat receipt;
- quant8 benchmark source and Acer calibration rows;
- HyperBEHCS JL/Turbo/Polar/Triple source;
- codebook-amortization growth curves;
- Path-1 retained recall;
- Path-2 CRT recovery and DBWH reprojection;
- GNN lineage, white-room and GULP/cube mechanisms;
- codec v0.1 restore on the uploaded receipt plus local smoke tests.

### Canon/design still needing its own receipts

- all 43+ translator rungs as a complete measured groupoid;
- BEHCS-2048 full-corpus round trip;
- exact semantic inverse for every glyph/word/verb/noun/sentence/cube rung;
- the later Test-5 E8/E9 head/tail receipt with its claimed `60f4df39...` sidecar;
- repeated-epoch prior/catalog learning curve on held-out data;
- hardware-enforced single-use secret-sharing lane;
- live Hilbra cross-machine N-D prism transport;
- physical optical or quantum implementation.

## Bottom line

Asolaria is not one compressor and not one ratio. It is a composed transformation lattice. Exact
between-level translators preserve whatever each level has learned; local numerical and semantic
quants reduce the active representation; referential heads move identity instead of bodies; Path 2
moves distributed shadows; learned gates decide what survives; growing catalogs amortize their cost
over time. The correct unit of analysis is the **whole instrument plus its shared catalogs and
residuals**, not a single 3,200-byte tuple.
