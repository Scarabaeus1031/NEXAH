"""Tests for the evidence-bound directed graph representation backend."""

from __future__ import annotations

from datetime import datetime, timezone
import json

import pytest

from nexah.backends import (
    BackendAdapterError,
    GraphBackendResult,
    GraphRepresentationBackend,
)
from nexah.orientation import Context, MapScope, Provenance, UncertaintyKind
from nexah.sources import ArraySourceAdapter, GraphSourceAdapter


NOW = datetime(2026, 7, 13, 22, 30, tzinfo=timezone.utc)
PROVENANCE = Provenance(
    source="graph-backend-fixture",
    method="declared test graph",
    recorded_at=NOW,
)


def graph_result() -> GraphBackendResult:
    source = {
        "nodes": ["a", "b", "c", "d", "e"],
        "edges": [
            {"from": "a", "to": "b"},
            {"from": "b", "to": "a"},
            {"from": "b", "to": "c"},
            {"from": "c", "to": "d"},
            {"from": "d", "to": "c"},
        ],
    }
    batch = GraphSourceAdapter().adapt(
        source,
        batch_id="graph-backend-source",
        provenance=PROVENANCE,
        context=Context(domain="graph-test"),
    )
    return GraphRepresentationBackend().adapt(
        batch,
        analysis_id="graph-backend",
        focus="a",
        target="d",
    )


def test_graph_backend_preserves_declared_identity_and_scope() -> None:
    result = graph_result()

    assert result.state.representation.scope is MapScope.PERSISTENT
    assert result.state.location is not None
    assert result.state.location.identifier.value == "a"
    assert result.state.uncertainty.kind is UncertaintyKind.QUALITATIVE
    assert all(transition.probability is None for transition in result.transitions)
    assert result.analysis.target_path == ("a", "b", "c", "d")


def test_graph_backend_computes_only_descriptive_topology() -> None:
    analysis = graph_result().analysis

    assert analysis.reachable_nodes == ("b", "c", "d")
    assert analysis.blocked_nodes == ("e",)
    assert analysis.dead_ends == ("e",)
    assert analysis.strongly_connected_components == (
        ("a", "b"),
        ("c", "d"),
        ("e",),
    )
    assert analysis.weakly_connected_components == (("a", "b", "c", "d"), ("e",))
    assert analysis.weak_articulation_points == ("b", "c")
    assert tuple((edge.source, edge.target) for edge in analysis.focus_critical_edges) == (
        ("a", "b"),
        ("b", "c"),
        ("c", "d"),
    )
    payload = json.dumps(graph_result().to_dict()).lower()
    assert "regime" not in payload
    assert "stability score" not in payload


def test_graph_backend_contract_round_trips() -> None:
    original = graph_result()

    restored = GraphBackendResult.from_dict(
        json.loads(json.dumps(original.to_dict()))
    )

    assert restored == original


def test_graph_backend_rejects_non_entity_batches_and_unknown_focus() -> None:
    array_batch = ArraySourceAdapter().adapt(
        [[0.0, 1.0], [1.0, 0.0]],
        batch_id="not-a-graph",
        provenance=PROVENANCE,
        context=Context(domain="array-test"),
    )
    with pytest.raises(BackendAdapterError, match="entity row axis"):
        GraphRepresentationBackend().adapt(
            array_batch,
            analysis_id="invalid",
            focus="a",
        )

    result_batch = GraphSourceAdapter().adapt(
        {"nodes": ["a"], "edges": []},
        batch_id="single-node",
        provenance=PROVENANCE,
        context=Context(domain="graph-test"),
    )
    with pytest.raises(BackendAdapterError, match="focus node"):
        GraphRepresentationBackend().adapt(
            result_batch,
            analysis_id="invalid-focus",
            focus="missing",
        )
