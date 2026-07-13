"""Schema-driven source adapter for declared directed graphs."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import isfinite
from typing import Any

from nexah.orientation import Context, Provenance
from nexah.orientation.base import ContractModel, require_text

from .base import (
    SourceAdapterError,
    SourceAxis,
    SourceBatch,
    SourceFeature,
    SourceQuality,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class GraphSchema(ContractModel):
    """Explicit keys used to extract one directed graph source."""

    nodes_key: str = "nodes"
    edges_key: str = "edges"
    source_key: str = "from"
    target_key: str = "to"
    weight_key: str | None = None

    def __post_init__(self) -> None:
        for value in (
            self.nodes_key,
            self.edges_key,
            self.source_key,
            self.target_key,
        ):
            require_text(value, "graph schema key")
        if self.weight_key is not None:
            require_text(self.weight_key, "weight_key")
        if self.source_key == self.target_key:
            raise ValueError("source and target keys must differ")


class GraphSourceAdapter:
    """Encode only declared nodes and edges as a directed adjacency batch.

    Regime labels, risk targets, actions, shock names, and other graph metadata
    are intentionally outside this source boundary.
    """

    def __init__(self, schema: GraphSchema | None = None) -> None:
        self.schema = schema or GraphSchema()

    @property
    def adapter_id(self) -> str:
        return "directed-graph-adjacency-source-v1"

    def adapt(
        self,
        source: Mapping[str, Any],
        *,
        batch_id: str,
        provenance: Provenance,
        context: Context,
    ) -> SourceBatch:
        if not isinstance(source, Mapping):
            raise SourceAdapterError("graph source must be a mapping")
        if self.schema.nodes_key not in source:
            raise SourceAdapterError(
                f"graph source is missing nodes key: {self.schema.nodes_key}"
            )
        if self.schema.edges_key not in source:
            raise SourceAdapterError(
                f"graph source is missing edges key: {self.schema.edges_key}"
            )
        nodes = self._nodes(source[self.schema.nodes_key])
        node_index = {node: index for index, node in enumerate(nodes)}
        edges = self._edges(source[self.schema.edges_key], node_index)
        values = [[0.0 for _ in nodes] for _ in nodes]
        for source_node, target_node, weight in edges:
            values[node_index[source_node]][node_index[target_node]] = weight

        ignored = sorted(
            str(key)
            for key in source
            if key not in {self.schema.nodes_key, self.schema.edges_key}
        )
        transformations = [
            "encoded declared directed edges as a node-by-node adjacency matrix"
        ]
        if ignored:
            transformations.append(
                "excluded undeclared graph metadata keys: " + ", ".join(ignored)
            )
        return SourceBatch(
            batch_id=batch_id,
            values=tuple(tuple(row) for row in values),
            features=tuple(
                SourceFeature(
                    name=f"edge_to:{node}",
                    unit="weight" if self.schema.weight_key is not None else "binary",
                    description=f"declared directed edge from row node to {node}",
                )
                for node in nodes
            ),
            context=context,
            provenance=provenance,
            quality=SourceQuality(
                input_rows=len(nodes),
                output_rows=len(nodes),
                missing_values=0,
                non_finite_values=0,
                transformations=tuple(transformations),
            ),
            row_axis=SourceAxis.ENTITY,
            row_ids=nodes,
        )

    def _nodes(self, raw_nodes: object) -> tuple[str, ...]:
        if isinstance(raw_nodes, (str, bytes)) or not isinstance(raw_nodes, Sequence):
            raise SourceAdapterError("graph nodes must be a sequence of identifiers")
        nodes = tuple(raw_nodes)
        if not nodes:
            raise SourceAdapterError("graph source must contain nodes")
        if any(not isinstance(node, str) or not node.strip() for node in nodes):
            raise SourceAdapterError("graph node identifiers must be non-empty strings")
        if len(nodes) != len(set(nodes)):
            raise SourceAdapterError("graph node identifiers must be unique")
        return nodes

    def _edges(
        self, raw_edges: object, node_index: Mapping[str, int]
    ) -> tuple[tuple[str, str, float], ...]:
        if isinstance(raw_edges, (str, bytes)) or not isinstance(raw_edges, Sequence):
            raise SourceAdapterError("graph edges must be a sequence of mappings")
        parsed: list[tuple[str, str, float]] = []
        seen: set[tuple[str, str]] = set()
        for edge in raw_edges:
            if not isinstance(edge, Mapping):
                raise SourceAdapterError("every graph edge must be a mapping")
            try:
                source_node = edge[self.schema.source_key]
                target_node = edge[self.schema.target_key]
            except KeyError as error:
                raise SourceAdapterError(
                    "graph edge is missing its declared source or target key"
                ) from error
            if not isinstance(source_node, str) or not isinstance(target_node, str):
                raise SourceAdapterError("graph edge endpoints must be strings")
            unknown = {source_node, target_node} - set(node_index)
            if unknown:
                raise SourceAdapterError(
                    "graph edge references unknown nodes: "
                    + ", ".join(sorted(unknown))
                )
            identity = (source_node, target_node)
            if identity in seen:
                raise SourceAdapterError(
                    f"duplicate directed graph edge: {source_node} -> {target_node}"
                )
            seen.add(identity)
            weight = 1.0
            if self.schema.weight_key is not None:
                if self.schema.weight_key not in edge:
                    raise SourceAdapterError(
                        f"weighted graph edge is missing: {self.schema.weight_key}"
                    )
                try:
                    weight = float(edge[self.schema.weight_key])
                except (TypeError, ValueError) as error:
                    raise SourceAdapterError("graph edge weights must be numeric") from error
                if not isfinite(weight):
                    raise SourceAdapterError("graph edge weights must be finite")
            parsed.append((source_node, target_node, weight))
        return tuple(parsed)
