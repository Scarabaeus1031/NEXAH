#!/usr/bin/env python3
"""Run the bounded G4 clean replay without changing frozen V1 sources."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.metadata
import io
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


APPROVED_PROTOCOL_SHA256 = (
    "bd9d0fa2094b17333b18ec7621f33fd32271c2e759f2b01c9b27f76702ffe5ba"
)
EXPECTED_DIRECT_VERSIONS = {
    "numpy": "1.26.4",
    "pandas": "2.3.3",
    "pandapower": "3.4.0",
    "scipy": "1.13.1",
    "pytest": "7.4.4",
}


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


def _inside(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def _git(source_root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=source_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({completed.returncode}): "
            f"{completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def _verify_hashes(source_root: Path, expected_path: Path) -> dict:
    expected = _load(expected_path)
    files = []
    for relative, expected_digest in sorted(expected["files"].items()):
        target = source_root / relative
        actual = _sha256(target) if target.is_file() else None
        files.append(
            {
                "path": relative,
                "expected_sha256": expected_digest,
                "actual_sha256": actual,
                "match": actual == expected_digest,
            }
        )
    return {
        "algorithm": "sha256",
        "baseline_revision": expected["baseline_revision"],
        "all_match": all(item["match"] for item in files),
        "files": files,
    }


def _run(command: list[str], cwd: Path, environment: dict[str, str]) -> dict:
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "command": command,
        "cwd": str(cwd),
        "exit_code": completed.returncode,
        "runtime_seconds": time.monotonic() - started,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def _environment_record(source_root: Path) -> dict:
    import numpy

    numpy_config = io.StringIO()
    with contextlib.redirect_stdout(numpy_config):
        numpy.show_config()
    versions = {}
    for package in (*EXPECTED_DIRECT_VERSIONS, "nexah"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    base = {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_executable": sys.executable,
        "sys_prefix": sys.prefix,
        "sys_base_prefix": sys.base_prefix,
        "is_virtual_environment": sys.prefix != sys.base_prefix,
        "platform": platform.platform(),
        "operating_system": platform.system(),
        "operating_system_release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "direct_package_versions": versions,
        "expected_direct_package_versions": EXPECTED_DIRECT_VERSIONS,
        "numpy_blas_lapack_configuration": numpy_config.getvalue(),
    }
    offline_environment = dict(os.environ)
    offline_environment["PIP_NO_INDEX"] = "1"
    base["pip_check"] = _run(
        [sys.executable, "-m", "pip", "check"], source_root, offline_environment
    )
    base["pip_freeze_all"] = _run(
        [sys.executable, "-m", "pip", "freeze", "--all"],
        source_root,
        offline_environment,
    )
    base["exact_environment_match"] = (
        base["python_version"] == "3.12.7"
        and base["is_virtual_environment"]
        and all(versions[name] == value for name, value in EXPECTED_DIRECT_VERSIONS.items())
        and base["pip_check"]["exit_code"] == 0
    )
    return base


def _artifact_hashes(out: Path) -> list[dict]:
    excluded = {"g4_result.json", "artifact_hashes.json"}
    return [
        {
            "path": str(path.relative_to(out)),
            "sha256": _sha256(path),
            "bytes": path.stat().st_size,
        }
        for path in sorted(out.rglob("*"))
        if path.is_file() and path.name not in excluded
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    sidecar = Path(__file__).resolve().parent
    source_root = args.source_root.resolve()
    out = args.out.resolve()
    if _inside(out, source_root) or _inside(out, sidecar):
        raise ValueError("G4 output must be outside the source checkout and sidecar")
    out.mkdir(parents=True, exist_ok=False)

    protocol = sidecar / "protocol" / "g2_protocol_approved.json"
    approval = sidecar / "protocol" / "g2_approval_record.json"
    g3_result_path = sidecar / "reports" / "g3_equivalence_result.json"
    expected_hashes = sidecar / "fixtures" / "expected_hashes.json"

    approval_record = _load(approval)
    protocol_digest = _sha256(protocol)
    g3_result = _load(g3_result_path)
    source_revision = _git(source_root, "rev-parse", "HEAD")
    source_status_before = _git(source_root, "status", "--porcelain=v1")
    hashes_before = _verify_hashes(source_root, expected_hashes)
    environment = _environment_record(source_root)

    entry_checks = {
        "approved_protocol_bytes_match": (
            protocol_digest == APPROVED_PROTOCOL_SHA256
            and protocol_digest == approval_record.get("approved_sha256")
            and approval_record.get("status") == "approved"
        ),
        "g3_equivalence_accepted": (
            g3_result.get("classification") == "G3_equivalence_passed"
            and g3_result.get("ieee9", {}).get("discrepancy_count") == 0
            and g3_result.get("ieee14", {}).get("discrepancy_count") == 0
        ),
        "frozen_hashes_match": hashes_before["all_match"],
        "source_revision_matches": (
            source_revision == args.source_revision
            and source_revision == hashes_before["baseline_revision"]
        ),
        "source_checkout_clean": not source_status_before,
        "exact_clean_environment": environment["exact_environment_match"],
    }
    entry_record = {
        "gate": "G4",
        "protocol": {
            "path": str(protocol),
            "approved_sha256": APPROVED_PROTOCOL_SHA256,
            "actual_sha256": protocol_digest,
        },
        "g3_result": {
            "path": str(g3_result_path),
            "classification": g3_result.get("classification"),
            "ieee9_discrepancies": g3_result.get("ieee9", {}).get(
                "discrepancy_count"
            ),
            "ieee14_discrepancies": g3_result.get("ieee14", {}).get(
                "discrepancy_count"
            ),
        },
        "source_revision": source_revision,
        "requested_source_revision": args.source_revision,
        "source_status_before": source_status_before,
        "checks": entry_checks,
        "all_pass": all(entry_checks.values()),
    }
    _write(out / "entry_verification.json", entry_record)
    _write(out / "environment_identity.json", environment)
    _write(out / "frozen_hashes_before.json", hashes_before)

    if not entry_record["all_pass"]:
        result = {
            "gate": "G4",
            "classification": "G4_blocked",
            "entry_verification": entry_record,
            "commands": [],
            "g5_begun": False,
            "canonical_v1_write_performed": False,
            "commit_created": False,
        }
        _write(out / "g4_result.json", result)
        return 2

    offline_environment = dict(os.environ)
    offline_environment["PIP_NO_INDEX"] = "1"
    commands = []

    development_out = out / "development"
    development_command = [
        sys.executable,
        str(sidecar / "replay_development.py"),
        "--source-root",
        str(source_root),
        "--sidecar-root",
        str(sidecar),
        "--out",
        str(development_out),
    ]
    development_record = _run(
        development_command, source_root, offline_environment
    )
    commands.append({"command_id": "ieee9-development-replay", **development_record})
    if development_record["exit_code"] != 0:
        evaluation_authorised = False
    else:
        evaluation_authorised = True

    # Negative control: a byte-altered protocol must refuse before evaluation load.
    control_dir = out / "protocol_hash_refusal_control"
    control_dir.mkdir(parents=True)
    mismatched_protocol = control_dir / "g2_protocol_byte_altered.json"
    mismatched_protocol.write_bytes(protocol.read_bytes() + b"\n")
    refusal_out = control_dir / "result"
    refusal_command = [
        sys.executable,
        str(sidecar / "replay_evaluation.py"),
        "--source-root",
        str(source_root),
        "--sidecar-root",
        str(sidecar),
        "--approved-protocol",
        str(mismatched_protocol),
        "--approval-record",
        str(approval),
        "--out",
        str(refusal_out),
    ]
    refusal_record = _run(refusal_command, source_root, offline_environment)
    commands.append({"command_id": "protocol-hash-refusal-control", **refusal_record})
    refusal_result_path = refusal_out / "evaluation_replay.json"
    refusal_result = (
        _load(refusal_result_path) if refusal_result_path.is_file() else {}
    )
    refusal_passed = (
        refusal_record["exit_code"] != 0
        and refusal_result.get("status") == "blocked"
        and refusal_result.get("evaluation_source_loaded") is False
        and refusal_result.get("comparator_output_generated") is False
    )
    evaluation_authorised = evaluation_authorised and refusal_passed

    evaluation_out = out / "evaluation"
    if evaluation_authorised:
        evaluation_command = [
            sys.executable,
            str(sidecar / "replay_evaluation.py"),
            "--source-root",
            str(source_root),
            "--sidecar-root",
            str(sidecar),
            "--approved-protocol",
            str(protocol),
            "--approval-record",
            str(approval),
            "--out",
            str(evaluation_out),
        ]
        evaluation_record = _run(
            evaluation_command, source_root, offline_environment
        )
    else:
        evaluation_record = {
            "command": [],
            "cwd": str(source_root),
            "exit_code": None,
            "runtime_seconds": 0.0,
            "stdout": "",
            "stderr": "evaluation not run because a prerequisite control failed",
        }
    commands.append({"command_id": "ieee14-evaluation-replay", **evaluation_record})

    pytest_command = [
        sys.executable,
        "-m",
        "pytest",
        "tests/validation/test_ieee_geometry_v1.py",
        "-q",
    ]
    pytest_record = _run(pytest_command, source_root, offline_environment)
    commands.append({"command_id": "frozen-v1-tests", **pytest_record})

    hashes_after = _verify_hashes(source_root, expected_hashes)
    source_status_after = _git(source_root, "status", "--porcelain=v1")
    development_result_path = development_out / "development_replay.json"
    evaluation_result_path = evaluation_out / "evaluation_replay.json"
    development_result = (
        _load(development_result_path) if development_result_path.is_file() else {}
    )
    evaluation_result = (
        _load(evaluation_result_path) if evaluation_result_path.is_file() else {}
    )
    all_commands_pass = (
        development_record["exit_code"] == 0
        and refusal_passed
        and evaluation_record["exit_code"] == 0
        and pytest_record["exit_code"] == 0
    )
    scientific_boundaries = {
        "development_case": development_result.get("case_id"),
        "development_role": development_result.get("case_role"),
        "development_failed_frames": development_result.get("failed_frames"),
        "development_failure_policy_preserved": development_result.get(
            "failure_policy_preserved"
        ),
        "evaluation_case": evaluation_result.get("case_id"),
        "evaluation_role": evaluation_result.get("case_role"),
        "evaluation_campaign_positions": evaluation_result.get(
            "campaign_positions"
        ),
        "evaluation_failed_frames": evaluation_result.get("failed_frames"),
        "comparator_output_generated": any(
            item.get("comparator_output_generated") is True
            for item in (development_result, refusal_result, evaluation_result)
        ),
        "combined_score_generated": False,
        "post_hoc_metric_added": False,
    }
    canonical_replay_exact = evaluation_result.get("canonical_exact_json_match")
    canonical_replay_checks_pass = evaluation_result.get("required_checks_pass")
    classification = (
        "G4_clean_replay_passed"
        if all_commands_pass
        and hashes_after["all_match"]
        and not source_status_after
        and canonical_replay_exact is True
        and canonical_replay_checks_pass is True
        and scientific_boundaries["development_case"] == "ieee9"
        and scientific_boundaries["development_role"] == "method_development"
        and scientific_boundaries["evaluation_case"] == "ieee14"
        and scientific_boundaries["evaluation_role"] == "locked_evaluation"
        and scientific_boundaries["evaluation_campaign_positions"] == 19
        and not scientific_boundaries["comparator_output_generated"]
        else "G4_clean_replay_failed"
    )
    result = {
        "gate": "G4",
        "classification": classification,
        "entry_verification": entry_record,
        "environment_path": "environment_identity.json",
        "commands": commands,
        "protocol_hash_refusal_control_passed": refusal_passed,
        "canonical_replay_exact_json_match": canonical_replay_exact,
        "canonical_replay_checks_pass": canonical_replay_checks_pass,
        "scientific_boundaries": scientific_boundaries,
        "frozen_hashes_before_path": "frozen_hashes_before.json",
        "frozen_hashes_after_path": "frozen_hashes_after.json",
        "frozen_hashes_after_all_match": hashes_after["all_match"],
        "source_status_before": source_status_before,
        "source_status_after": source_status_after,
        "source_checkout_remained_clean": not source_status_after,
        "reader_route_required_manual_data_edit": False,
        "reader_route_required_network_during_replay": False,
        "reader_route_used_declared_commands_only": True,
        "g5_begun": False,
        "g6_begun": False,
        "canonical_v1_write_performed": False,
        "commit_created": False,
    }
    _write(out / "frozen_hashes_after.json", hashes_after)
    _write(out / "g4_result.json", result)
    artifacts = _artifact_hashes(out)
    _write(
        out / "artifact_hashes.json",
        {"algorithm": "sha256", "artifacts": artifacts},
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if classification == "G4_clean_replay_passed" else 1


if __name__ == "__main__":
    sys.exit(main())
