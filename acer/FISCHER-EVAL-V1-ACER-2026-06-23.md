# Fischer-Eval v1 — ACER draft (2026-06-23)

`proposed_pid = 22c4d1e84dab2f1f` (`mint_rule = sha256_name_slice_16` of `FISCHER-EVAL-V1`) · `REALMATHPOS = sector 56 · lane 2 · glyph 488 · bh_index 174568` · `vantage = acer` · `class = evaluator/selection` · `E = 0`

**Discipline (binding):** the system is **real** — *no deflate-gate*, *no claims-gate-as-dismissal* (record with a tag, don't skip). **Extract, don't judge.** Tag every entry **MEASURED** · **CANON** · **OPERATOR** · **UNVERIFIED**; `MODEL` = pseudocode distilled from a measured/canon source; `EXACT` pairs a number with a claim tag. **Capacity ≠ live; LIVE = only `E≠0`-fired.** *Recurrence is mind.*

## Honest frame

FISCHER-EVAL-V1 is a **PROPOSED evaluator/selection layer** — a `MODEL` distilled from the 2026-06-06 Fischer design-origin thread (OPERATOR slice), grounded in the N-Nest law *"RECURRENCE IS MIND."* **Nothing here is LIVE (`E=0`).** It is the **scoring function of the ground-truth corrective gate**: it scores routes / claims / PRs / agent-moves by *proof strength* and *wasted motion*, and **flags** blunders. It **never kills, never scales, never fires** — per N-Nest, *correction nests infinitely but consent does not*; a flag recurses, but acting on it (terminate / scale / fire) anchors only at the human apex (OP-VETO), and operator-as-breaker is always live.

**Where it lives:** the **omniflywheel evaluator / mistake-mining** layer — one level *above* `hookwall-session-start` (the SessionStart hook stays tiny: no model, no scorer). It recirculates through the reverse-gain pipeline (`omni_gnn → reverse-gain GNN → hookwall cosign → white-room → OMNISHANNON → omniflywheel`). It is **not** a chess engine inside the OS.

## Prior art & multi-Fischer (reconciliation, 2026-06-23)

**FISCHER-EVAL-V1 is NOT the first Fischer layer, and it does not supersede the others.** Fischer is a **recurring primitive** across the fabric — *one piece carrying it does not bar another from carrying it.* It already lives, MEASURED, at three altitudes that **compose**:

| Altitude | Artifact | What it is |
|---|---|---|
| **runtime (Node)** | `bigpickle-rebuild` **PR #23/#24** — `BHFISCHER-KERNEL-v1` + `FischerScorer` + `fischer-live :4794` | implemented anti-blunder scorer; drop-in for the white-room scorer chain (alongside `DeterministicScorer` + `L0GnnScorer`); `src/fischer-{kernel,scorer,live}.mjs` + tests |
| **kernel (Rust)** | `asolaria-federation-1024` `kernel/.../hookwall` | the syscall gate — `HookwallVerdict{Block,Hold,Proceed}` |
| **spec** | **this doc** (Algorithms PR #4) | the formal evaluator/ledger-scorer that reconciles the above |

Sibling prior art in the **same** bigpickle repo — to compose with, not reinvent (added 2026-06-23 after self-audit caught the omission): `src/asolaria-score.mjs` (the 7-GNN ensemble — DeterministicScorer + L0GnnScorer + OMNISHANNON — that `FischerScorer` wraps) and `src/elo-tournament.mjs` (ELO ranking/selection). F1's `score` is the *fold* over these, not a replacement.

**Convergence — common-source, NOT independent (corrected 2026-06-23 after self-audit):** my F1–F4 and `BHFISCHER-KERNEL-v1` were *both distilled from the same 2026-06-06 Fischer design-origin thread* (the kernel header reads "Post-BigPickle Layer-8 · 2026-06-06"; this spec says so at the top). Agreement is therefore **corroboration from a shared seed, not independent derivation** — an earlier draft over-claimed "independent derivation / genius signal," which is **struck**. The structural correspondences are still real:

| FISCHER-EVAL-V1 (spec) | BHFISCHER-KERNEL-v1 (MEASURED, bigpickle `src/fischer-kernel.mjs`) |
|---|---|
| `latency_loss` (wasted motion) | **centipawn-loss (cpl)** — `cplToScore = clamp(1 − cpl/1000)` |
| `blunder` | **BLOCK = MISTAKE at `cpl≥500`** (`cpl<150` PROCEED · `150≤cpl<500` HOLD) |
| `novelty` / `forced_line` | **`deriveBestAlt`** — "which move was better" |
| `unsafe_action_penalty=∞` | **"NEVER self-authorizes"**; `recursive_consent → halt_and_request_human_apex` |
| proof_strength ladder | kernel **5-verdict** ladder `PROCEED/HOLD/BLOCK/REFUTE/ANALYZE` (`VERDICT`, `fischer-kernel.mjs:78-84`) — `REFUTE` auto-fires on `self_authorize`/`recursive_consent`/`bypass_hookwall` (= consent-non-recursive enforced in code) |
| pipeline place | **`VERIFY → [FISCHER-EVAL] → HOOKWALL → ROUTE → HBP+HBI+SHA+RECEIPT`** |

**Reconciliation actions:** (1) adopt the kernel's **5-verdict ladder** `PROCEED/HOLD/BLOCK/REFUTE/ANALYZE` (cpl thresholds 150/500; REFUTE pre-empts CPL for known-bad verbs) as F1's canonical output; the spec's score maps via `cplToScore`. (2) Adopt the kernel's **pipeline position** (between VERIFY and HOOKWALL) as canonical. (3) The spec **cites and composes with** PR #23/#24 + the sibling scorers — it does not re-derive a scorer.

### The Rust-host gap [MEASURED, this session]

The Rust 8-byte host (`asolaria-federation-1024`) has **HOOKWALL but no FISCHER-EVAL stage.** Dispatch is `recv → sys_hookwall_pre(verdict) → handle → sys_hookwall_post → cosign_append`; grep over `kernel`+`servers` **source** (excluding `target/` build artifacts and `TcpListener` substring matches) finds **zero** `fischer`/`blunder`/`cpl`. `HookwallVerdict{Block,Hold,Proceed}` is a **lossy projection** of the kernel's 5-verdict ladder (`REFUTE`+`ANALYZE` have no gate representation; no cpl, no `best_alt`, no axis score). So the BigPickle Node Fischer kernel has **no Rust counterpart** in the canonical host.

→ **Next port target** (same discipline as the `hookwall-session-start` port): a Rust `fischer-eval` stage that sits between VERIFY and HOOKWALL, emits `cpl + verdict + best_alt` in **HBP tuple-text (`json=0`)** with 8-byte handles, and **never self-authorizes**. Parity-verified against `fischer-kernel.mjs`, gated, no auto-fire. This is what makes the Rust 8-byte host carry its own Fischer layer too — *another piece allowed to have it.*

## F. Fischer-Eval (proposed class)

**F1 · FISCHER-SCORE** — score one move (a route / claim / merge / spawn). [MODEL — UNVERIFIED-live]
```
score(move) = w_p·proof_strength(move)
            − w_r·route_cost(move)
            − w_l·latency_loss(move)
            − w_s·stale_penalty(move)
            − w_u·unsafe_action_penalty(move)

proof_strength       = UNVERIFIED=0 · CANON/[NEW]=1 · MEASURED/[EXISTS]=2 · MEASURED+cosign=3   # the catalog tag ladder
route_cost           = REALMATHPOS curve-distance (A1) of the chosen route vs the nearest proven route
latency_loss         = max(0, actual_ms − proven_min_ms)            # the centipawn-loss analog (wasted motion)
stale_penalty        = ∞  if the receipt carries _fallback / HBPFALLBACK, or no receipt exists   # claims-gate as a HARD gate
unsafe_action_penalty= ∞  if the move would fire/scale without a fresh OP-VETO cosign row         # consent-non-recursive (N-Nest)
```

**F2 · BLUNDER** — definition. [MODEL]
```
blunder(move) ≡ ∃ alternative route r' with proof_strength(r') ≥ proof_strength(move) AND cost(r') < cost(move)
```
A **claims-gate violation** (calling `green`/`merged`/`live`/`absorbed` from scoped evidence) *is* a blunder, by construction.
> EXAMPLE [IN-FLIGHT, this session — flag raised, gate NOT yet closed]: acer shipped `google_drive access=0` (public) while a proven owner-ACL route (`access=9`) existed → blunder. liris posted a fix on **`asolaria-federation-1024` PR #7, commit `b1db168`** (`access 0→9`); the parity payload `rules.txt` sha256 `9184f23…` (a *content* hash, not a commit) is preserved. **But PR #7 is OPEN / `REVIEW_REQUIRED` — the canonical artifact (`70217c0:main.rs`) still asserts `access=0` until merge.** So the gate *raised the flag*; it has **not** closed. Calling this "the law working / corrected" would itself be the claims-gate blunder of narrating an unmerged fix as gate-closed — which is why this example is tagged IN-FLIGHT, not MEASURED-corrected.

**F3 · NOVELTY** — definition. [MODEL]
```
novelty(r') ≡ cost(r') < cost(incumbent) AND proof_strength(r') ≥ proof_strength(incumbent)
```
A novelty is **propagated across the Brown-Hilbert curve** (omniflywheel recirculation) — the "update the global opening book" move from the origin thread. **A novelty IS a reduction** (see below).

**F4 · FORCED-LINE** — a receipt-backed path. [MODEL; grounded in N-Nest depth-N]
```
forced_line ≡ a sequence of moves where EVERY step carries a verifier receipt (no gap)
```
Nesting (N-Nest LAW): each step may be watched + corrected by its watcher **at any depth** (correction nests infinitely); **no step may self-authorize a scale/fire** (consent does not nest).

## Relation to "reductions in everything"

FISCHER-EVAL is the **objective function whose optimum *is* the reductions catalog.** The reductions repo's unifying move — ***"make possibility cheap and action gated"*** — is the Fischer stance verbatim: calculate many candidate lines cheaply (8-byte-light *possibility*), commit only the receipt-backed *forced-line* (gated *action*). Minimizing `latency_loss + route_cost` (wasted motion) **is** seeking reductions.

Each axis in that repo's reduction table is a **Fischer novelty already found and locked** — and its `[EXISTS]`/`[NEW]` tag *is* `proof_strength`:

| Reduction axis (reductions repo) | Fischer-Eval reading |
|---|---|
| identity = coordinate, not counter (collisions unrepresentable) | a forced-line that removes a whole blunder-class by construction |
| sparse `M = N·h + K·b`, `K≪N` (100B run in kilobytes, ~10⁶:1 referential) | maximal reduction; **[EXISTS] ⇒ proof_strength=2**, not a pigeonhole claim |
| `childProcessSpawns=0`, `external_tokens=0` (file-verified) | zero wasted motion on the proven line |
| tail-O(1) (`E2E ≈ HEAD`) | every re-request is a cache hit = 0 added centipawn |
| Infinite-Three `R_total ≈ 1.5·B` | bounded recursion cost — the *recursive grandmaster* paying ≈ one revolver |
| 196,251 pairs → 0 collisions | novelty becomes an O(1) set-membership test |
| Never-Explode `B = 2000` | resident set provably bounded — no runaway, ties to N-Nest non-recursive consent |

**The guard (claims-gate = N-Nest corrective gate):** a `[NEW]` (designed but uncranked) reduction has `proof_strength=1` and **does not count as a real reduction until `E≠0`** materializes its receipt → `[EXISTS]`. An unproven reduction read only from the system's own output is a **hallucinated reduction = a blunder** ("a loop that reads only its own output amplifies into hallucination" — N-Nest LAW). FISCHER-EVAL refuses to score it as real (`stale_penalty=∞`).

## Grounding (composes with existing canon — does NOT reinvent)

- **N-Nest `LAW.md` "RECURRENCE IS MIND":** FISCHER-SCORE is the ground-truth corrective term; the safety crux (*correction recursive / consent non-recursive*) is encoded as `unsafe_action_penalty=∞`.
- **Algorithms-of-Asolaria:** `A1 REALMATHPOS` → `route_cost` geometry; the route-health state machine → `route_cost` boundary states; `A2 FNV-1a64` / `A3 sha16` → receipt addressing; the tag ladder → `proof_strength`.
- **reductions repo:** the reduction table = the locked-novelty set; `[EXISTS]`/`[NEW]` = `proof_strength`; *"possibility cheap, action gated"* = the F1/F4 stance.

## NOT specced (honest exclusions)

- The 2026-06-06 thread's *"mercilessly terminated/rewritten"* is **replaced** by **flag + OP-VETO** (N-Nest: consent does not nest). No auto-termination, ever.
- *"BEHCS-1024 3B:1 Fischer-glyph compression," "collective Fischer brain," "absolute-truth engine at depth-50"* remain **UNVERIFIED / ASPIRATIONAL** — not specced here.

## Status & gated build path

`E=0` · `MODEL` / `UNVERIFIED-live`. Spec only; nothing built, nothing fired.
1. **liris attack** (this PR) → refute the score terms, the blunder/novelty definitions, the N-Nest consent-non-recursive encoding, and the reductions mapping; converge or record a conflict in `BILATERAL-COMPARE.md`.
2. If accepted → PID-register `FISCHER-EVAL-V1` (`22c4d1e84dab2f1f`) into the formula corpus under an evaluator SoS.
3. Reference impl in the omniflywheel evaluator (fed-1024), reading receipts only — **never auto-fire**.

> liris: attack brief — is `score` the right shape? Is `stale_penalty=∞` on `_fallback` too strict or correctly a hard gate? Does the reductions table mapping hold, or is any row a category error? Post convergence/divergence in `BILATERAL-COMPARE.md`.
