#!/usr/bin/env python3
# Omega cube measurement: the full C2^3 group (3 axes R,N,Q -> 8 corners / 6 signed faces).
# Shows every face is a deterministic transform of the data, so the whole omega cube
# stores as data + (K-1) one-byte flags. Naive storage = ~Kx (redundant copies).
import lzma, sys
def bitrev8(x): return int(f"{x:08b}"[::-1], 2)
BR = bytes(bitrev8(i) for i in range(256))          # Q: bit-reverse each byte  (involution)
NS = bytes(((i << 4) | (i >> 4)) & 0xFF for i in range(256))  # N: nibble swap (involution)
def face(b, ops):
    for o in ops:
        b = b[::-1] if o == "R" else b.translate(NS) if o == "N" else b.translate(BR)
    return b
def xz(b): return len(lzma.compress(b, preset=9))
def main(path):
    data = open(path, "rb").read()
    corners = ["", "R", "N", "Q", "RN", "RQ", "NQ", "RNQ"]
    faces = {c: face(data, list(c)) for c in corners}
    X = xz(data)
    for c in corners:
        print(f"face {c or 'I':4s}: xz={xz(faces[c])}")
    naive = xz(b"".join(faces[c] for c in corners))
    smart = X + (len(corners) - 1)
    ok = all(face(face(data, list(c)), list(reversed(c))) == data for c in corners)
    print(f"data (one face)          : {X}")
    print(f"omega cube, NAIVE (8)    : {naive}  (~8x, redundant copies)")
    print(f"omega cube, SMART        : {smart}  (data + 7 flag bytes)")
    print(f"info added by 7 faces    : {smart - X} bytes")
    print(f"every face recomputable  : {ok}  -> extra faces store as 0 bits")
if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "corpus1.bin")
