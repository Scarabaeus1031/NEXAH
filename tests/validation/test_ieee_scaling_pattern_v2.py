"""Tests for the frozen H–K IEEE scaling validation design."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

import numpy as np
import pytest

from validation.ieee_scaling_pattern_v2.run_validation import (
    canonicalize_for_json,
    detect_interior_peak,
    downward_scales,
    local_polynomial_curvature,
    run_validation,
    upward_scales,
)


RECORDED_AT = datetime(2026, 7, 13, 21, 0, tzinfo=timezone.utc)
CANONICAL_RESULT = (
    Path(__file__).parents[2]
    / "validation"
    / "ieee_scaling_pattern_v2"
    / "canonical_result.json"
)


def test_branch_axes_share_only_the_native_baseline() -> None:
    upward = upward_scales(1.2, 0.05)
    downward = downward_scales(0.8, 0.05)

    assert upward[0] == 1.0
    assert downward[0] == 1.0
    assert all(current > previous for previous, current in zip(upward, upward[1:]))
    assert all(
        current < previous for previous, current in zip(downward, downward[1:])
    )
    assert set(upward).intersection(downward) == {1.0}


def test_local_polynomial_curvature_recovers_quadratic_without_peak() -> None:
    load = np.linspace(1.0, 2.0, 41)
    values = 3.0 * load**2 + 2.0 * load + 1.0
    positions, curvature = local_polynomial_curvature(load, values)

    assert len(positions) == 35
    assert np.allclose(curvature, 6.0)
    assert detect_interior_peak(load, values, 2.0) is None


def test_reduced_v2_is_reproducible_and_heldout_is_separate() -> None:
    kwargs = {
        "recorded_at": RECORDED_AT,
        "development_cases": ("ieee9",),
        "held_out_case": "ieee14",
        "upper_scale": 4.2,
        "lower_scale": 0.8,
        "coarse_step": 0.1,
        "downward_step": 0.1,
        "write_outputs": False,
    }
    first = run_validation(**kwargs)
    second = run_validation(**kwargs)

    assert canonicalize_for_json(first) == canonicalize_for_json(second)
    assert first["frozen_design"]["parameters_tuned_on_held_out_case"] is False
    assert first["frozen_design"]["fabricated_failed_physics"] is False
    assert first["development_cases"][0]["role"] == "method_development"
    assert first["held_out_case"]["role"] == "held_out_scale"
    assert first["aggregate"]["held_out_gate"]["executed"] is True


def test_heldout_case_cannot_enter_development_set() -> None:
    with pytest.raises(ValueError, match="held-out"):
        run_validation(
            recorded_at=RECORDED_AT,
            development_cases=("ieee9",),
            held_out_case="ieee9",
            write_outputs=False,
        )


def test_canonical_v2_closes_with_declared_boundary_of_validity() -> None:
    result = json.loads(CANONICAL_RESULT.read_text(encoding="utf-8"))

    assert result["frozen_design"]["held_out_case"] == "pegase9241"
    assert result["frozen_design"]["parameters_tuned_on_held_out_case"] is False
    assert result["aggregate"]["development_upward_boundaries"] == 7
    assert result["aggregate"]["development_candidate_precursors"] == 0
    assert result["aggregate"]["held_out_gate"]["executed"] is True
    assert (
        result["aggregate"]["held_out_gate"]["outcome"]
        == "boundary_of_validity"
    )
