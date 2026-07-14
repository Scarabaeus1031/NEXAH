"""Phase V work package D: bounded IEEE geometry perspectives and briefs."""

from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys

import pytest

from nexah.orientation import (
    BriefEvidenceClass,
    BriefOutcomeStatus,
    FindingStance,
    OrientationBrief,
    render_orientation_brief_markdown,
)
from nexah.power_systems import (
    IEEEGeometryAnalysis,
    IEEEGeometryCampaign,
    IEEEGeometryCaseManifest,
    IEEEGeometryLearningContext,
    build_ieee_geometry_orientation_brief,
    run_ieee_geometry_probe_suite,
)


ROOT = Path(__file__).parents[2]
CASE_DIR = ROOT / "APPLICATIONS" / "power_systems" / "ieee_geometry_v1"
MANIFEST_PATH = CASE_DIR / "case_manifest.json"
FRAMES_PATH = CASE_DIR / "development_frames.json"
GEOMETRY_PATH = CASE_DIR / "development_geometry.json"
ORIENTATION_PATH = CASE_DIR / "development_orientation.json"
BRIEF_JSON_PATH = CASE_DIR / "development_orientation_brief.json"
BRIEF_MARKDOWN_PATH = CASE_DIR / "development_orientation_brief.md"


def _inputs() -> tuple[
    IEEEGeometryCampaign,
    IEEEGeometryAnalysis,
    IEEEGeometryCaseManifest,
]:
    manifest = IEEEGeometryCaseManifest.from_dict(
        json.loads(MANIFEST_PATH.read_text())
    )
    campaign = IEEEGeometryCampaign.from_dict(json.loads(FRAMES_PATH.read_text()))
    analysis = IEEEGeometryAnalysis.from_dict(
        json.loads(GEOMETRY_PATH.read_text())["analysis"]
    )
    return campaign, analysis, manifest


def test_five_ieee_probes_preserve_identity_limits_and_read_only_status() -> None:
    campaign, analysis, manifest = _inputs()
    context = run_ieee_geometry_probe_suite(campaign, analysis, manifest)

    assert len(context.synthesis.probe_results) == 5
    assert all(result.read_only for result in context.synthesis.probe_results)
    assert context.synthesis.representation_id == campaign.campaign_id
    assert context.outcome_recorded is False
    assert context.report.position is not None
    assert context.report.position.identifier.scope == campaign.campaign_id
    assert context.synthesis.contradictions == ()
    assert {agreement.subject for agreement in context.synthesis.agreements} >= {
        "physical-stability-boundary",
        "observed-outcome",
    }


def test_physical_geometry_and_boundary_findings_are_descriptive() -> None:
    campaign, analysis, manifest = _inputs()
    context = run_ieee_geometry_probe_suite(campaign, analysis, manifest)
    by_id = {result.probe_id: result for result in context.synthesis.probe_results}

    physical = by_id["ieee-physical-state-probe-v1"]
    assert "17 converged" in physical.findings[0].statement
    assert "2 explicit failed" in physical.findings[0].statement
    assert "λ=2.2" in physical.findings[1].statement

    geometry = by_id["ieee-geometry-probe-v1"]
    assert "16 available adjacent" in geometry.findings[0].statement
    projection = next(
        finding
        for finding in geometry.findings
        if finding.subject == "cross-projection-agreement"
    )
    assert projection.stance is FindingStance.UNKNOWN
    assert "no comparison metric" in projection.statement

    boundary = by_id["ieee-boundary-probe-v1"]
    assert "λ=2.3" in boundary.findings[0].statement
    assert "λ=2.2" in boundary.findings[0].statement
    assert boundary.findings[1].stance is FindingStance.LIMITATION
    assert "do not certify" in boundary.findings[1].statement


def test_claim_critic_is_manifest_bound_and_memory_stays_closed() -> None:
    campaign, analysis, manifest = _inputs()
    context = run_ieee_geometry_probe_suite(campaign, analysis, manifest)
    critic = next(
        result
        for result in context.synthesis.probe_results
        if result.probe_id == "ieee-claim-critic-probe-v1"
    )

    assert len(critic.findings) == len(manifest.prohibited_claims)
    assert all(
        claim in finding.statement
        for claim, finding in zip(manifest.prohibited_claims, critic.findings)
    )
    assert all(finding.stance is FindingStance.LIMITATION for finding in critic.findings)
    assert context.report.similar_episodes == ()


def test_learning_context_and_brief_round_trip() -> None:
    campaign, analysis, manifest = _inputs()
    context = run_ieee_geometry_probe_suite(campaign, analysis, manifest)
    restored_context = IEEEGeometryLearningContext.from_dict(
        json.loads(json.dumps(context.to_dict()))
    )
    assert restored_context == context

    brief = build_ieee_geometry_orientation_brief(context, manifest)
    restored_brief = OrientationBrief.from_dict(
        json.loads(json.dumps(brief.to_dict()))
    )
    assert restored_brief == brief
    assert brief.outcome_status is BriefOutcomeStatus.COMPUTATION_ONLY
    assert brief.episode_id is None
    assert len(brief.perspectives) == 5
    assert {item.evidence_class for item in brief.evidence} >= {
        BriefEvidenceClass.BENCHMARK_MODEL,
        BriefEvidenceClass.COMPUTED_RESULT,
        BriefEvidenceClass.NOT_SUPPORTED,
    }
    markdown = render_orientation_brief_markdown(brief)
    assert "## Perspectives" in markdown
    assert "NO OBSERVED OUTCOME → NO EPISODIC MEMORY UPDATE" in markdown


def test_mismatched_campaign_identity_is_rejected() -> None:
    campaign, analysis, manifest = _inputs()
    changed = replace(analysis, campaign_id="different-campaign")

    with pytest.raises(ValueError, match="analysis and campaign identities differ"):
        run_ieee_geometry_probe_suite(campaign, changed, manifest)


@pytest.mark.parametrize(
    ("output_format", "expected_key"),
    (("report", "explanation"), ("probes", "synthesis"), ("brief-json", "perspectives")),
)
def test_cli_emits_ieee_orientation_products(
    output_format: str,
    expected_key: str,
) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "nexah.cli",
            "analyze-ieee-geometry",
            str(MANIFEST_PATH),
            str(FRAMES_PATH),
            "--format",
            output_format,
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(completed.stdout)
    assert expected_key in payload


def test_cli_emits_human_readable_ieee_brief() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "nexah.cli",
            "analyze-ieee-geometry",
            str(MANIFEST_PATH),
            str(FRAMES_PATH),
            "--format",
            "brief",
            "--question",
            "What does this sampled benchmark campaign support?",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert completed.stdout.startswith("# IEEE Geometry Orientation Brief")
    assert "What does this sampled benchmark campaign support?" in completed.stdout
    assert "NO OBSERVED OUTCOME → NO EPISODIC MEMORY UPDATE" in completed.stdout


def test_committed_orientation_products_are_canonical() -> None:
    campaign, analysis, manifest = _inputs()
    context = run_ieee_geometry_probe_suite(campaign, analysis, manifest)
    brief = build_ieee_geometry_orientation_brief(context, manifest)

    assert json.loads(ORIENTATION_PATH.read_text()) == context.to_dict()
    assert json.loads(BRIEF_JSON_PATH.read_text()) == brief.to_dict()
    assert BRIEF_MARKDOWN_PATH.read_text() == render_orientation_brief_markdown(brief)
