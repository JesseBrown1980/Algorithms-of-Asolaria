# Bridge receipt — third-seat landing + independent verification (2026-07-19)

## What landed
- 20 compression patches (900ae60..bf8300e) + merge 3effec0 → `claude/repo-movement-ifzeru`
- 1 kernel patch → `asolaria-os` branch `claude/mtp-watcher-trio` (tip 4adfad9)
- Payload: asolaria-export.tar.gz, sha256 `6c990446…b483698` — verified byte-exact,
  all 26 files matched MANIFEST.txt sha256s; all patches content-reviewed before apply.

## Independent third-seat verification (this cloud seat, distinct from the Cowork container)
- Corpus: enwik8 first 1,000,000 bytes, sha256 `369b6889…9552cad` (matches container's slice)
- Built `rust/cm3ti.rs` from the *pushed* code (rustc -O), ran `cm3ti slice1m.bin 7`:

```
payload=242655  bpc_total=1.9412(payload-only)  restore=OK  comp_sha=101c86ae05358c32
```

- **comp_sha matches the manifest's determinism anchor exactly.** Same bytes on a third,
  fully independent environment. Cross-seat determinism: container x86_64 = container
  aarch64 = this cloud seat. The instrument is real.

## Still open (to land when sealed by the container)
- combo (sector+URL) at 100 MB — crown challenger
- 6/12/24/48 sector-refinement sweep at 10 MB+ (1 MB optimum measured at 24: 2.0785)
