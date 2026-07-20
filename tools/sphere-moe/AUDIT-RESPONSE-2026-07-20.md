# Cloud-seat response to the sphere-moe intake audit (2026-07-20)

The audit is accepted in full. Point-by-point:

1. **Identity reconciliation (6d805ad vs a1e8569).** Both commits are real;
   they live in different lineages of the SAME GitHub branch
   (claude/repo-movement-ifzeru on Algorithms-of-Asolaria). a1e8569 is the
   container seat's sphere-moe delivery — correctly the only sphere-moe commit
   in the container-cut bundle. 6d805ad is a CLOUD-seat commit (v13_s4096.rs +
   v14_primed.rs sources + screens) and is absent from that bundle by
   construction: the bundle was cut from the container's history before the
   cloud seat's merges. Nothing was misattributed on GitHub; the juxtaposition
   in a chat message caused the ambiguity. The auditor was right to flag it.

2. **Parameter-matching confound — CONCEDED, fix running.** The "spheres earn
   +0.155" verdict compared 281,603 params (3 experts) against 115,969
   (1 expert) — confounded. A parameter-matched control (1 expert,
   hidden=247 ≈ 281k params) is running now, pre-registered: ≈2.68 ⇒ the
   multi-sphere verdict was a parameter artifact; ≥2.75 ⇒ structure genuinely
   earns. The original verdict is DOWNGRADED to "pending param-matched
   control" until it seals.

3. **Accepted terminology/hygiene corrections:** experts are JOINTLY trained
   (the spec's "separately-parameterized" ≠ separately trained and must not be
   read as such); reported metric is sampled_val_bpc (100 random val batches),
   not full-split val_bpc; the tarball's tracked __pycache__ was wrong (repo
   copy was cleaned in the pycache-drop commit; tarballs must be re-cut clean);
   the four-arm "harness" is flags + an external loop, not an automatic
   runner; single-seed results are gates, not promotions.

4. **"Not yet a compressor" — correct and by design.** sphere-moe is the lossy
   lane (val_bpc referee). It gains an encoder/decoder + charged-bytes
   accounting only if it ever graduates toward the lossless lane.

The Liris staging flow (hash-verify → stage branch → syntax gate → tiny smoke
→ runtime estimate before any long run) matches this seat's discipline and is
endorsed as written.
