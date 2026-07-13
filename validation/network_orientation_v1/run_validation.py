"""Reproduce the bounded Network Orientation V1 validation summary."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from nexah.applications import NetworkOrientationApplication, remove_declared_edge
from nexah.orientation import Context, Provenance


ROOT = Path(__file__).parents[2]
RECORDED_AT = datetime(2026, 7, 13, 22, 45, tzinfo=timezone.utc)


def _load(filename: str) -> dict[str, Any]:
    path = ROOT / "APPLICATIONS" / "datasets" / filename
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"fixture must be a JSON object: {filename}")
    return value


def _provenance(filename: str, method: str) -> Provenance:
    return Provenance(
        source=f"APPLICATIONS/datasets/{filename}",
        method=method,
        recorded_at=RECORDED_AT,
    )


def build_summary() -> dict[str, Any]:
    """Return the frozen, domain-bounded Phase IV validation summary."""

    application = NetworkOrientationApplication()
    supply = _load("supply_chain.json")
    supply_result = application.orient(
        supply,
        analysis_id="network-v1-supply-development",
        provenance=_provenance("supply_chain.json", "illustrative development fixture"),
        context=Context(domain="supply-chain", values={"role": "development"}),
        focus="normal_operation",
        target="system_disruption",
    )
    scenario = remove_declared_edge(
        supply,
        "production_slowdown",
        "distribution_backlog",
    )
    scenario_result = application.orient(
        scenario,
        baseline_source=supply,
        analysis_id="network-v1-supply-scenario",
        provenance=_provenance(
            "supply_chain.json", "declared edge-removal training scenario"
        ),
        baseline_provenance=_provenance(
            "supply_chain.json", "illustrative development fixture"
        ),
        context=Context(domain="supply-chain", values={"role": "scenario"}),
        focus="normal_operation",
        target="system_disruption",
    )
    ecosystem = _load("ecosystem_food_web.json")
    ecosystem_result = application.orient(
        ecosystem,
        analysis_id="network-v1-ecosystem-held-out",
        provenance=_provenance(
            "ecosystem_food_web.json", "illustrative held-out fixture"
        ),
        context=Context(domain="ecosystem", values={"role": "held-out"}),
        focus="balanced_ecosystem",
        target="ecosystem_collapse",
    )
    assert scenario_result.comparison is not None
    return {
        "validation_id": "network-orientation-v1",
        "recorded_at": RECORDED_AT.isoformat(),
        "development_fixture": {
            "domain": "supply-chain",
            "target_path": list(supply_result.structure.target_path or ()),
            "reachable_count": len(supply_result.structure.reachable_nodes),
            "blocked_count": len(supply_result.structure.blocked_nodes),
            "weak_articulation_points": list(
                supply_result.structure.weak_articulation_points
            ),
            "focus_critical_edges": [
                [edge.source, edge.target]
                for edge in supply_result.structure.focus_critical_edges
            ],
        },
        "training_scenario": {
            "removed_edge": ["production_slowdown", "distribution_backlog"],
            "newly_unreachable": list(
                scenario_result.comparison.newly_unreachable
            ),
            "target_path": (
                list(scenario_result.structure.target_path)
                if scenario_result.structure.target_path is not None
                else None
            ),
            "interpretation": "structural sensitivity, not causal response",
        },
        "held_out_fixture": {
            "domain": "ecosystem",
            "target_path": list(ecosystem_result.structure.target_path or ()),
            "reachable_count": len(ecosystem_result.structure.reachable_nodes),
            "blocked_count": len(ecosystem_result.structure.blocked_nodes),
            "focus_critical_edge_count": len(
                ecosystem_result.structure.focus_critical_edges
            ),
        },
        "supported": [
            "deterministic topology analysis of declared directed graphs",
            "domain-blind contract reuse across two illustrative fixtures",
            "focus-relative reachability and structural sensitivity comparison",
        ],
        "not_supported": [
            "real-world supply-chain or ecosystem generalization",
            "generalization to a topologically distinct graph family",
            "stability, risk, or causal intervention claims",
            "autonomous control",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    encoded = json.dumps(build_summary(), indent=2, sort_keys=True) + "\n"
    if args.out is None:
        print(encoded, end="")
    else:
        args.out.write_text(encoded, encoding="utf-8")


if __name__ == "__main__":
    main()
