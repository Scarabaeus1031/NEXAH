"""Read-only perspectives and report binding for Phase V IEEE geometry."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from nexah.orientation import (
    FindingStance,
    OrientationReport,
    ProbeFinding,
    ProbeResult,
    ProbeSynthesis,
    Provenance,
    ScopedIdentifier,
    StateRef,
    synthesize_probe_results,
)
from nexah.orientation.base import ContractModel, require_text

from .ieee_geometry import (
    IEEEEntityView,
    IEEEFrameStatus,
    IEEEGeometryCampaign,
    IEEEGeometryFrame,
)
from .ieee_geometry_operators import (
    IEEEGeometryAnalysis,
    IEEEGeometryValueStatus,
)
from .ieee_manifest import IEEEGeometryCaseManifest


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEGeometryLearningContext(ContractModel):
    """One Phase V geometry analysis plus five preserved perspectives."""

    analysis: IEEEGeometryAnalysis
    report: OrientationReport
    synthesis: ProbeSynthesis
    outcome_recorded: bool = False
    application_id: str = "ieee-geometry-orientation-probes-v1"
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        require_text(self.application_id, "application_id")
        require_text(self.schema_version, "schema_version")
        if self.outcome_recorded:
            raise ValueError(
                "benchmark geometry probes cannot record an observed outcome"
            )
        if self.synthesis.representation_id != self.analysis.campaign_id:
            raise ValueError("probe synthesis must share the campaign identity")
        if self.report.position is not None and (
            self.report.position.identifier.scope != self.analysis.campaign_id
        ):
            raise ValueError("report position must share the campaign identity")


class IEEEPhysicalStateProbe:
    probe_id = "ieee-physical-state-probe-v1"

    def evaluate(
        self,
        campaign: IEEEGeometryCampaign,
        analysis: IEEEGeometryAnalysis,
        manifest: IEEEGeometryCaseManifest,
    ) -> ProbeResult:
        converged = tuple(
            frame for frame in campaign.frames if frame.status is IEEEFrameStatus.CONVERGED
        )
        failed = tuple(
            frame for frame in campaign.frames if frame.status is IEEEFrameStatus.FAILED
        )
        evidence = _evidence_ids(campaign, analysis)
        findings = [
            ProbeFinding(
                finding_id=f"{self.probe_id}:frame-status",
                subject="physical-frame-availability",
                statement=(
                    f"The declared {campaign.case_id} campaign contains "
                    f"{len(converged)} converged physical frame(s) and "
                    f"{len(failed)} explicit failed frame(s) across "
                    f"{len(campaign.frames)} ordered load-scale positions."
                ),
                stance=FindingStance.OBSERVED,
                evidence_ids=evidence,
            )
        ]
        missing: list[str] = []
        if converged:
            last = converged[-1]
            summary = _physical_summary(last)
            if summary is None:
                findings.append(
                    ProbeFinding(
                        finding_id=f"{self.probe_id}:last-frame-incomplete",
                        subject="last-converged-physical-state",
                        statement=(
                            "The last converged frame lacks one or more variables "
                            "needed for the compact voltage/loading summary."
                        ),
                        stance=FindingStance.UNKNOWN,
                        evidence_ids=evidence,
                    )
                )
                missing.append("Aligned bus voltage and line loading variables")
            else:
                min_vm, max_vm, max_loading = summary
                findings.append(
                    ProbeFinding(
                        finding_id=f"{self.probe_id}:last-frame",
                        subject="last-converged-physical-state",
                        statement=(
                            f"At the last converged sampled position λ={last.load_scale:g}, "
                            f"bus voltage magnitude spans {min_vm:.6g}–{max_vm:.6g} pu "
                            f"and maximum declared line loading is "
                            f"{max_loading:.6g} percent."
                        ),
                        stance=FindingStance.OBSERVED,
                        evidence_ids=evidence,
                    )
                )
        else:
            findings.append(
                ProbeFinding(
                    finding_id=f"{self.probe_id}:no-converged-frame",
                    subject="last-converged-physical-state",
                    statement="No converged physical frame is available for inspection.",
                    stance=FindingStance.UNKNOWN,
                    evidence_ids=evidence,
                )
            )
            missing.append("At least one converged physical frame")
        return _probe_result(
            self.probe_id,
            "physical state and solver-visible variables",
            campaign,
            analysis,
            tuple(findings),
            tuple(missing),
            (
                "Each position is an independent steady-state benchmark computation.",
                "A failed solver position contains no fabricated physical values.",
            ),
        )


class IEEEGeometryProbe:
    probe_id = "ieee-geometry-probe-v1"

    def evaluate(
        self,
        campaign: IEEEGeometryCampaign,
        analysis: IEEEGeometryAnalysis,
        manifest: IEEEGeometryCaseManifest,
    ) -> ProbeResult:
        evidence = _evidence_ids(campaign, analysis)
        available_steps = tuple(
            step
            for step in analysis.steps
            if step.status is IEEEGeometryValueStatus.AVAILABLE
        )
        available_turns = tuple(
            turn
            for turn in analysis.turns
            if turn.status is IEEEGeometryValueStatus.AVAILABLE
        )
        findings = [
            ProbeFinding(
                finding_id=f"{self.probe_id}:coverage",
                subject="sampled-geometry-coverage",
                statement=(
                    f"The frozen operators return {len(available_steps)} available "
                    f"adjacent measurement(s) and {len(available_turns)} available "
                    "centered direction/curvature measurement(s)."
                ),
                stance=FindingStance.OBSERVED,
                evidence_ids=evidence,
            )
        ]
        missing: list[str] = []
        if available_steps:
            maximum = max(
                available_steps,
                key=lambda step: step.normalized_local_drift or 0.0,
            )
            assert maximum.normalized_local_drift is not None
            findings.append(
                ProbeFinding(
                    finding_id=f"{self.probe_id}:maximum-drift",
                    subject="sampled-local-drift",
                    statement=(
                        "The largest sampled normalized local drift is "
                        f"{maximum.normalized_local_drift:.6g} between "
                        f"λ={maximum.source_load_scale:g} and "
                        f"λ={maximum.target_load_scale:g}."
                    ),
                    stance=FindingStance.OBSERVED,
                    evidence_ids=evidence,
                )
            )
        else:
            findings.append(
                ProbeFinding(
                    finding_id=f"{self.probe_id}:drift-insufficient",
                    subject="sampled-local-drift",
                    statement="No adjacent projected pair supports a drift value.",
                    stance=FindingStance.UNKNOWN,
                    evidence_ids=evidence,
                )
            )
            missing.append("At least two aligned, available projected frames")
        if available_turns:
            maximum_turn = max(
                available_turns,
                key=lambda turn: turn.discrete_curvature or 0.0,
            )
            assert maximum_turn.discrete_curvature is not None
            findings.append(
                ProbeFinding(
                    finding_id=f"{self.probe_id}:maximum-curvature",
                    subject="sampled-discrete-curvature",
                    statement=(
                        "The largest sampled discrete curvature is "
                        f"{maximum_turn.discrete_curvature:.6g} at campaign index "
                        f"{maximum_turn.center_index}."
                    ),
                    stance=FindingStance.OBSERVED,
                    evidence_ids=evidence,
                )
            )
        findings.append(
            ProbeFinding(
                finding_id=f"{self.probe_id}:projection-comparison",
                subject="cross-projection-agreement",
                statement=(
                    "No agreement or disagreement between declared projections is "
                    "computed because the frozen protocol declares no comparison metric."
                ),
                stance=FindingStance.UNKNOWN,
                evidence_ids=evidence,
            )
        )
        missing.append("A prospectively declared cross-projection comparison metric")
        return _probe_result(
            self.probe_id,
            "sampled geometry along the declared load parameter",
            campaign,
            analysis,
            tuple(findings),
            tuple(missing),
            (
                "Geometry is measured in the frozen standardized system-summary view.",
                "Load-scale adjacency is not interpreted as elapsed physical time.",
            ),
        )


class IEEEBoundaryProbe:
    probe_id = "ieee-boundary-probe-v1"

    def evaluate(
        self,
        campaign: IEEEGeometryCampaign,
        analysis: IEEEGeometryAnalysis,
        manifest: IEEEGeometryCaseManifest,
    ) -> ProbeResult:
        evidence = _evidence_ids(campaign, analysis)
        available = tuple(
            boundary
            for boundary in analysis.solver_boundaries
            if boundary.status is IEEEGeometryValueStatus.AVAILABLE
        )
        findings: list[ProbeFinding] = []
        missing: list[str] = []
        if available:
            first = available[0]
            assert first.last_converged_load_scale is not None
            assert first.distance_load_scale is not None
            findings.append(
                ProbeFinding(
                    finding_id=f"{self.probe_id}:first-failure",
                    subject="sampled-solver-boundary",
                    statement=(
                        f"The first explicit solver failure occurs at λ="
                        f"{first.failed_load_scale:g}, following the last converged "
                        f"sample at λ={first.last_converged_load_scale:g}; the sampled "
                        f"load-scale gap is {first.distance_load_scale:.6g}."
                    ),
                    stance=FindingStance.OBSERVED,
                    evidence_ids=evidence,
                )
            )
        else:
            findings.append(
                ProbeFinding(
                    finding_id=f"{self.probe_id}:no-bracket",
                    subject="sampled-solver-boundary",
                    statement=(
                        "The campaign contains no failed position with a preceding "
                        "converged sample."
                    ),
                    stance=FindingStance.UNKNOWN,
                    evidence_ids=evidence,
                )
            )
            missing.append("A converged-to-failed sampled bracket")
        findings.append(
            ProbeFinding(
                finding_id=f"{self.probe_id}:physical-limit",
                subject="physical-stability-boundary",
                statement=(
                    "Pandapower non-convergence and its sampled bracket do not certify "
                    "a physical voltage-stability boundary."
                ),
                stance=FindingStance.LIMITATION,
                evidence_ids=evidence,
            )
        )
        missing.extend(
            (
                "A declared boundary-refinement protocol beyond the frozen grid",
                "Independent physical stability evidence",
            )
        )
        return _probe_result(
            self.probe_id,
            "solver boundary and sampling resolution",
            campaign,
            analysis,
            tuple(findings),
            tuple(missing),
            ("Boundary distance is reported only in the declared load-scale parameter.",),
        )


class IEEEEvidenceProbe:
    probe_id = "ieee-evidence-probe-v1"

    def evaluate(
        self,
        campaign: IEEEGeometryCampaign,
        analysis: IEEEGeometryAnalysis,
        manifest: IEEEGeometryCaseManifest,
    ) -> ProbeResult:
        evidence = _evidence_ids(campaign, analysis)
        model = analysis.projection_model
        findings = (
            ProbeFinding(
                finding_id=f"{self.probe_id}:traceability",
                subject="evidence-traceability",
                statement=(
                    f"Manifest {manifest.manifest_id}, campaign "
                    f"{campaign.campaign_id}, geometry analysis, and the "
                    f"standardization fitted on {model.fit_case_id} retain explicit "
                    "identities and provenance."
                ),
                stance=FindingStance.SUPPORTED,
                evidence_ids=evidence,
            ),
            ProbeFinding(
                finding_id=f"{self.probe_id}:uncertainty",
                subject="calibrated-uncertainty",
                statement=(
                    f"Uncertainty remains {analysis.uncertainty.kind.value}; no "
                    "calibrated physical or probabilistic uncertainty is attached."
                ),
                stance=FindingStance.LIMITATION,
                evidence_ids=evidence,
            ),
            ProbeFinding(
                finding_id=f"{self.probe_id}:outcome",
                subject="observed-outcome",
                statement=(
                    "The input is benchmark-model evidence and the result is a "
                    "computation; no independently observed outcome is recorded."
                ),
                stance=FindingStance.LIMITATION,
                evidence_ids=evidence,
            ),
        )
        return _probe_result(
            self.probe_id,
            "provenance, uncertainty, and evaluation leakage",
            campaign,
            analysis,
            findings,
            (
                "Calibrated uncertainty",
                "Independent operational measurements and observed outcomes",
            ),
            (
                "Manifest roles and the development fit identity are authoritative.",
                "Provenance supports traceability but does not establish external validity.",
            ),
        )


class IEEEClaimCriticProbe:
    probe_id = "ieee-claim-critic-probe-v1"

    def evaluate(
        self,
        campaign: IEEEGeometryCampaign,
        analysis: IEEEGeometryAnalysis,
        manifest: IEEEGeometryCaseManifest,
    ) -> ProbeResult:
        evidence = _evidence_ids(campaign, analysis)
        subjects = (
            "time-trajectory",
            "physical-stability-boundary",
            "causal-or-control-claim",
            "real-world-generalization",
            "global-manifold-or-field",
            "historically-untouched-evaluation",
            "observed-outcome",
        )
        findings = tuple(
            ProbeFinding(
                finding_id=f"{self.probe_id}:{index}",
                subject=subject,
                statement=f"The frozen manifest prohibits this interpretation: {claim}",
                stance=FindingStance.LIMITATION,
                evidence_ids=evidence,
            )
            for index, (subject, claim) in enumerate(
                zip(subjects, manifest.prohibited_claims), start=1
            )
        )
        return _probe_result(
            self.probe_id,
            "claim-boundary criticism",
            campaign,
            analysis,
            findings,
            (
                "External validation and observed outcomes for claims beyond the manifest",
            ),
            (
                "The critic checks claim scope and does not validate or reject domain truth.",
            ),
        )


def build_ieee_geometry_orientation_report(
    campaign: IEEEGeometryCampaign,
    analysis: IEEEGeometryAnalysis,
    manifest: IEEEGeometryCaseManifest,
) -> OrientationReport:
    """Describe the sampled campaign without adding planning or control semantics."""

    _validate_inputs(campaign, analysis, manifest)
    evidence = _evidence_ids(campaign, analysis)
    converged = tuple(
        frame for frame in campaign.frames if frame.status is IEEEFrameStatus.CONVERGED
    )
    available_steps = tuple(
        step
        for step in analysis.steps
        if step.status is IEEEGeometryValueStatus.AVAILABLE
    )
    changes = [
        f"{len(converged)} of {len(campaign.frames)} physical frames converged.",
        (
            f"{len(available_steps)} of {len(analysis.steps)} adjacent relations "
            "support frozen geometry measurements."
        ),
    ]
    if analysis.solver_boundaries:
        first = analysis.solver_boundaries[0]
        changes.append(
            f"The first recorded solver failure is at load scale "
            f"{first.failed_load_scale:g}."
        )
    position = None
    if converged:
        last = converged[-1]
        position = StateRef(
            identifier=ScopedIdentifier(
                value=last.frame_id,
                scope=campaign.campaign_id,
            ),
            label=f"last converged sampled position at load scale {last.load_scale:g}",
        )
    return OrientationReport(
        change=tuple(changes),
        reachable_options=(),
        blocked_options=(),
        missing_information=(
            "Dynamic trajectories between independently solved load cases",
            "A prospectively declared cross-projection comparison metric",
            "Calibrated physical or probabilistic uncertainty",
            "Independent operational measurements and observed outcomes",
        ),
        assumptions=(
            "The campaign axis is ordered load scale, not elapsed time.",
            "Frames are independent Pandapower steady-state benchmark computations.",
            "Solver non-convergence is a numerical result, not a certified physical limit.",
            "Geometry values describe the frozen standardized projection only.",
        ),
        evidence_references=evidence,
        uncertainty=analysis.uncertainty,
        explanation=(
            "This report locates the last converged sampled position and summarizes "
            "descriptive geometry and numerical boundaries in the declared IEEE "
            "benchmark campaign. It provides orientation, not prediction, causal "
            "attribution, control authority, or an operational-grid conclusion."
        ),
        timestamp=analysis.provenance.recorded_at,
        provenance=Provenance(
            source=analysis.provenance.source,
            method="IEEE geometry orientation report v1",
            recorded_at=analysis.provenance.recorded_at,
            record_id=f"{campaign.campaign_id}:orientation-report",
            metadata={
                "manifest_id": manifest.manifest_id,
                "geometry_analysis_id": analysis.provenance.record_id,
                "case_id": campaign.case_id,
                "case_role": campaign.case_role,
            },
        ),
        position=position,
    )


def run_ieee_geometry_probe_suite(
    campaign: IEEEGeometryCampaign,
    analysis: IEEEGeometryAnalysis,
    manifest: IEEEGeometryCaseManifest,
) -> IEEEGeometryLearningContext:
    """Run five independent read-only perspectives and preserve every finding."""

    _validate_inputs(campaign, analysis, manifest)
    probes = (
        IEEEPhysicalStateProbe(),
        IEEEGeometryProbe(),
        IEEEBoundaryProbe(),
        IEEEEvidenceProbe(),
        IEEEClaimCriticProbe(),
    )
    results = tuple(
        probe.evaluate(campaign, analysis, manifest) for probe in probes
    )
    report = build_ieee_geometry_orientation_report(campaign, analysis, manifest)
    synthesis = synthesize_probe_results(
        results,
        provenance=Provenance(
            source=analysis.provenance.source,
            method="read-only IEEE geometry probe synthesis v1",
            recorded_at=analysis.provenance.recorded_at,
            record_id=f"{campaign.campaign_id}:probe-synthesis",
            metadata={
                "manifest_id": manifest.manifest_id,
                "probe_count": len(results),
                "aggregation": "preserve-all-findings-no-majority-vote",
                "read_only": True,
            },
        ),
    )
    return IEEEGeometryLearningContext(
        analysis=analysis,
        report=report,
        synthesis=synthesis,
    )


def _probe_result(
    probe_id: str,
    perspective: str,
    campaign: IEEEGeometryCampaign,
    analysis: IEEEGeometryAnalysis,
    findings: tuple[ProbeFinding, ...],
    missing_information: tuple[str, ...],
    assumptions: tuple[str, ...],
) -> ProbeResult:
    return ProbeResult(
        probe_id=probe_id,
        perspective=perspective,
        representation_id=campaign.campaign_id,
        findings=findings,
        missing_information=missing_information,
        assumptions=assumptions,
        uncertainty=analysis.uncertainty,
        provenance=Provenance(
            source=analysis.provenance.source,
            method=probe_id,
            recorded_at=analysis.provenance.recorded_at,
            record_id=f"{campaign.campaign_id}:{probe_id}",
            metadata={"manifest_id": campaign.manifest_id, "read_only": True},
        ),
    )


def _validate_inputs(
    campaign: IEEEGeometryCampaign,
    analysis: IEEEGeometryAnalysis,
    manifest: IEEEGeometryCaseManifest,
) -> None:
    if campaign.manifest_id != manifest.manifest_id:
        raise ValueError("campaign and manifest identities differ")
    if analysis.manifest_id != manifest.manifest_id:
        raise ValueError("analysis and manifest identities differ")
    if analysis.campaign_id != campaign.campaign_id:
        raise ValueError("analysis and campaign identities differ")
    if analysis.case_id != campaign.case_id or analysis.case_role != campaign.case_role:
        raise ValueError("analysis and campaign case identities differ")


def _evidence_ids(
    campaign: IEEEGeometryCampaign,
    analysis: IEEEGeometryAnalysis,
) -> tuple[str, ...]:
    values = (
        campaign.provenance.record_id,
        analysis.projection_model.provenance.record_id,
        analysis.provenance.record_id,
    )
    return tuple(value for value in values if value is not None)


def _physical_summary(frame: IEEEGeometryFrame) -> tuple[float, float, float] | None:
    bus = _entity_view(frame, "bus")
    line = _entity_view(frame, "line")
    if bus is None or line is None:
        return None
    voltage = _column(bus, "vm_pu")
    loading = _column(line, "loading_percent")
    if not voltage or not loading:
        return None
    values = (min(voltage), max(voltage), max(loading))
    return values if all(isfinite(value) for value in values) else None


def _entity_view(frame: IEEEGeometryFrame, scope: str) -> IEEEEntityView | None:
    return next(
        (view for view in frame.entity_views if view.entity_scope == scope),
        None,
    )


def _column(view: IEEEEntityView, name: str) -> tuple[float, ...]:
    try:
        index = view.variable_names.index(name)
    except ValueError:
        return ()
    return tuple(row[index] for row in view.values)
