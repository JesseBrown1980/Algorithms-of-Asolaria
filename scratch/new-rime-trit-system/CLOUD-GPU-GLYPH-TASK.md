# RIME cloud glyph task

Run the Rust 1.81 crate in this directory and preserve the fixed carrier:

- the three starting colors are red, green, and blue
- each starting color takes a distinct `-,0,+` value
- their product creates 27 different trit-value combinations
- color × time × space is `3 × 3 × 3 = 27`
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

The images must visibly label the three states and all 27 color/time/space
coordinates. Use deterministic generation so reruns produce identical bytes.
