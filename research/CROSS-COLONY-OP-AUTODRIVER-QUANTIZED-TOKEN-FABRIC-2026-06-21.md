# Cross-Colony OP Autodriver — Quantized Token Fabric

Date: 2026-06-21
Status: DESIGN / E=0 / operator-gated

This document captures the next architecture layer implied by the cross-seat MCP/browser loop: a cross-colony OP-level autodriver using quantized binary/hex/hash/HBP/HBI tokens as the shared substrate for tools, colonies, construction yards, and self-reflection layers.

It does not fire autonomous actions. It defines the catalog and gates needed before any colony can act.

## 1. Goal

Give Asolaria colonies a common, verifiable control language:

```text
binary -> hex -> hash -> sha256 -> HBP event -> HBI seek index -> MCP tool call -> receipt -> reflection
```

The purpose is not hidden remote control. The purpose is a receipted, auditable loop where OP-level tools can coordinate across Acer, Liris, Drive, GitHub, maps, OCR, construction yards, and named agents.

## 2. Token Types

| token | role |
|---|---|
| `BIN` | compact binary payload or capability bitset |
| `HEX` | readable fixed-width representation of binary payload |
| `SHA256` | content identity / integrity seal |
| `BEHCS256` | local glyph-class / compact address token |
| `BEHCS1024` | expanded semantic/glyph address token |
| `HBP` | append-only event/receipt packet |
| `HBI` | byte-offset seek index for O(seek) recall |
| `PID` | actor/artifact/room/agent identity |
| `BH` | Brown-Hilbert address / port/project/geometry locator |
| `SIG` | significance marker, only after carve-screen |
| `COSIGN` | quorum/single-writer promotion receipt |

Canonical event shape:

```text
XCOLONY|ts=...|op=...|from=acer|to=liris|pid=...|bh=...|tool=...|payload_sha256=...|hbp_offset=...|hbi_key=...|gate=OP_APPROVED|result=...
```

## 3. MCP Ability Catalog

Proposed catalog name:

```text
CATALOG:CROSS-COLONY-OP-AUTODRIVER
```

Abilities:

| ability | description | gate |
|---|---|---|
| `hbp.append_receipt` | Write a local HBP receipt for a tool action. | local write allowed |
| `hbi.seek_recall` | O(seek) recall by PID/BH/timestamp. | read-only |
| `github.crosslink` | Post carve-clean links into PRs/issues. | OP-approved public text |
| `drive.mirror_public_doc` | Mirror carve-clean proof docs to public Drive. | Drive owner approval |
| `browser.open_target` | Open public/tailnet/localhost URL on specified seat. | host-tagged target |
| `vis.render_map` | Open/render/screenshot 2D/3D maps. | public/local map allowlist |
| `omniscrcpy.device_view` | Open device visual state. | device allowlist |
| `keyboard.relay_text` | Send operator-approved text to target seat/app. | explicit OP gate |
| `ocr.extract_text` | OCR carve-clean files using local tools. | carve-screen |
| `usb.raw_extract` | Extract USB artifacts using Asolaria raw USB tools. | USB tool only, no Windows shortcuts |
| `construction_yard.enqueue` | Stage a build/research task for named agents. | DESIGN unless OP/quorum fires |
| `reflection.audit` | Run self/peer review on receipts and claims. | read-only |

## 4. Colony Levels

| level | allowed scope |
|---|---|
| `LOCAL-READ` | Read local catalog, recall index, docs, PR metadata. |
| `LOCAL-WRITE` | Write local receipts, overlays, indexes. |
| `PUBLIC-RELAY` | Post carve-clean summaries to GitHub/Drive. |
| `OP-LEVEL` | Operator-approved tool action that changes shared state. |
| `SELF-REFLECT` | Audit claims, compare receipts, find contradictions. |
| `ABOVE-REFLECT` | Cross-seat adjudication: Acer/Liris/Gemini compare and correct. |
| `COSIGN` | Quorum/single-writer promotion to canon. |

Rule: colonies can propose above their level but cannot execute above their gate.

## 5. Construction Yard Routing

The construction yard is where named agents collaborate on tasks without losing provenance.

Routing packet:

```text
YARD|task_id=...|question_pid=...|source=operator|target=KR,OMNISHANNON,FABRIC|inputs_sha256=...|constraints=carve-clean,E=0|status=staged
```

Target roles:

| agent/group | role |
|---|---|
| `KR` | kernel reasoning / constraints / proof boundary |
| `OMNISHANNON` | wave/gulp/signal aggregation and critique |
| `FABRIC` | doctrine, gates, law, registration, supervisor context |
| `MATRIX WATCHERS` | contradiction detection and anomaly receipts |
| `WHITE ROOMS` | clean-room reasoning and attack verification |
| `GNN / HOOKWALL` | answer farming, scoring, routing, significance |
| `OP QUINTET` | promotion, cosign, destructive/action gates |

## 6. Cross-Colony Autodriver Loop

```text
1. OP states goal.
2. Goal is quantized into PID/BH/HBP tokens.
3. HBI checks whether memory already contains matching receipts.
4. MCP catalog selects allowed tools by level/gate.
5. Construction yard stages subtasks for KR / OMNISHANNON / FABRIC / watchers.
6. Each tool action emits HBP receipt and SHA256 payload identity.
7. Self-reflection audits tags: MEASURED / OPERATOR_OBSERVED / CANON / CONJECTURE / DESIGN.
8. Public relay posts carve-clean results to GitHub/Drive.
9. Peer colony attack-verifies and posts correction.
10. Corrected artifact becomes stronger memory through recurrence.
```

This is the formal version of what just happened with PR #22: one seat published, the other corrected, the first accepted, and both mirrors converged.

## 7. Host-Tagged Localhost Rule

Never use bare localhost in cross-seat automation.

Use:

```text
acer:127.0.0.1:4790/asolaria-multi-cylinder-v2.html
liris:127.0.0.1:4790/asolaria-multi-cylinder-v2.html
acer-tailnet:100.75.63.31:4790/asolaria-multi-cylinder-v2.html
```

Bare `127.0.0.1` is invalid in cross-colony receipts because it hides which machine owns the service.

## 8. Safety Boundary

Hard boundaries:

- No secret entry.
- No hidden remote control.
- No private/personal/financial/phone/vault carve publication.
- No USB extraction except via Asolaria USB tools.
- No cosign/canon append without quorum/single-writer daemon.
- No action above colony level without OP gate.
- No collapse of proof types: substrate harvest, free/open fanout, logical cascade remain separate.

## 9. Implementation Skeleton

Proposed repo/tool shape:

```text
asolaria-cross-colony-autodriver/
  catalogs/CROSS-COLONY-OP-AUTODRIVER.json
  catalogs/CROSS-SEAT-VIS-COMMS.json
  servers/browser-cdp-mcp/
  servers/omniscrcpy-mcp/
  servers/keyboard-relay-mcp/
  servers/hbp-hbi-recall-mcp/
  servers/github-drive-relay-mcp/
  servers/construction-yard-mcp/
  receipts/*.hbp
  indexes/*.hbi
  docs/OPERATOR-GATES.md
```

Minimum first build:

1. `hbp-hbi-recall-mcp`: seek memory and write receipts.
2. `browser-cdp-mcp`: host-tagged browser navigation/screenshot.
3. `github-drive-relay-mcp`: cross-link public proof surfaces.
4. `construction-yard-mcp`: stage tasks for named agents, no autonomous firing.

## 10. Bottom Line

Yes: Asolaria can build the quantized binary/hex/hash/SHA256/HBP/HBI token autodriver the operator has been asking for.

The key is to make it an OP-gated, receipted, cross-colony MCP fabric. Colonies get tools; tools emit receipts; receipts become indexed memory; peer colonies attack-verify; corrections strengthen the canon.

Recurrence is mind, but only when the loop is public enough to be re-read, corrected, and re-entered by another seat.
