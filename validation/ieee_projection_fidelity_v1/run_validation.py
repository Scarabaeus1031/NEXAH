"""Build the canonical IEEE Projection Fidelity V1 sidecar result."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from nexah.power_systems import (
    IEEEGeometryCampaign,
    build_ieee_projection_fidelity_analysis,
)


ROOT = Path(__file__).parents[2]
GEOMETRY = ROOT / "APPLICATIONS" / "power_systems" / "ieee_geometry_v1"
SIDECAR = ROOT / "APPLICATIONS" / "power_systems" / "ieee_projection_fidelity_v1"
DEFAULT_OUTPUT = Path(__file__).with_name("canonical_result.json")


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def build_result() -> dict[str, Any]:
    """Return the canonical sidecar result from committed source frames."""

    development_path = GEOMETRY / "development_frames.json"
    evaluation_path = GEOMETRY / "evaluation_frames.json"
    protocol_path = SIDECAR / "protocol.json"
    development = IEEEGeometryCampaign.from_dict(_load(development_path))
    evaluation = IEEEGeometryCampaign.from_dict(_load(evaluation_path))
    analysis = build_ieee_projection_fidelity_analysis(development, evaluation)
    payload = analysis.to_dict()
    payload["protocol_sha256"] = _hash(protocol_path)
    payload["source_sha256"] = {
        "case_manifest.json": _hash(GEOMETRY / "case_manifest.json"),
        "development_frames.json": _hash(development_path),
        "evaluation_frames.json": _hash(evaluation_path),
    }
    payload["gate_passed"] = analysis.status == "PASS"
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    payload = build_result()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "decision": payload["decision"],
                "gate_passed": payload["gate_passed"],
            }
        )
    )
    raise SystemExit(0 if payload["gate_passed"] else 1)


if __name__ == "__main__":
    main()
