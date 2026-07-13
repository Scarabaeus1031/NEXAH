"""Network Orientation V1: descriptive structure, comparison, and learning context."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from nexah.backends import GraphAnalysis, GraphBackendResult, GraphEdge
from nexah.backends import GraphRepresentationBackend
from nexah.orientation import (
    Context,
    Option,
    OptionStatus,
    OrientationReport,
    Provenance,
)
from nexah.orientation.base import ContractModel, require_text
from nexah.sources import GraphSchema, GraphSourceAdapter


@dataclass(frozen=True, slots=True, kw_only=True)
class PathChange(ContractModel):
    """Shortest-path change between two declared graph snapshots."""

    node: str
    baseline_path: tuple[str, ...] | None
    current_path: tuple[str, ...] | None

    def __post_init__(self) -> None:
        require_text(self.node, "node")


@dataclass(frozen=True, slots=True, kw_only=True)
class GraphComparison(ContractModel):
    """Purely structural delta between a baseline and a current graph."""

    baseline_representation_id: str
    current_representation_id: str
    focus: str
    target: str | None
    added_nodes: tuple[str, ...]
    removed_nodes: tuple[str, ...]
    added_edges: tuple[GraphEdge, ...]
    removed_edges: tuple[GraphEdge, ...]
    changed_edge_weights: tuple[tuple[GraphEdge, GraphEdge], ...]
    newly_reachable: tuple[str, ...]
    newly_unreachable: tuple[str, ...]
    path_changes: tuple[PathChange, ...]
    baseline_evidence_ids: tuple[str, ...]
    current_evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        require_text(self.baseline_representation_id, "baseline_representation_id")
        require_text(self.current_representation_id, "current_representation_id")
        require_text(self.focus, "focus")
        if self.target is not None:
            require_text(self.target, "target")


@dataclass(frozen=True, slots=True, kw_only=True)
class NetworkOrientationResult(ContractModel):
    """Machine-readable output of the Network Orientation V1 application."""

    orientation: OrientationReport
    structure: GraphAnalysis
    comparison: GraphComparison | None = None
    application_id: str = "network-orientation-v1"
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        require_text(self.application_id, "application_id")
        require_text(self.schema_version, "schema_version")
        if self.orientation.position is None:
            raise ValueError("network orientation requires a focus position")
        if (
            self.orientation.position.identifier.scope
            != self.structure.representation_id
        ):
            raise ValueError("report and structure representation IDs must match")


class NetworkOrientationApplication:
    """Run one graph through source, representation, and report boundaries."""

    def __init__(self, schema: GraphSchema | None = None) -> None:
        self.source_adapter = GraphSourceAdapter(schema)
        self.backend = GraphRepresentationBackend()

    def orient(
        self,
        source: Mapping[str, Any],
        *,
        analysis_id: str,
        provenance: Provenance,
        context: Context,
        focus: str,
        target: str | None = None,
        baseline_source: Mapping[str, Any] | None = None,
        baseline_provenance: Provenance | None = None,
    ) -> NetworkOrientationResult:
        current = self._adapt(
            source,
            analysis_id=analysis_id,
            provenance=provenance,
            context=context,
            focus=focus,
            target=target,
        )
        comparison = None
        if baseline_source is not None:
            baseline = self._adapt(
                baseline_source,
                analysis_id=f"{analysis_id}:baseline",
                provenance=baseline_provenance or provenance,
                context=context,
                focus=focus,
                target=target,
            )
            comparison = compare_graph_results(baseline, current)
        return NetworkOrientationResult(
            orientation=_generate_network_report(current, comparison),
            structure=current.analysis,
            comparison=comparison,
        )

    def _adapt(
        self,
        source: Mapping[str, Any],
        *,
        analysis_id: str,
        provenance: Provenance,
        context: Context,
        focus: str,
        target: str | None,
    ) -> GraphBackendResult:
        batch = self.source_adapter.adapt(
            source,
            batch_id=f"{analysis_id}:source",
            provenance=provenance,
            context=context,
        )
        return self.backend.adapt(
            batch,
            analysis_id=analysis_id,
            focus=focus,
            target=target,
        )


def compare_graph_results(
    baseline: GraphBackendResult,
    current: GraphBackendResult,
) -> GraphComparison:
    """Compare topology without interpreting a perturbation as causal evidence."""

    left = baseline.analysis
    right = current.analysis
    if left.focus != right.focus:
        raise ValueError("graph comparison requires the same focus node")
    if left.target != right.target:
        raise ValueError("graph comparison requires the same target node")

    left_edges = {(edge.source, edge.target): edge for edge in left.edges}
    right_edges = {(edge.source, edge.target): edge for edge in right.edges}
    left_keys = set(left_edges)
    right_keys = set(right_edges)
    shared_keys = left_keys & right_keys
    changed = tuple(
        (left_edges[key], right_edges[key])
        for key in sorted(shared_keys)
        if left_edges[key].weight != right_edges[key].weight
    )
    all_path_nodes = set(left.shortest_paths) | set(right.shortest_paths)
    path_changes = tuple(
        PathChange(
            node=node,
            baseline_path=left.shortest_paths.get(node),
            current_path=right.shortest_paths.get(node),
        )
        for node in sorted(all_path_nodes)
        if left.shortest_paths.get(node) != right.shortest_paths.get(node)
    )
    return GraphComparison(
        baseline_representation_id=left.representation_id,
        current_representation_id=right.representation_id,
        focus=left.focus,
        target=left.target,
        added_nodes=tuple(sorted(set(right.nodes) - set(left.nodes))),
        removed_nodes=tuple(sorted(set(left.nodes) - set(right.nodes))),
        added_edges=tuple(right_edges[key] for key in sorted(right_keys - left_keys)),
        removed_edges=tuple(left_edges[key] for key in sorted(left_keys - right_keys)),
        changed_edge_weights=changed,
        newly_reachable=tuple(
            sorted(set(right.reachable_nodes) - set(left.reachable_nodes))
        ),
        newly_unreachable=tuple(
            sorted(set(left.reachable_nodes) - set(right.reachable_nodes))
        ),
        path_changes=path_changes,
        baseline_evidence_ids=tuple(
            item.evidence_id for item in baseline.state.evidence
        ),
        current_evidence_ids=tuple(item.evidence_id for item in current.state.evidence),
    )


def remove_declared_edge(
    source: Mapping[str, Any],
    source_node: str,
    target_node: str,
    *,
    schema: GraphSchema | None = None,
) -> dict[str, Any]:
    """Return a minimal scenario graph with one declared edge removed."""

    graph_schema = schema or GraphSchema()
    require_text(source_node, "source_node")
    require_text(target_node, "target_node")
    raw_nodes = source.get(graph_schema.nodes_key)
    raw_edges = source.get(graph_schema.edges_key)
    if isinstance(raw_nodes, (str, bytes)) or not isinstance(raw_nodes, Sequence):
        raise ValueError("scenario source requires a node sequence")
    if isinstance(raw_edges, (str, bytes)) or not isinstance(raw_edges, Sequence):
        raise ValueError("scenario source requires an edge sequence")
    retained: list[Mapping[str, Any]] = []
    removed = 0
    for edge in raw_edges:
        if not isinstance(edge, Mapping):
            raise ValueError("scenario edges must be mappings")
        if (
            edge.get(graph_schema.source_key) == source_node
            and edge.get(graph_schema.target_key) == target_node
        ):
            removed += 1
        else:
            retained.append(dict(edge))
    if removed != 1:
        raise ValueError(
            "scenario edge removal requires exactly one matching declared edge"
        )
    return {
        graph_schema.nodes_key: list(raw_nodes),
        graph_schema.edges_key: retained,
    }


def _generate_network_report(
    result: GraphBackendResult,
    comparison: GraphComparison | None,
) -> OrientationReport:
    state = result.state
    analysis = result.analysis
    assert state.location is not None
    evidence_ids = tuple(item.evidence_id for item in state.evidence)
    reachable = tuple(
        Option(
            option_id=f"{analysis.representation_id}:node-option:{node}",
            description=(
                f"A declared directed path exists from {analysis.focus} to {node}. "
                "This is structural reachability, not a recommendation, desired "
                "outcome, or claim of physical feasibility."
            ),
            status=OptionStatus.REACHABLE,
            evidence_ids=evidence_ids,
        )
        for node in analysis.reachable_nodes
    )
    blocked = tuple(
        Option(
            option_id=f"{analysis.representation_id}:node-option:{node}",
            description=(
                f"No declared directed path exists from {analysis.focus} to {node} "
                "in this snapshot. Absence from the map does not establish real-world "
                "impossibility."
            ),
            status=OptionStatus.BLOCKED,
            evidence_ids=evidence_ids,
        )
        for node in analysis.blocked_nodes
    )
    changes = _change_statements(analysis, comparison)
    missing = [
        "Independent evidence that the declared graph is complete",
        "Domain semantics and measurement uncertainty for nodes and edges",
        "Observed outcomes linking structural changes to system behavior",
        "Causal evidence for any intervention or training effect",
    ]
    if comparison is None:
        missing.append("A second observed or declared scenario snapshot for comparison")
    if analysis.target is None:
        missing.append("An explicit structural target for target-path reporting")
    assumptions = (
        "Every non-zero adjacency entry is treated as one declared directed edge.",
        "Missing edges mean absent from this source, not impossible in reality.",
        "Reachability and bottlenecks are structural descriptions, not stability scores.",
        "Snapshot comparison is a learning context, not proof of causal response.",
    )
    target_statement = "No target was requested."
    if analysis.target is not None:
        target_statement = (
            f"Target {analysis.target} is structurally reachable by the shortest "
            f"declared path {' → '.join(analysis.target_path)}."
            if analysis.target_path is not None
            else f"Target {analysis.target} is not reachable in this declared graph."
        )
    explanation = (
        f"From focus {analysis.focus}, {len(analysis.reachable_nodes)} node(s) are "
        f"reachable and {len(analysis.blocked_nodes)} node(s) are blocked within "
        f"the declared directed graph. {target_statement} The analysis identifies "
        f"{len(analysis.weak_articulation_points)} weak articulation point(s) and "
        f"{len(analysis.focus_critical_edges)} focus-relative critical edge(s). "
        "These are exact topology statements for the supplied snapshot with "
        "qualitative uncertainty about source completeness and domain meaning."
    )
    return OrientationReport(
        position=state.location,
        change=changes,
        regimes=tuple(),
        reachable_options=reachable,
        blocked_options=blocked,
        similar_episodes=state.episodes,
        missing_information=tuple(missing),
        assumptions=assumptions,
        evidence_references=evidence_ids,
        uncertainty=state.uncertainty,
        explanation=explanation,
        timestamp=state.timestamp,
        provenance=Provenance(
            source=state.provenance.source,
            method="network-orientation-report-generator-v1",
            recorded_at=state.timestamp,
            record_id=f"{analysis.representation_id}:network-report",
            metadata={
                "representation_id": analysis.representation_id,
                "backend": state.representation.backend,
                "comparison_present": comparison is not None,
            },
        ),
    )


def _change_statements(
    analysis: GraphAnalysis,
    comparison: GraphComparison | None,
) -> tuple[str, ...]:
    if comparison is None:
        return (
            "One graph snapshot was supplied; no temporal or scenario change is established.",
        )
    statements = [
        f"The comparison contains {len(comparison.added_edges)} added and "
        f"{len(comparison.removed_edges)} removed directed edge(s)."
    ]
    if comparison.changed_edge_weights:
        statements.append(
            f"{len(comparison.changed_edge_weights)} retained edge(s) changed weight."
        )
    if comparison.newly_unreachable:
        statements.append(
            "Newly unreachable from the declared focus: "
            + ", ".join(comparison.newly_unreachable)
            + "."
        )
    if comparison.newly_reachable:
        statements.append(
            "Newly reachable from the declared focus: "
            + ", ".join(comparison.newly_reachable)
            + "."
        )
    if not comparison.newly_unreachable and not comparison.newly_reachable:
        statements.append(
            "The set of reachable nodes is unchanged, although paths may differ."
        )
    if comparison.path_changes:
        statements.append(
            f"Shortest declared paths changed for {len(comparison.path_changes)} node(s)."
        )
    return tuple(statements)


def render_network_orientation_text(result: NetworkOrientationResult) -> str:
    """Render a compact human-readable companion to the JSON contract."""

    analysis = result.structure
    lines = [
        "NEXAH Network Orientation V1",
        f"Focus: {analysis.focus}",
        f"Target: {analysis.target or 'not declared'}",
        f"Reachable: {', '.join(analysis.reachable_nodes) or 'none'}",
        f"Blocked: {', '.join(analysis.blocked_nodes) or 'none'}",
        f"Dead ends: {', '.join(analysis.dead_ends) or 'none'}",
        (
            "Weak articulation points: "
            + (", ".join(analysis.weak_articulation_points) or "none")
        ),
        "Focus-critical edges: "
        + (
            ", ".join(
                f"{edge.source}->{edge.target}"
                for edge in analysis.focus_critical_edges
            )
            or "none"
        ),
    ]
    if analysis.target is not None:
        lines.append(
            "Target path: "
            + (
                " -> ".join(analysis.target_path)
                if analysis.target_path is not None
                else "blocked"
            )
        )
    if result.comparison is not None:
        lines.extend(
            [
                "Comparison: structural sensitivity scenario",
                "Newly unreachable: "
                + (", ".join(result.comparison.newly_unreachable) or "none"),
                "Newly reachable: "
                + (", ".join(result.comparison.newly_reachable) or "none"),
            ]
        )
    lines.extend(
        [
            "",
            result.orientation.explanation,
            "Boundary: learning from declared structure; no control or causal claim.",
        ]
    )
    return "\n".join(lines)
