"""Reference source adapter for in-memory numeric trajectories."""

from __future__ import annotations

from datetime import datetime
from typing import Sequence

import numpy as np
from numpy.typing import ArrayLike

from nexah.orientation import Context, Provenance
from nexah.orientation.base import require_aware_datetime, require_text

from .base import (
    SourceAdapterError,
    SourceAxis,
    SourceBatch,
    SourceFeature,
    SourceQuality,
)


class ArraySourceAdapter:
    """Translate a finite one- or two-dimensional numeric array without analysis."""

    @property
    def adapter_id(self) -> str:
        return "numpy-array-source-v1"

    def adapt(
        self,
        source: ArrayLike,
        *,
        batch_id: str,
        provenance: Provenance,
        context: Context,
        timestamps: Sequence[datetime] | None = None,
        feature_names: Sequence[str] | None = None,
        units: Sequence[str | None] | None = None,
        row_axis: SourceAxis = SourceAxis.ORDERED_SAMPLE,
    ) -> SourceBatch:
        require_text(batch_id, "batch_id")
        try:
            values = np.asarray(source, dtype=np.float64)
        except (TypeError, ValueError) as error:
            raise SourceAdapterError("source must contain numeric values") from error
        if values.ndim == 1:
            values = values.reshape(-1, 1)
        if values.ndim != 2:
            raise SourceAdapterError("source must be one- or two-dimensional")
        if values.shape[0] == 0 or values.shape[1] == 0:
            raise SourceAdapterError("source must contain rows and features")
        non_finite = int(values.size - np.count_nonzero(np.isfinite(values)))
        if non_finite:
            raise SourceAdapterError(
                f"source contains {non_finite} missing or non-finite values"
            )

        width = int(values.shape[1])
        names = tuple(feature_names or (f"feature_{index}" for index in range(width)))
        if len(names) != width:
            raise SourceAdapterError("feature_names must match source width")
        for name in names:
            require_text(name, "feature name")
        if len(names) != len(set(names)):
            raise SourceAdapterError("feature_names must be unique")

        declared_units = tuple(units or (None for _ in range(width)))
        if len(declared_units) != width:
            raise SourceAdapterError("units must match source width")
        for unit in declared_units:
            if unit is not None:
                require_text(unit, "unit")

        observation_times = tuple(timestamps or ())
        if observation_times:
            if row_axis is not SourceAxis.TIME:
                raise SourceAdapterError("timestamps require the time row axis")
            if len(observation_times) != values.shape[0]:
                raise SourceAdapterError("timestamps must match source rows")
            for timestamp in observation_times:
                require_aware_datetime(timestamp, "timestamp")
            if any(
                current <= previous
                for previous, current in zip(
                    observation_times, observation_times[1:]
                )
            ):
                raise SourceAdapterError("timestamps must be strictly increasing")

        features = tuple(
            SourceFeature(name=name, unit=unit)
            for name, unit in zip(names, declared_units)
        )
        rows = tuple(tuple(float(value) for value in row) for row in values)
        return SourceBatch(
            batch_id=batch_id,
            values=rows,
            features=features,
            timestamps=observation_times,
            context=context,
            provenance=provenance,
            quality=SourceQuality(
                input_rows=int(values.shape[0]),
                output_rows=int(values.shape[0]),
                missing_values=0,
                non_finite_values=0,
                transformations=("one-dimensional input expanded to one feature",)
                if np.asarray(source).ndim == 1
                else (),
            ),
            row_axis=row_axis,
        )
