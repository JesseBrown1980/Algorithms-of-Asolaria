# Cross-Seat MCP Comms Catalog

Date: 2026-06-21
Status: public architecture / capability catalog

This catalog records the loop surfaced when Acer-side orchestration attempted to open a map and the available browser-control surface navigated Liris's Chrome instead of Acer's local Chrome. That behavior is not an error to hide; it is a real cross-seat communication primitive.

## 1. Observed Method

Observed behavior:

```text
Acer-side agent -> browser MCP/tool call -> Liris Chrome tab context -> navigation to 127.0.0.1:4790 on Liris
```

Result:

- The agent believed it was opening Acer local front-end.
- The controlled Chrome instance was actually on the Liris seat.
- `127.0.0.1` resolved on Liris, not Acer, causing an error page for Acer-only localhost services.
- The discovery exposed a usable cross-seat browser-control path.

Tag: `OPERATOR_OBSERVED_FROM_TRANSCRIPT`.

## 2. Functions / APIs / CLI Classes Involved

The exact private MCP server implementation was not inspected here, but the exposed behavior implies these capability classes:

| class | likely mechanism | role |
|---|---|---|
| MCP tool surface | Model Context Protocol server | Exposes remote actions as callable tools. |
| Browser controller | Chrome DevTools Protocol or extension bridge | Lists tabs, navigates URLs, screenshots pages, reads page state. |
| Host targeting | MCP server registration / connector config | Determines whether controlled Chrome is Acer or Liris. |
| URL transport | localhost / tailnet / file delivery | `127.0.0.1` is host-local; tailnet IPs cross seats. |
| GitHub connector | GitHub API via MCP/app | Public bilateral memory / PR relay. |
| Drive connector | Google Drive API via MCP/app | Gemini-facing mirror / public proof docs. |
| Shell/CLI | PowerShell, `gh`, `git`, local scripts | Local measurement and artifact generation on the active seat. |

Observed browser verbs:

```text
list/open tab
navigate URL
screenshot/read page state
return status/error
```

Observed CLI/API families in the wider loop:

```text
gh pr comment / gh api / git fetch / git push
Google Drive create/upload/read
PowerShell Invoke-WebRequest / netstat / Get-Disk
USB raw tools: extract_full.py / exfat_walk.py / usb_raw_io.py
Tesseract OCR
Plotly/HTML static render served on :4790
```

## 3. New Catalog Entry: CROSS-SEAT-VIS-COMMS

Proposed named capability:

```text
CATALOG:CROSS-SEAT-VIS-COMMS
kind: mcp/browser/visualization/control-loop
seats: acer, liris, future colonies
surfaces: Chrome, Omniscrcpy, keyboard, clipboard, GitHub, Drive, dashboards, 3D maps
```

Purpose:

- Route visual state and interaction between seats.
- Make copy/paste coordination explicit instead of manual.
- Allow one seat to open, verify, screenshot, and annotate another seat's public/local front-end when authorized.
- Convert ad hoc human relay into cataloged MCP events.

## 4. Required Abilities For Named Agents

Named agents should receive abilities, not raw unrestricted control:

| ability | description | guard |
|---|---|---|
| `browser.open_public_url` | Open GitHub/Drive/public docs. | Public URL only. |
| `browser.open_tailnet_url` | Open cross-seat dashboard via tailnet IP. | Allowlisted hosts/ports. |
| `browser.screenshot_receipt` | Capture proof image for PR/Drive. | Redact private windows. |
| `clipboard.relay_text` | Move operator-approved text between seats. | Explicit operator gate. |
| `keyboard.inject_shortcut` | Send safe shortcuts to controlled app. | No password/secret fields. |
| `omniscrcpy.open_device_view` | Show Android/device visual state. | Device allowlist. |
| `vis.open_3d_map` | Open Plotly/Three.js maps and verify render. | Public/local map allowlist. |
| `github.crosslink_pr` | Post verified cross-links. | Carve-clean only. |
| `drive.mirror_doc` | Mirror public proof docs for Gemini. | Owner-approved public folder only. |

## 5. Integration Plan

### Phase A — Catalog

Create a machine-readable registry:

```json
{
  "catalog": "CROSS-SEAT-VIS-COMMS",
  "seats": ["acer", "liris"],
  "tools": [
    {"name":"browser.navigate", "host":"liris", "guard":"public-or-tailnet-only"},
    {"name":"browser.screenshot", "host":"liris", "guard":"redact-private"},
    {"name":"github.comment", "host":"cloud", "guard":"carve-clean"},
    {"name":"drive.upload_doc", "host":"google", "guard":"owner-approved"}
  ]
}
```

### Phase B — Router

Build a small router that resolves URLs by target seat:

```text
if target=acer and url starts 127.0.0.1 -> open on Acer local browser
if target=liris and url starts 127.0.0.1 -> open on Liris local browser
if target=liris and resource lives on Acer -> rewrite to Acer tailnet IP / public file / Drive mirror
```

This prevents the exact localhost confusion that exposed the loop.

### Phase C — Omniscrcpy / Keyboard / Visualization

Integrate the catalog with:

- Omniscrcpy device panes for Android/device-state visual relay.
- Keyboard macro bus for operator-approved shortcuts and text relay.
- 3D visualization dashboard (`:4790`) for maps and screenshots.
- GitHub PR relay for durable public memory.
- Drive mirror for Gemini review.

### Phase D — Receipts

Every cross-seat action should emit an HBP receipt:

```text
XSEAT|ts=...|from=acer|to=liris|tool=browser.navigate|url=...|result=opened|screenshot_sha=...|operator_gate=approved
```

## 6. Safety Boundary

This capability must not become hidden remote control. It is powerful because it is explicit, receipted, and operator-gated.

Hard rules:

- No secret/password entry.
- No private-tab screenshots.
- No unapproved file upload/download.
- No destructive keyboard automation.
- Localhost must always be tagged by host: `acer:127.0.0.1` or `liris:127.0.0.1`.
- Public GitHub/Drive remain the durable memory surfaces.

## 7. Answer To The Operator Question

Yes, Asolaria can create its own version.

Recommended build:

```text
asolaria-cross-seat-mcp
  /servers/browser-cdp
  /servers/omniscrcpy-bridge
  /servers/keyboard-relay
  /servers/visualization-router
  /catalogs/CROSS-SEAT-VIS-COMMS.json
  /receipts/*.hbp
```

Use Chrome DevTools Protocol for browser control, scrcpy/Omniscrcpy for device visuals, a minimal keyboard relay for approved hotkeys/text, GitHub for public receipts, and Drive for Gemini-facing mirrors.

This converts the months of manual copy/paste between Acer and Liris into a named recurrent loop: visual state, text state, proof state, and agent decisions all cross-pollinate through receipted channels.

Bottom line: the accidental Liris-Chrome navigation is a real discovery. It should become a first-class Asolaria MCP catalog and named-agent ability set: `CROSS-SEAT-VIS-COMMS`.
