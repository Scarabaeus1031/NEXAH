"""Schema-driven source adapter for tabular observations."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd  # type: ignore[import-untyped]

from nexah.orientation import Context, Provenance
from nexah.orientation.base import ContractModel, require_text

from .array import ArraySourceAdapter
from .base import SourceAdapterError, SourceAxis, SourceBatch


@dataclass(frozen=True, slots=True, kw_only=True)
class TableSchema(ContractModel):
    """Explicit selection and semantics for a tabular source."""

    feature_columns: tuple[str, ...]
    timestamp_column: str | None = None
    units: dict[str, str | None] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.feature_columns:
            raise ValueError("TableSchema requires feature columns")
        for column in self.feature_columns:
            require_text(column, "feature column")
        if len(self.feature_columns) != len(set(self.feature_columns)):
            raise ValueError("feature columns must be unique")
        if self.timestamp_column is not None:
            require_text(self.timestamp_column, "timestamp_column")
            if self.timestamp_column in self.feature_columns:
                raise ValueError("timestamp column cannot also be a feature")
        unknown_units = set(self.units) - set(self.feature_columns)
        if unknown_units:
            raise ValueError("units contain columns outside feature_columns")
        for unit in self.units.values():
            if unit is not None:
                require_text(unit, "unit")


class TableSourceAdapter:
    """Translate only explicitly declared DataFrame columns into a SourceBatch."""

    def __init__(self, schema: TableSchema) -> None:
        self.schema = schema

    @property
    def adapter_id(self) -> str:
        return "pandas-table-source-v1"

    def adapt(
        self,
        source: pd.DataFrame,
        *,
        batch_id: str,
        provenance: Provenance,
        context: Context,
    ) -> SourceBatch:
        if not isinstance(source, pd.DataFrame):
            raise SourceAdapterError("source must be a pandas DataFrame")
        required = set(self.schema.feature_columns)
        if self.schema.timestamp_column is not None:
            required.add(self.schema.timestamp_column)
        missing = required - set(source.columns)
        if missing:
            names = ", ".join(sorted(missing))
            raise SourceAdapterError(f"source is missing required columns: {names}")
        if source.empty:
            raise SourceAdapterError("source table must contain rows")

        try:
            numeric = source.loc[:, self.schema.feature_columns].apply(
                pd.to_numeric, errors="raise"
            )
        except (TypeError, ValueError) as error:
            raise SourceAdapterError(
                "feature columns must contain numeric values"
            ) from error

        timestamps: tuple[datetime, ...] = ()
        if self.schema.timestamp_column is not None:
            raw_time = source.loc[:, self.schema.timestamp_column]
            try:
                parsed = pd.to_datetime(raw_time, errors="raise", utc=False)
            except (TypeError, ValueError) as error:
                raise SourceAdapterError("timestamp column cannot be parsed") from error
            timestamps = tuple(
                value.to_pydatetime() if isinstance(value, pd.Timestamp) else value
                for value in parsed
            )

        return ArraySourceAdapter().adapt(
            numeric.to_numpy(),
            batch_id=batch_id,
            provenance=provenance,
            context=context,
            timestamps=timestamps or None,
            feature_names=self.schema.feature_columns,
            units=tuple(
                self.schema.units.get(column)
                for column in self.schema.feature_columns
            ),
            row_axis=SourceAxis.TIME
            if self.schema.timestamp_column is not None
            else SourceAxis.ORDERED_SAMPLE,
        )
