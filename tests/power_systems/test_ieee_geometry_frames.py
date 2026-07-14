"""Typed physical-frame tests for Phase V work package B."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
import json
from pathlib import Path

import pytest

from nexah.orientation import Context, Provenance, UncertaintyKind
from nexah.power_systems import (
    IEEEFrameStatus,
    IEEEGeometryCampaign,
    IEEEGeometryCaseManifest,
    IEEEGeometryFrameError,
    build_ieee_geometry_campaign,
)
from nexah.sources import IEEEPandapowerAdapter


ROOT = Path(__file__).parents[2]
MANIFEST_PATH = (
    ROOT / "APPLICATIONS" / "power_systems" / "ieee_geometry_v1" / "case_manifest.json"
)
FRAMES_PATH = MANIFEST_PATH.with_name("development_frames.json")
NOW = datetime(2026, 7, 14, 14, 0, tzinfo=timezone.utc)


def _manifest_for(scales: tuple[float, ...]) -> IEEEGeometryCaseManifest:
    manifest = IEEEGeometryCaseManifest.from_dict(
        json.loads(MANIFEST_PATH.read_text())
    )
    return replace(
        manifest,
        cases=tuple(replace(case, load_scales=scales) for case in manifest.cases),
    )


def _campaign(scales: tuple[float, ...], *, campaign_id: str = "geometry-test"):
    return IEEEPandapowerAdapter(case_id="ieee9").run_campaign(
        scales,
        campaign_id=campaign_id,
        provenance=Provenance(
            source="pandapower:ieee9",
            method="independent Newton-Raphson load-scale campaign",
            recorded_at=NOW,
            record_id=campaign_id,
        ),
        context=Context(
            domain="power-system",
            values={"evidence_class": "benchmark_model"},
        ),
    )


def test_converged_frames_preserve_physics_units_scope_and_identity() -> None:
    scales = (0.8, 1.0, 1.2)
    geometry = build_ieee_geometry_campaign(
        _campaign(scales),
        _manifest_for(scales),
        require_environment_match=False,
    )

    assert geometry.case_role == "method_development"
    assert geometry.campaign_axis == "ordered_load_scale_not_time"
    assert geometry.topology_id.startswith("sha256:")
    assert len({frame.topology_id for frame in geometry.frames}) == 1
    assert [frame.campaign_index for frame in geometry.frames] == [0, 1, 2]
    assert [frame.load_scale for frame in geometry.frames] == list(scales)
    assert all(frame.status is IEEEFrameStatus.CONVERGED for frame in geometry.frames)

    frame = geometry.frames[0]
    assert [view.entity_scope for view in frame.entity_views] == ["bus", "line"]
    assert frame.entity_views[0].variable_names == (
        "vm_pu",
        "va_degree",
        "p_mw",
        "q_mvar",
    )
    assert frame.entity_views[0].units == ("pu", "degree", "MW", "MVAr")
    assert frame.system_features is not None
    assert frame.system_features.feature_names[0] == "minimum_bus_voltage"
    assert "system-summary-standardized-v1" in frame.declared_projection_ids
    assert frame.uncertainty.kind is UncertaintyKind.UNKNOWN
    assert frame.evidence_class == "benchmark_model"


def test_geometry_campaign_round_trips_without_computing_geometry() -> None:
    scales = (0.8, 1.0, 1.2)
    geometry = build_ieee_geometry_campaign(
        _campaign(scales, campaign_id="geometry-json"),
        _manifest_for(scales),
        require_environment_match=False,
    )
    restored = IEEEGeometryCampaign.from_dict(
        json.loads(json.dumps(geometry.to_dict()))
    )

    assert restored == geometry
    assert not hasattr(restored.frames[0], "curvature")
    assert restored.frames[0].provenance.metadata["manifest_id"] == (
        "phase-v-ieee-geometry-v1"
    )


def test_failed_position_remains_a_frame_without_fabricated_physics() -> None:
    scales = (1.0, 2.0, 5.0)
    geometry = build_ieee_geometry_campaign(
        _campaign(scales, campaign_id="geometry-failure"),
        _manifest_for(scales),
        require_environment_match=False,
    )
    failed = [frame for frame in geometry.frames if frame.status is IEEEFrameStatus.FAILED]

    assert failed
    assert all(frame.entity_views == () for frame in failed)
    assert all(frame.system_features is None for frame in failed)
    assert all(frame.failure for frame in failed)
    assert all(frame.topology_id == geometry.topology_id for frame in failed)


def test_builder_rejects_campaign_outside_frozen_grid() -> None:
    with pytest.raises(IEEEGeometryFrameError, match="differ from frozen manifest"):
        build_ieee_geometry_campaign(
            _campaign((0.8, 1.0, 1.2)),
            _manifest_for((0.7, 1.0, 1.3)),
            require_environment_match=False,
        )


def test_topology_identity_is_stable_across_repeated_campaigns() -> None:
    scales = (0.8, 1.0, 1.2)
    manifest = _manifest_for(scales)
    first = build_ieee_geometry_campaign(
        _campaign(scales, campaign_id="geometry-first"),
        manifest,
        require_environment_match=False,
    )
    second = build_ieee_geometry_campaign(
        _campaign(scales, campaign_id="geometry-second"),
        manifest,
        require_environment_match=False,
    )

    assert first.topology_id == second.topology_id


def test_committed_development_frames_are_typed_and_failure_complete() -> None:
    geometry = IEEEGeometryCampaign.from_dict(
        json.loads(FRAMES_PATH.read_text())
    )

    assert len(geometry.frames) == 19
    assert sum(
        frame.status is IEEEFrameStatus.CONVERGED for frame in geometry.frames
    ) == 17
    assert [
        frame.load_scale
        for frame in geometry.frames
        if frame.status is IEEEFrameStatus.FAILED
    ] == [2.3, 2.4]
    assert all(frame.system_features is None for frame in geometry.frames[-2:])
