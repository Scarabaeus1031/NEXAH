"""Contract, policy, CLI, and memory-gateway tests for the outcome firewall."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

from nexah.backends import V07BackendAdapter
from nexah.orientation import (
    ComputationResultRecord,
    Context,
    Episode,
    EpisodeStoreError,
    FirewallCheckStatus,
    FirewallDisposition,
    JsonlEpisodeStore,
    MethodSelectionRelation,
    ObservedOutcomeRecord,
    OrientationEvidenceEnvelope,
    Outcome,
    OutcomeSourceRelation,
    Provenance,
    ScenarioRecord,
    evaluate_outcome_firewall,
    evidence_record_from_dict,
    generate_orientation_report,
    put_episode_if_authorized,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "testkit" / "observed_evidence" / "fixtures"
EVALUATED_AT = datetime(2026, 7, 14, 11, 5, tzinfo=timezone.utc)


def load_fixture(name: str) -> dict[str, object]:
    value = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def envelope() -> OrientationEvidenceEnvelope:
    return OrientationEvidenceEnvelope.from_dict(
        load_fixture("orientation_envelope.json")
    )


def observed_outcome(name: str = "valid_observed_outcome.json") -> ObservedOutcomeRecord:
    record = evidence_record_from_dict(load_fixture(name))
    assert isinstance(record, ObservedOutcomeRecord)
    return record


@pytest.mark.parametrize(
    ("fixture_name", "expected_type"),
    (
        ("scenario_record.json", ScenarioRecord),
        ("computation_result.json", ComputationResultRecord),
        ("valid_observed_outcome.json", ObservedOutcomeRecord),
    ),
)
def test_evidence_records_round_trip_strictly(
    fixture_name: str,
    expected_type: type[object],
) -> None:
    record = evidence_record_from_dict(load_fixture(fixture_name))

    restored = evidence_record_from_dict(
        json.loads(json.dumps(record.to_dict()))
    )

    assert isinstance(restored, expected_type)
    assert restored == record


@pytest.mark.parametrize(
    "fixture_name",
    ("scenario_record.json", "computation_result.json"),
)
def test_generated_or_authored_records_never_authorize_memory(
    fixture_name: str,
) -> None:
    record = evidence_record_from_dict(load_fixture(fixture_name))

    result = evaluate_outcome_firewall(
        envelope(), record, evaluated_at=EVALUATED_AT
    )

    assert result.disposition is FirewallDisposition.ACCEPTED_BENCHMARK_RECORD
    assert not result.episode_update_allowed
    assert result.checks[0].status is FirewallCheckStatus.FAIL
    assert all(
        check.status is FirewallCheckStatus.NOT_APPLICABLE
        for check in result.checks[1:]
    )


def test_valid_later_independent_outcome_authorizes_memory() -> None:
    result = evaluate_outcome_firewall(
        envelope(), observed_outcome(), evaluated_at=EVALUATED_AT
    )

    assert result.disposition is FirewallDisposition.ACCEPTED_OUTCOME_LINKED_CASE
    assert result.episode_update_allowed
    assert all(check.status is FirewallCheckStatus.PASS for check in result.checks)


def test_outcome_before_orientation_is_rejected() -> None:
    result = evaluate_outcome_firewall(
        envelope(),
        observed_outcome("invalid_temporal_outcome.json"),
        evaluated_at=EVALUATED_AT,
    )

    assert result.disposition is FirewallDisposition.REJECTED
    assert not result.episode_update_allowed
    assert result.checks[1].status is FirewallCheckStatus.FAIL


def test_unknown_source_independence_is_indeterminate() -> None:
    result = evaluate_outcome_firewall(
        envelope(),
        observed_outcome("unknown_independence_outcome.json"),
        evaluated_at=EVALUATED_AT,
    )

    assert result.disposition is FirewallDisposition.INDETERMINATE
    assert not result.episode_update_allowed
    assert result.checks[2].status is FirewallCheckStatus.UNKNOWN


@pytest.mark.parametrize(
    "candidate",
    (
        replace(
            observed_outcome(),
            source_relation=OutcomeSourceRelation.TESTED_METHOD_OUTPUT,
            source_relation_basis="The candidate is the tested method output.",
        ),
        replace(observed_outcome(), scope="different-scope"),
        replace(
            observed_outcome(),
            method_selection_relation=MethodSelectionRelation.USED,
            method_selection_basis="The result was inspected before method freeze.",
        ),
    ),
)
def test_failed_policy_conditions_reject_outcome(
    candidate: ObservedOutcomeRecord,
) -> None:
    result = evaluate_outcome_firewall(
        envelope(), candidate, evaluated_at=EVALUATED_AT
    )

    assert result.disposition is FirewallDisposition.REJECTED
    assert not result.episode_update_allowed
    assert FirewallCheckStatus.FAIL in {check.status for check in result.checks}


def test_report_evidence_unavailable_at_orientation_is_rejected() -> None:
    leaky_envelope = replace(
        envelope(),
        report_evidence_ids=("evidence-input-001", "future-outcome-evidence"),
    )

    result = evaluate_outcome_firewall(
        leaky_envelope, observed_outcome(), evaluated_at=EVALUATED_AT
    )

    assert result.disposition is FirewallDisposition.REJECTED
    assert result.checks[4].status is FirewallCheckStatus.FAIL


def make_memory_case() -> tuple[
    Episode,
    OrientationEvidenceEnvelope,
    ObservedOutcomeRecord,
]:
    orientation_time = datetime(2026, 7, 14, 12, 0, tzinfo=timezone.utc)
    provenance = Provenance(
        source="firewall-memory-fixture.csv",
        method="frozen memory gateway fixture",
        recorded_at=orientation_time,
        record_id="firewall-memory-input-001",
    )
    adapted = V07BackendAdapter(n_clusters=3, window=8, random_state=7).adapt(
        np.sin(np.linspace(0.0, 8.0 * np.pi, 160)),
        analysis_id="firewall-memory-scope-001",
        provenance=provenance,
        context=Context(domain="outcome-firewall-test"),
    )
    report = generate_orientation_report(adapted)
    outcome_time = orientation_time + timedelta(minutes=5)
    outcome_provenance = Provenance(
        source="independent memory fixture observer",
        method="post-orientation observation",
        recorded_at=outcome_time,
        record_id="firewall-memory-outcome-provenance-001",
    )
    outcome = Outcome(
        outcome_id="firewall-memory-outcome-001",
        description="The later fixture observation remained bounded.",
        observed_at=outcome_time,
        provenance=outcome_provenance,
        uncertainty=adapted.state.uncertainty,
    )
    episode = Episode(
        episode_id="firewall-memory-episode-001",
        state=adapted.state,
        report=report,
        outcome=outcome,
        created_at=outcome_time,
        provenance=outcome_provenance,
    )
    evidence_ids = tuple(item.evidence_id for item in adapted.state.evidence)
    orientation_envelope = OrientationEvidenceEnvelope(
        orientation_id="firewall-memory-orientation-001",
        scope=adapted.state.representation.representation_id,
        orientation_timestamp=adapted.state.timestamp,
        report_evidence_ids=report.evidence_references,
        available_evidence_ids=evidence_ids,
        provenance=adapted.state.provenance,
    )
    outcome_record = ObservedOutcomeRecord(
        record_id=outcome.outcome_id,
        orientation_id=orientation_envelope.orientation_id,
        scope=orientation_envelope.scope,
        observed_at=outcome.observed_at,
        description=outcome.description,
        source_relation=OutcomeSourceRelation.INDEPENDENT,
        source_relation_basis="Separate declared fixture observer.",
        method_selection_relation=MethodSelectionRelation.NOT_USED,
        method_selection_basis="The adapter configuration was frozen first.",
        uncertainty=outcome.uncertainty,
        provenance=outcome.provenance,
    )
    return episode, orientation_envelope, outcome_record


def test_safe_memory_gateway_requires_matching_positive_authorization(tmp_path: Path) -> None:
    episode, orientation_envelope, outcome_record = make_memory_case()
    authorization = evaluate_outcome_firewall(
        orientation_envelope,
        outcome_record,
        evaluated_at=outcome_record.observed_at + timedelta(seconds=1),
    )
    store = JsonlEpisodeStore(tmp_path / "episodes.jsonl")

    put_episode_if_authorized(store, episode, authorization)

    assert store.get(episode.episode_id) == episode


def test_safe_memory_gateway_rejects_non_outcome_authorization(tmp_path: Path) -> None:
    episode, orientation_envelope, _ = make_memory_case()
    scenario = evidence_record_from_dict(load_fixture("scenario_record.json"))
    authorization = evaluate_outcome_firewall(
        orientation_envelope, scenario, evaluated_at=EVALUATED_AT
    )

    with pytest.raises(EpisodeStoreError, match="rejected"):
        put_episode_if_authorized(
            JsonlEpisodeStore(tmp_path / "episodes.jsonl"),
            episode,
            authorization,
        )


def test_outcome_firewall_cli_emits_machine_readable_decision() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "nexah.cli",
            "validate-outcome-firewall",
            str(FIXTURES / "orientation_envelope.json"),
            str(FIXTURES / "valid_observed_outcome.json"),
            "--evaluated-at",
            EVALUATED_AT.isoformat(),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["disposition"] == "accepted_outcome_linked_case"
    assert payload["episode_update_allowed"] is True
    assert [check["status"] for check in payload["checks"]] == ["pass"] * 6
