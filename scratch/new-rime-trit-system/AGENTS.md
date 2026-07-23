# RIME Trit Build Invariants

Status: `ACCEPTED_BY_OPERATOR`. The canonical SkillOpt scenario file is not present in this checkout, so this is not `VALIDATION_ACCEPTED`. The crate-local held-out regression is `trit::tests::two_color_2d_source_produces_27_probe_signatures`.

`REJECTED_BUFFER`: the prior model "three parent RGB colors branch directly to 27 color glyphs" merged the source plane with the observation apparatus and must not be restored.

- The source begins as a 2D slice with exactly two starting colors. Keep their actual names as operator inputs unless Jesse names them explicitly.
- Red, blue, and green are three independent flashlight probes, not the starting colors.
- Each flashlight is observed through mirror paths 1, 2, and 3, mapped computationally to `{-,0,+}`.
- Their Cartesian product produces 27 distinct reflected view signatures:
  `(red_path, blue_path, green_path) in {-,0,+}^3`.
- Never describe the result as 27 starting colors or three parent colors. It is a two-color 2D source observed by three RGB flashlight/mirror paths.
- Anti and anti-anti verses are the operator's interpretation of those reflected views. Keep any physical-universe mapping `UNVERIFIED` until separately measured.
- Time, space, gradient, calculation time, play time, bits, and storage are separately measured trit-valued pass dimensions; do not relabel the flashlight tuple as color/time/space.
- Do not introduce 256, 1024, 4096, PID, or binary identities into the internal RIME glyph alphabet.
- The `6x6x6x6x6x12 = 93,312` Deep Wave number is route topology over the fixed trit carrier, not glyph-alphabet growth.
- Keep GPU execution evidence explicit. A cloud agent run without an exposed GPU is a valid CPU artifact run with `gpu_execution=0`, never a GPU-kernel claim.
