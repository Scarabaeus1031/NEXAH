#!/usr/bin/env python3
"""Replay the Q106 prime-index, radix-mirror and root-growth audit."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def primes(count: int) -> list[int]:
    found: list[int] = []
    candidate = 2
    while len(found) < count:
        if all(candidate % p for p in found if p * p <= candidate):
            found.append(candidate)
        candidate += 1
    return found


def validate() -> dict[str, object]:
    contract = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, observed: object, expected: object) -> None:
        checks.append({
            "name": name,
            "status": "PASS" if passed else "FAIL",
            "observed": observed,
            "expected": expected,
        })

    check(
        "existing identity reused without creation",
        contract["identity"]["reuse"] == "A0OE:PASCAL_PENTAGON_D5_TEST"
        and contract["identity"]["creates"] == [],
        contract["identity"],
        {"reuse": "A0OE:PASCAL_PENTAGON_D5_TEST", "creates": []},
    )

    paths: dict[str, Path] = {}
    source_resolution: dict[str, object] = {}
    for name, spec in contract["frozen_sources"].items():
        path = ROOT / spec["path"]
        paths[name] = path
        observed = sha256(path) if path.exists() else None
        source_resolution[name] = {"path": spec["path"], "sha256": observed}
        check(f"frozen source {name}", observed == spec["sha256"], observed, spec["sha256"])

    with paths["q106_nodes"].open(newline="", encoding="utf-8") as handle:
        nodes = list(csv.DictReader(handle))
    automorphisms = json.loads(paths["q106_automorphisms"].read_text(encoding="utf-8"))
    permutations = [action["permutation_zero_based"] for action in automorphisms["actions"]]

    level_counts = dict(sorted(Counter(int(node["level_n"]) for node in nodes).items()))
    expected_levels = {0: 1, 1: 5, 2: 10, 3: 15, 4: 20, 5: 25, 6: 30}
    check("M1 frozen level counts", level_counts == expected_levels, level_counts, expected_levels)

    q_sequence = [sum(count for level, count in level_counts.items() if level <= m) for m in range(7)]
    formula_sequence = [1 + 5 * m * (m + 1) // 2 for m in range(7)]
    first = [b - a for a, b in zip(q_sequence, q_sequence[1:])]
    second = [b - a for a, b in zip(first, first[1:])]
    residual = [q_sequence[-1] - q for q in q_sequence]
    residual_first = [b - a for a, b in zip(residual, residual[1:])]
    residual_second = [b - a for a, b in zip(residual_first, residual_first[1:])]
    check("M1 triangular Q sequence", q_sequence == formula_sequence == [1, 6, 16, 31, 51, 76, 106], q_sequence, formula_sequence)
    check("M1 discrete convexity", first == [5, 10, 15, 20, 25, 30] and second == [5] * 5, {"first": first, "second": second}, {"second": [5] * 5})
    check("M1 residual discrete concavity", residual_second == [-5] * 5, {"residual": residual, "second": residual_second}, {"second": [-5] * 5})
    parity = ["odd" if value % 2 else "even" for value in q_sequence]
    check("M1 parity sequence", parity == ["odd", "even", "even", "odd", "odd", "even", "even"], parity, ["odd", "even", "even", "odd", "odd", "even", "even"])

    seed = {
        "sum": 2 + 3,
        "product": 2 * 3,
        "ratio": str(Fraction(2, 3)),
        "power_2_cubed": 2**3,
        "q2": q_sequence[2],
    }
    check("M2 2+3 supplies fivefold coefficient", seed["sum"] == 5, seed["sum"], 5)
    check("M2 2*3 equals Q1", seed["product"] == q_sequence[1] == 6, {"product": seed["product"], "Q1": q_sequence[1]}, 6)
    check("M2 2/3 is rational and not integer six", Fraction(2, 3) != 6 and 2 == 0 * 3 + 2, seed["ratio"], "2/3 (decimal 0.666...)")
    check("M2 2^3 retained only as external comparator", seed["power_2_cubed"] == 8 and 8 not in q_sequence, {"2^3": 8, "in_Q": 8 in q_sequence}, {"2^3": 8, "in_Q": False})
    check("M2 Q2 is 2^4 rather than 2^3", q_sequence[2] == 2**4 and q_sequence[2] != 2**3, q_sequence[2], 16)

    seen: set[int] = set()
    orbits: list[list[int]] = []
    for node in range(len(nodes)):
        if node in seen:
            continue
        orbit = sorted({permutation[node] for permutation in permutations})
        seen.update(orbit)
        orbits.append(orbit)
    profile = dict(sorted(Counter(len(orbit) for orbit in orbits).items()))
    check("M3 frozen D5 orbit profile", profile == {1: 1, 5: 9, 10: 6}, profile, {1: 1, 5: 9, 10: 6})

    orbit_count = len(orbits)
    five_orbits = profile.get(5, 0)
    final_interior = sum(1 for node in nodes if node["kind"] == "interior" and int(node["level_n"]) == 6)
    p = primes(25)
    prime_joint = {
        "O": orbit_count,
        "F": five_orbits,
        "L": final_interior,
        "p_O": p[orbit_count - 1],
        "p_L": p[final_interior - 1],
        "index_steps": final_interior - orbit_count,
        "strictly_between": final_interior - orbit_count - 1,
    }
    check("M3 O+F reaches final-level interior count", orbit_count + five_orbits == final_interior == 25, prime_joint, {"O": 16, "F": 9, "L": 25})
    check("M3 prime-index endpoints", prime_joint["p_O"] == 53 and prime_joint["p_L"] == 97, {"p16": prime_joint["p_O"], "p25": prime_joint["p_L"]}, {"p16": 53, "p25": 97})
    check("M3 Q106 prime-index identities", 106 == 2 * prime_joint["p_O"] and 106 - five_orbits == prime_joint["p_L"], {"2*p16": 2 * prime_joint["p_O"], "106-F": 106-five_orbits}, {"2*p16": 106, "106-F": 97})
    check("M3 prime endpoint closure", prime_joint["p_O"] + prime_joint["p_L"] == 150, prime_joint["p_O"] + prime_joint["p_L"], 150)
    check("M3 prime-index distance", prime_joint["index_steps"] == 9 and prime_joint["strictly_between"] == 8, {"steps": prime_joint["index_steps"], "strictly_between": prime_joint["strictly_between"]}, {"steps": 9, "strictly_between": 8})

    invariant_53 = 0
    for mask in range(1 << len(orbits)):
        if sum(len(orbits[i]) for i in range(len(orbits)) if mask & (1 << i)) == 53:
            invariant_53 += 1
    check("M4 no D5-invariant 53-node half", invariant_53 == 0 and 53 % 5 == 3, {"target": 53, "mod5": 53 % 5, "orbit_unions": invariant_53}, {"orbit_unions": 0})

    values = [53, 97, 100, 106, 150]
    bases = [20, 40, 50]
    coordinates = {str(n): {str(b): [n // b, n % b] for b in bases} for n in values}
    expected_coordinates = {
        "53": {"20": [2, 13], "40": [1, 13], "50": [1, 3]},
        "97": {"20": [4, 17], "40": [2, 17], "50": [1, 47]},
        "100": {"20": [5, 0], "40": [2, 20], "50": [2, 0]},
        "106": {"20": [5, 6], "40": [2, 26], "50": [2, 6]},
        "150": {"20": [7, 10], "40": [3, 30], "50": [3, 0]},
    }
    check("M5 radix coordinates", coordinates == expected_coordinates, coordinates, expected_coordinates)
    preserved = all(coordinates[str(n)]["20"][1] == coordinates[str(n)]["40"][1] and coordinates[str(n)]["20"][0] == 2 * coordinates[str(n)]["40"][0] for n in (53, 97))
    check("M5 53 and 97 preserve columns under 20-to-40 row halving", preserved, {str(n): {"b20": coordinates[str(n)]["20"], "b40": coordinates[str(n)]["40"]} for n in (53, 97)}, "same column; b20 row = 2*b40 row")
    check("M5 Q106 does not preserve its column under 20-to-40", coordinates["106"]["20"][1] != coordinates["106"]["40"][1], {"b20": coordinates["106"]["20"], "b40": coordinates["106"]["40"]}, "columns differ")

    mirror = lambda x: 150 - x
    mirror_domain = range(50, 101)
    involution = all(mirror(mirror(x)) == x for x in mirror_domain)
    fixed = [x for x in mirror_domain if mirror(x) == x]
    check("M5 J50 is an involution with fixed point 75", involution and fixed == [75], {"involution": involution, "fixed": fixed}, {"involution": True, "fixed": [75]})
    check("M5 J50 swaps prime endpoints and closes at 150", mirror(53) == 97 and mirror(97) == 53 and 53 + 97 == 150, {"J50(53)": mirror(53), "J50(97)": mirror(97), "sum": 150}, {"J50(53)": 97, "J50(97)": 53, "sum": 150})

    ratios = [Fraction(q_sequence[i], q_sequence[i - 1]) for i in range(1, len(q_sequence))]
    fractal = {
        "status": "NOT_ESTABLISHED",
        "quadratic_growth": second == [5] * 5,
        "constant_scale_ratio": len(set(ratios)) == 1,
        "recursive_substitution_supplied": False,
        "ratios": [str(ratio) for ratio in ratios],
    }
    check("M6 quadratic growth is not promoted to a fractal", fractal["quadratic_growth"] and not fractal["constant_scale_ratio"] and not fractal["recursive_substitution_supplied"] and fractal["status"] == "NOT_ESTABLISHED", fractal, {"status": "NOT_ESTABLISHED"})

    passed = all(item["status"] == "PASS" for item in checks)
    classification = "PASS_EXACT_ORBIT_PRIME_RADIX_ROOT_GROWTH_WITH_FRACTAL_OPEN" if passed else "CONTRACT_INVALID"
    return {
        "contract_id": contract["contract_id"],
        "date": contract["date"],
        "classification": classification,
        "summary": {"passed": sum(item["status"] == "PASS" for item in checks), "total": len(checks)},
        "source_resolution": source_resolution,
        "derived": {
            "q_sequence": q_sequence,
            "first_differences": first,
            "second_differences": second,
            "residual_sequence": residual,
            "parity": parity,
            "seed_235": seed,
            "orbit_profile": {str(k): v for k, v in profile.items()},
            "prime_joint": prime_joint,
            "radix_coordinates": coordinates,
            "fractal": fractal
        },
        "checks": checks,
        "claim_boundary": contract["claim_boundary"],
    }


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["classification"].startswith("PASS_") else 1)
