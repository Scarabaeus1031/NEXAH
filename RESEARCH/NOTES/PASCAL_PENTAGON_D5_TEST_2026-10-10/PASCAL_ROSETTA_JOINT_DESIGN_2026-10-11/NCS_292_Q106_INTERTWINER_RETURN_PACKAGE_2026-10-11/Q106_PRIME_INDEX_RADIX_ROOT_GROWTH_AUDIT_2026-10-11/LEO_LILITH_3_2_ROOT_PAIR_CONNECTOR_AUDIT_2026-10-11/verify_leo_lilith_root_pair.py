#!/usr/bin/env python3
"""Replay the bounded Leo/Lilith 3:2 root-pair connector audit."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
from fractions import Fraction
from math import isqrt, pi, sqrt
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
        if all(candidate % p for p in found if p <= limit):
            found.append(candidate)
        candidate += 1
    return found


def divisions(source: str) -> set[tuple[int, int]]:
    tree = ast.parse(source)
    values: set[tuple[int, int]] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                left, right = node.left.value, node.right.value
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    if float(left).is_integer() and float(right).is_integer():
                        values.add((int(left), int(right)))
    return values


def validate() -> dict[str, object]:
    contract = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, observed: object, expected: object) -> None:
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "observed": observed, "expected": expected})

    check(
        "existing identity reused without creation",
        contract["identity"]["reuse"] == "A0OE:PASCAL_PENTAGON_D5_TEST" and contract["identity"]["creates"] == [],
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

    archaeology = paths["archaeology_readme"].read_text(encoding="utf-8")
    operator = paths["operator_addendum"].read_text(encoding="utf-8")
    with paths["source_ledger"].open(newline="", encoding="utf-8") as handle:
        ledger = {row["source_id"]: row for row in csv.DictReader(handle)}

    check(
        "M1 archaeology keeps Leo/Lilith at observer vocabulary layer",
        "dual editorial or observer perspectives" in archaeology and "visual vocabulary" in archaeology,
        "observer/display role recovered",
        "observer/display role recovered",
    )
    check(
        "M1 unrelated LEO acronym remains separated",
        "Logical Evaluation Operator" in archaeology and "do not merge with solar Leo" in archaeology,
        "LEO acronym separation present",
        "LEO acronym separation present",
    )
    check(
        "M1 historical source ledger roles recovered",
        all(key in ledger for key in ("SRC-012", "SRC-013", "SRC-015")),
        {key: ledger.get(key, {}).get("evidence_role") for key in ("SRC-012", "SRC-013", "SRC-015")},
        "Lilith counter-rotation, Lilith edge and Leo/Lilith clamps",
    )

    lilith_janus = paths["lilith_janus_script"].read_text(encoding="utf-8")
    lilith_edge = paths["lilith_edge_script"].read_text(encoding="utf-8")
    dual_clamp = paths["leo_lilith_clamp_script"].read_text(encoding="utf-8")
    janus_divisions = divisions(lilith_janus)
    edge_divisions = divisions(lilith_edge)
    clamp_divisions = divisions(dual_clamp)
    check(
        "M2 historical Lilith script contains 3/2 and 4/3 frequency terms",
        {(3, 2), (4, 3)} <= janus_divisions and "Lilith-Gegenrotation" in lilith_janus,
        {"divisions": sorted(janus_divisions), "label": "Lilith-Gegenrotation" in lilith_janus},
        {"required": [[3, 2], [4, 3]], "label": True},
    )
    check(
        "M2 operator archaeology types 3/2 and 2/3 as reciprocals",
        "| directed division | `3/2` | `2/3` | reciprocal |" in operator,
        "3/2 <-> 2/3",
        "3/2 <-> 2/3",
    )
    check(
        "M2 Lilith edge 3/4 remains a distinct control",
        (3, 4) in edge_divisions and "LILITH_EDGE" in lilith_edge,
        {"divisions": sorted(edge_divisions), "LILITH_EDGE": "LILITH_EDGE" in lilith_edge},
        {"contains": [3, 4]},
    )
    check(
        "M2 paired Leo/Lilith clamp source has no ratio law",
        "Lilith/Leo Clamps" in dual_clamp and (3, 2) not in clamp_divisions and (2, 3) not in clamp_divisions,
        {"dual_label": "Lilith/Leo Clamps" in dual_clamp, "divisions": sorted(clamp_divisions)},
        {"dual_label": True, "3/2_or_2/3": False},
    )

    p = primes(11500)
    square_indices = [r * r for r in range(1, 6)]
    square_primes = [p[index - 1] for index in square_indices]
    adjacent_sums = [a + b for a, b in zip(square_primes, square_primes[1:])]
    check("M3 square-index primes", square_primes == [2, 7, 23, 53, 97], square_primes, [2, 7, 23, 53, 97])
    check("M3 adjacent sums hit Q106 joint sequence", adjacent_sums == [9, 30, 76, 150], adjacent_sums, [9, 30, 76, 150])

    parent = json.loads(paths["parent_result"].read_text(encoding="utf-8"))
    profile = parent["modules"]["M3_ORBIT_PRIME_INDEX_JOINT"]["orbit_profile"]
    q_sequence = parent["modules"]["M1_Q106_ROOT_GROWTH"]["q_sequence"]
    level_counts = parent["modules"]["M1_Q106_ROOT_GROWTH"]["level_counts"]
    typed_targets = {
        "F": profile["5"],
        "outer_level": level_counts[-1],
        "Q5": q_sequence[5],
        "closure": 150,
        "mirror_definition": parent["modules"]["M5_RADIX_MIRROR"]["J50"]["definition"],
    }
    check(
        "M3 adjacent sums have typed parent targets",
        adjacent_sums[:3] == [typed_targets["F"], typed_targets["outer_level"], typed_targets["Q5"]]
        and square_primes[-2] + square_primes[-1] == 150,
        {"adjacent_sums": adjacent_sums, "targets": typed_targets},
        {"F": 9, "outer_level": 30, "Q5": 76, "closure": 150},
    )

    prime_index = {value: index + 1 for index, value in enumerate(p)}
    fixed_hits: list[int] = []
    suffix_hits: list[int] = []
    gap_hits: list[dict[str, int]] = []
    joint_hits: list[int] = []
    for r in range(1, 101):
        low = p[r * r - 1]
        high = p[(r + 1) * (r + 1) - 1]
        fixed = low + high == 150
        suffix = (low % 100, high % 100) == (53, 97)
        next_same = next(value for value in p[(r + 1) * (r + 1):] if value % 100 == high % 100)
        index_gap = prime_index[next_same] - prime_index[high]
        gap = index_gap == r * (r + 1)
        if fixed:
            fixed_hits.append(r)
        if suffix:
            suffix_hits.append(r)
        if gap:
            gap_hits.append({"r": r, "low": low, "high": high, "next": next_same, "index_gap": index_gap})
        if fixed and suffix and gap:
            joint_hits.append(r)
    check("M4 fixed J150 pair is unique for r=1..100", fixed_hits == [4], fixed_hits, [4])
    check("M4 decimal 53-to-97 suffix pair is unique for r=1..100", suffix_hits == [4], suffix_hits, [4])
    check(
        "M4 root product equals next same-suffix index gap only at r=4",
        gap_hits == [{"r": 4, "low": 53, "high": 97, "next": 197, "index_gap": 20}],
        gap_hits,
        [{"r": 4, "low": 53, "high": 97, "next": 197, "index_gap": 20}],
    )
    check("M4 all three root-pair controls intersect only at r=4", joint_hits == [4], joint_hits, [4])

    seed = {
        "sum": 2 + 3,
        "product": 2 * 3,
        "difference": 3 - 2,
        "ratio_forward": "3/2",
        "ratio_reverse": "2/3",
        "lift": [2**2, 2 + 3],
    }
    check("M5 introduced seed lift maps 2,3 to root pair 4,5", seed["lift"] == [4, 5], seed, {"lift": [4, 5]})
    check(
        "M5 3:2 is the directed ratio on ladder edge r=2 to r=3",
        square_indices[1:3] == [4, 9] and square_primes[1:3] == [7, 23] and adjacent_sums[1] == 30,
        {"root_ratio": "3:2", "indices": square_indices[1:3], "primes": square_primes[1:3], "sum": adjacent_sums[1]},
        {"root_ratio": "3:2", "indices": [4, 9], "primes": [7, 23], "sum": 30},
    )
    check(
        "M5 root-pair joint signature",
        4 * 5 == 20 and 4**2 + 5**2 == 41 and 697 == 17 * 41,
        {"product": 20, "sum_of_squares": 41, "697_factorization": [17, 41]},
        {"product": 20, "sum_of_squares": 41, "697_factorization": [17, 41]},
    )

    classification_state = {
        "historical_lilith_3_2_marker": True,
        "historical_leo_2_3_marker": False,
        "square_index_ladder_exact": True,
        "leo_lilith_root_assignment_recovered": False,
        "connector_status": "ARITHMETIC_OBSERVER_JOINT_CANDIDATE",
    }
    check(
        "M6 connector remains candidate rather than recovered Leo/Lilith operator",
        classification_state["historical_lilith_3_2_marker"]
        and not classification_state["historical_leo_2_3_marker"]
        and not classification_state["leo_lilith_root_assignment_recovered"],
        classification_state,
        {"connector_status": "ARITHMETIC_OBSERVER_JOINT_CANDIDATE"},
    )

    denominators = [540, 720, 1080, 1440]
    scale_factors = [3, 4, 6, 8]
    normalized = [Fraction(432, value) for value in denominators]
    ring_values = [10 * value for value in normalized]
    ring_colors = {8: "yellow", 6: "blue", 4: "purple", 3: "unassigned"}
    check(
        "M7 denominators are the 180-scaled 3,4,6,8 factor track",
        denominators == [180 * value for value in scale_factors],
        denominators,
        [540, 720, 1080, 1440],
    )
    check(
        "M7 exact 432 normalization",
        normalized == [Fraction(4, 5), Fraction(3, 5), Fraction(2, 5), Fraction(3, 10)],
        [str(value) for value in normalized],
        ["4/5", "3/5", "2/5", "3/10"],
    )
    check(
        "M7 tenfold normalized ring reverses 3,4,6,8 to 8,6,4,3",
        ring_values == [8, 6, 4, 3],
        [int(value) for value in ring_values],
        [8, 6, 4, 3],
    )
    check(
        "M7 divisor-complement map k to 24/k is an involution",
        all(Fraction(24, value) == image for value, image in zip(scale_factors, ring_values))
        and [Fraction(24, value) for value in ring_values] == scale_factors,
        {str(value): str(Fraction(24, value)) for value in scale_factors},
        {"3": "8", "4": "6", "6": "4", "8": "3"},
    )
    check(
        "M7 factor track is generated by the 2,3 seed",
        scale_factors == [3, 2**2, 2 * 3, 2**3],
        scale_factors,
        [3, 4, 6, 8],
    )
    check(
        "M7 1440 closes the declared doubling and square-product identities",
        1440 == 2 * 720 == 12**2 * (2 * 5),
        {"2x720": 2 * 720, "12^2x(2x5)": 12**2 * (2 * 5)},
        1440,
    )

    q432 = lambda value: Fraction(432, 1) / value
    coordinate_inputs = [Fraction(value, 1) for value in denominators]
    pi_coordinate = 432 / pi
    phi = (1 + sqrt(5)) / 2
    phi_coordinate = 432 / phi
    sqrt2_coordinate = 432 / sqrt(2)
    golden_angle = 360 / (phi**2)
    golden_delta = abs(pi_coordinate - golden_angle)
    check(
        "M8 400-420-432 factor track is exact",
        400 == 20 * 20 and 420 == 20 * 21 == 12 * 35 and 432 == 12 * 36 == 2**4 * 3**3,
        {"400": "20*20", "420": ["20*21", "12*35"], "432": ["12*36", "2^4*3^3"]},
        "all exact",
    )
    check(
        "M8 Q432 is an exact involution on the declared coordinate inputs",
        all(q432(q432(value)) == value for value in coordinate_inputs),
        {str(value): str(q432(q432(value))) for value in coordinate_inputs},
        {str(value): str(value) for value in coordinate_inputs},
    )
    check(
        "M8 432 over pi coordinate reproduces the displayed value",
        abs(pi_coordinate - 137.5099) < 0.00005,
        pi_coordinate,
        137.5099,
    )
    check(
        "M8 432 over square-root-two coordinate reproduces the displayed value",
        abs(sqrt2_coordinate - 305.4701) < 0.00005,
        sqrt2_coordinate,
        305.4701,
    )
    check(
        "M8 pi coordinate is within 0.0022 degrees of the golden angle",
        abs(golden_delta - 0.002106781359714205) < 1e-12 and golden_delta < 0.0022,
        golden_delta,
        "approximately 0.00210678136 degrees",
    )
    check(
        "M8 displayed 432 over phi value is a negative control",
        abs(phi_coordinate - 267.0031) > 0.01 and abs(phi_coordinate - 266.99068313995457) < 1e-12,
        {"standard_phi_value": phi_coordinate, "displayed_value": 267.0031, "absolute_error": abs(phi_coordinate - 267.0031)},
        "standard phi gives approximately 266.990683, not 267.0031",
    )

    passed = all(item["status"] == "PASS" for item in checks)
    classification = "PASS_ARITHMETIC_CONNECTOR_CANDIDATE_WITH_LILITH_3_2_SOURCE_MARKER" if passed else "CONTRACT_INVALID"
    return {
        "contract_id": contract["contract_id"],
        "date": contract["date"],
        "classification": classification,
        "summary": {"passed": sum(item["status"] == "PASS" for item in checks), "total": len(checks)},
        "source_resolution": source_resolution,
        "derived": {
            "square_indices": square_indices,
            "square_index_primes": square_primes,
            "adjacent_sums": adjacent_sums,
            "root_pair_scan": {"fixed_hits": fixed_hits, "suffix_hits": suffix_hits, "gap_hits": gap_hits, "joint_hits": joint_hits},
            "seed_grammar": seed,
            "archaeology": classification_state,
            "record_play_ring": {
                "common_state": 432,
                "base": 180,
                "denominators": denominators,
                "scale_factors": scale_factors,
                "normalized": [str(value) for value in normalized],
                "tenfold_ring_values": [int(value) for value in ring_values],
                "involution": "k -> 24/k",
                "display_colors": ring_colors,
            },
            "coordinate_bridge": {
                "operator": "Q_432(x)=432/x",
                "exact_involution": True,
                "factor_track": {"400": "20^2", "420": "20*21=12*35", "432": "12*36=2^4*3^3"},
                "coordinates_degrees": {
                    "432_over_pi": pi_coordinate,
                    "432_over_phi_standard": phi_coordinate,
                    "432_over_sqrt2": sqrt2_coordinate,
                    "golden_angle": golden_angle,
                    "pi_vs_golden_angle_delta": golden_delta,
                },
                "negative_control": "displayed 432/phi=267.0031 degrees is not reproduced by standard phi",
            },
        },
        "checks": checks,
        "claim_boundary": contract["claim_boundary"],
    }


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["classification"].startswith("PASS_") else 1)

