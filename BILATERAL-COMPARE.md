# Bilateral compare — acer ↔ liris (algorithms & formulas)

Each seat extracts independently; this doc reconciles. Status: **acer seed posted; liris seed posted; liris v2 supplement posted.** Conflicts are preserved, not smoothed. Live runtime remains separate from file-byte/catalog convergence.

## Convergences already visible (acer catalog ↔ liris scour findings)

| Algorithm/formula | acer | liris (from its scour) | status |
|---|---|---|---|
| REALMATHPOS placement | `sector=seed%113 · lane=seed%3 · glyph=seed%1024` | `mod113 × mod3 × mod1024` (room/sector allocator) | **CONVERGE** |
| Whiteroom room density | `1,000,000 rooms per prime sector` | `SECTOR_CAPACITY = 1_000_000` | **CONVERGE** |
| Quant / zeta lanes | HEAD/TAIL O(1), 3200-B tuple, zeta=informational-never-gating | zeta/quant byte-measured, descriptor/draft-gated where repo says | **CONVERGE** |
| HBP/HBI integrity | `\|json=0` rows, FOOT content_sha256, .sha256 sidecar, HBIv1 index | pipe rows, json=0, sidecars, footer hashing, row-chain variants | **CONVERGE** |
| Rust PID minter / 8-byte host | sha256-first-8 of anchor PID; room pid = host8 | Rust PID minter + Host8 source + parity receipts | **CONVERGE; serving/swap/retire UNVERIFIED-live** |
| 100B layer | LCG substrate, regenerable, childProcessSpawns=0 | packet/run + compact-pool math, NOT live runtime | **CONVERGE** |
| FNV-1a64 source formula | basis `0xcbf29ce484222325`, prime `0x100000001b3` | liris v2 found cloned Rust source and parity receipt rows | **CONVERGE / MEASURED-in-cloned-Rust-source** |
| model-citizen prism source/descriptors | source read locally `D:/bigpickle-rebuild/src/model-citizen-rotator.mjs`; 16 citizens + 2 seats registered | liris: source absent from clone slice, descriptors present in maps/indexes | **DIVERGE-by-source; CONVERGE-by-descriptor; firing UNVERIFIED-live** |
| route health | bus health uses dedicated route, wrong-port is boundary not death | full state machine: `UP/ROUTE_BOUNDARY/HTTP_DEGRADED/DOWN/TIMEOUT/UNPROBED`; fallback markers degrade evidence | **CONVERGE with fallback boundary** |
| HBP/HBI receipt grammar | pipe rows, `json=0`, sha footers/sidecars | row-chain formulas measured; local `.hbi` artifacts are manifest rows while byte-offset HBI is design/canon | **CONVERGE with artifact split** |
| golden vectors | catalog seed lists exact expressions | liris locked prime-sector PID, whiteroom row-hash, zeta, token-cube, answer-producer, N-Nest, quant, D22/dashboard baselines | **CONVERGE** |
| device/storage | USB and 35TB are separate gated substrates | liris measured raw sector formulas, Drive page-store formula, no Drive chunker, no live USB/cloud probe | **CONVERGE with live-gate** |
| MTP/HRM/zeta/JL/codecs | acer names MTP/HRM/GNN and quant families | liris v2 extracts MTP heads, HRM slow/fast stubs, zeta/von-Mangoldt, JL/Achlioptas, Turbo/polar/triple formulas | **PARTIAL-CONVERGE; trained/live weights UNVERIFIED-live** |
| performance/compression | 100B/quant/BEHCS ratios present | liris v2 splits measured speed, referential compression, address capacity, and operator/canon anchors | **CONVERGE with category boundary** |
| secret/gate/tier findings | secret values are carve-out; gated paths remain gated | liris v2 redacts key/token material, records USB/token gates, and keeps tier-policy conflict | **CONVERGE on carve-out; CONFLICT-kept on 6-vs-7 tiers** |
| formula-PID registration boundary | Acer posted receipt branch `e8268d2`: 242 formulas + 23 PROFs + 6 SoS + 1 chief in `DISTRICT-F-FORMULA-CORPUS`; `E=0`, live roster gated | liris mirrored HBP byte-exact, `sha256=782b39c1...`, CR=0, LF=277; no Liris live fire | **REGISTERED-DESCRIPTOR / CONVERGE; live office-feed+cosign still GATED** |
| multi-cylinder / Shannon / Gemini research | operator observation: PTP must expand into rule-of-three multi-cylinder geometry with all 113 sectors, 16 levels, pipes, and no sector flattening; 6x6x6x6x6x12 waves across 113 sectors are a research design, not a fired run | liris added `MULTICYLINDER-SHANNON-GDRIVE-RESEARCH-2026-06-20` with formulas, anti-flattening law, 35TB/Gemini section, and explicit no-fire boundary | **NEW-RESEARCH / PROPOSAL; OP/resource-gated before any scale wave** |

## Known conflict to keep (not smooth)

- **Operator ladder:** active AGENTS law = `03 OP-FELIPE · 04 OP-DAN · 05 OP-AMY`; some older clone-corpus rows carry `03 Amy · 05 Felipe`. Keep both; active law wins. [acer + liris both observed]

## Posted catalogs

- Acer: `acer/ALGORITHMS-CATALOG-ACER-2026-06-19.md`
- Acer formula-PID receipt: `acer/ALGORITHMS-PID-REGISTRATION-ACER-2026-06-19.hbp`
- Liris: `liris/ALGORITHMS-CATALOG-LIRIS-2026-06-19.md`
- Liris v2: `liris/ALGORITHMS-CATALOG-LIRIS-2026-06-19-V2.md`
- Liris receipt crossverify: `liris/FORMULA-PID-REGISTRATION-CROSSVERIFY-2026-06-19.md`

## Open

- Compare Acer full-scour enrichment and physical-substrate scour #2 when posted.
- Compare any Acer live office-feed/cosign/cube materialization receipt separately from the E=0 descriptor registration.
- Keep model-citizen rotator implementation source open for Liris until the source file is present on this seat or otherwise transferred.
- Normalize line endings/sidecar policy before treating adjacent `.sha256` files as cross-seat byte proof.

## ACER attack-verify of the LIRIS catalog (2026-06-19) — ACCEPT-SPINE / CONVERGE

acer independently recomputed liris's deterministic golden vectors (node, from scratch) — **all MATCH, byte/arithmetic-exact**:
- `primeAt(0..7) = 2,3,5,7,11,13,17,19` ✓
- N-Nest `depth3·b3 = nodes 40 / pids 80 / bytes 640` ✓ ; `depth7·b2 = 255 / 510 / 4080` ✓
- Quant8 tuple `= 1024+128+1024+1024 = 3200` ✓
- Fischer `score(9eb8e1db)=0.916571` ✓ ; `reverseGain(7ec091f5)=0.549493` ✓

**Verdict:** liris catalog golden vectors VERIFIED by acer independent recompute -> CONVERGE. The earlier FNV divergence is superseded by Liris v2: FNV/Host8 source is now MEASURED in cloned Rust source. Model-citizen remains split: descriptor rows converge, rotator source is still absent from Liris clone roots, and firing is UNVERIFIED-live. Operator-ladder conflict kept (active law `03 OP-FELIPE/04 OP-DAN/05 OP-AMY` wins; older clone rows = historical). acer full-scour (`wnzybl0n6`) enrichment appends to `acer/` when it lands.
