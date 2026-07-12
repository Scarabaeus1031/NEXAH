"""Tests for evidence-linked orientation output."""

from __future__ import annotations

from datetime import datetime

import pytest

from nexah.orientation import (
    Option,
    OptionStatus,
    OrientationReport,
    Provenance,
    Uncertainty,
)


def report_kwargs(
    timestamp: datetime,
    provenance: Provenance,
    uncertainty: Uncertainty,
) -> dict:
    return {
        "change": ("No externally validated change claim is available.",),
        "reachable_options": (),
        "blocked_options": (),
        "missing_information": ("External regime labels",),
        "assumptions": ("The representation is local to this analysis.",),
        "evidence_references": (),
        "uncertainty": uncertainty,
        "explanation": "The current map is descriptive and locally scoped.",
        "timestamp": timestamp,
        "provenance": provenance,
    }


def test_report_requires_evidence_or_explicit_assumptions(
    timestamp: datetime,
    provenance: Provenance,
    uncertainty: Uncertainty,
) -> None:
    values = report_kwargs(timestamp, provenance, uncertainty)
    values["assumptions"] = ()

    with pytest.raises(ValueError, match="evidence references or explicit assumptions"):
        OrientationReport(**values)


def test_option_cannot_be_reachable_and_blocked(
    timestamp: datetime,
    provenance: Provenance,
    uncertainty: Uncertainty,
) -> None:
    option = Option(
        option_id="target-1",
        description="Navigate to local state 1",
        status=OptionStatus.UNKNOWN,
    )
    values = report_kwargs(timestamp, provenance, uncertainty)
    values["reachable_options"] = (option,)
    values["blocked_options"] = (option,)

    with pytest.raises(ValueError, match="both reachable and blocked"):
        OrientationReport(**values)


def test_missing_information_is_a_valid_report_result(
    timestamp: datetime,
    provenance: Provenance,
    uncertainty: Uncertainty,
) -> None:
    report = OrientationReport(**report_kwargs(timestamp, provenance, uncertainty))

    assert report.missing_information == ("External regime labels",)
    assert report.evidence_references == ()
    assert report.assumptions

