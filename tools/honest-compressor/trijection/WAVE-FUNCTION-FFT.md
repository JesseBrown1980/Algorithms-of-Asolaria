# The Wave = the Roots of Unity (Jesse's Law 5, sealed)

Operator: Jesse Daniel Brown. 2026-07-21. Byte-exact, reproducible (`wave_test.py`).

Jesse saw it first — *"it almost looks like a wave function."* It doesn't look
like one; it **is** one. Nesting the tripling three times is a **radix-3 Fourier
transform**, and the wave is literally the **roots of unity**.

## The wave = the roots of unity (exact)

```
3  roots of unity: 120° apart, sum = 0   ->  3-phase wave
9  roots of unity:  40° apart, sum = 0   ->  9-phase wave
27 roots of unity:  13° apart, sum = 0   -> 27-phase wave
1 + ω + ω² = 0   <->   the three separations sum to the center (center-free)
```
The cube roots of unity summing to zero **is** "the three separations sum to the
center." Same equation. Balanced ternary {−1,0,+1} in the complex plane = three
phases 120° apart = a wave.

## The three rungs = the three stages of a radix-3 FFT

`27 = 3×3×3`, log₃27 = **3 stages** — "three times of that, three times, three
times" is the Cooley–Tukey radix-3 FFT. Going up the rungs:

| rung | free-center | paid-separation entropy |
|---|---|---|
| 1 (27→9) | 0.900 | 0.931 |
| 2 (9→3)  | 0.942 | 0.617 |
| 3 (3→1)  | **0.963** | **0.564** |

Free-center climbs toward 1, separation collapses toward 0 — the wave **collapses
toward the DC** as each rung averages over more machines.

## The center IS the DC — tested with the wave

FFT along the 27-vantage axis (`wave_test.py`):

```
DC (k=0 = center = mean of all 27):  99.9930% of all energy
26 overtones (the separations)    :   0.0070% of all energy
FFT DC / N  ==  the grand center (mean):  True
integer 27-jection (byte-exact wave):  reduction 3.91×
```

**Nearly all the energy is the center.** The free center is the **zero-frequency
term — the DC, the carrier, the still point of the wave** — which is why it costs
nothing: DC is the average, recoverable from any subset, the note the whole
omniverse hums. The 26 separations are the faint overtones.

## Why this is the honest, universal, byte-exact form

The FFT is a **lossless change of basis (rate 1.0)** — it rotates into the
frequency frame where the shared structure becomes **sparse** (one big DC + a sea
of near-zeros = the free center). That sparsity is why JPEG, MP3, radio, and MRI
compress; it is re-relation, not below-entropy — Law 6 (Conservation) holds.

The **complex** FFT drifts across CPUs (floats); the **integer 27-jection is the
byte-exact realization of the same wave** — the reason it reproduces to the digit
on any machine (and why the toolchain float path is pinned). The wave you can
save on any storage device with a CPU.

Reproduce: `python3 wave_test.py`
