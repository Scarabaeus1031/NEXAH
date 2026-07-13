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
from .ieee import (
    IEEECoupledCampaign,
    IEEEPandapowerAdapter,
    IEEEPhysicalSnapshot,
    IEEESourceAdapterError,
)

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
    "IEEECoupledCampaign",
    "IEEEPandapowerAdapter",
    "IEEEPhysicalSnapshot",
    "IEEESourceAdapterError",
]
