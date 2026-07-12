"""Tests for the multi-system episodic retrieval benchmark."""

from __future__ import annotations

from datetime import datetime, timezone
import json

import numpy as np

from validation.memory_generalization.run_validation import run_validation
from validation.memory_generalization.systems import (
    add_relative_noise,
    kuramoto,
    lorenz,
    rossler,
)


RECORDED_AT = datetime(2026, 7, 13, 10, 0, tzinfo=timezone.utc)


def test_system_fixtures_are_deterministic_and_dimensionally_distinct() -> None:
    assert np.array_equal(lorenz(samples=300), lorenz(samples=300))
    assert np.array_equal(rossler(samples=300), rossler(samples=300))
    assert np.array_equal(kuramoto(samples=300), kuramoto(samples=300))
    assert lorenz(samples=300).shape == (300, 3)
    assert rossler(samples=300).shape == (300, 3)
    assert kuramoto(samples=300).shape == (300, 2)


def test_relative_noise_is_seeded_and_non_destructive() -> None:
    source = lorenz(samples=300)
    original = source.copy()

    first = add_relative_noise(source, fraction=0.05, seed=7)
    second = add_relative_noise(source, fraction=0.05, seed=7)

    assert np.array_equal(first, second)
    assert np.array_equal(source, original)
    assert not np.array_equal(first, source)


def test_reduced_benchmark_is_reproducible_and_family_blind() -> None:
    first = run_validation(
        recorded_at=RECORDED_AT,
        samples=500,
        write_outputs=False,
    )
    second = run_validation(
        recorded_at=RECORDED_AT,
        samples=500,
        write_outputs=False,
    )

    assert first == second
    design = first["preregistered_design"]
    assert design["shared_context_domain"] == "synthetic-dynamical-system"
    assert design["top1_chance_baseline"] == 1.0 / 3.0
    assert design["parameters_tuned_on_results"] is False
    assert first["store_history_records"] == 3
    assert first["aggregate"]["queries"] == 12
    assert 0.0 <= first["aggregate"]["top1_accuracy"] <= 1.0


def test_benchmark_writes_result_and_summary(tmp_path) -> None:
    result = run_validation(
        recorded_at=RECORDED_AT,
        samples=500,
        output_dir=tmp_path,
    )

    result_path = tmp_path / "validation_result.json"
    summary_path = tmp_path / "validation_summary.md"
    assert result_path.exists()
    assert summary_path.exists()
    assert json.loads(result_path.read_text()) == result
    assert "Chance baseline" in summary_path.read_text()
