"""Baseline-anchored load branches and explicit convergence boundaries."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from collections.abc import Callable, Sequence

from nexah.orientation import Context, Provenance
from nexah.sources import IEEEPandapowerAdapter, IEEEPhysicalSnapshot


class BranchDirection(str, Enum):
    """Direction away from the native load point."""

    DOWNWARD = "downward"
    UPWARD = "upward"


@dataclass(frozen=True, slots=True)
class ContinuationPoint:
    """One honestly solved point on a load branch."""

    load_scale: float
    converged: bool
    metric: float | None
    failure: str | None

    def __post_init__(self) -> None:
        if not isfinite(self.load_scale) or self.load_scale <= 0.0:
            raise ValueError("load_scale must be finite and positive")
        if self.converged != (self.metric is not None):
            raise ValueError("only converged points may contain a metric")
        if self.converged == (self.failure is not None):
            raise ValueError("exactly failed points require a failure description")
        if self.metric is not None and not isfinite(self.metric):
            raise ValueError("metric must be finite")


@dataclass(frozen=True, slots=True)
class ContinuationBranch:
    """Ordered branch beginning at the native ``lambda = 1`` baseline."""

    case_id: str
    direction: BranchDirection
    points: tuple[ContinuationPoint, ...]

    def __post_init__(self) -> None:
        if not self.points:
            raise ValueError("continuation branch requires points")
        if self.points[0].load_scale != 1.0:
            raise ValueError("continuation branch must begin at lambda = 1.0")
        if not self.points[0].converged:
            raise ValueError("native baseline must converge")
        scales = tuple(point.load_scale for point in self.points)
        pairs = zip(scales, scales[1:])
        if self.direction is BranchDirection.UPWARD:
            valid = all(current > previous for previous, current in pairs)
        else:
            valid = all(current < previous for previous, current in pairs)
        if not valid:
            raise ValueError("branch scales must move strictly in its direction")
        failures = [index for index, point in enumerate(self.points) if not point.converged]
        if failures and failures != [len(self.points) - 1]:
            raise ValueError("a branch may contain only one terminal failure")

    @property
    def converged_points(self) -> tuple[ContinuationPoint, ...]:
        return tuple(point for point in self.points if point.converged)

    @property
    def last_converged_scale(self) -> float:
        return self.converged_points[-1].load_scale

    @property
    def first_failed_scale(self) -> float | None:
        final = self.points[-1]
        return None if final.converged else final.load_scale

    @property
    def boundary_status(self) -> str:
        return "bracketed" if self.first_failed_scale is not None else "right_censored"


@dataclass(frozen=True, slots=True)
class RefinedBoundary:
    """Explicit interval between the last converged and first failed point."""

    direction: BranchDirection
    last_converged_scale: float
    first_failed_scale: float
    tolerance: float
    evaluations: tuple[ContinuationPoint, ...]

    def __post_init__(self) -> None:
        if self.direction is BranchDirection.UPWARD:
            width = self.first_failed_scale - self.last_converged_scale
        else:
            width = self.last_converged_scale - self.first_failed_scale
        if width <= 0.0 or width > self.tolerance:
            raise ValueError("refined boundary must be ordered within tolerance")

    @property
    def interval_width(self) -> float:
        return abs(self.first_failed_scale - self.last_converged_scale)


Metric = Callable[[IEEEPhysicalSnapshot], float]


def scan_branch(
    adapter: IEEEPandapowerAdapter,
    load_scales: Sequence[float],
    *,
    direction: BranchDirection,
    campaign_id: str,
    provenance: Provenance,
    context: Context,
    metric: Metric,
) -> ContinuationBranch:
    """Evaluate independent physical points, stopping at the first failure.

    This is parameter continuation, not a continuation-power-flow algorithm:
    every point starts from the declared standard case so numerical state is not
    silently carried between samples.
    """

    scales = tuple(float(value) for value in load_scales)
    _validate_scales(scales, direction)
    points: list[ContinuationPoint] = []
    for index, load_scale in enumerate(scales):
        snapshot = adapter.run_snapshot(
            load_scale,
            scenario_id=f"{campaign_id}:{direction.value}-{index:03d}",
            provenance=provenance,
            context=context,
        )
        points.append(_point(snapshot, metric))
        if not snapshot.converged:
            break
    return ContinuationBranch(
        case_id=adapter.case_id,
        direction=direction,
        points=tuple(points),
    )


def refine_boundary(
    adapter: IEEEPandapowerAdapter,
    branch: ContinuationBranch,
    *,
    tolerance: float,
    maximum_evaluations: int,
    campaign_id: str,
    provenance: Provenance,
    context: Context,
    metric: Metric,
) -> RefinedBoundary:
    """Bisect a bracketed convergence boundary without inventing outcomes."""

    if branch.first_failed_scale is None:
        raise ValueError("boundary refinement requires a bracketed branch")
    if not isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("tolerance must be finite and positive")
    if maximum_evaluations < 1:
        raise ValueError("maximum_evaluations must be positive")
    converged = branch.last_converged_scale
    failed = branch.first_failed_scale
    evaluations: list[ContinuationPoint] = []
    for index in range(maximum_evaluations):
        if abs(failed - converged) <= tolerance:
            break
        midpoint = (converged + failed) / 2.0
        snapshot = adapter.run_snapshot(
            midpoint,
            scenario_id=f"{campaign_id}:refine-{index:03d}",
            provenance=provenance,
            context=context,
        )
        point = _point(snapshot, metric)
        evaluations.append(point)
        if point.converged:
            converged = midpoint
        else:
            failed = midpoint
    if abs(failed - converged) > tolerance:
        raise ValueError("maximum evaluations did not resolve boundary tolerance")
    return RefinedBoundary(
        direction=branch.direction,
        last_converged_scale=converged,
        first_failed_scale=failed,
        tolerance=tolerance,
        evaluations=tuple(evaluations),
    )


def _validate_scales(
    scales: tuple[float, ...], direction: BranchDirection
) -> None:
    if len(scales) < 2:
        raise ValueError("continuation branch requires at least two scales")
    if scales[0] != 1.0:
        raise ValueError("continuation branch must start at lambda = 1.0")
    if any(not isfinite(value) or value <= 0.0 for value in scales):
        raise ValueError("load scales must be finite and positive")
    pairs = zip(scales, scales[1:])
    if direction is BranchDirection.UPWARD:
        valid = all(current > previous for previous, current in pairs)
    else:
        valid = all(current < previous for previous, current in pairs)
    if not valid:
        raise ValueError("load scales must move strictly in branch direction")


def _point(snapshot: IEEEPhysicalSnapshot, metric: Metric) -> ContinuationPoint:
    if snapshot.converged:
        return ContinuationPoint(
            load_scale=snapshot.load_scale,
            converged=True,
            metric=float(metric(snapshot)),
            failure=None,
        )
    return ContinuationPoint(
        load_scale=snapshot.load_scale,
        converged=False,
        metric=None,
        failure=snapshot.failure,
    )
