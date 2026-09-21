"""Deterministic tests for the IEEE Projection Fidelity V1 sidecar."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from nexah.power_systems import (
    IEEEGeometryCampaign,
    IEEEProjectionFidelityAnalysis,
    IEEEProjectionFidelityError,
    build_ieee_projection_fidelity_analysis,
    fit_ieee_projection_fidelity_model,
)


ROOT = Path(__file__).parents[2]
CASE = ROOT / "APPLICATIONS" / "power_systems" / "ieee_geometry_v1"


def _campaign(name: str) -> IEEEGeometryCampaign:
    return IEEEGeometryCampaign.from_dict(
        json.loads((CASE / name).read_text(encoding="utf-8"))
    )


def test_projection_fidelity_sidecar_passes_without_evaluation_refit() -> None:
    analysis = build_ieee_projection_fidelity_analysis(
        _campaign("development_frames.json"),
        _campaign("evaluation_frames.json"),
    )

    assert analysis.status == "PASS"
    assert analysis.evaluation_refit is False
    assert analysis.model.fit_case_id == "ieee9"
    assert analysis.evaluation.case_id == "ieee14"
    assert analysis.source_reproduction_max_error == 0.0
    assert analysis.q_plus_r_raw_reconstruction_max_error < 1e-12
    assert analysis.q_plus_r_pair_distance_max_error < 1e-12
    assert analysis.q_only_kernel_max_distance < 1e-12
    assert analysis.q_plus_r_kernel_detection_rate == 1.0

    holdout = {item.representation: item for item in analysis.evaluation.metrics}
    assert holdout["PCA7"].pair_distance_nrmse < holdout["Q_ONLY7"].pair_distance_nrmse
    assert holdout["Q_PLUS_R8"].stored_scalars == 8


def test_projection_fidelity_contract_roundtrips() -> None:
    analysis = build_ieee_projection_fidelity_analysis(
        _campaign("development_frames.json"),
        _campaign("evaluation_frames.json"),
    )
    assert IEEEProjectionFidelityAnalysis.from_dict(analysis.to_dict()) == analysis


def test_projection_fidelity_fit_rejects_evaluation_campaign() -> None:
    evaluation = _campaign("evaluation_frames.json")
    with pytest.raises(IEEEProjectionFidelityError, match="method_development"):
        fit_ieee_projection_fidelity_model(evaluation)
