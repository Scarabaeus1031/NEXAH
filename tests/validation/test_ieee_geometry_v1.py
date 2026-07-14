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


def test_ieee_geometry_v1_is_byte_reproducible(tmp_path: Path) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    for output in (first, second):
        subprocess.run(
            [sys.executable, str(RUNNER), "--out", str(output)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    assert first.read_bytes() == second.read_bytes()
    assert first.read_bytes() == CANONICAL.read_bytes()


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
