# M2 Outer-Watcher Upgrade Plan (E=0)

Status: E=0 upgrade plan. No migration, no fire, no process launch, no restart.

This plan follows the completed map artifact:

- `research/OUTER-WATCHER-MATRIX-LAYER-MAP-2026-07-01.md`
- `research/MAP-VERTICES-NOT-HOST8-PROCESSES-2026-06-30.md`

It turns the outer-watcher / matrix map into the next bounded Host-8 work cells. It does not implement
them in this repo. The implementation gate belongs to the Rust host repo (`asolaria-federation-1024` /
the owning Host-8 source branch) after a fresh owning-gate check.

## Evidence and boundaries

```text
M2PLAN_EVIDENCE|class=MEASURED_GITHUB|repo=JesseBrown1980/Algorithms-of-Asolaria|branch=acer/map-host8-boundary-2026-06-30|tip=4c5d951|artifact=research/OUTER-WATCHER-MATRIX-LAYER-MAP-2026-07-01.md|signed=1|json=0
M2PLAN_EVIDENCE|class=LIRIS_MEASURED|surface=fabric_health|ok=true|service=super-asolaria-os-dashboard-liris-mirror|port=4944|apex=COL-ASOLARIA|json=0
M2PLAN_BOUNDARY|class=LIRIS_MEASURED|surface=bus_health_and_council_query|state=fallback_unavailable|action_confirmed=0|do_not_claim_bus_ok_from_liris=1|json=0
M2PLAN_EVIDENCE|class=LIRIS_LOCAL|surface=.asolaria-workers/supervisors|profile_files=28|meaning=local_supervisor_profiles_not_global_census|json=0
M2PLAN_EVIDENCE|class=OPERATOR_OBSERVED_ACER_TRANSCRIPT|m1a=24_profile_subagents|m1b=16_gac_seats|fabric_route_map_seen_by_acer=1|not_remeasured_from_liris=1|json=0
```

Boundary rule: map rows and atlas vertices stay `host_process=0` unless an owning Host-8 runtime receipt
proves a running process. M2 may build source and tests; M2 must not fire E != 0.

## Target shape

The map's key finding is still the governing design:

```text
M2_SCOPE|shape=compose_one_surface_not_five_engines|preferred_first_cut=host8_serve_watch_routes|alternate=servers_outer_watcher_crate|build=E0|fire=operator_T0_only|json=0
```

Start with a `/watch.*` route family inside `host8-serve` unless the owning Rust repo shows that a sibling
`servers/outer-watcher` crate is already the local pattern. The reason is narrow blast radius: route-family
first proves the watcher contract over existing primitives before adding another server binary.

## Work cells

| Cell | Scope | Acceptance gate |
|---|---|---|
| W0 | Fresh owning-gate check of Host-8 repo, branch, CI, and live/fallback fabric state. | Report exact branch, commit, Rust toolchain, required CI, and live-vs-fallback probes before edits. |
| W1 | Define read-only HBP watch routes: `/watch.health.hbp`, `/watch.liveness.hbp`, `/watch.verdict.hbp`. | Tuple-text only (`json=0`); no process launch; no restart verb; no mutation path. |
| W2 | OP-00 witness surface. | Witness rows are describe-only unless cosign/T0 grants E != 0; OP-00 can observe and hold, never restart. |
| W3 | ROOK freshness map. | Per-seat last-seen / last-kick values produce `fresh`, `stale`, or `unknown`; `timeout` is not `dead`. |
| W4 | SENTINEL held-safe-vs-dead guard. | Any restart-class intent is converted to HOLD unless explicit operator/T0 receipt exists. |
| W5 | Hookwall interposition in observe/log-only mode. | `sys_envelope_send`, `sys_envelope_recv`, and `sys_exec` pass through hookwall pre/post; 10K-call bypass test passes. |
| W6 | N-Nest correction gate port. | Port parity against `nest-depthN-prime-verify.cjs` golden vectors; consensus never overrides recomputed truth. |
| W7 | GNN/reverse-risk/crypto fail-closed fixes. | No hard-zero reverse risk; no always-false signature verification unless named as a held blocker; no trained-GNN claim until model load is measured. |
| W8 | Fischer gap handling. | Keep Fischer as blocker unless Rust source has a score producer; verdict-only port requires golden-vector parity and no auto-fire. |
| W9 | OmniShannon/Shannon feedback prerequisite. | Treat dormant 4820/4821 and unwired reverse-gain sink as blockers for self-improvement crank claims. |

## Non-negotiable invariants

```text
M2_INVARIANT|name=no_fire|auto_fire_allowed=0|process_launch=0|restart=0|kill=0|taskkill=0|reboot=0|json=0
M2_INVARIANT|name=hbp_first|json=0|tuple_text=1|browser_json=diagnostic_only|json=0
M2_INVARIANT|name=map_boundary|map_node_semantics=visual_coordinate|host_process=0|promote_requires_host8_receipt=1|json=0
M2_INVARIANT|name=fail_closed|unknown=hold|timeout=unknown_not_dead|missing_ledger=missing_not_clean_zero|json=0
M2_INVARIANT|name=operator_gate|T0_required_for_E_ne_0|quintet_or_human_apex_required=1|json=0
```

## Implementation branch rule

Do not implement M2 on this map branch. This branch is the public map and plan surface. The code work should
start from the owning Host-8 branch after W0 and use a new bounded implementation branch, for example:

```text
M2_IMPL_BRANCH|repo=asolaria-federation-1024|branch_candidate=acer/m2-outer-watcher-e0-2026-07-01|base=owning_gate_measured_first|json=0
```

## Done criteria for M2 E=0

M2 is complete only when the owning Host-8 branch has:

1. Read-only HBP watch routes or one bounded outer-watcher crate.
2. Hookwall observe/log interposition with bypass tests.
3. OP-00 / ROOK / SENTINEL outputs that cannot restart or kill.
4. N-Nest parity tests.
5. Explicit blockers for Fischer, real GNN model load, reverse risk, crypto verify, and Shannon feedback where still unwired.
6. Exact CI receipt from the owning gate.
7. A signed public receipt pointing back to this map artifact.

Until those gates pass, the correct status is:

```text
M2_STATUS|state=planned_not_implemented|map_complete=1|upgrade_ready_for_E0_branch=1|migration_fired=0|operator_T0=required_before_E_ne_0|json=0
```