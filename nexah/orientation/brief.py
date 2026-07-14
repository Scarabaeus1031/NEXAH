"""Human-centered, evidence-bound Orientation Brief contracts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .base import ContractModel, require_aware_datetime, require_text
from .evidence import Provenance
from .probes import FindingStance, ProbeSynthesis
from .report import OrientationReport


class BriefEvidenceClass(str, Enum):
    """Repository-visible evidence roles; not a quality ranking."""

    DECLARED_INPUT = "declared_input"
    BENCHMARK_MODEL = "benchmark_model"
    COMPUTED_RESULT = "computed_result"
    OBSERVED_MEASUREMENT = "observed_measurement"
    OBSERVED_OUTCOME = "observed_outcome"
    ASSUMPTION = "assumption"
    UNKNOWN = "unknown"
    NOT_SUPPORTED = "not_supported"


class BriefOutcomeStatus(str, Enum):
    """Whether the brief has an independently observed outcome."""

    NOT_RECORDED = "not_recorded"
    COMPUTATION_ONLY = "computation_only"
    OBSERVED = "observed"


@dataclass(frozen=True, slots=True, kw_only=True)
class BriefPerspective(ContractModel):
    perspective_id: str
    title: str
    question: str
    findings: tuple[str, ...]
    limitations: tuple[str, ...]
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        require_text(self.perspective_id, "perspective_id")
        require_text(self.title, "title")
        require_text(self.question, "question")
        if not self.findings:
            raise ValueError("brief perspective requires at least one finding")


@dataclass(frozen=True, slots=True, kw_only=True)
class BriefEvidenceStatement(ContractModel):
    statement_id: str
    evidence_class: BriefEvidenceClass
    statement: str
    references: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_text(self.statement_id, "statement_id")
        require_text(self.statement, "statement")
        if (
            self.evidence_class is BriefEvidenceClass.OBSERVED_OUTCOME
            and not self.references
        ):
            raise ValueError(
                "observed-outcome evidence requires an independent reference"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class BriefReproduction(ContractModel):
    command: str
    artifacts: tuple[str, ...]
    deterministic: bool

    def __post_init__(self) -> None:
        require_text(self.command, "command")
        if not self.artifacts:
            raise ValueError("brief reproduction requires at least one artifact")
        for artifact in self.artifacts:
            require_text(artifact, "artifact")


@dataclass(frozen=True, slots=True, kw_only=True)
class OrientationBrief(ContractModel):
    """A compact orientation product for people, not an action recommendation."""

    brief_id: str
    title: str
    question: str
    scope: str
    position: str
    changes: tuple[str, ...]
    perspectives: tuple[BriefPerspective, ...]
    agreements: tuple[str, ...]
    contradictions: tuple[str, ...]
    evidence: tuple[BriefEvidenceStatement, ...]
    boundaries: tuple[str, ...]
    missing_information: tuple[str, ...]
    assumptions: tuple[str, ...]
    next_questions: tuple[str, ...]
    outcome_status: BriefOutcomeStatus
    reproduction: BriefReproduction
    timestamp: datetime
    provenance: Provenance
    episode_id: str | None = None
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        require_text(self.brief_id, "brief_id")
        require_text(self.title, "title")
        require_text(self.question, "question")
        require_text(self.scope, "scope")
        require_text(self.position, "position")
        require_text(self.schema_version, "schema_version")
        require_aware_datetime(self.timestamp, "timestamp")
        if len(self.perspectives) < 2:
            raise ValueError("OrientationBrief requires at least two perspectives")
        perspective_ids = [item.perspective_id for item in self.perspectives]
        if len(perspective_ids) != len(set(perspective_ids)):
            raise ValueError("brief perspective IDs must be unique")
        evidence_ids = [item.statement_id for item in self.evidence]
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("brief evidence statement IDs must be unique")
        if not self.next_questions:
            raise ValueError("OrientationBrief requires at least one next question")
        if self.episode_id is not None:
            require_text(self.episode_id, "episode_id")
            if self.outcome_status is not BriefOutcomeStatus.OBSERVED:
                raise ValueError(
                    "episode reference requires an independently observed outcome"
                )
        has_observed_outcome = any(
            item.evidence_class is BriefEvidenceClass.OBSERVED_OUTCOME
            for item in self.evidence
        )
        if self.outcome_status is BriefOutcomeStatus.OBSERVED:
            if not has_observed_outcome:
                raise ValueError(
                    "observed outcome status requires observed-outcome evidence"
                )
        elif has_observed_outcome:
            raise ValueError(
                "observed-outcome evidence conflicts with non-observed status"
            )


def generate_orientation_brief(
    report: OrientationReport,
    synthesis: ProbeSynthesis,
    *,
    brief_id: str,
    title: str,
    question: str,
    scope: str,
    position: str,
    next_questions: tuple[str, ...],
    reproduction: BriefReproduction,
    input_evidence_class: BriefEvidenceClass,
    input_description: str,
    outcome_status: BriefOutcomeStatus = BriefOutcomeStatus.NOT_RECORDED,
    observed_outcome: BriefEvidenceStatement | None = None,
    episode_id: str | None = None,
) -> OrientationBrief:
    """Convert a report and probe synthesis into a standalone user brief."""

    if report.position is not None:
        if report.position.identifier.scope != synthesis.representation_id:
            raise ValueError("report and synthesis representation IDs must match")

    perspectives = tuple(
        BriefPerspective(
            perspective_id=result.probe_id,
            title=result.perspective,
            question=f"What does the {result.perspective} perspective show?",
            findings=tuple(
                f"[{finding.stance.value}] {finding.statement}"
                for finding in result.findings
            ),
            limitations=tuple(
                [
                    finding.statement
                    for finding in result.findings
                    if finding.stance is FindingStance.LIMITATION
                ]
                + list(result.missing_information)
            ),
            evidence_ids=tuple(
                sorted(
                    {
                        evidence_id
                        for finding in result.findings
                        for evidence_id in finding.evidence_ids
                    }
                )
            ),
        )
        for result in synthesis.probe_results
    )
    limitation_statements = tuple(
        finding.statement
        for result in synthesis.probe_results
        for finding in result.findings
        if finding.stance is FindingStance.LIMITATION
    )
    agreements = tuple(
        f"{agreement.subject}: {agreement.stance.value} by "
        + ", ".join(agreement.probe_ids)
        for agreement in synthesis.agreements
    )
    contradictions = tuple(
        f"{contradiction.subject}: support from "
        + ", ".join(contradiction.supporting_probe_ids)
        + "; challenge from "
        + ", ".join(contradiction.challenging_probe_ids)
        for contradiction in synthesis.contradictions
    )
    evidence: list[BriefEvidenceStatement] = [
        BriefEvidenceStatement(
            statement_id=f"{brief_id}:input",
            evidence_class=input_evidence_class,
            statement=input_description,
            references=report.evidence_references,
        ),
        BriefEvidenceStatement(
            statement_id=f"{brief_id}:computed",
            evidence_class=BriefEvidenceClass.COMPUTED_RESULT,
            statement=(
                "The Orientation Report and probe findings are computed from the "
                "declared input under the recorded methods."
            ),
            references=synthesis.evidence_references,
        ),
    ]
    evidence.extend(
        BriefEvidenceStatement(
            statement_id=f"{brief_id}:assumption:{index}",
            evidence_class=BriefEvidenceClass.ASSUMPTION,
            statement=assumption,
        )
        for index, assumption in enumerate(report.assumptions, start=1)
    )
    if outcome_status is BriefOutcomeStatus.OBSERVED:
        if observed_outcome is None:
            raise ValueError(
                "observed status requires an explicit observed-outcome statement"
            )
        if observed_outcome.evidence_class is not BriefEvidenceClass.OBSERVED_OUTCOME:
            raise ValueError(
                "observed outcome statement must use observed_outcome evidence class"
            )
        evidence.append(observed_outcome)
    else:
        if observed_outcome is not None:
            raise ValueError(
                "observed-outcome statement conflicts with non-observed status"
            )
        evidence.append(
            BriefEvidenceStatement(
                statement_id=f"{brief_id}:outcome",
                evidence_class=BriefEvidenceClass.NOT_SUPPORTED,
                statement=(
                    "No independently observed outcome is attached; episodic "
                    "memory must not be updated from this brief."
                ),
            )
        )
    boundaries = tuple(
        dict.fromkeys(
            limitation_statements
            + (
                "The brief supports orientation and question formation, not "
                "autonomous action or control.",
            )
        )
    )
    return OrientationBrief(
        brief_id=brief_id,
        title=title,
        question=question,
        scope=scope,
        position=position,
        changes=report.change,
        perspectives=perspectives,
        agreements=agreements,
        contradictions=contradictions,
        evidence=tuple(evidence),
        boundaries=boundaries,
        missing_information=report.missing_information,
        assumptions=report.assumptions,
        next_questions=next_questions,
        outcome_status=outcome_status,
        episode_id=episode_id,
        reproduction=reproduction,
        timestamp=report.timestamp,
        provenance=Provenance(
            source=report.provenance.source,
            method="orientation-brief-generator-v1",
            recorded_at=report.timestamp,
            record_id=brief_id,
            metadata={
                "representation_id": synthesis.representation_id,
                "probe_count": len(synthesis.probe_results),
            },
        ),
    )


def render_orientation_brief_markdown(brief: OrientationBrief) -> str:
    """Render the typed brief as a stable, human-readable Markdown document."""

    lines = [
        f"# {brief.title}",
        "",
        f"**Question:** {brief.question}",
        "",
        f"**Scope:** {brief.scope}",
        "",
        f"**Position:** {brief.position}",
        "",
        f"**Outcome status:** `{brief.outcome_status.value}`",
        "",
        "## What changed",
        "",
    ]
    lines.extend(f"- {item}" for item in brief.changes)
    lines.extend(["", "## Perspectives", ""])
    for perspective in brief.perspectives:
        lines.extend(
            [
                f"### {perspective.title}",
                "",
                f"*{perspective.question}*",
                "",
            ]
        )
        lines.extend(f"- {finding}" for finding in perspective.findings)
        if perspective.limitations:
            lines.extend(["", "Limits:"])
            lines.extend(f"- {item}" for item in perspective.limitations)
        lines.append("")
    lines.extend(["## Agreement and disagreement", ""])
    lines.append("Agreements:")
    lines.extend(
        f"- {item}" for item in (brief.agreements or ("None recorded.",))
    )
    lines.extend(["", "Contradictions:"])
    lines.extend(
        f"- {item}" for item in (brief.contradictions or ("None recorded.",))
    )
    lines.extend(["", "## Evidence", ""])
    lines.extend(
        f"- **{item.evidence_class.value}:** {item.statement}"
        for item in brief.evidence
    )
    lines.extend(["", "## Boundaries", ""])
    lines.extend(f"- {item}" for item in brief.boundaries)
    lines.extend(["", "## Missing information", ""])
    lines.extend(f"- {item}" for item in brief.missing_information)
    lines.extend(["", "## What should we ask next?", ""])
    lines.extend(f"- {item}" for item in brief.next_questions)
    lines.extend(
        [
            "",
            "## Reproduce",
            "",
            "```bash",
            brief.reproduction.command,
            "```",
            "",
            "Expected artifacts:",
        ]
    )
    lines.extend(f"- `{item}`" for item in brief.reproduction.artifacts)
    lines.extend(
        [
            "",
            "> NO OBSERVED OUTCOME → NO EPISODIC MEMORY UPDATE",
            "",
        ]
    )
    return "\n".join(lines)
