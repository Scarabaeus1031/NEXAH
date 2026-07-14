"""Reproduce the frozen Phase V IEEE-14 geometry evaluation gate."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from nexah.orientation import Context, Provenance, render_orientation_brief_markdown
from nexah.power_systems import (
    IEEEFrameStatus,
    IEEEGeometryCampaign,
    IEEEGeometryCaseManifest,
    IEEEGeometryValueStatus,
    analyze_ieee_geometry,
    build_ieee_geometry_campaign,
    build_ieee_geometry_orientation_brief,
    check_manifest_adapter_protocol,
    check_manifest_environment,
    fit_ieee_standardization,
    run_ieee_geometry_probe_suite,
)
from nexah.sources import IEEEPandapowerAdapter


ROOT = Path(__file__).parents[2]
CASE_DIR = ROOT / "APPLICATIONS" / "power_systems" / "ieee_geometry_v1"
RECORDED_AT = datetime(2026, 7, 14, 18, 0, tzinfo=timezone.utc)


def _load(name: str) -> dict[str, Any]:
    value = json.loads((CASE_DIR / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"canonical artifact must be a JSON object: {name}")
    return value


def _canonical_json(payload: object) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _payload_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _fresh_evaluation_campaign(
    manifest: IEEEGeometryCaseManifest,
) -> IEEEGeometryCampaign:
    case = next(item for item in manifest.cases if item.case_id == "ieee14")
    campaign_id = f"{manifest.manifest_id}-{case.case_id}"
    source_campaign = IEEEPandapowerAdapter(case_id=case.case_id).run_campaign(
        case.load_scales,
        campaign_id=campaign_id,
        provenance=Provenance(
            source=case.source_loader,
            method="frozen independent Newton-Raphson load-scale campaign",
            recorded_at=RECORDED_AT,
            record_id=campaign_id,
            metadata={"manifest_id": manifest.manifest_id},
        ),
        context=Context(
            domain="power-system",
            values={
                "evidence_class": manifest.evidence_class,
                "case_role": case.role,
                "campaign_axis": manifest.campaign_axis,
            },
        ),
    )
    return build_ieee_geometry_campaign(source_campaign, manifest)


def build_summary() -> dict[str, Any]:
    """Return the complete frozen gate and its bounded claim audit."""

    manifest_source = _load("case_manifest.json")
    manifest = IEEEGeometryCaseManifest.from_dict(manifest_source)
    development_campaign = IEEEGeometryCampaign.from_dict(
        _load("development_frames.json")
    )
    development_model = fit_ieee_standardization(development_campaign, manifest)
    development_analysis = analyze_ieee_geometry(
        development_campaign,
        manifest,
        development_model,
    )
    development_payload = {
        "standardization_model": development_model.to_dict(),
        "analysis": development_analysis.to_dict(),
    }

    evaluation_campaign = _fresh_evaluation_campaign(manifest)
    evaluation_analysis = analyze_ieee_geometry(
        evaluation_campaign,
        manifest,
        development_model,
    )
    evaluation_payload = {
        "standardization_model": development_model.to_dict(),
        "analysis": evaluation_analysis.to_dict(),
    }
    evaluation_context = run_ieee_geometry_probe_suite(
        evaluation_campaign,
        evaluation_analysis,
        manifest,
    )
    evaluation_brief = build_ieee_geometry_orientation_brief(
        evaluation_context,
        manifest,
    )
    evaluation_brief_markdown = render_orientation_brief_markdown(evaluation_brief)

    environment = check_manifest_environment(manifest)
    adapter_mismatches = check_manifest_adapter_protocol(manifest)
    committed_evaluation_frames = _load("evaluation_frames.json")
    committed_evaluation_geometry = _load("evaluation_geometry.json")
    committed_evaluation_orientation = _load("evaluation_orientation.json")
    committed_evaluation_brief = _load("evaluation_orientation_brief.json")

    checks = (
        {
            "check_id": "environment-lock",
            "passed": environment.compatible,
            "detail": "Frozen package versions match the manifest."
            if environment.compatible
            else "; ".join(environment.mismatches),
        },
        {
            "check_id": "adapter-protocol",
            "passed": not adapter_mismatches,
            "detail": "Adapter variables and units match the manifest."
            if not adapter_mismatches
            else "; ".join(adapter_mismatches),
        },
        {
            "check_id": "development-freeze",
            "passed": development_payload == _load("development_geometry.json"),
            "detail": "The committed IEEE-9 model and geometry reproduce exactly.",
        },
        {
            "check_id": "no-evaluation-refit",
            "passed": (
                evaluation_analysis.case_role == "locked_evaluation"
                and development_model.fit_case_id == "ieee9"
                and evaluation_analysis.projection_model == development_model
            ),
            "detail": "IEEE-14 uses the unchanged model fitted on IEEE-9.",
        },
        {
            "check_id": "evaluation-source-replay",
            "passed": evaluation_campaign.to_dict() == committed_evaluation_frames,
            "detail": "The fresh IEEE-14 source campaign matches the canonical frames.",
        },
        {
            "check_id": "evaluation-geometry-replay",
            "passed": evaluation_payload == committed_evaluation_geometry,
            "detail": "Frozen geometry output matches the canonical evaluation.",
        },
        {
            "check_id": "evaluation-report-replay",
            "passed": evaluation_context.to_dict() == committed_evaluation_orientation,
            "detail": "Five probes and the Orientation Report reproduce exactly.",
        },
        {
            "check_id": "evaluation-brief-replay",
            "passed": (
                evaluation_brief.to_dict() == committed_evaluation_brief
                and evaluation_brief_markdown
                == (CASE_DIR / "evaluation_orientation_brief.md").read_text(
                    encoding="utf-8"
                )
            ),
            "detail": "JSON and Markdown briefs derive from the same typed result.",
        },
        {
            "check_id": "failure-preservation",
            "passed": all(
                frame.system_features is None and not frame.entity_views
                for frame in (
                    *development_campaign.frames,
                    *evaluation_campaign.frames,
                )
                if frame.status is IEEEFrameStatus.FAILED
            )
            and any(
                frame.status is IEEEFrameStatus.FAILED
                for frame in development_campaign.frames
            ),
            "detail": (
                "The two IEEE-9 failure fixtures remain explicit and contain no "
                "fabricated physics; the same policy applies to IEEE-14."
            ),
        },
        {
            "check_id": "outcome-boundary",
            "passed": (
                manifest.outcome_status == "not_observed"
                and not manifest.episode_update_allowed
                and not evaluation_context.outcome_recorded
            ),
            "detail": "Benchmark computation remains outside episodic memory.",
        },
    )

    converged = tuple(
        frame
        for frame in evaluation_campaign.frames
        if frame.status is IEEEFrameStatus.CONVERGED
    )
    failed = tuple(
        frame
        for frame in evaluation_campaign.frames
        if frame.status is IEEEFrameStatus.FAILED
    )
    available_steps = tuple(
        step
        for step in evaluation_analysis.steps
        if step.status is IEEEGeometryValueStatus.AVAILABLE
    )
    available_turns = tuple(
        turn
        for turn in evaluation_analysis.turns
        if turn.status is IEEEGeometryValueStatus.AVAILABLE
    )
    gate_passed = all(check["passed"] for check in checks)
    development_converged = tuple(
        frame
        for frame in development_campaign.frames
        if frame.status is IEEEFrameStatus.CONVERGED
    )
    development_failed = tuple(
        frame
        for frame in development_campaign.frames
        if frame.status is IEEEFrameStatus.FAILED
    )
    return {
        "validation_id": "phase-v-ieee-geometry-v1",
        "recorded_at": RECORDED_AT.isoformat(),
        "gate_passed": gate_passed,
        "checks": list(checks),
        "freeze": {
            "manifest_id": manifest.manifest_id,
            "manifest_sha256": _payload_sha256(manifest_source),
            "development_case": development_model.fit_case_id,
            "development_campaign": development_model.fit_campaign_id,
            "development_model_sha256": _payload_sha256(
                development_model.to_dict()
            ),
            "evaluation_case": evaluation_analysis.case_id,
            "evaluation_role": evaluation_analysis.case_role,
            "operator_ids": list(evaluation_analysis.operator_ids),
            "parameter_retuning": False,
        },
        "evaluation_result": {
            "declared_frames": len(evaluation_campaign.frames),
            "converged_frames": len(converged),
            "failed_frames": len(failed),
            "failed_load_scales": [frame.load_scale for frame in failed],
            "available_steps": len(available_steps),
            "insufficient_steps": len(evaluation_analysis.steps)
            - len(available_steps),
            "available_turns": len(available_turns),
            "insufficient_turns": len(evaluation_analysis.turns)
            - len(available_turns),
            "solver_boundaries": len(evaluation_analysis.solver_boundaries),
            "boundary_interpretation": (
                "No sampled solver boundary is observed on the frozen IEEE-14 grid."
                if not evaluation_analysis.solver_boundaries
                else "Sampled solver non-convergence is recorded without physical certification."
            ),
            "total_path_length": evaluation_analysis.total_path_length,
            "frames_sha256": _payload_sha256(evaluation_campaign.to_dict()),
            "geometry_sha256": _payload_sha256(evaluation_payload),
            "orientation_sha256": _payload_sha256(evaluation_context.to_dict()),
            "brief_sha256": _payload_sha256(evaluation_brief.to_dict()),
        },
        "development_result": {
            "declared_frames": len(development_campaign.frames),
            "converged_frames": len(development_converged),
            "failed_frames": len(development_failed),
            "failed_load_scales": [
                frame.load_scale for frame in development_failed
            ],
            "failure_values_fabricated": False,
        },
        "validation_ladder": [
            "deterministic operator fixtures",
            "manually inspectable IEEE-9 development campaign",
            "shared implementation across development and evaluation roles",
            "explicit failure and insufficient-result preservation",
            "IEEE-14 frozen evaluation without parameter retuning",
            "byte-reproducible machine-readable summary",
            "manifest-bound supported and prohibited claim audit",
        ],
        "claim_audit": {
            "supported": [
                {
                    "claim": claim,
                    "status": (
                        "supported_within_manifest"
                        if gate_passed
                        else "not_supported_by_failed_gate"
                    ),
                }
                for claim in manifest.supported_claims
            ],
            "prohibited": [
                {"claim": claim, "status": "explicitly_excluded"}
                for claim in manifest.prohibited_claims
            ],
        },
        "limitations": [
            "The campaign axis is ordered load scale, not elapsed time.",
            "No solver failure occurs on the frozen IEEE-14 grid, so no sampled boundary is inferred.",
            "Uncertainty is uncalibrated and remains explicitly unknown.",
            "The result is benchmark computation, not operational-grid evidence.",
            "No causal, predictive, control, or real-world generalization claim is made.",
            "No observed outcome exists; episodic-memory update remains prohibited.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    encoded = _canonical_json(build_summary())
    if args.out is None:
        print(encoded, end="")
    else:
        args.out.write_text(encoded, encoding="utf-8")


if __name__ == "__main__":
    main()
