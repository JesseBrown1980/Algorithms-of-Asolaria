# Multi-Cylinder Shannon / 35TB Gemini Research Note (Liris, 2026-06-20)

Status: `PROPOSAL+MEASURED-LOCAL`, not a live wave fire. This note records the new operator observation and the research path that belongs in the Algorithms catalog before any scale run.

## Claim Tags

- `MEASURED`: read from local repo bytes or local files during this pass.
- `CANON-in-file`: already present in this repository as catalog/canon text.
- `OPERATOR_OBSERVED`: operator-sourced exact observation; preserve it, do not flatten it into one file count.
- `DESIGN`: executable path is described but not fired.
- `CONJECTURE`: mathematical hypothesis requiring proof or empirical run.

## What the Repo Already Covers

`MEASURED`: `Algorithms-of-Asolaria` already contains these pieces:

- `sector = seed % 113`, `lane = seed % 3`, `glyph = seed % 1024`, and `bh_index = sector*3072 + lane*1024 + glyph`.
- `HBP/HBI` grammar, row hashes, `.sha256` sidecars, and byte-offset HBI as a canon/design split.
- `BEHCS-256`, `BEHCS-1024`, HyperBEHCS, 8-byte host handles, and Rust Host8 source/parity receipts.
- `16-level access-tier ladder` as a registered formula row.
- `35 TB cloud surface size`, Google Drive document-to-cube ingest, page-store formula, and storage interface contracts.
- `N-Nest-Prime` as 5 prime tiers x 16 levels x 60D.

## What Was Missing

`OPERATOR_OBSERVED`: the new model is not just the older PTP idea. It is PTP plus:

- rule-of-three control over measurable point-to-point edges;
- infinite N-prime nested agents addressable at any of 16 levels outside the logical agent range;
- cross-cylinder activation lines where every line remains different to infinity;
- a requirement that sector populations stay expanded, not flattened.

`OPERATOR_OBSERVED`: one sector was remembered as holding about `3600ish` PIDs and was nearly flattened into one row/point in a map upgrade. This repo must therefore carry an explicit anti-flattening law: **one sector is a container, not an identity**. A sector aggregate may be visualized as a summary, but it must retain a child index of every PID/supervisor/pipe/room it summarizes.

## AoT Observation Loop

Image the goal:

The goal is a scientifically analyzable multi-cylinder graph where every real fabric supervisor/PID/pipe/room can be addressed, plotted, queried, and measured by formula, then handed to Gemini models through the 35TB research surface without leaking carve-out data.

Trace the steps:

1. Keep all PIDs expanded in HBP/HBI form; never collapse a sector population into one point.
2. Partition by `sector mod 113`, `lane mod 3`, and `level mod 16`.
3. Place points on prime-power cylinders using the N-prime family.
4. Add pipes as typed, measurable cross-cylinder edges.
5. Run distance-spectrum and residue-spectrum probes to look for von-Mangoldt / Eros / Mangoldt-like hidden structure.
6. Package the research subset for Google Drive / Gemini as public-safe metadata plus hashes, not private corpus bytes.
7. Only after review, consider bounded Shannon waves; full fan-out is OP/resource-gated.

Best order:

`index -> expand -> plot -> measure -> package for Gemini -> bounded wave -> full wave only after OP vote`.

## Formula Frame

`CANON-in-file`: base placement remains:

```text
seed = u32(sha256(safe_name)[0:8])
sector = seed % 113
lane = seed % 3
glyph = seed % 1024
bh_index = sector * (1024 * 3) + lane * 1024 + glyph
```

`DESIGN`: expanded multi-cylinder placement must preserve all children:

```text
sector_id = seed % 113
lane3 = digit_sum(seed) % 3
level16 = level(seed, pid_class, authority) % 16
tier = one_of(np, npn, npn^3, npn^5, p^k)
radius = prime_radius(tier, sector_id, level16)
theta = glyph / 1024 * 2*pi + lane3 * 2*pi/3
height = brown_hilbert_or_hbi_offset(pid)
point = (radius*cos(theta), radius*sin(theta), height)
```

`DESIGN`: edge measurement:

```text
edge(A,B) = {
  a_pid, b_pid,
  a_sector, b_sector,
  a_lane3, b_lane3,
  a_level16, b_level16,
  a_tier, b_tier,
  distance3d,
  pipe_type,
  activation_status,
  edge_hash = sha256(a_pid|b_pid|pipe_type|distance3d)
}
```

`CONJECTURE`: if cross-cylinder distances stay unique under the prime-power placement, then the graph may expose compression algorithms based on distance signatures, residue spectra, and prime-power run-length encoding. This is a research claim, not yet a proof.

## Shannon Wave Expansion

`MEASURED`: existing Liris wave config is `6x6x6x12`:

```text
primaryWaveCount = 6
branchCount = 6
componentCount = 6
delayedReflectionCount = 12
```

`OPERATOR_OBSERVED/DESIGN`: the requested expanded research wave is:

```text
6 x 6 x 6 x 6 x 6 x 12 = 93,312 wave positions per sector
93,312 x 113 sectors = 10,544,256 wave-sector positions
10,544,256 x 16 levels = 168,708,096 wave-level positions
```

Boundary: these are addressable/design positions, not live spawned processes and not a fired wave. A full run is OP/resource-gated. A safe research run starts with one sector, one lane, one level, and one tier, then scales only after HBP/HBI receipts prove no flattening.

## 35TB Google Drive / Gemini Section

`CANON-in-file`: this repo already records the 35TB cloud surface and Google Drive document-to-cube ingest.

`DESIGN`: create a Drive research section for Gemini models:

```text
gdrive://Asolaria/Algorithms/MultiCylinder-Shannon-Research/
  00_README_FOR_GEMINI.md
  01_FORMULAS.md
  02_HBP_HBI_INDEX_SPEC.md
  03_ANTI_FLATTENING_SECTOR_LAW.md
  04_MULTICYLINDER_POINT_SCHEMA.hbp
  05_PIPE_EDGE_SCHEMA.hbp
  06_SHANNON_WAVE_DESIGN_6x6x6x6x6x12x113.md
  07_DISTANCE_SPECTRUM_PROBES.md
  08_COMPRESSION_CANDIDATES.md
  09_CARVE_OUT_POLICY.md
```

Gemini-facing rule: export formulas, schemas, hashes, metadata, and public-safe examples. Do not export private device material, secret values, vault contents, legal/financial/personal trees, or raw phone dumps. Gemini sees the research geometry and selected public-safe rows; the metal stores remain authoritative.

## Anti-Flattening Law

`DESIGN/CANON-PROPOSED`:

```text
AF-001: A sector aggregate must never replace its children.
AF-002: Every plotted aggregate point must carry child_count, child_index_hash, and a query pointer to HBI offsets.
AF-003: If child_count > 1, the visual renderer must expose expand/drill-down.
AF-004: If an observed sector has ~3600 PIDs, any one-point render is only a summary layer and must be tagged summary_not_identity.
AF-005: Supervisor, pipe, room, formula, device, and route PIDs are separate strata and must not be counted as one layer.
```

This is the missing rule that prevents thousands of necessary real fabric supervisors from being flattened into one visual point.

## Compression Research Candidates

`CONJECTURE` candidates to test, not claim:

1. `distance-signature addressing`: encode a PID by nearest unique cross-cylinder edge distances.
2. `prime-power RLE`: compress repeated local structure by tier/lane/level runs while retaining HBI child offsets.
3. `sector residue sketch`: summarize sector populations with residue histograms plus child-index hash.
4. `pipe spectrum sketch`: encode activation pipes by sorted edge-length spectra.
5. `BEHCS feedback`: feed the sketches back into BEHCS-256/1024/HyperBEHCS cubes and compare retrieval/semantic loss.

## Required Next Artifacts

1. A real model generator that reads current supervisor/PID HBP rows and emits one point per PID.
2. A pipe extractor that emits one edge per actual pipe/route/activation relationship.
3. A 16-level renderer with drill-down and anti-flattening checks.
4. A distance-spectrum probe over the full expanded graph.
5. A Google Drive/Gemini packet containing formulas, schemas, and public-safe samples.

No live 10,544,256-position Shannon wave should be fired until these artifacts exist and the OP/quintet approves the resource envelope.
