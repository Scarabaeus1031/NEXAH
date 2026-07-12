"""Tests for evidence-bound OrientationReport generation."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone
import json
import subprocess
import sys

import numpy as np
import pytest

from nexah.backends import BackendResult, V07BackendAdapter
from nexah.orientation import (
    Context,
    OrientationReport,
    OrientationReportGenerator,
    OptionStatus,
    Provenance,
    ReportGenerationError,
    ScopedIdentifier,
    StateRef,
    Transition,
    UncertaintyKind,
    generate_orientation_report,
)


NOW = datetime(2026, 7, 13, 8, 0, tzinfo=timezone.utc)


def backend_result(*, timestamps: bool = False) -> BackendResult:
    signal = np.concatenate(
        [
            np.sin(np.linspace(0.0, 4.0 * np.pi, 80)),
            1.5 + 0.5 * np.cos(np.linspace(0.0, 4.0 * np.pi, 80)),
        ]
    )
    observed_at = (
        tuple(NOW + timedelta(seconds=index) for index in range(len(signal)))
        if timestamps
        else None
    )
    return V07BackendAdapter(n_clusters=3, window=8, random_state=7).adapt(
        signal,
        analysis_id="report-fixture",
        provenance=Provenance(
            source="report-fixture.csv",
            method="synthetic test signal",
            recorded_at=NOW,
            record_id="report-run-001",
        ),
        context=Context(domain="synthetic-test"),
        timestamps=observed_at,
    )


def test_generator_produces_a_scoped_evidence_bound_report() -> None:
    result = backend_result()

    report = generate_orientation_report(result)

    assert report.position == result.state.location
    assert report.evidence_references == (result.state.evidence[0].evidence_id,)
    assert report.uncertainty.kind is UncertaintyKind.UNKNOWN
    assert report.provenance.method == "orientation-report-generator-v1"
    assert report.provenance.metadata["representation_id"] == (
        result.state.representation.representation_id
    )
    assert report.assumptions
    assert report.missing_information


def test_change_language_preserves_embedded_index_alignment() -> None:
    result = backend_result()

    report = OrientationReportGenerator().generate(result)

    assert any("local-cluster label changes" in statement for statement in report.change)
    assert any("source-sample anchor" in statement for statement in report.change)
    assert not report.regimes


def test_reachable_options_are_graph_paths_not_action_claims() -> None:
    result = backend_result()

    report = generate_orientation_report(result)

    assert all(option.status is OptionStatus.REACHABLE for option in report.reachable_options)
    assert all("observed directed path" in option.description for option in report.reachable_options)
    assert all("not established" in option.description for option in report.reachable_options)


def test_disconnected_observed_state_is_reported_as_locally_blocked() -> None:
    result = backend_result()
    assert result.state.location is not None
    scope = result.state.representation.representation_id
    evidence_id = result.state.evidence[0].evidence_id
    disconnected = StateRef(
        identifier=ScopedIdentifier(value="99", scope=scope),
        label="disconnected fixture state",
    )
    extended = replace(
        result,
        transitions=result.transitions
        + (
            Transition(
                source=disconnected,
                target=disconnected,
                probability=1.0,
                evidence_ids=(evidence_id,),
            ),
        ),
    )

    report = generate_orientation_report(extended)

    blocked = {option.option_id: option for option in report.blocked_options}
    option_id = f"{scope}:state-option:99"
    assert blocked[option_id].status is OptionStatus.BLOCKED
    assert "impossibility outside this fitted map is not established" in (
        blocked[option_id].description
    )


def test_missing_information_reflects_absent_contextual_inputs() -> None:
    report = generate_orientation_report(backend_result())

    assert "Calibrated uncertainty for v0.7 state and transition claims" in (
        report.missing_information
    )
    assert "Persistent state identity and cross-run state alignment" in (
        report.missing_information
    )
    assert "Goal criteria for ranking reachable options" in report.missing_information
    assert "Domain constraints for evaluating feasible options" in (
        report.missing_information
    )
    assert "Source observation timestamps" in report.missing_information
    assert "Causal evidence for interventions or real-world transitions" in (
        report.missing_information
    )


def test_supplied_observation_times_are_not_reported_as_missing() -> None:
    report = generate_orientation_report(backend_result(timestamps=True))

    assert "Source observation timestamps" not in report.missing_information
    assert all("sample index" not in assumption for assumption in report.assumptions)


def test_report_round_trips_through_json() -> None:
    original = generate_orientation_report(backend_result())

    payload = json.loads(json.dumps(original.to_dict()))
    restored = OrientationReport.from_dict(payload)

    assert restored == original


def test_report_generation_is_deterministic_for_same_backend_result() -> None:
    result = backend_result()
    generator = OrientationReportGenerator()

    assert generator.generate(result) == generator.generate(result)


def test_missing_location_fails_visibly() -> None:
    result = backend_result()
    invalid = replace(result, state=replace(result.state, location=None))

    with pytest.raises(ReportGenerationError, match="no current location"):
        generate_orientation_report(invalid)


def test_mismatched_transition_scope_fails_visibly() -> None:
    result = backend_result()
    first = result.transitions[0]
    invalid_target = replace(
        first.target,
        identifier=replace(first.target.identifier, scope="another-analysis"),
    )
    invalid = replace(
        result,
        transitions=(replace(first, target=invalid_target),) + result.transitions[1:],
    )

    with pytest.raises(ReportGenerationError, match="target scope"):
        generate_orientation_report(invalid)


def test_unknown_transition_evidence_fails_visibly() -> None:
    result = backend_result()
    first = replace(result.transitions[0], evidence_ids=("unknown-evidence",))
    invalid = replace(result, transitions=(first,) + result.transitions[1:])

    with pytest.raises(ReportGenerationError, match="unknown evidence"):
        generate_orientation_report(invalid)


def test_orient_cli_emits_an_orientation_report(tmp_path) -> None:
    signal = np.sin(np.linspace(0.0, 8.0 * np.pi, 120))
    source = tmp_path / "orientation-signal.csv"
    np.savetxt(source, signal, delimiter=",")

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "nexah.cli",
            "orient",
            str(source),
            "--recorded-at",
            "2026-07-13T08:00:00+00:00",
            "--analysis-id",
            "cli-orientation",
            "--domain",
            "synthetic-test",
            "--clusters",
            "3",
            "--window",
            "8",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    report = json.loads(completed.stdout)
    assert report["schema_version"] == "1.0"
    assert report["position"]["identifier"]["scope"] == (
        "cli-orientation:v07-local-fit"
    )
    assert report["provenance"]["method"] == "orientation-report-generator-v1"
    assert report["uncertainty"]["kind"] == "unknown"
