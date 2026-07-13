"""Run the frozen IEEE Orientation D–F validation."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from nexah.orientation import Context, Provenance
from nexah.power_systems import IEEEAttributionEvent, orient_ieee_campaign
from nexah.sources import IEEECoupledCampaign, IEEEPandapowerAdapter


DEFAULT_OUTPUT_DIR = Path("outputs/ieee_orientation_v1")
DEFAULT_CASES = ("ieee9", "ieee14")
DEFAULT_LOAD_SCALES = tuple(float(value) for value in np.linspace(0.6, 2.4, 19))


def run_validation(
    *,
    recorded_at: datetime,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    case_ids: Sequence[str] = DEFAULT_CASES,
    load_scales: Sequence[float] = DEFAULT_LOAD_SCALES,
    n_clusters: int = 4,
    window: int = 4,
    random_state: int = 42,
    alignment_tolerance: float = 0.1,
    write_outputs: bool = True,
) -> dict[str, Any]:
    if recorded_at.tzinfo is None:
        raise ValueError("recorded_at must include a timezone")
    if len(case_ids) < 1:
        raise ValueError("at least one IEEE case is required")
    results = [
        _evaluate_case(
            case_id=case_id,
            load_scales=load_scales,
            recorded_at=recorded_at,
            n_clusters=n_clusters,
            window=window,
            random_state=random_state,
            alignment_tolerance=alignment_tolerance,
        )
        for case_id in case_ids
    ]
    scored_references = sum(item["scored_physical_references"] for item in results)
    covered_references = sum(item["covered_physical_references"] for item in results)
    distances = [
        reference["nearest_event_distance"]
        for item in results
        for reference in item["physical_references"]
        if reference["nearest_event_distance"] is not None
    ]
    attribution_checks = sum(item["attribution_checks"] for item in results)
    attribution_matches = sum(item["attribution_matches"] for item in results)
    result = {
        "validation_id": "ieee-orientation-v1",
        "frozen_design": {
            "case_roles": {
                case_ids[0]: "reference",
                **{case_id: "held_out" for case_id in case_ids[1:]},
            },
            "load_scales": [float(value) for value in load_scales],
            "campaign_axis": "ordered_load_scale_not_time",
            "independent_steady_state_solutions": True,
            "v07_config": {
                "n_clusters": n_clusters,
                "window": window,
                "random_state": random_state,
            },
            "physical_thresholds": {
                "minimum_bus_voltage_below_pu": 0.95,
                "maximum_line_loading_at_least_percent": 100.0,
            },
            "alignment_tolerance_load_scale": alignment_tolerance,
            "nonconvergence_scored_as_numeric_event": False,
            "parameters_tuned_on_results": False,
        },
        "cases": results,
        "aggregate": {
            "scored_physical_references": scored_references,
            "covered_physical_references": covered_references,
            "threshold_coverage": covered_references / scored_references
            if scored_references
            else None,
            "mean_nearest_event_distance": float(np.mean(distances))
            if distances
            else None,
            "attribution_checks": attribution_checks,
            "attribution_matches": attribution_matches,
            "attribution_overlap": attribution_matches / attribution_checks
            if attribution_checks
            else None,
        },
        "interpretation": (
            "Alignment and entity co-change validation for ordered independent "
            "power-flow solutions; not dynamic prediction or causal attribution."
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
    n_clusters: int,
    window: int,
    random_state: int,
    alignment_tolerance: float,
) -> dict[str, Any]:
    provenance = Provenance(
        source=f"pandapower:{case_id}",
        method="independent Newton-Raphson load-scale campaign",
        recorded_at=recorded_at,
        record_id=f"ieee-orientation-v1:{case_id}",
    )
    campaign = IEEEPandapowerAdapter(case_id=case_id).run_campaign(
        load_scales,
        campaign_id=f"ieee-orientation-v1-{case_id}",
        provenance=provenance,
        context=Context(
            domain="power-system",
            values={"benchmark_case": case_id, "campaign_axis": "load_scale"},
        ),
    )
    run = orient_ieee_campaign(
        campaign,
        analysis_id=f"ieee-orientation-v1-{case_id}",
        n_clusters=n_clusters,
        window=window,
        random_state=random_state,
    )
    event_scales = [event.load_scale for event in run.attributions]
    references = _physical_references(
        campaign,
        event_scales=event_scales,
        tolerance=alignment_tolerance,
    )
    attribution = _attribution_overlap(campaign, run.attributions)
    failed = [
        {
            "scenario_id": snapshot.scenario_id,
            "load_scale": snapshot.load_scale,
            "failure_type": snapshot.failure.split(":", 1)[0]
            if snapshot.failure
            else "unknown",
        }
        for snapshot in campaign.snapshots
        if not snapshot.converged
    ]
    return {
        "case_id": case_id,
        "requested_scenarios": len(campaign.snapshots),
        "converged_scenarios": len(campaign.campaign_batch.values),
        "failed_scenarios": failed,
        "first_nonconverged_load_scale": failed[0]["load_scale"] if failed else None,
        "v07_event_count": len(event_scales),
        "v07_event_load_scales": event_scales,
        "physical_references": references,
        "scored_physical_references": len(references),
        "covered_physical_references": sum(
            bool(reference["covered_within_tolerance"]) for reference in references
        ),
        **attribution,
        "report_scope_confirmed": (
            "not a time trajectory" in run.report.explanation
            and run.report.provenance.metadata.get("ordered_parameter")
            == "load_scale"
        ),
    }


def _physical_references(
    campaign: IEEECoupledCampaign,
    *,
    event_scales: list[float],
    tolerance: float,
) -> list[dict[str, Any]]:
    matrix = campaign.campaign_batch.to_numpy()
    names = [feature.name for feature in campaign.campaign_batch.features]
    load = matrix[:, names.index("load_scale")]
    candidates = (
        (
            "minimum_bus_voltage_below_0.95_pu",
            matrix[:, names.index("minimum_bus_voltage")] < 0.95,
        ),
        (
            "maximum_line_loading_at_least_100_percent",
            matrix[:, names.index("maximum_line_loading")] >= 100.0,
        ),
    )
    references = []
    for reference_id, mask in candidates:
        indices = np.flatnonzero(mask)
        if len(indices) == 0:
            continue
        crossing_scale = float(load[int(indices[0])])
        nearest = min(
            (abs(crossing_scale - event_scale) for event_scale in event_scales),
            default=None,
        )
        references.append(
            {
                "reference_id": reference_id,
                "crossing_load_scale": crossing_scale,
                "nearest_event_distance": nearest,
                "covered_within_tolerance": nearest is not None
                and nearest <= tolerance + 1e-12,
            }
        )
    return references


def _attribution_overlap(
    campaign: IEEECoupledCampaign,
    events: tuple[IEEEAttributionEvent, ...],
) -> dict[str, int]:
    snapshots = {snapshot.scenario_id: snapshot for snapshot in campaign.snapshots}
    checks = 0
    matches = 0
    for event in events:
        snapshot = snapshots[event.scenario_id]
        if snapshot.bus_batch is None or snapshot.line_batch is None:
            continue
        buses = snapshot.bus_batch.to_numpy()
        lines = snapshot.line_batch.to_numpy()
        minimum_voltage_bus = snapshot.bus_batch.row_ids[int(np.argmin(buses[:, 0]))]
        maximum_loading_line = snapshot.line_batch.row_ids[int(np.argmax(lines[:, 0]))]
        top_voltage_change = next(
            delta for delta in event.bus_deltas if delta.feature == "vm_pu"
        )
        top_loading_change = next(
            delta
            for delta in event.line_deltas
            if delta.feature == "loading_percent"
        )
        checks += 2
        matches += int(top_voltage_change.entity_id == minimum_voltage_bus)
        matches += int(top_loading_change.entity_id == maximum_loading_line)
    return {"attribution_checks": checks, "attribution_matches": matches}


def _write_outputs(result: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "validation_result.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    aggregate = result["aggregate"]
    summary = f"""# IEEE Orientation Validation V1

| Metric | Result |
|---|---:|
| Physical references | {aggregate['scored_physical_references']} |
| Covered within one load step | {aggregate['covered_physical_references']} |
| Threshold coverage | {aggregate['threshold_coverage']} |
| Mean nearest event distance | {aggregate['mean_nearest_event_distance']} |
| Attribution overlap | {aggregate['attribution_overlap']} |

Ordered steady-state load campaigns; not time dynamics or causal validation.
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
    aggregate = result["aggregate"]
    print(f"Threshold coverage: {aggregate['threshold_coverage']}")
    print(f"Attribution overlap: {aggregate['attribution_overlap']}")


if __name__ == "__main__":
    main()
