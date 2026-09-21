"""Evidence binding and closed-bundle tests for IEEE Projection Fidelity."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

import pytest

from nexah.orientation import ComputationResultRecord, EvidenceRecordType
from nexah.power_systems import (
    IEEEGeometryCampaign,
    build_ieee_projection_fidelity_analysis,
    build_ieee_projection_fidelity_computation_record,
    sha256_reference,
    verify_ieee_projection_fidelity_evidence_bundle,
    write_ieee_projection_fidelity_evidence_bundle,
)


ROOT = Path(__file__).parents[2]
CASE = ROOT / "APPLICATIONS" / "power_systems" / "ieee_geometry_v1"
CANONICAL = ROOT / "validation" / "ieee_projection_fidelity_v1" / "canonical_result.json"
COMPUTED_AT = datetime(2026, 9, 21, 12, 0, tzinfo=timezone.utc)


def _campaign(name: str) -> IEEEGeometryCampaign:
    return IEEEGeometryCampaign.from_dict(
        json.loads((CASE / name).read_text(encoding="utf-8"))
    )


def _bound_result():
    analysis = build_ieee_projection_fidelity_analysis(
        _campaign("development_frames.json"),
        _campaign("evaluation_frames.json"),
    )
    record = build_ieee_projection_fidelity_computation_record(
        analysis,
        computed_at=COMPUTED_AT,
        development_reference="development_campaign:sha256:development",
        evaluation_reference="evaluation_campaign:sha256:evaluation",
    )
    return analysis, record


def test_computation_record_binds_analysis_without_observation_claim() -> None:
    analysis, record = _bound_result()

    assert record.record_type is EvidenceRecordType.COMPUTATION_RESULT
    assert record.status.value == "success"
    assert record.deterministic_seed == 8208
    assert record.provenance.metadata["evaluation_refit"] is False
    assert record.output_checksums == {
        "analysis.json": sha256_reference(
            json.dumps(
                analysis.to_dict(),
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        )
    }
    assert ComputationResultRecord.from_dict(record.to_dict()) == record


def test_bundle_roundtrips_and_report_preserves_boundaries(tmp_path: Path) -> None:
    analysis, record = _bound_result()
    output = tmp_path / "bundle"

    manifest = write_ieee_projection_fidelity_evidence_bundle(
        output, analysis, record
    )
    verified = verify_ieee_projection_fidelity_evidence_bundle(output)
    report = (output / "report.md").read_text(encoding="utf-8")

    assert verified == manifest
    assert manifest["classification"] == "COMPUTATION_RESULT_ONLY"
    assert manifest["view_adapter_status"] == "NOT_IMPLEMENTED_GOVERNANCE_GATED"
    assert "Q_PLUS_R8" in report
    assert "not a seven-dimensional compression result" in report
    assert "not an ORION Orientation Report" in report


def test_bundle_verification_rejects_tampering(tmp_path: Path) -> None:
    analysis, record = _bound_result()
    output = tmp_path / "bundle"
    write_ieee_projection_fidelity_evidence_bundle(output, analysis, record)
    (output / "analysis.json").write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="mismatch"):
        verify_ieee_projection_fidelity_evidence_bundle(output)


def test_bundle_writer_refuses_existing_directory(tmp_path: Path) -> None:
    analysis, record = _bound_result()
    output = tmp_path / "bundle"
    output.mkdir()

    with pytest.raises(FileExistsError, match="already exists"):
        write_ieee_projection_fidelity_evidence_bundle(output, analysis, record)


def test_cli_exports_and_verifies_bundle(tmp_path: Path) -> None:
    output = tmp_path / "bundle"
    exported = subprocess.run(
        [
            sys.executable,
            "-m",
            "nexah.cli",
            "export-ieee-projection-fidelity-evidence",
            str(CANONICAL),
            "--computed-at",
            COMPUTED_AT.isoformat(),
            "--out-dir",
            str(output),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    verified = subprocess.run(
        [
            sys.executable,
            "-m",
            "nexah.cli",
            "verify-ieee-projection-fidelity-evidence",
            str(output),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert exported.returncode == 0, exported.stderr
    assert verified.returncode == 0, verified.stderr
    assert json.loads(exported.stdout)["status"] == "PASS"
    assert json.loads(verified.stdout)["schema"].endswith("/1.0")
    assert (output / "analysis.json").read_bytes() == CANONICAL.read_bytes()
