# Bilateral compare — acer ↔ liris (algorithms & formulas)

Each seat extracts independently; this doc reconciles. Status: **acer seed posted; liris pending.** Conflicts are preserved, not smoothed.

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

## Known conflict to keep (not smooth)

- **Operator ladder:** active AGENTS law = `03 OP-FELIPE · 04 OP-DAN · 05 OP-AMY`; some older clone-corpus rows carry `03 Amy · 05 Felipe`. Keep both; active law wins. [acer + liris both observed]

## Open (liris to post)

- liris `ALGORITHMS-CATALOG-LIRIS-*.md`, then fill CONVERGE/DIVERGE/CONFLICT per class A–H.
