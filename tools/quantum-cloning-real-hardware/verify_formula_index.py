#!/usr/bin/env python3
"""Independently verify the quantum-cloning formula-index HBP/HBI/SHA packet."""

from __future__ import annotations

import hashlib
from pathlib import Path
from collections import Counter
from urllib.parse import unquote


LAW_ID = "LAW-ENCRYPTED-SINGLE-USE-QUANTUM-CLONING-REAL-HARDWARE"
PROFILE = "SOS-INTEGRITY-CRYPTO-LEARNING/QUANTUM-ENCRYPTED-CLONING"
SOURCE_COMMIT = "e74b89be27e683fd1fed03321fa092b0c5982a62"
SOURCE_HBP_SHA256 = "6687d25652769bfd87f2df5bed86bc37135feaba209437482f07000e32e3611e"
PAPER_SHA256 = "95febbd44ed31c9072acedee156c928f27ce38fffcc159696f3c864d6dafa755"
LAW_PID16 = hashlib.sha256(LAW_ID.encode("utf-8")).hexdigest()[:16]

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "receipts" / "quantum-cloning-real-hardware"
STEM = LAW_ID


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_row(text: str) -> tuple[str, dict[str, str]]:
    parts = text.rstrip("\n").split("|")
    kind = parts[0]
    fields: dict[str, str] = {}
    for part in parts[1:]:
        if not part:
            continue
        key, value = part.split("=", 1)
        if key in fields:
            raise AssertionError(f"duplicate tuple key: {key}")
        fields[key] = unquote(value)
    return kind, fields


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    hbp_path = OUT / f"{STEM}.hbp"
    hbi_path = OUT / f"{STEM}.hbi"
    md_path = OUT / f"{STEM}.md"
    core = [md_path, hbp_path, hbi_path]
    for path in core:
        require(path.is_file(), f"missing {path}")
        require(b"\r" not in path.read_bytes(), f"non-LF line endings: {path.name}")
        require(path.read_bytes().endswith(b"\n"), f"missing final LF: {path.name}")
    for path in core:
        sidecar = path.with_name(path.name + ".sha256").read_text(encoding="ascii").strip().split()
        require(sidecar == [digest(path.read_bytes()), path.name], f"sidecar mismatch: {path.name}")
    sums_path = OUT / "SHA256SUMS"
    sums: dict[str, str] = {}
    for line in sums_path.read_text(encoding="ascii").splitlines():
        value, name = line.split(None, 1)
        sums[name.strip()] = value
    require(set(sums) == {path.name for path in core}, "SHA256SUMS file set mismatch")
    for path in core:
        require(sums[path.name] == digest(path.read_bytes()), f"SHA256SUMS mismatch: {path.name}")
    sums_sidecar = (OUT / "SHA256SUMS.sha256").read_text(encoding="ascii").strip().split()
    require(sums_sidecar == [digest(sums_path.read_bytes()), "SHA256SUMS"], "SHA256SUMS sidecar mismatch")

    hbp = hbp_path.read_bytes()
    rows_bytes = hbp.splitlines()
    rows = [parse_row(item.decode("utf-8")) for item in rows_bytes]
    require(len(rows) == 10, "unexpected HBP row count")
    expected_kinds = Counter({
        "QCLONEFORMULAINDEXHDR": 1,
        "SOURCE": 1,
        "FORMULA": 1,
        "MEASURED": 2,
        "BOUNDARY": 1,
        "CLASSICALBOUNDARY": 1,
        "PROFILE": 1,
        "CORRECTION": 1,
        "QCLONEFORMULAINDEXFTR": 1,
    })
    require(Counter(kind for kind, _ in rows) == expected_kinds, "unexpected HBP row kinds")
    header_fields = rows[0][1]
    require(header_fields["law"] == LAW_ID and header_fields["profile"] == PROFILE and header_fields["pid16"] == LAW_PID16, "header identity mismatch")
    require(rows[0][0] == "QCLONEFORMULAINDEXHDR", "missing formula-index header")
    require(rows[-1][0] == "QCLONEFORMULAINDEXFTR", "missing formula-index footer")
    source = next(fields for kind, fields in rows if kind == "SOURCE")
    require(source["source_commit"] == SOURCE_COMMIT, "source commit mismatch")
    require(source["source_pr"] == "6", "source PR mismatch")
    require(source["paper"] == "arXiv:2602.10695v1", "paper version mismatch")
    require(source["peer_review_status"] == "NOT_ESTABLISHED_BY_THIS_INDEX", "peer-review boundary missing")
    require(source["source_hbp_sha256"] == SOURCE_HBP_SHA256, "source HBP mismatch")
    require(source["paper_pdf_sha256"] == PAPER_SHA256, "paper PDF mismatch")
    formula = next(fields for kind, fields in rows if kind == "FORMULA")
    require(formula["law"] == LAW_ID and formula["profile"] == PROFILE, "formula identity mismatch")
    require(formula["key_use"] == "SINGLE_USE", "key-use boundary missing")
    require(formula["pid16"] == LAW_PID16, "formula PID16 mismatch")
    measured = [fields for kind, fields in rows if kind == "MEASURED"]
    require(len(measured) == 2, "measured row count mismatch")
    require(measured[0]["platform"] == "IBM_HERON_R2_SUPERCONDUCTING_TRANSMON_QUBITS", "platform mismatch")
    require(measured[0]["physical_encrypted_clones_max"] == "77", "clone count mismatch")
    require(measured[1]["selected_clone_fidelity"] == "0.286_PLUS_MINUS_0.009", "fidelity mismatch")
    boundary = next(fields for kind, fields in rows if kind == "BOUNDARY")
    for key in ("simultaneous_readable_plaintext_clones", "no_cloning_theorem_abolished", "arbitrary_particle_replication_tested", "prismed_laser_photons_tested_by_paper", "physical_projection_or_uap_claim"):
        require(boundary[key] == "0", f"inflated boundary: {key}")
    classical = next(fields for kind, fields in rows if kind == "CLASSICALBOUNDARY")
    require(classical["is_ibm_hardware_experiment"] == "0", "classical/physical conflation")
    require(classical["blanket_denial_of_measured_encrypted_cloning"] == "0", "blanket denial retained")
    profile = next(fields for kind, fields in rows if kind == "PROFILE")
    require(profile["E"] == "0" and profile["fire"] == "0", "live activation claimed")
    require(profile["live_pid_office_ingest"] == "0", "live PID ingest claimed")

    correction = next(fields for kind, fields in rows if kind == "CORRECTION")
    require(correction["status"] == "ACCEPTED_BY_OPERATOR", "correction authority mismatch")
    require(correction["heldout_skillopt"] == "NOT_RUN_IN_THIS_REPOSITORY", "SkillOpt scope inflated")
    hbi_lines = hbi_path.read_text(encoding="utf-8").splitlines()
    hbi_kind, header = parse_row(hbi_lines[0])
    require(hbi_kind == "HBIHDR", "missing HBI header")
    require(header["target_sha256"] == digest(hbp), "HBI target hash mismatch")
    require(int(header["target_bytes"]) == len(hbp), "HBI target byte count mismatch")
    require(int(header["rows"]) == len(rows_bytes), "HBI row count mismatch")
    require(Counter(parse_row(line)[0] for line in hbi_lines) == Counter({"HBIHDR": 1, "HBIRANGE": 10}), "unexpected HBI row kinds")
    require(len(hbi_lines) == len(rows_bytes) + 1, "HBI range count mismatch")
    for expected_number, line in enumerate(hbi_lines[1:], start=1):
        kind, fields = parse_row(line)
        require(kind == "HBIRANGE", "unexpected HBI row")
        require(int(fields["row"]) == expected_number, "HBI row sequence mismatch")
        offset = int(fields["offset"])
        length = int(fields["length"])
        payload = hbp[offset : offset + length]
        require(payload == rows_bytes[expected_number - 1], "HBI byte range mismatch")
        require(fields["sha256"] == digest(payload), "HBI row hash mismatch")
        require(fields["row_kind"] == rows[expected_number - 1][0], "HBI row-kind mismatch")
    md = md_path.read_text(encoding="utf-8")
    require(SOURCE_COMMIT in md and SOURCE_HBP_SHA256 in md and PAPER_SHA256 in md, "human note lacks anchors")
    require("E=0" in md and "fire=0" in md, "human note lacks activation boundary")
    print(f"VERIFY|status=PASS|rows={len(rows_bytes)}|hbi_ranges={len(hbi_lines)-1}/{len(rows_bytes)}|hbp_sha256={digest(hbp)}|hbi_sha256={digest(hbi_path.read_bytes())}|E=0|fire=0|json=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
