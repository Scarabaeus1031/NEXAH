"""Validate the Orientation Report against the canonical Demonstrator proxy."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
import json
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from PROTO_CORE.NEXAH_DEMONSTRATOR.scripts.generate_transition_structure import (
    generate_transition_data,
)
from nexah.backends import V07BackendAdapter
from nexah.orientation import Context, Provenance, generate_orientation_report


DEFAULT_OUTPUT_DIR = Path("outputs/orientation_mvp")


def match_events(
    predicted: Sequence[int],
    reference: Sequence[int],
    *,
    tolerance: int,
    sample_count: int,
) -> dict[str, Any]:
    """One-to-one event matching with a declared symmetric sample tolerance."""

    unmatched = set(int(event) for event in reference)
    distances: list[int] = []
    for event in sorted(int(item) for item in predicted):
        candidates = [
            reference_event
            for reference_event in unmatched
            if abs(reference_event - event) <= tolerance
        ]
        if not candidates:
            continue
        matched = min(candidates, key=lambda item: (abs(item - event), item))
        unmatched.remove(matched)
        distances.append(abs(matched - event))

    matched_count = len(distances)
    precision = matched_count / len(predicted) if predicted else 0.0
    recall = matched_count / len(reference) if reference else 0.0
    f1 = (
        2.0 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )

    predicted_set = set(int(item) for item in predicted)
    reference_set = set(int(item) for item in reference)
    exact_correct = sample_count - len(predicted_set ^ reference_set)
    return {
        "predicted_events": len(predicted),
        "reference_events": len(reference),
        "matched_events": matched_count,
        "tolerance_samples": tolerance,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "mean_absolute_event_error": (
            float(np.mean(distances)) if distances else None
        ),
        "exact_sample_accuracy": exact_correct / sample_count,
    }


def run_validation(
    *,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    recorded_at: datetime,
    steps: int = 8000,
    dt: float = 0.01,
    requested_sheets: int = 6,
    n_clusters: int = 6,
    window: int = 10,
    random_state: int = 42,
    write_outputs: bool = True,
) -> dict[str, Any]:
    """Run the declared proxy validation without tuning against its outcome."""

    if recorded_at.tzinfo is None:
        raise ValueError("recorded_at must include a timezone")

    reference = generate_transition_data(
        steps=steps,
        dt=dt,
        num_sheets=requested_sheets,
    )
    trajectory = reference["trajectory"]
    sheets = reference["sheets"]
    reference_events = np.flatnonzero(reference["transition_events"]).astype(int)
    timestamps = tuple(
        recorded_at + timedelta(seconds=index * dt) for index in range(steps)
    )

    adapted = V07BackendAdapter(
        n_clusters=n_clusters,
        window=window,
        random_state=random_state,
    ).adapt(
        trajectory,
        analysis_id="lorenz-sheet-proxy-v1",
        provenance=Provenance(
            source=(
                "PROTO_CORE/NEXAH_DEMONSTRATOR/scripts/"
                "generate_transition_structure.py"
            ),
            method="deterministic Euler Lorenz Demonstrator",
            recorded_at=recorded_at,
            record_id="orientation-mvp-validation-v1",
            metadata={
                "steps": steps,
                "dt": dt,
                "requested_sheets": requested_sheets,
            },
        ),
        context=Context(
            domain="lorenz-demonstrator",
            values={
                "reference_type": "constructed radial-sheet proxy",
                "external_ground_truth": False,
            },
        ),
        timestamps=timestamps,
    )
    report = generate_orientation_report(adapted)

    embedded_shifts = adapted.raw_output["regime_shifts"]
    predicted_events = [
        adapted.alignment.raw_anchor(int(index)) for index in embedded_shifts
    ]
    v07_metrics = match_events(
        predicted_events,
        reference_events.tolist(),
        tolerance=window,
        sample_count=steps,
    )
    null_metrics = match_events(
        [],
        reference_events.tolist(),
        tolerance=window,
        sample_count=steps,
    )

    observed_labels = sorted(int(label) for label in np.unique(sheets))
    failure_cases = [
        {
            "id": "constructed-reference-not-ground-truth",
            "severity": "boundary",
            "description": (
                "Reference transitions are changes in radial bins constructed by "
                "the Demonstrator, not externally observed dynamical regimes."
            ),
        },
        {
            "id": "sheet-count-upper-bound-bin",
            "severity": "confirmed",
            "description": (
                f"requested_sheets={requested_sheets} produced "
                f"{len(observed_labels)} labels {observed_labels} because the "
                "maximum radius enters an additional np.digitize boundary bin."
            ),
        },
        {
            "id": "state-identities-not-aligned",
            "severity": "boundary",
            "description": (
                "v0.7 KMeans cluster IDs and Demonstrator radial-sheet IDs do not "
                "share semantics; validation compares event timing only."
            ),
        },
        {
            "id": "overlapping-window-dependence",
            "severity": "known",
            "description": (
                "v0.7 embedded windows overlap and may affect persistence and "
                "change timing."
            ),
        },
        {
            "id": "event-class-imbalance",
            "severity": "metric",
            "description": (
                "Transition samples are sparse enough that the no-change baseline "
                "has higher exact sample accuracy despite zero event recall; event "
                "precision, recall, and F1 are the relevant comparison metrics."
            ),
        },
    ]

    comparison = {
        "validation_id": "orientation-mvp-validation-v1",
        "reference": {
            "type": "constructed radial-sheet transition proxy",
            "external_ground_truth": False,
            "requested_sheets": requested_sheets,
            "observed_labels": observed_labels,
            "transition_events": int(len(reference_events)),
        },
        "v07": {
            "config": {
                "n_clusters": n_clusters,
                "window": window,
                "random_state": random_state,
            },
            "metrics": v07_metrics,
        },
        "null_no_change_baseline": {
            "description": "Predict no transition at any source sample.",
            "metrics": null_metrics,
        },
        "interpretation": (
            "This comparison tests reproducible temporal correspondence with a "
            "constructed proxy. It does not validate regime truth, causality, "
            "or cross-system generality."
        ),
    }
    result = {
        "orientation_state": adapted.state.to_dict(),
        "orientation_report": report.to_dict(),
        "baseline_comparison": comparison,
        "failure_cases": failure_cases,
    }

    if write_outputs:
        _write_outputs(result, output_dir)
    return result


def _write_outputs(result: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for name in (
        "orientation_state",
        "orientation_report",
        "baseline_comparison",
        "failure_cases",
    ):
        with (output_dir / f"{name}.json").open("w", encoding="utf-8") as handle:
            json.dump(result[name], handle, indent=2)
            handle.write("\n")

    metrics = result["baseline_comparison"]["v07"]["metrics"]
    baseline = result["baseline_comparison"]["null_no_change_baseline"]["metrics"]
    summary = f"""# Orientation MVP Validation Summary

Reference: constructed radial-sheet transition proxy (not external ground truth)

| Method | Precision | Recall | F1 | Exact sample accuracy |
|---|---:|---:|---:|---:|
| v0.7 local label changes | {metrics['precision']:.6f} | {metrics['recall']:.6f} | {metrics['f1']:.6f} | {metrics['exact_sample_accuracy']:.6f} |
| Null: no changes | {baseline['precision']:.6f} | {baseline['recall']:.6f} | {baseline['f1']:.6f} | {baseline['exact_sample_accuracy']:.6f} |

Event tolerance: ±{metrics['tolerance_samples']} source samples.

This run validates reproducible pipeline integration and proxy-event comparison.
It does not validate external regime truth, causal intervention, or generality.
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
    result = run_validation(
        output_dir=args.output_dir,
        recorded_at=args.recorded_at,
    )
    metrics = result["baseline_comparison"]["v07"]["metrics"]
    print(f"Orientation report: {args.output_dir / 'orientation_report.json'}")
    print(f"Proxy event F1: {metrics['f1']:.6f}")


if __name__ == "__main__":
    main()
