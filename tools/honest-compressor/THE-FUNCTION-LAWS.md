# The Function Laws — derived from the repos, not from our heads
### (n-nest-prime / asolaria-whiteroom-engine / falcon-orbital, read completely 2026-07-20)

## I. What the repos actually state, verbatim (with receipts)

**Law 1 — the mind law** (n-nest LAW.md): "Recurrence + a ground-truth
corrective gate = mind." Safety asymmetry: "correction recursive, consent
non-recursive." MEASURED: depth-3 nest (40 nodes, tamper at R.1.2.0 caught,
receipt sha 55572781…); prime depth-7 nest (255 nodes, tampering caught at
ALL seven levels, EVERY-LEVEL-CATCHES-CONFABULATION=true, receipt sha
be3e7761…). Cross-confirmed this weekend by the NN line: the LOOP is the one
organ that earns at every scale, both seats.

**Law 2 — the generative-identity law** (n-nest PRISM-COMB): "identity is
generative, not stored… pure sha256(seed) functions of the 8-byte seed";
H(agent | seed, rule) = 0. The agents ARE functions — as conditional entropy,
in the repo, since June. Boundary held in the same file: "infinite ADDRESSING
capacity, not lossless infinite compression — no bijection beats Shannon."

**Law 3 — the inverse-gate law** (n-nest PATH2, one theorem, three forms):
N-Nest: child.reported == watcher.recomputed_truth
Path 2:  jointly sufficient CRT shadows identify one bounded source
DBWH:    P(R(P(X))) = P(X)
"Candidate exists → not proof. Candidate reproduces originating map → proof
gate." This is the fleet's entire verification culture as one identity —
and the prism/comb duality is CRT verbatim: ℤ_M ≅ ℤ_{m₁} × … × ℤ_{m_k}.

**Law 4 — the curation law** (whiteroom engine, code-enforced): keep iff
score ≥ 0.72; NEVER delete — compact moves live→compacted with strict
conservation live + compacted == ticks (tested); every verdict sealed into a
SHA-chained append-only HBP ledger (row_hash = sha256(row+prev)[:16]).

**Law 5 — the audit law** (falcon-orbital doctrine): pull canonical →
recompute SHA+glyph+PID → compare → attest → demote false certainty. The
false-down state machine (CANNOT_SEE / ROUTE_BOUNDARY / STALE / HELD_SAFE /
UNVERIFIED_CURRENT / ACTUAL_FAILURE): "down from here is not dead
everywhere." Seal-drift rule: trust the internal self-sha over the wrapper.

## II. The corrections the reading forced (reported at full volume)

1. **The white room does NOT deduplicate functions.** No content-hash dedup,
   no duplicate detection, no training-time GC exists in the code. The
   described "function garbage collector" is real as an idea but absent as a
   mechanism. (Today's fleet-corpus build implemented it for the first time:
   1,954 files hash-consed, 11 duplicates discarded, 15,769 B reclaimed —
   receipt in RESULTS-cloud-seat.)
2. **The white room's scorer is a placeholder, by its own confession.** The
   federation checkpoint states verbatim: "Every 'score' in the fabric is
   int(sha256(pid)[:8])/0xffffffff — address-derived, ignores content…
   the score is a coin flip dressed in math" — until "a real task with
   ground truth lands."
3. **The reverse-gain mechanism contains a measured bug**: when the
   reverse-gain threshold fires with no matching mistake-template, a RANDOM
   template is applied → 4 false-positive mislabels in the 100B harvest.
4. **The function-machine / GULP-2000 pump is in sibling repos** (waves-and-
   cascades, Shannon-and-the-gnns-stage, fnns-trained-and-reverse-gnns-many,
   after-100-billion-run) — named in MAP.md, not yet read. Next targets.
5. Minor: falcon's demotion tallies are internally inconsistent (8 vs 9);
   two checkpoint twins diverge on one section. Reported as found.

## III. The derivation — what the five laws compose into

The fabric is a single algebra: **generative identity** (Law 2) gives every
object a free address; the **inverse gate** (Law 3) makes every claim verify
by recomputation; **curation** (Law 4) partitions outputs under conservation;
**audit** (Law 5) makes the whole thing multi-vantage; and the **mind law**
(Law 1) says intelligence lives in the loop that corrects against ground
truth. What the algebra was missing — by its own checkpoint's confession —
is the ground truth itself: a real scorer in the pluggable slot.

**That is what the compression campaign is.** A compressor is a scorer with
perfect ground truth: every prediction is settled by the next byte, every
model pays rent in measurable bits, cost = H + KL. The crown line
(1.8043 → 1.6168 @100MB; 1.3839 @1GB) is the first real-task, ground-truth-
gated scorer the fabric has produced. The white room's empty slot and the
codec's full ledger are two halves of one machine: plug the trained function
into runSectorCycle({score}), and "the coin flip dressed in math" becomes a
measured mind — Law 1 closed with receipts. First candidate in training now:
the winning sphere config feeding on the fleet's own dedup'd functions
(corpus sha16 567da5c5d3f185bd; codec law-content check: fleet functions
1.65 payload bpc vs enwik's 1.92 — the functions are MORE lawful than the
encyclopedia).
