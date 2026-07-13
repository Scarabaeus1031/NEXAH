"""Reproduce Network Orientation V2 probe and topology validation."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from nexah.applications import (
    NetworkOrientationApplication,
    remove_declared_edge,
    run_network_probe_suite,
)
from nexah.orientation import Context, Provenance


ROOT = Path(__file__).parents[2]
VALIDATION_DIR = Path(__file__).parent
RECORDED_AT = datetime(2026, 7, 13, 22, 45, tzinfo=timezone.utc)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"fixture must be a JSON object: {path}")
    return value


def _provenance(path: Path, method: str) -> Provenance:
    return Provenance(
        source=str(path.relative_to(ROOT)),
        method=method,
        recorded_at=RECORDED_AT,
    )


def _orient(
    source: dict[str, Any],
    *,
    path: Path,
    analysis_id: str,
    domain: str,
    focus: str,
    target: str,
    baseline: dict[str, Any] | None = None,
):
    result = NetworkOrientationApplication().orient(
        source,
        baseline_source=baseline,
        analysis_id=analysis_id,
        provenance=_provenance(path, "illustrative V2 validation fixture"),
        baseline_provenance=(
            _provenance(path, "illustrative V2 baseline fixture")
            if baseline is not None
            else None
        ),
        context=Context(domain=domain, values={"role": "illustrative-validation"}),
        focus=focus,
        target=target,
    )
    return result, run_network_probe_suite(result)


def build_summary() -> dict[str, Any]:
    """Return the frozen V2 summary without changing the V1 record."""

    supply_path = ROOT / "APPLICATIONS" / "datasets" / "supply_chain.json"
    supply = _load(supply_path)
    supply_result, supply_learning = _orient(
        supply,
        path=supply_path,
        analysis_id="network-v2-supply",
        domain="supply-chain",
        focus="normal_operation",
        target="system_disruption",
    )

    ecosystem_path = ROOT / "APPLICATIONS" / "datasets" / "ecosystem_food_web.json"
    ecosystem = _load(ecosystem_path)
    ecosystem_result, ecosystem_learning = _orient(
        ecosystem,
        path=ecosystem_path,
        analysis_id="network-v2-ecosystem",
        domain="ecosystem",
        focus="balanced_ecosystem",
        target="ecosystem_collapse",
    )

    topology_path = VALIDATION_DIR / "branched_cycle_graph.json"
    topology = _load(topology_path)
    topology_result, topology_learning = _orient(
        topology,
        path=topology_path,
        analysis_id="network-v2-branched-cycle",
        domain="generic-network",
        focus="start",
        target="target",
    )
    scenario = remove_declared_edge(topology, "loop_2", "target")
    scenario_result, scenario_learning = _orient(
        scenario,
        baseline=topology,
        path=topology_path,
        analysis_id="network-v2-branched-cycle-scenario",
        domain="generic-network",
        focus="start",
        target="target",
    )
    assert scenario_result.comparison is not None

    return {
        "validation_id": "network-orientation-v2",
        "recorded_at": RECORDED_AT.isoformat(),
        "version_boundary": {
            "v1": "frozen and unchanged",
            "v2": "read-only probes plus topologically distinct synthetic fixture",
        },
        "probe_contract": {
            "probe_count": len(topology_learning.synthesis.probe_results),
            "probe_ids": [
                result.probe_id
                for result in topology_learning.synthesis.probe_results
            ],
            "all_read_only": all(
                result.read_only
                for result in topology_learning.synthesis.probe_results
            ),
            "outcome_recorded": topology_learning.outcome_recorded,
            "aggregation": topology_learning.synthesis.provenance.metadata[
                "aggregation"
            ],
        },
        "cross_domain_contract_reuse": {
            "supply_chain_target_reachable": (
                supply_result.structure.target_path is not None
            ),
            "ecosystem_target_reachable": (
                ecosystem_result.structure.target_path is not None
            ),
            "supply_chain_probe_count": len(
                supply_learning.synthesis.probe_results
            ),
            "ecosystem_probe_count": len(
                ecosystem_learning.synthesis.probe_results
            ),
        },
        "distinct_topology_fixture": {
            "nodes": len(topology_result.structure.nodes),
            "edges": len(topology_result.structure.edges),
            "reachable_nodes": list(topology_result.structure.reachable_nodes),
            "blocked_nodes": list(topology_result.structure.blocked_nodes),
            "target_path": list(topology_result.structure.target_path or ()),
            "strong_components": [
                list(component)
                for component in topology_result.structure.strongly_connected_components
            ],
            "weak_components": [
                list(component)
                for component in topology_result.structure.weakly_connected_components
            ],
            "weak_articulation_points": list(
                topology_result.structure.weak_articulation_points
            ),
        },
        "training_scenario": {
            "removed_edge": ["loop_2", "target"],
            "newly_unreachable": list(
                scenario_result.comparison.newly_unreachable
            ),
            "target_path": scenario_result.structure.target_path,
            "probe_agreements": [
                {
                    "subject": agreement.subject,
                    "stance": agreement.stance.value,
                    "probe_ids": list(agreement.probe_ids),
                }
                for agreement in scenario_learning.synthesis.agreements
            ],
            "contradictions": len(scenario_learning.synthesis.contradictions),
        },
        "supported": [
            "five typed read-only perspectives over one network orientation",
            "transparent agreement and contradiction collation without voting",
            "deterministic analysis of a branch, directed cycle, and isolated node",
            "structural sensitivity when one declared edge is removed",
            "software contract reuse across three illustrative domains or fixtures",
        ],
        "not_supported": [
            "observed learning outcome or episodic memory update",
            "calibrated uncertainty or empirical source completeness",
            "real-world cross-domain generalization",
            "causal intervention, stability, risk, or control",
            "autonomous or multi-agent execution",
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
