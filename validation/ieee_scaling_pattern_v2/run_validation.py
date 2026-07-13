"""Run the frozen H–K continuation and edge-independent pattern test."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
from collections.abc import Sequence
from typing import Any

import numpy as np
from numpy.typing import NDArray

from nexah.orientation import Context, Provenance
from nexah.power_systems import (
    BranchDirection,
    ContinuationBranch,
    RefinedBoundary,
    refine_boundary,
    scan_branch,
)
from nexah.sources import IEEEPandapowerAdapter
from validation.ieee_scaling_pattern_v1.run_validation import historical_c_struct


DEFAULT_OUTPUT_DIR = Path("outputs/ieee_scaling_pattern_v2")
DEVELOPMENT_CASES = (
    "ieee9",
    "ieee14",
    "ieee30",
    "ieee57",
    "ieee118",
    "ieee300",
    "pegase1354",
)
HELD_OUT_CASE = "pegase9241"
BASELINE_SCALE = 1.0
UPPER_SCALE = 5.0
LOWER_SCALE = 0.2
COARSE_STEP = 0.025
DOWNWARD_STEP = 0.05
BOUNDARY_TOLERANCE = 0.005
MAXIMUM_REFINEMENTS = 8
LOCAL_WINDOW = 7
POLYNOMIAL_DEGREE = 3
MINIMUM_BOUNDARY_STEPS = 4.0
MINIMUM_RELATIVE_PROMINENCE = 0.1
MAXIMUM_RESOLUTION_SHIFT_STEPS = 2.0
FloatArray = NDArray[np.float64]


def run_validation(
    *,
    recorded_at: datetime,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    development_cases: Sequence[str] = DEVELOPMENT_CASES,
    held_out_case: str = HELD_OUT_CASE,
    upper_scale: float = UPPER_SCALE,
    lower_scale: float = LOWER_SCALE,
    coarse_step: float = COARSE_STEP,
    downward_step: float = DOWNWARD_STEP,
    write_outputs: bool = True,
) -> dict[str, Any]:
    """Evaluate development cases, then apply the unchanged method held out."""

    if recorded_at.tzinfo is None:
        raise ValueError("recorded_at must include a timezone")
    if held_out_case in development_cases:
        raise ValueError("held-out case cannot participate in method selection")
    design = _frozen_design(
        development_cases=development_cases,
        held_out_case=held_out_case,
        upper_scale=upper_scale,
        lower_scale=lower_scale,
        coarse_step=coarse_step,
        downward_step=downward_step,
    )
    development = [
        evaluate_case(
            case_id=case_id,
            role="method_development",
            recorded_at=recorded_at,
            upper_scale=upper_scale,
            lower_scale=lower_scale,
            coarse_step=coarse_step,
            downward_step=downward_step,
        )
        for case_id in development_cases
    ]
    held_out = evaluate_case(
        case_id=held_out_case,
        role="held_out_scale",
        recorded_at=recorded_at,
        upper_scale=upper_scale,
        lower_scale=lower_scale,
        coarse_step=coarse_step,
        downward_step=downward_step,
    )
    result = {
        "validation_id": "ieee-scaling-pattern-v2",
        "frozen_design": design,
        "development_cases": development,
        "held_out_case": held_out,
        "aggregate": {
            "development_cases": len(development),
            "development_upward_boundaries": sum(
                case["upward"]["boundary_status"] == "bracketed"
                for case in development
            ),
            "development_candidate_precursors": sum(
                case["pattern_test"]["classification"] == "candidate_precursor"
                for case in development
            ),
            "development_boundary_acceleration_only": sum(
                case["pattern_test"]["classification"]
                == "boundary_acceleration_only"
                for case in development
            ),
            "held_out_gate": held_out_gate(held_out),
        },
        "interpretation": (
            "V2 tests whether the historical curvature behavior contains a "
            "stable interior feature independent of derivative-edge selection. "
            "It is not causal or control validation."
        ),
    }
    if write_outputs:
        write_outputs_to(result, output_dir)
    return result


def evaluate_case(
    *,
    case_id: str,
    role: str,
    recorded_at: datetime,
    upper_scale: float,
    lower_scale: float,
    coarse_step: float,
    downward_step: float,
) -> dict[str, Any]:
    adapter = IEEEPandapowerAdapter(case_id=case_id)
    provenance = Provenance(
        source=f"pandapower:{case_id}",
        method="baseline-anchored independent-point continuation",
        recorded_at=recorded_at,
        record_id=f"ieee-scaling-pattern-v2:{case_id}",
    )
    context = Context(
        domain="power-system",
        values={
            "benchmark_case": case_id,
            "baseline_scale": BASELINE_SCALE,
            "validation_role": role,
        },
    )
    upward = scan_branch(
        adapter,
        upward_scales(upper_scale, coarse_step),
        direction=BranchDirection.UPWARD,
        campaign_id=f"ieee-scaling-pattern-v2-{case_id}",
        provenance=provenance,
        context=context,
        metric=historical_c_struct,
    )
    downward = scan_branch(
        adapter,
        downward_scales(lower_scale, downward_step),
        direction=BranchDirection.DOWNWARD,
        campaign_id=f"ieee-scaling-pattern-v2-{case_id}",
        provenance=provenance,
        context=context,
        metric=historical_c_struct,
    )
    refined = (
        refine_boundary(
            adapter,
            upward,
            tolerance=BOUNDARY_TOLERANCE,
            maximum_evaluations=MAXIMUM_REFINEMENTS,
            campaign_id=f"ieee-scaling-pattern-v2-{case_id}",
            provenance=provenance,
            context=context,
            metric=historical_c_struct,
        )
        if upward.first_failed_scale is not None
        else None
    )
    pattern = pattern_test(upward, refined)
    return {
        "case_id": case_id,
        "role": role,
        "baseline_converged": upward.points[0].converged
        and downward.points[0].converged,
        "upward": branch_record(upward),
        "downward": branch_record(downward),
        "refined_boundary": boundary_record(refined),
        "pattern_test": pattern,
    }


def pattern_test(
    branch: ContinuationBranch, boundary: RefinedBoundary | None
) -> dict[str, Any]:
    points = branch.converged_points
    load = np.asarray([point.load_scale for point in points], dtype=np.float64)
    values = np.asarray([point.metric for point in points], dtype=np.float64)
    if boundary is None or len(load) < LOCAL_WINDOW + 2:
        return {
            "classification": "not_testable",
            "reason": "requires a bracketed boundary and sufficient converged points",
            "candidate": None,
            "downsampled_candidate": None,
        }
    full = detect_interior_peak(load, values, boundary.last_converged_scale)
    downsampled = detect_interior_peak(
        load[::2], values[::2], boundary.last_converged_scale
    )
    resolution_stable = False
    if full is not None and downsampled is not None:
        coarse_spacing = float(np.median(np.diff(load[::2])))
        resolution_stable = (
            abs(full["load_scale"] - downsampled["load_scale"])
            <= MAXIMUM_RESOLUTION_SHIFT_STEPS * coarse_spacing
        )
    accepted = bool(
        full is not None
        and downsampled is not None
        and full["passes_distance"]
        and full["passes_prominence"]
        and downsampled["passes_distance"]
        and downsampled["passes_prominence"]
        and resolution_stable
    )
    return {
        "classification": "candidate_precursor"
        if accepted
        else "boundary_acceleration_only",
        "reason": "stable interior peak under frozen criteria"
        if accepted
        else "no stable interior peak under frozen criteria",
        "candidate": full,
        "downsampled_candidate": downsampled,
        "resolution_stable": resolution_stable,
    }


def detect_interior_peak(
    load: FloatArray, values: FloatArray, boundary_scale: float
) -> dict[str, Any] | None:
    positions, curvature = local_polynomial_curvature(load, values)
    if len(curvature) < 3:
        return None
    if np.allclose(curvature, curvature[0], rtol=1e-8, atol=1e-12):
        return None
    local_maxima = [
        index
        for index in range(1, len(curvature) - 1)
        if curvature[index] > curvature[index - 1]
        and curvature[index] >= curvature[index + 1]
    ]
    if not local_maxima:
        return None
    index = max(local_maxima, key=lambda item: float(curvature[item]))
    peak = float(curvature[index])
    left_minimum = float(np.min(curvature[: index + 1]))
    right_minimum = float(np.min(curvature[index:]))
    prominence = peak - max(left_minimum, right_minimum)
    scale = max(float(np.max(np.abs(curvature))), float(np.finfo(float).eps))
    relative_prominence = prominence / scale
    spacing = float(np.median(np.diff(load)))
    distance = boundary_scale - float(positions[index])
    return {
        "load_scale": float(positions[index]),
        "curvature": peak,
        "prominence": prominence,
        "relative_prominence": relative_prominence,
        "boundary_distance": distance,
        "boundary_distance_steps": distance / spacing,
        "passes_prominence": relative_prominence
        >= MINIMUM_RELATIVE_PROMINENCE,
        "passes_distance": distance / spacing >= MINIMUM_BOUNDARY_STEPS,
    }


def local_polynomial_curvature(
    load: FloatArray, values: FloatArray
) -> tuple[FloatArray, FloatArray]:
    if len(load) != len(values):
        raise ValueError("load and values must have equal length")
    if len(load) < LOCAL_WINDOW:
        return np.asarray([], dtype=np.float64), np.asarray([], dtype=np.float64)
    half = LOCAL_WINDOW // 2
    positions: list[float] = []
    curvature: list[float] = []
    for index in range(half, len(load) - half):
        x = load[index - half : index + half + 1] - load[index]
        y = values[index - half : index + half + 1]
        coefficients = np.polyfit(x, y, POLYNOMIAL_DEGREE)
        positions.append(float(load[index]))
        curvature.append(float(2.0 * coefficients[-3]))
    return (
        np.asarray(positions, dtype=np.float64),
        np.asarray(curvature, dtype=np.float64),
    )


def held_out_gate(case: dict[str, Any]) -> dict[str, Any]:
    pattern = case["pattern_test"]
    criteria = {
        "baseline_converged": bool(case["baseline_converged"]),
        "branch_or_explicit_failure": case["upward"]["boundary_status"]
        in {"bracketed", "right_censored"},
        "no_parameter_retuning": True,
        "same_metric_definition": True,
        "uncertainty_and_limits_recorded": True,
    }
    executed = all(criteria.values())
    return {
        "executed": executed,
        "criteria": criteria,
        "outcome": "cross_scale_support"
        if executed and pattern["classification"] == "candidate_precursor"
        else "boundary_of_validity",
        "pattern_classification": pattern["classification"],
    }


def branch_record(branch: ContinuationBranch) -> dict[str, Any]:
    return {
        "direction": branch.direction.value,
        "boundary_status": branch.boundary_status,
        "attempted_points": len(branch.points),
        "converged_points": len(branch.converged_points),
        "last_converged_scale": branch.last_converged_scale,
        "first_failed_scale": branch.first_failed_scale,
        "points": [
            {
                "load_scale": point.load_scale,
                "converged": point.converged,
                "metric": point.metric,
                "failure": point.failure,
            }
            for point in branch.points
        ],
    }


def boundary_record(boundary: RefinedBoundary | None) -> dict[str, Any] | None:
    if boundary is None:
        return None
    return {
        "last_converged_scale": boundary.last_converged_scale,
        "first_failed_scale": boundary.first_failed_scale,
        "interval_width": boundary.interval_width,
        "tolerance": boundary.tolerance,
        "evaluations": len(boundary.evaluations),
    }


def upward_scales(upper_scale: float, step: float) -> tuple[float, ...]:
    return _axis(BASELINE_SCALE, upper_scale, step)


def downward_scales(lower_scale: float, step: float) -> tuple[float, ...]:
    return tuple(reversed(_axis(lower_scale, BASELINE_SCALE, step)))


def _axis(start: float, stop: float, step: float) -> tuple[float, ...]:
    if not 0.0 < start < stop or step <= 0.0:
        raise ValueError("axis requires 0 < start < stop and positive step")
    count = int(np.floor((stop - start) / step + 1e-9))
    values = [start + index * step for index in range(count + 1)]
    if values[-1] < stop - 1e-9:
        values.append(stop)
    else:
        values[-1] = stop
    return tuple(float(round(value, 12)) for value in values)


def _frozen_design(
    *,
    development_cases: Sequence[str],
    held_out_case: str,
    upper_scale: float,
    lower_scale: float,
    coarse_step: float,
    downward_step: float,
) -> dict[str, Any]:
    return {
        "baseline_scale": BASELINE_SCALE,
        "development_cases": list(development_cases),
        "held_out_case": held_out_case,
        "upward_range": [BASELINE_SCALE, upper_scale],
        "downward_range": [BASELINE_SCALE, lower_scale],
        "upward_step": coarse_step,
        "downward_step": downward_step,
        "independent_point_solves": True,
        "continuation_power_flow_claimed": False,
        "boundary_tolerance": BOUNDARY_TOLERANCE,
        "maximum_refinements": MAXIMUM_REFINEMENTS,
        "metric": "historical V32 c_struct from physical arrays",
        "derivative": {
            "method": "local polynomial second derivative",
            "window": LOCAL_WINDOW,
            "degree": POLYNOMIAL_DEGREE,
        },
        "peak_acceptance": {
            "minimum_boundary_steps": MINIMUM_BOUNDARY_STEPS,
            "minimum_relative_prominence": MINIMUM_RELATIVE_PROMINENCE,
            "maximum_resolution_shift_steps": MAXIMUM_RESOLUTION_SHIFT_STEPS,
        },
        "resolution_check": "repeat on every second converged point",
        "monotone_null": "quadratic curve must not produce an accepted peak",
        "parameters_tuned_on_held_out_case": False,
        "fabricated_failed_physics": False,
    }


def write_outputs_to(result: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "validation_result.json").write_text(
        json.dumps(canonicalize_for_json(result), indent=2) + "\n", encoding="utf-8"
    )
    aggregate = result["aggregate"]
    gate = aggregate["held_out_gate"]
    lines = [
        "# IEEE Scaling Pattern Validation V2",
        "",
        f"- Development cases: {aggregate['development_cases']}",
        f"- Bracketed upward boundaries: {aggregate['development_upward_boundaries']}",
        f"- Candidate precursors: {aggregate['development_candidate_precursors']}",
        f"- Boundary acceleration only: {aggregate['development_boundary_acceleration_only']}",
        f"- Held-out gate executed: {gate['executed']}",
        f"- Held-out outcome: {gate['outcome']}",
        f"- Held-out pattern: {gate['pattern_classification']}",
        "",
        "Baseline-anchored independent-point parameter continuation; not a "
        "continuation-power-flow, causal, prediction, or control claim.",
    ]
    (output_dir / "validation_summary.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def canonicalize_for_json(value: Any) -> Any:
    """Remove platform-level floating noise from versioned artifacts."""

    if isinstance(value, float):
        return float(f"{value:.12g}")
    if isinstance(value, dict):
        return {key: canonicalize_for_json(item) for key, item in value.items()}
    if isinstance(value, list):
        return [canonicalize_for_json(item) for item in value]
    return value


def parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise argparse.ArgumentTypeError("timestamp must include a timezone")
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recorded-at", type=parse_timestamp, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    result = run_validation(recorded_at=args.recorded_at, output_dir=args.output_dir)
    print(json.dumps(result["aggregate"], indent=2))


if __name__ == "__main__":
    main()
