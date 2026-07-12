"""Command-line characterization for the NEXAH v0.7 baseline."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np


def test_analyze_command_emits_json(tmp_path: Path) -> None:
    signal = np.sin(np.linspace(0.0, 8.0 * np.pi, 120))
    source = tmp_path / "signal.csv"
    np.savetxt(source, signal, delimiter=",")

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "nexah.cli",
            "analyze",
            str(source),
            "--clusters",
            "3",
            "--window",
            "8",
            "--seed",
            "5",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    report = json.loads(completed.stdout)
    assert report["config"]["n_clusters"] == 3
    assert report["config"]["window"] == 8
    assert "transitions" in report

