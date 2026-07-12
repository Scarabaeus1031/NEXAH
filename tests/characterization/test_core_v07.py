"""Characterization tests for the frozen NEXAH v0.7 backend."""

from __future__ import annotations

import math

import numpy as np

from nexah import NEXAH, __version__


def trajectory() -> np.ndarray:
    """A deterministic two-regime signal with enough samples for KMeans."""

    first = np.sin(np.linspace(0.0, 4.0 * np.pi, 80))
    second = 1.5 + 0.5 * np.cos(np.linspace(0.0, 4.0 * np.pi, 80))
    return np.concatenate([first, second])


def test_public_version_identifies_the_v07_baseline() -> None:
    assert __version__ == "0.7.0"


def test_preprocess_normalizes_a_one_dimensional_trajectory() -> None:
    engine = NEXAH(normalize=True)

    processed = engine._preprocess(np.arange(10, dtype=float))

    assert processed.shape == (10, 1)
    assert np.mean(processed[:, 0]) == pytest_approx(0.0)
    assert np.std(processed[:, 0]) == pytest_approx(1.0)


def test_legacy_embedding_shape_and_alignment_are_characterized() -> None:
    engine = NEXAH(window=3, normalize=False)
    source = np.arange(6, dtype=float).reshape(-1, 1)

    embedded = engine._embed(source)

    # v0.7 intentionally records the historical T-window behavior.
    assert embedded.shape == (3, 3)
    np.testing.assert_array_equal(embedded[0], [0.0, 1.0, 2.0])
    np.testing.assert_array_equal(embedded[-1], [2.0, 3.0, 4.0])


def test_transition_rows_are_empirical_probabilities() -> None:
    engine = NEXAH()

    transitions = engine._compute_transitions([0, 0, 1, 1, 0])

    assert transitions == {0: {0: 0.5, 1: 0.5}, 1: {1: 0.5, 0: 0.5}}
    assert all(math.isclose(sum(row.values()), 1.0) for row in transitions.values())


def test_analysis_schema_and_embedded_index_lengths() -> None:
    signal = trajectory()
    engine = NEXAH(n_clusters=3, window=8, random_state=7)

    result = engine.analyze(signal)

    expected = {
        "config",
        "current_state",
        "next_state",
        "best_state",
        "stable_states",
        "regime_shifts",
        "instability",
        "regime_zones",
        "escape_difficulty",
        "state_scores",
        "signature",
        "transitions",
    }
    assert set(result) == expected
    assert result["config"] == {
        "n_clusters": 3,
        "window": 8,
        "random_state": 7,
        "normalize": True,
    }
    assert len(result["instability"]) == len(signal) - 8
    assert result["signature"]["n_states_observed"] == 3
    assert all(
        math.isclose(sum(row.values()), 1.0)
        for row in result["transitions"].values()
    )


def test_fixed_seed_reproduces_non_stochastic_analysis() -> None:
    signal = trajectory()

    first = NEXAH(n_clusters=3, window=8, random_state=11).analyze(signal)
    second = NEXAH(n_clusters=3, window=8, random_state=11).analyze(signal)

    assert first == second


def test_current_state_is_trivially_reachable_as_target() -> None:
    signal = trajectory()
    engine = NEXAH(n_clusters=3, window=8, random_state=13)
    current = engine.analyze(signal)["current_state"]

    targeted = engine.analyze(signal, target_state=current)

    assert targeted["path_bfs"] == [current]
    assert targeted["path_prob"] == [current]
    assert targeted["intervention"] == {
        "reachable": True,
        "path": [current],
        "steps": 0,
        "cost": 0.0,
    }
    assert targeted["dynamics"] == {
        "hit_probability": 1.0,
        "expected_steps": 0.0,
    }


def test_identical_trajectories_have_identical_summary_signatures() -> None:
    signal = trajectory()

    comparison = NEXAH(n_clusters=3, window=8, random_state=17).compare(
        signal, signal
    )

    assert comparison["similarity"] == pytest_approx(1.0)
    assert comparison["stability_delta"] == pytest_approx(0.0)
    assert comparison["entropy_delta"] == pytest_approx(0.0)


def pytest_approx(value: float):
    """Import pytest lazily to keep the tested package import surface explicit."""

    import pytest

    return pytest.approx(value)

