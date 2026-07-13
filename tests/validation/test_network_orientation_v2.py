"""Reproducibility and claim gates for Network Orientation V2."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).parents[2]
RUNNER = ROOT / "validation" / "network_orientation_v2" / "run_validation.py"
CANONICAL = (
    ROOT / "validation" / "network_orientation_v2" / "canonical_summary.json"
)


def test_network_orientation_v2_is_byte_reproducible(tmp_path: Path) -> None:
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


def test_v2_records_scope_without_inventing_an_outcome() -> None:
    summary = json.loads(CANONICAL.read_text(encoding="utf-8"))

    assert summary["probe_contract"]["probe_count"] == 5
    assert summary["probe_contract"]["all_read_only"] is True
    assert summary["probe_contract"]["outcome_recorded"] is False
    assert summary["distinct_topology_fixture"]["blocked_nodes"] == ["isolated"]
    assert summary["training_scenario"]["newly_unreachable"] == ["target"]
    assert "real-world cross-domain generalization" in summary["not_supported"]
