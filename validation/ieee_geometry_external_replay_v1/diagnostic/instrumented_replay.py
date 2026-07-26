#!/usr/bin/env python3
"""One-shot observational capture for the accepted failed G4 replay."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.metadata
import importlib.util
import io
import json
import math
import os
import platform
import struct
import subprocess
import sys
import sysconfig
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


THREAD_ENVIRONMENT_NAMES = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "BLIS_NUM_THREADS",
    "OMP_DYNAMIC",
    "OMP_PROC_BIND",
)
KEY_DISTRIBUTIONS = (
    "nexah",
    "numpy",
    "scipy",
    "pandas",
    "pandapower",
    "numba",
    "llvmlite",
)


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(source_root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=source_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip())
    return completed.stdout.strip()


def _file_record(path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "bytes": path.stat().st_size,
        "sha256": _sha256(path),
    }


def _distribution_record(name: str) -> dict[str, Any]:
    try:
        distribution = importlib.metadata.distribution(name)
    except importlib.metadata.PackageNotFoundError:
        return {"name": name, "installed": False}
    root = Path(distribution._path)  # type: ignore[attr-defined]
    metadata_files = {}
    for filename in ("METADATA", "WHEEL", "RECORD", "INSTALLER", "direct_url.json"):
        path = root / filename
        if path.is_file():
            metadata_files[filename] = _file_record(path)
            if filename in {"WHEEL", "INSTALLER", "direct_url.json"}:
                metadata_files[filename]["text"] = path.read_text(
                    encoding="utf-8", errors="replace"
                )
    binaries = []
    for item in distribution.files or ():
        if Path(item).suffix.lower() not in {".so", ".dylib", ".pyd"}:
            continue
        located = Path(distribution.locate_file(item))
        if located.is_file():
            binaries.append(_file_record(located))
    return {
        "name": distribution.metadata["Name"],
        "version": distribution.version,
        "installed": True,
        "dist_info": str(root),
        "metadata_files": metadata_files,
        "binary_extensions": binaries,
    }


def capture_environment(source_root: Path) -> dict[str, Any]:
    import numpy

    numpy_configuration = io.StringIO()
    with contextlib.redirect_stdout(numpy_configuration):
        numpy.show_config()
    pip_freeze = subprocess.run(
        [sys.executable, "-m", "pip", "freeze", "--all"],
        cwd=source_root,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PIP_NO_INDEX": "1"},
    )
    return {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "source_revision": _git(source_root, "rev-parse", "HEAD"),
        "source_status": _git(source_root, "status", "--porcelain=v1"),
        "operating_system": {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": _file_record(Path(sys.executable).resolve()),
            "cache_tag": sys.implementation.cache_tag,
            "abi_flags": getattr(sys, "abiflags", ""),
            "sys_prefix": sys.prefix,
            "sys_base_prefix": sys.base_prefix,
            "is_virtual_environment": sys.prefix != sys.base_prefix,
            "platform_tag": sysconfig.get_platform(),
            "configuration_arguments": sysconfig.get_config_var("CONFIG_ARGS"),
        },
        "installed_package_lock": {
            "command": [sys.executable, "-m", "pip", "freeze", "--all"],
            "exit_code": pip_freeze.returncode,
            "stdout": pip_freeze.stdout,
            "stderr": pip_freeze.stderr,
        },
        "key_distributions": [
            _distribution_record(name) for name in KEY_DISTRIBUTIONS
        ],
        "numpy_configuration": numpy_configuration.getvalue(),
        "thread_environment": {
            name: os.environ.get(name) for name in THREAD_ENVIRONMENT_NAMES
        },
        "pandapower_execution_identity": {
            "numba_module_available": importlib.util.find_spec("numba") is not None,
            "algorithm": "nr",
            "max_iteration": 30,
            "tolerance_mva": 1e-6,
            "initialization": "auto",
            "independent_load_points": True,
        },
    }


def _ordered_float_integer(value: float) -> int:
    bits = struct.unpack(">Q", struct.pack(">d", value))[0]
    if bits & (1 << 63):
        return (~bits) & ((1 << 64) - 1)
    return bits | (1 << 63)


def _numeric_record(path: str, value: int | float) -> dict[str, Any]:
    if isinstance(value, bool):
        raise TypeError("booleans are not numeric evidence")
    if isinstance(value, int):
        return {
            "path": path,
            "type": "int",
            "value": value,
            "repr": repr(value),
        }
    return {
        "path": path,
        "type": "float",
        "value": value,
        "repr": repr(value),
        "hex": value.hex(),
        "binary64_be_hex": struct.pack(">d", value).hex(),
        "ulp": math.ulp(value),
    }


def _path_key(path: str, key: str) -> str:
    return f"{path}/{key.replace('~', '~0').replace('/', '~1')}"


def _numeric_inventory(value: Any, path: str = "") -> list[dict[str, Any]]:
    records = []
    if isinstance(value, dict):
        for key in sorted(value):
            records.extend(_numeric_inventory(value[key], _path_key(path, key)))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            records.extend(_numeric_inventory(item, f"{path}/{index}"))
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        records.append(_numeric_record(path or "/", value))
    return records


def _recursive_diff(canonical: Any, fresh: Any) -> dict[str, Any]:
    differences: list[dict[str, Any]] = []
    order_differences: list[dict[str, Any]] = []
    counters = {
        "numeric": 0,
        "categorical": 0,
        "type": 0,
        "missing_key": 0,
        "length": 0,
        "mapping_order": 0,
    }

    def walk(left: Any, right: Any, path: str = "") -> None:
        if type(left) is not type(right):
            counters["type"] += 1
            differences.append(
                {
                    "path": path or "/",
                    "kind": "type",
                    "canonical_type": type(left).__name__,
                    "fresh_type": type(right).__name__,
                    "canonical": left,
                    "fresh": right,
                }
            )
            return
        if isinstance(left, dict):
            left_keys = list(left)
            right_keys = list(right)
            if left_keys != right_keys and set(left_keys) == set(right_keys):
                counters["mapping_order"] += 1
                order_differences.append(
                    {
                        "path": path or "/",
                        "kind": "mapping_key_order",
                        "canonical": left_keys,
                        "fresh": right_keys,
                    }
                )
            for key in sorted(set(left) | set(right)):
                child = _path_key(path, key)
                if key not in left or key not in right:
                    counters["missing_key"] += 1
                    differences.append(
                        {
                            "path": child,
                            "kind": "missing_key",
                            "canonical_present": key in left,
                            "fresh_present": key in right,
                        }
                    )
                else:
                    walk(left[key], right[key], child)
            return
        if isinstance(left, list):
            if len(left) != len(right):
                counters["length"] += 1
                differences.append(
                    {
                        "path": path or "/",
                        "kind": "length",
                        "canonical": len(left),
                        "fresh": len(right),
                    }
                )
            for index, (left_item, right_item) in enumerate(zip(left, right)):
                walk(left_item, right_item, f"{path}/{index}")
            return
        if left == right:
            return
        if isinstance(left, (int, float)) and not isinstance(left, bool):
            counters["numeric"] += 1
            record = {
                "path": path or "/",
                "kind": "numeric",
                "canonical": _numeric_record(path or "/", left),
                "fresh": _numeric_record(path or "/", right),
                "absolute_difference": abs(float(left) - float(right)),
                "relative_difference": (
                    abs(float(left) - float(right))
                    / max(abs(float(left)), abs(float(right)))
                    if max(abs(float(left)), abs(float(right))) != 0.0
                    else 0.0
                ),
            }
            if isinstance(left, float):
                record["ulp_distance"] = abs(
                    _ordered_float_integer(left) - _ordered_float_integer(right)
                )
            differences.append(record)
            return
        counters["categorical"] += 1
        differences.append(
            {
                "path": path or "/",
                "kind": "categorical",
                "canonical_type": type(left).__name__,
                "fresh_type": type(right).__name__,
                "canonical": left,
                "fresh": right,
            }
        )

    walk(canonical, fresh)
    return {
        "equal": not differences and not order_differences,
        "difference_count": len(differences),
        "order_difference_count": len(order_differences),
        "counts": counters,
        "first_difference": differences[0] if differences else None,
        "differences": differences,
        "order_differences": order_differences,
    }


def _verify_binding(
    protocol_path: Path,
    binding_path: Path,
    instrument_path: Path,
) -> dict[str, Any]:
    binding = _load(binding_path)
    protocol_sha256 = _sha256(protocol_path)
    instrument_sha256 = _sha256(instrument_path)
    if binding.get("status") != "approved":
        raise RuntimeError("diagnostic binding is not approved")
    if protocol_sha256 != binding.get("protocol_sha256"):
        raise RuntimeError("diagnostic protocol SHA-256 mismatch")
    if instrument_sha256 != binding.get("instrumentation_sha256"):
        raise RuntimeError("diagnostic instrumentation SHA-256 mismatch")
    return {
        "protocol_sha256": protocol_sha256,
        "instrumentation_sha256": instrument_sha256,
        "verified": True,
    }


def _artifact_manifest(out: Path) -> dict[str, Any]:
    artifacts = []
    for path in sorted(out.rglob("*")):
        if not path.is_file() or path.name == "artifact_manifest.json":
            continue
        artifacts.append(
            {
                "path": str(path.relative_to(out)),
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
            }
        )
    return {"algorithm": "sha256", "artifacts": artifacts}


def execute_once(
    source_root: Path,
    out: Path,
    protocol_path: Path,
    binding_path: Path,
) -> int:
    instrument_path = Path(__file__).resolve()
    binding = _verify_binding(
        protocol_path.resolve(), binding_path.resolve(), instrument_path
    )
    if out.exists():
        raise RuntimeError("diagnostic output directory already exists")
    if source_root == out or source_root in out.parents:
        raise RuntimeError("diagnostic output must be outside source root")
    out.mkdir(parents=True)
    ledger_path = out / "execution_ledger.json"
    _write(
        ledger_path,
        {
            "authorised_ieee14_diagnostic_attempts": 1,
            "attempt_number": 1,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "completed": False,
            "retry_permitted": False,
            "binding": binding,
        },
    )

    sys.path.insert(0, str(source_root))
    from nexah.orientation import render_orientation_brief_markdown
    from nexah.power_systems import (
        IEEEGeometryCampaign,
        IEEEGeometryCaseManifest,
        analyze_ieee_geometry,
        build_ieee_geometry_orientation_brief,
        check_manifest_adapter_protocol,
        check_manifest_environment,
        fit_ieee_standardization,
        run_ieee_geometry_probe_suite,
    )
    from validation.ieee_geometry_v1 import run_validation as canonical_runner

    case_dir = source_root / "APPLICATIONS" / "power_systems" / "ieee_geometry_v1"
    canonical = {
        "frames": _load(case_dir / "evaluation_frames.json"),
        "geometry": _load(case_dir / "evaluation_geometry.json"),
        "orientation": _load(case_dir / "evaluation_orientation.json"),
        "brief": _load(case_dir / "evaluation_orientation_brief.json"),
    }
    manifest_source = _load(case_dir / "case_manifest.json")
    manifest = IEEEGeometryCaseManifest.from_dict(manifest_source)
    development_campaign = IEEEGeometryCampaign.from_dict(
        _load(case_dir / "development_frames.json")
    )
    development_model = fit_ieee_standardization(development_campaign, manifest)
    development_analysis = analyze_ieee_geometry(
        development_campaign, manifest, development_model
    )

    # Exactly one scientific replay call. No output is written until all
    # numerical and categorical scientific objects have been computed.
    started = time.monotonic()
    evaluation_campaign = canonical_runner._fresh_evaluation_campaign(manifest)
    evaluation_analysis = analyze_ieee_geometry(
        evaluation_campaign, manifest, development_model
    )
    evaluation_context = run_ieee_geometry_probe_suite(
        evaluation_campaign, evaluation_analysis, manifest
    )
    evaluation_brief = build_ieee_geometry_orientation_brief(
        evaluation_context, manifest
    )
    evaluation_brief_markdown = render_orientation_brief_markdown(evaluation_brief)
    runtime_seconds = time.monotonic() - started

    fresh = {
        "frames": evaluation_campaign.to_dict(),
        "geometry": {
            "standardization_model": development_model.to_dict(),
            "analysis": evaluation_analysis.to_dict(),
        },
        "orientation": evaluation_context.to_dict(),
        "brief": evaluation_brief.to_dict(),
    }
    environment_check = check_manifest_environment(manifest)
    adapter_mismatches = check_manifest_adapter_protocol(manifest)
    comparisons = {
        name: _recursive_diff(canonical[name], fresh[name])
        for name in ("frames", "geometry", "orientation", "brief")
    }
    checks = {
        "environment_lock": environment_check.compatible,
        "adapter_protocol": not adapter_mismatches,
        "development_freeze": {
            "standardization_model": development_model.to_dict(),
            "analysis": development_analysis.to_dict(),
        }
        == _load(case_dir / "development_geometry.json"),
        "no_evaluation_refit": (
            evaluation_analysis.case_role == "locked_evaluation"
            and development_model.fit_case_id == "ieee9"
            and evaluation_analysis.projection_model == development_model
        ),
        "evaluation_source_replay": comparisons["frames"]["equal"],
        "evaluation_geometry_replay": comparisons["geometry"]["equal"],
        "evaluation_report_replay": comparisons["orientation"]["equal"],
        "evaluation_brief_replay": (
            comparisons["brief"]["equal"]
            and evaluation_brief_markdown
            == (case_dir / "evaluation_orientation_brief.md").read_text(
                encoding="utf-8"
            )
        ),
    }
    claim_audit_inputs = {
        "supported_claims": list(manifest.supported_claims),
        "prohibited_claims": list(manifest.prohibited_claims),
        "gate_checks": checks,
        "gate_passed": all(checks.values()),
        "outcome_status": manifest.outcome_status,
        "episode_update_allowed": manifest.episode_update_allowed,
    }

    fresh_dir = out / "fresh"
    _write(fresh_dir / "evaluation_frames.json", fresh["frames"])
    _write(fresh_dir / "evaluation_geometry.json", fresh["geometry"])
    _write(fresh_dir / "evaluation_orientation.json", fresh["orientation"])
    _write(fresh_dir / "evaluation_orientation_brief.json", fresh["brief"])
    (fresh_dir / "evaluation_orientation_brief.md").write_text(
        evaluation_brief_markdown, encoding="utf-8"
    )
    analysis_payload = fresh["geometry"]["analysis"]
    _write(
        fresh_dir / "geometry_projected_frames.json",
        analysis_payload["projected_frames"],
    )
    _write(fresh_dir / "geometry_steps.json", analysis_payload["steps"])
    _write(fresh_dir / "geometry_turns.json", analysis_payload["turns"])
    _write(
        fresh_dir / "geometry_solver_boundaries.json",
        analysis_payload["solver_boundaries"],
    )
    _write(fresh_dir / "orientation_report.json", fresh["orientation"]["report"])
    _write(fresh_dir / "claim_audit_inputs.json", claim_audit_inputs)
    _write(
        out / "raw_numeric_representations.json",
        {
            name: {
                "canonical": _numeric_inventory(canonical[name]),
                "fresh": _numeric_inventory(fresh[name]),
            }
            for name in ("frames", "geometry", "orientation", "brief")
        },
    )
    _write(
        out / "recursive_diff.json",
        {
            "deterministic_traversal": (
                "artifact order frames, geometry, orientation, brief; "
                "mapping keys sorted lexicographically; list indices ascending"
            ),
            "artifact_order": ["frames", "geometry", "orientation", "brief"],
            "artifacts": comparisons,
            "first_global_difference": next(
                (
                    {
                        "artifact": name,
                        **comparisons[name]["first_difference"],
                    }
                    for name in ("frames", "geometry", "orientation", "brief")
                    if comparisons[name]["first_difference"] is not None
                ),
                None,
            ),
        },
    )
    _write(
        out / "diagnostic_summary.json",
        {
            "binding": binding,
            "source_revision": _git(source_root, "rev-parse", "HEAD"),
            "source_status_after": _git(
                source_root, "status", "--porcelain=v1"
            ),
            "runtime_seconds": runtime_seconds,
            "exactly_one_ieee14_replay_attempted": True,
            "retry_permitted": False,
            "checks": checks,
            "claim_audit_inputs_path": "fresh/claim_audit_inputs.json",
            "first_global_difference": next(
                (
                    {
                        "artifact": name,
                        **comparisons[name]["first_difference"],
                    }
                    for name in ("frames", "geometry", "orientation", "brief")
                    if comparisons[name]["first_difference"] is not None
                ),
                None,
            ),
            "difference_counts": {
                name: comparisons[name]["counts"]
                for name in ("frames", "geometry", "orientation", "brief")
            },
            "comparator_output_generated": False,
            "g4_official_classification": "G4_clean_replay_failed",
            "g5_begun": False,
            "g6_begun": False,
        },
    )
    _write(
        ledger_path,
        {
            "authorised_ieee14_diagnostic_attempts": 1,
            "attempt_number": 1,
            "started_at": _load(ledger_path)["started_at"],
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "completed": True,
            "retry_permitted": False,
            "binding": binding,
        },
    )
    _write(out / "artifact_manifest.json", _artifact_manifest(out))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    environment_parser = subparsers.add_parser("capture-environment")
    environment_parser.add_argument("--source-root", type=Path, required=True)
    environment_parser.add_argument("--out", type=Path, required=True)
    execute_parser = subparsers.add_parser("execute-once")
    execute_parser.add_argument("--source-root", type=Path, required=True)
    execute_parser.add_argument("--out", type=Path, required=True)
    execute_parser.add_argument("--protocol", type=Path, required=True)
    execute_parser.add_argument("--binding", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "capture-environment":
        if args.out.exists():
            raise RuntimeError("environment output already exists")
        _write(args.out, capture_environment(args.source_root.resolve()))
        return 0
    return execute_once(
        args.source_root.resolve(),
        args.out.resolve(),
        args.protocol.resolve(),
        args.binding.resolve(),
    )


if __name__ == "__main__":
    sys.exit(main())
