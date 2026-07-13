"""Tests for explicit tabular source translation."""

from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
import pytest

from nexah.orientation import Context, Provenance
from nexah.sources import (
    SourceAdapterError,
    SourceAxis,
    TableSchema,
    TableSourceAdapter,
)


RECORDED_AT = datetime(2026, 7, 13, 15, 0, tzinfo=timezone.utc)
PROVENANCE = Provenance(
    source="table-fixture",
    method="explicit DataFrame schema",
    recorded_at=RECORDED_AT,
)
CONTEXT = Context(domain="table-contract-test")


def test_table_adapter_selects_ordered_features_and_ignores_extra_columns() -> None:
    table = pd.DataFrame(
        {
            "time": ["2026-07-13T15:00:00Z", "2026-07-13T15:00:01Z"],
            "angle": [0.1, 0.2],
            "voltage": [1.0, 0.99],
            "evaluation_label": ["stable", "unstable"],
        }
    )
    schema = TableSchema(
        feature_columns=("voltage", "angle"),
        timestamp_column="time",
        units={"voltage": "pu", "angle": "rad"},
    )

    batch = TableSourceAdapter(schema).adapt(
        table,
        batch_id="table-001",
        provenance=PROVENANCE,
        context=CONTEXT,
    )

    assert batch.values == ((1.0, 0.1), (0.99, 0.2))
    assert tuple(feature.name for feature in batch.features) == (
        "voltage",
        "angle",
    )
    assert len(batch.timestamps) == 2
    assert all(timestamp.tzinfo is not None for timestamp in batch.timestamps)
    assert batch.row_axis is SourceAxis.TIME
    assert "evaluation_label" not in batch.to_dict()


def test_table_schema_rejects_ambiguous_declarations() -> None:
    with pytest.raises(ValueError, match="unique"):
        TableSchema(feature_columns=("x", "x"))
    with pytest.raises(ValueError, match="cannot also be a feature"):
        TableSchema(feature_columns=("time",), timestamp_column="time")
    with pytest.raises(ValueError, match="outside feature_columns"):
        TableSchema(feature_columns=("x",), units={"y": "m"})


def test_table_adapter_rejects_missing_and_non_numeric_features() -> None:
    adapter = TableSourceAdapter(TableSchema(feature_columns=("x", "y")))
    with pytest.raises(SourceAdapterError, match="missing required columns: y"):
        adapter.adapt(
            pd.DataFrame({"x": [1.0]}),
            batch_id="missing",
            provenance=PROVENANCE,
            context=CONTEXT,
        )
    with pytest.raises(SourceAdapterError, match="numeric"):
        adapter.adapt(
            pd.DataFrame({"x": [1.0], "y": ["not-a-number"]}),
            batch_id="non-numeric",
            provenance=PROVENANCE,
            context=CONTEXT,
        )


def test_table_adapter_rejects_naive_or_unordered_time() -> None:
    adapter = TableSourceAdapter(
        TableSchema(feature_columns=("x",), timestamp_column="time")
    )
    with pytest.raises(ValueError, match="timezone-aware"):
        adapter.adapt(
            pd.DataFrame(
                {"time": ["2026-07-13 15:00:00", "2026-07-13 15:00:01"], "x": [1, 2]}
            ),
            batch_id="naive",
            provenance=PROVENANCE,
            context=CONTEXT,
        )
    with pytest.raises(SourceAdapterError, match="strictly increasing"):
        adapter.adapt(
            pd.DataFrame(
                {"time": ["2026-07-13T15:00:01Z", "2026-07-13T15:00:00Z"], "x": [1, 2]}
            ),
            batch_id="unordered",
            provenance=PROVENANCE,
            context=CONTEXT,
        )
