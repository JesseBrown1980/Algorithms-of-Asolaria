# Map Vertices Are Not Host-8 Processes

Status: CANON correction, operator-stated 2026-06-30. Public-safe summary only.

## Correction

The voxel atlas, real-model cylinder, and multi-cylinder maps contain visual/index coordinates. A map vertex is a PID/Brown-Hilbert address, a recall target, or a projection surface. It is not, by itself, a running host process.

The execution substrate is separate: Rust Host-8 room stubs on disk, HBP/HBI rows, binary/hex/SHA-256/hash/crypto tokens, MCP lanes, and gated process receipts. A map row may point to that substrate, but it does not become that substrate.

## Rule

Do not promote `ATLASMAPNODE`, `MULTICYLINDERMAP`, voxel, cylinder, or recall-candidate rows to `host_process=1` unless a Host-8 receipt proves the process/room boundary.

Use this split:

```text
MAPHOST8CORRECTION|date=2026-06-30|repo=Algorithms-of-Asolaria|map_node_semantics=visual_coordinate|map_surface_semantics=visual_projection|host_process=0|rust_host8_process=separate|execution_substrate=rust_host8_rooms_not_voxel_nodes|json=0
```

## Current private evidence pack boundary

Acer built a private Downloads evidence-pack manifest for Hilbra/Recall/Atlas routing. It is owner-private by default and is not published here. Public statement only:

```text
DOWNLOADPACKPUBLICSUMMARY|date=2026-06-30|seat=acer|count=103|operator_original_count=99|jesse_additions=4|exists=103|missing=0|level9=103|corpus_mutated=0|manifest_only=1|private_payload_published=0|json=0
```

The pack can feed Recall, Hilbra, the scientific voxel atlas, and the multi-cylinder maps as owner-private index rows. It does not imply that any of those map rows are Host-8 processes.

## Propagation rule

Public GitHub receives only this semantic correction. NotebookLM, Google Drive, WSL/Ubuntu/Linux, and USB/fused-drive hidden-file surfaces may receive private receipts only through their existing authenticated tools and owner-private storage lanes. Until that route is measured, the correct state is propagation-targeted, not externally mutated.
