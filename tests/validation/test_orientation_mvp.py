"""Reproducibility tests for the canonical Orientation MVP validation."""

from __future__ import annotations

from datetime import datetime, timezone
import json

import pytest

from PROTO_CORE.NEXAH_DEMONSTRATOR.scripts.generate_transition_structure import (
    generate_transition_data,
)
from validation.orientation_mvp.run_validation import run_validation


RECORDED_AT = datetime(2026, 7, 13, 8, 0, tzinfo=timezone.utc)


def test_canonical_demonstrator_reference_is_deterministic() -> None:
    first = generate_transition_data()
    second = generate_transition_data()

    assert first["trajectory"].shape == (8000, 3)
    assert first["sheets"].tolist() == second["sheets"].tolist()
    assert int(first["transition_events"].sum()) == 594
    assert sorted(set(first["sheets"].tolist())) == [0, 1, 2, 3, 4, 5, 6]
    assert float(first["transition_matrix"].sum()) == 7999.0


def test_canonical_validation_repeats_and_records_declared_metrics() -> None:
    first = run_validation(recorded_at=RECORDED_AT, write_outputs=False)
    second = run_validation(recorded_at=RECORDED_AT, write_outputs=False)

    assert first == second
    metrics = first["baseline_comparison"]["v07"]["metrics"]
    null_metrics = first["baseline_comparison"]["null_no_change_baseline"][
        "metrics"
    ]
    assert metrics["predicted_events"] == 336
    assert metrics["reference_events"] == 594
    assert metrics["matched_events"] == 268
    assert metrics["precision"] == pytest.approx(0.7976190476190477)
    assert metrics["recall"] == pytest.approx(0.4511784511784512)
    assert metrics["f1"] == pytest.approx(0.5763440860215054)
    assert null_metrics["f1"] == 0.0
    assert null_metrics["exact_sample_accuracy"] > metrics["exact_sample_accuracy"]


def test_validation_writes_the_complete_evidence_bundle(tmp_path) -> None:
    result = run_validation(
        recorded_at=RECORDED_AT,
        steps=600,
        output_dir=tmp_path,
    )

    expected = {
        "orientation_state.json",
        "orientation_report.json",
        "baseline_comparison.json",
        "failure_cases.json",
        "validation_summary.md",
    }
    assert {path.name for path in tmp_path.iterdir()} == expected
    report = json.loads((tmp_path / "orientation_report.json").read_text())
    assert report == result["orientation_report"]
    assert report["uncertainty"]["kind"] == "unknown"

