"""Human-facing Orientation Brief for the Phase V IEEE geometry case."""

from __future__ import annotations

from nexah.orientation import (
    BriefEvidenceClass,
    BriefOutcomeStatus,
    BriefReproduction,
    OrientationBrief,
    generate_orientation_brief,
)

from .ieee_geometry_probes import IEEEGeometryLearningContext
from .ieee_manifest import IEEEGeometryCaseManifest


def build_ieee_geometry_orientation_brief(
    context: IEEEGeometryLearningContext,
    manifest: IEEEGeometryCaseManifest,
    *,
    question: str | None = None,
    reproduction_command: str = (
        "nexah analyze-ieee-geometry <manifest.json> <frames.json> --format brief"
    ),
) -> OrientationBrief:
    """Build a bounded benchmark brief without creating observed experience."""

    analysis = context.analysis
    if analysis.manifest_id != manifest.manifest_id:
        raise ValueError("learning context and manifest identities differ")
    position = (
        context.report.position.label
        if context.report.position is not None
        and context.report.position.label is not None
        else "No converged sampled position is available"
    )
    transfer_question = (
        "Which new case should test the next prospectively frozen revision?"
        if analysis.case_role == "locked_evaluation"
        else "Does the frozen method transfer to IEEE-14 without parameter retuning?"
    )
    return generate_orientation_brief(
        context.report,
        context.synthesis,
        brief_id=f"{analysis.campaign_id}:orientation-brief",
        title=f"IEEE Geometry Orientation Brief — {analysis.case_id}",
        question=question or manifest.research_question,
        scope=(
            f"The {analysis.case_id} {analysis.case_role} benchmark campaign, its "
            "manifest-bound physical frames, frozen standardized projection, and "
            "descriptive geometry operators. The scope excludes elapsed-time "
            "dynamics, certified stability limits, causal inference, and control."
        ),
        position=position,
        next_questions=(
            transfer_question,
            "How do the geometric measurements compare with established power-system measures?",
            "Which prospectively declared metric should compare alternative projections?",
            "What observed measurements and outcomes would be required for external evaluation?",
        ),
        reproduction=BriefReproduction(
            command=reproduction_command,
            artifacts=(
                "geometry-analysis.json",
                "orientation-brief.json",
                "orientation-brief.md",
            ),
            deterministic=True,
        ),
        input_evidence_class=BriefEvidenceClass.BENCHMARK_MODEL,
        input_description=(
            "The input is an IEEE/Pandapower benchmark model evaluated through a "
            "frozen computational protocol; it is not an operational-grid measurement."
        ),
        outcome_status=BriefOutcomeStatus.COMPUTATION_ONLY,
    )
