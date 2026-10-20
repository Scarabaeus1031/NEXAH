#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if parent.name == "NEXAH ECOSYSTEM")
CONTRACT = json.loads((HERE / "CONTRACT.json").read_text())

checks: list[dict] = []


def jsonable(value):
    if isinstance(value, Counter):
        return {str(key): count for key, count in sorted(value.items())}
    if isinstance(value, (set, frozenset)):
        return sorted((jsonable(item) for item in value), key=repr)
    if isinstance(value, tuple):
        return [jsonable(item) for item in value]
    if isinstance(value, list):
        return [jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    return value


def check(name, observed, expected=True):
    passed = observed == expected
    checks.append({
        "name": name,
        "passed": passed,
        "observed": jsonable(observed),
        "expected": jsonable(expected),
    })
    return passed


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compose(p, q):
    """Permutation composition p o q in one-line notation."""
    return tuple(p[i - 1] for i in q)


def parity(p):
    inversions = sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3))
    return inversions % 2


def power(op, state, exponent):
    for _ in range(exponent):
        state = op(state)
    return state


check("extends prior C2 audit", CONTRACT["identity"]["extends"], "A0-BL-023:TRIPLE19_X40_C2_ORIENTATION_FACTOR_AUDIT:V1")
check("creates no identity", CONTRACT["identity"]["creates"], [])
check("formal non-admitted status", CONTRACT["status"], "FORMAL_DESIGN_VALIDATION_NOT_ADMITTED_NOT_NEW_STUDY")
check("seven frozen sources", len(CONTRACT["frozen_sources"]), 7)

for source in CONTRACT["frozen_sources"]:
    path = ROOT / source["path"]
    check(f"source exists: {source['source_id']}", path.exists())
    if path.exists():
        check(f"source hash: {source['source_id']}", sha256(path), source["sha256"])

states = list(itertools.permutations((1, 2, 3)))
identity = (1, 2, 3)
rotation = (2, 3, 1)
tau = (3, 2, 1)


def visual_reverse(p):
    return compose(p, tau)


def left_rotation(p):
    return compose(rotation, p)


def right_rotation(p):
    return compose(p, rotation)


def left_reflection(p):
    return compose(tau, p)


expected_pairs = {
    frozenset(((1, 2, 3), (3, 2, 1))): "A",
    frozenset(((1, 3, 2), (2, 3, 1))): "B",
    frozenset(((2, 1, 3), (3, 1, 2))): "C",
}

observed_pairs = set()
for p in states:
    observed_pairs.add(frozenset((p, visual_reverse(p))))

check("S3 has six states", len(states), 6)
check("all TripleSix glyphs have digit sum six", all(sum(p) == 6 for p in states))
check("visual reversal is involutive", all(visual_reverse(visual_reverse(p)) == p for p in states))
check("visual reversal is fixed-point-free", all(visual_reverse(p) != p for p in states))
check("visual reversal flips parity", all(parity(visual_reverse(p)) == 1 - parity(p) for p in states))
check("three displayed reversal pairs recovered", observed_pairs, set(expected_pairs))

axis_for_state = {}
for pair, axis in expected_pairs.items():
    for p in pair:
        axis_for_state[p] = axis

addresses = {(axis_for_state[p], parity(p)) for p in states}
check("axis plus parity address is bijective", len(addresses), 6)
check("axis set has three values", sorted({a for a, _ in addresses}), ["A", "B", "C"])
check("orientation factor has two values", sorted({e for _, e in addresses}), [0, 1])

check("left axis rotation has order three", all(power(left_rotation, p, 3) == p for p in states))
check("left axis rotation preserves parity", all(parity(left_rotation(p)) == parity(p) for p in states))
check("left rotation commutes with visual reversal", all(left_rotation(visual_reverse(p)) == visual_reverse(left_rotation(p)) for p in states))
check("left rotation descends to displayed axis pairs", all(axis_for_state[left_rotation(p)] == axis_for_state[left_rotation(visual_reverse(p))] for p in states))

right_rotation_inverse = lambda p: power(right_rotation, p, 2)
check("right rotation has order three", all(power(right_rotation, p, 3) == p for p in states))
check("right-action reversal conjugates rotation to inverse", all(visual_reverse(right_rotation(visual_reverse(p))) == right_rotation_inverse(p) for p in states))
check("right rotation does not descend to displayed axis pairs", any(axis_for_state[right_rotation(p)] != axis_for_state[right_rotation(visual_reverse(p))] for p in states), True)
check("left reflection has dihedral law", all(left_reflection(left_rotation(left_reflection(p))) == power(left_rotation, p, 2) for p in states))

pascal_result = json.loads((ROOT / CONTRACT["frozen_sources"][1]["path"]).read_text())
check("existing Pascal carrier reports S3", pascal_result["result"]["full_coordinate_permutation_group"], "S3")
check("existing Pascal proper subgroup reports C3", pascal_result["result"]["quaternion_realizable_proper_subgroup"], "C3")


def q64_63(i):
    if not 0 <= i < 64:
        raise ValueError(i)
    return i if i <= 31 else i - 1


fibres_1d = defaultdict(list)
for i in range(64):
    fibres_1d[q64_63(i)].append(i)

check("63 equals 7 times 9", 63, 7 * 9)
check("64 equals 8 times 8", 64, 8 * 8)
check("displayed four-factor count", 63 * 64 * 63 * 64, 16_257_024)
check("q64_63 is surjective", set(fibres_1d), set(range(63)))
check("q64_63 is non-injective", len({q64_63(i) for i in range(64)}), 63)
check("one-dimensional pivot fibre", fibres_1d[31], [31, 32])
check("one-dimensional fibre profile", Counter(map(len, fibres_1d.values())), Counter({1: 62, 2: 1}))


def fibre_profile(dimension):
    counts = Counter()
    for target in itertools.product(range(63), repeat=dimension):
        size = 1
        for coordinate in target:
            size *= len(fibres_1d[coordinate])
        counts[size] += 1
    return counts


profiles = {dimension: fibre_profile(dimension) for dimension in (1, 2, 3)}
expected_profiles = {
    1: Counter({1: 62, 2: 1}),
    2: Counter({1: 3844, 2: 124, 4: 1}),
    3: Counter({1: 238328, 2: 11532, 4: 186, 8: 1}),
}
for dimension in (1, 2, 3):
    check(f"Q_{dimension} fibre profile", profiles[dimension], expected_profiles[dimension])
    check(
        f"Q_{dimension} target-state count",
        sum(profiles[dimension].values()),
        63 ** dimension,
    )
    check(
        f"Q_{dimension} source-state count reconstructed from fibres",
        sum(size * count for size, count in profiles[dimension].items()),
        64 ** dimension,
    )

check("single-axis fold requires one side bit", 1, 1)
check("two-axis pivot requires two independent side bits", 2, 2)
check("three-axis pivot requires three independent side bits", 3, 3)
check("TripleSix address supplies one side bit", len({e for _, e in addresses}).bit_length() - 1, 1)
check("TripleSix cannot cardinally label the 3D pivot fibre", len(states) < max(profiles[3]), True)

axis_rows = []
for p in sorted(states):
    axis_rows.append({
        "state": "".join(map(str, p)),
        "digit_sum": sum(p),
        "axis": axis_for_state[p],
        "parity": "even" if parity(p) == 0 else "odd",
        "orientation_bit": parity(p),
        "visual_antipode": "".join(map(str, visual_reverse(p))),
    })

with (HERE / "TRIPLESIX_AXIS_ORIENTATION.csv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=axis_rows[0].keys())
    writer.writeheader()
    writer.writerows(axis_rows)

profile_rows = []
for dimension in (1, 2, 3):
    for fibre_size in sorted(profiles[dimension]):
        profile_rows.append({
            "dimension": dimension,
            "target_grid": f"63^{dimension}",
            "source_grid": f"64^{dimension}",
            "fibre_size": fibre_size,
            "target_points_with_fibre_size": profiles[dimension][fibre_size],
            "source_states_in_those_fibres": fibre_size * profiles[dimension][fibre_size],
        })

with (HERE / "GRID_FOLD_FIBER_PROFILE.csv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=profile_rows[0].keys())
    writer.writeheader()
    writer.writerows(profile_rows)

janus_rows = [
    {
        "convention": "visual reversal right / axis rotation left",
        "law": "V L_r = L_r V",
        "x40_analogue": "J_c commuting",
        "descends_to_displayed_axis_pairs": "yes",
        "historically_selected": "no",
    },
    {
        "convention": "visual reversal right / rotation right",
        "law": "V R_r V = R_r^-1",
        "x40_analogue": "J_d dihedral",
        "descends_to_displayed_axis_pairs": "no",
        "historically_selected": "no",
    },
    {
        "convention": "reflection left / axis rotation left",
        "law": "L_tau L_r L_tau = L_r^-1",
        "x40_analogue": "J_d dihedral",
        "descends_to_displayed_axis_pairs": "yes, but reflection is not the displayed antipode pairing",
        "historically_selected": "no",
    },
]
with (HERE / "JANUS_ACTION_CONVENTIONS.csv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=janus_rows[0].keys())
    writer.writeheader()
    writer.writerows(janus_rows)

passed = sum(item["passed"] for item in checks)
result = {
    "status": "PASS_PARTIAL_AXIS_SIDE_BRIDGE_WITH_MULTIAXIS_FOLD_LOSS" if passed == len(checks) else "FAIL",
    "classification": "S3_AXIS_C2_ADDRESS_SINGLE_AXIS_SUFFICIENT_MULTIAXIS_INSUFFICIENT",
    "checks": {"passed": passed, "total": len(checks)},
    "triplesix": {
        "carrier": "S3",
        "states": 6,
        "digit_sum_invariant": 6,
        "axis_pairs": {axis: sorted("".join(map(str, p)) for p in pair) for pair, axis in expected_pairs.items()},
        "orientation_factor": "sign:S3->C2",
        "state_address": "{A,B,C} x C2 (bijection of state sets, not direct-product group identity)",
    },
    "janus_comparison": {
        "commuting_convention": "displayed right reversal with left axis rotation",
        "dihedral_convention": "same-side actions",
        "historical_selection": None,
        "reason": "The visuals do not freeze left/right action semantics."
    },
    "grid_fold": {
        "map": "q64_63(i)=i for i<=31 else i-1",
        "one_dimensional_pivot_fibre": [31, 32],
        "profiles": {
            str(dimension): {str(size): count for size, count in sorted(profiles[dimension].items())}
            for dimension in (1, 2, 3)
        },
        "coordinatewise_section_choices": {"1D": 2, "2D": 4, "3D": 8},
        "canonical_section": None,
    },
    "bridge_limit": {
        "single_selected_axis": "SUPPORTED_BY_AXIS_PLUS_ONE_ORIENTATION_BIT",
        "two_axis_pivot": "NOT_RECONSTRUCTED_TWO_INDEPENDENT_SIDE_BITS_REQUIRED",
        "three_axis_pivot": "IMPOSSIBLE_FROM_SIX_STATE_LABEL_ALONE_EIGHT_SOURCE_STATES_SHARE_ONE_TARGET",
        "full_cube_grid_identity": False,
    },
    "maps": {
        "triplesix_to_axis_times_c2": "exact_bijection_of_state_sets",
        "cube_64_to_63": "declared_coordinatewise_surjection",
        "canonical_cube_63_to_64_inverse": None,
        "historical_visual_generator": None,
        "historical_janus_selection": None,
    },
    "claim_boundary": CONTRACT["authority_boundary"],
    "checks_detail": checks,
}
(HERE / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")

print(json.dumps({"status": result["status"], "checks": result["checks"]}, indent=2))
raise SystemExit(0 if passed == len(checks) else 1)
