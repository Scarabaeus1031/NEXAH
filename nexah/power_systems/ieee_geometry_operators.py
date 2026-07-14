"""Inspectable geometry measurements over manifest-bound IEEE frame campaigns."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import acos, fsum, isfinite, sqrt

from nexah.orientation import Provenance, Uncertainty
from nexah.orientation.base import ContractModel, require_text

from .ieee_geometry import (
    IEEEFeatureVector,
    IEEEFrameStatus,
    IEEEGeometryCampaign,
    IEEEGeometryFrame,
)
from .ieee_manifest import IEEEGeometryCaseManifest, IEEEProjectionDefinition


STANDARDIZED_PROJECTION_ID = "system-summary-standardized-v1"
REQUIRED_OPERATOR_IDS = (
    "adjacent-displacement-v1",
    "normalized-local-drift-v1",
    "campaign-path-length-v1",
    "direction-change-v1",
    "discrete-curvature-v1",
    "distance-to-last-converged-v1",
)


class IEEEGeometryOperatorError(ValueError):
    """Raised when a campaign cannot be measured under its frozen manifest."""


class IEEEGeometryValueStatus(str, Enum):
    """Availability of one geometry result without fabricating a replacement."""

    AVAILABLE = "available"
    INSUFFICIENT = "insufficient"
    NOT_APPLICABLE = "not_applicable"


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEStandardizationModel(ContractModel):
    """Development-fitted population standardization for one declared projection."""

    manifest_id: str
    projection_id: str
    fit_campaign_id: str
    fit_case_id: str
    feature_names: tuple[str, ...]
    means: tuple[float, ...]
    population_stddevs: tuple[float, ...]
    status: IEEEGeometryValueStatus
    zero_variance_features: tuple[str, ...]
    reason: str | None
    provenance: Provenance
    uncertainty: Uncertainty
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        for value, name in (
            (self.manifest_id, "manifest_id"),
            (self.projection_id, "projection_id"),
            (self.fit_campaign_id, "fit_campaign_id"),
            (self.fit_case_id, "fit_case_id"),
            (self.schema_version, "schema_version"),
        ):
            require_text(value, name)
        if not self.feature_names:
            raise ValueError("standardization model requires feature names")
        if len(self.feature_names) != len(set(self.feature_names)):
            raise ValueError("standardization feature names must be unique")
        if self.means or self.population_stddevs:
            if not (
                len(self.feature_names)
                == len(self.means)
                == len(self.population_stddevs)
            ):
                raise ValueError("standardization vectors must align")
            if any(not isfinite(value) for value in self.means):
                raise ValueError("standardization means must be finite")
            if any(
                not isfinite(value) or value < 0.0
                for value in self.population_stddevs
            ):
                raise ValueError("population standard deviations must be finite")
        if self.status is IEEEGeometryValueStatus.AVAILABLE:
            if self.reason is not None or self.zero_variance_features:
                raise ValueError("available model cannot carry insufficiency")
            if not self.means:
                raise ValueError("available model requires fitted values")
            if any(value == 0.0 for value in self.population_stddevs):
                raise ValueError("available model cannot contain zero variance")
        else:
            if not self.reason:
                raise ValueError("unavailable model requires a reason")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEProjectedFrame(ContractModel):
    """One frame represented in the frozen standardized system projection."""

    frame_id: str
    campaign_index: int
    load_scale: float
    status: IEEEGeometryValueStatus
    values: tuple[float, ...] | None
    reason: str | None

    def __post_init__(self) -> None:
        require_text(self.frame_id, "frame_id")
        if self.campaign_index < 0:
            raise ValueError("projected frame index cannot be negative")
        if not isfinite(self.load_scale) or self.load_scale <= 0.0:
            raise ValueError("projected frame load scale must be positive")
        _validate_optional_values(self.status, self.values, self.reason, "projection")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEGeometryStep(ContractModel):
    """Adjacent load-parameter relation; not a claim of physical time evolution."""

    source_frame_id: str
    target_frame_id: str
    source_index: int
    target_index: int
    source_load_scale: float
    target_load_scale: float
    delta_load_scale: float
    status: IEEEGeometryValueStatus
    delta_vector: tuple[float, ...] | None
    displacement: float | None
    normalized_local_drift: float | None
    cumulative_path_length: float | None
    reason: str | None
    parameter_semantics: str = "ordered_load_scale_not_time"

    def __post_init__(self) -> None:
        require_text(self.source_frame_id, "source_frame_id")
        require_text(self.target_frame_id, "target_frame_id")
        require_text(self.parameter_semantics, "parameter_semantics")
        if self.target_index != self.source_index + 1:
            raise ValueError("geometry step must connect adjacent frame indices")
        if self.delta_load_scale <= 0.0 or not isfinite(self.delta_load_scale):
            raise ValueError("geometry step requires positive load-scale spacing")
        values = (
            self.displacement,
            self.normalized_local_drift,
            self.cumulative_path_length,
        )
        if self.status is IEEEGeometryValueStatus.AVAILABLE:
            if self.delta_vector is None or any(value is None for value in values):
                raise ValueError("available geometry step requires all measurements")
            if self.reason is not None:
                raise ValueError("available geometry step cannot carry a reason")
            if any(not isfinite(value) or value < 0.0 for value in values if value is not None):
                raise ValueError("geometry step measurements must be finite")
        else:
            if self.delta_vector is not None or any(value is not None for value in values):
                raise ValueError("unavailable geometry step cannot carry measurements")
            if not self.reason:
                raise ValueError("unavailable geometry step requires a reason")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEGeometryTurn(ContractModel):
    """Direction change and discrete curvature at one centered campaign frame."""

    previous_frame_id: str
    center_frame_id: str
    next_frame_id: str
    center_index: int
    status: IEEEGeometryValueStatus
    direction_change_radians: float | None
    discrete_curvature: float | None
    reason: str | None

    def __post_init__(self) -> None:
        for value, name in (
            (self.previous_frame_id, "previous_frame_id"),
            (self.center_frame_id, "center_frame_id"),
            (self.next_frame_id, "next_frame_id"),
        ):
            require_text(value, name)
        if self.center_index < 1:
            raise ValueError("geometry turn requires a centered index")
        values = (self.direction_change_radians, self.discrete_curvature)
        if self.status is IEEEGeometryValueStatus.AVAILABLE:
            if any(value is None for value in values) or self.reason is not None:
                raise ValueError("available geometry turn requires both measurements")
            if any(not isfinite(value) or value < 0.0 for value in values if value is not None):
                raise ValueError("geometry turn measurements must be finite")
        else:
            if any(value is not None for value in values) or not self.reason:
                raise ValueError("unavailable geometry turn requires only a reason")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEESolverBoundaryDistance(ContractModel):
    """Sampled distance from a failed frame to the preceding converged frame."""

    failed_frame_id: str
    failed_index: int
    failed_load_scale: float
    last_converged_frame_id: str | None
    last_converged_load_scale: float | None
    status: IEEEGeometryValueStatus
    distance_load_scale: float | None
    solver_failure: str
    reason: str | None
    boundary_type: str = "solver_non_convergence"

    def __post_init__(self) -> None:
        require_text(self.failed_frame_id, "failed_frame_id")
        require_text(self.solver_failure, "solver_failure")
        require_text(self.boundary_type, "boundary_type")
        if self.status is IEEEGeometryValueStatus.AVAILABLE:
            if (
                self.last_converged_frame_id is None
                or self.last_converged_load_scale is None
                or self.distance_load_scale is None
                or self.reason is not None
            ):
                raise ValueError("available boundary distance requires a bracket origin")
            if self.distance_load_scale <= 0.0:
                raise ValueError("boundary distance must be positive")
        else:
            if self.distance_load_scale is not None or not self.reason:
                raise ValueError("unavailable boundary distance requires only a reason")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEGeometryAnalysis(ContractModel):
    """Typed, failure-aware WP-C measurements for one IEEE geometry campaign."""

    manifest_id: str
    campaign_id: str
    case_id: str
    case_role: str
    projection_model: IEEEStandardizationModel
    projected_frames: tuple[IEEEProjectedFrame, ...]
    steps: tuple[IEEEGeometryStep, ...]
    turns: tuple[IEEEGeometryTurn, ...]
    solver_boundaries: tuple[IEEESolverBoundaryDistance, ...]
    contiguous_converged_frame_ids: tuple[str, ...]
    total_path_length: float | None
    terminal_frame_id: str | None
    operator_ids: tuple[str, ...]
    provenance: Provenance
    uncertainty: Uncertainty
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        for value, name in (
            (self.manifest_id, "manifest_id"),
            (self.campaign_id, "campaign_id"),
            (self.case_id, "case_id"),
            (self.case_role, "case_role"),
            (self.schema_version, "schema_version"),
        ):
            require_text(value, name)
        if len(self.steps) != max(0, len(self.projected_frames) - 1):
            raise ValueError("analysis steps must cover every adjacent frame pair")
        if len(self.turns) != max(0, len(self.projected_frames) - 2):
            raise ValueError("analysis turns must cover every centered frame triple")
        if len(self.operator_ids) != len(set(self.operator_ids)):
            raise ValueError("analysis operator IDs must be unique")
        if self.total_path_length is not None and (
            not isfinite(self.total_path_length) or self.total_path_length < 0.0
        ):
            raise ValueError("total path length must be finite and non-negative")


def fit_ieee_standardization(
    campaign: IEEEGeometryCampaign,
    manifest: IEEEGeometryCaseManifest,
) -> IEEEStandardizationModel:
    """Fit the manifest-declared population standardization on development data."""

    _validate_campaign_manifest(campaign, manifest)
    if campaign.case_role != "method_development":
        raise IEEEGeometryOperatorError(
            "standardization must be fitted on a method-development campaign"
        )
    projection = _projection(manifest, STANDARDIZED_PROJECTION_ID)
    rows: list[tuple[float, ...]] = []
    for frame in campaign.frames:
        if frame.status is IEEEFrameStatus.CONVERGED:
            vector = _aligned_feature_values(frame.system_features, projection.inputs)
            if vector is None:
                return _insufficient_model(
                    campaign,
                    projection,
                    "converged development frame does not provide every projection feature",
                )
            rows.append(vector)
    if len(rows) < 2:
        return _insufficient_model(
            campaign,
            projection,
            "at least two converged development frames are required",
        )

    means = tuple(fsum(row[index] for row in rows) / len(rows) for index in range(len(projection.inputs)))
    stddevs = tuple(
        sqrt(fsum((row[index] - means[index]) ** 2 for row in rows) / len(rows))
        for index in range(len(projection.inputs))
    )
    zero_variance = tuple(
        name for name, value in zip(projection.inputs, stddevs) if value == 0.0
    )
    status = (
        IEEEGeometryValueStatus.INSUFFICIENT
        if zero_variance
        else IEEEGeometryValueStatus.AVAILABLE
    )
    reason = (
        "zero-variance development feature(s): " + ", ".join(zero_variance)
        if zero_variance
        else None
    )
    return IEEEStandardizationModel(
        manifest_id=manifest.manifest_id,
        projection_id=projection.projection_id,
        fit_campaign_id=campaign.campaign_id,
        fit_case_id=campaign.case_id,
        feature_names=projection.inputs,
        means=means,
        population_stddevs=stddevs,
        status=status,
        zero_variance_features=zero_variance,
        reason=reason,
        provenance=_analysis_provenance(
            campaign,
            method="IEEE-9 development population standardization v1",
            suffix="standardization",
        ),
        uncertainty=campaign.frames[0].uncertainty,
    )


def analyze_ieee_geometry(
    campaign: IEEEGeometryCampaign,
    manifest: IEEEGeometryCaseManifest,
    model: IEEEStandardizationModel,
) -> IEEEGeometryAnalysis:
    """Compute exactly the six frozen WP-C operators without bridging failures."""

    _validate_campaign_manifest(campaign, manifest)
    _validate_model(model, manifest)
    operator_ids = tuple(operator.operator_id for operator in manifest.operators)
    if set(operator_ids) != set(REQUIRED_OPERATOR_IDS):
        raise IEEEGeometryOperatorError(
            "manifest operator set differs from the implemented WP-C freeze"
        )

    projected = tuple(_project_frame(frame, model) for frame in campaign.frames)
    steps, total_path_length, terminal_frame_id = _steps(campaign.frames, projected)
    turns = _turns(campaign.frames, projected)
    boundaries = _solver_boundaries(campaign.frames)
    contiguous = []
    for frame in campaign.frames:
        if frame.status is not IEEEFrameStatus.CONVERGED:
            break
        contiguous.append(frame.frame_id)
    return IEEEGeometryAnalysis(
        manifest_id=manifest.manifest_id,
        campaign_id=campaign.campaign_id,
        case_id=campaign.case_id,
        case_role=campaign.case_role,
        projection_model=model,
        projected_frames=projected,
        steps=steps,
        turns=turns,
        solver_boundaries=boundaries,
        contiguous_converged_frame_ids=tuple(contiguous),
        total_path_length=total_path_length,
        terminal_frame_id=terminal_frame_id,
        operator_ids=operator_ids,
        provenance=_analysis_provenance(
            campaign,
            method="manifest-bound IEEE geometry operators v1",
            suffix="geometry-analysis",
        ),
        uncertainty=campaign.frames[0].uncertainty,
    )


def _project_frame(
    frame: IEEEGeometryFrame,
    model: IEEEStandardizationModel,
) -> IEEEProjectedFrame:
    if frame.status is IEEEFrameStatus.FAILED:
        return IEEEProjectedFrame(
            frame_id=frame.frame_id,
            campaign_index=frame.campaign_index,
            load_scale=frame.load_scale,
            status=IEEEGeometryValueStatus.INSUFFICIENT,
            values=None,
            reason="failed frame contains no fabricated physical feature vector",
        )
    if model.status is not IEEEGeometryValueStatus.AVAILABLE:
        return IEEEProjectedFrame(
            frame_id=frame.frame_id,
            campaign_index=frame.campaign_index,
            load_scale=frame.load_scale,
            status=IEEEGeometryValueStatus.INSUFFICIENT,
            values=None,
            reason=model.reason or "standardization model is unavailable",
        )
    raw = _aligned_feature_values(frame.system_features, model.feature_names)
    if raw is None:
        return IEEEProjectedFrame(
            frame_id=frame.frame_id,
            campaign_index=frame.campaign_index,
            load_scale=frame.load_scale,
            status=IEEEGeometryValueStatus.INSUFFICIENT,
            values=None,
            reason="frame features do not align with the frozen projection",
        )
    values = tuple(
        (value - mean) / scale
        for value, mean, scale in zip(raw, model.means, model.population_stddevs)
    )
    return IEEEProjectedFrame(
        frame_id=frame.frame_id,
        campaign_index=frame.campaign_index,
        load_scale=frame.load_scale,
        status=IEEEGeometryValueStatus.AVAILABLE,
        values=values,
        reason=None,
    )


def _steps(
    frames: tuple[IEEEGeometryFrame, ...],
    projected: tuple[IEEEProjectedFrame, ...],
) -> tuple[tuple[IEEEGeometryStep, ...], float | None, str | None]:
    records: list[IEEEGeometryStep] = []
    cumulative = 0.0
    available_count = 0
    terminated = False
    terminal_frame_id: str | None = None
    for source, target, left, right in zip(
        frames, frames[1:], projected, projected[1:]
    ):
        spacing = target.load_scale - source.load_scale
        reason: str | None = None
        if terminated:
            reason = f"sampled path already terminated at {terminal_frame_id}"
        elif left.status is not IEEEGeometryValueStatus.AVAILABLE:
            reason = left.reason or "source projection is unavailable"
        elif right.status is not IEEEGeometryValueStatus.AVAILABLE:
            reason = right.reason or "target projection is unavailable"
        if reason is not None:
            if not terminated and (
                source.status is IEEEFrameStatus.FAILED
                or target.status is IEEEFrameStatus.FAILED
            ):
                terminal = source if source.status is IEEEFrameStatus.FAILED else target
                terminal_frame_id = terminal.frame_id
                terminated = True
            records.append(
                IEEEGeometryStep(
                    source_frame_id=source.frame_id,
                    target_frame_id=target.frame_id,
                    source_index=source.campaign_index,
                    target_index=target.campaign_index,
                    source_load_scale=source.load_scale,
                    target_load_scale=target.load_scale,
                    delta_load_scale=spacing,
                    status=IEEEGeometryValueStatus.INSUFFICIENT,
                    delta_vector=None,
                    displacement=None,
                    normalized_local_drift=None,
                    cumulative_path_length=None,
                    reason=reason,
                )
            )
            continue
        assert left.values is not None and right.values is not None
        delta = tuple(current - previous for previous, current in zip(left.values, right.values))
        displacement = _norm(delta)
        cumulative += displacement
        available_count += 1
        records.append(
            IEEEGeometryStep(
                source_frame_id=source.frame_id,
                target_frame_id=target.frame_id,
                source_index=source.campaign_index,
                target_index=target.campaign_index,
                source_load_scale=source.load_scale,
                target_load_scale=target.load_scale,
                delta_load_scale=spacing,
                status=IEEEGeometryValueStatus.AVAILABLE,
                delta_vector=delta,
                displacement=displacement,
                normalized_local_drift=displacement / spacing,
                cumulative_path_length=cumulative,
                reason=None,
            )
        )
    return tuple(records), cumulative if available_count else None, terminal_frame_id


def _turns(
    frames: tuple[IEEEGeometryFrame, ...],
    projected: tuple[IEEEProjectedFrame, ...],
) -> tuple[IEEEGeometryTurn, ...]:
    records = []
    for index in range(1, len(frames) - 1):
        previous, center, following = frames[index - 1 : index + 2]
        p_previous, p_center, p_following = projected[index - 1 : index + 2]
        unavailable = next(
            (
                item.reason or "projection is unavailable"
                for item in (p_previous, p_center, p_following)
                if item.status is not IEEEGeometryValueStatus.AVAILABLE
            ),
            None,
        )
        if unavailable is not None:
            records.append(
                IEEEGeometryTurn(
                    previous_frame_id=previous.frame_id,
                    center_frame_id=center.frame_id,
                    next_frame_id=following.frame_id,
                    center_index=center.campaign_index,
                    status=IEEEGeometryValueStatus.INSUFFICIENT,
                    direction_change_radians=None,
                    discrete_curvature=None,
                    reason=unavailable,
                )
            )
            continue
        assert (
            p_previous.values is not None
            and p_center.values is not None
            and p_following.values is not None
        )
        incoming = tuple(
            current - prior
            for prior, current in zip(p_previous.values, p_center.values)
        )
        outgoing = tuple(
            future - current
            for current, future in zip(p_center.values, p_following.values)
        )
        incoming_norm = _norm(incoming)
        outgoing_norm = _norm(outgoing)
        if incoming_norm == 0.0 or outgoing_norm == 0.0:
            records.append(
                IEEEGeometryTurn(
                    previous_frame_id=previous.frame_id,
                    center_frame_id=center.frame_id,
                    next_frame_id=following.frame_id,
                    center_index=center.campaign_index,
                    status=IEEEGeometryValueStatus.INSUFFICIENT,
                    direction_change_radians=None,
                    discrete_curvature=None,
                    reason="direction change requires two non-zero displacements",
                )
            )
            continue
        cosine = fsum(a * b for a, b in zip(incoming, outgoing)) / (
            incoming_norm * outgoing_norm
        )
        angle = acos(max(-1.0, min(1.0, cosine)))
        local_arc_length = 0.5 * (incoming_norm + outgoing_norm)
        records.append(
            IEEEGeometryTurn(
                previous_frame_id=previous.frame_id,
                center_frame_id=center.frame_id,
                next_frame_id=following.frame_id,
                center_index=center.campaign_index,
                status=IEEEGeometryValueStatus.AVAILABLE,
                direction_change_radians=angle,
                discrete_curvature=angle / local_arc_length,
                reason=None,
            )
        )
    return tuple(records)


def _solver_boundaries(
    frames: tuple[IEEEGeometryFrame, ...],
) -> tuple[IEEESolverBoundaryDistance, ...]:
    records = []
    last_converged: IEEEGeometryFrame | None = None
    for frame in frames:
        if frame.status is IEEEFrameStatus.CONVERGED:
            last_converged = frame
            continue
        assert frame.failure is not None
        if last_converged is None:
            records.append(
                IEEESolverBoundaryDistance(
                    failed_frame_id=frame.frame_id,
                    failed_index=frame.campaign_index,
                    failed_load_scale=frame.load_scale,
                    last_converged_frame_id=None,
                    last_converged_load_scale=None,
                    status=IEEEGeometryValueStatus.INSUFFICIENT,
                    distance_load_scale=None,
                    solver_failure=frame.failure,
                    reason="no preceding converged frame exists in the campaign",
                )
            )
            continue
        records.append(
            IEEESolverBoundaryDistance(
                failed_frame_id=frame.frame_id,
                failed_index=frame.campaign_index,
                failed_load_scale=frame.load_scale,
                last_converged_frame_id=last_converged.frame_id,
                last_converged_load_scale=last_converged.load_scale,
                status=IEEEGeometryValueStatus.AVAILABLE,
                distance_load_scale=frame.load_scale - last_converged.load_scale,
                solver_failure=frame.failure,
                reason=None,
            )
        )
    return tuple(records)


def _projection(
    manifest: IEEEGeometryCaseManifest,
    projection_id: str,
) -> IEEEProjectionDefinition:
    try:
        return next(
            projection
            for projection in manifest.projections
            if projection.projection_id == projection_id
        )
    except StopIteration as error:
        raise IEEEGeometryOperatorError(
            f"manifest does not declare projection {projection_id}"
        ) from error


def _aligned_feature_values(
    vector: IEEEFeatureVector | None,
    names: tuple[str, ...],
) -> tuple[float, ...] | None:
    if vector is None:
        return None
    values = dict(zip(vector.feature_names, vector.values))
    if not set(names) <= set(values):
        return None
    return tuple(values[name] for name in names)


def _insufficient_model(
    campaign: IEEEGeometryCampaign,
    projection: IEEEProjectionDefinition,
    reason: str,
) -> IEEEStandardizationModel:
    return IEEEStandardizationModel(
        manifest_id=campaign.manifest_id,
        projection_id=projection.projection_id,
        fit_campaign_id=campaign.campaign_id,
        fit_case_id=campaign.case_id,
        feature_names=projection.inputs,
        means=(),
        population_stddevs=(),
        status=IEEEGeometryValueStatus.INSUFFICIENT,
        zero_variance_features=(),
        reason=reason,
        provenance=_analysis_provenance(
            campaign,
            method="insufficient IEEE development standardization v1",
            suffix="standardization",
        ),
        uncertainty=campaign.frames[0].uncertainty,
    )


def _validate_campaign_manifest(
    campaign: IEEEGeometryCampaign,
    manifest: IEEEGeometryCaseManifest,
) -> None:
    if campaign.manifest_id != manifest.manifest_id:
        raise IEEEGeometryOperatorError("campaign and manifest identities differ")
    if campaign.campaign_axis != manifest.campaign_axis:
        raise IEEEGeometryOperatorError("campaign and manifest axes differ")
    try:
        case = next(item for item in manifest.cases if item.case_id == campaign.case_id)
    except StopIteration as error:
        raise IEEEGeometryOperatorError("campaign case is absent from manifest") from error
    if case.role != campaign.case_role:
        raise IEEEGeometryOperatorError("campaign role differs from manifest")
    if tuple(frame.load_scale for frame in campaign.frames) != case.load_scales:
        raise IEEEGeometryOperatorError("campaign grid differs from manifest")


def _validate_model(
    model: IEEEStandardizationModel,
    manifest: IEEEGeometryCaseManifest,
) -> None:
    projection = _projection(manifest, STANDARDIZED_PROJECTION_ID)
    if model.manifest_id != manifest.manifest_id:
        raise IEEEGeometryOperatorError("model and manifest identities differ")
    if model.projection_id != projection.projection_id:
        raise IEEEGeometryOperatorError("model uses a different projection")
    if model.feature_names != projection.inputs:
        raise IEEEGeometryOperatorError("model features differ from frozen projection")


def _analysis_provenance(
    campaign: IEEEGeometryCampaign,
    *,
    method: str,
    suffix: str,
) -> Provenance:
    return Provenance(
        source=campaign.provenance.source,
        method=method,
        recorded_at=campaign.provenance.recorded_at,
        record_id=f"{campaign.campaign_id}:{suffix}",
        metadata={
            "manifest_id": campaign.manifest_id,
            "source_record_id": campaign.provenance.record_id,
            "case_id": campaign.case_id,
            "campaign_axis": campaign.campaign_axis,
        },
    )


def _norm(values: tuple[float, ...]) -> float:
    return sqrt(fsum(value * value for value in values))


def _validate_optional_values(
    status: IEEEGeometryValueStatus,
    values: tuple[float, ...] | None,
    reason: str | None,
    label: str,
) -> None:
    if status is IEEEGeometryValueStatus.AVAILABLE:
        if values is None or not values or reason is not None:
            raise ValueError(f"available {label} requires values and no reason")
        if any(not isfinite(value) for value in values):
            raise ValueError(f"available {label} values must be finite")
    elif values is not None or not reason:
        raise ValueError(f"unavailable {label} requires only a reason")
