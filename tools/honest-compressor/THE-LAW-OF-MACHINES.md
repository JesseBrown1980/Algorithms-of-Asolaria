# The Law of Machines — the mathematics under "match the machine to the law"

Derived 2026-07-20 from the fleet's measured grid (8 machines × 4 laws, 32
runs, all restore=OK) and the day's crown line. Every claim here either has a
receipt already or states the exact experiment that would give it one.

## 1. The master identity: mismatch is paid in bits

For a data source S and a machine (model) M, the cost of coding S with M is

    cost = H(S) + KL(S ‖ M)

H(S) is the entropy floor — the surprise that must be paid no matter what.
KL(S‖M) is the mismatch tax — extra bytes paid because the machine's law is
not the data's law. EVERY number in the 32-run grid is this identity:
- Lawful sphere: H≈0, so cost ≈ pure KL — and the simplest machine already
  drove KL≈0 (597 B). Organs past M4 earned exactly zero: KL was already gone.
- Chaos: KL≈0 for every machine (no law to mismatch) so cost ≈ H = the floor;
  bigger machines paid MORE only in overhead — friction, not mismatch.
- Text: H large but not total; each organ that removed real mismatch earned
  monotonically (273,119 → 237,716).
- Foreign-glyph priming (+34,156 @100MB): DELIBERATELY installed KL. The
  unlearning tax is KL made visible.

## 2. The mixture theorem: why mirrors are cheap insurance

A Bayesian mixture over K machines codes within log2(K) bits TOTAL of the best
single machine in hindsight (universal coding regret bound). That is why the
mirror's downside on homogeneous text was microscopic (+0.004 bpc: bounded
regret), and why ensembles-of-laws are always worth carrying if any segment of
the data might prefer another machine. Corollary measured: the two-row soft
gate (even blend) beats hard assignment — a mixture IS the optimal posture
under uncertainty about which law rules the position.

## 3. The switching theorem: what the mirror is FOR

For piecewise data (laws that change under your feet), the optimal coder is a
SWITCHING mixture: pay ~log2(K) at each law boundary, then ride the best
machine inside each segment. Value of the router = Σ_segments [KL(best-global)
− KL(best-local)] − switching cost. Prediction (in flight, task bh7b0kp2c):
on a 4-law concatenation the mirror earns >0.02 bpc; on one law it cannot.
The real universe — and enwik10, and fabric traffic — is piecewise. This is
the mirror's true regime.

## 4. The tracking theorem: why >>14 was already optimal

For a law that DRIFTS at rate d, a learner with rate η pays
excess ≈ a·η (noise chased) + b·d²/η (drift missed), minimized at
η* ∝ d^(2/3)-class tradeoffs. Consequences, both already measured:
- The color-triad collapse (fast/slow banks → tie as the triad tightens):
  enwik's drift rate fixes ONE optimal η; extra rates are redundant dials.
- The gradiated sphere costing 2.4× the fixed sphere, with M4 (not the crown)
  winning: drift is information — you pay for the law's derivative, forever,
  and over-fragmented machines (4096 wheel) track drifting simple law WORSE.

## 5. The capacity theorem: why the ladders never turned (yet)

Wheels (12→65,536) and tables (23→28 bits) are the same object: partitions of
context space into rooms of statistics. Finer rooms cut KL (specific laws per
room) but raise cold-start cost (each room learns alone). The measured
monotone wins at 1–100MB say enwik's law-diversity still exceeds our room
count at every rung tried on this box. Prediction: every partition ladder
turns when rooms ≈ distinct sub-laws in the corpus; the turn point grows with
corpus size (measured: 48 flattened at 1MB-era configs, won at 100MB-era).

## 6. The convergence: what the whole fabric is

- The 65,536 wheel = a HARD router keyed by last-2-bytes.
- The mirror = a SOFT router with learned keys.
- Phase-2 "gravity" = a router whose KEYS the data invents (latent identities).
- The 8-byte PID atom = the address of a room.
- The sphere-moe = the same architecture in the lossy world.
Compression = removing KL against discovered law. Hutter's thesis: that IS
the measurable core of intelligence. One object, many masks: a mixture over
machine-space, and every design question is where to spend the log K.

## Testable predictions this document commits to

P1. Mirror earns >0.02 bpc on 4-law mixed corpus, ~0 on any single law. [running]
P2. Partition ladders (wheel/tables) turn exactly when room-count ≈ corpus
    sub-law count; turn point rises with corpus size. [tb29+ on big-RAM seats]
P3. Two-timescale (HRM) earns only on corpora with two drift scales — fails
    at 2MB text (measured ✓), should earn on mixed drift-rate corpora. [queued]
P4. Router value grows with segment length × law-contrast; a boundary-dense
    corpus (short segments) starves it via switching cost. [cheap follow-up]
P5. In-domain priming saving grows sublinearly per decade (11.6k→19.4k→55.3k
    measured) and never crosses a 1MB charge. [extrapolation on record]
