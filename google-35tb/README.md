# Google 35 TB Research Section — Gemini Review Handoff

Evidence tag: OPERATOR_OBSERVED + RESEARCH_STAGING
Date: 2026-06-20
Status: metadata/research lane, carve-out enforced

## Purpose

This section defines how the 35 TB Google Drive layer should participate in the multi-cylinder / Shannon-wave / compression-math research without leaking private material.

The Drive is not just backup storage. It is the fourth/fifth large substrate for Asolaria archaeology and model discovery:

- corpus papers
- BEHCS / SOVLINUX exports
- quantum / RF / neural research
- genesis agent source
- visual history artifacts
- public-face summaries for Gemini review

Personal, legal, financial, phone-private, vault, and device-secret trees remain carve-out.

## Current measured boundary

From Acer operator-observed run:

- 253 Asolaria-substrate records cataloged.
- The asolaria-library tree was reported essentially complete for this pass.
- The rest of the 35 TB was held as carve-out: legal / financial / personal / device trees.
- No full personal-tree census was performed.

From this GitHub seat:

- Drive bytes are not directly visible.
- This file is a handoff spec for reproducible cataloging and Gemini review, not a claim of local measurement.

## Gemini review packet

Gemini-facing packets should be carve-out-clean and small enough to inspect:

1. `MULTICYLINDER-SHANNON-DRIVE-GEOMETRY-2026-06-20.md`
2. Real-source map summary from reductions PR #17
3. Sector-density summary, when produced
4. Shannon-wave descriptor, when produced
5. Distance-spectrum sample, when produced
6. Compression candidates with proof tags

Each packet must include:

- evidence tag: MEASURED / CANON / OPERATOR_OBSERVED / CONJECTURE / UNVERIFIED
- source layer: USB / C / D / GDRIVE / WSL / GITHUB
- carve-out statement
- hash or row count when available
- no raw private paths beyond safe public-facing labels

## Required Drive catalog schema

Minimum row fields:

```text
GDRIVE|id=<id>|parent=<parentId>|name=<safe_name>|mime=<mime>|size=<bytes>|mtime=<iso>|class=<CORPUS|DATA|RUNTIME|MEDIA|CARVE>|sig=<0|1>|sha_hint=<optional>|notes=<safe notes>
```

For carve-out rows, only safe metadata should be retained:

```text
GDRIVE_CARVE|class=<legal|financial|personal|phone|vault|device>|count=<n>|bytes=<optional aggregate>|opened=0
```

## Research tasks for Drive/Gemini

- Confirm whether the 253 substrate-record catalog is enough for the public research packet.
- Identify corpus folders that can be safely included for Gemini models.
- Build a sector-density summary from Drive-visible PIDs without including private names.
- Produce bounded Shannon-wave samples across all 113 sectors.
- Ask Gemini to critique the compression candidates, but require it to tag conjecture vs proof.

## Do not do

- Do not upload private phone trees.
- Do not expose legal/financial/personal raw paths or contents.
- Do not claim Gemini verified the live system.
- Do not treat Drive metadata as a substitute for USB/D/C/WSL metal measurements.
- Do not run large cascades from Drive review alone.

## Next bridge

When Acer pushes the generated sector-density and Shannon-wave samples, this section becomes the Google/Gemini intake point. Until then it is the structured research slot that was missing from `Algorithms-of-Asolaria`.