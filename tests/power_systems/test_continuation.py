"""Tests for baseline-anchored physical load branches."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from nexah.orientation import Context, Provenance
from nexah.power_systems import BranchDirection, refine_boundary, scan_branch
from nexah.sources import IEEEPandapowerAdapter, IEEEPhysicalSnapshot
from validation.ieee_scaling_pattern_v1.run_validation import historical_c_struct


RECORDED_AT = datetime(2026, 7, 14, 10, 0, tzinfo=timezone.utc)
PROVENANCE = Provenance(
    source="pandapower:ieee9",
    method="baseline-anchored continuation fixture",
    recorded_at=RECORDED_AT,
)
CONTEXT = Context(domain="power-system", values={"benchmark_case": "ieee9"})


def test_public_snapshot_preserves_failure_instead_of_physics() -> None:
    snapshot = IEEEPandapowerAdapter(case_id="ieee9").run_snapshot(
        10.0,
        scenario_id="failed-point",
        provenance=PROVENANCE,
        context=CONTEXT,
    )

    assert not snapshot.converged
    assert snapshot.failure is not None
    assert snapshot.bus_batch is None
    assert snapshot.line_batch is None


def test_upward_branch_starts_at_baseline_and_stops_at_failure() -> None:
    branch = scan_branch(
        IEEEPandapowerAdapter(case_id="ieee9"),
        (1.0, 2.0, 3.0, 4.0),
        direction=BranchDirection.UPWARD,
        campaign_id="upward-fixture",
        provenance=PROVENANCE,
        context=CONTEXT,
        metric=historical_c_struct,
    )

    assert branch.points[0].load_scale == 1.0
    assert branch.points[0].converged
    assert branch.first_failed_scale is not None
    assert not branch.points[-1].converged
    assert all(point.metric is not None for point in branch.converged_points)


def test_downward_branch_requires_decreasing_axis() -> None:
    with pytest.raises(ValueError, match="strictly"):
        scan_branch(
            IEEEPandapowerAdapter(case_id="ieee9"),
            (1.0, 1.1),
            direction=BranchDirection.DOWNWARD,
            campaign_id="invalid-downward",
            provenance=PROVENANCE,
            context=CONTEXT,
            metric=historical_c_struct,
        )


def test_boundary_refinement_resolves_bracket_reproducibly() -> None:
    adapter = IEEEPandapowerAdapter(case_id="ieee9")
    branch = scan_branch(
        adapter,
        (1.0, 2.0, 3.0),
        direction=BranchDirection.UPWARD,
        campaign_id="refinement-fixture",
        provenance=PROVENANCE,
        context=CONTEXT,
        metric=historical_c_struct,
    )
    first = refine_boundary(
        adapter,
        branch,
        tolerance=0.01,
        maximum_evaluations=10,
        campaign_id="refinement-fixture",
        provenance=PROVENANCE,
        context=CONTEXT,
        metric=historical_c_struct,
    )
    second = refine_boundary(
        adapter,
        branch,
        tolerance=0.01,
        maximum_evaluations=10,
        campaign_id="refinement-fixture",
        provenance=PROVENANCE,
        context=CONTEXT,
        metric=historical_c_struct,
    )

    assert first == second
    assert first.interval_width <= 0.01
    assert first.last_converged_scale < first.first_failed_scale


def test_snapshot_rejects_invalid_scale() -> None:
    with pytest.raises(Exception, match="finite and positive"):
        IEEEPandapowerAdapter(case_id="ieee9").run_snapshot(
            0.0,
            scenario_id="invalid",
            provenance=PROVENANCE,
            context=CONTEXT,
        )
