"""Manifest-bound physical frames for the Phase V IEEE geometry case."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from math import isfinite

from nexah.orientation import Provenance, Uncertainty, UncertaintyKind
from nexah.orientation.base import ContractModel, require_text
from nexah.sources import IEEECoupledCampaign, IEEEPhysicalSnapshot, SourceBatch

from .ieee_manifest import (
    IEEEGeometryCaseManifest,
    check_manifest_adapter_protocol,
    check_manifest_environment,
)


class IEEEGeometryFrameError(ValueError):
    """Raised when a physical campaign cannot satisfy the frozen frame contract."""


class IEEEFrameStatus(str, Enum):
    CONVERGED = "converged"
    FAILED = "failed"


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEEntityView(ContractModel):
    """One immutable bus or line table with explicit variables and units."""

    view_id: str
    entity_scope: str
    entity_ids: tuple[str, ...]
    variable_names: tuple[str, ...]
    units: tuple[str, ...]
    values: tuple[tuple[float, ...], ...]

    def __post_init__(self) -> None:
        require_text(self.view_id, "view_id")
        require_text(self.entity_scope, "entity_scope")
        if not self.entity_ids or len(self.entity_ids) != len(self.values):
            raise ValueError("entity IDs must match non-empty view rows")
        if len(self.entity_ids) != len(set(self.entity_ids)):
            raise ValueError("entity IDs must be unique")
        if not self.variable_names or len(self.variable_names) != len(self.units):
            raise ValueError("variable names and units must align")
        if len(self.variable_names) != len(set(self.variable_names)):
            raise ValueError("entity-view variable names must be unique")
        width = len(self.variable_names)
        if any(len(row) != width for row in self.values):
            raise ValueError("every entity row must match the declared variables")
        if any(not isfinite(value) for row in self.values for value in row):
            raise ValueError("entity-view values must be finite")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEFeatureVector(ContractModel):
    """Raw system-summary vector; normalization belongs to the next work package."""

    feature_names: tuple[str, ...]
    units: tuple[str, ...]
    values: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.feature_names:
            raise ValueError("feature vector requires features")
        if not (
            len(self.feature_names) == len(self.units) == len(self.values)
        ):
            raise ValueError("feature names, units, and values must align")
        if len(self.feature_names) != len(set(self.feature_names)):
            raise ValueError("feature names must be unique")
        if any(not isfinite(value) for value in self.values):
            raise ValueError("feature-vector values must be finite")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEGeometryFrame(ContractModel):
    """One manifest-bound campaign position, including honest failed positions."""

    frame_id: str
    manifest_id: str
    campaign_id: str
    case_id: str
    case_role: str
    campaign_index: int
    campaign_axis: str
    load_scale: float
    topology_id: str
    status: IEEEFrameStatus
    entity_views: tuple[IEEEEntityView, ...]
    system_features: IEEEFeatureVector | None
    declared_projection_ids: tuple[str, ...]
    failure: str | None
    provenance: Provenance
    uncertainty: Uncertainty
    evidence_class: str = "benchmark_model"
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        for value, name in (
            (self.frame_id, "frame_id"),
            (self.manifest_id, "manifest_id"),
            (self.campaign_id, "campaign_id"),
            (self.case_id, "case_id"),
            (self.case_role, "case_role"),
            (self.campaign_axis, "campaign_axis"),
            (self.topology_id, "topology_id"),
            (self.schema_version, "schema_version"),
        ):
            require_text(value, name)
        if self.campaign_index < 0:
            raise ValueError("campaign_index cannot be negative")
        if not isfinite(self.load_scale) or self.load_scale <= 0.0:
            raise ValueError("load_scale must be finite and positive")
        if self.campaign_axis != "ordered_load_scale_not_time":
            raise ValueError("geometry frame axis must remain ordered load scale")
        if self.evidence_class != "benchmark_model":
            raise ValueError("IEEE frames must remain benchmark-model evidence")
        if not self.declared_projection_ids:
            raise ValueError("frame requires declared projection identities")
        if len(self.declared_projection_ids) != len(set(self.declared_projection_ids)):
            raise ValueError("declared projection identities must be unique")
        scopes = [view.entity_scope for view in self.entity_views]
        if len(scopes) != len(set(scopes)):
            raise ValueError("entity view scopes must be unique")
        if self.status is IEEEFrameStatus.CONVERGED:
            if self.failure is not None:
                raise ValueError("converged frame cannot contain a failure")
            if self.system_features is None or set(scopes) != {"bus", "line"}:
                raise ValueError(
                    "converged frame requires system features and bus/line views"
                )
        else:
            if not self.failure:
                raise ValueError("failed frame requires a failure description")
            if self.system_features is not None or self.entity_views:
                raise ValueError("failed frame cannot contain fabricated physics")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEGeometryCampaign(ContractModel):
    """Ordered immutable frames sharing one explicit topology identity."""

    manifest_id: str
    campaign_id: str
    case_id: str
    case_role: str
    campaign_axis: str
    topology_id: str
    frames: tuple[IEEEGeometryFrame, ...]
    provenance: Provenance
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        for value, name in (
            (self.manifest_id, "manifest_id"),
            (self.campaign_id, "campaign_id"),
            (self.case_id, "case_id"),
            (self.case_role, "case_role"),
            (self.campaign_axis, "campaign_axis"),
            (self.topology_id, "topology_id"),
            (self.schema_version, "schema_version"),
        ):
            require_text(value, name)
        if len(self.frames) < 3:
            raise ValueError("geometry campaign requires at least three frames")
        if tuple(frame.campaign_index for frame in self.frames) != tuple(
            range(len(self.frames))
        ):
            raise ValueError("frame indices must be contiguous and ordered")
        if any(
            current.load_scale <= previous.load_scale
            for previous, current in zip(self.frames, self.frames[1:])
        ):
            raise ValueError("frame load scales must be strictly increasing")
        if any(
            frame.manifest_id != self.manifest_id
            or frame.campaign_id != self.campaign_id
            or frame.case_id != self.case_id
            or frame.case_role != self.case_role
            or frame.campaign_axis != self.campaign_axis
            or frame.topology_id != self.topology_id
            for frame in self.frames
        ):
            raise ValueError("all frames must share campaign identity and topology")


def build_ieee_geometry_campaign(
    campaign: IEEECoupledCampaign,
    manifest: IEEEGeometryCaseManifest,
    *,
    require_environment_match: bool = True,
) -> IEEEGeometryCampaign:
    """Wrap existing coupled evidence without adding geometric interpretation."""

    protocol_mismatches = check_manifest_adapter_protocol(manifest)
    if protocol_mismatches:
        raise IEEEGeometryFrameError("; ".join(protocol_mismatches))
    environment = check_manifest_environment(manifest)
    if require_environment_match and not environment.compatible:
        raise IEEEGeometryFrameError("; ".join(environment.mismatches))
    try:
        case = next(item for item in manifest.cases if item.case_id == campaign.case_id)
    except StopIteration as error:
        raise IEEEGeometryFrameError(
            f"case {campaign.case_id} is not declared by manifest"
        ) from error
    actual_scales = tuple(snapshot.load_scale for snapshot in campaign.snapshots)
    if actual_scales != case.load_scales:
        raise IEEEGeometryFrameError("campaign load scales differ from frozen manifest")
    topology_id = _campaign_topology_id(campaign)
    summary_rows = dict(
        zip(campaign.campaign_batch.row_ids, campaign.campaign_batch.values)
    )
    projection_ids = tuple(item.projection_id for item in manifest.projections)
    frames = tuple(
        _build_frame(
            snapshot,
            campaign=campaign,
            manifest=manifest,
            case_role=case.role,
            campaign_index=index,
            topology_id=topology_id,
            summary_row=summary_rows.get(snapshot.scenario_id),
            projection_ids=projection_ids,
        )
        for index, snapshot in enumerate(campaign.snapshots)
    )
    return IEEEGeometryCampaign(
        manifest_id=manifest.manifest_id,
        campaign_id=campaign.campaign_id,
        case_id=campaign.case_id,
        case_role=case.role,
        campaign_axis=manifest.campaign_axis,
        topology_id=topology_id,
        frames=frames,
        provenance=Provenance(
            source=campaign.provenance.source,
            method="manifest-bound IEEE geometry frame builder v1",
            recorded_at=campaign.provenance.recorded_at,
            record_id=f"{campaign.campaign_id}:geometry-frames",
            metadata={
                "manifest_id": manifest.manifest_id,
                "source_record_id": campaign.provenance.record_id,
            },
        ),
    )


def _build_frame(
    snapshot: IEEEPhysicalSnapshot,
    *,
    campaign: IEEECoupledCampaign,
    manifest: IEEEGeometryCaseManifest,
    case_role: str,
    campaign_index: int,
    topology_id: str,
    summary_row: tuple[float, ...] | None,
    projection_ids: tuple[str, ...],
) -> IEEEGeometryFrame:
    provenance = Provenance(
        source=campaign.provenance.source,
        method="manifest-bound IEEE geometry frame builder v1",
        recorded_at=campaign.provenance.recorded_at,
        record_id=f"{snapshot.scenario_id}:geometry-frame",
        metadata={
            "source_record_id": campaign.provenance.record_id,
            "manifest_id": manifest.manifest_id,
        },
    )
    uncertainty = Uncertainty(
        kind=UncertaintyKind.UNKNOWN,
        value=None,
        basis=(
            "No calibrated physical or probabilistic uncertainty is available; "
            "the frame records deterministic benchmark computation and solver status."
        ),
    )
    if not snapshot.converged:
        if summary_row is not None:
            raise IEEEGeometryFrameError("failed snapshot has a numeric summary row")
        return IEEEGeometryFrame(
            frame_id=f"{snapshot.scenario_id}:geometry-frame",
            manifest_id=manifest.manifest_id,
            campaign_id=campaign.campaign_id,
            case_id=campaign.case_id,
            case_role=case_role,
            campaign_index=campaign_index,
            campaign_axis=manifest.campaign_axis,
            load_scale=snapshot.load_scale,
            topology_id=topology_id,
            status=IEEEFrameStatus.FAILED,
            entity_views=(),
            system_features=None,
            declared_projection_ids=projection_ids,
            failure=snapshot.failure,
            provenance=provenance,
            uncertainty=uncertainty,
        )
    if snapshot.bus_batch is None or snapshot.line_batch is None or summary_row is None:
        raise IEEEGeometryFrameError("converged snapshot is missing physical evidence")
    if summary_row[0] != snapshot.load_scale:
        raise IEEEGeometryFrameError("summary row and snapshot load scales differ")
    summary_features = campaign.campaign_batch.features[1:]
    return IEEEGeometryFrame(
        frame_id=f"{snapshot.scenario_id}:geometry-frame",
        manifest_id=manifest.manifest_id,
        campaign_id=campaign.campaign_id,
        case_id=campaign.case_id,
        case_role=case_role,
        campaign_index=campaign_index,
        campaign_axis=manifest.campaign_axis,
        load_scale=snapshot.load_scale,
        topology_id=topology_id,
        status=IEEEFrameStatus.CONVERGED,
        entity_views=(
            _entity_view(snapshot.bus_batch, scope="bus"),
            _entity_view(snapshot.line_batch, scope="line"),
        ),
        system_features=IEEEFeatureVector(
            feature_names=tuple(feature.name for feature in summary_features),
            units=tuple(feature.unit or "unspecified" for feature in summary_features),
            values=tuple(summary_row[1:]),
        ),
        declared_projection_ids=projection_ids,
        failure=None,
        provenance=provenance,
        uncertainty=uncertainty,
    )


def _entity_view(batch: SourceBatch, *, scope: str) -> IEEEEntityView:
    return IEEEEntityView(
        view_id=batch.batch_id,
        entity_scope=scope,
        entity_ids=batch.row_ids,
        variable_names=tuple(feature.name for feature in batch.features),
        units=tuple(feature.unit or "unspecified" for feature in batch.features),
        values=batch.values,
    )


def _campaign_topology_id(campaign: IEEECoupledCampaign) -> str:
    converged = [snapshot for snapshot in campaign.snapshots if snapshot.converged]
    if not converged:
        raise IEEEGeometryFrameError("campaign has no converged topology evidence")
    first = converged[0]
    assert first.bus_batch is not None and first.line_batch is not None
    signature = _topology_signature(first)
    if any(_topology_signature(snapshot) != signature for snapshot in converged[1:]):
        raise IEEEGeometryFrameError("topology identity changes within frozen campaign")
    encoded = json.dumps(signature, sort_keys=True, separators=(",", ":")).encode()
    return f"sha256:{sha256(encoded).hexdigest()}"


def _topology_signature(snapshot: IEEEPhysicalSnapshot) -> dict[str, object]:
    if snapshot.bus_batch is None or snapshot.line_batch is None:
        raise IEEEGeometryFrameError("failed snapshot has no topology signature")
    return {
        "case_id": snapshot.case_id,
        "bus_ids": snapshot.bus_batch.row_ids,
        "line_ids": snapshot.line_batch.row_ids,
        "bus_variables": tuple(
            (feature.name, feature.unit) for feature in snapshot.bus_batch.features
        ),
        "line_variables": tuple(
            (feature.name, feature.unit) for feature in snapshot.line_batch.features
        ),
    }
