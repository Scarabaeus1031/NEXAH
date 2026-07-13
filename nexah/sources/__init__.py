"""Source-side contracts and reference adapters."""

from .array import ArraySourceAdapter
from .base import (
    SourceAdapter,
    SourceAdapterError,
    SourceAxis,
    SourceBatch,
    SourceFeature,
    SourceQuality,
)
from .table import TableSchema, TableSourceAdapter

__all__ = [
    "ArraySourceAdapter",
    "SourceAdapter",
    "SourceAdapterError",
    "SourceAxis",
    "SourceBatch",
    "SourceFeature",
    "SourceQuality",
    "TableSchema",
    "TableSourceAdapter",
]
