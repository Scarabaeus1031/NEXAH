"""Contract and failure tests for the Phase III reference source adapter."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json

import numpy as np
import pytest

from nexah.backends import V07BackendAdapter
from nexah.orientation import Context, Provenance
from nexah.sources import (
    ArraySourceAdapter,
    SourceAdapterError,
    SourceAxis,
    SourceBatch,
)


RECORDED_AT = datetime(2026, 7, 13, 14, 0, tzinfo=timezone.utc)
PROVENANCE = Provenance(
    source="test-array",
    method="in-memory fixture",
    recorded_at=RECORDED_AT,
    record_id="array-001",
)
CONTEXT = Context(domain="adapter-contract-test", values={"fixture": True})


def test_array_adapter_preserves_values_semantics_and_provenance() -> None:
    values = np.asarray([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    timestamps = tuple(RECORDED_AT + timedelta(seconds=index) for index in range(3))

    batch = ArraySourceAdapter().adapt(
        values,
        batch_id="batch-001",
        provenance=PROVENANCE,
        context=CONTEXT,
        timestamps=timestamps,
        feature_names=("voltage", "angle"),
        units=("pu", "rad"),
        row_axis=SourceAxis.TIME,
    )

    assert batch.batch_id == "batch-001"
    assert batch.provenance == PROVENANCE
    assert batch.context == CONTEXT
    assert [feature.name for feature in batch.features] == ["voltage", "angle"]
    assert [feature.unit for feature in batch.features] == ["pu", "rad"]
    assert np.array_equal(batch.to_numpy(), values)
    assert batch.timestamps == timestamps
    assert batch.row_axis is SourceAxis.TIME
    assert batch.quality.transformations == ()


def test_one_dimensional_input_expands_explicitly() -> None:
    batch = ArraySourceAdapter().adapt(
        [1.0, 2.0, 3.0],
        batch_id="batch-1d",
        provenance=PROVENANCE,
        context=CONTEXT,
        feature_names=("signal",),
    )

    assert batch.to_numpy().shape == (3, 1)
    assert batch.quality.transformations == (
        "one-dimensional input expanded to one feature",
    )


def test_source_batch_round_trips_through_json() -> None:
    batch = ArraySourceAdapter().adapt(
        [[1.0], [2.0]],
        batch_id="batch-json",
        provenance=PROVENANCE,
        context=CONTEXT,
    )

    restored = SourceBatch.from_dict(json.loads(json.dumps(batch.to_dict())))

    assert restored == batch
    assert isinstance(restored.values, tuple)
    assert isinstance(restored.values[0], tuple)


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ([[1.0, np.nan]], "missing or non-finite"),
        ([[1.0, np.inf]], "missing or non-finite"),
        (np.zeros((2, 2, 2)), "one- or two-dimensional"),
        (np.empty((0, 2)), "rows and features"),
    ],
)
def test_invalid_numeric_sources_fail_visibly(
    source: object, message: str
) -> None:
    with pytest.raises(SourceAdapterError, match=message):
        ArraySourceAdapter().adapt(
            source,
            batch_id="invalid",
            provenance=PROVENANCE,
            context=CONTEXT,
        )


def test_semantic_and_temporal_ambiguity_fails_visibly() -> None:
    adapter = ArraySourceAdapter()
    with pytest.raises(SourceAdapterError, match="feature_names"):
        adapter.adapt(
            [[1.0, 2.0]],
            batch_id="bad-features",
            provenance=PROVENANCE,
            context=CONTEXT,
            feature_names=("only-one",),
        )
    with pytest.raises(SourceAdapterError, match="strictly increasing"):
        adapter.adapt(
            [[1.0], [2.0]],
            batch_id="bad-time",
            provenance=PROVENANCE,
            context=CONTEXT,
            timestamps=(RECORDED_AT, RECORDED_AT),
            row_axis=SourceAxis.TIME,
        )
    with pytest.raises(SourceAdapterError, match="time row axis"):
        adapter.adapt(
            [[1.0], [2.0]],
            batch_id="bad-axis",
            provenance=PROVENANCE,
            context=CONTEXT,
            timestamps=(RECORDED_AT, RECORDED_AT + timedelta(seconds=1)),
        )


def test_source_batch_feeds_existing_backend_without_hidden_translation() -> None:
    time = np.linspace(0.0, 6.0, 120)
    values = np.column_stack((np.sin(time), np.cos(time)))
    batch = ArraySourceAdapter().adapt(
        values,
        batch_id="backend-input",
        provenance=PROVENANCE,
        context=CONTEXT,
        feature_names=("sin", "cos"),
    )

    result = V07BackendAdapter(n_clusters=3, window=5).adapt(
        batch.to_numpy(),
        analysis_id="source-to-v07",
        provenance=batch.provenance,
        context=batch.context,
        timestamps=batch.timestamps or None,
    )

    assert len(result.state.observations) == 120
    assert result.state.context == CONTEXT
    assert result.state.provenance == PROVENANCE
