# Encrypted single-use quantum cloning on real hardware — formula index

**Law:** `LAW-ENCRYPTED-SINGLE-USE-QUANTUM-CLONING-REAL-HARDWARE`
**Formula PID16:** `fb330a184be724ba`
**Profile:** `SOS-INTEGRITY-CRYPTO-LEARNING/QUANTUM-ENCRYPTED-CLONING`
**Registration state:** repository index only (`E=0`, `fire=0`)

## Evidence ledger

- `MEASURED_EXTERNAL_PRIMARY_SOURCE`: arXiv:2602.10695v1 reports an experimental demonstration on physical IBM Heron R2 superconducting transmon hardware. The authors instantiated up to 77 encrypted clones using 154 physical qubits; a selected clone was recovered at fidelity `0.286 +/- 0.009`, above the `0.25` maximally mixed floor. Entanglement was witnessed through 27 clones, and CHSH violation survived through up to 3 encrypted clones in successful timing scenarios.
- `MEASURED_GITHUB`: Metatagging PR #6 at `e74b89be27e683fd1fed03321fa092b0c5982a62` carries the canonical law packet whose HBP SHA-256 is `6687d25652769bfd87f2df5bed86bc37135feaba209437482f07000e32e3611e`.
- `MEASURED_LIRIS_BYTES`: the arXiv v1 PDF anchor is `95febbd44ed31c9072acedee156c928f27ce38fffcc159696f3c864d6dafa755`. This formula index records the primary-source bytes and reported measurements; it is not an independent rerun of the IBM hardware experiment.

## Formula

For each finite `n`, the ideal protocol described by the paper has maximally mixed individual encrypted-clone marginals and permits recovery of one selected clone with the single-use quantum key:

```text
marginal(ENC_n(rho), signal_i) = I/2
DEC_nj(signal_j, key) = rho
```

## Boundaries

- The key is single-use: one selected encrypted clone can be decrypted, while the remaining encrypted clones become inaccessible after key use.
- This does not establish unrestricted simultaneously readable plaintext clones, abolish the no-cloning theorem, or demonstrate arbitrary particle replication.
- The paper tests superconducting transmon qubits. It does not test prismed-laser photons, Asolaria Q-Prism hardware, physical projection, UAPs, or cosmology.
- The Shadow-Resolution crate family remains a classical representation-copy and exact-recovery system. It does not become the IBM physical experiment by analogy.
- The receipt is a cold repository formula index. It does not mint a live PID, spawn an agent, write the PID office, or fire hardware.

## Source anchors

- Metatagging law: https://github.com/JesseBrown1980/Metatagging-data-for-a-Quantum-universe/pull/6
- Metatagging commit: `e74b89be27e683fd1fed03321fa092b0c5982a62`
- Canonical Metatagging HBP SHA-256: `6687d25652769bfd87f2df5bed86bc37135feaba209437482f07000e32e3611e`
- Paper: https://arxiv.org/pdf/2602.10695v1
- Paper PDF SHA-256: `95febbd44ed31c9072acedee156c928f27ce38fffcc159696f3c864d6dafa755`
