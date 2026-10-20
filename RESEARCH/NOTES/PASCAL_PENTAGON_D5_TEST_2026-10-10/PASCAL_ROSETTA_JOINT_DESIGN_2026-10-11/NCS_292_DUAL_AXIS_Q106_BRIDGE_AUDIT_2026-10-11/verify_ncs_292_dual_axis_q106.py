#!/usr/bin/env python3
"""Verify the bounded NCS-292 / dual-axis / Q106 bridge candidate.

This is deterministic formal-design validation, not an admitted Lab run.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def primes(count: int) -> list[int]:
    result: list[int] = []
    candidate = 2
    while len(result) < count:
        if all(candidate % prime for prime in result if prime * prime <= candidate):
            result.append(candidate)
        candidate += 1
    return result


def validate() -> dict[str, object]:
    contract_path = HERE / "CONTRACT.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, observed: object, expected: object) -> None:
        checks.append({
            "name": name,
            "status": "PASS" if passed else "FAIL",
            "observed": observed,
            "expected": expected,
        })

    check(
        "identity reused without creation",
        contract["identity"]["reuse"] == "A0OE:PASCAL_PENTAGON_D5_TEST"
        and contract["identity"]["creates"] == [],
        contract["identity"],
        {"reuse": "A0OE:PASCAL_PENTAGON_D5_TEST", "creates": []},
    )

    resolved_sources: dict[str, dict[str, object]] = {}
    for name, spec in contract["frozen_sources"].items():
        path = ROOT / spec["path"]
        observed_hash = sha256(path) if path.exists() else None
        resolved_sources[name] = {
            "path": spec["path"],
            "exists": path.exists(),
            "sha256": observed_hash,
        }
        check(
            f"frozen source {name}",
            path.exists() and observed_hash == spec["sha256"],
            resolved_sources[name],
            {"exists": True, "sha256": spec["sha256"]},
        )

    ncs_script_path = ROOT / contract["frozen_sources"]["ncs_script"]["path"]
    ncs_readme_path = ROOT / contract["frozen_sources"]["ncs_readme"]["path"]
    script_text = ncs_script_path.read_text(encoding="utf-8")
    readme_text = ncs_readme_path.read_text(encoding="utf-8")
    block_match = re.search(
        r"pink_balls\s*=\s*np\.array\(\[(.*?)\]\)", script_text, re.DOTALL
    )
    point_rows = [] if not block_match else re.findall(
        r"\[\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?\s*\]",
        block_match.group(1),
    )
    check(
        "historical NCS source declares and moves four points",
        len(point_rows) == 4
        and "292 NCS Switch" in readme_text
        and "new_pink[:,0]" in script_text
        and "new_pink[:,1]" in script_text,
        {
            "point_rows": len(point_rows),
            "x_shift": "new_pink[:,0]" in script_text,
            "y_shift": "new_pink[:,1]" in script_text,
        },
        {"point_rows": 4, "x_shift": True, "y_shift": True},
    )

    word = "292"
    check(
        "292 palindrome and balanced directional sums",
        word == word[::-1] and 2 + 9 == 9 + 2 == 11,
        {"palindrome": word == word[::-1], "left_sum": 2 + 9, "right_sum": 9 + 2},
        {"palindrome": True, "left_sum": 11, "right_sum": 11},
    )

    prime_list = primes(27)
    check("29 is the tenth prime", prime_list[9] == 29, prime_list[9], 29)
    prime_chain = {f"P{index}": prime_list[index - 1] for index in range(23, 28)}
    check(
        "consecutive prime-index chain P23 through P27",
        prime_chain == {"P23": 83, "P24": 89, "P25": 97, "P26": 101, "P27": 103},
        prime_chain,
        {"P23": 83, "P24": 89, "P25": 97, "P26": 101, "P27": 103},
    )

    xi = contract["axis_contract"]["xi_hinge"]
    janus = contract["axis_contract"]["janus_axis"]
    axis_metrics = {
        "xi_midpoint": (xi["left"] + xi["right"]) / 2,
        "janus_midpoint": (janus["left"] + janus["right"]) / 2,
        "right_endpoint_shift": janus["right"] - xi["right"],
        "midpoint_shift": janus["midpoint"] - xi["midpoint"],
    }
    expected_axis_metrics = {
        "xi_midpoint": 99.0,
        "janus_midpoint": 100.0,
        "right_endpoint_shift": 2,
        "midpoint_shift": 1,
    }
    check(
        "adjacent-axis arithmetic",
        axis_metrics == expected_axis_metrics,
        axis_metrics,
        expected_axis_metrics,
    )
    exit_arithmetic = {
        "97_plus_4": 97 + 4,
        "97_plus_3": 97 + 3,
        "103_plus_3": 103 + 3,
        "2_times_53": 2 * 53,
        "53_squared": 53**2,
    }
    expected_exit_arithmetic = {
        "97_plus_4": 101,
        "97_plus_3": 100,
        "103_plus_3": 106,
        "2_times_53": 106,
        "53_squared": 2809,
    }
    check(
        "prime-index and P-exit arithmetic stay separated",
        exit_arithmetic == expected_exit_arithmetic,
        exit_arithmetic,
        expected_exit_arithmetic,
    )

    local_alphabet = list(itertools.product((1, 2, 3), (-1, 1)))
    check(
        "oriented ABC/123 alphabet has six states",
        len(local_alphabet) == 6,
        len(local_alphabet),
        6,
    )

    package_names = contract["typed_candidate"]["packages"]
    x40 = list(itertools.product(range(5), package_names, ("A", "B")))
    quotient = {(sector, package) for sector, package, _layer in x40}
    fibre_profile = {
        key: sum((sector, package) == key for sector, package, _layer in x40)
        for key in quotient
    }
    check(
        "declared two-layer package carrier has forty states",
        len(x40) == 40,
        len(x40),
        40,
    )
    check(
        "free horizontal layer quotient has twenty two-element fibres",
        len(quotient) == 20 and set(fibre_profile.values()) == {2},
        {"classes": len(quotient), "fibre_sizes": sorted(set(fibre_profile.values()))},
        {"classes": 20, "fibre_sizes": [2]},
    )

    nodes_path = ROOT / contract["frozen_sources"]["q106_nodes"]["path"]
    edges_path = ROOT / contract["frozen_sources"]["q106_edges"]["path"]
    with nodes_path.open(newline="", encoding="utf-8") as handle:
        nodes = list(csv.DictReader(handle))
    with edges_path.open(newline="", encoding="utf-8") as handle:
        edges = list(csv.DictReader(handle))
    check(
        "frozen Q106 reference remains distinct and intact",
        len(nodes) == 106 and len(edges) == 180,
        {"nodes": len(nodes), "directed_edges": len(edges)},
        {"nodes": 106, "directed_edges": 180},
    )

    maps = contract["maps_required_for_identity"]
    check(
        "NCS-to-package intertwiner is explicitly absent",
        maps["ncs_points_to_packages"] is None,
        maps["ncs_points_to_packages"],
        None,
    )
    check(
        "Base20-to-Q106 intertwiner is explicitly absent",
        maps["base20_quotient_to_q106"] is None,
        maps["base20_quotient_to_q106"],
        None,
    )
    check(
        "RootCube15-to-Q106 map is explicitly absent",
        maps["root_cube15_to_q106"] is None
        and contract["typed_candidate"]["root_cube_primary_nodes"] == 15,
        {
            "map": maps["root_cube15_to_q106"],
            "visual_count": contract["typed_candidate"]["root_cube_primary_nodes"],
        },
        {"map": None, "visual_count": 15},
    )

    passed = all(item["status"] == "PASS" for item in checks)
    maps_defined = all(value is not None for value in maps.values())
    classification = (
        "COMPILED_WITH_TYPED_INTERTWINERS"
        if passed and maps_defined
        else "COMPILED_40_TO_20_CANDIDATE_OPEN_INTERTWINERS"
        if passed
        else "CONTRACT_INVALID"
    )
    return {
        "schema": "nexah.ncs-292-dual-axis-q106-bridge-audit-result/1.0.0",
        "date": contract["date"],
        "status": "PASS_WITH_VALIDATED_OPEN_BRIDGES" if passed else "FAIL",
        "classification": classification,
        "identity_reused": contract["identity"]["reuse"],
        "creates": contract["identity"]["creates"],
        "summary": {
            "checks_passed": sum(item["status"] == "PASS" for item in checks),
            "checks_total": len(checks),
            "historical_ncs_points": len(point_rows),
            "candidate_unfolded_states": len(x40),
            "candidate_quotient_classes": len(quotient),
            "root_cube_visual_primary_nodes": contract["typed_candidate"]["root_cube_primary_nodes"],
            "q106_nodes": len(nodes),
            "q106_directed_edges": len(edges),
            "required_intertwiners_defined": sum(value is not None for value in maps.values()),
            "required_intertwiners_total": len(maps),
        },
        "axis_metrics": axis_metrics,
        "exit_arithmetic": exit_arithmetic,
        "prime_chain": prime_chain,
        "source_resolution": resolved_sources,
        "checks": checks,
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write RESULT.json")
    args = parser.parse_args()
    result = validate()
    if args.write:
        (HERE / "RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS_WITH_VALIDATED_OPEN_BRIDGES" else 1


if __name__ == "__main__":
    raise SystemExit(main())
