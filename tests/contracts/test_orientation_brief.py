"""Contract invariants for the human-facing Orientation Brief."""

from __future__ import annotations

from dataclasses import replace

import pytest

from nexah.applications import (
    NetworkOrientationApplication,
    build_network_orientation_brief,
    run_network_probe_suite,
)
from nexah.orientation import (
    BriefEvidenceClass,
    BriefEvidenceStatement,
    BriefOutcomeStatus,
    Context,
    Provenance,
)

from datetime import datetime, timezone


NOW = datetime(2026, 7, 14, 12, 0, tzinfo=timezone.utc)


def _brief():
    source = {
        "nodes": ["a", "b"],
        "edges": [{"from": "a", "to": "b"}],
    }
    result = NetworkOrientationApplication().orient(
        source,
        analysis_id="brief-contract",
        provenance=Provenance(
            source="inline-test-fixture",
            method="declared fixture",
            recorded_at=NOW,
        ),
        context=Context(domain="contract-test"),
        focus="a",
        target="b",
    )
    return build_network_orientation_brief(run_network_probe_suite(result))


def test_episode_reference_requires_observed_outcome() -> None:
    with pytest.raises(ValueError, match="episode reference requires"):
        replace(_brief(), episode_id="episode-1")


def test_observed_status_requires_observed_outcome_evidence() -> None:
    with pytest.raises(ValueError, match="requires observed-outcome evidence"):
        replace(_brief(), outcome_status=BriefOutcomeStatus.OBSERVED)


def test_observed_outcome_evidence_conflicts_with_non_observed_status() -> None:
    brief = _brief()
    evidence = brief.evidence + (
        BriefEvidenceStatement(
            statement_id="observed-outcome",
            evidence_class=BriefEvidenceClass.OBSERVED_OUTCOME,
            statement="An independently observed outcome.",
            references=("external-outcome-record",),
        ),
    )
    with pytest.raises(ValueError, match="conflicts with non-observed status"):
        replace(brief, evidence=evidence)
