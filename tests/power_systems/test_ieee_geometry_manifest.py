"""Frozen protocol tests for Phase V IEEE Geometry V1."""

from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys

import pytest

from nexah.power_systems import (
    IEEEGeometryCaseManifest,
    check_manifest_adapter_protocol,
    check_manifest_environment,
)


ROOT = Path(__file__).parents[2]
MANIFEST_PATH = (
    ROOT / "APPLICATIONS" / "power_systems" / "ieee_geometry_v1" / "case_manifest.json"
)


def _manifest() -> IEEEGeometryCaseManifest:
    return IEEEGeometryCaseManifest.from_dict(json.loads(MANIFEST_PATH.read_text()))


def test_canonical_manifest_round_trips_and_freezes_roles() -> None:
    manifest = _manifest()
    restored = IEEEGeometryCaseManifest.from_dict(
        json.loads(json.dumps(manifest.to_dict()))
    )

    assert restored == manifest
    assert {case.case_id: case.role for case in manifest.cases} == {
        "ieee9": "method_development",
        "ieee14": "locked_evaluation",
    }
    assert all(case.historically_inspected for case in manifest.cases)
    assert manifest.axis_is_time is False
    assert manifest.episode_update_allowed is False
    assert check_manifest_adapter_protocol(manifest) == ()


def test_environment_check_is_explicit_and_non_mutating() -> None:
    manifest = _manifest()
    installed = {lock.package: lock.exact_version for lock in manifest.software_locks}
    compatible = check_manifest_environment(
        manifest,
        installed_versions=installed,
        installed_python=manifest.python_exact_version,
    )
    mismatch = check_manifest_environment(
        manifest,
        installed_versions={**installed, "pandapower": "0.0.0"},
        installed_python=manifest.python_exact_version,
    )

    assert compatible.compatible is True
    assert compatible.mismatches == ()
    assert mismatch.compatible is False
    assert "pandapower" in mismatch.mismatches[0]
    assert manifest.software_locks[-2].exact_version == "3.4.0"


def test_manifest_rejects_time_and_memory_relabeling() -> None:
    manifest = _manifest()
    with pytest.raises(ValueError, match="must not be represented as time"):
        replace(manifest, axis_is_time=True)
    with pytest.raises(ValueError, match="cannot authorize episodic memory"):
        replace(manifest, episode_update_allowed=True)


def test_manifest_rejects_unknown_projection_input() -> None:
    manifest = _manifest()
    invalid_projection = replace(
        manifest.projections[0],
        inputs=manifest.projections[0].inputs + ("future_result",),
    )
    with pytest.raises(ValueError, match="unknown inputs"):
        replace(
            manifest,
            projections=(invalid_projection, *manifest.projections[1:]),
        )


def test_cli_validates_schema_environment_and_adapter_protocol() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "nexah.cli",
            "validate-ieee-manifest",
            str(MANIFEST_PATH),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)

    assert payload["schema_valid"] is True
    assert payload["adapter_protocol_compatible"] is True
    assert payload["case_roles"]["ieee14"] == "locked_evaluation"
    assert payload["outcome_status"] == "not_observed"
    assert payload["episode_update_allowed"] is False
