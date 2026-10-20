#!/usr/bin/env python3
"""Replay the bounded NCS/SNC order, envelope and return design test."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
State = tuple[int, int, int]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    return all(number % divisor for divisor in range(2, math.isqrt(number) + 1))


def prime_index(number: int) -> int | None:
    if not is_prime(number):
        return None
    return sum(is_prime(candidate) for candidate in range(2, number + 1))


def factorize(number: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= number:
        while number % divisor == 0:
            factors.append(divisor)
            number //= divisor
        divisor += 1
    if number > 1:
        factors.append(number)
    return factors


def cycle_profile(mapping: dict[State, State]) -> dict[int, int]:
    seen: set[State] = set()
    lengths: Counter[int] = Counter()
    for state in mapping:
        if state in seen:
            continue
        current = state
        length = 0
        while current not in seen:
            seen.add(current)
            current = mapping[current]
            length += 1
        lengths[length] += 1
    return dict(sorted(lengths.items()))


def permutation_order(mapping: dict[State, State]) -> int:
    order = 1
    for length in cycle_profile(mapping):
        order = math.lcm(order, length)
    return order


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

    # M1 — keep unlike numeric registers distinct while checking exact facts.
    wobble = Fraction(1069, 365)
    numeric = {
        "292_palindrome": str(292) == str(292)[::-1],
        "929_palindrome": str(929) == str(929)[::-1],
        "929_prime": is_prime(929),
        "929_prime_index": prime_index(929),
        "2929_factors": factorize(2929),
        "29_prime_index": prime_index(29),
        "101_prime_index": prime_index(101),
        "2929_reverse": int(str(2929)[::-1]),
        "wobble_exact": f"{wobble.numerator}/{wobble.denominator}",
        "wobble_decimal": float(wobble),
        "distance_to_2_929": abs(float(wobble) - 2.929),
        "171929_929171_reversal_pair": str(171929)[::-1] == str(929171),
        "171929_prime": is_prime(171929),
        "929171_prime": is_prime(929171),
        "179129_factors": factorize(179129),
    }
    check(
        "M1 exact 292/929 register facts",
        numeric["292_palindrome"]
        and numeric["929_palindrome"]
        and numeric["929_prime"]
        and numeric["929_prime_index"] == 158
        and numeric["2929_factors"] == [29, 101]
        and numeric["29_prime_index"] == 10
        and numeric["101_prime_index"] == 26
        and numeric["2929_reverse"] == 9292,
        numeric,
        {"929": "P158 palindrome", "2929": "P10*P26", "reverse_2929": 9292},
    )
    check(
        "M1 pulse-ring arithmetic separates reversal pair and composite control",
        numeric["171929_929171_reversal_pair"]
        and numeric["171929_prime"]
        and numeric["929171_prime"]
        and numeric["179129_factors"] == [17, 41, 257],
        {
            "171929_prime": numeric["171929_prime"],
            "929171_prime": numeric["929171_prime"],
            "179129_factors": numeric["179129_factors"],
        },
        {"reversal_pair": "171929<->929171", "composite_control": "179129=17*41*257"},
    )
    check(
        "M1 typed registers remain non-identical",
        len({"integer_address", "normalized_metric", "ratio", "exact_joint"}) == 4
        and 929 != 2929
        and not math.isclose(float(wobble), 2.929, rel_tol=0.0, abs_tol=0.0),
        {"address": 929, "metric": 0.929, "ratio": float(wobble), "joint": 2929},
        "four typed registers; decimal proximity is not identity",
    )

    # M2 — recover W20 as five weight-20 nodes, not five 20-node blocks.
    with paths["q106_nodes"].open(newline="", encoding="utf-8") as handle:
        nodes = list(csv.DictReader(handle))
    with paths["q106_edges"].open(newline="", encoding="utf-8") as handle:
        edges = list(csv.DictReader(handle))
    automorphisms = json.loads(paths["q106_automorphisms"].read_text(encoding="utf-8"))
    permutations = [action["permutation_zero_based"] for action in automorphisms["actions"]]
    w20 = [index for index, node in enumerate(nodes) if int(node["weight"]) == 20]
    w20_set = set(w20)
    orbit = sorted({permutation[w20[0]] for permutation in permutations})
    internal_edges = [
        edge for edge in edges
        if int(edge["source_index"]) in w20_set and int(edge["target_index"]) in w20_set
    ]
    incoming = Counter(
        int(edge["target_index"]) for edge in edges
        if int(edge["target_index"]) in w20_set and int(edge["source_index"]) not in w20_set
    )
    outgoing = Counter(
        int(edge["source_index"]) for edge in edges
        if int(edge["source_index"]) in w20_set and int(edge["target_index"]) not in w20_set
    )
    w20_ids = [nodes[index]["node_id"] for index in w20]
    check(
        "M2 W20 is one complete five-node D5 orbit",
        len(w20) == 5 and orbit == w20,
        {"indices": w20, "node_ids": w20_ids, "orbit": orbit},
        {"node_count": 5, "orbit_size": 5},
    )
    check(
        "M2 W20 terminal incidence profile",
        len(internal_edges) == 0
        and set(incoming) == w20_set
        and set(incoming.values()) == {2}
        and not outgoing,
        {"internal_edges": len(internal_edges), "incoming": dict(incoming), "outgoing": dict(outgoing)},
        {"internal_edges": 0, "incoming_per_node": 2, "outgoing": 0},
    )
    check(
        "M2 weighted subtotal is not node cardinality",
        len(w20) == 5 and sum(int(nodes[index]["weight"]) for index in w20) == 100,
        {"node_count": len(w20), "weight_each": 20, "weighted_subtotal": 100},
        {"node_count": 5, "weight_each": 20, "weighted_subtotal": 100},
    )

    # M3 — compile all six candidate N/S/C orders on X40.
    x40 = list(itertools.product(range(5), range(4), range(2)))

    def n_op(state: State) -> State:
        sector, package, layer = state
        return ((sector + 1) % 5, package, layer)

    def s_op(state: State) -> State:
        sector, package, layer = state
        return ((-sector) % 5, package, 1 - layer)

    def c_op(state: State) -> State:
        sector, package, layer = state
        return (sector, package, 1 - layer)

    operators = {"N": n_op, "S": s_op, "C": c_op}
    words = ["".join(order) for order in itertools.permutations("NSC")]

    def apply_word(word: str, state: State) -> State:
        current = state
        for symbol in word:
            current = operators[symbol](current)
        return current

    maps = {word: {state: apply_word(word, state) for state in x40} for word in words}
    canonical_maps = {word: tuple(maps[word][state] for state in x40) for word in words}
    grouped: defaultdict[tuple[State, ...], list[str]] = defaultdict(list)
    for word, mapping in canonical_maps.items():
        grouped[mapping].append(word)
    order_classes = sorted((sorted(group) for group in grouped.values()), key=lambda group: group[0])
    check(
        "M3 complete S3 scan yields two exact order classes",
        len(words) == 6 and len(grouped) == 2 and sorted(map(len, order_classes)) == [3, 3],
        order_classes,
        "two classes of three words",
    )
    ncs_snc_difference = sum(maps["NCS"][state] != maps["SNC"][state] for state in x40)
    check(
        "M3 NCS and SNC are distinct on the full carrier",
        ncs_snc_difference == 40,
        ncs_snc_difference,
        40,
    )

    # M4 — typed ALGO/OLGO/OKO signatures and finite envelope.
    signatures: dict[str, dict[str, object]] = {}
    inverse_n = lambda state: ((state[0] - 1) % 5, state[1], state[2])
    for word, mapping in maps.items():
        fixed = sum(mapping[state] == state for state in x40)
        packages_preserved = sum(mapping[state][1] == state[1] for state in x40)
        layers_preserved = sum(mapping[state][2] == state[2] for state in x40)
        orientation_reversing = all(
            mapping[n_op(state)] == inverse_n(mapping[state]) for state in x40
        )
        two_pass = all(mapping[mapping[state]] == state for state in x40)
        profile = cycle_profile(mapping)
        fixed_sectors = sorted({state[0] for state in x40 if mapping[state] == state})
        signatures[word] = {
            "ALGO": {
                "fixed_ratio": f"{fixed}/40",
                "moved_ratio": f"{40-fixed}/40",
                "package_preservation_ratio": f"{packages_preserved}/40",
                "layer_preservation_ratio": f"{layers_preserved}/40",
            },
            "OLGO": {
                "orientation": "reversing" if orientation_reversing else "not_reversing",
                "reflection_axis_sectors": fixed_sectors,
                "conjugates_N_to_inverse": orientation_reversing,
            },
            "OKO": {
                "cycle_profile": {str(key): value for key, value in profile.items()},
                "permutation_order": permutation_order(mapping),
                "one_pass_exact_all_states": fixed == 40,
                "two_pass_exact_all_states": two_pass,
            },
        }
    check(
        "M4 ALGO proportions are 1/5 fixed and 4/5 moved",
        all(
            signature["ALGO"]["fixed_ratio"] == "8/40"
            and signature["ALGO"]["moved_ratio"] == "32/40"
            for signature in signatures.values()
        ),
        {word: signature["ALGO"] for word, signature in signatures.items()},
        {"fixed_ratio": "8/40", "moved_ratio": "32/40"},
    )
    check(
        "M4 OLGO mirror law holds for every order",
        all(signature["OLGO"]["conjugates_N_to_inverse"] for signature in signatures.values()),
        {word: signature["OLGO"] for word, signature in signatures.items()},
        "f N f = N^-1 for all six compiled maps",
    )
    check(
        "M4 OKO gives orientation change after one pass and exact two-pass return",
        all(
            not signature["OKO"]["one_pass_exact_all_states"]
            and signature["OKO"]["two_pass_exact_all_states"]
            and signature["OKO"]["permutation_order"] == 2
            and signature["OKO"]["cycle_profile"] == {"1": 8, "2": 16}
            for signature in signatures.values()
        ),
        {word: signature["OKO"] for word, signature in signatures.items()},
        {"one_pass_exact_all_states": False, "two_pass_exact_all_states": True, "order": 2},
    )
    envelope_axes = sorted({tuple(signature["OLGO"]["reflection_axis_sectors"]) for signature in signatures.values()})
    check(
        "M4 envelope contains two mirror-axis signatures",
        len(envelope_axes) == 2,
        envelope_axes,
        "two distinct reflection-axis signatures",
    )

    # M5 — Operator 16 is the record composition; X16 remains unmapped.
    operator_16_records = {
        word: {
            "ALGO": signatures[word]["ALGO"],
            "OLGO": signatures[word]["OLGO"],
            "OKO": signatures[word]["OKO"],
        }
        for word in words
    }
    x16 = list(itertools.product((0, 1), repeat=4))
    x16_action = None
    check(
        "M5 Operator 16 composes three typed measurement records",
        len(operator_16_records) == 6
        and all(set(record) == {"ALGO", "OLGO", "OKO"} for record in operator_16_records.values()),
        {"records": len(operator_16_records), "fields": ["ALGO", "OLGO", "OKO"]},
        "six three-track records",
    )
    check(
        "M5 separate sixteen-state carrier remains explicitly unmapped",
        len(x16) == 16 and x16_action is None,
        {"x16_cardinality": len(x16), "declared_action": x16_action},
        {"x16_cardinality": 16, "declared_action": None},
    )

    passed = all(item["status"] == "PASS" for item in checks)
    return {
        "schema": "nexah.ncs-snc-292-929-order-envelope-return-result/1.0.0",
        "date": contract["date"],
        "status": "PASS_WITH_BOUNDARIES" if passed else "FAIL",
        "classification": "PASS_TWO_ORDER_CLASSES_WITH_OPEN_HISTORICAL_BINDING" if passed else "CONTRACT_INVALID",
        "identity_reused": contract["identity"]["reuse"],
        "creates": contract["identity"]["creates"],
        "summary": {
            "checks_passed": sum(item["status"] == "PASS" for item in checks),
            "checks_total": len(checks),
            "operator_words": words,
            "distinct_order_classes": len(grouped),
            "order_classes": order_classes,
            "ncs_snc_different_states": ncs_snc_difference,
            "w20_node_count": len(w20),
            "w20_weight_each": 20,
            "w20_weighted_subtotal": 100,
            "historical_ncs_decomposition_recovered": None,
            "address_to_x40_map": None,
            "x16_action": None,
        },
        "module_1_typed_registers": numeric,
        "module_2_w20": {
            "indices": w20,
            "node_ids": w20_ids,
            "d5_orbit": orbit,
            "internal_edges": len(internal_edges),
            "incoming_per_node": {str(index): incoming[index] for index in w20},
            "outgoing_edges": sum(outgoing.values()),
            "weighted_subtotal": 100,
        },
        "module_3_order_scan": {
            "convention": contract["operator_convention"],
            "classes": order_classes,
            "ncs_snc_different_states": ncs_snc_difference,
        },
        "module_4_envelope": {
            "distinct_reflection_axes": envelope_axes,
            "signatures": signatures,
        },
        "module_5_operator_16": {
            "meaning": contract["measurement_stack"]["OPERATOR_16"],
            "records": operator_16_records,
            "x16_cardinality": len(x16),
            "x16_action": x16_action,
        },
        "ilau": {
            "retained": [
                "package coordinate",
                "layer coordinate after the full three-operator word",
                "1/5 fixed-state ratio",
                "4/5 moved-state ratio",
                "reflection conjugacy",
                "two-pass exact return",
                "W20 D5 orbit and weight",
            ],
            "lost": [],
            "introduced": [
                "declared N/S/C short names for the parent finite maps",
                "ALGO/OLGO/OKO measurement-role crosswalk",
            ],
            "unresolved": [
                "historical meaning of NCS letters",
                "292/929 address map into X40",
                "action on the separate sixteen-state carrier",
                "canonical Operator identity",
            ],
        },
        "source_resolution": source_resolution,
        "checks": checks,
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    result = validate()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
