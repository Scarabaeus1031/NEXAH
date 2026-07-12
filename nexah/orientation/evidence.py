"""Evidence, provenance, and uncertainty contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from .base import ContractModel, require_aware_datetime, require_text


class EvidenceKind(str, Enum):
    OBSERVATION = "observation"
    COMPUTATION = "computation"
    EXPERIMENT = "experiment"
    EXTERNAL = "external"
    ASSUMPTION = "assumption"


class UncertaintyKind(str, Enum):
    PROBABILITY = "probability"
    CONFIDENCE = "confidence"
    INTERVAL = "interval"
    QUALITATIVE = "qualitative"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True, kw_only=True)
class Provenance(ContractModel):
    source: str
    method: str
    recorded_at: datetime
    record_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        require_text(self.source, "source")
        require_text(self.method, "method")
        require_aware_datetime(self.recorded_at, "recorded_at")
        if self.record_id is not None:
            require_text(self.record_id, "record_id")


@dataclass(frozen=True, slots=True, kw_only=True)
class Uncertainty(ContractModel):
    kind: UncertaintyKind
    value: float | None
    basis: str
    lower: float | None = None
    upper: float | None = None

    def __post_init__(self) -> None:
        require_text(self.basis, "basis")
        if self.kind in (UncertaintyKind.PROBABILITY, UncertaintyKind.CONFIDENCE):
            if self.value is None or not 0.0 <= self.value <= 1.0:
                raise ValueError(f"{self.kind.value} uncertainty requires value in [0, 1]")
        if self.kind is UncertaintyKind.INTERVAL:
            if self.lower is None or self.upper is None or self.lower > self.upper:
                raise ValueError("interval uncertainty requires lower <= upper")
        if self.kind is UncertaintyKind.UNKNOWN and self.value is not None:
            raise ValueError("unknown uncertainty must not provide a numeric value")


@dataclass(frozen=True, slots=True, kw_only=True)
class Evidence(ContractModel):
    evidence_id: str
    claim: str
    kind: EvidenceKind
    provenance: Provenance
    uncertainty: Uncertainty
    payload: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        require_text(self.evidence_id, "evidence_id")
        require_text(self.claim, "claim")

