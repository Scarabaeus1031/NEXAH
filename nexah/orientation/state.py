"""Input and internal-state contract for orientation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .base import ContractModel, require_aware_datetime, require_text
from .evidence import Evidence, Provenance, Uncertainty
from .primitives import (
    Constraint,
    Context,
    EpisodeRef,
    Goal,
    MapRef,
    Observation,
    Option,
    ReferenceFrame,
    RepresentationRef,
    StateRef,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class OrientationState(ContractModel):
    observations: tuple[Observation, ...]
    representation: RepresentationRef
    reference_frame: ReferenceFrame
    context: Context
    uncertainty: Uncertainty
    timestamp: datetime
    provenance: Provenance
    location: StateRef | None = None
    goals: tuple[Goal, ...] = ()
    constraints: tuple[Constraint, ...] = ()
    map: MapRef | None = None
    episodes: tuple[EpisodeRef, ...] = ()
    options: tuple[Option, ...] = ()
    evidence: tuple[Evidence, ...] = ()
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        require_text(self.schema_version, "schema_version")
        require_aware_datetime(self.timestamp, "timestamp")
        if not self.observations:
            raise ValueError("OrientationState requires at least one observation")
        _require_unique(
            [observation.observation_id for observation in self.observations],
            "observation IDs",
        )
        _require_unique(
            [item.evidence_id for item in self.evidence],
            "evidence IDs",
        )
        if self.map is not None:
            if self.map.representation_id != self.representation.representation_id:
                raise ValueError("map and representation IDs must match")
            if self.map.scope != self.representation.scope:
                raise ValueError("map and representation scopes must match")


def _require_unique(values: list[str], label: str) -> None:
    if len(values) != len(set(values)):
        raise ValueError(f"{label} must be unique")

