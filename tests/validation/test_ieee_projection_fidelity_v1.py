"""Canonical gate tests for IEEE Projection Fidelity V1."""

from __future__ import annotations

import json
from pathlib import Path

from validation.ieee_projection_fidelity_v1.run_validation import build_result


ROOT = Path(__file__).parents[2]
CANONICAL = (
    ROOT
    / "validation"
    / "ieee_projection_fidelity_v1"
    / "canonical_result.json"
)


def test_projection_fidelity_canonical_primary_gate() -> None:
    result = build_result()

    assert result["gate_passed"] is True
    assert result["status"] == "PASS"
    assert result["evaluation_refit"] is False
    assert result["development"]["case_id"] == "ieee9"
    assert result["evaluation"]["case_id"] == "ieee14"
    assert result["source_reproduction_max_error"] < 1e-12
    assert result["q_plus_r_raw_reconstruction_max_error"] < 1e-12
    assert result["q_plus_r_pair_distance_max_error"] < 1e-12
    assert result["q_only_kernel_max_distance"] < 1e-12
    assert result["q_plus_r_kernel_detection_rate"] == 1.0


def test_projection_fidelity_canonical_artifact_matches_runner() -> None:
    assert build_result() == json.loads(CANONICAL.read_text(encoding="utf-8"))
