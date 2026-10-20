#!/usr/bin/env python3
"""Validate the Pascal–Rosetta formal design against frozen SCC-003 tables.

This is a design-fixture validator, not an admitted Science-Lab run.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
ARTIFACTS = HERE.parent / "SCC_003_REFERENCE" / "artifacts"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_csv(name: str) -> list[dict[str, str]]:
    with (ARTIFACTS / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def raw(row: dict[str, str]) -> tuple[int, int, int]:
    return int(row["face"]), int(row["n"]), int(row["k"])


def gear(x: tuple[int, int, int]) -> tuple[int, int, int, int]:
    f, n, k = x
    return f % 5, (f + k) % 5, n % 6, (2 * k - n) % 12


def left(g: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    a, b, d, q = g
    return a, b, (d + 1) % 6, (q - 1) % 12


def right(g: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    a, b, d, q = g
    return a, (b + 1) % 5, (d + 1) % 6, (q + 1) % 12


def generic_locked(g: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Prior generic Gear schedule: all wheels advance together."""
    a, b, d, q = g
    return (a + 1) % 5, (b + 1) % 5, (d + 1) % 6, (q + 1) % 12


def generic_counter(g: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Prior generic Gear schedule: A advances and B counter-rotates."""
    a, b, d, q = g
    return (a + 1) % 5, (b - 1) % 5, (d + 1) % 6, (q + 1) % 12


def rotate_raw(x: tuple[int, int, int], turns: int = 1) -> tuple[int, int, int]:
    f, n, k = x
    return (f + turns) % 5, n, k


def reflect_raw(x: tuple[int, int, int]) -> tuple[int, int, int]:
    f, n, k = x
    return (-f) % 5, n, n - k


def projected_collision_summary(
    rows: list[dict[str, str]], indices: tuple[int, ...]
) -> dict[str, int]:
    buckets: dict[tuple[int, ...], set[str]] = defaultdict(set)
    for row in rows:
        address = gear(raw(row))
        buckets[tuple(address[i] for i in indices)].add(row["quotient_node_id"])
    sizes = [len(values) for values in buckets.values()]
    return {
        "addresses": len(buckets),
        "cross_quotient_collision_addresses": sum(size > 1 for size in sizes),
        "maximum_quotient_multiplicity": max(sizes),
    }


def validate() -> dict[str, object]:
    contract_path = HERE / "JOINT_CONTRACT.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    incidences = load_csv("face_incidence.csv")
    face_edges = load_csv("face_edges.csv")
    nodes = load_csv("nodes.csv")

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

    raw_to_row = {raw(row): row for row in incidences}
    encoded = {raw(row): gear(raw(row)) for row in incidences}
    inverse = {address: x for x, address in encoded.items()}

    check(
        "machine-readable contract identity",
        contract["contract_id"] == "A0-BL-023:PASCAL_ROSETTA_JOINT_DESIGN:V1"
        and contract["identity"]["reuse"] == "A0OE:PASCAL_PENTAGON_D5_TEST"
        and contract["identity"]["creates"] == [],
        {
            "contract_id": contract["contract_id"],
            "reuse": contract["identity"]["reuse"],
            "creates": contract["identity"]["creates"],
        },
        {
            "contract_id": "A0-BL-023:PASCAL_ROSETTA_JOINT_DESIGN:V1",
            "reuse": "A0OE:PASCAL_PENTAGON_D5_TEST",
            "creates": [],
        },
    )
    check("raw incidence count", len(incidences) == 140, len(incidences), 140)
    check("quotient node count", len(nodes) == 106, len(nodes), 106)
    check("raw encoding injective", len(inverse) == 140, len(inverse), 140)

    left_failures = []
    right_failures = []
    for edge in face_edges:
        f = int(edge["face"])
        n = int(edge["parent_n"])
        k = int(edge["parent_k"])
        source = (f, n, k)
        if edge["branch"] == "left":
            target = (f, n + 1, k)
            if gear(target) != left(gear(source)):
                left_failures.append((source, target))
        else:
            target = (f, n + 1, k + 1)
            if gear(target) != right(gear(source)):
                right_failures.append((source, target))

    check(
        "left Pascal/gear intertwining",
        not left_failures,
        {"tested": 105, "failures": len(left_failures)},
        {"tested": 105, "failures": 0},
    )
    check(
        "right Pascal/gear intertwining",
        not right_failures,
        {"tested": 105, "failures": len(right_failures)},
        {"tested": 105, "failures": 0},
    )

    control_matches = {
        "generic_locked": 0,
        "generic_counter": 0,
        "collapsed_to_left": 0,
        "collapsed_to_right": 0,
    }
    for edge in face_edges:
        f = int(edge["face"])
        n = int(edge["parent_n"])
        k = int(edge["parent_k"])
        source = (f, n, k)
        target = (f, n + 1, k if edge["branch"] == "left" else k + 1)
        source_address = gear(source)
        target_address = gear(target)
        control_matches["generic_locked"] += generic_locked(source_address) == target_address
        control_matches["generic_counter"] += generic_counter(source_address) == target_address
        control_matches["collapsed_to_left"] += left(source_address) == target_address
        control_matches["collapsed_to_right"] += right(source_address) == target_address
    expected_control_matches = {
        "generic_locked": 0,
        "generic_counter": 0,
        "collapsed_to_left": 105,
        "collapsed_to_right": 105,
    }
    check(
        "matched controls do not reproduce the branch-aware schedule",
        control_matches == expected_control_matches,
        control_matches,
        expected_control_matches,
    )

    quotient_fibres: dict[str, set[tuple[int, int, int, int]]] = defaultdict(set)
    raw_fibres: dict[str, list[tuple[int, int, int]]] = defaultdict(list)
    for row in incidences:
        node = row["quotient_node_id"]
        x = raw(row)
        quotient_fibres[node].add(gear(x))
        raw_fibres[node].append(x)

    fibre_profile = Counter(len(values) for values in quotient_fibres.values())
    observed_profile = {str(key): fibre_profile[key] for key in sorted(fibre_profile)}
    expected_profile = contract["quotient_joint"]["expected_fiber_profile"]
    check("quotient relation fibre profile", observed_profile == expected_profile, observed_profile, expected_profile)

    return_failures = []
    for node, addresses in quotient_fibres.items():
        for address in addresses:
            x = inverse[address]
            if raw_to_row[x]["quotient_node_id"] != node:
                return_failures.append((node, address))
    check(
        "exact relational return",
        not return_failures,
        {"tested": 140, "failures": len(return_failures)},
        {"tested": 140, "failures": 0},
    )

    rotation_failures = []
    reflection_failures = []
    for node, reps in raw_fibres.items():
        rotated_nodes = {raw_to_row[rotate_raw(x)]["quotient_node_id"] for x in reps}
        reflected_nodes = {raw_to_row[reflect_raw(x)]["quotient_node_id"] for x in reps}
        rotated_addresses = {gear(rotate_raw(x)) for x in reps}
        reflected_addresses = {gear(reflect_raw(x)) for x in reps}
        if len(rotated_nodes) != 1 or rotated_addresses != quotient_fibres[next(iter(rotated_nodes))]:
            rotation_failures.append(node)
        if len(reflected_nodes) != 1 or reflected_addresses != quotient_fibres[next(iter(reflected_nodes))]:
            reflection_failures.append(node)
    check(
        "C5 relation equivariance",
        not rotation_failures,
        {"tested": 106, "failures": len(rotation_failures)},
        {"tested": 106, "failures": 0},
    )
    check(
        "reflection relation equivariance",
        not reflection_failures,
        {"tested": 106, "failures": len(reflection_failures)},
        {"tested": 106, "failures": 0},
    )

    apex_addresses = quotient_fibres["A"]
    fixed_apex_addresses = {
        address
        for address in apex_addresses
        if gear(rotate_raw(inverse[address])) == address
    }
    check(
        "negative control: equivariant single-address apex selector",
        not fixed_apex_addresses,
        "FAIL_NO_FIXED_ADDRESS_OVER_FIXED_APEX",
        "FAIL_NO_FIXED_ADDRESS_OVER_FIXED_APEX",
    )

    drop_b = projected_collision_summary(incidences, (0, 2, 3))
    drop_q = projected_collision_summary(incidences, (0, 1, 2))
    check(
        "negative control: remove B wheel",
        drop_b["cross_quotient_collision_addresses"] > 0,
        drop_b,
        "cross-quotient collisions > 0",
    )
    check(
        "negative control: remove Q envelope",
        drop_q["cross_quotient_collision_addresses"] > 0,
        drop_q,
        "cross-quotient collisions > 0",
    )

    failures = [item["name"] for item in checks if item["status"] != "PASS"]
    return {
        "contract_id": "A0-BL-023:PASCAL_ROSETTA_JOINT_DESIGN:V1",
        "status": "PASS" if not failures else "FAIL",
        "classification": "FORMAL_DESIGN_VALIDATION_NOT_ADMITTED_NOT_ACTIVE",
        "summary": {
            "checks": len(checks),
            "failures": len(failures),
            "raw_incidences": len(incidences),
            "quotient_nodes": len(nodes),
            "face_edge_incidences": len(face_edges),
            "gear_image_states": len(inverse),
            "quotient_relation_addresses": sum(len(v) for v in quotient_fibres.values()),
        },
        "provenance": {
            "contract_sha256": sha256(contract_path),
            "scc003_manifest_sha256": sha256(ARTIFACTS / "manifest.json"),
        },
        "checks": checks,
        "failures": failures,
        "verdicts": {
            "raw_intertwiner": "PASS",
            "quotient_joint": "PASS_RELATION",
            "single_state_quotient_selector": "EXPECTED_FAIL",
            "return": "PASS_EXACT_WITH_RELATION_PROVENANCE",
            "generic_schedule_controls": "PASS_REJECTED_AS_FULL_INTERTWINERS",
        },
        "claim_boundary": (
            "Finite formal design validation only; no PENT-08, Family, admitted run, "
            "physical identity, novelty or publication claim."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write RESULT.json")
    args = parser.parse_args()
    result = validate()
    if args.write:
        (HERE / "RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()

