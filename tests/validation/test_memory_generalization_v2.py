"""Tests for the split multi-episode memory benchmark."""

from __future__ import annotations

from datetime import datetime, timezone
import json

from validation.memory_generalization_v2.run_validation import run_validation


RECORDED_AT = datetime(2026, 7, 13, 12, 0, tzinfo=timezone.utc)


def test_reduced_v2_is_reproducible_split_and_family_blind() -> None:
    first = run_validation(
        recorded_at=RECORDED_AT, samples=500, write_outputs=False
    )
    second = run_validation(
        recorded_at=RECORDED_AT, samples=500, write_outputs=False
    )

    assert first == second
    design = first["design"]
    assert design["reference_episodes"] == 15
    assert design["validation_queries"] == 6
    assert design["held_out_test_queries"] == 6
    assert design["shared_context_domain"] == "synthetic-dynamical-system"
    assert design["test_used_for_selection"] is False
    assert first["store"]["active_episodes"] == 15
    assert first["selected_method"] in design["methods"]


def test_v2_reports_all_predeclared_methods_on_both_splits() -> None:
    result = run_validation(
        recorded_at=RECORDED_AT, samples=500, write_outputs=False
    )

    methods = set(result["design"]["methods"])
    assert set(result["validation_by_method"]) == methods
    assert set(result["held_out_test_all_methods"]) == methods
    for metrics in result["held_out_test_all_methods"].values():
        assert 0.0 <= metrics["top1_accuracy"] <= 1.0
        assert 0.0 <= metrics["recall_at_3"] <= 1.0


def test_v2_writes_result_and_summary(tmp_path) -> None:
    result = run_validation(
        recorded_at=RECORDED_AT, samples=500, output_dir=tmp_path
    )

    result_path = tmp_path / "validation_result.json"
    summary_path = tmp_path / "validation_summary.md"
    assert json.loads(result_path.read_text()) == result
    assert "Held-out test" in summary_path.read_text()
