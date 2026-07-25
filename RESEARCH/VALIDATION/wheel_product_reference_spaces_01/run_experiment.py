#!/usr/bin/env python3
"""Deterministic wheel and product-reference-space validation."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import statistics
import tempfile
from collections import Counter, defaultdict
from pathlib import Path


N_PRIMES = 20_000
POLICIES = ("all_primes", "without_2_3")
FOLDS = ((0.50, 0.60), (0.60, 0.70), (0.70, 0.80),
         (0.80, 0.90), (0.90, 1.00))
SCAN_MODULI = tuple(range(5, 61)) + (120, 210, 280, 360)
COMPLEMENT_MODULI = (6, 30, 40, 42, 120, 280, 360)
ALPHA = 0.5
NULL_RUNS_MOD6 = 100
BOOTSTRAP_RUNS = 10_000
SEED = 20_260_725

ROOT = Path(__file__).resolve().parent
GENERATED_PATHS = (
    Path("RESULTS.md"),
    Path("results/prediction_folds.csv"),
    Path("results/modulus_summary.csv"),
    Path("results/product_folds.csv"),
    Path("results/complement_folds.csv"),
    Path("results/arithmetic_invariants.json"),
    Path("results/summary.json"),
)
CHECKSUM_PATHS = (
    Path("README.md"),
    Path("SPEC.md"),
    Path("run_experiment.py"),
    Path("test_experiment.py"),
    *GENERATED_PATHS,
)


def first_n_primes(count: int) -> list[int]:
    if count < 1:
        return []
    limit = 15 if count < 6 else int(
        count * (math.log(count) + math.log(math.log(count)))
    ) + 10
    while True:
        sieve = bytearray(b"\x01") * (limit + 1)
        sieve[0:2] = b"\x00\x00"
        for candidate in range(2, math.isqrt(limit) + 1):
            if sieve[candidate]:
                start = candidate * candidate
                length = ((limit - start) // candidate) + 1
                sieve[start:limit + 1:candidate] = b"\x00" * length
        primes = [number for number, flag in enumerate(sieve) if flag]
        if len(primes) >= count:
            return primes[:count]
        limit *= 2


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    return all(number % divisor for divisor in range(2, math.isqrt(number) + 1))


def euler_phi(number: int) -> int:
    result = number
    remaining = number
    factor = 2
    while factor * factor <= remaining:
        if remaining % factor == 0:
            while remaining % factor == 0:
                remaining //= factor
            result -= result // factor
        factor += 1
    if remaining > 1:
        result -= result // remaining
    return result


def radical(number: int) -> int:
    result = 1
    remaining = number
    factor = 2
    while factor * factor <= remaining:
        if remaining % factor == 0:
            result *= factor
            while remaining % factor == 0:
                remaining //= factor
        factor += 1
    if remaining > 1:
        result *= remaining
    return result


def policy_prefix(primes: list[int], end: int, policy: str) -> list[int]:
    prefix = primes[:end]
    if policy == "all_primes":
        return prefix
    if policy == "without_2_3":
        return [prime for prime in prefix if prime not in (2, 3)]
    raise ValueError(f"unknown policy: {policy}")


def fit_markov(
    residues: list[int],
) -> tuple[dict[tuple[int, int], int], Counter[int], dict[int, int]]:
    edges: dict[tuple[int, int], int] = defaultdict(int)
    rows: Counter[int] = Counter()
    best: dict[int, tuple[int, int]] = {}
    for left, right in zip(residues, residues[1:]):
        edges[(left, right)] += 1
        rows[left] += 1
    for (left, right), count in edges.items():
        candidate = (count, -right)
        if left not in best or candidate > best[left]:
            best[left] = candidate
    choices = {left: -candidate[1] for left, candidate in best.items()}
    return dict(edges), rows, choices


def markov_probability(
    model: tuple[dict[tuple[int, int], int], Counter[int], dict[int, int]],
    left: int,
    right: int,
    modulus: int,
) -> float:
    edges, rows, _ = model
    return (
        edges.get((left, right), 0) + ALPHA
    ) / (rows.get(left, 0) + ALPHA * modulus)


def fit_marginal(residues: list[int], modulus: int) -> tuple[Counter[int], int, int]:
    counts = Counter(residues[1:])
    total = sum(counts.values())
    choice = max(range(modulus), key=lambda value: (counts[value], -value))
    return counts, total, choice


def marginal_probability(
    model: tuple[Counter[int], int, int],
    right: int,
    modulus: int,
) -> float:
    counts, total, _ = model
    return (counts[right] + ALPHA) / (total + ALPHA * modulus)


def evaluate_prediction(
    test_residues: list[int],
    markov: tuple[dict[tuple[int, int], int], Counter[int], dict[int, int]],
    marginal: tuple[Counter[int], int, int],
    modulus: int,
) -> dict[str, float]:
    events = len(test_residues) - 1
    markov_loss = 0.0
    marginal_loss = 0.0
    markov_hits = 0
    marginal_hits = 0
    choices = markov[2]
    marginal_choice = marginal[2]
    for left, right in zip(test_residues, test_residues[1:]):
        markov_loss -= math.log(markov_probability(markov, left, right, modulus))
        marginal_loss -= math.log(
            marginal_probability(marginal, right, modulus)
        )
        markov_hits += choices.get(left, 0) == right
        marginal_hits += marginal_choice == right
    markov_loss /= events
    marginal_loss /= events
    gain = (marginal_loss - markov_loss) / math.log(2)
    return {
        "events": events,
        "markov_log_loss": markov_loss,
        "marginal_log_loss": marginal_loss,
        "information_gain_bits": gain,
        "normalized_gain": gain / math.log2(euler_phi(modulus)),
        "markov_accuracy": markov_hits / events,
        "marginal_accuracy": marginal_hits / events,
    }


def deterministic_seed(*parts: int) -> int:
    value = SEED
    for part in parts:
        value = (value * 1_000_003 + part) & ((1 << 63) - 1)
    return value


def prediction_rows(primes: list[int]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for policy_index, policy in enumerate(POLICIES):
        for fold_index, (train_fraction, test_fraction) in enumerate(FOLDS, 1):
            train_end = int(N_PRIMES * train_fraction)
            test_end = int(N_PRIMES * test_fraction)
            train_values = policy_prefix(primes, train_end, policy)
            test_values = primes[train_end:test_end]
            for modulus in SCAN_MODULI:
                train_residues = [value % modulus for value in train_values]
                test_residues = [value % modulus for value in test_values]
                markov = fit_markov(train_residues)
                marginal = fit_marginal(train_residues, modulus)
                observed = evaluate_prediction(
                    test_residues, markov, marginal, modulus
                )
                null_mean = None
                null_sd = None
                null_p = None
                if modulus == 6:
                    null_gains = []
                    for null_index in range(NULL_RUNS_MOD6):
                        shuffled = train_residues.copy()
                        random.Random(deterministic_seed(
                            policy_index, fold_index, null_index
                        )).shuffle(shuffled)
                        null_result = evaluate_prediction(
                            test_residues,
                            fit_markov(shuffled),
                            marginal,
                            modulus,
                        )
                        null_gains.append(
                            null_result["information_gain_bits"]
                        )
                    null_mean = statistics.fmean(null_gains)
                    null_sd = statistics.stdev(null_gains)
                    null_p = (
                        1 + sum(
                            gain >= observed["information_gain_bits"]
                            for gain in null_gains
                        )
                    ) / (NULL_RUNS_MOD6 + 1)
                rows.append({
                    "policy": policy,
                    "modulus": modulus,
                    "fold": fold_index,
                    "train_end_index": train_end,
                    "test_end_index": test_end,
                    "train_primes": len(train_values),
                    "test_primes": len(test_values),
                    "phi": euler_phi(modulus),
                    "radical": radical(modulus),
                    **observed,
                    "null_mean_information_gain_bits": null_mean,
                    "null_sd_information_gain_bits": null_sd,
                    "null_empirical_p": null_p,
                })
    return rows


def crt_encode_6_7(residue6: int, residue7: int) -> int:
    return (7 * residue6 + 36 * residue7) % 42


def crt_decode_42(residue42: int) -> tuple[int, int]:
    return residue42 % 6, residue42 % 7


def product_rows(primes: list[int]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for policy in POLICIES:
        for fold_index, (train_fraction, test_fraction) in enumerate(FOLDS, 1):
            train_end = int(N_PRIMES * train_fraction)
            test_end = int(N_PRIMES * test_fraction)
            train = policy_prefix(primes, train_end, policy)
            test = primes[train_end:test_end]
            train6 = [value % 6 for value in train]
            train7 = [value % 7 for value in train]
            train42 = [value % 42 for value in train]
            test42 = [value % 42 for value in test]
            model6 = fit_markov(train6)
            model7 = fit_markov(train7)
            model42 = fit_markov(train42)
            joint_loss = 0.0
            product_loss = 0.0
            events = len(test42) - 1
            for left, right in zip(test42, test42[1:]):
                left6, left7 = crt_decode_42(left)
                right6, right7 = crt_decode_42(right)
                joint_loss -= math.log(
                    markov_probability(model42, left, right, 42)
                )
                product_loss -= math.log(
                    markov_probability(model6, left6, right6, 6)
                    * markov_probability(model7, left7, right7, 7)
                )
            joint_loss /= events
            product_loss /= events
            rows.append({
                "policy": policy,
                "fold": fold_index,
                "train_end_index": train_end,
                "test_end_index": test_end,
                "events": events,
                "joint_mod42_log_loss": joint_loss,
                "product_mod6_mod7_log_loss": product_loss,
                "joint_advantage_bits": (
                    product_loss - joint_loss
                ) / math.log(2),
            })
    return rows


def reflection_tv(residues: list[int], modulus: int) -> float:
    edges = Counter(zip(residues, residues[1:]))
    total = sum(edges.values())
    support = set(edges)
    support.update(
        ((-left) % modulus, (-right) % modulus)
        for left, right in edges
    )
    difference = sum(
        abs(
            edges.get((left, right), 0)
            - edges.get(((-left) % modulus, (-right) % modulus), 0)
        )
        for left, right in support
    )
    return 0.5 * difference / total


def complement_rows(primes: list[int]) -> list[dict[str, object]]:
    rows = []
    for fold_index, (_, test_fraction) in enumerate(FOLDS, 1):
        test_start = int(N_PRIMES * (test_fraction - 0.10))
        test_end = int(N_PRIMES * test_fraction)
        test = primes[test_start:test_end]
        for modulus in COMPLEMENT_MODULI:
            rows.append({
                "fold": fold_index,
                "modulus": modulus,
                "test_start_index": test_start,
                "test_end_index": test_end,
                "reflection_tv": reflection_tv(
                    [value % modulus for value in test], modulus
                ),
            })
    return rows


def arithmetic_invariants(primes: list[int]) -> dict[str, object]:
    units30 = [value for value in range(30) if math.gcd(value, 30) == 1]
    units360 = [
        value for value in range(360) if math.gcd(value, 360) == 1
    ]
    lifts = {
        str(residue): sum(value % 30 == residue for value in units360)
        for residue in units30
    }
    common_angles = [
        degree for degree in range(360)
        if degree % 15 == 0 and degree % 6 == 0
    ]
    crt_roundtrip = all(
        crt_encode_6_7(*crt_decode_42(value)) == value
        for value in range(42)
    )
    all_prime_coordinates_roundtrip = all(
        crt_encode_6_7(prime % 6, prime % 7) == prime % 42
        for prime in primes
    )
    prime_mod6_exceptions = [
        prime for prime in primes if prime > 3 and prime % 6 not in (1, 5)
    ]
    transitions = Counter()
    exact_gap_counts = Counter()
    selected = [prime for prime in primes if prime > 3]
    for left, right in zip(selected, selected[1:]):
        transitions[f"{left % 6}->{right % 6}"] += 1
        exact_gap_counts[right - left] += 1
    return {
        "mod6": {
            "allowed_prime_residues_after_3": [1, 5],
            "exceptions_in_input": prime_mod6_exceptions,
            "transition_counts": dict(sorted(transitions.items())),
            "exact_gap_2_count": exact_gap_counts[2],
            "exact_gap_4_count": exact_gap_counts[4],
        },
        "crt_6_7_42": {
            "formula": "(7*a + 36*b) mod 42",
            "all_42_states_roundtrip": crt_roundtrip,
            "all_prime_coordinates_roundtrip": all_prime_coordinates_roundtrip,
        },
        "wheel_lift": {
            "radical_360": radical(360),
            "phi_280": euler_phi(280),
            "phi_360": euler_phi(360),
            "units_mod30": units30,
            "unit_lifts_mod360_per_mod30_class": lifts,
        },
        "grid_intersections": {
            "lcm_20_24_30": math.lcm(20, 24, 30),
            "lcm_7_17_30": math.lcm(7, 17, 30),
            "common_24_node_60_tick_angles_degrees": common_angles,
            "common_angle_count": len(common_angles),
            "360_refines": [
                divisor for divisor in (20, 24, 30, 60, 120)
                if 360 % divisor == 0
            ],
        },
    }


def paired_bootstrap(
    differences: list[float],
    seed_offset: int,
) -> tuple[float, float, float]:
    rng = random.Random(deterministic_seed(seed_offset))
    samples = []
    for _ in range(BOOTSTRAP_RUNS):
        samples.append(statistics.fmean(
            differences[rng.randrange(len(differences))]
            for _ in differences
        ))
    samples.sort()
    return (
        statistics.fmean(differences),
        samples[int(0.025 * BOOTSTRAP_RUNS)],
        samples[int(0.975 * BOOTSTRAP_RUNS) - 1],
    )


def rounded(value: object) -> object:
    if isinstance(value, float):
        return round(value, 12)
    if isinstance(value, dict):
        return {key: rounded(item) for key, item in value.items()}
    if isinstance(value, list):
        return [rounded(item) for item in value]
    return value


def aggregate_predictions(
    predictions: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows = []
    for policy in POLICIES:
        for modulus in SCAN_MODULI:
            selected = [
                row for row in predictions
                if row["policy"] == policy and row["modulus"] == modulus
            ]
            rows.append({
                "policy": policy,
                "modulus": modulus,
                "phi": euler_phi(modulus),
                "radical": radical(modulus),
                "mean_information_gain_bits": statistics.fmean(
                    float(row["information_gain_bits"]) for row in selected
                ),
                "mean_normalized_gain": statistics.fmean(
                    float(row["normalized_gain"]) for row in selected
                ),
                "mean_markov_accuracy": statistics.fmean(
                    float(row["markov_accuracy"]) for row in selected
                ),
                "mean_marginal_accuracy": statistics.fmean(
                    float(row["marginal_accuracy"]) for row in selected
                ),
            })
    return rows


def summary_from(
    predictions: list[dict[str, object]],
    aggregates: list[dict[str, object]],
    products: list[dict[str, object]],
    complements: list[dict[str, object]],
    invariants: dict[str, object],
) -> dict[str, object]:
    mod6_decisions = {}
    interaction = {}
    matched = {}
    for policy_index, policy in enumerate(POLICIES):
        mod6 = [
            row for row in predictions
            if row["policy"] == policy and row["modulus"] == 6
        ]
        mean_gain = statistics.fmean(
            float(row["information_gain_bits"]) for row in mod6
        )
        max_p = max(float(row["null_empirical_p"]) for row in mod6)
        mod6_decisions[policy] = {
            "mean_information_gain_bits": mean_gain,
            "max_null_empirical_p": max_p,
            "supported": mean_gain > 0 and max_p <= 0.05,
        }

        product_selected = [
            row for row in products if row["policy"] == policy
        ]
        product_diffs = [
            float(row["joint_advantage_bits"]) for row in product_selected
        ]
        mean, low, high = paired_bootstrap(
            product_diffs, 100 + policy_index
        )
        interaction[policy] = {
            "joint_advantage_mean_bits": mean,
            "bootstrap_95_ci": [low, high],
            "joint_interaction_supported": low > 0,
        }

        selected280 = [
            row for row in predictions
            if row["policy"] == policy and row["modulus"] == 280
        ]
        selected360 = [
            row for row in predictions
            if row["policy"] == policy and row["modulus"] == 360
        ]
        differences = [
            float(right["normalized_gain"]) - float(left["normalized_gain"])
            for left, right in zip(selected280, selected360)
        ]
        mean, low, high = paired_bootstrap(differences, 200 + policy_index)
        matched[policy] = {
            "mod360_minus_mod280_normalized_gain": mean,
            "bootstrap_95_ci": [low, high],
            "distinguishable": low > 0 or high < 0,
        }

    aggregate_map = {
        int(row["modulus"]): float(row["mean_normalized_gain"])
        for row in aggregates if row["policy"] == "all_primes"
    }
    curvatures = {
        center: (
            aggregate_map[center - 1]
            - 2 * aggregate_map[center]
            + aggregate_map[center + 1]
        )
        for center in range(6, 60)
    }
    target = abs(curvatures[32])
    percentile = sum(
        abs(value) <= target for value in curvatures.values()
    ) / len(curvatures)
    complement_summary = {
        str(modulus): statistics.fmean(
            float(row["reflection_tv"]) for row in complements
            if row["modulus"] == modulus
        )
        for modulus in COMPLEMENT_MODULI
    }
    decisions = {
        "mod6_dual_transition_supported": all(
            item["supported"] for item in mod6_decisions.values()
        ),
        "crt_6_7_42_exact": bool(
            invariants["crt_6_7_42"]["all_42_states_roundtrip"]
            and invariants["crt_6_7_42"]["all_prime_coordinates_roundtrip"]
        ),
        "joint_mod42_interaction_supported": all(
            item["joint_interaction_supported"]
            for item in interaction.values()
        ),
        "mod280_mod360_distinguishable": all(
            item["distinguishable"] for item in matched.values()
        ),
        "boundary_31_32_33_flagged": percentile >= 0.95,
        "stabilization_supported": False,
    }
    return rounded({
        "experiment": "wheel_product_reference_spaces_01",
        "input": {
            "prime_count": N_PRIMES,
            "policies": list(POLICIES),
            "folds": len(FOLDS),
            "scan_moduli": list(SCAN_MODULI),
            "mod6_null_runs_per_fold": NULL_RUNS_MOD6,
            "bootstrap_runs": BOOTSTRAP_RUNS,
        },
        "mod6": mod6_decisions,
        "mod42_product": interaction,
        "mod280_vs_mod360": matched,
        "boundary_31_32_33": {
            "normalized_gain_31": aggregate_map[31],
            "normalized_gain_32": aggregate_map[32],
            "normalized_gain_33": aggregate_map[33],
            "curvature_at_32": curvatures[32],
            "absolute_curvature_percentile": percentile,
            "flagged_at_95_percent": percentile >= 0.95,
        },
        "mean_reflection_tv": complement_summary,
        "decisions": decisions,
    })


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow(rounded(row))


def results_markdown(
    summary: dict[str, object],
    invariants: dict[str, object],
) -> str:
    decisions = summary["decisions"]
    boundary = summary["boundary_31_32_33"]
    lines = [
        "# Results",
        "",
        "Status: deterministic evidence generated from the frozen specification.",
        "",
        "## Decision summary",
        "",
        "| Claim | Result |",
        "|---|---|",
        f"| Mod 6 carries held-out dual transition information | "
        f"{'SUPPORTED' if decisions['mod6_dual_transition_supported'] else 'NOT SUPPORTED'} |",
        f"| `Z/42Z ↔ Z/6Z × Z/7Z` round-trip is exact | "
        f"{'SUPPORTED' if decisions['crt_6_7_42_exact'] else 'NOT SUPPORTED'} |",
        f"| Mod-42 transitions require joint 6×7 interaction | "
        f"{'SUPPORTED' if decisions['joint_mod42_interaction_supported'] else 'NOT SUPPORTED'} |",
        f"| Mod 280 and 360 differ under matched normalized gain | "
        f"{'SUPPORTED' if decisions['mod280_mod360_distinguishable'] else 'NOT SUPPORTED'} |",
        f"| The 31/32/33 boundary is a top-5% local anomaly | "
        f"{'SUPPORTED' if decisions['boundary_31_32_33_flagged'] else 'NOT SUPPORTED'} |",
        "| Any tested modulus stabilizes dynamics | NOT TESTED / NOT SUPPORTED |",
        "",
        "## Mod 6",
        "",
        "| Policy | Mean information gain (bits/event) | Maximum null p |",
        "|---|---:|---:|",
    ]
    for policy in POLICIES:
        item = summary["mod6"][policy]
        lines.append(
            f"| `{policy}` | {item['mean_information_gain_bits']:.6f} | "
            f"{item['max_null_empirical_p']:.6f} |"
        )
    mod6 = invariants["mod6"]
    lines.extend([
        "",
        f"All primes greater than 3 occupied only residues 1 and 5. "
        f"Exceptions: `{mod6['exceptions_in_input']}`. Exact gap-2 pairs: "
        f"{mod6['exact_gap_2_count']}; exact gap-4 pairs: "
        f"{mod6['exact_gap_4_count']}.",
        "",
        "## Mod 42 as a product reference space",
        "",
        "| Policy | Joint advantage (bits/event) | 95% paired bootstrap CI |",
        "|---|---:|---:|",
    ])
    for policy in POLICIES:
        item = summary["mod42_product"][policy]
        ci = item["bootstrap_95_ci"]
        lines.append(
            f"| `{policy}` | {item['joint_advantage_mean_bits']:.6f} | "
            f"[{ci[0]:.6f}, {ci[1]:.6f}] |"
        )
    lines.extend([
        "",
        "The coordinate equivalence is exhaustive and exact. The interaction "
        "result concerns only whether independent Mod-6 and Mod-7 transition "
        "models reproduce the joint Mod-42 transition kernel.",
        "",
        "## Mod 280 versus Mod 360",
        "",
        "| Policy | Normalized-gain difference `360-280` | 95% CI |",
        "|---|---:|---:|",
    ])
    for policy in POLICIES:
        item = summary["mod280_vs_mod360"][policy]
        ci = item["bootstrap_95_ci"]
        lines.append(
            f"| `{policy}` | "
            f"{item['mod360_minus_mod280_normalized_gain']:.6f} | "
            f"[{ci[0]:.6f}, {ci[1]:.6f}] |"
        )
    lines.extend([
        "",
        "## 31/32/33 boundary",
        "",
        f"Normalized gains: 31 = {boundary['normalized_gain_31']:.6f}, "
        f"32 = {boundary['normalized_gain_32']:.6f}, "
        f"33 = {boundary['normalized_gain_33']:.6f}.",
        "",
        f"Local curvature percentile: "
        f"{100 * boundary['absolute_curvature_percentile']:.2f}%. "
        f"Predeclared 95% anomaly flag: "
        f"{'YES' if boundary['flagged_at_95_percent'] else 'NO'}.",
        "",
        "## Exact wheel facts",
        "",
        f"- `rad(360) = {invariants['wheel_lift']['radical_360']}`.",
        f"- `phi(280) = {invariants['wheel_lift']['phi_280']}` and "
        f"`phi(360) = {invariants['wheel_lift']['phi_360']}`.",
        f"- `lcm(20,24,30) = "
        f"{invariants['grid_intersections']['lcm_20_24_30']}`.",
        f"- The 24-node and 60-tick grids meet at "
        f"{invariants['grid_intersections']['common_angle_count']} angles.",
        "",
        "## Interpretation boundary",
        "",
        "Arithmetic round-trips establish coordinate equivalence, not dynamic "
        "independence. Held-out predictability establishes descriptive sequence "
        "structure, not attraction, recovery or stabilization. Polar and wheel "
        "representations remain representations of these records.",
        "",
    ])
    return "\n".join(lines)


def generate(output_root: Path) -> None:
    primes = first_n_primes(N_PRIMES)
    predictions = prediction_rows(primes)
    aggregates = aggregate_predictions(predictions)
    products = product_rows(primes)
    complements = complement_rows(primes)
    invariants = rounded(arithmetic_invariants(primes))
    summary = summary_from(
        predictions, aggregates, products, complements, invariants
    )
    write_csv(output_root / "results/prediction_folds.csv", predictions)
    write_csv(output_root / "results/modulus_summary.csv", aggregates)
    write_csv(output_root / "results/product_folds.csv", products)
    write_csv(output_root / "results/complement_folds.csv", complements)
    results_dir = output_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / "arithmetic_invariants.json").write_text(
        json.dumps(invariants, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (results_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_root / "RESULTS.md").write_text(
        results_markdown(summary, invariants), encoding="utf-8"
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65_536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_checksums() -> None:
    lines = [
        f"{sha256(ROOT / path)}  {path.as_posix()}"
        for path in CHECKSUM_PATHS
    ]
    (ROOT / "SHA256SUMS").write_text(
        "\n".join(lines) + "\n", encoding="ascii"
    )


def verify_checksums() -> None:
    for line in (ROOT / "SHA256SUMS").read_text(
        encoding="ascii"
    ).splitlines():
        expected, relative = line.split("  ", 1)
        if sha256(ROOT / relative) != expected:
            raise SystemExit(f"checksum mismatch: {relative}")


def check_replay() -> None:
    with tempfile.TemporaryDirectory(prefix="nexah-wheel-product-") as temp:
        candidate = Path(temp)
        generate(candidate)
        for relative in GENERATED_PATHS:
            if (ROOT / relative).read_bytes() != (
                candidate / relative
            ).read_bytes():
                raise SystemExit(f"byte mismatch: {relative}")
    verify_checksums()
    print("PASS: generated evidence is byte-stable and checksums are valid")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    if arguments.check:
        check_replay()
    else:
        generate(ROOT)
        write_checksums()
        print("PASS: deterministic evidence and checksums generated")


if __name__ == "__main__":
    main()
