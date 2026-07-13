"""Reproducibility gate for the Phase IV Network Orientation V1 summary."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).parents[2]
RUNNER = ROOT / "validation" / "network_orientation_v1" / "run_validation.py"
CANONICAL = (
    ROOT / "validation" / "network_orientation_v1" / "canonical_summary.json"
)


def test_network_orientation_validation_is_byte_reproducible(tmp_path: Path) -> None:
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
