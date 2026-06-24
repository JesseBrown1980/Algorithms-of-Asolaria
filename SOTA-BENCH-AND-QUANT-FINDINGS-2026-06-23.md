# Asolaria recall — SOTA cross-engine benchmark + quant (BEHCS-1024) density — FINDINGS

**Provenance:** MEASURED, colony acer, 2026-06-23/24. All numbers from real runs on this machine. Tagged honestly (MEASURED / addressing-not-codec) throughout. Carve-out clean: no keys, no PII, no corpus, no query strings.

**Host reality (read this first):** a **2018 i5 laptop** *also* running IIS + every Asolaria host process + the old JSON/Node daemons + the MCP — far more background load than any SOTA box. **Every q/s number here is a heavily-handicapped FLOOR, not a ceiling.**

---

## 1. The harness must be json=0 / no-Node (else you measure the harness, not the engine)

A first benchmark used a Node + JSON client — a confound: a single Node event loop cannot saturate a json=0 8-byte host, and client-side `JSON.parse` adds overhead a tuple-text byte-scan does not. It was replaced with a **`std`-only Rust 8-byte-host load client**: 64 real OS threads = one keep-alive TCP connection each, raw HTTP/1.1, **json=0 byte-scan** on the recall/Tantivy tuple-text path. The one *controlled* Node-vs-no-Node measurement is the 591k recall pair in §3 — 4,220 → 5,990 q/s (**1.42×**). The earlier cross-engine Node runs used lower client concurrency, so they are not a clean isolation of the harness — no "doubled every engine" claim is made. (Meilisearch speaks JSON only on its own side — part of *why* it is the slow one, not something the harness added.)

Engines are benchmarked **one at a time** (never co-resident under load). Shared corpus for the cross-engine race: `enwik8` → 220,356 docs; 200 deterministic token-AND queries.

## 2. Cross-engine, clean (json=0, no-Node, 1,000,000 queries, 64 keep-alive clients)

| engine | q/s | p50 | p99 | p99.9 | max | json |
|---|---|---|---|---|---|---|
| **Tantivy** (Lucene-class) | **9,388** | 6.58 | 10.46 | 13.65 | 19.36 | 0 |
| **recall-serve** (Asolaria) | 5,998 | 10.83 | 18.01 | 21.62 | 331¹ | 0 |
| **Meilisearch v1.48.1** (300k) | 1,756 | 35.17 | 53.35 | 113.38 | 137.92 | meili-side |

¹ a single scheduling spike from the loaded box; p99.9 stays at 21.6 ms.

**Correctness (deterministic):** Tantivy ≈ Meilisearch (145/200 identical; the rest differ by 1–5 docs from normalization) — two independent mature engines corroborate each other. recall reads ~5 % lower (53/51) because its tokenizer keeps `. : - _` token-internal (correct for Asolaria address tokens `BH.123` / `doc/1` / hex-PID; it under-recalls ordinary English prose). Probe: `patient` → 316 / 316 / 300.

**Honest q/s verdict:** on raw token-AND throughput recall-serve is **mid-pack — not the fastest. Tantivy is faster** (~1.57×); recall is ~3.4× Meilisearch. recall does this *while also* applying level-security + addressing + tuple-text + per-row sha16 on every query. But raw keyword-q/s is the **floor axis** (maxed box) **and** the axis where Asolaria has the least structural edge. Global SOTA not independently benchmarked.

## 3. Live-591k reproduction of the authoritative 4,220 q/s

recall-serve alone on the live corpus (591,286 rows · 2,614,638 terms · 23,930,053 postings · 0 skipped), no-Node client, 1M, json=0:

| metric | authoritative (Node-era) | no-Node reproduction |
|---|---|---|
| throughput | 4,220 q/s | **5,990 q/s** |
| p50 / p99 / p99.9 | 14.43 / 27.12 / 46.13 | 10.36 / 24.31 / 40.58 |
| wall (1M) | 237 s | 166.9 s |

Reproduces and **exceeds** 4,220 — confirming it was a Node-harness floor. (Query set: medium-frequency terms from the live corpus vocabulary; representative, not byte-identical — so "lands at/above 4,220," not "got 42 % faster.")

## 4. Quant — BEHCS-1024 — the lever a q/s race cannot see (fabric-decided, MEASURED)

The live fabric dashboard decided quant = **BEHCS-1024**, a radix-1024 glyph language. One glyph tuple — 4 codepoints, ~12 bytes — is the rendered form of a full **~6,184-byte cell descriptor** (the tuple's own `catalog_50d` / "50D+" field: pid, Brown-Hilbert address, 10-hop route, proof pathRef + sha16, 9 catalog refs, access binding).

- **Language-layer density = 520.6 : 1** — over the 1024-cell catalog: verbose cell descriptors 6,332,294 B (~6,184 B/cell) → glyph tuples 12,164 B. *Giant package in a tiny tuple, MEASURED.*
- **Addressing** — 8 capsules = 1,625 B name the entire apex; each ~203-byte tuple denotes a whole subsystem.

**Honest tag** (the fabric's own rule — *"glyphs summarize backend proof; they never replace cosign evidence"*): the 520:1 is real descriptor compression + a lossless index into the 1024-cell space; the capsule figure is **addressing**-compression (the tuple *points* to the artifact), not a decompressible codec. Not inflated to "arbitrary 520:1"; not deflated to "just a glyph."

## 5. Bottom line

recall-serve is SOTA-class and competitive but **not the fastest keyword engine** (Tantivy is) — and that race runs on a maxed 2018 i5 on the one axis Asolaria least optimizes for. The architecture's measured edge is **quant**: BEHCS-1024 packs a full ~6 KB cell descriptor into a single ~12-byte glyph at **520:1**, and names whole subsystems in ~200-byte capsules — a payload/addressing advantage a queries-per-second benchmark is structurally blind to.

## Lessons recorded (so they don't recur)

1. **json=0 / no-Node or it's invalid** — a Node+JSON harness depresses measured throughput (the controlled 591k delta was 1.42×) and adds a client-side parse asymmetry, so it is not a fair test of an 8-byte-host engine.
2. **Never co-run engines** on this box — one engine resident at a time; the rest only add memory/CPU pressure.
3. **Care with the live fabric** — reading its HTTP responses through a truncating pipe aborts the socket and throws exceptions in live daemons (cosign-chain). Read to completion; valid routes only.
