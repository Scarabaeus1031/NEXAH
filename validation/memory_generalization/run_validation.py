"""Evaluate episodic retrieval across systems, noise, and parameter shifts."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import numpy as np
from numpy.typing import NDArray

from nexah.backends import V07BackendAdapter
from nexah.orientation import (
    Context,
    Episode,
    JsonlEpisodeStore,
    OrientationState,
    Outcome,
    Provenance,
    generate_orientation_report,
)

from .systems import add_relative_noise, kuramoto, lorenz, rossler


FloatArray = NDArray[np.float64]
DEFAULT_OUTPUT_DIR = Path("outputs/memory_generalization")
SYSTEM_ORDER = ("lorenz", "rossler", "kuramoto")


def run_validation(
    *,
    recorded_at: datetime,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    write_outputs: bool = True,
    samples: int = 2500,
) -> dict[str, Any]:
    if recorded_at.tzinfo is None:
        raise ValueError("recorded_at must include a timezone")

    references = {
        "lorenz": lorenz(samples=samples),
        "rossler": rossler(samples=samples),
        "kuramoto": kuramoto(samples=samples),
    }
    queries: list[tuple[str, str, FloatArray]] = []
    for index, family in enumerate(SYSTEM_ORDER):
        base = references[family]
        queries.extend(
            [
                (family, "clean", base.copy()),
                (
                    family,
                    "noise_0.01",
                    add_relative_noise(base, fraction=0.01, seed=100 + index),
                ),
                (
                    family,
                    "noise_0.05",
                    add_relative_noise(base, fraction=0.05, seed=200 + index),
                ),
            ]
        )
    queries.extend(
        [
            ("lorenz", "parameter_shift", lorenz(rho=26.0, samples=samples)),
            ("rossler", "parameter_shift", rossler(c=6.0, samples=samples)),
            (
                "kuramoto",
                "parameter_shift",
                kuramoto(coupling=1.8, samples=samples),
            ),
        ]
    )

    with TemporaryDirectory(prefix="nexah-memory-validation-") as temporary:
        store = JsonlEpisodeStore(Path(temporary) / "episodes.jsonl")
        for index, family in enumerate(SYSTEM_ORDER):
            store.put(
                _episode(
                    family=family,
                    trajectory=references[family],
                    recorded_at=recorded_at + timedelta(minutes=index),
                )
            )

        query_results = []
        for index, (family, condition, trajectory) in enumerate(queries):
            state = _state(
                trajectory,
                analysis_id=f"query-{family}-{condition}",
                recorded_at=recorded_at + timedelta(hours=1, minutes=index),
            )
            ranking = store.retrieve_similar(state, limit=3)
            scores = {
                reference.episode_id.removeprefix("episode-"): (
                    reference.similarity.value if reference.similarity else 0.0
                )
                for reference in ranking
            }
            predicted = ranking[0].episode_id.removeprefix("episode-")
            expected_score = scores[family]
            other_scores = [score for key, score in scores.items() if key != family]
            best_other = max(other_scores)
            query_results.append(
                {
                    "family": family,
                    "condition": condition,
                    "predicted_family": predicted,
                    "correct": predicted == family,
                    "expected_similarity": expected_score,
                    "best_other_similarity": best_other,
                    "margin": expected_score - best_other,
                    "ranking": [
                        {
                            "family": reference.episode_id.removeprefix("episode-"),
                            "similarity": reference.similarity.value
                            if reference.similarity
                            else None,
                            "method": reference.similarity.method
                            if reference.similarity
                            else None,
                        }
                        for reference in ranking
                    ],
                }
            )

        history_records = store.history()

    aggregate = _aggregate(query_results)
    failure_cases = _failure_cases(query_results, aggregate)
    result = {
        "validation_id": "memory-generalization-v1",
        "preregistered_design": {
            "families": list(SYSTEM_ORDER),
            "reference_episodes_per_family": 1,
            "samples_per_trajectory": samples,
            "conditions": ["clean", "noise_0.01", "noise_0.05", "parameter_shift"],
            "shared_context_domain": "synthetic-dynamical-system",
            "v07_config": {"n_clusters": 6, "window": 10, "random_state": 42},
            "top1_chance_baseline": 1.0 / 3.0,
            "parameters_tuned_on_results": False,
        },
        "aggregate": aggregate,
        "queries": query_results,
        "store_history_records": len(history_records),
        "failure_cases": failure_cases,
        "interpretation": (
            "This validates heuristic retrieval discrimination for three "
            "deterministic synthetic families. It does not establish semantic "
            "memory, calibrated similarity, or real-world generality."
        ),
    }
    if write_outputs:
        _write_outputs(result, output_dir)
    return result


def _state(
    trajectory: FloatArray,
    *,
    analysis_id: str,
    recorded_at: datetime,
) -> OrientationState:
    return V07BackendAdapter(
        n_clusters=6,
        window=10,
        random_state=42,
    ).adapt(
        trajectory,
        analysis_id=analysis_id,
        provenance=Provenance(
            source=f"memory-generalization:{analysis_id}",
            method="deterministic synthetic validation trajectory",
            recorded_at=recorded_at,
            record_id=analysis_id,
        ),
        context=Context(
            domain="synthetic-dynamical-system",
            values={"family_hidden_from_similarity": True},
        ),
    ).state


def _episode(
    *,
    family: str,
    trajectory: FloatArray,
    recorded_at: datetime,
) -> Episode:
    adapted = V07BackendAdapter(
        n_clusters=6,
        window=10,
        random_state=42,
    ).adapt(
        trajectory,
        analysis_id=f"reference-{family}",
        provenance=Provenance(
            source=f"memory-generalization:reference:{family}",
            method="deterministic synthetic reference episode",
            recorded_at=recorded_at,
            record_id=f"reference-{family}",
        ),
        context=Context(
            domain="synthetic-dynamical-system",
            values={"family_hidden_from_similarity": True},
        ),
    )
    report = generate_orientation_report(adapted)
    outcome_time = recorded_at + timedelta(seconds=1)
    return Episode(
        episode_id=f"episode-{family}",
        state=adapted.state,
        report=report,
        outcome=Outcome(
            outcome_id=f"outcome-{family}",
            description=f"Synthetic {family} reference trajectory completed.",
            observed_at=outcome_time,
            provenance=Provenance(
                source=f"memory-generalization:outcome:{family}",
                method="completed synthetic simulation",
                recorded_at=outcome_time,
                record_id=f"outcome-{family}",
            ),
            uncertainty=adapted.state.uncertainty,
        ),
        created_at=outcome_time,
        provenance=adapted.state.provenance,
        tags=("synthetic", "memory-generalization", family),
    )


def _aggregate(queries: list[dict[str, Any]]) -> dict[str, Any]:
    correct = sum(bool(query["correct"]) for query in queries)
    margins = [float(query["margin"]) for query in queries]
    by_condition: dict[str, dict[str, Any]] = {}
    for condition in ("clean", "noise_0.01", "noise_0.05", "parameter_shift"):
        selected = [query for query in queries if query["condition"] == condition]
        by_condition[condition] = {
            "queries": len(selected),
            "top1_accuracy": sum(bool(query["correct"]) for query in selected)
            / len(selected),
            "mean_margin": float(np.mean([query["margin"] for query in selected])),
            "minimum_margin": min(float(query["margin"]) for query in selected),
        }
    return {
        "queries": len(queries),
        "correct_top1": correct,
        "top1_accuracy": correct / len(queries),
        "chance_baseline": 1.0 / 3.0,
        "mean_margin": float(np.mean(margins)),
        "minimum_margin": min(margins),
        "by_condition": by_condition,
    }


def _failure_cases(
    queries: list[dict[str, Any]], aggregate: dict[str, Any]
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = [
        {
            "id": "synthetic-family-benchmark",
            "severity": "boundary",
            "description": (
                "All trajectories are deterministic synthetic fixtures; the "
                "benchmark does not establish real-world memory semantics."
            ),
        },
        {
            "id": "single-reference-per-family",
            "severity": "boundary",
            "description": (
                "Each family has one stored reference, so within-family outcome "
                "diversity and episode density are not evaluated."
            ),
        },
        {
            "id": "heuristic-uncalibrated-similarity",
            "severity": "known",
            "description": (
                "Similarity scores are weighted v0.7 signature heuristics, not "
                "calibrated probabilities or semantic equivalence."
            ),
        },
    ]
    confused = [query for query in queries if not query["correct"]]
    if confused:
        failures.append(
            {
                "id": "cross-family-confusion",
                "severity": "observed",
                "description": (
                    f"{len(confused)} of {len(queries)} queries ranked a different "
                    "system family first."
                ),
                "queries": [
                    f"{query['family']}:{query['condition']}→{query['predicted_family']}"
                    for query in confused
                ],
            }
        )
    if float(aggregate["minimum_margin"]) < 0.05:
        failures.append(
            {
                "id": "low-retrieval-separation",
                "severity": "observed",
                "description": (
                    "At least one expected-family score is separated from the "
                    "best alternative by less than 0.05 or is ranked below it."
                ),
            }
        )
    return failures


def _write_outputs(result: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "validation_result.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")

    aggregate = result["aggregate"]
    rows = []
    for condition, metrics in aggregate["by_condition"].items():
        rows.append(
            f"| {condition} | {metrics['top1_accuracy']:.6f} | "
            f"{metrics['mean_margin']:.6f} | {metrics['minimum_margin']:.6f} |"
        )
    summary = "\n".join(
        [
            "# Memory Generalization Validation",
            "",
            "| Condition | Top-1 accuracy | Mean margin | Minimum margin |",
            "|---|---:|---:|---:|",
            *rows,
            "",
            f"Overall top-1 accuracy: {aggregate['top1_accuracy']:.6f}",
            f"Chance baseline: {aggregate['chance_baseline']:.6f}",
            "",
            "Synthetic heuristic retrieval benchmark; not semantic or real-world validation.",
            "",
        ]
    )
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
    print(f"Result: {args.output_dir / 'validation_result.json'}")
    print(f"Top-1 accuracy: {aggregate['top1_accuracy']:.6f}")
    print(f"Minimum margin: {aggregate['minimum_margin']:.6f}")


if __name__ == "__main__":
    main()
