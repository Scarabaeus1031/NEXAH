"""Evaluate multi-episode retrieval with validation/test method selection."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import numpy as np
from numpy.typing import NDArray

from nexah.backends import BackendResult, EmbeddingAlignment, V07BackendAdapter
from nexah.orientation import (
    Context,
    Episode,
    JsonlEpisodeStore,
    OrientationState,
    Outcome,
    Provenance,
    generate_orientation_report,
    orientation_similarity,
)
from validation.memory_generalization.systems import (
    add_relative_noise,
    kuramoto,
    lorenz,
    rossler,
)


FloatArray = NDArray[np.float64]
DEFAULT_OUTPUT_DIR = Path("outputs/memory_generalization_v2")
FAMILIES = ("lorenz", "rossler", "kuramoto")
METHOD_ORDER = ("current_signature", "sequence_profile", "hybrid_50_50")


@dataclass(frozen=True, slots=True)
class BenchmarkItem:
    item_id: str
    family: str
    condition: str
    state: OrientationState
    labels: tuple[int, ...]


def run_validation(
    *,
    recorded_at: datetime,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    samples: int = 1500,
    write_outputs: bool = True,
) -> dict[str, Any]:
    if recorded_at.tzinfo is None:
        raise ValueError("recorded_at must include a timezone")

    references = _reference_items(recorded_at=recorded_at, samples=samples)
    validation_queries = _query_items(
        split="validation",
        recorded_at=recorded_at + timedelta(hours=2),
        samples=samples,
    )
    test_queries = _query_items(
        split="test",
        recorded_at=recorded_at + timedelta(hours=4),
        samples=samples,
    )

    with TemporaryDirectory(prefix="nexah-memory-v2-") as temporary:
        store = JsonlEpisodeStore(Path(temporary) / "episodes.jsonl")
        for index, item in enumerate(references):
            store.put(
                _episode_from_item(
                    item,
                    recorded_at=recorded_at + timedelta(minutes=index),
                )
            )
        persisted_ids = [episode.episode_id for episode in store.all()]
        history_records = len(store.history())

    validation_by_method = {
        method: _evaluate(method, validation_queries, references)
        for method in METHOD_ORDER
    }
    selected_method = max(
        METHOD_ORDER,
        key=lambda method: (
            validation_by_method[method]["top1_accuracy"],
            validation_by_method[method]["mean_reciprocal_rank"],
            -METHOD_ORDER.index(method),
        ),
    )
    test_selected = _evaluate(selected_method, test_queries, references)
    test_all_methods = {
        method: _evaluate(method, test_queries, references)
        for method in METHOD_ORDER
    }
    failure_cases = _failure_cases(
        selected_method=selected_method,
        validation=validation_by_method[selected_method],
        test=test_selected,
    )
    result = {
        "validation_id": "memory-generalization-v2",
        "design": {
            "families": list(FAMILIES),
            "reference_episodes_per_family": 5,
            "reference_episodes": len(references),
            "validation_queries": len(validation_queries),
            "held_out_test_queries": len(test_queries),
            "samples_per_trajectory": samples,
            "shared_context_domain": "synthetic-dynamical-system",
            "methods": list(METHOD_ORDER),
            "selection_rule": (
                "maximum validation Top-1 accuracy, then MRR, then simpler "
                "predeclared method order"
            ),
            "test_used_for_selection": False,
            "v07_config": {"n_clusters": 6, "window": 10, "random_state": 42},
            "chance_top1": 1.0 / 3.0,
            "chance_recall_at_3": 1.0 - (_combination(10, 3) / _combination(15, 3)),
        },
        "store": {
            "active_episodes": len(persisted_ids),
            "history_records": history_records,
            "episode_ids": persisted_ids,
        },
        "validation_by_method": validation_by_method,
        "selected_method": selected_method,
        "held_out_test_selected_method": test_selected,
        "held_out_test_all_methods": test_all_methods,
        "failure_cases": failure_cases,
        "interpretation": (
            "V2 tests family-level retrieval from a denser synthetic memory. "
            "It does not validate semantic outcome relevance or real-world memory."
        ),
    }
    if write_outputs:
        _write_outputs(result, output_dir)
    return result


def _reference_items(*, recorded_at: datetime, samples: int) -> tuple[BenchmarkItem, ...]:
    specs: list[tuple[str, str, FloatArray]] = []
    for index, rho in enumerate((24.0, 26.0, 28.0, 30.0, 32.0)):
        specs.append(
            (
                "lorenz",
                f"rho_{rho:g}",
                lorenz(
                    rho=rho,
                    samples=samples,
                    initial=(0.1 + index * 0.01, 0.0, 0.0),
                ),
            )
        )
    for index, c in enumerate((4.8, 5.2, 5.7, 6.2, 6.6)):
        specs.append(
            (
                "rossler",
                f"c_{c:g}",
                rossler(
                    c=c,
                    samples=samples,
                    initial=(0.1 + index * 0.01, 0.0, 0.0),
                ),
            )
        )
    for coupling, seed in zip((1.4, 1.8, 2.2, 2.6, 3.0), (3, 5, 7, 9, 11)):
        specs.append(
            (
                "kuramoto",
                f"k_{coupling:g}_seed_{seed}",
                kuramoto(coupling=coupling, samples=samples, seed=seed),
            )
        )
    return tuple(
        _item(
            family=family,
            condition=condition,
            trajectory=trajectory,
            item_id=f"reference-{family}-{condition}",
            recorded_at=recorded_at + timedelta(seconds=index),
        )
        for index, (family, condition, trajectory) in enumerate(specs)
    )


def _query_items(
    *, split: str, recorded_at: datetime, samples: int
) -> tuple[BenchmarkItem, ...]:
    if split == "validation":
        specs = [
            ("lorenz", "rho_25", lorenz(rho=25.0, samples=samples)),
            ("lorenz", "rho_29_noise", add_relative_noise(lorenz(rho=29.0, samples=samples), fraction=0.02, seed=301)),
            ("rossler", "c_5", rossler(c=5.0, samples=samples)),
            ("rossler", "c_6_noise", add_relative_noise(rossler(c=6.0, samples=samples), fraction=0.02, seed=302)),
            ("kuramoto", "k_1.6", kuramoto(coupling=1.6, samples=samples, seed=13)),
            ("kuramoto", "k_2.4_noise", add_relative_noise(kuramoto(coupling=2.4, samples=samples, seed=15), fraction=0.02, seed=303)),
        ]
    elif split == "test":
        specs = [
            ("lorenz", "rho_27_noise", add_relative_noise(lorenz(rho=27.0, samples=samples), fraction=0.03, seed=401)),
            ("lorenz", "rho_31", lorenz(rho=31.0, samples=samples)),
            ("rossler", "c_5.4_noise", add_relative_noise(rossler(c=5.4, samples=samples), fraction=0.03, seed=402)),
            ("rossler", "c_6.4", rossler(c=6.4, samples=samples)),
            ("kuramoto", "k_2_seed_17", kuramoto(coupling=2.0, samples=samples, seed=17)),
            ("kuramoto", "k_2.8_seed_19_noise", add_relative_noise(kuramoto(coupling=2.8, samples=samples, seed=19), fraction=0.03, seed=403)),
        ]
    else:
        raise ValueError(f"unknown split: {split}")
    return tuple(
        _item(
            family=family,
            condition=condition,
            trajectory=trajectory,
            item_id=f"{split}-{family}-{condition}",
            recorded_at=recorded_at + timedelta(seconds=index),
        )
        for index, (family, condition, trajectory) in enumerate(specs)
    )


def _item(
    *,
    family: str,
    condition: str,
    trajectory: FloatArray,
    item_id: str,
    recorded_at: datetime,
) -> BenchmarkItem:
    adapted = V07BackendAdapter(
        n_clusters=6,
        window=10,
        random_state=42,
    ).adapt(
        trajectory,
        analysis_id=item_id,
        provenance=Provenance(
            source=f"memory-generalization-v2:{item_id}",
            method="deterministic held-out synthetic trajectory",
            recorded_at=recorded_at,
            record_id=item_id,
        ),
        context=Context(
            domain="synthetic-dynamical-system",
            values={"family_hidden_from_similarity": True},
        ),
    )
    labels = _labels_from_transitions_and_raw(adapted.raw_output)
    return BenchmarkItem(
        item_id=item_id,
        family=family,
        condition=condition,
        state=adapted.state,
        labels=labels,
    )


def _labels_from_transitions_and_raw(raw_output: dict[str, Any]) -> tuple[int, ...]:
    # v0.7 does not expose labels publicly. Reconstructing labels from shifts is
    # impossible, so V2 stores a permutation-invariant change profile derived
    # from the available instability sequence instead.
    instability = raw_output.get("instability", [])
    return tuple(int(round(float(value) * 1000.0)) for value in instability)


def _episode_from_item(item: BenchmarkItem, *, recorded_at: datetime) -> Episode:
    # The persisted episode tests the real store; evaluation features remain in
    # BenchmarkItem so no validation-only labels enter the production contract.
    adapted = _backend_result_for_state(item)
    report = generate_orientation_report(adapted)
    outcome_time = recorded_at + timedelta(seconds=1)
    return Episode(
        episode_id=item.item_id,
        state=item.state,
        report=report,
        outcome=Outcome(
            outcome_id=f"outcome-{item.item_id}",
            description=f"Synthetic {item.family} reference completed.",
            observed_at=outcome_time,
            provenance=Provenance(
                source=f"memory-generalization-v2:outcome:{item.item_id}",
                method="completed synthetic reference",
                recorded_at=outcome_time,
                record_id=f"outcome-{item.item_id}",
            ),
            uncertainty=item.state.uncertainty,
        ),
        created_at=outcome_time,
        provenance=item.state.provenance,
        tags=("synthetic", "memory-generalization-v2", item.family),
    )


def _backend_result_for_state(item: BenchmarkItem) -> BackendResult:
    # Regenerate the deterministic source represented by the item is neither
    # possible nor necessary here. Report generation needs structural artifacts,
    # so reference Episodes use a minimal coherent result derived from state
    # evidence and no additional transition claims.
    embedded = int(item.state.representation.parameters["embedded_samples"])
    window = int(item.state.representation.parameters["window"])
    return BackendResult(
        state=item.state,
        transitions=(),
        regimes=(),
        alignment=EmbeddingAlignment(
            input_samples=len(item.state.observations),
            embedded_samples=embedded,
            window=window,
            final_source_sample_used=len(item.state.observations) - 2,
        ),
        raw_output={"regime_shifts": [], "regime_zones": []},
    )


def _evaluate(
    method: str,
    queries: tuple[BenchmarkItem, ...],
    references: tuple[BenchmarkItem, ...],
) -> dict[str, Any]:
    details = []
    reciprocal_ranks = []
    recall_at_3 = []
    margins = []
    for query in queries:
        ranking = sorted(
            (
                (_score(method, query, reference), reference)
                for reference in references
            ),
            key=lambda item: (-item[0], item[1].item_id),
        )
        top1 = ranking[0][1].family
        first_correct_rank = next(
            index
            for index, (_, reference) in enumerate(ranking, start=1)
            if reference.family == query.family
        )
        best_same = max(
            score for score, reference in ranking if reference.family == query.family
        )
        best_other = max(
            score for score, reference in ranking if reference.family != query.family
        )
        reciprocal_ranks.append(1.0 / first_correct_rank)
        recall_at_3.append(
            any(reference.family == query.family for _, reference in ranking[:3])
        )
        margins.append(best_same - best_other)
        details.append(
            {
                "query_id": query.item_id,
                "family": query.family,
                "predicted_family": top1,
                "correct": top1 == query.family,
                "first_correct_rank": first_correct_rank,
                "margin": best_same - best_other,
                "top3": [
                    {
                        "reference_id": reference.item_id,
                        "family": reference.family,
                        "score": score,
                    }
                    for score, reference in ranking[:3]
                ],
            }
        )
    return {
        "queries": len(queries),
        "top1_accuracy": sum(bool(item["correct"]) for item in details) / len(details),
        "recall_at_3": sum(recall_at_3) / len(recall_at_3),
        "mean_reciprocal_rank": float(np.mean(reciprocal_ranks)),
        "mean_margin": float(np.mean(margins)),
        "minimum_margin": min(margins),
        "details": details,
    }


def _score(method: str, query: BenchmarkItem, reference: BenchmarkItem) -> float:
    current = orientation_similarity(
        query.state,
        reference.state,
        reference.item_id,
    ).value
    sequence = _sequence_similarity(query.labels, reference.labels)
    if method == "current_signature":
        return current
    if method == "sequence_profile":
        return sequence
    if method == "hybrid_50_50":
        return 0.5 * current + 0.5 * sequence
    raise ValueError(f"unknown method: {method}")


def _sequence_similarity(left: tuple[int, ...], right: tuple[int, ...]) -> float:
    left_profile = _sequence_profile(left)
    right_profile = _sequence_profile(right)
    distance = float(np.mean(np.abs(left_profile - right_profile)))
    return 1.0 / (1.0 + distance)


def _sequence_profile(values: tuple[int, ...]) -> FloatArray:
    sequence = np.asarray(values, dtype=np.float64) / 1000.0
    if len(sequence) < 2:
        return np.zeros(8, dtype=np.float64)
    changes = np.abs(np.diff(sequence))
    return np.asarray(
        [
            float(np.mean(sequence)),
            float(np.std(sequence)),
            float(np.quantile(sequence, 0.25)),
            float(np.quantile(sequence, 0.50)),
            float(np.quantile(sequence, 0.75)),
            float(np.mean(changes)),
            float(np.std(changes)),
            float(np.quantile(changes, 0.90)),
        ],
        dtype=np.float64,
    )


def _failure_cases(
    *,
    selected_method: str,
    validation: dict[str, Any],
    test: dict[str, Any],
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = [
        {
            "id": "synthetic-only",
            "severity": "boundary",
            "description": "V2 contains only deterministic synthetic systems.",
        },
        {
            "id": "family-label-objective",
            "severity": "boundary",
            "description": (
                "The target is system-family retrieval, not outcome relevance or "
                "semantic similarity."
            ),
        },
        {
            "id": "validation-only-sequence-proxy",
            "severity": "boundary",
            "description": (
                "The sequence profile uses the exposed v0.7 instability sequence; "
                "raw cluster labels are not part of the public backend contract."
            ),
        },
    ]
    confused = [item for item in test["details"] if not item["correct"]]
    if confused:
        failures.append(
            {
                "id": "held-out-family-confusion",
                "severity": "observed",
                "description": (
                    f"Selected method {selected_method} misclassified "
                    f"{len(confused)} of {test['queries']} held-out queries."
                ),
                "queries": [item["query_id"] for item in confused],
            }
        )
    if float(test["minimum_margin"]) < 0.05:
        failures.append(
            {
                "id": "held-out-low-margin",
                "severity": "observed",
                "description": "At least one held-out retrieval margin is below 0.05.",
            }
        )
    if validation["top1_accuracy"] > test["top1_accuracy"]:
        failures.append(
            {
                "id": "validation-test-drop",
                "severity": "observed",
                "description": "Top-1 accuracy drops from validation to held-out test.",
            }
        )
    return failures


def _combination(n: int, k: int) -> int:
    from math import comb

    return comb(n, k)


def _write_outputs(result: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "validation_result.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    selected = result["selected_method"]
    validation = result["validation_by_method"][selected]
    test = result["held_out_test_selected_method"]
    summary = f"""# Memory Generalization V2

Selected method: `{selected}`

| Split | Top-1 | Recall@3 | MRR | Mean margin | Minimum margin |
|---|---:|---:|---:|---:|---:|
| Validation | {validation['top1_accuracy']:.6f} | {validation['recall_at_3']:.6f} | {validation['mean_reciprocal_rank']:.6f} | {validation['mean_margin']:.6f} | {validation['minimum_margin']:.6f} |
| Held-out test | {test['top1_accuracy']:.6f} | {test['recall_at_3']:.6f} | {test['mean_reciprocal_rank']:.6f} | {test['mean_margin']:.6f} | {test['minimum_margin']:.6f} |

Synthetic family-level retrieval benchmark; not semantic outcome validation.
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
    test = result["held_out_test_selected_method"]
    print(f"Selected method: {result['selected_method']}")
    print(f"Held-out Top-1: {test['top1_accuracy']:.6f}")
    print(f"Held-out Recall@3: {test['recall_at_3']:.6f}")


if __name__ == "__main__":
    main()
