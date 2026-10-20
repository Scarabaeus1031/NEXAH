#!/usr/bin/env python3
"""Run the bounded 46/106/194 contrast for the frozen Q106 lens."""

from __future__ import annotations

import argparse
import hashlib
import json
from math import log
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[7]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def first_n_primes(count: int) -> list[int]:
    if count < 1:
        return []
    limit = 15 if count < 6 else int(count * (log(count) + log(log(count)))) + 100
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for prime in range(2, int(limit**0.5) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (((limit - start) // prime) + 1)
    values = [value for value, is_prime in enumerate(sieve) if is_prime]
    if len(values) < count:
        raise RuntimeError("deterministic prime bound was insufficient")
    return values[:count]


def run() -> dict[str, object]:
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
        "existing identity reused with no created identity",
        contract["identity"]["reuse"] == "A0OE:PASCAL_PENTAGON_D5_TEST"
        and contract["identity"]["creates"] == [],
        contract["identity"],
        {"reuse": "A0OE:PASCAL_PENTAGON_D5_TEST", "creates": []},
    )

    source_path = ROOT / contract["frozen_source"]["path"]
    source_hash = sha256(source_path) if source_path.exists() else None
    check(
        "frozen Q106 square-index source integrity",
        source_hash == contract["frozen_source"]["sha256"],
        source_hash,
        contract["frozen_source"]["sha256"],
    )
    source = json.loads(source_path.read_text(encoding="utf-8"))
    check(
        "frozen source classification",
        source["classification"]
        == "PASS_EXACT_SQUARE_INDEX_PRIME_READOUT_WITH_NO_D5_INVARIANT_53_SUBCARRIER",
        source["classification"],
        "PASS_EXACT_SQUARE_INDEX_PRIME_READOUT_WITH_NO_D5_INVARIANT_53_SUBCARRIER",
    )

    maximum_k = contract["declared_windows"]["finite_scan"]["maximum_k"]
    primes = first_n_primes((maximum_k + 1) ** 2)
    p = lambda index: primes[index - 1]

    homologues = []
    for k in contract["declared_windows"]["homologues"]:
        left = p((k - 1) ** 2)
        center = p(k**2)
        right = p((k + 1) ** 2)
        carrier = 2 * center
        residual = carrier - right
        target = (k - 1) ** 2
        homologues.append({
            "k": k,
            "square_indices": [(k - 1) ** 2, k**2, (k + 1) ** 2],
            "square_index_primes": [left, center, right],
            "carrier": carrier,
            "return_residual": residual,
            "target_square": target,
            "return_equation_holds": residual == target,
        })

    carriers = [item["carrier"] for item in homologues]
    residuals = [item["return_residual"] for item in homologues]
    targets = [item["target_square"] for item in homologues]
    direct_hits = [item["k"] for item in homologues if item["return_equation_holds"]]
    check("C3/C4/C5 carrier values", carriers == [46, 106, 194], carriers, [46, 106, 194])
    check("homologue residuals", residuals == [-7, 9, 43], residuals, [-7, 9, 43])
    check("homologue target squares", targets == [4, 9, 16], targets, [4, 9, 16])
    check("Q106 is the sole direct homologue hit", direct_hits == [4], direct_hits, [4])

    scan_hits = []
    scan_minimum = contract["declared_windows"]["finite_scan"]["minimum_k"]
    for k in range(scan_minimum, maximum_k + 1):
        if 2 * p(k**2) - p((k + 1) ** 2) == (k - 1) ** 2:
            scan_hits.append(k)
    check(
        "Q106 is the sole hit in the declared finite scan",
        scan_hits == [4],
        scan_hits,
        [4],
    )

    root_pythagorean_hits = [
        k
        for k in range(scan_minimum, maximum_k + 1)
        if (k - 1) ** 2 + k**2 == (k + 1) ** 2
    ]
    check(
        "3-4-5 square root window is independently selective",
        root_pythagorean_hits == [4],
        root_pythagorean_hits,
        [4],
    )
    check(
        "root selectivity has exact factorization",
        all(
            (k - 1) ** 2 + k**2 - (k + 1) ** 2 == k * (k - 4)
            for k in range(scan_minimum, maximum_k + 1)
        ),
        "(k-1)^2+k^2-(k+1)^2=k(k-4)",
        "identity holds",
    )

    local = []
    for value in contract["declared_windows"]["local_perturbations"]:
        local.append({
            "value": value,
            "minus_p25": value - p(25),
            "minus_2p16": value - 2 * p(16),
            "both_q106_closures": value - p(25) == 9 and value == 2 * p(16),
        })
    local_hits = [item["value"] for item in local if item["both_q106_closures"]]
    check("106 is the sole local perturbation hit", local_hits == [106], local_hits, [106])
    check(
        "local p25 residuals expose the one-step perturbation",
        [item["minus_p25"] for item in local] == [7, 8, 9, 10, 11],
        [item["minus_p25"] for item in local],
        [7, 8, 9, 10, 11],
    )
    check(
        "local 2p16 residuals are centered on zero",
        [item["minus_2p16"] for item in local] == [-2, -1, 0, 1, 2],
        [item["minus_2p16"] for item in local],
        [-2, -1, 0, 1, 2],
    )

    boundaries = contract["claim_boundary"]
    check(
        "undefined R extensions remain excluded",
        any("no R(Q46) or R(Q194)" in item for item in boundaries),
        boundaries,
        "explicit no R(Q46) or R(Q194) boundary",
    )
    check(
        "finite scan remains non-universal",
        any("not uniqueness for all positive integers" in item for item in boundaries),
        boundaries,
        "explicit bounded-only statement",
    )
    check(
        "no new identity declared",
        any("no new Study" in item for item in boundaries),
        boundaries,
        "explicit no-new-identity statement",
    )

    passed = all(item["status"] == "PASS" for item in checks)
    return {
        "contract_id": contract["contract_id"],
        "date": contract["date"],
        "classification": (
            "PASS_Q106_LOCAL_AND_BOUNDED_HOMOLOGUE_SELECTIVITY"
            if passed
            else "FAIL_Q106_NOT_SELECTIVE_IN_DECLARED_WINDOWS"
        ),
        "summary": {
            "passed": sum(item["status"] == "PASS" for item in checks),
            "total": len(checks),
            "failed": sum(item["status"] == "FAIL" for item in checks),
        },
        "source_resolution": {
            "path": contract["frozen_source"]["path"],
            "sha256": source_hash,
        },
        "definitions": contract["definitions"],
        "result": {
            "homologues": homologues,
            "direct_homologue_hits": direct_hits,
            "finite_scan": {"minimum_k": scan_minimum, "maximum_k": maximum_k, "hits": scan_hits},
            "root_pythagorean_hits": root_pythagorean_hits,
            "local_perturbations": local,
            "local_exact_hits": local_hits,
        },
        "checks": checks,
        "claim_boundary": boundaries,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    raise SystemExit(0 if result["classification"].startswith("PASS_") else 1)
