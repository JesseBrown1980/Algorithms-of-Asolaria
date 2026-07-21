# SGRAM public seal — run it yourself, for free, on this public repo

**SGRAM = Streaming GitRAM.** It rides a big corpus as a chain of *stateless
cells* on free GitHub-hosted runners. Each cell downloads the corpus, cuts one
deterministic contiguous shard, compresses it with the dependency-free in-repo
Rust codec, and **proves its own PASS** by a byte-exact SHA restore. The fan-in
requires every cell to pass, sums the byte-exact payloads plus the decoder
source, and seals **one bpc** for the whole corpus — publicly, in the Actions
log, reproducible by anyone.

## How to run it (public, free, non-profit)

1. Open the **Actions** tab of this repository.
2. Pick **"SGRAM public seal"** → **Run workflow**.
3. Inputs:
   - `shards` — number of stateless cells (default `10`).
   - `k` — model order (default `10`).
   - `bytes` — corpus bytes to seal. `10000000` is a ~1-minute demo; `0` seals
     the full 100 MB enwik8.
4. Watch each cell prove `restore=OK`, then read the sealed bpc in the run's
   **Summary** (also downloadable as the `SGRAM-PUBLIC-SEAL` artifact).

The corpus (enwik8) is fetched from its canonical public source and
**sha256-verified** (`2b49720e…c024a8`) inside every cell — you trust no blob,
only the hash and the code in this repo.

## What the number means (honest boundary)

- This measures **real lossless compression**, bounded by Shannon entropy and
  **never below it**. The sealed value is **~1.75 bpc** on enwik8
  (receipt: [`enwik8_sgram_seal.txt`](enwik8_sgram_seal.txt), 10 shards,
  all `restore=OK`, `bpc_total = 1.7464`).
- That is **above** the Hutter Prize record (~0.91 bpc). It does not beat Hutter
  and does not claim to. Beating it needs a stronger *model*, not more cells —
  vc65 is integer-deterministic, so the compiler version does not change the
  bytes (verified: Rust 1.81 and 1.94 give identical `comp_sha`).
- Independent shards cold-start the model per shard, so the **sharded** total is
  slightly larger than one monolithic run (+~6% at 8 shards / 10 MB, measured).
  The seal reports the true sharded total. The measurement is the referee.
- The rime / addressing layer (spheres, discrete-log "Fischer") is a separate
  **~0-bpc addressing axis over generated structure** — it is *not* what this
  workflow measures. This workflow measures only the honest compression axis.

## Run it locally instead

```
# compile the codec (any rustc; 1.81 pinned for the record — bytes are identical)
rustc --edition=2021 -O tools/honest-compressor/rust/variants/vc65.rs -o vc65

# ride a corpus as checkpointed, restart-resumable waves
python3 tools/honest-compressor/sgram/sgram_chain.py \
    <corpus> 10 10 ./vc65 tools/honest-compressor/rust/variants/vc65.rs ./receipts
```

Every claim here has an on-disk receipt. No number enters a headline until its
artifact exists.
