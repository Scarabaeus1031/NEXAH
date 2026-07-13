"""Contracts for transparent read-only probe synthesis."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from nexah.orientation import (
    FindingStance,
    ProbeFinding,
    ProbeResult,
    Provenance,
    Uncertainty,
    UncertaintyKind,
    synthesize_probe_results,
)


NOW = datetime(2026, 7, 13, 22, 45, tzinfo=timezone.utc)
PROVENANCE = Provenance(source="fixture", method="test", recorded_at=NOW)
UNCERTAINTY = Uncertainty(
    kind=UncertaintyKind.QUALITATIVE,
    value=None,
    basis="test fixture uncertainty",
)


def _result(probe_id: str, stance: FindingStance) -> ProbeResult:
    return ProbeResult(
        probe_id=probe_id,
        perspective=probe_id,
        representation_id="graph-1",
        findings=(
            ProbeFinding(
                finding_id=f"{probe_id}:finding",
                subject="target-reachability",
                statement=f"{probe_id} statement",
                stance=stance,
                evidence_ids=("evidence-1",),
            ),
        ),
        missing_information=(),
        assumptions=(),
        uncertainty=UNCERTAINTY,
        provenance=PROVENANCE,
    )


def test_synthesis_preserves_visible_agreement_and_contradiction() -> None:
    synthesis = synthesize_probe_results(
        (
            _result("support-a", FindingStance.SUPPORTED),
            _result("support-b", FindingStance.SUPPORTED),
            _result("challenge", FindingStance.CHALLENGED),
        ),
        provenance=PROVENANCE,
    )

    assert synthesis.agreements[0].probe_ids == ("support-a", "support-b")
    assert synthesis.contradictions[0].supporting_probe_ids == (
        "support-a",
        "support-b",
    )
    assert synthesis.contradictions[0].challenging_probe_ids == ("challenge",)
    assert synthesis.evidence_references == ("evidence-1",)


def test_probe_contract_rejects_execution_authority() -> None:
    with pytest.raises(ValueError, match="read-only"):
        ProbeResult(
            probe_id="executor",
            perspective="invalid executor",
            representation_id="graph-1",
            findings=(),
            missing_information=(),
            assumptions=(),
            uncertainty=UNCERTAINTY,
            provenance=PROVENANCE,
            read_only=False,
        )
