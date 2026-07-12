"""Tests for the OrientationState input contract."""

from __future__ import annotations

from datetime import datetime

import pytest

from nexah.orientation import (
    Context,
    Evidence,
    MapRef,
    MapScope,
    Observation,
    Provenance,
    ReferenceFrame,
    RepresentationRef,
    Uncertainty,
)
from nexah.orientation.state import OrientationState


def test_state_requires_observations(
    representation: RepresentationRef,
    frame: ReferenceFrame,
    context: Context,
    uncertainty: Uncertainty,
    timestamp: datetime,
    provenance: Provenance,
) -> None:
    with pytest.raises(ValueError, match="at least one observation"):
        OrientationState(
            observations=(),
            representation=representation,
            reference_frame=frame,
            context=context,
            uncertainty=uncertainty,
            timestamp=timestamp,
            provenance=provenance,
        )


def test_state_requires_unique_observation_ids(
    observation: Observation,
    representation: RepresentationRef,
    frame: ReferenceFrame,
    context: Context,
    uncertainty: Uncertainty,
    timestamp: datetime,
    provenance: Provenance,
) -> None:
    with pytest.raises(ValueError, match="observation IDs"):
        OrientationState(
            observations=(observation, observation),
            representation=representation,
            reference_frame=frame,
            context=context,
            uncertainty=uncertainty,
            timestamp=timestamp,
            provenance=provenance,
        )


def test_map_must_match_representation_scope_and_identity(
    observation: Observation,
    representation: RepresentationRef,
    frame: ReferenceFrame,
    context: Context,
    uncertainty: Uncertainty,
    timestamp: datetime,
    provenance: Provenance,
) -> None:
    incompatible_map = MapRef(
        map_id="map-other",
        scope=MapScope.PERSISTENT,
        representation_id="rep-other",
        description="An unrelated map",
    )

    with pytest.raises(ValueError, match="IDs must match"):
        OrientationState(
            observations=(observation,),
            representation=representation,
            reference_frame=frame,
            context=context,
            uncertainty=uncertainty,
            timestamp=timestamp,
            provenance=provenance,
            map=incompatible_map,
        )


def test_valid_state_preserves_evidence_and_scope(
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
    state = OrientationState(
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

    assert state.schema_version == "1.0"
    assert state.map is not None
    assert state.map.scope is MapScope.LOCAL_FIT
    assert state.evidence[0].evidence_id == "ev-001"

