"""Reproducibility and evidence-boundary tests for Phase V WP G–H."""

from __future__ import annotations

import json
from pathlib import Path
import os
import subprocess
import sys

from PIL import Image


ROOT = Path(__file__).parents[2]
SHOWCASE = (
    ROOT
    / "APPLICATIONS"
    / "power_systems"
    / "ieee_geometry_v1"
    / "showcase"
)
GENERATOR = SHOWCASE / "generate_figures.py"
COMMITTED_FIGURES = SHOWCASE / "figures"
EXPECTED_FIGURES = (
    "01-physical-campaign.png",
    "02-path-geometry.png",
    "03-turning-geometry.png",
    "04-evidence-boundary.png",
)


def _generate(output: Path) -> None:
    environment = os.environ.copy()
    environment["MPLCONFIGDIR"] = str(output / "mpl-cache")
    environment["XDG_CACHE_HOME"] = str(output / "xdg-cache")
    subprocess.run(
        [sys.executable, str(GENERATOR), "--out-dir", str(output)],
        cwd=ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )


def test_showcase_figures_are_deterministic_in_current_runtime(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    _generate(first)
    _generate(second)

    for name in EXPECTED_FIGURES:
        assert (first / name).read_bytes() == (second / name).read_bytes()
        with Image.open(COMMITTED_FIGURES / name) as committed:
            assert committed.format == "PNG"
            assert committed.width > 1000
            assert committed.height > 500


def test_showcase_entry_depths_preserve_the_claim_boundary() -> None:
    map_text = (SHOWCASE / "90_SECOND_MAP.md").read_text(encoding="utf-8")
    quickstart = (SHOWCASE / "QUICKSTART_10_MINUTES.md").read_text(
        encoding="utf-8"
    )
    research = (SHOWCASE / "RESEARCH_PATH.md").read_text(encoding="utf-8")

    assert "not operational-grid measurements" in map_text
    assert "no sampled\nboundary" in map_text
    assert "parameter_retuning: false" in quickstart
    assert "deterministic within one declared runtime" in quickstart
    assert "Observed-Evidence Bridge" in research
    assert "not automatically physical invariants" in research


def test_observed_evidence_template_starts_closed_and_unadmitted() -> None:
    template_path = (
        ROOT
        / "testkit"
        / "observed_evidence"
        / "templates"
        / "observed_case_manifest.template.json"
    )
    template = json.loads(template_path.read_text(encoding="utf-8"))

    assert template["template_status"] == "not_evidence"
    assert template["observations"]["status"] == "not_acquired"
    assert template["outcome_plan"]["status"] == "not_acquired"
    assert template["outcome_plan"]["independent_source_required"] is True
    assert template["firewall"]["required_check_count"] == 6
    assert template["firewall"]["current_disposition"] == "indeterminate"
    assert template["firewall"]["episode_update_allowed"] is False
