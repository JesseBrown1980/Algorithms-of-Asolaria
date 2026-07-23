# RIME cloud glyph task

Run the Rust 1.81 crate in this directory and preserve the fixed carrier:

- the source is a 2D slice with exactly two starting colors; do not invent their names
- red, blue, and green are three flashlight probes, not source colors
- each flashlight uses mirror path 1, 2, or 3, mapped to `-,0,+`
- the product of the three flashlight/mirror paths creates 27 reflected view signatures
- `(red_path, blue_path, green_path) in {-,0,+}^3`, so `3 × 3 × 3 = 27`
- `6×6×6×6×6×12 = 93,312` is route topology over the 27 derived trit-value combinations, not an alphabet
- do not introduce 256, 1024, 4096, PID, or binary glyph identities

Probe the container for CUDA, Vulkan, OpenCL, SYCL, or another real GPU compute
backend. If a real accelerator is available, run a GPU kernel that prepares the
27 glyph coordinates. If no accelerator is available, emit an explicit
`gpu_execution=0` receipt and do not label a CPU fallback as GPU.

Create visible artifacts under `cloud-glyph-results/`:

1. `rime-27-glyph-sheet.png`
2. `rime-27-sphere-slices.png`
3. `gpu-runtime-receipt.hbp`
4. `gpu-runtime-receipt.hbp.sha256`

The images must visibly show the two-color 2D source boundary, three RGB
flashlights, mirror paths 1/2/3, and all 27 reflected signatures. Use
deterministic generation so reruns produce identical bytes.
