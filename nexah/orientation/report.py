"""Evidence-linked output contract for orientation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .base import ContractModel, require_aware_datetime, require_text
from .evidence import Provenance, Uncertainty
from .primitives import EpisodeRef, Option, Regime, StateRef


@dataclass(frozen=True, slots=True, kw_only=True)
class OrientationReport(ContractModel):
    change: tuple[str, ...]
    reachable_options: tuple[Option, ...]
    blocked_options: tuple[Option, ...]
    missing_information: tuple[str, ...]
    assumptions: tuple[str, ...]
    evidence_references: tuple[str, ...]
    uncertainty: Uncertainty
    explanation: str
    timestamp: datetime
    provenance: Provenance
    position: StateRef | None = None
    regimes: tuple[Regime, ...] = ()
    similar_episodes: tuple[EpisodeRef, ...] = ()
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        require_text(self.schema_version, "schema_version")
        require_text(self.explanation, "explanation")
        require_aware_datetime(self.timestamp, "timestamp")
        if not self.evidence_references and not self.assumptions:
            raise ValueError(
                "OrientationReport requires evidence references or explicit assumptions"
            )

        reachable_ids = {option.option_id for option in self.reachable_options}
        blocked_ids = {option.option_id for option in self.blocked_options}
        overlap = reachable_ids & blocked_ids
        if overlap:
            names = ", ".join(sorted(overlap))
            raise ValueError(f"options cannot be both reachable and blocked: {names}")

