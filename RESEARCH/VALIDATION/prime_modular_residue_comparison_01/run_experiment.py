#!/usr/bin/env python3
"""Deterministic held-out comparison of prime residue spaces."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import statistics
import tempfile
from pathlib import Path


N_PRIMES = 20_000
MODULI = (5, 7, 11, 13, 17, 19, 23)
POLICIES = ("all_primes", "without_2_3")
FOLDS = ((0.50, 0.60), (0.60, 0.70), (0.70, 0.80),
         (0.80, 0.90), (0.90, 1.00))
ALPHA = 0.5
NULL_RUNS = 100
BOOTSTRAP_RUNS = 10_000
SEED = 20_260_725
BRIDGE_DELTA = 8
SENSITIVITY_THRESHOLD_BITS = 0.001

ROOT = Path(__file__).resolve().parent
GENERATED_PATHS = (
    Path("RESULTS.md"),
    Path("results/prediction_folds.csv"),
    Path("results/bridge_folds.csv"),
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
    if count < 6:
        limit = 15
    else:
        limit = int(count * (math.log(count) + math.log(math.log(count)))) + 10
    while True:
        sieve = bytearray(b"\x01") * (limit + 1)
        sieve[0:2] = b"\x00\x00"
        for candidate in range(2, math.isqrt(limit) + 1):
            if sieve[candidate]:
                start = candidate * candidate
                step_count = ((limit - start) // candidate) + 1
                sieve[start:limit + 1:candidate] = b"\x00" * step_count
        primes = [value for value, is_prime in enumerate(sieve) if is_prime]
        if len(primes) >= count:
            return primes[:count]
        limit *= 2


def policy_slice(values: list[int], end: int, policy: str) -> list[int]:
    selected = values[:end]
    if policy == "without_2_3":
        return [value for value in selected if value not in (2, 3)]
    if policy != "all_primes":
        raise ValueError(f"unknown policy: {policy}")
    return selected


def transition_model(residues: list[int], modulus: int) -> list[list[float]]:
    counts = [[ALPHA for _ in range(modulus)] for _ in range(modulus)]
    for left, right in zip(residues, residues[1:]):
        counts[left][right] += 1.0
    return [[item / sum(row) for item in row] for row in counts]


def marginal_model(residues: list[int], modulus: int) -> list[float]:
    counts = [ALPHA for _ in range(modulus)]
    for residue in residues[1:]:
        counts[residue] += 1.0
    total = sum(counts)
    return [item / total for item in counts]


def evaluate_prediction(
    test_residues: list[int],
    transition: list[list[float]],
    marginal: list[float],
) -> dict[str, float]:
    if len(test_residues) < 2:
        raise ValueError("test sequence must contain at least two residues")
    markov_loss = 0.0
    marginal_loss = 0.0
    markov_hits = 0
    marginal_hits = 0
    marginal_choice = max(range(len(marginal)), key=marginal.__getitem__)
    events = len(test_residues) - 1
    for left, right in zip(test_residues, test_residues[1:]):
        markov_loss -= math.log(transition[left][right])
        marginal_loss -= math.log(marginal[right])
        markov_hits += max(
            range(len(transition[left])),
            key=transition[left].__getitem__,
        ) == right
        marginal_hits += marginal_choice == right
    markov_loss /= events
    marginal_loss /= events
    return {
        "events": events,
        "markov_log_loss": markov_loss,
        "marginal_log_loss": marginal_loss,
        "information_gain_bits": (marginal_loss - markov_loss) / math.log(2),
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
        for modulus in MODULI:
            for fold_index, (train_fraction, test_fraction) in enumerate(FOLDS, 1):
                train_end = int(N_PRIMES * train_fraction)
                test_end = int(N_PRIMES * test_fraction)
                train_values = policy_slice(primes, train_end, policy)
                test_values = primes[train_end:test_end]
                train_residues = [value % modulus for value in train_values]
                test_residues = [value % modulus for value in test_values]
                transition = transition_model(train_residues, modulus)
                marginal = marginal_model(train_residues, modulus)
                observed = evaluate_prediction(test_residues, transition, marginal)

                null_gains = []
                for null_index in range(NULL_RUNS):
                    shuffled = train_residues.copy()
                    rng = random.Random(deterministic_seed(
                        policy_index, modulus, fold_index, null_index
                    ))
                    rng.shuffle(shuffled)
                    null_transition = transition_model(shuffled, modulus)
                    null_result = evaluate_prediction(
                        test_residues, null_transition, marginal
                    )
                    null_gains.append(null_result["information_gain_bits"])
                null_mean = statistics.fmean(null_gains)
                null_sd = statistics.stdev(null_gains)
                null_z = (
                    (observed["information_gain_bits"] - null_mean) / null_sd
                    if null_sd else 0.0
                )
                null_p = (
                    1 + sum(
                        gain >= observed["information_gain_bits"]
                        for gain in null_gains
                    )
                ) / (NULL_RUNS + 1)
                rows.append({
                    "policy": policy,
                    "modulus": modulus,
                    "fold": fold_index,
                    "train_end_index": train_end,
                    "test_end_index": test_end,
                    "train_primes": len(train_values),
                    "test_primes": len(test_values),
                    **observed,
                    "null_mean_information_gain_bits": null_mean,
                    "null_sd_information_gain_bits": null_sd,
                    "null_z": null_z,
                    "null_empirical_p": null_p,
                })
    return rows


def learned_bridge_lookup(
    train_values: list[int],
) -> dict[int, int]:
    counts = {source: [0] * 17 for source in range(7)}
    for value in train_values:
        counts[value % 7][value % 17] += 1
    return {
        source: max(range(17), key=target_counts.__getitem__)
        for source, target_counts in counts.items()
    }


def bridge_rows(primes: list[int]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for policy in POLICIES:
        for fold_index, (train_fraction, test_fraction) in enumerate(FOLDS, 1):
            train_end = int(N_PRIMES * train_fraction)
            test_end = int(N_PRIMES * test_fraction)
            train_values = policy_slice(primes, train_end, policy)
            test_values = primes[train_end:test_end]
            target_counts = [0] * 17
            for value in train_values:
                target_counts[value % 17] += 1
            majority = max(range(17), key=target_counts.__getitem__)
            lookup = learned_bridge_lookup(train_values)
            fixed_hits = 0
            majority_hits = 0
            learned_hits = 0
            for value in test_values:
                source = value % 7
                target = value % 17
                fixed_hits += ((7 * source + BRIDGE_DELTA) % 17) == target
                majority_hits += majority == target
                learned_hits += lookup[source] == target
            count = len(test_values)
            rows.append({
                "policy": policy,
                "fold": fold_index,
                "train_end_index": train_end,
                "test_end_index": test_end,
                "train_primes": len(train_values),
                "test_primes": count,
                "fixed_delta": BRIDGE_DELTA,
                "fixed_accuracy": fixed_hits / count,
                "majority_accuracy": majority_hits / count,
                "learned_lookup_accuracy": learned_hits / count,
                "fixed_minus_majority": (fixed_hits - majority_hits) / count,
            })
    return rows


def paired_bootstrap_interval(
    differences: list[float],
    seed_offset: int,
) -> tuple[float, float, float]:
    rng = random.Random(deterministic_seed(seed_offset))
    samples = []
    for _ in range(BOOTSTRAP_RUNS):
        draw = [differences[rng.randrange(len(differences))]
                for _ in differences]
        samples.append(statistics.fmean(draw))
    samples.sort()
    low = samples[int(0.025 * BOOTSTRAP_RUNS)]
    high = samples[int(0.975 * BOOTSTRAP_RUNS) - 1]
    return statistics.fmean(differences), low, high


def rounded(value: object) -> object:
    if isinstance(value, float):
        return round(value, 12)
    if isinstance(value, dict):
        return {key: rounded(item) for key, item in value.items()}
    if isinstance(value, list):
        return [rounded(item) for item in value]
    return value


def build_summary(
    predictions: list[dict[str, object]],
    bridges: list[dict[str, object]],
) -> dict[str, object]:
    aggregates: dict[str, dict[str, object]] = {}
    comparisons: dict[str, dict[str, object]] = {}
    bridge_summary: dict[str, dict[str, object]] = {}

    for policy_index, policy in enumerate(POLICIES):
        policy_aggregates: dict[str, object] = {}
        for modulus in MODULI:
            selected = [
                row for row in predictions
                if row["policy"] == policy and row["modulus"] == modulus
            ]
            policy_aggregates[str(modulus)] = {
                "mean_information_gain_bits": statistics.fmean(
                    float(row["information_gain_bits"]) for row in selected
                ),
                "mean_markov_accuracy": statistics.fmean(
                    float(row["markov_accuracy"]) for row in selected
                ),
                "mean_marginal_accuracy": statistics.fmean(
                    float(row["marginal_accuracy"]) for row in selected
                ),
                "mean_null_z": statistics.fmean(
                    float(row["null_z"]) for row in selected
                ),
                "max_null_empirical_p": max(
                    float(row["null_empirical_p"]) for row in selected
                ),
            }
        aggregates[policy] = policy_aggregates

        mod7 = [
            row for row in predictions
            if row["policy"] == policy and row["modulus"] == 7
        ]
        mod17 = [
            row for row in predictions
            if row["policy"] == policy and row["modulus"] == 17
        ]
        differences = [
            float(right["information_gain_bits"])
            - float(left["information_gain_bits"])
            for left, right in zip(mod7, mod17)
        ]
        mean_difference, ci_low, ci_high = paired_bootstrap_interval(
            differences, 100 + policy_index
        )
        ranked = sorted(
            (
                (modulus, float(policy_aggregates[str(modulus)]
                                ["mean_information_gain_bits"]))
                for modulus in MODULI
            ),
            key=lambda item: (-item[1], item[0]),
        )
        comparisons[policy] = {
            "mod17_minus_mod7_mean_bits": mean_difference,
            "bootstrap_95_ci": [ci_low, ci_high],
            "mod17_exceeds_mod7": ci_low > 0,
            "highest_gain_modulus": ranked[0][0],
            "mod17_is_highest": ranked[0][0] == 17,
            "ranking": [
                {"modulus": modulus, "mean_information_gain_bits": gain}
                for modulus, gain in ranked
            ],
        }

        selected_bridges = [
            row for row in bridges if row["policy"] == policy
        ]
        bridge_differences = [
            float(row["fixed_minus_majority"]) for row in selected_bridges
        ]
        bridge_mean, bridge_low, bridge_high = paired_bootstrap_interval(
            bridge_differences, 200 + policy_index
        )
        bridge_summary[policy] = {
            "mean_fixed_accuracy": statistics.fmean(
                float(row["fixed_accuracy"]) for row in selected_bridges
            ),
            "mean_majority_accuracy": statistics.fmean(
                float(row["majority_accuracy"]) for row in selected_bridges
            ),
            "mean_learned_lookup_accuracy": statistics.fmean(
                float(row["learned_lookup_accuracy"])
                for row in selected_bridges
            ),
            "fixed_minus_majority_mean": bridge_mean,
            "bootstrap_95_ci": [bridge_low, bridge_high],
            "fixed_bridge_supported": bridge_low > 0,
        }

    all_difference = float(
        comparisons["all_primes"]["mod17_minus_mod7_mean_bits"]
    )
    without_difference = float(
        comparisons["without_2_3"]["mod17_minus_mod7_mean_bits"]
    )
    sign_changed = (
        (all_difference > 0) != (without_difference > 0)
        if all_difference != 0 and without_difference != 0
        else all_difference != without_difference
    )
    sensitivity_delta = abs(all_difference - without_difference)
    sensitive = (
        sign_changed or sensitivity_delta > SENSITIVITY_THRESHOLD_BITS
    )
    prediction_supported = all(
        bool(comparisons[policy]["mod17_exceeds_mod7"])
        and bool(comparisons[policy]["mod17_is_highest"])
        for policy in POLICIES
    )
    fixed_bridge_supported = all(
        bool(bridge_summary[policy]["fixed_bridge_supported"])
        for policy in POLICIES
    )
    return rounded({
        "experiment": "prime_modular_residue_comparison_01",
        "input": {
            "prime_count": N_PRIMES,
            "first_primes": [2, 3],
            "moduli": list(MODULI),
            "folds": len(FOLDS),
            "null_runs_per_fold": NULL_RUNS,
            "bootstrap_runs": BOOTSTRAP_RUNS,
        },
        "prediction_aggregates": aggregates,
        "mod17_vs_mod7": comparisons,
        "prime_2_3_sensitivity": {
            "difference_change_bits": sensitivity_delta,
            "sign_changed": sign_changed,
            "threshold_bits": SENSITIVITY_THRESHOLD_BITS,
            "sensitive": sensitive,
        },
        "bridge_7_to_17": bridge_summary,
        "decisions": {
            "mod17_predictive_advantage_supported": prediction_supported,
            "fixed_7_to_17_bridge_supported": fixed_bridge_supported,
            "mod17_stabilization_supported": False,
            "stabilization_reason": (
                "No dynamical intervention or stability endpoint is present."
            ),
        },
    })


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow(rounded(row))


def format_bool(value: object) -> str:
    return "SUPPORTED" if value else "NOT SUPPORTED"


def results_markdown(summary: dict[str, object]) -> str:
    comparisons = summary["mod17_vs_mod7"]
    bridge = summary["bridge_7_to_17"]
    decisions = summary["decisions"]
    sensitivity = summary["prime_2_3_sensitivity"]
    lines = [
        "# Results",
        "",
        "Status: deterministic evidence generated from the frozen specification.",
        "",
        "## Decision summary",
        "",
        "| Claim | Result |",
        "|---|---|",
        (
            "| Modulo 17 has a held-out predictive advantage over modulo 7 "
            "and controls | "
            f"{format_bool(decisions['mod17_predictive_advantage_supported'])} |"
        ),
        (
            "| Fixed `(7*r7+8) mod 17` bridge exceeds the majority baseline | "
            f"{format_bool(decisions['fixed_7_to_17_bridge_supported'])} |"
        ),
        "| Modulo 17 stabilizes dynamics | NOT TESTED / NOT SUPPORTED |",
        "",
        "## Modulo 17 versus modulo 7",
        "",
        "| Prime policy | Mean difference (bits/event) | 95% paired bootstrap CI "
        "| Highest-gain modulus |",
        "|---|---:|---:|---:|",
    ]
    for policy in POLICIES:
        item = comparisons[policy]
        ci = item["bootstrap_95_ci"]
        lines.append(
            f"| `{policy}` | {item['mod17_minus_mod7_mean_bits']:.6f} | "
            f"[{ci[0]:.6f}, {ci[1]:.6f}] | "
            f"{item['highest_gain_modulus']} |"
        )
    lines.extend([
        "",
        "## Primes 2 and 3",
        "",
        "The canonical run includes 2 and 3. The sensitivity policy removes them "
        "only from the training prefix while keeping every test range unchanged.",
        "",
        f"Observed change in the modulo-17 minus modulo-7 estimate: "
        f"{sensitivity['difference_change_bits']:.6f} bits/event. "
        f"Predeclared sensitivity flag: "
        f"{'YES' if sensitivity['sensitive'] else 'NO'}.",
        "",
        "## Proposed 7-to-17 bridge",
        "",
        "| Prime policy | Fixed accuracy | Majority accuracy | Learned lookup "
        "| Fixed-minus-majority 95% CI |",
        "|---|---:|---:|---:|---:|",
    ])
    for policy in POLICIES:
        item = bridge[policy]
        ci = item["bootstrap_95_ci"]
        lines.append(
            f"| `{policy}` | {item['mean_fixed_accuracy']:.6f} | "
            f"{item['mean_majority_accuracy']:.6f} | "
            f"{item['mean_learned_lookup_accuracy']:.6f} | "
            f"[{ci[0]:.6f}, {ci[1]:.6f}] |"
        )
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "Modulo 17 exceeds modulo 7 in the held-out comparison, but modulo 23 "
        "has the highest gain under both policies. The predeclared specificity "
        "rule therefore rejects a special Mod-17 predictive status. This is "
        "evidence for modular transition structure in the tested prime sequence, "
        "not evidence that 17 is uniquely privileged.",
        "",
        "The fixed 7-to-17 rule does not exceed its training-only majority "
        "baseline. The observed interval spans zero, so the proposed affine "
        "bridge is not supported as a reconstructive mapping by this test.",
        "",
        "A predictive result concerns residue-sequence description. A bridge "
        "result concerns coordinate reconstruction. Neither is evidence of "
        "dynamical damping, recovery, attraction, error correction or stability. "
        "The repository's proposed Mod-17 stabilizer remains an unvalidated "
        "hypothesis after this experiment.",
        "",
    ])
    return "\n".join(lines)


def generate(output_root: Path) -> None:
    primes = first_n_primes(N_PRIMES)
    predictions = prediction_rows(primes)
    bridges = bridge_rows(primes)
    summary = build_summary(predictions, bridges)
    write_csv(output_root / "results/prediction_folds.csv", predictions)
    write_csv(output_root / "results/bridge_folds.csv", bridges)
    summary_path = output_root / "results/summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_root / "RESULTS.md").write_text(
        results_markdown(summary), encoding="utf-8"
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65_536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_checksums() -> None:
    lines = [f"{sha256(ROOT / path)}  {path.as_posix()}"
             for path in CHECKSUM_PATHS]
    (ROOT / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="ascii")


def verify_checksums() -> None:
    checksum_file = ROOT / "SHA256SUMS"
    for line in checksum_file.read_text(encoding="ascii").splitlines():
        expected, relative = line.split("  ", 1)
        actual = sha256(ROOT / relative)
        if actual != expected:
            raise SystemExit(f"checksum mismatch: {relative}")


def check_replay() -> None:
    with tempfile.TemporaryDirectory(prefix="nexah-prime-modular-") as temp:
        candidate_root = Path(temp)
        generate(candidate_root)
        for relative in GENERATED_PATHS:
            committed = (ROOT / relative).read_bytes()
            candidate = (candidate_root / relative).read_bytes()
            if committed != candidate:
                raise SystemExit(f"byte mismatch: {relative}")
    verify_checksums()
    print("PASS: generated evidence is byte-stable and checksums are valid")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="generate temporary candidates and compare with committed evidence",
    )
    arguments = parser.parse_args()
    if arguments.check:
        check_replay()
    else:
        generate(ROOT)
        write_checksums()
        print("PASS: deterministic evidence and checksums generated")


if __name__ == "__main__":
    main()
