"""Bound, export, and render IEEE Projection Fidelity computation evidence.

This module does not reinterpret the sidecar analysis.  It binds the exact
analysis payload to the existing computation-result contract and exports a
small, hash-checked bundle for Human inspection or later presentation.
"""

from __future__ import annotations

from dataclasses import fields
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from nexah.orientation import (
    ComputationResultRecord,
    ComputationStatus,
    Provenance,
    Uncertainty,
    UncertaintyKind,
)

from .ieee_projection_fidelity import IEEEProjectionFidelityAnalysis


EVIDENCE_BUNDLE_SCHEMA = "nexah.ieee_projection_fidelity_evidence_bundle/1.0"
CLAIM_CEILING = "BOUNDED_IEEE_REPRESENTATION_FIDELITY_AUDIT"
HUMAN_AUTHORITY = (
    "Inspection, interpretation, adoption, rejection, and continuation remain "
    "Human-owned."
)


def canonical_json_bytes(value: Any) -> bytes:
    """Return stable UTF-8 JSON bytes for hashing and bundle output."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_reference(data: bytes) -> str:
    """Return one explicit SHA-256 reference."""

    return f"sha256:{sha256(data).hexdigest()}"


def analysis_from_result_payload(
    payload: dict[str, Any],
) -> IEEEProjectionFidelityAnalysis:
    """Extract the typed analysis from a canonical validation result payload."""

    names = {field.name for field in fields(IEEEProjectionFidelityAnalysis)}
    missing = names.difference(payload)
    if missing:
        raise ValueError(
            "canonical result lacks analysis fields: " + ", ".join(sorted(missing))
        )
    return IEEEProjectionFidelityAnalysis.from_dict(
        {name: payload[name] for name in names}
    )


def build_ieee_projection_fidelity_computation_record(
    analysis: IEEEProjectionFidelityAnalysis,
    *,
    computed_at: datetime,
    development_reference: str,
    evaluation_reference: str,
    analysis_payload: bytes | None = None,
) -> ComputationResultRecord:
    """Bind an exact sidecar result without promoting it to an observation."""

    analysis_bytes = analysis_payload or canonical_json_bytes(analysis.to_dict())
    analysis_reference = sha256_reference(analysis_bytes)
    model_reference = sha256_reference(canonical_json_bytes(analysis.model.to_dict()))
    status = (
        ComputationStatus.SUCCESS
        if analysis.status == "PASS"
        else ComputationStatus.FAILURE
    )
    return ComputationResultRecord(
        record_id=f"computation:ieee-projection-fidelity:{analysis_reference}",
        scope=(
            f"{analysis.development.case_id}-development/"
            f"{analysis.evaluation.case_id}-evaluation"
        ),
        computed_at=computed_at,
        input_references=(development_reference, evaluation_reference),
        configuration_reference=(
            f"ieee-projection-fidelity-model:{model_reference}"
        ),
        status=status,
        output_checksums={"analysis.json": analysis_reference},
        numerical_warnings=(
            "Floating-point comparisons are bounded by the declared protocol tolerance.",
            "This computation result is not an independently observed outcome.",
        ),
        uncertainty=Uncertainty(
            kind=UncertaintyKind.QUALITATIVE,
            value=None,
            basis=(
                "Bounded by the declared IEEE-9 development and untouched IEEE-14 "
                "evaluation campaigns; no external scientific generalization is assigned."
            ),
        ),
        provenance=Provenance(
            source="NEXAH Core IEEE Projection Fidelity Sidecar V1",
            method=analysis.protocol_id,
            recorded_at=computed_at,
            record_id=analysis_reference,
            metadata={
                "analysis_schema_version": analysis.schema_version,
                "decision": analysis.decision,
                "development_case": analysis.development.case_id,
                "evaluation_case": analysis.evaluation.case_id,
                "evaluation_refit": analysis.evaluation_refit,
                "claim_ceiling": CLAIM_CEILING,
            },
        ),
        deterministic_seed=analysis.model.random_seed,
    )


def render_ieee_projection_fidelity_evidence_markdown(
    analysis: IEEEProjectionFidelityAnalysis,
    record: ComputationResultRecord,
) -> str:
    """Render a faithful Human-readable projection of the bound computation."""

    evaluation = {item.representation: item for item in analysis.evaluation.metrics}
    rows = []
    for name in ("FULL8", "Q_ONLY7", "Q_PLUS_R8", "PCA7"):
        metric = evaluation[name]
        rows.append(
            "| "
            f"`{name}` | {metric.stored_scalars} | "
            f"{metric.pair_distance_nrmse:.12g} | "
            f"{metric.path_length_relative_error:.12g} | "
            f"{metric.turn_angle_mae_degrees:.12g} |"
        )
    nonclaims = "\n".join(f"- {item}" for item in analysis.nonclaims)
    warnings = "\n".join(f"- {item}" for item in record.numerical_warnings)
    return "\n".join(
        (
            "# NEXAH Compare — IEEE Projection Fidelity Evidence",
            "",
            f"- Status: `{analysis.status}`",
            f"- Decision: `{analysis.decision}`",
            f"- Claim ceiling: `{CLAIM_CEILING}`",
            f"- Record type: `{record.record_type.value}`",
            f"- Record ID: `{record.record_id}`",
            f"- Protocol: `{analysis.protocol_id}`",
            f"- Development: `{analysis.development.case_id}`",
            f"- Evaluation: `{analysis.evaluation.case_id}`",
            f"- Evaluation refit: `{str(analysis.evaluation_refit).lower()}`",
            "",
            "## Held-out evaluation comparison",
            "",
            "| Representation | Stored scalars | Pair-distance NRMSE | Path-length relative error | Turn-angle MAE (degrees) |",
            "|---|---:|---:|---:|---:|",
            *rows,
            "",
            "## Quotient–residual checks",
            "",
            f"- Q+R standardized reconstruction max error: `{analysis.q_plus_r_standardized_reconstruction_max_error:.12g}`",
            f"- Q+R raw reconstruction max error: `{analysis.q_plus_r_raw_reconstruction_max_error:.12g}`",
            f"- Q+R pair-distance max error: `{analysis.q_plus_r_pair_distance_max_error:.12g}`",
            f"- Q-only kernel-counterfactual max distance: `{analysis.q_only_kernel_max_distance:.12g}`",
            f"- Q+R kernel-event detection rate: `{analysis.q_plus_r_kernel_detection_rate:.12g}`",
            "",
            "## What this establishes",
            "",
            "Within the declared campaigns and tolerance, the quotient-only view hides "
            "the tested antisymmetric kernel direction, while the explicitly typed "
            "residual restores the full standardized coordinate state and the tested geometry.",
            "",
            "`Q_PLUS_R8` is an eight-scalar coordinate transformation and exact "
            "reconstruction control. It is not a seven-dimensional compression result.",
            "",
            "## Nonclaims",
            "",
            nonclaims,
            "",
            "## Numerical and evidence boundary",
            "",
            warnings,
            "",
            HUMAN_AUTHORITY,
            "",
            "This document is a faithful projection of `analysis.json` and "
            "`computation_result.json`. It is not an ORION Orientation Report, an "
            "independent observation, a Human decision, or a THE EYE A2 comparison result.",
            "",
        )
    )


def write_ieee_projection_fidelity_evidence_bundle(
    output_directory: Path,
    analysis: IEEEProjectionFidelityAnalysis,
    record: ComputationResultRecord,
    *,
    analysis_payload: bytes | None = None,
) -> dict[str, Any]:
    """Write a new, closed evidence bundle and return its manifest."""

    if output_directory.exists():
        raise FileExistsError("evidence bundle output directory already exists")

    analysis_bytes = analysis_payload or canonical_json_bytes(analysis.to_dict())
    try:
        bound_analysis = analysis_from_result_payload(json.loads(analysis_bytes))
    except (TypeError, ValueError, json.JSONDecodeError) as error:
        raise ValueError("analysis payload is not a valid fidelity result") from error
    if bound_analysis != analysis:
        raise ValueError("analysis payload differs from the supplied typed analysis")
    if record.output_checksums != {"analysis.json": sha256_reference(analysis_bytes)}:
        raise ValueError("computation record does not bind the supplied analysis bytes")
    record_bytes = canonical_json_bytes(record.to_dict())
    report_bytes = render_ieee_projection_fidelity_evidence_markdown(
        analysis, record
    ).encode("utf-8")
    files = {
        "analysis.json": analysis_bytes,
        "computation_result.json": record_bytes,
        "report.md": report_bytes,
    }
    manifest = {
        "schema": EVIDENCE_BUNDLE_SCHEMA,
        "classification": "COMPUTATION_RESULT_ONLY",
        "claim_ceiling": CLAIM_CEILING,
        "protocol_id": analysis.protocol_id,
        "status": analysis.status,
        "decision": analysis.decision,
        "human_authority": HUMAN_AUTHORITY,
        "view_adapter_status": "NOT_IMPLEMENTED_GOVERNANCE_GATED",
        "files": {
            name: {"sha256": sha256_reference(data), "bytes": len(data)}
            for name, data in sorted(files.items())
        },
    }
    output_directory.mkdir(parents=True)
    for name, data in files.items():
        (output_directory / name).write_bytes(data)
    (output_directory / "manifest.json").write_bytes(canonical_json_bytes(manifest))
    return manifest


def verify_ieee_projection_fidelity_evidence_bundle(
    bundle_directory: Path,
) -> dict[str, Any]:
    """Fail closed unless every bundled byte and cross-reference is exact."""

    manifest_path = bundle_directory / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("evidence bundle manifest is unavailable or invalid") from error
    if not isinstance(manifest, dict) or manifest.get("schema") != EVIDENCE_BUNDLE_SCHEMA:
        raise ValueError("unknown evidence bundle schema")
    expected_names = {"analysis.json", "computation_result.json", "report.md"}
    file_manifest = manifest.get("files")
    if not isinstance(file_manifest, dict) or set(file_manifest) != expected_names:
        raise ValueError("evidence bundle file allowlist differs")

    payloads: dict[str, bytes] = {}
    for name in sorted(expected_names):
        declaration = file_manifest[name]
        if not isinstance(declaration, dict):
            raise ValueError(f"invalid manifest declaration for {name}")
        try:
            payload = (bundle_directory / name).read_bytes()
        except OSError as error:
            raise ValueError(f"evidence bundle file is unavailable: {name}") from error
        if declaration.get("bytes") != len(payload):
            raise ValueError(f"evidence bundle byte count mismatch: {name}")
        if declaration.get("sha256") != sha256_reference(payload):
            raise ValueError(f"evidence bundle checksum mismatch: {name}")
        payloads[name] = payload

    try:
        analysis = analysis_from_result_payload(json.loads(payloads["analysis.json"]))
        record = ComputationResultRecord.from_dict(
            json.loads(payloads["computation_result.json"])
        )
    except (TypeError, ValueError, json.JSONDecodeError) as error:
        raise ValueError("evidence bundle contract payload is invalid") from error
    analysis_reference = sha256_reference(payloads["analysis.json"])
    if record.output_checksums != {"analysis.json": analysis_reference}:
        raise ValueError("computation record does not bind the bundled analysis")
    expected_report = render_ieee_projection_fidelity_evidence_markdown(
        analysis, record
    ).encode("utf-8")
    if payloads["report.md"] != expected_report:
        raise ValueError("evidence report is not a faithful contract projection")
    if manifest.get("protocol_id") != analysis.protocol_id:
        raise ValueError("manifest protocol does not match analysis")
    if manifest.get("status") != analysis.status or manifest.get("decision") != analysis.decision:
        raise ValueError("manifest outcome does not match analysis")
    return manifest
