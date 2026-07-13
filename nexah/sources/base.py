"""Typed contracts for data entering the NEXAH Orientation Layer."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Protocol, TypeVar

import numpy as np
from numpy.typing import NDArray

from nexah.orientation import Context, Provenance
from nexah.orientation.base import (
    ContractModel,
    require_aware_datetime,
    require_text,
)


FloatArray = NDArray[np.float64]
SourceT = TypeVar("SourceT", contravariant=True)


class SourceAdapterError(ValueError):
    """Raised when source data cannot be translated without ambiguity."""


class SourceAxis(str, Enum):
    """Meaning of successive rows; backends must declare compatible axes."""

    ORDERED_SAMPLE = "ordered_sample"
    TIME = "time"
    ENTITY = "entity"
    EVENT = "event"


@dataclass(frozen=True, slots=True, kw_only=True)
class SourceFeature(ContractModel):
    """One ordered source variable and its declared physical semantics."""

    name: str
    unit: str | None = None
    description: str = ""

    def __post_init__(self) -> None:
        require_text(self.name, "name")
        if self.unit is not None:
            require_text(self.unit, "unit")


@dataclass(frozen=True, slots=True, kw_only=True)
class SourceQuality(ContractModel):
    """Observed quality facts at the adapter boundary, not a confidence score."""

    input_rows: int
    output_rows: int
    missing_values: int
    non_finite_values: int
    transformations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        counts = (
            self.input_rows,
            self.output_rows,
            self.missing_values,
            self.non_finite_values,
        )
        if any(count < 0 for count in counts):
            raise ValueError("source quality counts cannot be negative")
        if self.output_rows > self.input_rows:
            raise ValueError("output_rows cannot exceed input_rows")
        for transformation in self.transformations:
            require_text(transformation, "transformation")


@dataclass(frozen=True, slots=True, kw_only=True)
class SourceBatch(ContractModel):
    """Backend-neutral, serializable observations from one source operation."""

    batch_id: str
    values: tuple[tuple[float, ...], ...]
    features: tuple[SourceFeature, ...]
    context: Context
    provenance: Provenance
    quality: SourceQuality
    row_axis: SourceAxis = SourceAxis.ORDERED_SAMPLE
    row_ids: tuple[str, ...] = ()
    timestamps: tuple[datetime, ...] = ()
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        require_text(self.batch_id, "batch_id")
        require_text(self.schema_version, "schema_version")
        if not self.values:
            raise ValueError("SourceBatch requires at least one row")
        if not self.features:
            raise ValueError("SourceBatch requires at least one feature")
        width = len(self.features)
        if any(len(row) != width for row in self.values):
            raise ValueError("every source row must match the feature count")
        numeric = np.asarray(self.values, dtype=np.float64)
        if not np.all(np.isfinite(numeric)):
            raise ValueError("SourceBatch values must be finite")
        if self.quality.output_rows != len(self.values):
            raise ValueError("quality output_rows must match SourceBatch rows")
        if self.row_ids:
            if len(self.row_ids) != len(self.values):
                raise ValueError("row_ids must match SourceBatch rows")
            for row_id in self.row_ids:
                require_text(row_id, "row_id")
            if len(self.row_ids) != len(set(self.row_ids)):
                raise ValueError("row_ids must be unique")
        names = [feature.name for feature in self.features]
        if len(names) != len(set(names)):
            raise ValueError("source feature names must be unique")
        if self.timestamps:
            if self.row_axis is not SourceAxis.TIME:
                raise ValueError("timestamps require the time row axis")
            if len(self.timestamps) != len(self.values):
                raise ValueError("timestamps must match SourceBatch rows")
            for timestamp in self.timestamps:
                require_aware_datetime(timestamp, "timestamp")
            if any(
                current <= previous
                for previous, current in zip(self.timestamps, self.timestamps[1:])
            ):
                raise ValueError("timestamps must be strictly increasing")

    def to_numpy(self) -> FloatArray:
        """Return a detached numeric matrix for a representation backend."""

        return np.asarray(self.values, dtype=np.float64).copy()


class SourceAdapter(Protocol[SourceT]):
    """Structural protocol for translating an independent source."""

    @property
    def adapter_id(self) -> str:
        ...

    def adapt(
        self,
        source: SourceT,
        *,
        batch_id: str,
        provenance: Provenance,
        context: Context,
    ) -> SourceBatch:
        ...
