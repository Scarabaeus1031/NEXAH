"""Read-only multi-perspective probe contracts for orientation results."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .base import ContractModel, require_text
from .evidence import Provenance, Uncertainty


class FindingStance(str, Enum):
    """How one probe relates its evidence to a narrowly stated subject."""

    OBSERVED = "observed"
    SUPPORTED = "supported"
    CHALLENGED = "challenged"
    LIMITATION = "limitation"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True, kw_only=True)
class ProbeFinding(ContractModel):
    """One traceable statement made by a read-only analytical perspective."""

    finding_id: str
    subject: str
    statement: str
    stance: FindingStance
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_text(self.finding_id, "finding_id")
        require_text(self.subject, "subject")
        require_text(self.statement, "statement")


@dataclass(frozen=True, slots=True, kw_only=True)
class ProbeResult(ContractModel):
    """Evidence-bound output of one perspective; never an execution command."""

    probe_id: str
    perspective: str
    representation_id: str
    findings: tuple[ProbeFinding, ...]
    missing_information: tuple[str, ...]
    assumptions: tuple[str, ...]
    uncertainty: Uncertainty
    provenance: Provenance
    read_only: bool = True
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        require_text(self.probe_id, "probe_id")
        require_text(self.perspective, "perspective")
        require_text(self.representation_id, "representation_id")
        require_text(self.schema_version, "schema_version")
        if not self.read_only:
            raise ValueError("orientation probes must be read-only")
        identifiers = [finding.finding_id for finding in self.findings]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("probe finding IDs must be unique")


@dataclass(frozen=True, slots=True, kw_only=True)
class ProbeAgreement(ContractModel):
    """Two or more probes independently take the same stance on a subject."""

    subject: str
    stance: FindingStance
    probe_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        require_text(self.subject, "subject")
        if len(set(self.probe_ids)) < 2:
            raise ValueError("probe agreement requires at least two probes")


@dataclass(frozen=True, slots=True, kw_only=True)
class ProbeContradiction(ContractModel):
    """Visible support/challenge disagreement that requires human review."""

    subject: str
    supporting_probe_ids: tuple[str, ...]
    challenging_probe_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        require_text(self.subject, "subject")
        if not self.supporting_probe_ids or not self.challenging_probe_ids:
            raise ValueError("contradiction requires support and challenge")


@dataclass(frozen=True, slots=True, kw_only=True)
class ProbeSynthesis(ContractModel):
    """Transparent collation of perspectives without majority-vote truth."""

    representation_id: str
    probe_results: tuple[ProbeResult, ...]
    agreements: tuple[ProbeAgreement, ...]
    contradictions: tuple[ProbeContradiction, ...]
    limitation_finding_ids: tuple[str, ...]
    evidence_references: tuple[str, ...]
    provenance: Provenance
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        require_text(self.representation_id, "representation_id")
        require_text(self.schema_version, "schema_version")
        if not self.probe_results:
            raise ValueError("probe synthesis requires at least one probe result")
        probe_ids = [result.probe_id for result in self.probe_results]
        if len(probe_ids) != len(set(probe_ids)):
            raise ValueError("probe IDs must be unique within one synthesis")
        mismatched = {
            result.representation_id
            for result in self.probe_results
            if result.representation_id != self.representation_id
        }
        if mismatched:
            raise ValueError("all probes must describe the same representation")


def synthesize_probe_results(
    results: tuple[ProbeResult, ...],
    *,
    provenance: Provenance,
) -> ProbeSynthesis:
    """Collate agreements and contradictions while preserving every finding."""

    if not results:
        raise ValueError("at least one probe result is required")
    representation_id = results[0].representation_id
    by_subject: dict[str, dict[FindingStance, set[str]]] = {}
    limitations: list[str] = []
    evidence_ids: set[str] = set()
    for result in results:
        if result.representation_id != representation_id:
            raise ValueError("cannot synthesize different representations")
        for finding in result.findings:
            by_subject.setdefault(finding.subject, {}).setdefault(
                finding.stance, set()
            ).add(result.probe_id)
            evidence_ids.update(finding.evidence_ids)
            if finding.stance is FindingStance.LIMITATION:
                limitations.append(finding.finding_id)

    agreements = tuple(
        ProbeAgreement(
            subject=subject,
            stance=stance,
            probe_ids=tuple(sorted(probe_ids)),
        )
        for subject, stances in sorted(by_subject.items())
        for stance, probe_ids in sorted(stances.items(), key=lambda item: item[0].value)
        if len(probe_ids) >= 2
    )
    contradictions = tuple(
        ProbeContradiction(
            subject=subject,
            supporting_probe_ids=tuple(sorted(stances[FindingStance.SUPPORTED])),
            challenging_probe_ids=tuple(sorted(stances[FindingStance.CHALLENGED])),
        )
        for subject, stances in sorted(by_subject.items())
        if FindingStance.SUPPORTED in stances
        and FindingStance.CHALLENGED in stances
    )
    return ProbeSynthesis(
        representation_id=representation_id,
        probe_results=results,
        agreements=agreements,
        contradictions=contradictions,
        limitation_finding_ids=tuple(sorted(limitations)),
        evidence_references=tuple(sorted(evidence_ids)),
        provenance=provenance,
    )
