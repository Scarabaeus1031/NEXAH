"""Read-only perspectives over a Network Orientation V1 result."""

from __future__ import annotations

from dataclasses import dataclass

from nexah.orientation import (
    FindingStance,
    ProbeFinding,
    ProbeResult,
    ProbeSynthesis,
    Provenance,
    synthesize_probe_results,
)
from nexah.orientation.base import ContractModel, require_text

from .network_orientation import NetworkOrientationResult


@dataclass(frozen=True, slots=True, kw_only=True)
class NetworkLearningContext(ContractModel):
    """V2 wrapper: one network result plus inspectable probe perspectives."""

    network_orientation: NetworkOrientationResult
    synthesis: ProbeSynthesis
    learning_mode: str = "comparative-observation"
    outcome_recorded: bool = False
    application_id: str = "network-orientation-v2-probes"
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        require_text(self.learning_mode, "learning_mode")
        require_text(self.application_id, "application_id")
        require_text(self.schema_version, "schema_version")
        if self.outcome_recorded:
            raise ValueError(
                "probe synthesis cannot claim an outcome without an observed Outcome"
            )
        if (
            self.network_orientation.structure.representation_id
            != self.synthesis.representation_id
        ):
            raise ValueError("network result and probe synthesis must share identity")


class ReachabilityProbe:
    probe_id = "network-reachability-probe-v1"

    def evaluate(self, result: NetworkOrientationResult) -> ProbeResult:
        analysis = result.structure
        evidence = result.orientation.evidence_references
        findings = [
            ProbeFinding(
                finding_id=f"{self.probe_id}:reachability",
                subject="declared-reachability",
                statement=(
                    f"From {analysis.focus}, {len(analysis.reachable_nodes)} node(s) "
                    f"are reachable and {len(analysis.blocked_nodes)} are blocked in "
                    "the supplied directed graph."
                ),
                stance=FindingStance.OBSERVED,
                evidence_ids=evidence,
            )
        ]
        missing: list[str] = []
        if analysis.target is None:
            findings.append(
                ProbeFinding(
                    finding_id=f"{self.probe_id}:target-unknown",
                    subject="target-reachability",
                    statement="No target was declared for a target-path assessment.",
                    stance=FindingStance.UNKNOWN,
                    evidence_ids=evidence,
                )
            )
            missing.append("A declared target node")
        else:
            reachable = analysis.target_path is not None
            findings.append(
                ProbeFinding(
                    finding_id=f"{self.probe_id}:target",
                    subject="target-reachability",
                    statement=(
                        f"Target {analysis.target} has a declared directed path from "
                        f"{analysis.focus}."
                        if reachable
                        else f"Target {analysis.target} has no declared directed path "
                        f"from {analysis.focus} in this snapshot."
                    ),
                    stance=(
                        FindingStance.SUPPORTED
                        if reachable
                        else FindingStance.CHALLENGED
                    ),
                    evidence_ids=evidence,
                )
            )
        return _probe_result(
            self.probe_id,
            "directed reachability and paths",
            result,
            tuple(findings),
            tuple(missing),
            ("Reachability is evaluated only over declared directed edges.",),
        )


class BottleneckProbe:
    probe_id = "network-bottleneck-probe-v1"

    def evaluate(self, result: NetworkOrientationResult) -> ProbeResult:
        analysis = result.structure
        evidence = result.orientation.evidence_references
        critical = ", ".join(
            f"{edge.source}->{edge.target}"
            for edge in analysis.focus_critical_edges
        ) or "none"
        finding = ProbeFinding(
            finding_id=f"{self.probe_id}:structural",
            subject="structural-bottlenecks",
            statement=(
                "Weak articulation points: "
                f"{', '.join(analysis.weak_articulation_points) or 'none'}; "
                f"focus-relative critical edges: {critical}."
            ),
            stance=FindingStance.OBSERVED,
            evidence_ids=evidence,
        )
        return _probe_result(
            self.probe_id,
            "structural bottlenecks",
            result,
            (finding,),
            ("Evidence that topological bottlenecks are operational bottlenecks",),
            (
                "Articulation is computed on the weak undirected projection; critical "
                "edges are relative to the declared focus.",
            ),
        )


class PerturbationProbe:
    probe_id = "network-perturbation-probe-v1"

    def evaluate(self, result: NetworkOrientationResult) -> ProbeResult:
        comparison = result.comparison
        current_evidence = result.orientation.evidence_references
        if comparison is None:
            finding = ProbeFinding(
                finding_id=f"{self.probe_id}:comparison-unknown",
                subject="structural-sensitivity",
                statement="Only one graph snapshot is available; no delta is assessed.",
                stance=FindingStance.UNKNOWN,
                evidence_ids=current_evidence,
            )
            return _probe_result(
                self.probe_id,
                "declared snapshot comparison",
                result,
                (finding,),
                ("A baseline or second declared graph snapshot",),
                ("No perturbation effect is inferred from a single snapshot.",),
            )

        evidence = tuple(
            sorted(
                set(comparison.baseline_evidence_ids)
                | set(comparison.current_evidence_ids)
            )
        )
        findings = [
            ProbeFinding(
                finding_id=f"{self.probe_id}:delta",
                subject="structural-sensitivity",
                statement=(
                    f"The declared comparison has {len(comparison.added_edges)} added, "
                    f"{len(comparison.removed_edges)} removed, and "
                    f"{len(comparison.changed_edge_weights)} reweighted edge(s); "
                    f"{len(comparison.newly_unreachable)} node(s) became unreachable."
                ),
                stance=FindingStance.OBSERVED,
                evidence_ids=evidence,
            )
        ]
        if result.structure.target is not None:
            target_reachable = result.structure.target_path is not None
            findings.append(
                ProbeFinding(
                    finding_id=f"{self.probe_id}:target",
                    subject="target-reachability",
                    statement=(
                        "The target remains reachable in the current declared snapshot."
                        if target_reachable
                        else "The target is unreachable in the current declared snapshot."
                    ),
                    stance=(
                        FindingStance.SUPPORTED
                        if target_reachable
                        else FindingStance.CHALLENGED
                    ),
                    evidence_ids=evidence,
                )
            )
        return _probe_result(
            self.probe_id,
            "declared snapshot comparison",
            result,
            tuple(findings),
            ("Observed outcomes following the declared structural difference",),
            ("A structural delta is a training scenario, not a causal intervention.",),
        )


class EvidenceProbe:
    probe_id = "network-evidence-probe-v1"

    def evaluate(self, result: NetworkOrientationResult) -> ProbeResult:
        references = result.orientation.evidence_references
        findings = [
            ProbeFinding(
                finding_id=f"{self.probe_id}:traceability",
                subject="evidence-traceability",
                statement=(
                    f"The report exposes {len(references)} current evidence reference(s) "
                    "and explicit provenance."
                ),
                stance=FindingStance.SUPPORTED,
                evidence_ids=references,
            ),
            ProbeFinding(
                finding_id=f"{self.probe_id}:completeness",
                subject="source-completeness",
                statement=(
                    "No independent evidence establishes that the declared graph is a "
                    "complete model of the external domain."
                ),
                stance=FindingStance.LIMITATION,
                evidence_ids=references,
            ),
        ]
        return _probe_result(
            self.probe_id,
            "provenance, evidence, and uncertainty",
            result,
            tuple(findings),
            ("Independent source-completeness and measurement evidence",),
            ("Presence of provenance does not establish source validity.",),
        )


class CriticProbe:
    probe_id = "network-claim-critic-probe-v1"

    def evaluate(self, result: NetworkOrientationResult) -> ProbeResult:
        evidence = result.orientation.evidence_references
        subjects = (
            ("stability-claim", "Graph topology alone does not establish stability."),
            ("causal-effect", "Snapshot comparison does not establish causal effect."),
            (
                "real-world-generalization",
                "Illustrative fixtures do not establish real-world generalization.",
            ),
            ("control-authority", "This result provides no execution authority."),
        )
        findings = tuple(
            ProbeFinding(
                finding_id=f"{self.probe_id}:{subject}",
                subject=subject,
                statement=statement,
                stance=FindingStance.LIMITATION,
                evidence_ids=evidence,
            )
            for subject, statement in subjects
        )
        return _probe_result(
            self.probe_id,
            "claim-boundary criticism",
            result,
            findings,
            (
                "Observed outcomes, external validation, and an authorization model "
                "for any later action",
            ),
            ("The critic evaluates claim scope, not domain truth.",),
        )


def run_network_probe_suite(
    result: NetworkOrientationResult,
) -> NetworkLearningContext:
    """Run five independent perspectives and retain their full outputs."""

    probes = (
        ReachabilityProbe(),
        BottleneckProbe(),
        PerturbationProbe(),
        EvidenceProbe(),
        CriticProbe(),
    )
    probe_results = tuple(probe.evaluate(result) for probe in probes)
    provenance = Provenance(
        source=result.orientation.provenance.source,
        method="read-only network probe synthesis v1",
        recorded_at=result.orientation.timestamp,
        record_id=f"{result.structure.representation_id}:probe-synthesis",
        metadata={
            "probe_count": len(probe_results),
            "aggregation": "preserve-all-findings-no-majority-vote",
        },
    )
    return NetworkLearningContext(
        network_orientation=result,
        synthesis=synthesize_probe_results(probe_results, provenance=provenance),
    )


def render_network_learning_text(context: NetworkLearningContext) -> str:
    """Render probe perspectives without hiding limits or disagreements."""

    lines = [
        "NEXAH Network Orientation V2 — Multi-Perspective Learning",
        f"Representation: {context.synthesis.representation_id}",
        f"Read-only probes: {len(context.synthesis.probe_results)}",
        f"Agreements: {len(context.synthesis.agreements)}",
        f"Contradictions: {len(context.synthesis.contradictions)}",
        f"Limitations: {len(context.synthesis.limitation_finding_ids)}",
    ]
    for result in context.synthesis.probe_results:
        lines.append(f"\n[{result.perspective}]")
        lines.extend(
            f"- {finding.stance.value}: {finding.statement}"
            for finding in result.findings
        )
    lines.extend(
        [
            "",
            "Learning boundary: findings are preserved, not voted into truth.",
            "No observed Outcome is recorded; episodic memory remains untouched.",
            "No probe has command or execution authority.",
        ]
    )
    return "\n".join(lines)


def _probe_result(
    probe_id: str,
    perspective: str,
    result: NetworkOrientationResult,
    findings: tuple[ProbeFinding, ...],
    missing_information: tuple[str, ...],
    assumptions: tuple[str, ...],
) -> ProbeResult:
    return ProbeResult(
        probe_id=probe_id,
        perspective=perspective,
        representation_id=result.structure.representation_id,
        findings=findings,
        missing_information=missing_information,
        assumptions=assumptions,
        uncertainty=result.orientation.uncertainty,
        provenance=Provenance(
            source=result.orientation.provenance.source,
            method=probe_id,
            recorded_at=result.orientation.timestamp,
            record_id=f"{result.structure.representation_id}:{probe_id}",
            metadata={"read_only": True},
        ),
    )
