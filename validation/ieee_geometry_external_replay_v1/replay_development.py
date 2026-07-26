#!/usr/bin/env python3
"""Replay only the frozen method-development case into a disposable output."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--sidecar-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    source_root = args.source_root.resolve()
    sidecar_root = args.sidecar_root.resolve()
    out = args.out.resolve()
    if source_root == out or source_root in out.parents:
        raise ValueError("development output must be outside source root")

    independent = sidecar_root / "independent"
    sys.path.insert(0, str(independent))
    from operators_v1 import (  # noqa: PLC0415
        build_independent_geometry,
        fit_ieee9_standardization,
    )
    from run_g3_equivalence import compare_case  # noqa: PLC0415

    case_root = source_root / "APPLICATIONS" / "power_systems" / "ieee_geometry_v1"
    manifest = _load(case_root / "case_manifest.json")
    frames = _load(case_root / "development_frames.json")
    canonical = _load(case_root / "development_geometry.json")
    model = fit_ieee9_standardization(manifest, frames)
    independent_geometry = build_independent_geometry(manifest, frames, model)
    comparison = compare_case(independent_geometry, canonical, manifest)

    failed = [frame for frame in frames["frames"] if frame["status"] == "failed"]
    result = {
        "command": "development_replay",
        "case_id": frames["case_id"],
        "case_role": frames["case_role"],
        "comparison": {
            key: value
            for key, value in comparison.items()
            if key != "discrepancies"
        },
        "failed_frames": [
            {
                "campaign_index": frame["campaign_index"],
                "load_scale": frame["load_scale"],
                "failure": frame["failure"],
                "system_features": frame["system_features"],
                "entity_view_count": len(frame["entity_views"]),
            }
            for frame in failed
        ],
        "failure_policy_preserved": all(
            frame["system_features"] is None and not frame["entity_views"]
            for frame in failed
        ),
        "gap_bridged": False,
        "comparator_output_generated": False,
        "status": (
            "passed"
            if comparison["status"] == "equivalent"
            and len(failed) == 2
            and all(
                frame["system_features"] is None and not frame["entity_views"]
                for frame in failed
            )
            else "failed"
        ),
    }
    _write(out / "development_replay.json", result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())

