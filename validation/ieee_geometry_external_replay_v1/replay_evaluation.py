#!/usr/bin/env python3
"""Replay the frozen evaluation case only after approved-protocol verification."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path


APPROVED_SHA256 = (
    "bd9d0fa2094b17333b18ec7621f33fd32271c2e759f2b01c9b27f76702ffe5ba"
)


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def _verify_protocol(protocol: Path, approval_record: Path) -> dict:
    actual = _digest(protocol)
    record = _load(approval_record)
    if record.get("status") != "approved":
        raise RuntimeError("G2 approval status is not approved")
    if record.get("protocol_id") != "sr1-ieee-geometry-comparator-analysis-v1":
        raise RuntimeError("approved protocol ID mismatch")
    if record.get("protocol_version") != "1.0.0":
        raise RuntimeError("approved protocol version mismatch")
    if actual != APPROVED_SHA256 or actual != record.get("approved_sha256"):
        raise RuntimeError("approved protocol SHA-256 mismatch")
    return {
        "protocol_id": record["protocol_id"],
        "protocol_version": record["protocol_version"],
        "sha256": actual,
        "verified": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--sidecar-root", type=Path, required=True)
    parser.add_argument("--approved-protocol", type=Path, required=True)
    parser.add_argument("--approval-record", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    source_root = args.source_root.resolve()
    sidecar_root = args.sidecar_root.resolve()
    out = args.out.resolve()
    if source_root == out or source_root in out.parents:
        raise ValueError("evaluation output must be outside source root")

    # This verification intentionally precedes every evaluation source load.
    protocol = _verify_protocol(
        args.approved_protocol.resolve(), args.approval_record.resolve()
    )

    independent = sidecar_root / "independent"
    sys.path.insert(0, str(independent))
    from operators_v1 import (  # noqa: PLC0415
        build_independent_geometry,
        fit_ieee9_standardization,
    )
    from run_g3_equivalence import compare_case  # noqa: PLC0415

    case_root = source_root / "APPLICATIONS" / "power_systems" / "ieee_geometry_v1"
    manifest = _load(case_root / "case_manifest.json")
    development_frames = _load(case_root / "development_frames.json")
    model = fit_ieee9_standardization(manifest, development_frames)
    frames = _load(case_root / "evaluation_frames.json")
    canonical_geometry = _load(case_root / "evaluation_geometry.json")
    independent_geometry = build_independent_geometry(manifest, frames, model)
    comparison = compare_case(
        independent_geometry, canonical_geometry, manifest
    )

    out.mkdir(parents=True, exist_ok=True)
    canonical_output = out / "canonical_replay.json"
    command = [
        sys.executable,
        str(source_root / "validation" / "ieee_geometry_v1" / "run_validation.py"),
        "--out",
        str(canonical_output),
    ]
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=source_root,
        text=True,
        capture_output=True,
        check=False,
    )
    runtime = time.monotonic() - started
    canonical_result = _load(canonical_output) if canonical_output.exists() else None
    canonical_reference = _load(
        source_root / "validation" / "ieee_geometry_v1" / "canonical_summary.json"
    )
    required_checks = tuple(
        item["check_id"] for item in canonical_result["checks"]
    ) if canonical_result else ()
    check_map = (
        {
            item["check_id"]: item["passed"]
            for item in canonical_result["checks"]
        }
        if canonical_result
        else {}
    )
    required_checks_pass = all(check_map.get(item) is True for item in required_checks)
    result = {
        "command": "evaluation_replay",
        "protocol_verified_before_evaluation_load": protocol,
        "case_id": frames["case_id"],
        "case_role": frames["case_role"],
        "comparison": {
            key: value
            for key, value in comparison.items()
            if key != "discrepancies"
        },
        "canonical_command": command,
        "canonical_exit_code": completed.returncode,
        "canonical_runtime_seconds": runtime,
        "canonical_stdout": completed.stdout,
        "canonical_stderr": completed.stderr,
        "canonical_output_exists": canonical_output.exists(),
        "canonical_exact_json_match": canonical_result == canonical_reference,
        "required_checks": {
            item: check_map.get(item) for item in required_checks
        },
        "required_checks_pass": required_checks_pass,
        "campaign_positions": len(frames["frames"]),
        "failed_frames": sum(
            frame["status"] == "failed" for frame in frames["frames"]
        ),
        "comparator_output_generated": False,
        "status": (
            "passed"
            if comparison["status"] == "equivalent"
            and completed.returncode == 0
            and canonical_output.exists()
            and required_checks_pass
            and canonical_result.get("gate_passed") is True
            and canonical_result == canonical_reference
            and len(frames["frames"]) == 19
            else "failed"
        ),
    }
    _write(out / "evaluation_replay.json", result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "passed" else 1


def _write_blocked_result(error: Exception) -> None:
    """Record a machine-readable refusal without touching evaluation inputs."""
    try:
        out_index = sys.argv.index("--out") + 1
        out = Path(sys.argv[out_index]).resolve()
    except (ValueError, IndexError):
        return
    result = {
        "command": "evaluation_replay",
        "status": "blocked",
        "reason": str(error),
        "protocol_verified_before_evaluation_load": False,
        "evaluation_source_loaded": False,
        "comparator_output_generated": False,
    }
    _write(out / "evaluation_replay.json", result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:  # noqa: BLE001 - gate refusals must be recorded
        _write_blocked_result(error)
        print(f"evaluation replay blocked: {error}", file=sys.stderr)
        sys.exit(2)
