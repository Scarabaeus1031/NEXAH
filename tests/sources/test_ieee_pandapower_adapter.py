"""Physical and coupling tests for the Phase III IEEE source adapter."""

from __future__ import annotations

from datetime import datetime, timezone
import json

import numpy as np
import pytest

from nexah.orientation import Context, Provenance
from nexah.sources import (
    IEEECoupledCampaign,
    IEEEPandapowerAdapter,
    IEEEPhysicalSnapshot,
    IEEESourceAdapterError,
    SourceAxis,
)


RECORDED_AT = datetime(2026, 7, 13, 16, 0, tzinfo=timezone.utc)
PROVENANCE = Provenance(
    source="pandapower:case9",
    method="Newton-Raphson load-scale campaign",
    recorded_at=RECORDED_AT,
    record_id="ieee9-campaign-001",
)
CONTEXT = Context(
    domain="power-system",
    values={"benchmark": "IEEE 9-bus", "campaign_axis": "load_scale"},
)


def test_coupled_ieee_campaign_preserves_spatial_and_ordered_views() -> None:
    campaign = IEEEPandapowerAdapter(case_id="ieee9").run_campaign(
        (0.8, 1.0, 1.2),
        campaign_id="ieee9-load-sweep",
        provenance=PROVENANCE,
        context=CONTEXT,
    )

    assert campaign.campaign_batch.row_axis is SourceAxis.ORDERED_SAMPLE
    assert campaign.campaign_batch.row_ids == (
        "ieee9-load-sweep:load-000",
        "ieee9-load-sweep:load-001",
        "ieee9-load-sweep:load-002",
    )
    assert tuple(feature.name for feature in campaign.campaign_batch.features) == (
        "load_scale",
        "minimum_bus_voltage",
        "mean_bus_voltage",
        "bus_voltage_std",
        "bus_angle_range",
        "maximum_line_loading",
        "total_bus_consumption_p",
        "total_bus_consumption_q",
    )
    assert campaign.campaign_batch.provenance == PROVENANCE
    assert campaign.campaign_batch.context == CONTEXT
    assert [snapshot.load_scale for snapshot in campaign.snapshots] == [0.8, 1.0, 1.2]

    first = campaign.snapshots[0]
    assert first.converged
    assert first.bus_batch is not None
    assert first.line_batch is not None
    assert first.bus_batch.row_axis is SourceAxis.ENTITY
    assert first.line_batch.row_axis is SourceAxis.ENTITY
    assert first.bus_batch.row_ids[0] == "bus:0"
    assert first.line_batch.row_ids[0].startswith("line:0:")
    assert first.bus_batch.to_numpy().shape == (9, 4)
    assert first.line_batch.to_numpy().shape == (9, 3)

    rows = campaign.campaign_batch.to_numpy()
    assert np.array_equal(rows[:, 0], np.asarray([0.8, 1.0, 1.2]))
    assert len(np.unique(rows[:, 1:], axis=0)) == 3
    assert "regime" not in json.dumps(campaign.to_dict()).lower()
    assert "risk" not in json.dumps(campaign.to_dict()).lower()
    assert "loops" not in json.dumps(campaign.to_dict()).lower()


def test_ieee_campaign_round_trips_through_json() -> None:
    campaign = IEEEPandapowerAdapter(case_id="ieee9").run_campaign(
        (0.9, 1.1),
        campaign_id="ieee9-json",
        provenance=PROVENANCE,
        context=CONTEXT,
    )

    restored = IEEECoupledCampaign.from_dict(
        json.loads(json.dumps(campaign.to_dict()))
    )

    assert restored == campaign
    assert restored.snapshots[0].bus_batch is not None
    assert restored.snapshots[0].bus_batch.row_axis is SourceAxis.ENTITY


@pytest.mark.parametrize(
    "scales",
    [(), (1.0,), (1.0, 1.0), (1.1, 1.0), (0.0, 1.0), (1.0, np.inf)],
)
def test_ieee_campaign_rejects_invalid_load_axes(scales: tuple[float, ...]) -> None:
    with pytest.raises(IEEESourceAdapterError):
        IEEEPandapowerAdapter(case_id="ieee9").run_campaign(
            scales,
            campaign_id="invalid",
            provenance=PROVENANCE,
            context=CONTEXT,
        )


def test_failed_snapshot_cannot_smuggle_fabricated_physics() -> None:
    with pytest.raises(ValueError, match="cannot contain physical batches"):
        valid_campaign = IEEEPandapowerAdapter(case_id="ieee9").run_campaign(
            (0.9, 1.0),
            campaign_id="fixture",
            provenance=PROVENANCE,
            context=CONTEXT,
        )
        IEEEPhysicalSnapshot(
            scenario_id="failed",
            case_id="ieee9",
            load_scale=5.0,
            converged=False,
            bus_batch=valid_campaign.snapshots[0].bus_batch,
            line_batch=None,
            failure="power flow did not converge",
        )


def test_unknown_ieee_case_fails_visibly() -> None:
    with pytest.raises(IEEESourceAdapterError, match="unsupported IEEE case"):
        IEEEPandapowerAdapter(case_id="ieee999")


def test_scaling_case_names_are_available_without_eager_network_loading() -> None:
    assert IEEEPandapowerAdapter(case_id="ieee300").case_id == "ieee300"
    assert IEEEPandapowerAdapter(case_id="pegase1354").case_id == "pegase1354"
    assert IEEEPandapowerAdapter(case_id="pegase9241").case_id == "pegase9241"
