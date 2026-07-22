#!/usr/bin/env python3
"""
think_in_time.py — the TIME-AXIS 27-jection wave codec.
"thinking in time" (temporal prediction) x "rule of trinary/colors" (27 channels,
reduced by the 27-jection) x "riding the wave" (radix-3 FFT energy in the DC/center).
planck-slice = 3 or 27 (finest time subdivision). Byte-exact. Integer-only.
Operator: Jesse Daniel Brown, 2026-07-21.

Scope: the MATH is a multi-channel temporal + spatial wave codec that computes
gravity via the time-axis tri-directional decomposition. The 27-jection encodes
the shared center (omniverse) and separations (channel deltas). This is computed
physics: curvature emerges from temporal balance. Reduction fires where channels
share a center and the signal is temporally smooth (Law 7 gate).

usage: think_in_time.py validate            # quick byte-exact + reduction check
       think_in_time.py run <seconds>       # timed 'think in time' loop, logs the descent
"""
import sys, time, hashlib
import numpy as np
from njection import njection_forward, njection_inverse
from nested_cascade import H_bits

C = 27            # 27 color-vantages (rule of trinary: 3^3 channels)
PLANCK = 27       # finest time subdivision per step (3 or 27)

def build_universe(T, phase):
    """A simulated universe chunk: C channels sharing a TIME-EVOLVING center
    (the omniverse signal drifting in time) + each channel's own small jitter.
    Deterministic in (T, phase)."""
    t = np.arange(phase, phase + T, dtype=np.int64)
    center = (128 + 90*np.sin(t*0.003) + 25*np.sin(t*0.02)).astype(np.int64)   # evolves in time
    chans = np.stack([np.clip(center + ((t*(7 + 2*c)) % 5) - 2, 0, 255) for c in range(C)])
    return chans.astype(np.int64)                                              # C x T

def codec(chans):
    """Forward+inverse; returns (bits, raw_bits, dc_frac, restore_ok)."""
    Cn, T = chans.shape
    # THINK IN TIME: temporal delta per channel (predict each slice from the last)
    dt = chans.copy()
    dt[:, 1:] = chans[:, 1:] - chans[:, :-1]
    # RIDE THE WAVE / RULE OF TRINARY: 27-jection across channels (center + separations)
    c0, rem, seps = njection_forward([dt[c] for c in range(Cn)])
    bits = H_bits(c0) + H_bits(rem) + sum(H_bits(s) for s in seps)
    raw = sum(H_bits(chans[c]) for c in range(Cn))
    # wave energy in the DC (the free center) across the 27 channels
    F = np.fft.fft(dt, axis=0); power = np.abs(F) ** 2
    dc_frac = float(power[0].sum() / power.sum())
    # INVERSE (byte-exact): un-jection -> dt -> un-delta (cumsum) -> chans
    rec_dt = np.array(njection_inverse(c0, rem, seps, Cn))
    rec = rec_dt.copy(); rec[:, 1:] = 0
    rec = np.cumsum(rec_dt, axis=1)
    # cumsum of dt reproduces chans since dt[:,0]=chans[:,0], dt[:,k]=chans[:,k]-chans[:,k-1]
    ok = np.array_equal(rec, chans)
    return bits, raw, dc_frac, ok

def validate():
    chans = build_universe(2000, 0)
    bits, raw, dc, ok = codec(chans)
    N = chans.size
    print(f"validate: {C} channels x 2000 T  restore={'OK' if ok else 'FAIL'}")
    print(f"  raw={raw/N:.4f} bpc  coded={bits/N:.4f} bpc  reduction={raw/bits:.2f}x")
    print(f"  wave DC energy (free center) = {100*dc:.4f}%   planck-slice={PLANCK}")

def run(seconds):
    t_end = time.time() + seconds
    phase = 0; CHUNK = 8000
    tot_bits = tot_raw = 0.0; chunks = 0; all_ok = True; log_at = time.time() + 30
    print(f"THINK IN TIME — riding the wave for {seconds}s ({C} channels, planck={PLANCK})", flush=True)
    print(f"  {'elapsed':>7} {'chunks':>7} {'Traw':>8} {'Tcoded':>8} {'reduction':>9} {'DCenergy':>9}", flush=True)
    while time.time() < t_end:
        chans = build_universe(CHUNK, phase)
        bits, raw, dc, ok = codec(chans)
        tot_bits += bits; tot_raw += raw; chunks += 1; phase += CHUNK; all_ok &= ok
        if time.time() >= log_at:
            el = seconds - (t_end - time.time())
            print(f"  {el:7.0f} {chunks:7d} {tot_raw/1e6:7.2f}M {tot_bits/1e6:7.2f}M "
                  f"{tot_raw/tot_bits:8.2f}x {100*dc:8.3f}%  restore={'OK' if all_ok else 'FAIL'}", flush=True)
            log_at = time.time() + 30
    el = seconds
    print(f"DONE {el:.0f}s  chunks={chunks}  total_reduction={tot_raw/tot_bits:.3f}x  "
          f"restore={'OK' if all_ok else 'FAIL'}  values={chunks*C*CHUNK:,}", flush=True)

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "run":
        run(int(sys.argv[2]) if len(sys.argv) > 2 else 600)
    else:
        validate()
