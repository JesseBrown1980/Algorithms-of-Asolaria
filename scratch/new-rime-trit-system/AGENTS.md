# RIME Trit Build Invariants

- The glyph basis starts with exactly three parent colors: red, green, and blue.
- Each parent color independently carries one trit in `{-,0,+}`.
- Their Cartesian product produces 27 distinct derived values:
  `(red_trit, green_trit, blue_trit) in {-,0,+}^3`.
- Never describe the result as 27 starting colors. It is 3 parent colors branching to 27 trit tuples.
- Time, space, gradient, calculation time, play time, bits, and storage are separately measured trit-valued pass dimensions; do not relabel the RGB tuple as color/time/space.
- Do not introduce 256, 1024, 4096, PID, or binary identities into the internal RIME glyph alphabet.
- The `6x6x6x6x6x12 = 93,312` Deep Wave number is route topology over the fixed trit carrier, not glyph-alphabet growth.
- Keep GPU execution evidence explicit. A cloud agent run without an exposed GPU is a valid CPU artifact run with `gpu_execution=0`, never a GPU-kernel claim.
