"""Shared contracts for computational backend adapters."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from nexah.orientation import OrientationState, Regime, Transition
from nexah.orientation.base import ContractModel


class BackendAdapterError(ValueError):
    """Raised when backend input cannot be translated without ambiguity."""


@dataclass(frozen=True, slots=True, kw_only=True)
class EmbeddingAlignment(ContractModel):
    """Mapping between v0.7 embedded positions and source sample indices."""

    input_samples: int
    embedded_samples: int
    window: int
    anchor: str = "window_end"
    final_source_sample_used: int = 0

    def raw_window(self, embedded_index: int) -> tuple[int, int]:
        if not 0 <= embedded_index < self.embedded_samples:
            raise IndexError("embedded index outside represented range")
        return embedded_index, embedded_index + self.window - 1

    def raw_anchor(self, embedded_index: int) -> int:
        return self.raw_window(embedded_index)[1]


@dataclass(frozen=True, slots=True, kw_only=True)
class BackendResult:
    """Typed orientation state plus backend-specific structural artifacts."""

    state: OrientationState
    transitions: tuple[Transition, ...]
    regimes: tuple[Regime, ...]
    alignment: EmbeddingAlignment
    raw_output: dict[str, Any]


class BackendAdapter(Protocol):
    """Structural protocol implemented by current backend adapters."""

    @property
    def backend_id(self) -> str:
        ...

