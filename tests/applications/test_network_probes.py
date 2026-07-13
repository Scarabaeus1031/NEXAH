"""Multi-perspective learning probes for Network Orientation V2."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

from nexah.applications import (
    NetworkLearningContext,
    NetworkOrientationApplication,
    remove_declared_edge,
    render_network_learning_text,
    run_network_probe_suite,
)
from nexah.orientation import Context, FindingStance, Provenance


ROOT = Path(__file__).parents[2]
NOW = datetime(2026, 7, 13, 22, 45, tzinfo=timezone.utc)


def _load(filename: str) -> dict[str, object]:
    return json.loads((ROOT / "APPLICATIONS" / "datasets" / filename).read_text())


def _result(*, comparison: bool = True):
    source = _load("supply_chain.json")
    current = (
        remove_declared_edge(source, "production_slowdown", "distribution_backlog")
        if comparison
        else source
    )
    return NetworkOrientationApplication().orient(
        current,
        baseline_source=source if comparison else None,
        analysis_id="probe-test",
        provenance=Provenance(
            source="APPLICATIONS/datasets/supply_chain.json",
            method="illustrative test fixture",
            recorded_at=NOW,
        ),
        context=Context(domain="supply-chain", values={"status": "illustrative"}),
        focus="normal_operation",
        target="system_disruption",
    )


def test_five_probes_preserve_findings_limits_and_identity() -> None:
    learning = run_network_probe_suite(_result())

    assert len(learning.synthesis.probe_results) == 5
    assert all(result.read_only for result in learning.synthesis.probe_results)
    assert learning.outcome_recorded is False
    assert len(learning.synthesis.limitation_finding_ids) == 5
    assert learning.synthesis.agreements[0].subject == "target-reachability"
    assert learning.synthesis.agreements[0].stance is FindingStance.CHALLENGED
    assert learning.synthesis.contradictions == ()
    assert "majority-vote" in learning.synthesis.provenance.metadata["aggregation"]


def test_single_snapshot_keeps_perturbation_unknown() -> None:
    learning = run_network_probe_suite(_result(comparison=False))
    perturbation = next(
        result
        for result in learning.synthesis.probe_results
        if result.probe_id == "network-perturbation-probe-v1"
    )

    assert perturbation.findings[0].stance is FindingStance.UNKNOWN
    assert "baseline" in perturbation.missing_information[0].lower()


def test_learning_context_round_trips_and_names_memory_boundary() -> None:
    learning = run_network_probe_suite(_result())
    restored = NetworkLearningContext.from_dict(
        json.loads(json.dumps(learning.to_dict()))
    )

    assert restored == learning
    text = render_network_learning_text(learning)
    assert "No observed Outcome" in text
    assert "No probe has command or execution authority" in text


def test_cli_can_emit_v2_probe_wrapper() -> None:
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
            "--probes",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["application_id"] == "network-orientation-v2-probes"
    assert len(payload["synthesis"]["probe_results"]) == 5
    assert payload["outcome_recorded"] is False
