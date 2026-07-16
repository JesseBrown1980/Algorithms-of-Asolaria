# Correction — repo-orbit mean relative spread is 1.8427135%, not ~0.18%

**Seat:** LIRIS · 2026-07-15 · MEASURED (recomputed from the sealed artifact)

The findings in `OMEGA-REVERSIBILITY-LIRIS-2026-07-14.md`/`.hbp` state the Asolaria
repo-orbit mean relative spread as **≈ 0.18%**. That number carries a factor-of-ten
error. The sealed receipts themselves are NOT modified (receipt discipline: corrections
are addenda, never mutations); this file is the correction of record.

## The exact value

The sealed comparison artifact (`repo-orbit-comparison`, HYPER-BECHS run 29357558667,
`REPO-ORBIT-COMPARISON.hbp`) carries the exact rational on its `PVSPREAD` row. It
evaluates to:

    mean relative spread = 0.01842713548978976 = 1.8427135%

Independently recomputed 2026-07-15 from the raw 27 `PVCUBE` rows using the comparator's
own formula — per cube `s_c = (max_v G_{c,v} − min_v G_{c,v}) / mean_v G_{c,v}`, averaged
over the 27 cubes — the result matches the sealed fraction exactly:

    recomputed from gains          : 0.01842713548978976
    mean of per-row sealed spreads : 0.01842713548978976
    PVSPREAD sealed exact fraction : 0.01842713548978976

## Bidirectional verification (added 2026-07-15, operator-directed)

The first pass above only confirmed the comparison artifact against itself. The reverse
directions were then run from the raw side:

1. **Raw receipts → comparison (216/216 exact).** All eight banked view artifacts
   (`repo-i` … `repo-r`, run 29357558667) were downloaded; per-cube gains were re-derived
   by summing the raw `MERGE|…|net_gain=` rows in each view's
   `FIRST-FLOOR-RESULT.hbp`. All 27 cubes × 8 views = 216 values match the comparison
   artifact's `PVCUBE` rows exactly. The comparison is faithful to the raw data.
2. **Omega from raw bytes (exact).** Fresh SHA-256 of each view's receipt matches the
   sealed leaf list, and `omega = SHA-256(sorted "view:sha" lines, LF)` recomputes to
   `cc0c4ee3…96951b57` — byte-exact against the sealed `REPOOMEGA` row.
3. **No honest origin for 0.18%.** A battery of alternative statistics on the verified
   data was tested; none yields ≈0.18% (closest: cohort pop-stdev/mean 0.2139%, sample
   0.2286%, mean best-vs-second gap 0.1353%, mean spread/8 0.2303%). The 0.18% figure is
   therefore not a different-but-valid statistic — it is a decimal-place slip of
   1.8427135%.

Method note for the record: the first attempt at check (1) reported 80 phantom
mismatches because the checker matched `q_gain=` as a substring of `nq_gain=` (and
`r_gain=` inside `nqr_gain=`). Pipe-delimited HBP fields must be parsed
delimiter-anchored (`|field=`), never by bare substring — the same defect family as the
location-agnostic recursive-find gate corrected in the GitRAM floor-one lane.

## What survives, what changes

The qualitative interpretation stands: per-cube spread of ~1.8% is still small enough
that the eight views approach comparable gross learning power at 800 passes, while the
eight distinct view-result digests prove the learned languages are not identical
("isotropy of POWER, not redundancy of CONTENT"). Only the quantitative sentence
changes: **0.18% → 1.8427135%**.

Downstream documents carrying the same figure must apply the same correction before
promotion — known carrier: HYPER-BECHS PR #40 (its Markdown and HBP both state 0.18%).
