"""Contract and alignment tests for the frozen v0.7 backend adapter."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
import random

import numpy as np
import pytest

from nexah.backends import BackendAdapterError, V07BackendAdapter
from nexah.orientation import (
    Context,
    MapScope,
    OrientationState,
    Provenance,
    UncertaintyKind,
)


NOW = datetime(2026, 7, 12, 12, 0, tzinfo=timezone.utc)


def provenance() -> Provenance:
    return Provenance(
        source="synthetic-v07-fixture",
        method="deterministic test signal",
        recorded_at=NOW,
        record_id="fixture-run-001",
    )


def context() -> Context:
    return Context(domain="synthetic-test", values={"purpose": "WP2 validation"})


def trajectory() -> np.ndarray:
    first = np.sin(np.linspace(0.0, 4.0 * np.pi, 80))
    second = 1.5 + 0.5 * np.cos(np.linspace(0.0, 4.0 * np.pi, 80))
    return np.concatenate([first, second])


def adapt():
    return V07BackendAdapter(n_clusters=3, window=8, random_state=7).adapt(
        trajectory(),
        analysis_id="analysis-001",
        provenance=provenance(),
        context=context(),
    )


def test_adapter_marks_every_backend_identity_as_local_to_the_fit() -> None:
    result = adapt()
    state = result.state

    assert state.representation.backend == "nexah-v07"
    assert state.representation.scope is MapScope.LOCAL_FIT
    assert state.map is not None
    assert state.map.scope is MapScope.LOCAL_FIT
    assert state.location is not None
    assert state.location.identifier.scope == state.representation.representation_id
    assert all(
        transition.source.identifier.scope == state.representation.representation_id
        and transition.target.identifier.scope
        == state.representation.representation_id
        for transition in result.transitions
    )


def test_alignment_records_the_historical_t_minus_window_behavior() -> None:
    result = adapt()

    assert result.alignment.input_samples == 160
    assert result.alignment.embedded_samples == 152
    assert result.alignment.raw_window(0) == (0, 7)
    assert result.alignment.raw_anchor(151) == 158
    assert result.alignment.final_source_sample_used == 158
    with pytest.raises(IndexError, match="outside represented range"):
        result.alignment.raw_anchor(152)


def test_observations_preserve_values_provenance_and_supplied_timestamps() -> None:
    signal = trajectory()
    timestamps = tuple(NOW + timedelta(seconds=index) for index in range(len(signal)))

    result = V07BackendAdapter(n_clusters=3, window=8).adapt(
        signal,
        analysis_id="timed-analysis",
        provenance=provenance(),
        context=context(),
        timestamps=timestamps,
    )

    assert len(result.state.observations) == len(signal)
    assert result.state.observations[0].value == pytest.approx(signal[0])
    assert result.state.observations[-1].observed_at == timestamps[-1]
    assert result.state.observations[0].provenance == provenance()


def test_adapter_does_not_invent_calibrated_uncertainty_or_regime_objects() -> None:
    result = adapt()

    assert result.state.uncertainty.kind is UncertaintyKind.UNKNOWN
    assert result.state.uncertainty.value is None
    assert result.regimes == ()
    evidence = result.state.evidence[0]
    assert evidence.uncertainty.kind is UncertaintyKind.UNKNOWN
    assert "regime_zones_embedded" in evidence.payload
    assert "cluster identifiers are local to this fit" in evidence.payload["limitations"]


def test_transitions_preserve_empirical_probabilities_and_evidence_links() -> None:
    result = adapt()
    evidence_id = result.state.evidence[0].evidence_id

    assert result.transitions
    assert all(0.0 <= transition.probability <= 1.0 for transition in result.transitions)
    assert all(transition.evidence_ids == (evidence_id,) for transition in result.transitions)

    by_source: dict[str, float] = {}
    for transition in result.transitions:
        source = transition.source.identifier.value
        by_source[source] = by_source.get(source, 0.0) + float(transition.probability)
    assert all(total == pytest.approx(1.0) for total in by_source.values())


def test_adapted_orientation_state_round_trips_through_json() -> None:
    original = adapt().state

    payload = json.loads(json.dumps(original.to_dict()))
    restored = OrientationState.from_dict(payload)

    assert restored == original


@pytest.mark.parametrize(
    ("signal", "message"),
    [
        ([1.0, float("nan"), 2.0, 3.0, 4.0, 5.0], "finite"),
        (np.zeros((3, 2, 1)), "one- or two-dimensional"),
        ([1.0, 2.0, 3.0], "greater than window"),
        (["a", "b", "c", "d", "e", "f"], "numeric"),
    ],
)
def test_invalid_trajectory_fails_with_adapter_error(signal, message: str) -> None:
    adapter = V07BackendAdapter(n_clusters=2, window=5)

    with pytest.raises(BackendAdapterError, match=message):
        adapter.adapt(
            signal,
            analysis_id="invalid",
            provenance=provenance(),
            context=context(),
        )


def test_timestamp_count_and_timezone_fail_visibly() -> None:
    signal = trajectory()
    adapter = V07BackendAdapter(n_clusters=3, window=8)

    with pytest.raises(BackendAdapterError, match="length must match"):
        adapter.adapt(
            signal,
            analysis_id="bad-time-count",
            provenance=provenance(),
            context=context(),
            timestamps=(NOW,),
        )

    naive = tuple(datetime(2026, 7, 12, 12, 0) for _ in range(len(signal)))
    with pytest.raises(BackendAdapterError, match="timezone-aware"):
        adapter.adapt(
            signal,
            analysis_id="bad-time-zone",
            provenance=provenance(),
            context=context(),
            timestamps=naive,
        )


def test_adapter_restores_process_global_random_generators() -> None:
    random.seed(1234)
    np.random.seed(1234)
    expected_python = random.random()
    expected_numpy = float(np.random.random())

    random.seed(1234)
    np.random.seed(1234)
    adapt()
    actual_python = random.random()
    actual_numpy = float(np.random.random())

    assert actual_python == expected_python
    assert actual_numpy == expected_numpy


def test_multidimensional_observations_are_json_compatible_lists() -> None:
    t = np.linspace(0.0, 8.0 * np.pi, 120)
    signal = np.column_stack([np.sin(t), np.cos(t)])

    result = V07BackendAdapter(n_clusters=3, window=8).adapt(
        signal,
        analysis_id="multidimensional",
        provenance=provenance(),
        context=context(),
    )

    assert result.state.observations[0].value == [0.0, 1.0]

