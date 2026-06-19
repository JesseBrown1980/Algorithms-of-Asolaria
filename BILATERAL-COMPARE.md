# Bilateral compare — acer ↔ liris (algorithms & formulas)

Each seat extracts independently; this doc reconciles. Status: **acer seed posted; liris seed posted.** Conflicts are preserved, not smoothed.

## Convergences already visible (acer catalog ↔ liris 40-lane scour findings)

| Algorithm/formula | acer | liris (from its scour) | status |
|---|---|---|---|
| REALMATHPOS placement | `sector=seed%113 · lane=seed%3 · glyph=seed%1024` | `mod113 × mod3 × mod1024` (room/sector allocator) | **CONVERGE** |
| Whiteroom room density | (room substrate) | `1,000,000 rooms per prime sector` | acer to confirm |
| Quant / zeta lanes | HEAD/TAIL O(1), 3200-B tuple, zeta=informational-never-gating | zeta/quant byte-measured, descriptor/draft-gated where repo says | **CONVERGE** |
| HBP/HBI integrity | `\|json=0` rows, FOOT content_sha256, .sha256 sidecar, HBIv1 index | pipe rows, json=0, sidecars, footer hashing, row-chain variants | **CONVERGE** |
| Rust PID minter / 8-byte host | sha256-first-8 of anchor PID; room pid = host8 | Rust PID minter + room handle + microkernel descriptor (small kernel slice) | **CONVERGE** |
| 100B layer | LCG substrate, regenerable, childProcessSpawns=0 | packet/run + compact-pool math, NOT live runtime | **CONVERGE** |
| FNV-1a64 source formula | basis `0xcbf29ce484222325`, prime `0x100000001b3` (acer-side generation) | liris noted **no FNV1a64 source formula in its map-clones** | **DIVERGE-by-slice** (formula is acer-side; liris clones lack it) |
| model-citizen prism source | read locally `D:/bigpickle-rebuild/src/model-citizen-rotator.mjs` | liris: prism source **not in the 8 map-clones** (separate commit) | **DIVERGE-by-slice** (expected; provider source not in map repos) |
| route health | bus health uses dedicated route, wrong-port is boundary not death | `4947 /behcs/health`; `/health` on bus is `ROUTE_BOUNDARY`; health is vantage-relative | **CONVERGE** |
| HBP/HBI receipt grammar | pipe rows, `json=0`, sha footers/sidecars | row-chain formulas measured; local `.hbi` artifacts are manifest rows while byte-offset HBI is design/canon | **CONVERGE with artifact split** |
| golden vectors | catalog seed lists exact expressions | liris locked prime-sector PID, whiteroom row-hash, zeta, token-cube, answer-producer, N-Nest, quant, D22/dashboard baselines | **CONVERGE** |
| device/storage | USB and 35TB are separate gated substrates | liris measured raw sector formulas, Drive page-store formula, no Drive chunker, no live USB/cloud probe | **CONVERGE with live-gate** |

## Known conflict to keep (not smooth)

- **Operator ladder:** active AGENTS law = `03 OP-FELIPE · 04 OP-DAN · 05 OP-AMY`; some older clone-corpus rows carry `03 Amy · 05 Felipe`. Keep both; active law wins. [acer + liris both observed]

## Posted catalogs

- Acer: `acer/ALGORITHMS-CATALOG-ACER-2026-06-19.md`
- Liris: `liris/ALGORITHMS-CATALOG-LIRIS-2026-06-19.md`

## Open

- Liris lanes 26-40 can append a v2 catalog after the remaining scour lanes land.
- Recompute Acer-only FNV-1a64 and model-citizen prism formulas from their source lanes where available.
- Update each map repo to point to this repository as the algorithm/formula comparison home.
