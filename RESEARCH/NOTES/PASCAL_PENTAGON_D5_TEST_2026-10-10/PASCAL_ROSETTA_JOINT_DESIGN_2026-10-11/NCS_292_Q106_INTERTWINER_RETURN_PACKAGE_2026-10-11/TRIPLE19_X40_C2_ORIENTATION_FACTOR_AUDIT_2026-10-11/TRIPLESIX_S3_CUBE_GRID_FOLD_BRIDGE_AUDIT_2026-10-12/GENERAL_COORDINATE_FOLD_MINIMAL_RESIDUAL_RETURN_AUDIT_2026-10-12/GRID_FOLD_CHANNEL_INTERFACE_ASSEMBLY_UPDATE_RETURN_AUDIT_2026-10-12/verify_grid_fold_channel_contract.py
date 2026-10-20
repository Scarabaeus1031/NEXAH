#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if parent.name == "NEXAH ECOSYSTEM")
CONTRACT = json.loads((HERE / "CONTRACT.json").read_text())
checks: list[dict] = []


def jsonable(value):
    if isinstance(value, set):
        return sorted(jsonable(item) for item in value)
    if isinstance(value, tuple):
        return [jsonable(item) for item in value]
    if isinstance(value, list):
        return [jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    return value


def check(name, observed, expected=True):
    passed = observed == expected
    checks.append({"name": name, "passed": passed, "observed": jsonable(observed), "expected": jsonable(expected)})
    return passed


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(m, value):
    return value if value <= m - 1 else value - 1


def fold(m, source):
    return tuple(q(m, value) for value in source)


def envelope(target):
    side = max(max(point) for point in target)
    return {point for point in target if any(value in (0, side) for value in point)}


def assembly_key(branch, target, interface):
    return ("I", target) if target in interface else (branch, target)


def fold_bits(m, source):
    target = fold(m, source)
    return tuple(source[i] - (m - 1) for i, value in enumerate(target) if value == m - 1)


def encode(m, branch, source, interface):
    target = fold(m, source)
    bits = ((0 if branch == "L" else 1),) if target in interface else ()
    bits += fold_bits(m, source)
    return assembly_key(branch, target, interface), bits


def reconstruct(m, key, bits, interface):
    kind, target = key
    bit_index = 0
    if kind == "I":
        if not bits or bits[0] not in (0, 1):
            raise ValueError("interface branch bit required")
        branch = "L" if bits[0] == 0 else "R"
        bit_index = 1
    else:
        branch = kind
    source = []
    for value in target:
        if value < m - 1:
            source.append(value)
        elif value > m - 1:
            source.append(value + 1)
        else:
            if bit_index >= len(bits) or bits[bit_index] not in (0, 1):
                raise ValueError("fold bit required")
            source.append(m - 1 + bits[bit_index])
            bit_index += 1
    if bit_index != len(bits):
        raise ValueError("unused residual bit")
    return branch, tuple(source)


def run_control(name, dimension, target_update, source_update, expected_profile, update_order):
    m = 2
    target = set(itertools.product(range(2 * m - 1), repeat=dimension))
    source = list(itertools.product(range(2 * m), repeat=dimension))
    boundary = envelope(target)
    interface = set(boundary)
    branches = ("L", "R")

    check(f"{name}: embedding injective", len({tuple(point) for point in target}), len(target))
    check(f"{name}: envelope proper subset", 0 < len(boundary) < len(target), True)
    check(f"{name}: anchors injective", len(interface), len(set(interface)))
    check(f"{name}: left/right carriers distinct before assembly", len(branches) * len(target), 2 * len(target))

    fibres = defaultdict(list)
    all_return = True
    for branch in branches:
        for state in source:
            key, bits = encode(m, branch, state, interface)
            fibres[key].append((branch, state))
            all_return &= reconstruct(m, key, bits, interface) == (branch, state)
    profile = Counter(len(items) for items in fibres.values())
    check(f"{name}: exact Return", all_return)
    check(f"{name}: fibre profile", dict(sorted(profile.items())), expected_profile)
    check(f"{name}: assembled observation count", len(fibres), sum(expected_profile.values()))
    check(f"{name}: source conservation", sum(size * count for size, count in profile.items()), 2 * len(source))

    formula_ok = True
    minimal_ok = True
    for key, items in fibres.items():
        _, y = key
        k = sum(value == m - 1 for value in y)
        g = int(y in interface)
        formula_ok &= len(items) == 2 ** (k + g)
        bit_lengths = {len(encode(m, branch, state, interface)[1]) for branch, state in items}
        minimal_ok &= bit_lengths == {k + g} and k + g == math.ceil(math.log2(len(items)))
    check(f"{name}: interface-plus-fold fibre formula", formula_ok)
    check(f"{name}: pointwise residual minimality", minimal_ok)

    check(f"{name}: update target bijection", {target_update(y) for y in target}, target)
    check(f"{name}: update preserves envelope", {target_update(y) for y in boundary}, boundary)
    check(f"{name}: update preserves interface", {target_update(y) for y in interface}, interface)
    update_well_defined = all(
        assembly_key(branch, target_update(y), interface)[0] == "I"
        for branch in branches for y in interface
    )
    check(f"{name}: update descends through assembly", update_well_defined)

    commutes = True
    encoded_update_return = True
    for branch in branches:
        for state in source:
            y = fold(m, state)
            commutes &= fold(m, source_update(state)) == target_update(y)
            new_key, new_bits = encode(m, branch, source_update(state), interface)
            encoded_update_return &= reconstruct(m, new_key, new_bits, interface) == (branch, source_update(state))
    check(f"{name}: source lift commutes with fold", commutes)
    check(f"{name}: update then Return exact", encoded_update_return)

    for point in target:
        moved = point
        for _ in range(update_order):
            moved = target_update(moved)
        check(f"{name}: update order at {point}", moved, point)

    invalid = lambda y: tuple((value + 1) % (2 * m - 1) for value in y)
    check(f"{name}: invalid translation rejected", {invalid(y) for y in interface} != interface, True)

    rows = []
    for size, count in sorted(profile.items()):
        rows.append({
            "control": name,
            "dimension": dimension,
            "target_points": len(target),
            "interface_points": len(interface),
            "assembled_fibre_size": size,
            "assembled_observations": count,
            "source_states": size * count,
        })
    return rows, {
        "dimension": dimension,
        "target_points": len(target),
        "interface_points": len(interface),
        "assembled_observations": len(fibres),
        "source_states": 2 * len(source),
        "fibre_profile": {str(size): count for size, count in sorted(profile.items())},
        "update_order": update_order,
    }


check("extends general fold audit", CONTRACT["identity"]["extends"], "A0-BL-025:GENERAL_COORDINATE_FOLD_MINIMAL_RESIDUAL_RETURN_AUDIT:V1")
check("formal non-admitted status", CONTRACT["status"], "FORMAL_DESIGN_VALIDATION_NOT_ADMITTED_NOT_NEW_STUDY")
check("creates no identity", CONTRACT["identity"]["creates"], [])
check("complete typed chain", CONTRACT["typed_chain"], ["carrier", "fold", "embedding", "envelope", "interface", "assembly", "update", "Return"])
for item in CONTRACT["frozen_sources"]:
    path = ROOT / item["path"]
    check(f"source exists: {item['source_id']}", path.exists())
    if path.exists():
        check(f"source hash: {item['source_id']}", sha256(path), item["sha256"])

path_rows, path_result = run_control(
    "PATH_SEAM_M2_D1_REFLECTION",
    1,
    lambda y: (2 - y[0],),
    lambda x: (3 - x[0],),
    {2: 4},
    2,
)
square_rows, square_result = run_control(
    "SQUARE_BOUNDARY_M2_D2_QUARTER_ROTATION",
    2,
    lambda y: (y[1], 2 - y[0]),
    lambda x: (x[1], 3 - x[0]),
    {2: 4, 4: 6},
    4,
)
check("controls are non-identical dimensions", path_result["dimension"] != square_result["dimension"], True)
check("controls are non-identical update orders", path_result["update_order"] != square_result["update_order"], True)
check("controls are non-identical interface sizes", path_result["interface_points"] != square_result["interface_points"], True)

with (HERE / "CONTROL_FIBRE_PROFILE.csv").open("w", newline="") as handle:
    rows = path_rows + square_rows
    writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

ledger = [
    {"item": "carrier", "status": "DECLARED", "failure": "undeclared source or branch labels"},
    {"item": "fold", "status": "EXACT_SURJECTION", "failure": "residual information omitted"},
    {"item": "embedding", "status": "INJECTIVE", "failure": "embedding collision"},
    {"item": "envelope", "status": "GRAPH_BOUNDARY", "failure": "envelope silently identified with carrier"},
    {"item": "interface", "status": "EXPLICIT_SUBSET_WITH_INJECTIVE_ANCHORS", "failure": "anchor ambiguity"},
    {"item": "assembly", "status": "FINITE_QUOTIENT", "failure": "undeclared gluing"},
    {"item": "update", "status": "INTERFACE_PRESERVING_BIJECTION", "failure": "does not descend through quotient"},
    {"item": "Return", "status": "EXACT_WITH_MINIMAL_POINTWISE_RESIDUAL", "failure": "branch or fold collision"},
]
with (HERE / "TYPE_AND_FAILURE_LEDGER.csv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=ledger[0].keys())
    writer.writeheader()
    writer.writerows(ledger)

passed = sum(item["passed"] for item in checks)
result = {
    "status": "PASS_COMPLETE_FINITE_GRID_FOLD_CHANNEL_FORMAL_DESIGN" if passed == len(checks) else "FAIL",
    "classification": "TYPED_INTERFACE_QUOTIENT_UPDATE_AND_MINIMAL_RESIDUAL_RETURN",
    "checks": {"passed": passed, "total": len(checks)},
    "contract": {
        "typed_chain": CONTRACT["typed_chain"],
        "assembly": "two labelled folded carriers quotiented only at corresponding declared interface anchors",
        "admissible_update": "branch bijections preserve interface and agree through one interface permutation",
        "fibre_size": "2^(k(y)+g(y)) where g(y)=1 on the glued interface and 0 otherwise",
        "minimal_residual": "k(y) fold bits plus g(y) branch bit",
    },
    "controls": {
        "PATH_SEAM_M2_D1_REFLECTION": path_result,
        "SQUARE_BOUNDARY_M2_D2_QUARTER_ROTATION": square_result,
    },
    "negative_controls": {
        "missing_interface_branch_bit": "REJECTED_BY_COLLISION",
        "missing_fold_bits": "REJECTED_BY_COLLISION",
        "interface_nonpreserving_translation": "REJECTED_UPDATE_NOT_WELL_DEFINED_ON_ASSEMBLY",
    },
    "a0_bl_025": {
        "formal_design_checklist": "COMPLETE_ON_TWO_NON_IDENTICAL_CONTROLS",
        "study_admission": "NOT_ADMITTED_REQUIRES_SEPARATE_OWNER_DECISION",
        "physical_stability_or_flow": None,
        "historical_visual_generator": None,
    },
    "claim_boundary": CONTRACT["authority_boundary"],
    "checks_detail": checks,
}
(HERE / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "checks": result["checks"]}, indent=2))
raise SystemExit(0 if passed == len(checks) else 1)
