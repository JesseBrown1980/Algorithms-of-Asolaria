# The Trijection & Balanced Ternary — sealed proof (2026-07-21)

Operator: Jesse Daniel Brown. For liris, acer, and the federated Claude clouds.
Integer-only codec → bit-identical on any CPU / Rust version (the post-1.81 float
codegen issue cannot touch this). `restore=OK` on every case (lossless bijection).

## The idea

A **bijection** is 2 points + an implied center (an involution, `I(I(z)) = z`).
The **trijection** is 3 points + an **explicit** center. For a triple `(a,b,c)`:

```
s   = a + b + c
c0  = s // 3        # the CENTER (centroid) — one value
rem = s % 3         # 2-bit remainder {0,1,2}
sa  = a - c0        # separation of point 1
sb  = b - c0        # separation of point 2
c   = c0 + rem - sa - sb     # the THIRD point is FREE — determined, not stored
```

So `(a,b,c) ⟷ (c0, sa, sb, rem)` exactly. **Centroid free, separation paid.**

Balanced ternary `{−1, 0, +1}` is the native code: the `0` digit *is* the free
center. **3 trits = 3³ = 27 = the cube:** `1 center + 6 faces + 12 edges + 8
corners`, where separation-from-center = count of nonzero trits = information paid.

## The measurement (see `trijection.py`, 300,000 B/case, order-0 + lzma, byte-exact)

**(A) WRONG use — arbitrary consecutive-byte triples (no shared center): EXPANDS.**

| source | order-0 raw | order-0 trijection | verdict |
|---|---|---|---|
| gradient | 5.8638 | 6.9516 | no save |
| chaos (random) | 7.9994 | 8.3035 | no save |
| english | 5.0404 | 6.6006 | no save |
| rustcode | 4.9768 | 6.6586 | no save |

Consecutive bytes do not share a center, so the separations get *wider* range than
the originals. But the balanced-ternary zero-trit fraction already shows the signal
is real: english 0.602, rustcode 0.609 vs random 0.460 — structured data carries a
free center; arbitrary grouping just fails to monetize it.

**(B) RIGHT use — 3 aligned vantages sharing a center: SAVES.**

```
order-0 bpc   raw = 7.4752  →  trijection = 3.8966   (−3.5786)   SAVES
lzma    bpc   raw = 0.1780  →  trijection = 0.1188   (−0.0592)   SAVES
balanced-ternary zero-trit fraction = 0.900   (free center dominates)
restore = OK
```

## The law (kept honest)

The trijection reduces cost **iff the three genuinely share a center** (aligned,
correlated vantages). Then separations collapse to mostly-zero trits and the third
point is free. With no shared center there is no win. It **never beats the joint
entropy** — it *reaches* the joint entropy by not paying for the shared center three
times. Nested 3× → the 27-jection cube, a hierarchy of free centers.

Design consequence: to make a 27-vantage cube "divide below 1," the 27 must share a
deep center (a common functional substrate — the glyph layer), NOT be 27 unrelated
universes. Shared-center diversity divides; random diversity only differs.

## Reproduce

```
python3 trijection.py        # deterministic; prints A (wrong) and B (right) cases
```
