"""Prospectively declared projection-fidelity sidecar for IEEE Geometry V1.

The sidecar consumes committed physical frames.  It does not run a solver,
alter the frozen IEEE Geometry V1 protocol, or assign prediction/control
semantics to representation comparisons.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt

import numpy as np
from numpy.typing import NDArray

from nexah.orientation.base import ContractModel, require_text

from .ieee_geometry import IEEEFrameStatus, IEEEGeometryCampaign, IEEEGeometryFrame


FloatArray = NDArray[np.float64]
SQRT2 = sqrt(2.0)
TOLERANCE = 1e-12
FEATURE_NAMES = (
    "mean_bus_voltage",
    "bus_voltage_std",
    "bus_angle_range",
    "maximum_line_loading",
    "total_bus_consumption_p",
    "total_bus_consumption_q",
    "minimum_bus_voltage",
    "maximum_bus_voltage",
)
REPRESENTATION_NAMES = (
    "FULL8",
    "Q_ONLY7",
    "Q_PLUS_R8",
    "PCA7",
    "RANDOM7",
    "DROP_MIN7",
    "DROP_MAX7",
    "MAINTAINED7",
)


class IEEEProjectionFidelityError(ValueError):
    """Raised when source semantics or fitted-sidecar boundaries are violated."""


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEProjectionFidelityModel(ContractModel):
    """All fitted state required for evaluation without target-case refitting."""

    protocol_id: str
    fit_campaign_id: str
    fit_case_id: str
    feature_names: tuple[str, ...]
    means: tuple[float, ...]
    population_stddevs: tuple[float, ...]
    pca_basis: tuple[tuple[float, ...], ...]
    random_basis: tuple[tuple[float, ...], ...]
    maintained_means: tuple[float, ...]
    maintained_population_stddevs: tuple[float, ...]
    random_seed: int = 8208
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        for value, name in (
            (self.protocol_id, "protocol_id"),
            (self.fit_campaign_id, "fit_campaign_id"),
            (self.fit_case_id, "fit_case_id"),
            (self.schema_version, "schema_version"),
        ):
            require_text(value, name)
        if self.feature_names != FEATURE_NAMES:
            raise ValueError("fidelity model feature contract differs from V1")
        if len(self.means) != 8 or len(self.population_stddevs) != 8:
            raise ValueError("fidelity model requires eight fitted features")
        if len(self.maintained_means) != 7 or len(self.maintained_population_stddevs) != 7:
            raise ValueError("maintained comparison requires seven fitted features")
        if len(self.pca_basis) != 8 or any(len(row) != 7 for row in self.pca_basis):
            raise ValueError("PCA basis must have shape 8x7")
        if len(self.random_basis) != 8 or any(len(row) != 7 for row in self.random_basis):
            raise ValueError("random basis must have shape 8x7")
        numeric = (
            *self.means,
            *self.population_stddevs,
            *self.maintained_means,
            *self.maintained_population_stddevs,
            *(value for row in self.pca_basis for value in row),
            *(value for row in self.random_basis for value in row),
        )
        if any(not isfinite(value) for value in numeric):
            raise ValueError("fidelity model values must be finite")
        if any(value <= 0.0 for value in self.population_stddevs):
            raise ValueError("fidelity model cannot contain zero variance")
        if any(value <= 0.0 for value in self.maintained_population_stddevs):
            raise ValueError("maintained comparison cannot contain zero variance")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEProjectionFidelityMetrics(ContractModel):
    """Distance and ordered-path fidelity against the eight-coordinate view."""

    representation: str
    stored_scalars: int
    pair_distance_nrmse: float
    pair_distance_correlation: float
    adjacent_relative_error_median: float
    adjacent_relative_error_max: float
    path_length_relative_error: float
    turn_angle_mae_degrees: float
    pair_distance_max_abs_error: float

    def __post_init__(self) -> None:
        require_text(self.representation, "representation")
        if self.representation not in REPRESENTATION_NAMES:
            raise ValueError("unknown fidelity representation")
        if self.stored_scalars not in (7, 8):
            raise ValueError("stored scalar count must be seven or eight")
        values = (
            self.pair_distance_nrmse,
            self.pair_distance_correlation,
            self.adjacent_relative_error_median,
            self.adjacent_relative_error_max,
            self.path_length_relative_error,
            self.turn_angle_mae_degrees,
            self.pair_distance_max_abs_error,
        )
        if any(not isfinite(value) for value in values):
            raise ValueError("fidelity metrics must be finite")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEProjectionFidelityCaseResult(ContractModel):
    """One development or evaluation campaign measured under a frozen model."""

    campaign_id: str
    case_id: str
    case_role: str
    frame_count: int
    converged_prefix_count: int
    failed_frame_count: int
    load_scale_min: float
    load_scale_max_converged: float
    source_reproduction_max_error: float
    standardized_reconstruction_max_error: float
    raw_reconstruction_max_error: float
    metrics: tuple[IEEEProjectionFidelityMetrics, ...]

    def __post_init__(self) -> None:
        for value, name in (
            (self.campaign_id, "campaign_id"),
            (self.case_id, "case_id"),
            (self.case_role, "case_role"),
        ):
            require_text(value, name)
        if self.frame_count < 1 or self.converged_prefix_count < 3:
            raise ValueError("fidelity analysis requires at least three prefix frames")
        if self.converged_prefix_count + self.failed_frame_count > self.frame_count:
            raise ValueError("campaign counts are inconsistent")
        if tuple(item.representation for item in self.metrics) != REPRESENTATION_NAMES:
            raise ValueError("fidelity metrics must follow the frozen representation order")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEProjectionFidelityAnalysis(ContractModel):
    """Bound development/evaluation result and explicit claim boundary."""

    protocol_id: str
    model: IEEEProjectionFidelityModel
    development: IEEEProjectionFidelityCaseResult
    evaluation: IEEEProjectionFidelityCaseResult
    source_reproduction_max_error: float
    q_plus_r_standardized_reconstruction_max_error: float
    q_plus_r_raw_reconstruction_max_error: float
    q_plus_r_pair_distance_max_error: float
    q_only_kernel_max_distance: float
    q_plus_r_kernel_detection_rate: float
    evaluation_refit: bool
    status: str
    decision: str
    nonclaims: tuple[str, ...]
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        require_text(self.protocol_id, "protocol_id")
        require_text(self.status, "status")
        require_text(self.decision, "decision")
        require_text(self.schema_version, "schema_version")
        if self.development.case_id != self.model.fit_case_id:
            raise ValueError("development result must match fitted case")
        if self.evaluation_refit:
            raise ValueError("evaluation refit is prohibited")
        if not self.nonclaims:
            raise ValueError("fidelity analysis requires explicit nonclaims")


def fit_ieee_projection_fidelity_model(
    campaign: IEEEGeometryCampaign,
    *,
    protocol_id: str = "ieee-projection-fidelity-v1",
    random_seed: int = 8208,
) -> IEEEProjectionFidelityModel:
    """Fit standardization and baselines on a development campaign only."""

    if campaign.case_role != "method_development":
        raise IEEEProjectionFidelityError("model fit requires method_development role")
    raw, _, _ = _campaign_matrix(campaign)
    means, stddevs = _fit_standardization(raw)
    standardized = (raw - means) / stddevs
    _, _, vt = np.linalg.svd(standardized, full_matrices=False)
    pca_basis = vt[:7].T
    rng = np.random.default_rng(random_seed)
    random_basis, _ = np.linalg.qr(rng.normal(size=(8, 7)))
    maintained = _maintained_raw(raw)
    maintained_means, maintained_stddevs = _fit_standardization(maintained)
    return IEEEProjectionFidelityModel(
        protocol_id=protocol_id,
        fit_campaign_id=campaign.campaign_id,
        fit_case_id=campaign.case_id,
        feature_names=FEATURE_NAMES,
        means=_tuple(means),
        population_stddevs=_tuple(stddevs),
        pca_basis=tuple(_tuple(row) for row in pca_basis),
        random_basis=tuple(_tuple(row) for row in random_basis),
        maintained_means=_tuple(maintained_means),
        maintained_population_stddevs=_tuple(maintained_stddevs),
        random_seed=random_seed,
    )


def analyze_ieee_projection_fidelity_case(
    campaign: IEEEGeometryCampaign,
    model: IEEEProjectionFidelityModel,
) -> IEEEProjectionFidelityCaseResult:
    """Apply one already-fitted fidelity model without target-case refitting."""

    raw, source_error, prefix = _campaign_matrix(campaign)
    means = np.asarray(model.means)
    stddevs = np.asarray(model.population_stddevs)
    standardized = (raw - means) / stddevs
    representations = _representations(standardized, raw, model)
    metrics = tuple(
        _fidelity_metrics(name, standardized, representations[name])
        for name in REPRESENTATION_NAMES
    )
    decoded_standardized = _qr_decode(representations["Q_PLUS_R8"])
    decoded_raw = decoded_standardized * stddevs + means
    failed = sum(frame.status is IEEEFrameStatus.FAILED for frame in campaign.frames)
    return IEEEProjectionFidelityCaseResult(
        campaign_id=campaign.campaign_id,
        case_id=campaign.case_id,
        case_role=campaign.case_role,
        frame_count=len(campaign.frames),
        converged_prefix_count=len(prefix),
        failed_frame_count=failed,
        load_scale_min=float(prefix[0].load_scale),
        load_scale_max_converged=float(prefix[-1].load_scale),
        source_reproduction_max_error=source_error,
        standardized_reconstruction_max_error=float(
            np.max(np.abs(decoded_standardized - standardized))
        ),
        raw_reconstruction_max_error=float(np.max(np.abs(decoded_raw - raw))),
        metrics=metrics,
    )


def build_ieee_projection_fidelity_analysis(
    development_campaign: IEEEGeometryCampaign,
    evaluation_campaign: IEEEGeometryCampaign,
    *,
    protocol_id: str = "ieee-projection-fidelity-v1",
    random_seed: int = 8208,
) -> IEEEProjectionFidelityAnalysis:
    """Fit IEEE-9 once and return the bounded IEEE-9/14 sidecar analysis."""

    if evaluation_campaign.case_role != "locked_evaluation":
        raise IEEEProjectionFidelityError("evaluation requires locked_evaluation role")
    model = fit_ieee_projection_fidelity_model(
        development_campaign,
        protocol_id=protocol_id,
        random_seed=random_seed,
    )
    development = analyze_ieee_projection_fidelity_case(development_campaign, model)
    evaluation = analyze_ieee_projection_fidelity_case(evaluation_campaign, model)
    dev_z = _standardized_matrix(development_campaign, model)
    counterfactual = dev_z[: min(8, len(dev_z))].copy()
    amplitudes = np.linspace(0.1, 0.8, len(counterfactual))
    shifted = counterfactual.copy()
    shifted[:, 6] += amplitudes
    shifted[:, 7] -= amplitudes
    q_distance = float(
        np.max(np.linalg.norm(_q_only(counterfactual) - _q_only(shifted), axis=1))
    )
    qr_detection = float(
        np.mean(
            np.linalg.norm(_q_plus_r(counterfactual) - _q_plus_r(shifted), axis=1)
            > TOLERANCE
        )
    )
    q_plus_metrics = (
        next(item for item in development.metrics if item.representation == "Q_PLUS_R8"),
        next(item for item in evaluation.metrics if item.representation == "Q_PLUS_R8"),
    )
    source_error = max(
        development.source_reproduction_max_error,
        evaluation.source_reproduction_max_error,
    )
    standardized_error = max(
        development.standardized_reconstruction_max_error,
        evaluation.standardized_reconstruction_max_error,
    )
    raw_error = max(
        development.raw_reconstruction_max_error,
        evaluation.raw_reconstruction_max_error,
    )
    distance_error = max(item.pair_distance_max_abs_error for item in q_plus_metrics)
    passed = (
        source_error < TOLERANCE
        and standardized_error < TOLERANCE
        and raw_error < TOLERANCE
        and distance_error < TOLERANCE
        and q_distance < TOLERANCE
        and qr_detection == 1.0
    )
    return IEEEProjectionFidelityAnalysis(
        protocol_id=protocol_id,
        model=model,
        development=development,
        evaluation=evaluation,
        source_reproduction_max_error=source_error,
        q_plus_r_standardized_reconstruction_max_error=standardized_error,
        q_plus_r_raw_reconstruction_max_error=raw_error,
        q_plus_r_pair_distance_max_error=distance_error,
        q_only_kernel_max_distance=q_distance,
        q_plus_r_kernel_detection_rate=qr_detection,
        evaluation_refit=False,
        status="PASS" if passed else "FAIL",
        decision=(
            "IEEE_PROJECTION_FIDELITY_CONFIRMED"
            if passed
            else "STOP_PROJECTION_FIDELITY_GATE_FAILED"
        ),
        nonclaims=(
            "no stability prediction or early warning",
            "no risk, causal, or control claim",
            "no physical AXIS08 identity",
            "no universal compression superiority",
            "Q_PLUS_R8 stores eight scalars and is not compression",
        ),
    )


def _campaign_matrix(
    campaign: IEEEGeometryCampaign,
) -> tuple[FloatArray, float, tuple[IEEEGeometryFrame, ...]]:
    prefix: list[IEEEGeometryFrame] = []
    for frame in campaign.frames:
        if frame.status is IEEEFrameStatus.FAILED:
            break
        prefix.append(frame)
    if len(prefix) < 3:
        raise IEEEProjectionFidelityError("campaign requires three converged prefix frames")
    rows, errors = zip(*(_derived_row(frame) for frame in prefix))
    return np.asarray(rows, dtype=np.float64), max(errors), tuple(prefix)


def _derived_row(frame: IEEEGeometryFrame) -> tuple[tuple[float, ...], float]:
    if frame.system_features is None:
        raise IEEEProjectionFidelityError("converged frame lacks system features")
    maintained = dict(
        zip(frame.system_features.feature_names, frame.system_features.values)
    )
    try:
        bus = next(view for view in frame.entity_views if view.entity_scope == "bus")
        line = next(view for view in frame.entity_views if view.entity_scope == "line")
    except StopIteration as error:
        raise IEEEProjectionFidelityError("frame lacks bus or line entity view") from error
    bus_values = np.asarray(bus.values, dtype=np.float64)
    line_values = np.asarray(line.values, dtype=np.float64)
    vm = bus_values[:, bus.variable_names.index("vm_pu")]
    va = bus_values[:, bus.variable_names.index("va_degree")]
    active = bus_values[:, bus.variable_names.index("p_mw")]
    reactive = bus_values[:, bus.variable_names.index("q_mvar")]
    loading = line_values[:, line.variable_names.index("loading_percent")]
    derived = {
        "minimum_bus_voltage": float(np.min(vm)),
        "mean_bus_voltage": float(np.mean(vm)),
        "bus_voltage_std": float(np.std(vm)),
        "bus_angle_range": float(np.max(va) - np.min(va)),
        "maximum_line_loading": float(np.max(loading)),
        "total_bus_consumption_p": float(np.sum(active[active > 0.0])),
        "total_bus_consumption_q": float(np.sum(reactive[reactive > 0.0])),
    }
    missing = set(derived) - set(maintained)
    if missing:
        raise IEEEProjectionFidelityError(
            "system summary lacks required features: " + ", ".join(sorted(missing))
        )
    error = max(abs(derived[name] - maintained[name]) for name in derived)
    row = (
        maintained["mean_bus_voltage"],
        maintained["bus_voltage_std"],
        maintained["bus_angle_range"],
        maintained["maximum_line_loading"],
        maintained["total_bus_consumption_p"],
        maintained["total_bus_consumption_q"],
        maintained["minimum_bus_voltage"],
        float(np.max(vm)),
    )
    return row, float(error)


def _fit_standardization(values: FloatArray) -> tuple[FloatArray, FloatArray]:
    means = values.mean(axis=0)
    stddevs = values.std(axis=0)
    if np.any(stddevs <= 0.0):
        raise IEEEProjectionFidelityError("development features contain zero variance")
    return means, stddevs


def _standardized_matrix(
    campaign: IEEEGeometryCampaign,
    model: IEEEProjectionFidelityModel,
) -> FloatArray:
    raw, _, _ = _campaign_matrix(campaign)
    return (raw - np.asarray(model.means)) / np.asarray(model.population_stddevs)


def _maintained_raw(raw: FloatArray) -> FloatArray:
    return np.column_stack([raw[:, 6], raw[:, :6]])


def _q_only(values: FloatArray) -> FloatArray:
    return np.column_stack([values[:, :6], (values[:, 6] + values[:, 7]) / SQRT2])


def _q_plus_r(values: FloatArray) -> FloatArray:
    return np.column_stack(
        [_q_only(values), (values[:, 6] - values[:, 7]) / SQRT2]
    )


def _qr_decode(values: FloatArray) -> FloatArray:
    quotient, residual = values[:, 6], values[:, 7]
    return np.column_stack(
        [
            values[:, :6],
            (quotient + residual) / SQRT2,
            (quotient - residual) / SQRT2,
        ]
    )


def _representations(
    standardized: FloatArray,
    raw: FloatArray,
    model: IEEEProjectionFidelityModel,
) -> dict[str, FloatArray]:
    maintained = _maintained_raw(raw)
    return {
        "FULL8": standardized,
        "Q_ONLY7": _q_only(standardized),
        "Q_PLUS_R8": _q_plus_r(standardized),
        "PCA7": standardized @ np.asarray(model.pca_basis),
        "RANDOM7": standardized @ np.asarray(model.random_basis),
        "DROP_MIN7": standardized[:, (0, 1, 2, 3, 4, 5, 7)],
        "DROP_MAX7": standardized[:, :7],
        "MAINTAINED7": (
            maintained - np.asarray(model.maintained_means)
        ) / np.asarray(model.maintained_population_stddevs),
    }


def _fidelity_metrics(
    name: str,
    reference: FloatArray,
    candidate: FloatArray,
) -> IEEEProjectionFidelityMetrics:
    ref_pairs = _pairwise_distances(reference)
    candidate_pairs = _pairwise_distances(candidate)
    ref_adjacent = np.linalg.norm(np.diff(reference, axis=0), axis=1)
    candidate_adjacent = np.linalg.norm(np.diff(candidate, axis=0), axis=1)
    relative_adjacent = np.abs(candidate_adjacent - ref_adjacent) / np.maximum(
        ref_adjacent, 1e-30
    )
    ref_turns = _turns(reference)
    candidate_turns = _turns(candidate)
    correlation = np.corrcoef(ref_pairs, candidate_pairs)[0, 1]
    return IEEEProjectionFidelityMetrics(
        representation=name,
        stored_scalars=int(candidate.shape[1]),
        pair_distance_nrmse=float(
            np.sqrt(np.mean((candidate_pairs - ref_pairs) ** 2)) / np.mean(ref_pairs)
        ),
        pair_distance_correlation=float(correlation),
        adjacent_relative_error_median=float(np.median(relative_adjacent)),
        adjacent_relative_error_max=float(np.max(relative_adjacent)),
        path_length_relative_error=float(
            abs(np.sum(candidate_adjacent) - np.sum(ref_adjacent))
            / np.sum(ref_adjacent)
        ),
        turn_angle_mae_degrees=float(
            np.degrees(np.nanmean(np.abs(candidate_turns - ref_turns)))
        ),
        pair_distance_max_abs_error=float(
            np.max(np.abs(candidate_pairs - ref_pairs))
        ),
    )


def _pairwise_distances(values: FloatArray) -> FloatArray:
    delta = values[:, None, :] - values[None, :, :]
    matrix = np.sqrt(np.sum(delta * delta, axis=2))
    return matrix[np.triu_indices(len(values), 1)]


def _turns(values: FloatArray) -> FloatArray:
    result = []
    for index in range(1, len(values) - 1):
        left = values[index] - values[index - 1]
        right = values[index + 1] - values[index]
        denominator = np.linalg.norm(left) * np.linalg.norm(right)
        result.append(
            np.nan
            if denominator <= 0.0
            else np.arccos(np.clip(np.dot(left, right) / denominator, -1.0, 1.0))
        )
    return np.asarray(result, dtype=np.float64)


def _tuple(values: FloatArray) -> tuple[float, ...]:
    return tuple(float(value) for value in values)
