"""Human-facing Orientation Brief for the Network Orientation application."""

from __future__ import annotations

from nexah.orientation import (
    BriefEvidenceClass,
    BriefOutcomeStatus,
    BriefReproduction,
    OrientationBrief,
    generate_orientation_brief,
)

from .network_probes import NetworkLearningContext


def build_network_orientation_brief(
    context: NetworkLearningContext,
    *,
    question: str | None = None,
    reproduction_command: str = "nexah orient-network <graph.json> --format brief",
) -> OrientationBrief:
    """Build a bounded brief without converting a scenario into experience."""

    result = context.network_orientation
    structure = result.structure
    target = f"; target: {structure.target}" if structure.target is not None else ""
    return generate_orientation_brief(
        result.orientation,
        context.synthesis,
        brief_id=f"{structure.representation_id}:orientation-brief",
        title=f"Network Orientation Brief — {structure.focus}",
        question=question
        or (
            f"From {structure.focus}, what is structurally reachable, what has "
            "changed, and where does the evidence stop?"
        ),
        scope=(
            "The supplied directed graph and any explicitly declared comparison "
            "snapshot. The brief describes structure; it does not establish domain "
            "completeness, causal effects, or control authority."
        ),
        position=f"focus: {structure.focus}{target}",
        next_questions=(
            "Is the supplied graph complete for the question being asked?",
            "Which measurements or domain semantics support its nodes and edges?",
            "Which independently observed outcomes could evaluate this orientation?",
        ),
        reproduction=BriefReproduction(
            command=reproduction_command,
            artifacts=("orientation-brief.md",),
            deterministic=True,
        ),
        input_evidence_class=BriefEvidenceClass.DECLARED_INPUT,
        input_description=(
            "The source is a declared graph snapshot or training scenario. It is "
            "not treated as an independently observed outcome."
        ),
        outcome_status=BriefOutcomeStatus.NOT_RECORDED,
    )
