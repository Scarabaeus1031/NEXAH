from __future__ import annotations

import ast
import importlib
import json
import sys
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[3]
SIDECAR = REPO_ROOT / "validation" / "ieee_geometry_external_replay_v1"
INDEPENDENT = SIDECAR / "independent"
APPLICATION = REPO_ROOT / "APPLICATIONS" / "power_systems" / "ieee_geometry_v1"

sys.path.insert(0, str(INDEPENDENT))
operators = importlib.import_module("operators_v1")
runner = importlib.import_module("run_g3_equivalence")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_g2_approved_protocol_binding():
    record = runner.verify_approved_protocol(REPO_ROOT)
    assert record == {
        "protocol_id": "sr1-ieee-geometry-comparator-analysis-v1",
        "protocol_version": "1.0.0",
        "sha256": "bd9d0fa2094b17333b18ec7621f33fd32271c2e759f2b01c9b27f76702ffe5ba",
        "verified": True,
    }


def test_independent_sources_do_not_import_production_operators():
    prohibited_roots = {
        "nexah",
        "APPLICATIONS",
        "validation.ieee_geometry_v1",
    }
    for source_path in [
        INDEPENDENT / "operators_v1.py",
        INDEPENDENT / "run_g3_equivalence.py",
    ]:
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        imported = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.append(node.module or "")
        assert not any(
            name == root or name.startswith(root + ".")
            for name in imported
            for root in prohibited_roots
        )
    operator_source = (INDEPENDENT / "operators_v1.py").read_text(
        encoding="utf-8"
    )
    assert "operators_v1" not in operator_source
    assert "ieee14" not in operator_source.lower()


def test_ieee9_equivalence_and_failure_gap_policy():
    manifest = load_json(APPLICATION / "case_manifest.json")
    frames = load_json(APPLICATION / "development_frames.json")
    model = operators.fit_ieee9_standardization(manifest, frames)
    independent = operators.build_independent_geometry(manifest, frames, model)
    canonical = load_json(APPLICATION / "development_geometry.json")
    comparison = runner.compare_case(independent, canonical, manifest)

    assert comparison["status"] == "equivalent"
    assert comparison["campaign_positions"] == 19
    assert comparison["adjacent_steps"] == 18
    assert comparison["centered_turns"] == 17
    assert comparison["solver_boundaries"] == 2
    assert comparison["discrepancy_count"] == 0

    analysis = independent["analysis"]
    assert [item["status"] for item in analysis["projected_frames"][-2:]] == [
        "insufficient",
        "insufficient",
    ]
    assert analysis["steps"][16]["status"] == "insufficient"
    assert analysis["steps"][16]["displacement"] is None
    assert analysis["steps"][17]["reason"].startswith(
        "sampled path already terminated at "
    )
    assert analysis["turns"][15]["direction_change_radians"] is None
    assert analysis["terminal_frame_id"].endswith("load-017:geometry-frame")


def test_ieee14_is_not_loaded_when_ieee9_comparison_fails(tmp_path):
    loaded_paths = []
    original_load_json = runner._load_json

    def tracking_load(path):
        loaded_paths.append(Path(path).name)
        return original_load_json(path)

    forced_ieee9 = {
        "case_id": "ieee9",
        "case_role": "method_development",
        "campaign_positions": 19,
        "adjacent_steps": 18,
        "centered_turns": 17,
        "solver_boundaries": 2,
        "structural_numeric_values_compared": 0,
        "structural_discrepancy_count": 1,
        "operators": {},
        "discrepancy_count": 1,
        "first_divergence": {"path": "forced"},
        "status": "mismatch",
        "discrepancies": [{"path": "forced"}],
    }
    with patch.object(runner, "_load_json", side_effect=tracking_load):
        with patch.object(runner, "compare_case", return_value=forced_ieee9):
            result = runner.run(REPO_ROOT, tmp_path / "g3-stop")

    assert result["classification"] == "specification_ambiguity"
    assert "evaluation_frames.json" not in loaded_paths
    assert "evaluation_geometry.json" not in loaded_paths


def test_full_g3_equivalence_is_conditional_and_disposable(tmp_path):
    before = runner.verify_frozen_hashes(REPO_ROOT)
    output_dir = tmp_path / "g3-output"
    result = runner.run(REPO_ROOT, output_dir)
    after = runner.verify_frozen_hashes(REPO_ROOT)

    assert result["classification"] == "G3_equivalence_passed"
    assert result["ieee9"]["status"] == "equivalent"
    assert result["ieee14"]["status"] == "equivalent"
    assert result["ieee14"]["campaign_positions"] == 19
    assert result["ieee14"]["adjacent_steps"] == 18
    assert result["ieee14"]["centered_turns"] == 17
    assert result["ieee14"]["solver_boundaries"] == 0
    assert result["comparator_output_generated"] is False
    assert result["g4_begun"] is False
    assert result["canonical_write_performed"] is False
    assert before["all_match"] and after["all_match"]
    assert [
        (item["path"], item["actual_sha256"]) for item in before["files"]
    ] == [
        (item["path"], item["actual_sha256"]) for item in after["files"]
    ]

    output_names = {path.name for path in output_dir.iterdir()}
    assert output_names == {
        "g3_discrepancy_ledger.json",
        "g3_result.json",
        "independent_ieee9_geometry.json",
        "independent_ieee14_geometry.json",
    }
    assert not any("comparator" in name.lower() for name in output_names)


def test_per_operator_discrepancies_are_zero(tmp_path):
    result = runner.run(REPO_ROOT, tmp_path / "g3-operators")
    for case in ["ieee9", "ieee14"]:
        assert set(result[case]["operators"]) == set(runner.OPERATOR_SPECS)
        assert all(
            record["discrepancy_count"] == 0
            for record in result[case]["operators"].values()
        )
