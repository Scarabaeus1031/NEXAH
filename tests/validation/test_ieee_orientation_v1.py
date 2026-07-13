"""Tests for the frozen IEEE D–F validation harness."""

from __future__ import annotations

from datetime import datetime, timezone
import json

import numpy as np

from validation.ieee_orientation_v1.run_validation import run_validation


RECORDED_AT = datetime(2026, 7, 13, 18, 0, tzinfo=timezone.utc)
SCALES = tuple(float(value) for value in np.linspace(0.6, 2.2, 17))


def test_reduced_ieee_validation_is_scoped_and_reproducible() -> None:
    first = run_validation(
        recorded_at=RECORDED_AT,
        case_ids=("ieee9",),
        load_scales=SCALES,
        write_outputs=False,
    )
    second = run_validation(
        recorded_at=RECORDED_AT,
        case_ids=("ieee9",),
        load_scales=SCALES,
        write_outputs=False,
    )

    assert first == second
    design = first["frozen_design"]
    assert design["campaign_axis"] == "ordered_load_scale_not_time"
    assert design["parameters_tuned_on_results"] is False
    assert design["nonconvergence_scored_as_numeric_event"] is False
    case = first["cases"][0]
    assert case["report_scope_confirmed"] is True
    assert case["v07_event_count"] > 0
    assert case["scored_physical_references"] == 2
    assert case["attribution_checks"] == 2 * case["v07_event_count"]


def test_ieee_validation_writes_machine_and_human_records(tmp_path) -> None:
    result = run_validation(
        recorded_at=RECORDED_AT,
        output_dir=tmp_path,
        case_ids=("ieee9",),
        load_scales=SCALES,
    )

    assert json.loads((tmp_path / "validation_result.json").read_text()) == result
    summary = (tmp_path / "validation_summary.md").read_text()
    assert "Threshold coverage" in summary
    assert "not time dynamics" in summary
