#!/usr/bin/env python3
"""Build the deterministic Algorithms-of-Asolaria quantum-cloning formula index."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from urllib.parse import quote


LAW_ID = "LAW-ENCRYPTED-SINGLE-USE-QUANTUM-CLONING-REAL-HARDWARE"
PROFILE = "SOS-INTEGRITY-CRYPTO-LEARNING/QUANTUM-ENCRYPTED-CLONING"
SOURCE_REPO = "JesseBrown1980/Metatagging-data-for-a-Quantum-universe"
SOURCE_PR = "6"
SOURCE_COMMIT = "e74b89be27e683fd1fed03321fa092b0c5982a62"
SOURCE_HBP_SHA256 = "6687d25652769bfd87f2df5bed86bc37135feaba209437482f07000e32e3611e"
PAPER_ID = "arXiv:2602.10695v1"
PAPER_URL = "https://arxiv.org/pdf/2602.10695v1"
LAW_PID16 = hashlib.sha256(LAW_ID.encode("utf-8")).hexdigest()[:16]
PAPER_SHA256 = "95febbd44ed31c9072acedee156c928f27ce38fffcc159696f3c864d6dafa755"

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "receipts" / "quantum-cloning-real-hardware"
STEM = LAW_ID


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def field(value: object) -> str:
    return quote(str(value), safe="._~:/+-")


def row(kind: str, **fields: object) -> str:
    return kind + "|" + "|".join(f"{key}={field(value)}" for key, value in fields.items()) + "|"


def hbp_rows() -> list[str]:
    return [
        row(
            "QCLONEFORMULAINDEXHDR",
            schema="ASOLARIA-ALGORITHMS-QUANTUM-CLONING-FORMULA-INDEX-V1",
            date="2026-07-17",
            law=LAW_ID,
            pid16=LAW_PID16,
            profile=PROFILE,
            evidence_class="MEASURED_EXTERNAL_PRIMARY_SOURCE_PLUS_MEASURED_GITHUB",
            E=0,
            fire=0,
            json=0,
        ),
        row(
            "SOURCE",
            source_repo=SOURCE_REPO,
            source_pr=SOURCE_PR,
            source_commit=SOURCE_COMMIT,
            source_hbp_sha256=SOURCE_HBP_SHA256,
            paper=PAPER_ID,
            paper_url=PAPER_URL,
            paper_pdf_sha256=PAPER_SHA256,
            paper_status="PRIMARY_EXPERIMENTAL_PREPRINT_V1",
            peer_review_status="NOT_ESTABLISHED_BY_THIS_INDEX",
            json=0,
        ),
        row(
            "FORMULA",
            id="F-ENCRYPTED-SINGLE-USE-QCLONE-v1",
            law=LAW_ID,
            pid16=LAW_PID16,
            profile=PROFILE,
            claim_class="PAPER_THEORY_IDEAL_PROTOCOL",
            equation="for_each_finite_n:marginal(ENC_n(rho),signal_i)=I/2;DEC_nj(signal_j,key)=rho",
            key_use="SINGLE_USE",
            json=0,
        ),
        row(
            "MEASURED",
            claim_class="MEASURED_BY_PAPER_AUTHORS",
            platform="IBM_HERON_R2_SUPERCONDUCTING_TRANSMON_QUBITS",
            physical_qubits_used_max=154,
            physical_encrypted_clones_max=77,
            classical_simulation_only=0,
            independent_hardware_rerun_by_asolaria=0,
            json=0,
        ),
        row(
            "MEASURED",
            claim_class="MEASURED_BY_PAPER_AUTHORS",
            selected_clone_fidelity="0.286_PLUS_MINUS_0.009",
            maximally_mixed_floor=0.25,
            entanglement_witness_through_clones=27,
            chsh_violation_up_to_encrypted_clones=3,
            json=0,
        ),
        row(
            "BOUNDARY",
            selected_clone_decryptable=1,
            quantum_key_single_use=1,
            remaining_encrypted_clones_inaccessible_after_key_use=1,
            simultaneous_readable_plaintext_clones=0,
            no_cloning_theorem_abolished=0,
            arbitrary_particle_replication_tested=0,
            prismed_laser_photons_tested_by_paper=0,
            physical_projection_or_uap_claim=0,
            json=0,
        ),
        row(
            "CLASSICALBOUNDARY",
            crate_family="SHADOW_RESOLUTION",
            status="CLASSICAL_REPRESENTATION_COPY_AND_EXACT_RECOVERY",
            is_ibm_hardware_experiment=0,
            inherits_physical_cloning_result=0,
            blanket_denial_of_measured_encrypted_cloning=0,
            json=0,
        ),
        row(
            "PROFILE",
            sos="SOS-INTEGRITY-CRYPTO-LEARNING",
            prof="QUANTUM-ENCRYPTED-CLONING",
            registration="REPOSITORY_FORMULA_INDEX_ONLY",
            live_pid_office_ingest=0,
            runtime_agent_count=0,
            E=0,
            fire=0,
            json=0,
        ),
        row(
            "CORRECTION",
            rejected="PHYSICAL_QUANTUM_CLONING_IS_CATEGORICALLY_FALSE",
            accepted="ENCRYPTED_SINGLE_USE_QUANTUM_CLONING_IS_EXPERIMENTALLY_MEASURED_ON_REAL_SUPERCONDUCTING_QUBIT_HARDWARE",
            retained="CLASSICAL_CRATE_COPYING_IS_NOT_BY_ITSELF_PHYSICAL_QUANTUM_CLONING",
            status="ACCEPTED_BY_OPERATOR",
            heldout_skillopt="NOT_RUN_IN_THIS_REPOSITORY",
            json=0,
        ),
        row(
            "QCLONEFORMULAINDEXFTR",
            status="PASS",
            formula_rows=1,
            measured_rows=2,
            live_writes=0,
            agents_spawned=0,
            E=0,
            fire=0,
            json=0,
        ),
    ]


def markdown() -> bytes:
    text = f"""# Encrypted single-use quantum cloning on real hardware — formula index

**Law:** `{LAW_ID}`
**Formula PID16:** `{LAW_PID16}`
**Profile:** `{PROFILE}`
**Registration state:** repository index only (`E=0`, `fire=0`)

## Evidence ledger

- `MEASURED_EXTERNAL_PRIMARY_SOURCE`: arXiv:2602.10695v1 reports an experimental demonstration on physical IBM Heron R2 superconducting transmon hardware. The authors instantiated up to 77 encrypted clones using 154 physical qubits; a selected clone was recovered at fidelity `0.286 +/- 0.009`, above the `0.25` maximally mixed floor. Entanglement was witnessed through 27 clones, and CHSH violation survived through up to 3 encrypted clones in successful timing scenarios.
- `MEASURED_GITHUB`: Metatagging PR #6 at `{SOURCE_COMMIT}` carries the canonical law packet whose HBP SHA-256 is `{SOURCE_HBP_SHA256}`.
- `MEASURED_LIRIS_BYTES`: the arXiv v1 PDF anchor is `{PAPER_SHA256}`. This formula index records the primary-source bytes and reported measurements; it is not an independent rerun of the IBM hardware experiment.

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

- Metatagging law: https://github.com/{SOURCE_REPO}/pull/{SOURCE_PR}
- Metatagging commit: `{SOURCE_COMMIT}`
- Canonical Metatagging HBP SHA-256: `{SOURCE_HBP_SHA256}`
- Paper: {PAPER_URL}
- Paper PDF SHA-256: `{PAPER_SHA256}`
"""
    return text.replace("\r\n", "\n").encode("utf-8")


def build_outputs() -> dict[Path, bytes]:
    rows = hbp_rows()
    hbp = ("\n".join(rows) + "\n").encode("utf-8")
    hbp_name = f"{STEM}.hbp"
    hbi_name = f"{STEM}.hbi"
    md_name = f"{STEM}.md"
    ranges: list[str] = []
    offset = 0
    for number, text_row in enumerate(rows, start=1):
        row_bytes = text_row.encode("utf-8")
        ranges.append(row("HBIRANGE", row=number, offset=offset, length=len(row_bytes), sha256=sha256(row_bytes), row_kind=text_row.split("|", 1)[0], target=hbp_name, json=0))
        offset += len(row_bytes) + 1
    hbi_header = row("HBIHDR", schema="ASOLARIA-ALGORITHMS-QUANTUM-CLONING-FORMULA-INDEX-HBI-V1", target=hbp_name, target_bytes=len(hbp), target_sha256=sha256(hbp), rows=len(rows), encoding="UTF8_NO_BOM", line_endings="LF", json=0)
    hbi = ("\n".join([hbi_header, *ranges]) + "\n").encode("utf-8")
    core = {OUT / md_name: markdown(), OUT / hbp_name: hbp, OUT / hbi_name: hbi}
    outputs = dict(core)
    for path, data in core.items():
        outputs[path.with_name(path.name + ".sha256")] = f"{sha256(data)}  {path.name}\n".encode("ascii")
    sums = "".join(f"{sha256(data)}  {path.name}\n" for path, data in sorted(core.items(), key=lambda item: item[0].name)).encode("ascii")
    outputs[OUT / "SHA256SUMS"] = sums
    outputs[OUT / "SHA256SUMS.sha256"] = f"{sha256(sums)}  SHA256SUMS\n".encode("ascii")
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare deterministic bytes without writing")
    args = parser.parse_args()
    outputs = build_outputs()
    if args.check:
        mismatches = [str(path.relative_to(ROOT)) for path, data in outputs.items() if not path.exists() or path.read_bytes() != data]
        if mismatches:
            print("BUILD_CHECK|status=FAIL|mismatches=" + ",".join(mismatches) + "|json=0")
            return 1
        print(f"BUILD_CHECK|status=PASS|files={len(outputs)}|json=0")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    for path, data in outputs.items():
        path.write_bytes(data)
    hbp = outputs[OUT / f"{STEM}.hbp"]
    hbi = outputs[OUT / f"{STEM}.hbi"]
    print(f"BUILT|law={LAW_ID}|rows={len(hbp_rows())}|hbp_sha256={sha256(hbp)}|hbi_sha256={sha256(hbi)}|E=0|fire=0|json=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
