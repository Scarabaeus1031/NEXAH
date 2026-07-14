"""Deterministic unit fixtures for Phase V work package C."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
import json
from math import sqrt
from pathlib import Path

import pytest

from nexah.orientation import Provenance, Uncertainty, UncertaintyKind
from nexah.power_systems import (
    IEEEEntityView,
    IEEEFeatureVector,
    IEEEFrameStatus,
    IEEEGeometryAnalysis,
    IEEEGeometryCampaign,
    IEEEGeometryCaseManifest,
    IEEEGeometryFrame,
    IEEEGeometryOperatorError,
    IEEEGeometryValueStatus,
    analyze_ieee_geometry,
    fit_ieee_standardization,
)


ROOT = Path(__file__).parents[2]
MANIFEST_PATH = (
    ROOT / "APPLICATIONS" / "power_systems" / "ieee_geometry_v1" / "case_manifest.json"
)
DEVELOPMENT_FRAMES_PATH = MANIFEST_PATH.with_name("development_frames.json")
DEVELOPMENT_GEOMETRY_PATH = MANIFEST_PATH.with_name("development_geometry.json")
NOW = datetime(2026, 7, 14, 16, 0, tzinfo=timezone.utc)


def _base_manifest() -> IEEEGeometryCaseManifest:
    return IEEEGeometryCaseManifest.from_dict(json.loads(MANIFEST_PATH.read_text()))


FEATURE_NAMES = next(
    projection.inputs
    for projection in _base_manifest().projections
    if projection.projection_id == "system-summary-standardized-v1"
)
UNITS = ("pu", "pu", "pu", "degree", "percent", "MW", "MVAr")


def _manifest(scales: tuple[float, ...]) -> IEEEGeometryCaseManifest:
    manifest = _base_manifest()
    return replace(
        manifest,
        cases=tuple(replace(case, load_scales=scales) for case in manifest.cases),
    )


def _frame(
    index: int,
    scale: float,
    values: tuple[float, ...] | None,
    *,
    case_id: str,
    role: str,
    campaign_id: str,
    manifest: IEEEGeometryCaseManifest,
) -> IEEEGeometryFrame:
    provenance = Provenance(
        source=f"fixture:{case_id}",
        method="manual deterministic geometry fixture",
        recorded_at=NOW,
        record_id=f"{campaign_id}:frame:{index}",
    )
    uncertainty = Uncertainty(
        kind=UncertaintyKind.UNKNOWN,
        value=None,
        basis="deterministic unit fixture without calibrated uncertainty",
    )
    projection_ids = tuple(item.projection_id for item in manifest.projections)
    if values is None:
        return IEEEGeometryFrame(
            frame_id=f"{campaign_id}:frame:{index}",
            manifest_id=manifest.manifest_id,
            campaign_id=campaign_id,
            case_id=case_id,
            case_role=role,
            campaign_index=index,
            campaign_axis=manifest.campaign_axis,
            load_scale=scale,
            topology_id=f"fixture-topology:{case_id}",
            status=IEEEFrameStatus.FAILED,
            entity_views=(),
            system_features=None,
            declared_projection_ids=projection_ids,
            failure="fixture solver non-convergence",
            provenance=provenance,
            uncertainty=uncertainty,
        )
    return IEEEGeometryFrame(
        frame_id=f"{campaign_id}:frame:{index}",
        manifest_id=manifest.manifest_id,
        campaign_id=campaign_id,
        case_id=case_id,
        case_role=role,
        campaign_index=index,
        campaign_axis=manifest.campaign_axis,
        load_scale=scale,
        topology_id=f"fixture-topology:{case_id}",
        status=IEEEFrameStatus.CONVERGED,
        entity_views=(
            IEEEEntityView(
                view_id=f"{campaign_id}:frame:{index}:bus",
                entity_scope="bus",
                entity_ids=("bus:0",),
                variable_names=("vm_pu",),
                units=("pu",),
                values=((1.0,),),
            ),
            IEEEEntityView(
                view_id=f"{campaign_id}:frame:{index}:line",
                entity_scope="line",
                entity_ids=("line:0",),
                variable_names=("loading_percent",),
                units=("percent",),
                values=((10.0,),),
            ),
        ),
        system_features=IEEEFeatureVector(
            feature_names=FEATURE_NAMES,
            units=UNITS,
            values=values,
        ),
        declared_projection_ids=projection_ids,
        failure=None,
        provenance=provenance,
        uncertainty=uncertainty,
    )


def _campaign(
    scales: tuple[float, ...],
    rows: tuple[tuple[float, ...] | None, ...],
    *,
    case_id: str = "ieee9",
    role: str = "method_development",
    campaign_id: str = "operator-fixture",
) -> tuple[IEEEGeometryCampaign, IEEEGeometryCaseManifest]:
    manifest = _manifest(scales)
    frames = tuple(
        _frame(
            index,
            scale,
            values,
            case_id=case_id,
            role=role,
            campaign_id=campaign_id,
            manifest=manifest,
        )
        for index, (scale, values) in enumerate(zip(scales, rows))
    )
    campaign = IEEEGeometryCampaign(
        manifest_id=manifest.manifest_id,
        campaign_id=campaign_id,
        case_id=case_id,
        case_role=role,
        campaign_axis=manifest.campaign_axis,
        topology_id=f"fixture-topology:{case_id}",
        frames=frames,
        provenance=Provenance(
            source=f"fixture:{case_id}",
            method="manual deterministic geometry fixture",
            recorded_at=NOW,
            record_id=campaign_id,
        ),
    )
    return campaign, manifest


def _linear_rows(count: int) -> tuple[tuple[float, ...], ...]:
    return tuple(
        tuple(float(feature + index) for feature in range(len(FEATURE_NAMES)))
        for index in range(count)
    )


def test_linear_fixture_computes_declared_step_path_and_turn_metrics() -> None:
    scales = (1.0, 1.1, 1.2, 1.3)
    linear = _linear_rows(3)
    campaign, manifest = _campaign(scales, (*linear, None))

    model = fit_ieee_standardization(campaign, manifest)
    analysis = analyze_ieee_geometry(campaign, manifest, model)

    assert model.status is IEEEGeometryValueStatus.AVAILABLE
    assert model.means[0] == pytest.approx(1.0)
    assert model.population_stddevs[0] == pytest.approx(sqrt(2.0 / 3.0))

    expected_step = sqrt(10.5)
    assert [step.status for step in analysis.steps] == [
        IEEEGeometryValueStatus.AVAILABLE,
        IEEEGeometryValueStatus.AVAILABLE,
        IEEEGeometryValueStatus.INSUFFICIENT,
    ]
    assert analysis.steps[0].displacement == pytest.approx(expected_step)
    assert analysis.steps[0].normalized_local_drift == pytest.approx(
        expected_step / 0.1
    )
    assert analysis.total_path_length == pytest.approx(2.0 * expected_step)
    assert analysis.turns[0].direction_change_radians == pytest.approx(0.0)
    assert analysis.turns[0].discrete_curvature == pytest.approx(0.0)
    assert analysis.turns[1].status is IEEEGeometryValueStatus.INSUFFICIENT
    assert analysis.terminal_frame_id == campaign.frames[-1].frame_id
    assert analysis.solver_boundaries[0].distance_load_scale == pytest.approx(0.1)


def test_failure_terminates_sampled_path_and_is_never_bridged() -> None:
    scales = (1.0, 1.1, 1.2, 1.3, 1.4)
    rows = (_linear_rows(2)[0], _linear_rows(2)[1], None, _linear_rows(4)[3], _linear_rows(5)[4])
    campaign, manifest = _campaign(scales, rows)
    model = fit_ieee_standardization(campaign, manifest)

    analysis = analyze_ieee_geometry(campaign, manifest, model)

    assert analysis.steps[0].status is IEEEGeometryValueStatus.AVAILABLE
    assert all(
        step.status is IEEEGeometryValueStatus.INSUFFICIENT
        for step in analysis.steps[1:]
    )
    assert analysis.terminal_frame_id == campaign.frames[2].frame_id
    assert analysis.contiguous_converged_frame_ids == tuple(
        frame.frame_id for frame in campaign.frames[:2]
    )
    assert "already terminated" in (analysis.steps[-1].reason or "")


def test_zero_variance_is_explicit_insufficiency_not_invented_geometry() -> None:
    scales = (1.0, 1.1, 1.2)
    constant = tuple(float(index) for index in range(len(FEATURE_NAMES)))
    campaign, manifest = _campaign(scales, (constant, constant, constant))

    model = fit_ieee_standardization(campaign, manifest)
    analysis = analyze_ieee_geometry(campaign, manifest, model)

    assert model.status is IEEEGeometryValueStatus.INSUFFICIENT
    assert model.zero_variance_features == FEATURE_NAMES
    assert analysis.total_path_length is None
    assert all(
        frame.status is IEEEGeometryValueStatus.INSUFFICIENT
        for frame in analysis.projected_frames
    )
    assert all(
        step.status is IEEEGeometryValueStatus.INSUFFICIENT
        for step in analysis.steps
    )


def test_development_model_applies_to_locked_case_without_refitting() -> None:
    scales = (1.0, 1.1, 1.2)
    development, manifest = _campaign(scales, _linear_rows(3))
    locked, locked_manifest = _campaign(
        scales,
        tuple(tuple(2.0 * value for value in row) for row in _linear_rows(3)),
        case_id="ieee14",
        role="locked_evaluation",
        campaign_id="locked-fixture",
    )
    assert locked_manifest == manifest

    model = fit_ieee_standardization(development, manifest)
    analysis = analyze_ieee_geometry(locked, manifest, model)

    assert analysis.case_role == "locked_evaluation"
    assert analysis.projection_model.fit_case_id == "ieee9"
    assert analysis.projection_model.fit_campaign_id == development.campaign_id
    assert all(
        step.status is IEEEGeometryValueStatus.AVAILABLE for step in analysis.steps
    )
    with pytest.raises(IEEEGeometryOperatorError, match="method-development"):
        fit_ieee_standardization(locked, manifest)


def test_analysis_round_trips_with_failures_and_unknown_uncertainty() -> None:
    scales = (1.0, 1.1, 1.2, 1.3)
    campaign, manifest = _campaign(scales, (*_linear_rows(3), None))
    analysis = analyze_ieee_geometry(
        campaign,
        manifest,
        fit_ieee_standardization(campaign, manifest),
    )

    restored = IEEEGeometryAnalysis.from_dict(
        json.loads(json.dumps(analysis.to_dict()))
    )

    assert restored == analysis
    assert restored.uncertainty.kind is UncertaintyKind.UNKNOWN
    assert restored.solver_boundaries[0].boundary_type == "solver_non_convergence"


def test_operator_catalog_drift_is_rejected() -> None:
    scales = (1.0, 1.1, 1.2)
    campaign, manifest = _campaign(scales, _linear_rows(3))
    model = fit_ieee_standardization(campaign, manifest)
    changed = replace(manifest, operators=manifest.operators[:-1])

    with pytest.raises(IEEEGeometryOperatorError, match="operator set differs"):
        analyze_ieee_geometry(campaign, changed, model)


def test_committed_development_geometry_is_canonical() -> None:
    manifest = IEEEGeometryCaseManifest.from_dict(
        json.loads(MANIFEST_PATH.read_text())
    )
    campaign = IEEEGeometryCampaign.from_dict(
        json.loads(DEVELOPMENT_FRAMES_PATH.read_text())
    )
    model = fit_ieee_standardization(campaign, manifest)
    analysis = analyze_ieee_geometry(campaign, manifest, model)

    expected = {
        "standardization_model": model.to_dict(),
        "analysis": analysis.to_dict(),
    }
    committed = json.loads(DEVELOPMENT_GEOMETRY_PATH.read_text())

    assert committed == expected
    assert len(analysis.projected_frames) == 19
    assert len(analysis.solver_boundaries) == 2
    assert analysis.terminal_frame_id == campaign.frames[17].frame_id
