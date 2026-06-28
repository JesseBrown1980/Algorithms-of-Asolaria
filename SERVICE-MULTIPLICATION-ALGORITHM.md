# The Service-Multiplication Algorithm (reduction-scaling by replication)

**Claim.** To scale reductions you do not tune the reducer — you **replicate the service**. Because the
rename-before-load seam makes replication free, multiplying a service multiplies its reductions at ~0
marginal cost. This is the algorithm behind the multi-emitter / trillion-agent regime.

## The service S (one emit→loop→reduce unit)
```
S = revolver PID emitter  →  asolaria-loop cycle  →  PRISM reduction
    (revolver.next, ~200ns)   (rename-free room)     (many rooms → reverse_gain GNN → 1 answer)
```
One thread runs S at the **~200ns-class spawn** rate: 1 PID / 200ns ≈ **5,000,000 emits/s**, each
emit driving one PRISM many→1 reduction.

## The algorithm
```
multiply_service(S, N_emitters, M_spindles):
    # 1. multiply the spindles: 24 → 100 → 1,000 → 10,000
    spindles = replicate(S.spindle, M)            # 24 → M ; each spindle runs its own S
    # 2. divide threads into N parallel emitters (NOT one 200ns emitter on one thread)
    emitters = [revolver_emitter(thread_i) for i in range(N)]
    # 3. rename-before-load makes each replica FREE (no same-name throttle to pay)
    for s in spindles: s.room = rename_before_load(s.room)   # cost ≈ 0
    # 4. run all N×M replicas; each independently emits → loops → PRISM-reduces
    return parallel(run(e, s) for e in emitters for s in spindles)   # N×M reduction streams
```

## Rate
| quantity | value | tag |
|---|---|---|
| 1 emitter, 1 thread | ~5,000,000 emits/s (1 PID / ~200ns) | **MEASURED** (`asolaria-loop.mjs`, `drive-wave-cascade-pipeline-60D`) |
| reductions per emit | 1 PRISM many→1 (reverse_gain GNN) | **MEASURED** (`planPrismRoute`) |
| N emitters × M spindles | N×M parallel reduction streams | derived |
| full multi-emitter regime | **≈ 1.16 trillion agents/second** | **OPERATOR-CANON** |

## Why it is a *reduction*-scaling algorithm
Each replica of S terminates in a PRISM many→1 collapse. Replicating S by `N×M` therefore replicates
the reductions by `N×M`. The multiplication itself is the reduction-scaler: **more emitters → more
parallel PRISM reductions → more total reduction**, and the rename seam makes the multiplication free.

This is the algorithmic core of the every-device-surface goal: each device runs a cheap replica of S
(local ~0-token emit + PRISM reduce); multiplying surfaces multiplies reductions, while the heavy
reasoning is forced onto the supercomputers via the dispatched envelopes.

Companion docs: `JesseBrown1980/omni-dispatcher` → `EMITTER.md` (the emitter that feeds the
dispatcher); reductions repo → `MULTI-EMITTER-SERVICE-MULTIPLICATION.md` (the reductions framing).
