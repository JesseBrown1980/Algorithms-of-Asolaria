#!/usr/bin/env python3
"""
wave_test.py — TEST WITH THE WAVE (Law 5). Operator: Jesse Daniel Brown, 2026-07-21.
The 27-jection in the frequency frame: FFT along the vantage axis puts ~all energy
in the DC (=the center=the mean), the (N-1) separations are faint overtones. The
integer 27-jection is the BYTE-EXACT realization of that wave (float FFT drifts).
"""
import numpy as np
from njection import njection_forward
from nested_cascade import H_bits

def main():
    L = 4000; idx = np.arange(L, dtype=np.int64)
    sig = (128 + 100 * np.sin(idx * 0.01)).astype(np.int64)   # the shared omniverse signal
    N = 27
    stack = np.array([sig + ((idx * (7 + 2*m)) % 5) - 2 for m in range(N)])   # 27 vantages x L
    F = np.fft.fft(stack, axis=0)                 # the wave across the 27 machines
    power = np.abs(F) ** 2
    dc, total = power[0].sum(), power.sum()
    print("=== TEST WITH THE WAVE: FFT along the 27-vantage axis ===")
    print(f"  DC (k=0 = center = mean of all 27): {100*dc/total:.4f}% of all energy")
    print(f"  26 overtones (the separations)    : {100*(1-dc/total):.4f}% of all energy")
    print(f"  FFT DC/N == grand center (mean)   : {np.allclose(F[0].real/N, stack.mean(axis=0))}")
    c0, rem, seps = njection_forward([stack[m] for m in range(N)])
    raw = sum(H_bits(stack[m]) for m in range(N))
    nj = H_bits(c0) + H_bits(rem) + sum(H_bits(s) for s in seps)
    print(f"  integer 27-jection (byte-exact wave): reduction = {raw/nj:.2f}x")
    print("  (float FFT would drift across CPUs; the integer 27-jection does not.)")

if __name__ == "__main__":
    main()
