"""Evidence-bound representation backend for declared directed graphs."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable

from nexah.orientation import (
    Context,
    Evidence,
    EvidenceKind,
    MapRef,
    MapScope,
    Observation,
    OrientationState,
    Provenance,
    ReferenceFrame,
    RepresentationRef,
    ScopedIdentifier,
    StateRef,
    Transition,
    Uncertainty,
    UncertaintyKind,
)
from nexah.orientation.base import ContractModel, require_text
from nexah.sources import SourceAxis, SourceBatch

from .base import BackendAdapterError


@dataclass(frozen=True, slots=True, kw_only=True)
class GraphEdge(ContractModel):
    """One declared directed edge in a graph representation."""

    source: str
    target: str
    weight: float = 1.0

    def __post_init__(self) -> None:
        require_text(self.source, "source")
        require_text(self.target, "target")


@dataclass(frozen=True, slots=True, kw_only=True)
class GraphAnalysis(ContractModel):
    """Descriptive topology computed from one declared graph snapshot."""

    representation_id: str
    focus: str
    target: str | None
    nodes: tuple[str, ...]
    edges: tuple[GraphEdge, ...]
    reachable_nodes: tuple[str, ...]
    blocked_nodes: tuple[str, ...]
    shortest_paths: dict[str, tuple[str, ...]]
    target_path: tuple[str, ...] | None
    in_degree: dict[str, int]
    out_degree: dict[str, int]
    dead_ends: tuple[str, ...]
    strongly_connected_components: tuple[tuple[str, ...], ...]
    weakly_connected_components: tuple[tuple[str, ...], ...]
    weak_articulation_points: tuple[str, ...]
    focus_critical_edges: tuple[GraphEdge, ...]

    def __post_init__(self) -> None:
        require_text(self.representation_id, "representation_id")
        require_text(self.focus, "focus")
        if self.target is not None:
            require_text(self.target, "target")
        if self.focus not in self.nodes:
            raise ValueError("focus must be present in graph nodes")
        if self.target is not None and self.target not in self.nodes:
            raise ValueError("target must be present in graph nodes")


@dataclass(frozen=True, slots=True, kw_only=True)
class GraphBackendResult(ContractModel):
    """Orientation state and descriptive artifacts for one graph snapshot."""

    state: OrientationState
    transitions: tuple[Transition, ...]
    analysis: GraphAnalysis

    def __post_init__(self) -> None:
        if self.state.representation.representation_id != self.analysis.representation_id:
            raise ValueError("state and graph analysis representation IDs must match")


class GraphRepresentationBackend:
    """Translate an entity-indexed adjacency batch into scoped graph evidence."""

    @property
    def backend_id(self) -> str:
        return "declared-directed-graph-v1"

    def adapt(
        self,
        batch: SourceBatch,
        *,
        analysis_id: str,
        focus: str,
        target: str | None = None,
    ) -> GraphBackendResult:
        require_text(analysis_id, "analysis_id")
        require_text(focus, "focus")
        if target is not None:
            require_text(target, "target")
        nodes, edges = self._validate_batch(batch)
        if focus not in nodes:
            raise BackendAdapterError(f"focus node is absent from graph: {focus}")
        if target is not None and target not in nodes:
            raise BackendAdapterError(f"target node is absent from graph: {target}")

        representation_id = f"{analysis_id}:declared-graph"
        evidence_id = f"{analysis_id}:declared-graph-observation"
        uncertainty = Uncertainty(
            kind=UncertaintyKind.QUALITATIVE,
            value=None,
            basis=(
                "Topology is exact for the declared nodes and non-zero adjacency "
                "entries; source completeness, domain meaning, and external "
                "validity are not established."
            ),
        )
        analysis = _analyze_graph(
            representation_id=representation_id,
            nodes=nodes,
            edges=edges,
            focus=focus,
            target=target,
        )
        representation = RepresentationRef(
            backend=self.backend_id,
            method="declared-adjacency-topology-v1",
            scope=MapScope.PERSISTENT,
            representation_id=representation_id,
            parameters={
                "node_count": len(nodes),
                "edge_count": len(edges),
                "row_axis": batch.row_axis.value,
                "node_identity": "declared-source-identifiers",
                "weighted": any(edge.weight != 1.0 for edge in edges),
            },
        )
        evidence = Evidence(
            evidence_id=evidence_id,
            claim=(
                "The source declares a directed graph whose topology supports "
                "the attached reachability and connectivity description."
            ),
            kind=EvidenceKind.COMPUTATION,
            provenance=batch.provenance,
            uncertainty=uncertainty,
            payload={
                "source_batch_id": batch.batch_id,
                "source_quality": batch.quality.to_dict(),
                "nodes": list(nodes),
                "edges": [edge.to_dict() for edge in edges],
                "reachable_nodes": list(analysis.reachable_nodes),
                "blocked_nodes": list(analysis.blocked_nodes),
                "limitations": [
                    "non-zero adjacency entries are interpreted as declared edges",
                    "missing edges mean absent from this source, not impossible",
                    "topology alone does not establish stability, risk, or causality",
                ],
            },
        )
        state = OrientationState(
            observations=tuple(
                Observation(
                    observation_id=f"{analysis_id}:node:{node}",
                    value=list(batch.values[index]),
                    variable="outgoing_adjacency",
                    observed_at=batch.provenance.recorded_at,
                    provenance=batch.provenance,
                )
                for index, node in enumerate(nodes)
            ),
            representation=representation,
            reference_frame=ReferenceFrame(
                frame_id=f"{analysis_id}:declared-node-frame",
                description=(
                    "Declared node identifiers and directed adjacency; no latent "
                    "embedding or temporal ordering is inferred"
                ),
                scale="entity",
            ),
            context=batch.context,
            uncertainty=uncertainty,
            timestamp=batch.provenance.recorded_at,
            provenance=batch.provenance,
            location=_state_ref(focus, representation_id, "declared graph focus"),
            map=MapRef(
                map_id=f"{analysis_id}:structural-map",
                scope=MapScope.PERSISTENT,
                representation_id=representation_id,
                description="Directed structural map of the declared graph snapshot",
            ),
            evidence=(evidence,),
        )
        transitions = tuple(
            Transition(
                source=_state_ref(edge.source, representation_id),
                target=_state_ref(edge.target, representation_id),
                probability=None,
                evidence_ids=(evidence_id,),
            )
            for edge in edges
        )
        return GraphBackendResult(
            state=state,
            transitions=transitions,
            analysis=analysis,
        )

    def _validate_batch(
        self, batch: SourceBatch
    ) -> tuple[tuple[str, ...], tuple[GraphEdge, ...]]:
        if batch.row_axis is not SourceAxis.ENTITY:
            raise BackendAdapterError("graph backend requires the entity row axis")
        if not batch.row_ids:
            raise BackendAdapterError("graph backend requires declared row IDs")
        nodes = batch.row_ids
        if len(batch.values) != len(nodes) or len(batch.features) != len(nodes):
            raise BackendAdapterError("graph adjacency must be square")
        expected_features = tuple(f"edge_to:{node}" for node in nodes)
        actual_features = tuple(feature.name for feature in batch.features)
        if actual_features != expected_features:
            raise BackendAdapterError(
                "graph features must align with row IDs as edge_to:<node>"
            )
        edges = tuple(
            GraphEdge(source=source, target=target, weight=float(weight))
            for source, row in zip(nodes, batch.values)
            for target, weight in zip(nodes, row)
            if weight != 0.0
        )
        return nodes, edges


def _state_ref(value: str, scope: str, label: str | None = None) -> StateRef:
    return StateRef(
        identifier=ScopedIdentifier(value=value, scope=scope),
        label=label,
    )


def _analyze_graph(
    *,
    representation_id: str,
    nodes: tuple[str, ...],
    edges: tuple[GraphEdge, ...],
    focus: str,
    target: str | None,
) -> GraphAnalysis:
    adjacency = _adjacency(nodes, edges)
    reverse = _reverse_adjacency(nodes, adjacency)
    paths = _shortest_paths(focus, adjacency)
    reachable = tuple(sorted(set(paths) - {focus}))
    blocked = tuple(sorted(set(nodes) - set(paths)))
    in_degree = {node: len(reverse[node]) for node in nodes}
    out_degree = {node: len(adjacency[node]) for node in nodes}
    target_path = paths.get(target) if target is not None else None
    return GraphAnalysis(
        representation_id=representation_id,
        focus=focus,
        target=target,
        nodes=nodes,
        edges=edges,
        reachable_nodes=reachable,
        blocked_nodes=blocked,
        shortest_paths={node: paths[node] for node in sorted(paths)},
        target_path=target_path,
        in_degree=in_degree,
        out_degree=out_degree,
        dead_ends=tuple(sorted(node for node in nodes if not adjacency[node])),
        strongly_connected_components=_strong_components(nodes, adjacency, reverse),
        weakly_connected_components=_weak_components(nodes, adjacency),
        weak_articulation_points=_weak_articulation_points(nodes, adjacency),
        focus_critical_edges=_focus_critical_edges(nodes, edges, focus, set(paths)),
    )


def _adjacency(
    nodes: Iterable[str], edges: Iterable[GraphEdge]
) -> dict[str, set[str]]:
    adjacency: dict[str, set[str]] = {node: set() for node in nodes}
    for edge in edges:
        adjacency[edge.source].add(edge.target)
    return adjacency


def _reverse_adjacency(
    nodes: Iterable[str], adjacency: dict[str, set[str]]
) -> dict[str, set[str]]:
    reverse: dict[str, set[str]] = {node: set() for node in nodes}
    for source, targets in adjacency.items():
        for target in targets:
            reverse[target].add(source)
    return reverse


def _shortest_paths(
    start: str, adjacency: dict[str, set[str]]
) -> dict[str, tuple[str, ...]]:
    paths: dict[str, tuple[str, ...]] = {start: (start,)}
    queue = deque([start])
    while queue:
        source = queue.popleft()
        for target in sorted(adjacency[source]):
            if target not in paths:
                paths[target] = paths[source] + (target,)
                queue.append(target)
    return paths


def _strong_components(
    nodes: tuple[str, ...],
    adjacency: dict[str, set[str]],
    reverse: dict[str, set[str]],
) -> tuple[tuple[str, ...], ...]:
    visited: set[str] = set()
    order: list[str] = []

    def visit(node: str) -> None:
        visited.add(node)
        for target in sorted(adjacency[node]):
            if target not in visited:
                visit(target)
        order.append(node)

    for node in nodes:
        if node not in visited:
            visit(node)

    visited.clear()
    components: list[tuple[str, ...]] = []

    def collect(node: str, component: list[str]) -> None:
        visited.add(node)
        component.append(node)
        for source in sorted(reverse[node]):
            if source not in visited:
                collect(source, component)

    for node in reversed(order):
        if node not in visited:
            component: list[str] = []
            collect(node, component)
            components.append(tuple(sorted(component)))
    return tuple(sorted(components))


def _weak_components(
    nodes: tuple[str, ...], adjacency: dict[str, set[str]]
) -> tuple[tuple[str, ...], ...]:
    undirected = _undirected(nodes, adjacency)
    remaining = set(nodes)
    components: list[tuple[str, ...]] = []
    while remaining:
        start = min(remaining)
        visited = {start}
        queue = deque([start])
        while queue:
            source = queue.popleft()
            for target in sorted(undirected[source]):
                if target not in visited:
                    visited.add(target)
                    queue.append(target)
        remaining -= visited
        components.append(tuple(sorted(visited)))
    return tuple(sorted(components))


def _undirected(
    nodes: tuple[str, ...], adjacency: dict[str, set[str]]
) -> dict[str, set[str]]:
    undirected: dict[str, set[str]] = {node: set() for node in nodes}
    for source, targets in adjacency.items():
        for target in targets:
            undirected[source].add(target)
            undirected[target].add(source)
    return undirected


def _weak_articulation_points(
    nodes: tuple[str, ...], adjacency: dict[str, set[str]]
) -> tuple[str, ...]:
    undirected = _undirected(nodes, adjacency)
    discovery: dict[str, int] = {}
    low: dict[str, int] = {}
    parent: dict[str, str | None] = {}
    points: set[str] = set()
    time = 0

    def visit(node: str) -> None:
        nonlocal time
        discovery[node] = time
        low[node] = time
        time += 1
        children = 0
        for neighbor in sorted(undirected[node]):
            if neighbor not in discovery:
                parent[neighbor] = node
                children += 1
                visit(neighbor)
                low[node] = min(low[node], low[neighbor])
                if parent[node] is None and children > 1:
                    points.add(node)
                if parent[node] is not None and low[neighbor] >= discovery[node]:
                    points.add(node)
            elif neighbor != parent[node]:
                low[node] = min(low[node], discovery[neighbor])

    for node in nodes:
        if node not in discovery:
            parent[node] = None
            visit(node)
    return tuple(sorted(points))


def _focus_critical_edges(
    nodes: tuple[str, ...],
    edges: tuple[GraphEdge, ...],
    focus: str,
    baseline_reachable: set[str],
) -> tuple[GraphEdge, ...]:
    critical: list[GraphEdge] = []
    for candidate in edges:
        remaining = tuple(edge for edge in edges if edge != candidate)
        reachable = set(_shortest_paths(focus, _adjacency(nodes, remaining)))
        if not baseline_reachable <= reachable:
            critical.append(candidate)
    return tuple(critical)
