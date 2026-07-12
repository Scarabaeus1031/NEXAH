"""Evidence-bound generation of the first NEXAH Orientation Report."""

from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from nexah.backends.base import BackendResult

from .evidence import Provenance, UncertaintyKind
from .primitives import MapScope, Option, OptionStatus, StateRef, Transition
from .report import OrientationReport


class ReportGenerationError(ValueError):
    """Raised when a backend result cannot support a coherent report."""


class OrientationReportGenerator:
    """Describe backend evidence without adding domain or causal semantics."""

    generator_id = "orientation-report-generator-v1"

    def generate(self, result: BackendResult) -> OrientationReport:
        self._validate(result)
        state = result.state
        assert state.location is not None  # established by _validate

        current = state.location.identifier.value
        scope = state.representation.representation_id
        evidence_ids = tuple(evidence.evidence_id for evidence in state.evidence)
        reachable, blocked = self._classify_reachability(
            current=current,
            transitions=result.transitions,
        )

        reachable_options = tuple(
            self._option(
                target=target,
                current=current,
                scope=scope,
                status=OptionStatus.REACHABLE,
                evidence_ids=evidence_ids,
            )
            for target in sorted(reachable)
        )
        blocked_options = tuple(
            self._option(
                target=target,
                current=current,
                scope=scope,
                status=OptionStatus.BLOCKED,
                evidence_ids=evidence_ids,
            )
            for target in sorted(blocked)
        )

        change = self._change_statements(result)
        missing_information = self._missing_information(result)
        assumptions = self._assumptions(result)
        explanation = self._explanation(
            state.location,
            len(reachable_options),
            len(blocked_options),
            result.raw_output,
        )
        report_provenance = Provenance(
            source=state.provenance.source,
            method=self.generator_id,
            recorded_at=state.timestamp,
            record_id=f"{scope}:orientation-report",
            metadata={
                "input_record_id": state.provenance.record_id,
                "representation_id": scope,
                "backend": state.representation.backend,
            },
        )

        return OrientationReport(
            position=state.location,
            change=change,
            regimes=result.regimes,
            reachable_options=reachable_options,
            blocked_options=blocked_options,
            similar_episodes=state.episodes,
            missing_information=missing_information,
            assumptions=assumptions,
            evidence_references=evidence_ids,
            uncertainty=state.uncertainty,
            explanation=explanation,
            timestamp=state.timestamp,
            provenance=report_provenance,
        )

    def _validate(self, result: BackendResult) -> None:
        state = result.state
        if state.location is None:
            raise ReportGenerationError("backend result has no current location")
        if state.map is None:
            raise ReportGenerationError("backend result has no map reference")
        if not state.evidence:
            raise ReportGenerationError("backend result has no evidence")

        scope = state.representation.representation_id
        if state.location.identifier.scope != scope:
            raise ReportGenerationError("current location scope does not match representation")

        known_evidence = {evidence.evidence_id for evidence in state.evidence}
        for transition in result.transitions:
            if transition.source.identifier.scope != scope:
                raise ReportGenerationError("transition source scope does not match representation")
            if transition.target.identifier.scope != scope:
                raise ReportGenerationError("transition target scope does not match representation")
            unknown = set(transition.evidence_ids) - known_evidence
            if unknown:
                names = ", ".join(sorted(unknown))
                raise ReportGenerationError(
                    f"transition references unknown evidence: {names}"
                )

    def _classify_reachability(
        self,
        *,
        current: str,
        transitions: tuple[Transition, ...],
    ) -> tuple[set[str], set[str]]:
        nodes = {current}
        adjacency: dict[str, set[str]] = {}
        for transition in transitions:
            source = transition.source.identifier.value
            target = transition.target.identifier.value
            nodes.update((source, target))
            adjacency.setdefault(source, set()).add(target)

        visited = {current}
        queue = deque([current])
        while queue:
            source = queue.popleft()
            for target in sorted(adjacency.get(source, set())):
                if target not in visited:
                    visited.add(target)
                    queue.append(target)

        reachable = visited - {current}
        blocked = nodes - visited
        return reachable, blocked

    def _option(
        self,
        *,
        target: str,
        current: str,
        scope: str,
        status: OptionStatus,
        evidence_ids: tuple[str, ...],
    ) -> Option:
        if status is OptionStatus.REACHABLE:
            description = (
                f"An observed directed path exists from local state {current} "
                f"to local state {target}; feasibility outside this fitted map "
                "is not established."
            )
        else:
            description = (
                f"No directed path from local state {current} to local state "
                f"{target} exists in the observed transition map; impossibility "
                "outside this fitted map is not established."
            )
        return Option(
            option_id=f"{scope}:state-option:{target}",
            description=description,
            status=status,
            evidence_ids=evidence_ids,
        )

    def _change_statements(self, result: BackendResult) -> tuple[str, ...]:
        shifts = result.raw_output.get("regime_shifts", [])
        zones = result.raw_output.get("regime_zones", [])
        statements: list[str] = []

        if shifts:
            last_embedded = int(shifts[-1])
            last_raw_anchor = result.alignment.raw_anchor(last_embedded)
            statements.append(
                f"v0.7 recorded {len(shifts)} local-cluster label changes in "
                "the embedded sequence."
            )
            statements.append(
                f"The last recorded label change is at embedded index "
                f"{last_embedded}, aligned to source-sample anchor "
                f"{last_raw_anchor}."
            )
        else:
            statements.append(
                "v0.7 recorded no local-cluster label changes in the embedded sequence."
            )

        if zones:
            statements.append(
                f"v0.7 aggregated {len(zones)} high-instability embedded-index "
                "zone(s); these are not externally validated regimes."
            )
        return tuple(statements)

    def _missing_information(self, result: BackendResult) -> tuple[str, ...]:
        state = result.state
        missing: list[str] = []
        if state.uncertainty.kind is UncertaintyKind.UNKNOWN:
            missing.append("Calibrated uncertainty for v0.7 state and transition claims")
        if state.representation.scope is MapScope.LOCAL_FIT:
            missing.append("Persistent state identity and cross-run state alignment")
        if not result.regimes:
            missing.append("Externally validated regime semantics")
        if not state.goals:
            missing.append("Goal criteria for ranking reachable options")
        if not state.constraints:
            missing.append("Domain constraints for evaluating feasible options")
        if not state.representation.parameters.get("timestamps_provided", False):
            missing.append("Source observation timestamps")
        missing.append("Causal evidence for interventions or real-world transitions")
        return tuple(missing)

    def _assumptions(self, result: BackendResult) -> tuple[str, ...]:
        assumptions = [
            "Cluster identifiers are meaningful only within this local v0.7 fit.",
            (
                "Graph reachability means only that a directed path exists in "
                "the empirical transition map."
            ),
            (
                "A local-cluster label change is a representational event, not "
                "an externally confirmed system transition."
            ),
        ]
        if not result.state.representation.parameters.get("timestamps_provided", False):
            assumptions.append(
                "Observation order is represented by source sample index because "
                "acquisition timestamps were not supplied."
            )
        return tuple(assumptions)

    def _explanation(
        self,
        position: StateRef,
        reachable_count: int,
        blocked_count: int,
        raw_output: dict[str, Any],
    ) -> str:
        shifts = len(raw_output.get("regime_shifts", []))
        return (
            f"Within this local v0.7 fit, the current represented position is "
            f"state {position.identifier.value}. The empirical graph contains "
            f"{reachable_count} other reachable observed state(s) and "
            f"{blocked_count} observed state(s) without a directed path from "
            f"the current state. The embedded label sequence contains {shifts} "
            "recorded change(s). These statements are descriptive, locally "
            "scoped, and carry uncalibrated uncertainty."
        )


def generate_orientation_report(result: BackendResult) -> OrientationReport:
    """Convenience entry point for the default report generator."""

    return OrientationReportGenerator().generate(result)
