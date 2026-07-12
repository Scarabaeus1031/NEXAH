"""Minimal operational vocabulary for the NEXAH Orientation Layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from .base import ContractModel, require_aware_datetime, require_text
from .evidence import Provenance, Uncertainty


class MapScope(str, Enum):
    LOCAL_FIT = "local_fit"
    SESSION = "session"
    PERSISTENT = "persistent"


class OptionStatus(str, Enum):
    REACHABLE = "reachable"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True, kw_only=True)
class ScopedIdentifier(ContractModel):
    value: str
    scope: str

    def __post_init__(self) -> None:
        require_text(self.value, "value")
        require_text(self.scope, "scope")


@dataclass(frozen=True, slots=True, kw_only=True)
class Observer(ContractModel):
    observer_id: str
    kind: str
    description: str = ""

    def __post_init__(self) -> None:
        require_text(self.observer_id, "observer_id")
        require_text(self.kind, "kind")


@dataclass(frozen=True, slots=True, kw_only=True)
class ReferenceFrame(ContractModel):
    frame_id: str
    description: str
    scale: str | None = None

    def __post_init__(self) -> None:
        require_text(self.frame_id, "frame_id")
        require_text(self.description, "description")


@dataclass(frozen=True, slots=True, kw_only=True)
class Context(ContractModel):
    domain: str
    values: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        require_text(self.domain, "domain")


@dataclass(frozen=True, slots=True, kw_only=True)
class Observation(ContractModel):
    observation_id: str
    value: Any
    observed_at: datetime
    provenance: Provenance
    variable: str | None = None
    unit: str | None = None

    def __post_init__(self) -> None:
        require_text(self.observation_id, "observation_id")
        require_aware_datetime(self.observed_at, "observed_at")
        if self.variable is not None:
            require_text(self.variable, "variable")


@dataclass(frozen=True, slots=True, kw_only=True)
class TimePoint(ContractModel):
    value: datetime
    frame: str

    def __post_init__(self) -> None:
        require_aware_datetime(self.value, "value")
        require_text(self.frame, "frame")


@dataclass(frozen=True, slots=True, kw_only=True)
class StateRef(ContractModel):
    identifier: ScopedIdentifier
    label: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class Transition(ContractModel):
    source: StateRef
    target: StateRef
    probability: float | None = None
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.probability is not None and not 0.0 <= self.probability <= 1.0:
            raise ValueError("probability must be in [0, 1]")


@dataclass(frozen=True, slots=True, kw_only=True)
class Regime(ContractModel):
    regime_id: ScopedIdentifier
    label: str
    state_ids: tuple[ScopedIdentifier, ...] = ()
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_text(self.label, "label")


@dataclass(frozen=True, slots=True, kw_only=True)
class RepresentationRef(ContractModel):
    backend: str
    method: str
    scope: MapScope
    representation_id: str
    parameters: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        require_text(self.backend, "backend")
        require_text(self.method, "method")
        require_text(self.representation_id, "representation_id")


@dataclass(frozen=True, slots=True, kw_only=True)
class MapRef(ContractModel):
    map_id: str
    scope: MapScope
    representation_id: str
    description: str

    def __post_init__(self) -> None:
        require_text(self.map_id, "map_id")
        require_text(self.representation_id, "representation_id")
        require_text(self.description, "description")


@dataclass(frozen=True, slots=True, kw_only=True)
class Goal(ContractModel):
    goal_id: str
    description: str
    priority: int = 0

    def __post_init__(self) -> None:
        require_text(self.goal_id, "goal_id")
        require_text(self.description, "description")


@dataclass(frozen=True, slots=True, kw_only=True)
class Constraint(ContractModel):
    constraint_id: str
    description: str
    hard: bool = True

    def __post_init__(self) -> None:
        require_text(self.constraint_id, "constraint_id")
        require_text(self.description, "description")


@dataclass(frozen=True, slots=True, kw_only=True)
class Option(ContractModel):
    option_id: str
    description: str
    status: OptionStatus
    evidence_ids: tuple[str, ...] = ()
    constraint_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_text(self.option_id, "option_id")
        require_text(self.description, "description")


@dataclass(frozen=True, slots=True, kw_only=True)
class Similarity(ContractModel):
    subject_id: str
    reference_id: str
    value: float
    method: str

    def __post_init__(self) -> None:
        require_text(self.subject_id, "subject_id")
        require_text(self.reference_id, "reference_id")
        require_text(self.method, "method")
        if not 0.0 <= self.value <= 1.0:
            raise ValueError("similarity value must be in [0, 1]")


@dataclass(frozen=True, slots=True, kw_only=True)
class OperatorRef(ContractModel):
    name: str
    version: str
    parameters: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        require_text(self.name, "name")
        require_text(self.version, "version")


@dataclass(frozen=True, slots=True, kw_only=True)
class EpisodeRef(ContractModel):
    episode_id: str
    summary: str
    similarity: Similarity | None = None

    def __post_init__(self) -> None:
        require_text(self.episode_id, "episode_id")
        require_text(self.summary, "summary")


@dataclass(frozen=True, slots=True, kw_only=True)
class Outcome(ContractModel):
    outcome_id: str
    description: str
    observed_at: datetime
    provenance: Provenance
    uncertainty: Uncertainty

    def __post_init__(self) -> None:
        require_text(self.outcome_id, "outcome_id")
        require_text(self.description, "description")
        require_aware_datetime(self.observed_at, "observed_at")
