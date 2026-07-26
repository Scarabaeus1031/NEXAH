#!/usr/bin/env python3
"""Run the bounded G3 independent-equivalence gate.

IEEE-9 is generated and compared first.  Evaluation inputs are not loaded until
IEEE-9 passes.  This runner creates no Comparator output and never writes to
canonical artifact paths.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

from operators_v1 import build_independent_geometry, fit_ieee9_standardization


ABS_TOLERANCE = 1e-12
REL_TOLERANCE = 1e-10
APPROVED_PROTOCOL_SHA256 = (
    "bd9d0fa2094b17333b18ec7621f33fd32271c2e759f2b01c9b27f76702ffe5ba"
)

MODEL_FIELDS = [
    "manifest_id",
    "projection_id",
    "fit_campaign_id",
    "fit_case_id",
    "feature_names",
    "means",
    "population_stddevs",
    "status",
    "zero_variance_features",
    "reason",
]
PROJECTED_FIELDS = [
    "frame_id",
    "campaign_index",
    "load_scale",
    "status",
    "values",
    "reason",
]
STEP_COMMON_FIELDS = [
    "source_frame_id",
    "target_frame_id",
    "source_index",
    "target_index",
    "source_load_scale",
    "target_load_scale",
    "delta_load_scale",
    "status",
    "reason",
    "parameter_semantics",
]
TURN_COMMON_FIELDS = [
    "previous_frame_id",
    "center_frame_id",
    "next_frame_id",
    "center_index",
    "status",
    "reason",
]
BOUNDARY_FIELDS = [
    "failed_frame_id",
    "failed_index",
    "failed_load_scale",
    "last_converged_frame_id",
    "last_converged_load_scale",
    "status",
    "distance_load_scale",
    "solver_failure",
    "reason",
    "boundary_type",
]
SUMMARY_FIELDS = [
    "manifest_id",
    "campaign_id",
    "case_id",
    "case_role",
    "contiguous_converged_frame_ids",
    "total_path_length",
    "terminal_frame_id",
    "operator_ids",
]
OPERATOR_SPECS = {
    "adjacent-displacement-v1": ("steps", STEP_COMMON_FIELDS + ["delta_vector", "displacement"]),
    "normalized-local-drift-v1": ("steps", STEP_COMMON_FIELDS + ["normalized_local_drift"]),
    "campaign-path-length-v1": ("steps", STEP_COMMON_FIELDS + ["cumulative_path_length"]),
    "direction-change-v1": ("turns", TURN_COMMON_FIELDS + ["direction_change_radians"]),
    "discrete-curvature-v1": ("turns", TURN_COMMON_FIELDS + ["discrete_curvature"]),
    "distance-to-last-converged-v1": ("solver_boundaries", BOUNDARY_FIELDS),
}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_approved_protocol(repo_root: Path) -> dict[str, Any]:
    protocol_dir = (
        repo_root
        / "validation"
        / "ieee_geometry_external_replay_v1"
        / "protocol"
    )
    approved = protocol_dir / "g2_protocol_approved.json"
    record = _load_json(protocol_dir / "g2_approval_record.json")
    actual = _sha256(approved)
    if record["status"] != "approved":
        raise RuntimeError("G2 approval record is not approved")
    if record["protocol_id"] != "sr1-ieee-geometry-comparator-analysis-v1":
        raise RuntimeError("G2 protocol identity mismatch")
    if record["protocol_version"] != "1.0.0":
        raise RuntimeError("G2 protocol version mismatch")
    if actual != APPROVED_PROTOCOL_SHA256 or actual != record["approved_sha256"]:
        raise RuntimeError("approved G2 protocol digest mismatch")
    return {
        "protocol_id": record["protocol_id"],
        "protocol_version": record["protocol_version"],
        "sha256": actual,
        "verified": True,
    }


def verify_frozen_hashes(repo_root: Path) -> dict[str, Any]:
    expected_path = (
        repo_root
        / "validation"
        / "ieee_geometry_external_replay_v1"
        / "fixtures"
        / "expected_hashes.json"
    )
    expected = _load_json(expected_path)
    files: list[dict[str, Any]] = []
    for relative_path, expected_digest in expected["files"].items():
        actual = _sha256(repo_root / relative_path)
        files.append(
            {
                "path": relative_path,
                "expected_sha256": expected_digest,
                "actual_sha256": actual,
                "match": actual == expected_digest,
            }
        )
    return {
        "algorithm": "sha256",
        "all_match": all(item["match"] for item in files),
        "files": files,
    }


def _select(record: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    return {field: record.get(field) for field in fields}


def _numeric(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _compare_value(
    independent: Any,
    canonical: Any,
    path: str,
    discrepancies: list[dict[str, Any]],
) -> int:
    numeric_count = 0
    if independent is None or canonical is None:
        if independent is not None or canonical is not None:
            discrepancies.append(
                {
                    "path": path,
                    "kind": "null_mismatch",
                    "independent": independent,
                    "canonical": canonical,
                }
            )
        return numeric_count
    if (
        isinstance(independent, bool)
        or isinstance(canonical, bool)
        or (
            isinstance(independent, int)
            and not isinstance(independent, bool)
            and isinstance(canonical, int)
            and not isinstance(canonical, bool)
        )
    ):
        if type(independent) is not type(canonical) or independent != canonical:
            discrepancies.append(
                {
                    "path": path,
                    "kind": "exact_mismatch",
                    "independent": independent,
                    "canonical": canonical,
                }
            )
        return numeric_count
    if _numeric(independent) and _numeric(canonical):
        numeric_count += 1
        left = float(independent)
        right = float(canonical)
        if (
            not math.isfinite(left)
            or not math.isfinite(right)
            or abs(left - right)
            > ABS_TOLERANCE + REL_TOLERANCE * abs(right)
        ):
            discrepancies.append(
                {
                    "path": path,
                    "kind": "numeric_mismatch",
                    "independent": independent,
                    "canonical": canonical,
                    "absolute_difference": abs(left - right),
                    "allowed_difference": (
                        ABS_TOLERANCE + REL_TOLERANCE * abs(right)
                    ),
                }
            )
        return numeric_count
    if isinstance(independent, list) and isinstance(canonical, list):
        if len(independent) != len(canonical):
            discrepancies.append(
                {
                    "path": path,
                    "kind": "length_mismatch",
                    "independent": len(independent),
                    "canonical": len(canonical),
                }
            )
        for index, (left, right) in enumerate(zip(independent, canonical)):
            numeric_count += _compare_value(
                left, right, f"{path}[{index}]", discrepancies
            )
        return numeric_count
    if isinstance(independent, dict) and isinstance(canonical, dict):
        keys = list(dict.fromkeys([*independent.keys(), *canonical.keys()]))
        for key in keys:
            if key not in independent or key not in canonical:
                discrepancies.append(
                    {
                        "path": f"{path}.{key}",
                        "kind": "field_presence_mismatch",
                        "independent": independent.get(key),
                        "canonical": canonical.get(key),
                    }
                )
                continue
            numeric_count += _compare_value(
                independent[key],
                canonical[key],
                f"{path}.{key}",
                discrepancies,
            )
        return numeric_count
    if type(independent) is not type(canonical) or independent != canonical:
        discrepancies.append(
            {
                "path": path,
                "kind": "exact_mismatch",
                "independent": independent,
                "canonical": canonical,
            }
        )
    return numeric_count


def _formula_map(manifest: dict[str, Any]) -> dict[str, str]:
    return {item["operator_id"]: item["formula"] for item in manifest["operators"]}


def compare_case(
    independent: dict[str, Any],
    canonical: dict[str, Any],
    manifest: dict[str, Any],
) -> dict[str, Any]:
    all_discrepancies: list[dict[str, Any]] = []
    structural: list[dict[str, Any]] = []
    numeric_count = _compare_value(
        _select(independent["standardization_model"], MODEL_FIELDS),
        _select(canonical["standardization_model"], MODEL_FIELDS),
        "standardization_model",
        structural,
    )
    independent_analysis = independent["analysis"]
    canonical_analysis = canonical["analysis"]
    numeric_count += _compare_value(
        [
            _select(item, PROJECTED_FIELDS)
            for item in independent_analysis["projected_frames"]
        ],
        [
            _select(item, PROJECTED_FIELDS)
            for item in canonical_analysis["projected_frames"]
        ],
        "analysis.projected_frames",
        structural,
    )
    numeric_count += _compare_value(
        _select(independent_analysis, SUMMARY_FIELDS),
        _select(canonical_analysis, SUMMARY_FIELDS),
        "analysis.summary",
        structural,
    )
    all_discrepancies.extend(structural)

    formulas = _formula_map(manifest)
    operators: dict[str, dict[str, Any]] = {}
    for operator_id, (collection_name, fields) in OPERATOR_SPECS.items():
        discrepancies: list[dict[str, Any]] = []
        independent_records = independent_analysis[collection_name]
        canonical_records = canonical_analysis[collection_name]
        operator_numeric_count = _compare_value(
            [_select(item, fields) for item in independent_records],
            [_select(item, fields) for item in canonical_records],
            f"analysis.{collection_name}.{operator_id}",
            discrepancies,
        )
        for discrepancy in discrepancies:
            discrepancy["operator_id"] = operator_id
            discrepancy["formula"] = formulas[operator_id]
        all_discrepancies.extend(discrepancies)
        operators[operator_id] = {
            "records_compared": min(
                len(independent_records), len(canonical_records)
            ),
            "numeric_values_compared": operator_numeric_count,
            "discrepancy_count": len(discrepancies),
            "status": "equivalent" if not discrepancies else "mismatch",
        }

    first = all_discrepancies[0] if all_discrepancies else None
    return {
        "case_id": independent_analysis["case_id"],
        "case_role": independent_analysis["case_role"],
        "campaign_positions": len(independent_analysis["projected_frames"]),
        "adjacent_steps": len(independent_analysis["steps"]),
        "centered_turns": len(independent_analysis["turns"]),
        "solver_boundaries": len(independent_analysis["solver_boundaries"]),
        "structural_numeric_values_compared": numeric_count,
        "structural_discrepancy_count": len(structural),
        "operators": operators,
        "discrepancy_count": len(all_discrepancies),
        "first_divergence": first,
        "status": "equivalent" if not all_discrepancies else "mismatch",
        "discrepancies": all_discrepancies,
    }


def _write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def run(repo_root: Path, output_dir: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    output_dir = output_dir.resolve()
    if output_dir == repo_root or repo_root in output_dir.parents:
        raise ValueError("G3 output directory must be outside the repository")
    output_dir.mkdir(parents=True, exist_ok=True)

    protocol = verify_approved_protocol(repo_root)
    before_hashes = verify_frozen_hashes(repo_root)
    if not before_hashes["all_match"]:
        result = {
            "classification": "frozen_baseline_changed",
            "g2_protocol": protocol,
            "frozen_hashes_before": before_hashes,
            "g4_begun": False,
            "comparator_output_generated": False,
        }
        _write_json(output_dir / "g3_result.json", result)
        return result

    application = repo_root / "APPLICATIONS" / "power_systems" / "ieee_geometry_v1"
    manifest = _load_json(application / "case_manifest.json")
    development_frames = _load_json(application / "development_frames.json")
    model = fit_ieee9_standardization(manifest, development_frames)
    independent_ieee9 = build_independent_geometry(
        manifest, development_frames, model
    )
    _write_json(output_dir / "independent_ieee9_geometry.json", independent_ieee9)
    canonical_ieee9 = _load_json(application / "development_geometry.json")
    ieee9_result = compare_case(
        independent_ieee9, canonical_ieee9, manifest
    )

    ieee14_result: dict[str, Any] | None = None
    if ieee9_result["status"] == "equivalent":
        evaluation_frames = _load_json(application / "evaluation_frames.json")
        independent_ieee14 = build_independent_geometry(
            manifest, evaluation_frames, model
        )
        _write_json(
            output_dir / "independent_ieee14_geometry.json",
            independent_ieee14,
        )
        canonical_ieee14 = _load_json(application / "evaluation_geometry.json")
        ieee14_result = compare_case(
            independent_ieee14, canonical_ieee14, manifest
        )

    after_hashes = verify_frozen_hashes(repo_root)
    if not after_hashes["all_match"]:
        classification = "frozen_baseline_changed"
    elif ieee9_result["status"] != "equivalent":
        classification = "specification_ambiguity"
    elif ieee14_result is None:
        classification = "G3_blocked"
    elif ieee14_result["status"] != "equivalent":
        classification = "independent_implementation_mismatch"
    else:
        classification = "G3_equivalence_passed"

    discrepancies = {
        "ieee9": ieee9_result["discrepancies"],
        "ieee14": (
            ieee14_result["discrepancies"] if ieee14_result is not None else None
        ),
    }
    result = {
        "gate": "G3",
        "classification": classification,
        "contract": {
            "absolute_tolerance": ABS_TOLERANCE,
            "relative_tolerance": REL_TOLERANCE,
            "tolerance_changed_after_result": False,
        },
        "g2_protocol": protocol,
        "ieee9": {k: v for k, v in ieee9_result.items() if k != "discrepancies"},
        "ieee14": (
            {k: v for k, v in ieee14_result.items() if k != "discrepancies"}
            if ieee14_result is not None
            else None
        ),
        "frozen_hashes_before": before_hashes,
        "frozen_hashes_after": after_hashes,
        "comparator_output_generated": False,
        "g4_begun": False,
        "canonical_write_performed": False,
        "production_operator_imported": False,
    }
    _write_json(output_dir / "g3_discrepancy_ledger.json", discrepancies)
    _write_json(output_dir / "g3_result.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = run(args.repo_root, args.out)
    except Exception as exc:
        result = {
            "gate": "G3",
            "classification": "G3_blocked",
            "error": f"{type(exc).__name__}: {exc}",
            "comparator_output_generated": False,
            "g4_begun": False,
        }
        args.out.mkdir(parents=True, exist_ok=True)
        _write_json(args.out / "g3_result.json", result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["classification"] == "G3_equivalence_passed" else 1


if __name__ == "__main__":
    sys.exit(main())
