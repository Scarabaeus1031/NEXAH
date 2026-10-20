#!/usr/bin/env python3
"""Replay the bounded Q106 square-index prime readout audit."""

from __future__ import annotations

import hashlib
import json
from itertools import product
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def primes(count: int) -> list[int]:
    found: list[int] = []
    candidate = 2
    while len(found) < count:
        limit = isqrt(candidate)
        if all(candidate % prime for prime in found if prime <= limit):
            found.append(candidate)
        candidate += 1
    return found


def validate() -> dict[str, object]:
    contract = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, observed: object, expected: object) -> None:
        checks.append(
            {
                "name": name,
                "status": "PASS" if passed else "FAIL",
                "observed": observed,
                "expected": expected,
            }
        )

    check(
        "existing Pascal/Q106 identity reused",
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

    pent04 = json.loads(paths["pent04_result"].read_text(encoding="utf-8"))
    q106 = json.loads(paths["q106_prime_result"].read_text(encoding="utf-8"))
    square_prime = json.loads(paths["square_prime_result"].read_text(encoding="utf-8"))

    projected_nodes = pent04["result"]["projected_node_count_per_hemisphere"]
    check(
        "M1 PENT-04 projects each hemisphere to Q106",
        pent04["checks"]["both_hemispheres_project_to_same_106_node_carrier"]
        and projected_nodes == 106,
        projected_nodes,
        106,
    )

    joint = q106["modules"]["M3_ORBIT_PRIME_INDEX_JOINT"]
    F, O, L, N = joint["F"], joint["O"], joint["L"], projected_nodes
    roots = [isqrt(F), isqrt(O), isqrt(L)]
    check(
        "M2 Q106 readout is the 3-4-5 square triple",
        [F, O, L] == [9, 16, 25]
        and [root * root for root in roots] == [F, O, L]
        and roots == [3, 4, 5],
        {"readout": [F, O, L, N], "roots": roots},
        {"readout": [9, 16, 25, 106], "roots": [3, 4, 5]},
    )
    check("M2 Pythagorean index closure", F + O == L, f"{F}+{O}={F + O}", "9+16=25")
    check(
        "M2 16 is a double square",
        O == (2**2) ** 2 == 2 ** (2**2) == 4**2,
        {"O": O, "(2^2)^2": (2**2) ** 2, "2^(2^2)": 2 ** (2**2)},
        16,
    )

    prime_values = primes(25)
    p = lambda index: prime_values[index - 1]
    lifted = [p(root * root) for root in roots]
    inherited = square_prime["modules"]["M3_SQUARE_INDEX_PRIME_LADDER"]
    check(
        "M3 standard one-based square-index prime lift",
        lifted == [23, 53, 97]
        and inherited["square_indices"] == [1, 4, 9, 16, 25]
        and inherited["primes"] == [2, 7, 23, 53, 97],
        {"roots": roots, "lifted": lifted},
        {"roots": [3, 4, 5], "lifted": [23, 53, 97]},
    )

    square_indices = [root * root for root in range(1, 6)]
    square_index_primes = [p(index) for index in square_indices]
    adjacent_sums = [a + b for a, b in zip(square_index_primes, square_index_primes[1:])]
    check(
        "M3 five-root adjacent-sum ladder",
        adjacent_sums == [9, 30, 76, 150],
        adjacent_sums,
        [9, 30, 76, 150],
    )

    p5, p9, p16, p25 = p(5), p(9), p(16), p(25)
    closure = {
        "p25_minus_p16": p25 - p16,
        "four_p5": 4 * p5,
        "Q106_minus_p25": N - p25,
        "four_p5_plus_3_squared": 4 * p5 + 3**2,
        "two_p16": 2 * p16,
    }
    check(
        "M4 exact C-closure",
        closure
        == {
            "p25_minus_p16": 44,
            "four_p5": 44,
            "Q106_minus_p25": 9,
            "four_p5_plus_3_squared": 53,
            "two_p16": 106,
        },
        closure,
        {"97-53": 44, "4*p5": 44, "106-97": 9, "44+9": 53, "2*p16": 106},
    )
    check(
        "M4 closure returns to p16 and Q106",
        4 * p5 + 3**2 == p16 and p25 + 3**2 == N and 2 * p16 == N,
        {"44+9": 4 * p5 + 3**2, "97+9": p25 + 3**2, "53+53": 2 * p16},
        {"p16": 53, "Q106": 106},
    )

    squared_primes = [p(root) ** 2 for root in roots]
    check(
        "M5 square-index primes remain distinct from squared primes",
        lifted == [23, 53, 97] and squared_primes == [25, 49, 121] and lifted != squared_primes,
        {"p_(n^2)": lifted, "(p_n)^2": squared_primes},
        {"distinct": True},
    )
    check(
        "M5 prime values are not a Pythagorean triple",
        p9**2 + p16**2 != p25**2,
        {"23^2+53^2": p9**2 + p16**2, "97^2": p25**2},
        "not equal",
    )

    profile = {int(size): count for size, count in joint["orbit_profile"].items()}
    invariant_53_witnesses = [
        [ones, fives, tens]
        for ones, fives, tens in product(
            range(profile.get(1, 0) + 1),
            range(profile.get(5, 0) + 1),
            range(profile.get(10, 0) + 1),
        )
        if ones + 5 * fives + 10 * tens == 53
    ]
    check(
        "M6 no D5-invariant 53-node orbit union",
        invariant_53_witnesses == [],
        invariant_53_witnesses,
        [],
    )

    consecutive_hits = [
        value
        for value in range(1, 10001)
        if value**2 + (value + 1) ** 2 == (value + 2) ** 2
    ]
    check(
        "M7 3-4-5 is the unique positive consecutive-root hit through 10000",
        consecutive_hits == [3],
        consecutive_hits,
        [3],
    )
    check(
        "M7 exact uniqueness factorization",
        all(
            value**2 + (value + 1) ** 2 - (value + 2) ** 2 == (value - 3) * (value + 1)
            for value in range(1, 101)
        ),
        "a^2+(a+1)^2-(a+2)^2=(a-3)(a+1)",
        "identity holds",
    )

    passed = all(item["status"] == "PASS" for item in checks)
    classification = (
        "PASS_EXACT_SQUARE_INDEX_PRIME_READOUT_WITH_NO_D5_INVARIANT_53_SUBCARRIER"
        if passed
        else "FAIL_ARITHMETIC_OR_SOURCE_INTEGRITY"
    )
    return {
        "contract_id": contract["contract_id"],
        "date": contract["date"],
        "classification": classification,
        "summary": {
            "passed": sum(item["status"] == "PASS" for item in checks),
            "total": len(checks),
            "failed": sum(item["status"] == "FAIL" for item in checks),
        },
        "source_resolution": source_resolution,
        "readout": {
            "Q106": {"F": F, "O": O, "L": L, "N": N},
            "square_roots": roots,
            "square_indices": [F, O, L],
            "square_index_primes": lifted,
            "five_root_ladder": {
                "indices": square_indices,
                "primes": square_index_primes,
                "adjacent_sums": adjacent_sums,
            },
            "closure": closure,
            "D5_invariant_53_witnesses": invariant_53_witnesses,
            "consecutive_root_hits_1_to_10000": consecutive_hits,
        },
        "checks": checks,
        "claim_boundary": contract["claim_boundary"],
    }


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["classification"].startswith("PASS_") else 1)
