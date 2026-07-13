"""Reconstruct the historical IEEE curvature pattern from physical outputs."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
from typing import Any, Sequence, TypedDict

import numpy as np
from numpy.typing import NDArray

from nexah.orientation import Context, Provenance
from nexah.sources import IEEEPandapowerAdapter, IEEEPhysicalSnapshot


DEFAULT_OUTPUT_DIR = Path("outputs/ieee_scaling_pattern_v1")
DEFAULT_CASES = (
    "ieee9",
    "ieee14",
    "ieee30",
    "ieee57",
    "ieee118",
    "ieee300",
    "pegase1354",
    "pegase9241",
)
DEFAULT_LOAD_SCALES = tuple(float(value) for value in np.linspace(0.6, 5.0, 200))
FloatArray = NDArray[np.float64]


class ScanRow(TypedDict):
    load_scale: float
    converged: bool
    c_struct: float | None


def run_validation(
    *,
    recorded_at: datetime,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    case_ids: Sequence[str] = DEFAULT_CASES,
    load_scales: Sequence[float] = DEFAULT_LOAD_SCALES,
    write_outputs: bool = True,
) -> dict[str, Any]:
    if recorded_at.tzinfo is None:
        raise ValueError("recorded_at must include a timezone")
    cases = [
        _evaluate_case(
            case_id=case_id,
            load_scales=load_scales,
            recorded_at=recorded_at,
        )
        for case_id in case_ids
    ]
    observed = [
        case
        for case in cases
        if case["boundary_status"] == "observed_after_converged_prefix"
    ]
    historical_leads = [
        float(case["historical_lead"])
        for case in observed
        if case["historical_lead"] is not None
    ]
    interior_leads = [
        float(case["interior_lead"])
        for case in observed
        if case["interior_lead"] is not None
    ]
    result = {
        "validation_id": "ieee-scaling-pattern-v1",
        "frozen_design": {
            "case_roles": {
                **{case_id: "historical_reference" for case_id in case_ids[:3]},
                **{case_id: "extension" for case_id in case_ids[3:6]},
                **{case_id: "held_out_scale" for case_id in case_ids[6:]},
            },
            "load_scales": [float(value) for value in load_scales],
            "metric": "std(theta_rad)*std(clip(1-vm_pu,-1,1))*mean(normalized_loop_signal)",
            "derivative": "numpy.gradient twice over load scale",
            "peak": "maximum signed second derivative",
            "interior_edge_exclusion": 2,
            "resolution_sensitivity": "every second dense sample",
            "maximum_load_scale": float(load_scales[-1]),
            "stop_after_first_nonconvergence": True,
            "fabricated_failed_physics": False,
            "parameters_tuned_on_results": False,
        },
        "cases": cases,
        "aggregate": {
            "cases": len(cases),
            "boundaries_after_converged_prefix": len(observed),
            "lower_scan_bound_nonconvergence": sum(
                case["boundary_status"] == "lower_bound_nonconverged"
                for case in cases
            ),
            "right_censored": sum(
                case["boundary_status"] == "right_censored" for case in cases
            ),
            "interior_peaks_at_exclusion_boundary": sum(
                bool(case["interior_peak_at_exclusion_boundary"])
                for case in observed
            ),
            "historical_positive_leads": sum(value > 0.0 for value in historical_leads),
            "interior_positive_leads": sum(value > 0.0 for value in interior_leads),
            "historical_lead_mean": _mean_or_none(historical_leads),
            "historical_lead_cv": _cv_or_none(historical_leads),
            "interior_lead_mean": _mean_or_none(interior_leads),
            "interior_lead_cv": _cv_or_none(interior_leads),
        },
        "interpretation": (
            "Physical reconstruction of a historical curvature hypothesis; "
            "not an early-warning, causal, or control validation."
        ),
    }
    if write_outputs:
        _write_outputs(result, output_dir)
    return result


def _evaluate_case(
    *,
    case_id: str,
    load_scales: Sequence[float],
    recorded_at: datetime,
) -> dict[str, Any]:
    adapter = IEEEPandapowerAdapter(case_id=case_id)
    provenance = Provenance(
        source=f"pandapower:{case_id}",
        method="dense physical load scan",
        recorded_at=recorded_at,
        record_id=f"ieee-scaling-pattern-v1:{case_id}",
    )
    rows: list[ScanRow] = []
    first_failure: float | None = None
    for snapshot in adapter.iter_snapshots(
        load_scales,
        campaign_id=f"ieee-scaling-pattern-v1-{case_id}",
        provenance=provenance,
        context=Context(domain="power-system", values={"benchmark_case": case_id}),
    ):
        if not snapshot.converged:
            if first_failure is None:
                first_failure = snapshot.load_scale
            rows.append(
                {
                    "load_scale": snapshot.load_scale,
                    "converged": False,
                    "c_struct": None,
                }
            )
            break
        rows.append(
            {
                "load_scale": snapshot.load_scale,
                "converged": True,
                "c_struct": historical_c_struct(snapshot),
            }
        )

    prefix: list[ScanRow] = []
    for row in rows:
        if not row["converged"]:
            continue
        if first_failure is not None and row["load_scale"] >= first_failure:
            continue
        if row["c_struct"] is None:
            raise ValueError("converged scan row lacks c_struct")
        prefix.append(row)
    load = np.asarray([row["load_scale"] for row in prefix], dtype=np.float64)
    values = np.asarray([row["c_struct"] for row in prefix], dtype=np.float64)
    derivatives = _derivatives(load, values) if len(load) >= 5 else None
    historical_peak = _peak(load, derivatives, edge=0) if derivatives is not None else None
    interior_peak = _peak(load, derivatives, edge=2) if derivatives is not None else None
    down_load = load[::2]
    down_values = values[::2]
    down_derivatives = (
        _derivatives(down_load, down_values) if len(down_load) >= 5 else None
    )
    down_peak = (
        _peak(down_load, down_derivatives, edge=2)
        if down_derivatives is not None
        else None
    )
    interior_offset = (
        len(load) - 1 - int(np.argmin(np.abs(load - interior_peak)))
        if interior_peak is not None
        else None
    )
    if first_failure is None:
        boundary_status = "right_censored"
    elif not prefix:
        boundary_status = "lower_bound_nonconverged"
    else:
        boundary_status = "observed_after_converged_prefix"
    return {
        "case_id": case_id,
        "planned_samples": len(load_scales),
        "attempted_samples": len(rows),
        "converged_samples": sum(bool(row["converged"]) for row in rows),
        "collapse_load_scale": first_failure,
        "boundary_status": boundary_status,
        "curvature_status": "estimated"
        if derivatives is not None
        else "insufficient_converged_samples",
        "historical_peak_load_scale": historical_peak,
        "historical_lead": _lead(first_failure, historical_peak),
        "interior_peak_load_scale": interior_peak,
        "interior_lead": _lead(first_failure, interior_peak),
        "interior_peak_offset_from_last_converged_sample": interior_offset,
        "interior_peak_at_exclusion_boundary": interior_offset == 2,
        "downsampled_interior_peak_load_scale": down_peak,
        "downsampled_interior_lead": _lead(first_failure, down_peak),
        "resolution_peak_shift": abs(interior_peak - down_peak)
        if interior_peak is not None and down_peak is not None
        else None,
        "curve": rows,
    }


def historical_c_struct(snapshot: IEEEPhysicalSnapshot) -> float:
    """Exact V32 metric from converged, non-fabricated physical arrays."""

    if snapshot.bus_batch is None or snapshot.line_batch is None:
        raise ValueError("historical metric requires a converged snapshot")
    bus_names = [feature.name for feature in snapshot.bus_batch.features]
    line_names = [feature.name for feature in snapshot.line_batch.features]
    buses = snapshot.bus_batch.to_numpy()
    lines = snapshot.line_batch.to_numpy()
    voltage = buses[:, bus_names.index("vm_pu")]
    theta = np.deg2rad(buses[:, bus_names.index("va_degree")])
    p_flow = lines[:, line_names.index("p_from_mw")]
    theta_by_bus = {
        int(row_id.split(":", 1)[1]): float(theta[index])
        for index, row_id in enumerate(snapshot.bus_batch.row_ids)
    }
    loop_signal = {bus_id: 0.0 for bus_id in theta_by_bus}
    for index, row_id in enumerate(snapshot.line_batch.row_ids):
        endpoints = row_id.rsplit(":", 1)[1]
        from_bus_text, to_bus_text = endpoints.split("-", 1)
        from_bus = int(from_bus_text)
        to_bus = int(to_bus_text)
        value = np.sqrt(abs(theta_by_bus[from_bus] - theta_by_bus[to_bus])) * abs(
            p_flow[index]
        )
        loop_signal[from_bus] += float(value)
        loop_signal[to_bus] += float(value)
    loop_values = np.asarray(list(loop_signal.values()), dtype=np.float64)
    maximum = float(np.max(loop_values)) if len(loop_values) else 0.0
    if maximum > 0.0:
        loop_values = loop_values / maximum
    field_intensity = np.clip(1.0 - voltage, -1.0, 1.0)
    return float(np.std(theta) * np.std(field_intensity) * np.mean(loop_values))


def _derivatives(load: FloatArray, values: FloatArray) -> FloatArray:
    if len(load) < 5:
        raise ValueError("curvature reconstruction requires at least five samples")
    first = np.gradient(values, load)
    return np.asarray(np.gradient(first, load), dtype=np.float64)


def _peak(load: FloatArray, curvature: FloatArray, *, edge: int) -> float | None:
    if len(load) <= 2 * edge:
        return None
    candidates = curvature[edge : len(curvature) - edge if edge else None]
    if len(candidates) == 0:
        return None
    index = int(np.argmax(candidates)) + edge
    return float(load[index])


def _lead(collapse: float | None, peak: float | None) -> float | None:
    if collapse is None or peak is None:
        return None
    return float(collapse - peak)


def _mean_or_none(values: list[float]) -> float | None:
    return float(np.mean(values)) if values else None


def _cv_or_none(values: list[float]) -> float | None:
    if not values:
        return None
    mean = float(np.mean(values))
    return float(np.std(values) / abs(mean)) if mean != 0.0 else None


def _write_outputs(result: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "validation_result.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    aggregate = result["aggregate"]
    summary = f"""# IEEE Scaling Pattern Validation V1

| Metric | Result |
|---|---:|
| Cases | {aggregate['cases']} |
| Boundaries after converged prefix | {aggregate['boundaries_after_converged_prefix']} |
| Lower-bound nonconvergence | {aggregate['lower_scan_bound_nonconvergence']} |
| Right-censored | {aggregate['right_censored']} |
| Interior peaks at exclusion boundary | {aggregate['interior_peaks_at_exclusion_boundary']} |
| Historical positive leads | {aggregate['historical_positive_leads']} |
| Interior positive leads | {aggregate['interior_positive_leads']} |
| Historical lead mean | {aggregate['historical_lead_mean']} |
| Historical lead CV | {aggregate['historical_lead_cv']} |
| Interior lead mean | {aggregate['interior_lead_mean']} |
| Interior lead CV | {aggregate['interior_lead_cv']} |

Physical curvature reconstruction; not early-warning or causal validation.
"""
    (output_dir / "validation_summary.md").write_text(summary, encoding="utf-8")


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
