"""D–E tests for scoped IEEE orientation and entity attribution."""

from __future__ import annotations

from datetime import datetime, timezone

import numpy as np
import pytest

from nexah.orientation import Context, Provenance
from nexah.power_systems import IEEEOrientationRun, orient_ieee_campaign
from nexah.sources import IEEEPandapowerAdapter


@pytest.fixture(scope="module")
def ieee_run() -> IEEEOrientationRun:
    provenance = Provenance(
        source="pandapower:case9",
        method="independent steady-state load campaign",
        recorded_at=datetime(2026, 7, 13, 17, 0, tzinfo=timezone.utc),
        record_id="ieee9-d-e-fixture",
    )
    campaign = IEEEPandapowerAdapter(case_id="ieee9").run_campaign(
        np.linspace(0.6, 2.2, 17),
        campaign_id="ieee9-d-e",
        provenance=provenance,
        context=Context(
            domain="power-system",
            values={"benchmark": "IEEE 9-bus"},
        ),
    )
    return orient_ieee_campaign(
        campaign,
        analysis_id="ieee9-d-e",
        n_clusters=4,
        window=4,
        random_state=42,
    )


def test_d_orientation_run_preserves_load_sweep_scope(
    ieee_run: IEEEOrientationRun,
) -> None:
    state = ieee_run.backend_result.state

    assert state.context.values["ordered_parameter"] == "load_scale"
    assert state.context.values["independent_steady_state_solutions"] is True
    assert state.reference_frame.scale == "load-scale order"
    assert "not physical time" in state.reference_frame.description
    assert ieee_run.report.provenance.method == "ieee-load-campaign-orientation-v1"
    assert "not a time trajectory" in ieee_run.report.explanation
    assert any(
        "not timestamps or dynamic evolution" in assumption
        for assumption in ieee_run.report.assumptions
    )
    assert "Source observation timestamps" not in ieee_run.report.missing_information
    assert "Dynamic trajectories between independently solved load cases" in (
        ieee_run.report.missing_information
    )


def test_e_attribution_aligns_events_to_physical_snapshots(
    ieee_run: IEEEOrientationRun,
) -> None:
    shifts = ieee_run.backend_result.raw_output["regime_shifts"]

    assert len(ieee_run.attributions) == len(shifts)
    for event in ieee_run.attributions:
        assert event.campaign_index == ieee_run.backend_result.alignment.raw_anchor(
            event.embedded_index
        )
        assert event.previous_load_scale < event.load_scale
        assert event.scenario_id == ieee_run.campaign.campaign_batch.row_ids[
            event.campaign_index
        ]
        assert len(event.bus_deltas) == 12
        assert len(event.line_deltas) == 9
        assert all(delta.entity_id.startswith("bus:") for delta in event.bus_deltas)
        assert all(delta.entity_id.startswith("line:") for delta in event.line_deltas)
        assert "does not establish causal" in event.interpretation


def test_e_attribution_is_deterministic(ieee_run: IEEEOrientationRun) -> None:
    repeated = orient_ieee_campaign(
        ieee_run.campaign,
        analysis_id="ieee9-d-e",
        n_clusters=4,
        window=4,
        random_state=42,
    )

    assert repeated.backend_result.raw_output == ieee_run.backend_result.raw_output
    assert repeated.report == ieee_run.report
    assert repeated.attributions == ieee_run.attributions


def test_e_top_entity_limit_fails_visibly(ieee_run: IEEEOrientationRun) -> None:
    with pytest.raises(ValueError, match="at least 1"):
        orient_ieee_campaign(
            ieee_run.campaign,
            analysis_id="invalid-attribution",
            top_entities_per_feature=0,
        )
