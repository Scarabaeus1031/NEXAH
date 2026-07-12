"""Validation tests for the minimal orientation vocabulary."""

from __future__ import annotations

from datetime import datetime

import pytest

from nexah.orientation import (
    Option,
    OptionStatus,
    Provenance,
    ScopedIdentifier,
    Similarity,
    StateRef,
    TimePoint,
    Transition,
    Uncertainty,
    UncertaintyKind,
)


def test_identifiers_carry_an_explicit_scope() -> None:
    identifier = ScopedIdentifier(value="2", scope="analysis:run-001")
    assert identifier.value == "2"
    assert identifier.scope == "analysis:run-001"


def test_transition_probability_is_bounded() -> None:
    state = StateRef(identifier=ScopedIdentifier(value="1", scope="local"))

    with pytest.raises(ValueError, match="probability"):
        Transition(source=state, target=state, probability=1.2)


def test_similarity_is_bounded() -> None:
    with pytest.raises(ValueError, match="similarity"):
        Similarity(subject_id="a", reference_id="b", value=-0.1, method="test")


def test_probability_uncertainty_requires_a_unit_interval_value() -> None:
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        Uncertainty(
            kind=UncertaintyKind.PROBABILITY,
            value=None,
            basis="No estimate was provided",
        )


def test_unknown_uncertainty_does_not_fake_a_numeric_value() -> None:
    with pytest.raises(ValueError, match="must not provide"):
        Uncertainty(
            kind=UncertaintyKind.UNKNOWN,
            value=0.5,
            basis="Unknown cannot be quantified",
        )


def test_provenance_rejects_naive_timestamps() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        Provenance(
            source="fixture",
            method="test",
            recorded_at=datetime(2026, 7, 12, 12, 0),
        )


def test_option_status_is_explicit() -> None:
    option = Option(
        option_id="stay",
        description="Remain in the current observed state",
        status=OptionStatus.UNKNOWN,
    )
    assert option.status is OptionStatus.UNKNOWN


def test_time_point_requires_an_explicit_frame(timestamp) -> None:
    point = TimePoint(value=timestamp, frame="event_time")
    assert point.frame == "event_time"
