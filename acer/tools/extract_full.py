#!/usr/bin/env python3
# extract_full.py — READ-ONLY contiguous (NoFatChain) full-file extractor for USB-SOVLINUX-2TB.
# Fixes the --extract-spec 1-cluster limit: these runtime dumps are contiguous, so read the
# whole cluster run (first .. first+ceil(size/cluster_bytes)-1) with aligned device reads.
# usage: python extract_full.py <out_dir> "first:size:relname" ["first:size:relname" ...]
import sys, os, hashlib
DEV = r'\\.\PHYSICALDRIVE2'
PART_LBA = 2048      # MBR part1 start (LBA)
HEAP = 34816         # cluster_heap_offset_sectors (from part start)
BPS = 512            # bytes/sector
SPC = 256            # sectors/cluster
CB = BPS * SPC       # 131072 cluster bytes
BLK = 64 * CB        # 8 MiB aligned read block
def clu_off(n): return (PART_LBA + HEAP + (n - 2) * SPC) * BPS
def extract(first, size, dest):
    nclu = (size + CB - 1) // CB
    total = nclu * CB
    off = clu_off(first)
    buf = bytearray()
    with open(DEV, 'rb', buffering=0) as f:
        f.seek(off)
        while len(buf) < total:
            blk = f.read(min(BLK, total - len(buf)))
            if not blk: break
            buf += blk
    data = bytes(buf[:size])
    with open(dest, 'wb') as o: o.write(data)
    return len(data), hashlib.sha256(data).hexdigest()[:16]
out_dir = sys.argv[1]; os.makedirs(out_dir, exist_ok=True)
for spec in sys.argv[2:]:
    c, s, name = spec.split(':', 2)
    wrote, sha16 = extract(int(c), int(s), os.path.join(out_dir, name))
    print(f'{name}  wrote={wrote}  want={s}  sha16={sha16}  {"OK" if str(wrote)==s else "SHORT"}')
