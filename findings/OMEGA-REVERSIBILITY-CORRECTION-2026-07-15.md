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

## What survives, what changes

The qualitative interpretation stands: per-cube spread of ~1.8% is still small enough
that the eight views approach comparable gross learning power at 800 passes, while the
eight distinct view-result digests prove the learned languages are not identical
("isotropy of POWER, not redundancy of CONTENT"). Only the quantitative sentence
changes: **0.18% → 1.8427135%**.

Downstream documents carrying the same figure must apply the same correction before
promotion — known carrier: HYPER-BECHS PR #40 (its Markdown and HBP both state 0.18%).
