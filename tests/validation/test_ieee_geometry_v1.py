"""Reproducibility and claim gates for Phase V IEEE Geometry V1."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).parents[2]
VALIDATION_DIR = ROOT / "validation" / "ieee_geometry_v1"
RUNNER = VALIDATION_DIR / "run_validation.py"
CANONICAL = VALIDATION_DIR / "canonical_summary.json"


def test_ieee_geometry_v1_replays_the_frozen_protocol(tmp_path: Path) -> None:
    output = tmp_path / "replayed.json"
    subprocess.run(
        [sys.executable, str(RUNNER), "--out", str(output)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    replayed = json.loads(output.read_text(encoding="utf-8"))
    canonical = json.loads(CANONICAL.read_text(encoding="utf-8"))
    checks = {check["check_id"]: check["passed"] for check in replayed["checks"]}

    # Solver and renderer byte streams may vary across operating systems even
    # under the frozen Python package set. The portable gate therefore checks
    # the declared protocol and its scientific boundary, while the committed
    # canonical artifact remains the reviewed reference for exact bytes.
    for check_id in (
        "environment-lock",
        "adapter-protocol",
        "development-freeze",
        "no-evaluation-refit",
        "failure-preservation",
        "outcome-boundary",
    ):
        assert checks[check_id] is True

    for field in (
        "declared_frames",
        "converged_frames",
        "failed_frames",
        "available_steps",
        "available_turns",
        "solver_boundaries",
    ):
        assert replayed["evaluation_result"][field] == canonical[
            "evaluation_result"
        ][field]
    assert replayed["freeze"] == canonical["freeze"]
    assert replayed["limitations"] == canonical["limitations"]


def test_ieee14_gate_preserves_freeze_results_and_boundaries() -> None:
    summary = json.loads(CANONICAL.read_text(encoding="utf-8"))

    assert summary["gate_passed"] is True
    assert all(check["passed"] for check in summary["checks"])
    assert summary["freeze"]["development_case"] == "ieee9"
    assert summary["freeze"]["evaluation_case"] == "ieee14"
    assert summary["freeze"]["parameter_retuning"] is False
    assert summary["evaluation_result"]["declared_frames"] == 19
    assert summary["evaluation_result"]["converged_frames"] == 19
    assert summary["evaluation_result"]["failed_frames"] == 0
    assert summary["evaluation_result"]["available_steps"] == 18
    assert summary["evaluation_result"]["available_turns"] == 17
    assert summary["evaluation_result"]["solver_boundaries"] == 0
    assert len(summary["claim_audit"]["supported"]) == 4
    assert len(summary["claim_audit"]["prohibited"]) == 7
    assert "No observed outcome exists" in summary["limitations"][-1]
