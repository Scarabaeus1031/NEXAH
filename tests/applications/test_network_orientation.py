"""Phase IV tests for the Network Orientation V1 application."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

from nexah.applications import (
    NetworkOrientationApplication,
    NetworkOrientationResult,
    remove_declared_edge,
    render_network_orientation_text,
)
from nexah.orientation import Context, Provenance
from nexah.sources import GraphSchema


ROOT = Path(__file__).parents[2]
NOW = datetime(2026, 7, 13, 22, 45, tzinfo=timezone.utc)


def load_graph(filename: str) -> dict[str, object]:
    return json.loads((ROOT / "APPLICATIONS" / "datasets" / filename).read_text())


def provenance(filename: str, method: str = "illustrative repository fixture") -> Provenance:
    return Provenance(
        source=f"APPLICATIONS/datasets/{filename}",
        method=method,
        recorded_at=NOW,
    )


def test_supply_chain_orientation_reports_declared_structure_only() -> None:
    result = NetworkOrientationApplication().orient(
        load_graph("supply_chain.json"),
        analysis_id="supply-chain-v1",
        provenance=provenance("supply_chain.json"),
        context=Context(domain="supply-chain", values={"status": "illustrative"}),
        focus="normal_operation",
        target="system_disruption",
    )

    assert result.structure.target_path == (
        "normal_operation",
        "supplier_delay",
        "production_slowdown",
        "distribution_backlog",
        "system_disruption",
    )
    assert result.structure.blocked_nodes == ()
    assert result.structure.weak_articulation_points == (
        "distribution_backlog",
        "production_slowdown",
        "supplier_delay",
    )
    assert len(result.structure.focus_critical_edges) == 4
    serialized = json.dumps(result.to_dict()).lower()
    assert "increase_inventory" not in serialized
    assert "supplier_shutdown" not in serialized
    assert result.orientation.regimes == ()
    assert "not a recommendation" in serialized


def test_edge_removal_is_reported_as_structural_sensitivity() -> None:
    baseline = load_graph("supply_chain.json")
    scenario = remove_declared_edge(
        baseline,
        "production_slowdown",
        "distribution_backlog",
    )
    result = NetworkOrientationApplication().orient(
        scenario,
        baseline_source=baseline,
        analysis_id="supply-chain-edge-removal",
        provenance=provenance("supply_chain.json", "declared edge-removal scenario"),
        baseline_provenance=provenance("supply_chain.json"),
        context=Context(domain="supply-chain", values={"status": "illustrative"}),
        focus="normal_operation",
        target="system_disruption",
    )

    assert result.comparison is not None
    assert result.comparison.newly_unreachable == (
        "distribution_backlog",
        "system_disruption",
    )
    assert tuple(
        (edge.source, edge.target) for edge in result.comparison.removed_edges
    ) == (("production_slowdown", "distribution_backlog"),)
    assert result.structure.target_path is None
    assert "learning context" in " ".join(result.orientation.assumptions)
    assert "control or causal claim" in render_network_orientation_text(result)
    assert NetworkOrientationResult.from_dict(
        json.loads(json.dumps(result.to_dict()))
    ) == result


def test_weight_change_is_recorded_without_stability_interpretation() -> None:
    baseline = {
        "nodes": ["a", "b"],
        "edges": [{"from": "a", "to": "b", "flow": 0.5}],
    }
    current = {
        "nodes": ["a", "b"],
        "edges": [{"from": "a", "to": "b", "flow": 0.8}],
    }
    result = NetworkOrientationApplication(GraphSchema(weight_key="flow")).orient(
        current,
        baseline_source=baseline,
        analysis_id="weighted-comparison",
        provenance=provenance("weighted.json", "declared weighted snapshot"),
        context=Context(domain="weighted-network"),
        focus="a",
        target="b",
    )

    assert result.comparison is not None
    assert result.comparison.changed_edge_weights[0][0].weight == 0.5
    assert result.comparison.changed_edge_weights[0][1].weight == 0.8
    assert result.comparison.newly_reachable == ()
    assert result.comparison.newly_unreachable == ()
    assert "stability" not in " ".join(result.orientation.change).lower()


def test_ecosystem_is_a_held_out_domain_blind_transfer() -> None:
    result = NetworkOrientationApplication().orient(
        load_graph("ecosystem_food_web.json"),
        analysis_id="ecosystem-held-out-v1",
        provenance=provenance("ecosystem_food_web.json"),
        context=Context(domain="ecosystem", values={"status": "held-out-illustrative"}),
        focus="balanced_ecosystem",
        target="ecosystem_collapse",
    )

    assert result.structure.target_path == (
        "balanced_ecosystem",
        "herbivore_increase",
        "plant_depletion",
        "predator_decline",
        "ecosystem_collapse",
    )
    assert len(result.structure.strongly_connected_components) == 1
    assert len(result.structure.focus_critical_edges) == 4
    assert result.orientation.provenance.method == (
        "network-orientation-report-generator-v1"
    )


def test_network_orientation_result_round_trips() -> None:
    result = NetworkOrientationApplication().orient(
        load_graph("supply_chain.json"),
        analysis_id="round-trip",
        provenance=provenance("supply_chain.json"),
        context=Context(domain="supply-chain"),
        focus="normal_operation",
    )

    restored = NetworkOrientationResult.from_dict(
        json.loads(json.dumps(result.to_dict()))
    )

    assert restored == result


def test_orient_network_cli_emits_machine_readable_json() -> None:
    source = ROOT / "APPLICATIONS" / "datasets" / "supply_chain.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "nexah.cli",
            "orient-network",
            str(source),
            "--focus",
            "normal_operation",
            "--target",
            "system_disruption",
            "--recorded-at",
            "2026-07-13T22:45:00+00:00",
            "--analysis-id",
            "cli-supply-chain",
            "--domain",
            "supply-chain",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["application_id"] == "network-orientation-v1"
    assert payload["structure"]["target_path"][-1] == "system_disruption"
    assert payload["comparison"] is None


def test_orient_network_cli_renders_training_scenario_text() -> None:
    source = ROOT / "APPLICATIONS" / "datasets" / "supply_chain.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "nexah.cli",
            "orient-network",
            str(source),
            "--focus",
            "normal_operation",
            "--target",
            "system_disruption",
            "--recorded-at",
            "2026-07-13T22:45:00+00:00",
            "--remove-edge",
            "production_slowdown",
            "distribution_backlog",
            "--format",
            "text",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "NEXAH Network Orientation V1" in completed.stdout
    assert "Newly unreachable: distribution_backlog, system_disruption" in (
        completed.stdout
    )
    assert "no control or causal claim" in completed.stdout
