"""Tests for the declared directed-graph source boundary."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

import numpy as np
import pytest

from nexah.orientation import Context, Provenance
from nexah.sources import (
    GraphSchema,
    GraphSourceAdapter,
    SourceAdapterError,
    SourceAxis,
    SourceBatch,
)


ROOT = Path(__file__).parents[2]
RECORDED_AT = datetime(2026, 7, 13, 22, 0, tzinfo=timezone.utc)
PROVENANCE = Provenance(
    source="repository:APPLICATIONS/datasets",
    method="declared graph fixture",
    recorded_at=RECORDED_AT,
)


@pytest.mark.parametrize(
    ("filename", "excluded_values"),
    [
        ("supply_chain.json", ("increase_inventory", "supplier_shutdown")),
        ("ecosystem_food_web.json", ("reintroduce_predators", "drought")),
    ],
)
def test_repository_graphs_preserve_only_declared_topology(
    filename: str, excluded_values: tuple[str, ...]
) -> None:
    source = json.loads((ROOT / "APPLICATIONS" / "datasets" / filename).read_text())
    batch = GraphSourceAdapter().adapt(
        source,
        batch_id=f"graph:{filename}",
        provenance=PROVENANCE,
        context=Context(domain=str(source["name"]), values={"status": "illustrative"}),
    )

    assert batch.row_axis is SourceAxis.ENTITY
    assert batch.row_ids == tuple(source["nodes"])
    assert batch.to_numpy().shape == (5, 5)
    assert int(np.sum(batch.to_numpy())) == len(source["edges"])
    serialized = json.dumps(batch.to_dict()).lower()
    assert all(value not in serialized for value in excluded_values)
    assert "excluded undeclared graph metadata" in serialized


def test_graph_batch_round_trips_and_preserves_direction() -> None:
    source = {
        "nodes": ["supplier", "factory", "customer"],
        "edges": [
            {"from": "supplier", "to": "factory"},
            {"from": "factory", "to": "customer"},
        ],
    }
    batch = GraphSourceAdapter().adapt(
        source,
        batch_id="directed-fixture",
        provenance=PROVENANCE,
        context=Context(domain="supply-chain"),
    )
    restored = SourceBatch.from_dict(json.loads(json.dumps(batch.to_dict())))

    assert restored == batch
    assert batch.to_numpy().tolist() == [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0],
    ]


def test_weighted_graph_requires_declared_finite_weights() -> None:
    adapter = GraphSourceAdapter(GraphSchema(weight_key="flow"))
    batch = adapter.adapt(
        {
            "nodes": ["a", "b"],
            "edges": [{"from": "a", "to": "b", "flow": 0.75}],
        },
        batch_id="weighted",
        provenance=PROVENANCE,
        context=Context(domain="weighted-graph"),
    )

    assert batch.values == ((0.0, 0.75), (0.0, 0.0))
    assert all(feature.unit == "weight" for feature in batch.features)

    with pytest.raises(SourceAdapterError, match="finite"):
        adapter.adapt(
            {
                "nodes": ["a", "b"],
                "edges": [{"from": "a", "to": "b", "flow": float("nan")}],
            },
            batch_id="invalid-weight",
            provenance=PROVENANCE,
            context=Context(domain="weighted-graph"),
        )


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ({"nodes": [], "edges": []}, "contain nodes"),
        ({"nodes": ["a", "a"], "edges": []}, "unique"),
        (
            {"nodes": ["a"], "edges": [{"from": "a", "to": "b"}]},
            "unknown nodes",
        ),
        (
            {
                "nodes": ["a", "b"],
                "edges": [
                    {"from": "a", "to": "b"},
                    {"from": "a", "to": "b"},
                ],
            },
            "duplicate directed",
        ),
    ],
)
def test_invalid_graphs_fail_visibly(source: object, message: str) -> None:
    with pytest.raises(SourceAdapterError, match=message):
        GraphSourceAdapter().adapt(
            source,  # type: ignore[arg-type]
            batch_id="invalid",
            provenance=PROVENANCE,
            context=Context(domain="invalid-graph"),
        )
