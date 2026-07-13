"""Tests for the physical reconstruction of the IEEE scaling hypothesis."""

from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from nexah.orientation import Context, Provenance
from nexah.sources import IEEEPandapowerAdapter
from validation.ieee_scaling_pattern_v1.run_validation import (
    historical_c_struct,
    run_validation,
)


RECORDED_AT = datetime(2026, 7, 13, 19, 0, tzinfo=timezone.utc)


def test_historical_metric_uses_only_converged_physical_views() -> None:
    campaign = IEEEPandapowerAdapter(case_id="ieee9").run_campaign(
        (0.9, 1.0),
        campaign_id="metric-fixture",
        provenance=Provenance(
            source="pandapower:case9",
            method="metric fixture",
            recorded_at=RECORDED_AT,
        ),
        context=Context(domain="power-system"),
    )

    first = historical_c_struct(campaign.snapshots[0])
    second = historical_c_struct(campaign.snapshots[1])

    assert np.isfinite(first)
    assert np.isfinite(second)
    assert first >= 0.0
    assert first != second


def test_reduced_scaling_validation_is_reproducible_and_collapse_aware() -> None:
    scales = tuple(float(value) for value in np.linspace(0.6, 3.0, 40))
    first = run_validation(
        recorded_at=RECORDED_AT,
        case_ids=("ieee9",),
        load_scales=scales,
        write_outputs=False,
    )
    second = run_validation(
        recorded_at=RECORDED_AT,
        case_ids=("ieee9",),
        load_scales=scales,
        write_outputs=False,
    )

    assert first == second
    assert first["frozen_design"]["fabricated_failed_physics"] is False
    assert first["frozen_design"]["parameters_tuned_on_results"] is False
    case = first["cases"][0]
    assert case["collapse_load_scale"] is not None
    assert case["historical_peak_load_scale"] is not None
    assert case["interior_peak_load_scale"] is not None
    assert len(case["curve"]) == len(scales)
    assert any(not row["converged"] for row in case["curve"])
