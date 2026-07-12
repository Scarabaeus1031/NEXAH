"""Schema and JSON round-trip tests for orientation contracts."""

from __future__ import annotations

import json
from datetime import datetime

import pytest

from nexah.orientation import (
    Context,
    Evidence,
    MapRef,
    Observation,
    OrientationReport,
    OrientationState,
    Provenance,
    ReferenceFrame,
    RepresentationRef,
    Uncertainty,
)


def test_orientation_state_round_trips_through_json(
    observation: Observation,
    representation: RepresentationRef,
    map_ref: MapRef,
    frame: ReferenceFrame,
    context: Context,
    evidence: Evidence,
    uncertainty: Uncertainty,
    timestamp: datetime,
    provenance: Provenance,
) -> None:
    original = OrientationState(
        observations=(observation,),
        representation=representation,
        reference_frame=frame,
        context=context,
        uncertainty=uncertainty,
        timestamp=timestamp,
        provenance=provenance,
        map=map_ref,
        evidence=(evidence,),
    )

    payload = json.loads(json.dumps(original.to_dict()))
    restored = OrientationState.from_dict(payload)

    assert restored == original
    assert isinstance(restored.observations, tuple)
    assert restored.timestamp.tzinfo is not None


def test_orientation_report_round_trips_through_json(
    uncertainty: Uncertainty,
    timestamp: datetime,
    provenance: Provenance,
) -> None:
    original = OrientationReport(
        change=("A local state label changed.",),
        reachable_options=(),
        blocked_options=(),
        missing_information=("External labels",),
        assumptions=("Cluster identity is local.",),
        evidence_references=("ev-001",),
        uncertainty=uncertainty,
        explanation="The statement is limited to the fitted representation.",
        timestamp=timestamp,
        provenance=provenance,
    )

    payload = json.loads(json.dumps(original.to_dict()))
    restored = OrientationReport.from_dict(payload)

    assert restored == original


def test_unknown_schema_fields_fail_visibly(
    observation: Observation,
    representation: RepresentationRef,
    frame: ReferenceFrame,
    context: Context,
    uncertainty: Uncertainty,
    timestamp: datetime,
    provenance: Provenance,
) -> None:
    state = OrientationState(
        observations=(observation,),
        representation=representation,
        reference_frame=frame,
        context=context,
        uncertainty=uncertainty,
        timestamp=timestamp,
        provenance=provenance,
    )
    payload = state.to_dict()
    payload["unsupported_field"] = True

    with pytest.raises(ValueError, match="Unknown OrientationState fields"):
        OrientationState.from_dict(payload)

