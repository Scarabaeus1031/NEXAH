"""Shared fixtures for Orientation Layer contract tests."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from nexah.orientation import (
    Context,
    Evidence,
    EvidenceKind,
    MapRef,
    MapScope,
    Observation,
    Provenance,
    ReferenceFrame,
    RepresentationRef,
    Uncertainty,
    UncertaintyKind,
)


@pytest.fixture
def timestamp() -> datetime:
    return datetime(2026, 7, 12, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def provenance(timestamp: datetime) -> Provenance:
    return Provenance(
        source="fixture.csv",
        method="test fixture",
        recorded_at=timestamp,
        record_id="run-001",
    )


@pytest.fixture
def uncertainty() -> Uncertainty:
    return Uncertainty(
        kind=UncertaintyKind.CONFIDENCE,
        value=0.8,
        basis="fixture confidence for contract validation",
    )


@pytest.fixture
def observation(timestamp: datetime, provenance: Provenance) -> Observation:
    return Observation(
        observation_id="obs-001",
        value=1.25,
        variable="signal",
        observed_at=timestamp,
        provenance=provenance,
    )


@pytest.fixture
def representation() -> RepresentationRef:
    return RepresentationRef(
        backend="nexah-v07",
        method="window-kmeans-transition",
        scope=MapScope.LOCAL_FIT,
        representation_id="rep-001",
        parameters={"window": 8, "n_clusters": 3},
    )


@pytest.fixture
def map_ref() -> MapRef:
    return MapRef(
        map_id="map-001",
        scope=MapScope.LOCAL_FIT,
        representation_id="rep-001",
        description="Locally fitted transition map",
    )


@pytest.fixture
def frame() -> ReferenceFrame:
    return ReferenceFrame(
        frame_id="embedded-sample-index",
        description="Indices in the v0.7 sliding-window representation",
        scale="window",
    )


@pytest.fixture
def context() -> Context:
    return Context(domain="synthetic-test", values={"purpose": "contract test"})


@pytest.fixture
def evidence(provenance: Provenance, uncertainty: Uncertainty) -> Evidence:
    return Evidence(
        evidence_id="ev-001",
        claim="The fixture contains one recorded observation.",
        kind=EvidenceKind.OBSERVATION,
        provenance=provenance,
        uncertainty=uncertainty,
    )

