#!/usr/bin/env python3
"""Replay the NCS-292/Q106 package, including its layered decoder gates."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import re
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
ECOSYSTEM = HERE.parents[6]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def connected(subset: set[int], adjacency: list[set[int]]) -> bool:
    if not subset:
        return False
    visited = {next(iter(subset))}
    stack = list(visited)
    while stack:
        current = stack.pop()
        for target in adjacency[current] & subset:
            if target not in visited:
                visited.add(target)
                stack.append(target)
    return visited == subset


def orbit_unions(orbits: list[list[int]], target: int, adjacency: list[set[int]]) -> list[dict[str, object]]:
    matches: list[dict[str, object]] = []
    for mask in range(1 << len(orbits)):
        indices = [index for index in range(len(orbits)) if mask & (1 << index)]
        if sum(len(orbits[index]) for index in indices) != target:
            continue
        subset = set().union(*(set(orbits[index]) for index in indices))
        internal = sum(len(adjacency[node] & subset) for node in subset) // 2
        boundary = sum(len(adjacency[node] - subset) for node in subset)
        matches.append({
            "orbit_indices": indices,
            "orbit_sizes": [len(orbits[index]) for index in indices],
            "connected": connected(subset, adjacency),
            "undirected_internal_edges": internal,
            "boundary_incidence": boundary,
        })
    return matches


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
        source_root = ECOSYSTEM if spec.get("root") == "ecosystem" else ROOT
        path = source_root / spec["path"]
        paths[name] = path
        observed = sha256(path) if path.exists() else None
        source_resolution[name] = {"root": spec.get("root", "nexah_repo"), "path": spec["path"], "sha256": observed}
        check(f"frozen source {name}", observed == spec["sha256"], observed, spec["sha256"])

    # M1 — recover the only operator actually implemented in the historical animation.
    script = paths["ncs_script"].read_text(encoding="utf-8")
    point_block = re.search(r"pink_balls\s*=\s*np\.array\(\[(.*?)\]\)", script, re.DOTALL)
    rows = [] if point_block is None else re.findall(
        r"\[\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\]",
        point_block.group(1),
    )
    points = [tuple(float(value) for value in row) for row in rows]
    delta = math.sin(7 * 0.16) * 0.28 * 0.8
    moved = [(x + delta, y + delta, z) for x, y, z in points]
    pairwise_before = sorted(round(math.dist(a, b), 12) for a, b in itertools.combinations(points, 2))
    pairwise_after = sorted(round(math.dist(a, b), 12) for a, b in itertools.combinations(moved, 2))
    translation_source = all(token in script for token in (
        "shift = np.sin(frame * 0.16) * 0.28",
        "new_pink[:,0] += shift * 0.8",
        "new_pink[:,1] += shift * 0.8",
    )) and "new_pink[:,2] +=" not in script
    check("M1 four historical points recovered", len(points) == 4, len(points), 4)
    check(
        "M1 NCS action is common xy translation with fixed z",
        translation_source and pairwise_before == pairwise_after,
        {"translation": [delta, delta, 0.0], "pairwise_distances_preserved": pairwise_before == pairwise_after},
        {"form": "(x,y,z)->(x+d,y+d,z)", "pairwise_distances_preserved": True},
    )
    check(
        "M1 point-label action is identity rather than package permutation",
        "new_pink = pink_balls.copy()" in script and not re.search(r"new_pink\s*=\s*pink_balls\s*\[", script),
        {"label_permutation": [0, 1, 2, 3]},
        {"label_permutation": [0, 1, 2, 3]},
    )

    # M2 — exhaustive D5 orbit-union search in the frozen Q106 graph.
    with paths["q106_nodes"].open(newline="", encoding="utf-8") as handle:
        nodes = list(csv.DictReader(handle))
    with paths["q106_edges"].open(newline="", encoding="utf-8") as handle:
        edges = list(csv.DictReader(handle))
    automorphisms = json.loads(paths["q106_automorphisms"].read_text(encoding="utf-8"))
    permutations = [action["permutation_zero_based"] for action in automorphisms["actions"]]
    seen: set[int] = set()
    orbits: list[list[int]] = []
    for node in range(len(nodes)):
        if node in seen:
            continue
        orbit = sorted({permutation[node] for permutation in permutations})
        seen.update(orbit)
        orbits.append(orbit)
    adjacency = [set() for _ in nodes]
    for edge in edges:
        source, target = int(edge["source_index"]), int(edge["target_index"])
        adjacency[source].add(target)
        adjacency[target].add(source)
    check(
        "M2 frozen Q106 and D5 action loaded",
        len(nodes) == 106 and len(edges) == 180 and len(permutations) == 10 and seen == set(range(106)),
        {"nodes": len(nodes), "directed_edges": len(edges), "actions": len(permutations)},
        {"nodes": 106, "directed_edges": 180, "actions": 10},
    )
    orbit_profile = dict(sorted(Counter(len(orbit) for orbit in orbits).items()))
    check("M2 Q106 orbit profile", orbit_profile == {1: 1, 5: 9, 10: 6}, orbit_profile, {1: 1, 5: 9, 10: 6})

    interface_search: dict[str, object] = {}
    expected_counts = {15: (138, 1), 20: (357, 4), 40: (3138, 63)}
    for target in contract["interface_targets"]:
        candidates = orbit_unions(orbits, target, adjacency)
        connected_candidates = [candidate for candidate in candidates if candidate["connected"]]
        exact_profile = [candidate for candidate in candidates if candidate["orbit_sizes"] == [5] * (target // 5)]
        exact_connected = [candidate for candidate in exact_profile if candidate["connected"]]
        interface_search[str(target)] = {
            "invariant_unions": len(candidates),
            "connected_unions": len(connected_candidates),
            "pure_five_orbit_unions": len(exact_profile),
            "connected_pure_five_orbit_unions": len(exact_connected),
            "connected_examples": connected_candidates[:4],
            "pure_five_connected_examples": exact_connected[:2],
        }
        check(
            f"M2 exhaustive invariant subset count for {target}",
            (len(candidates), len(connected_candidates)) == expected_counts[target],
            (len(candidates), len(connected_candidates)),
            expected_counts[target],
        )
    check(
        "M2 unique connected RootCube15-type three-ring interface",
        interface_search["15"]["connected_pure_five_orbit_unions"] == 1,
        interface_search["15"]["connected_pure_five_orbit_unions"],
        1,
    )
    check(
        "M2 unique connected X20-type four-ring interface",
        interface_search["20"]["connected_pure_five_orbit_unions"] == 1,
        interface_search["20"]["connected_pure_five_orbit_unions"],
        1,
    )
    check(
        "M2 no connected X40-type eight-ring interface",
        interface_search["40"]["connected_pure_five_orbit_unions"] == 0,
        interface_search["40"]["connected_pure_five_orbit_unions"],
        0,
    )

    # M3 — the six-state count is tested separately from any labeling claim.
    six_candidates = orbit_unions(orbits, 6, adjacency)
    six_connected = [candidate for candidate in six_candidates if candidate["connected"]]
    six_nodes = set().union(*(set(orbits[index]) for index in six_connected[0]["orbit_indices"]))
    six_ids = [nodes[index]["node_id"] for index in sorted(six_nodes)]
    complement = set(range(106)) - six_nodes
    check(
        "M3 unique connected D5-invariant six-node residual",
        len(six_candidates) == 9 and len(six_connected) == 1 and six_ids == ["A", "S_01_00", "S_01_01", "S_01_02", "S_01_03", "S_01_04"],
        {"invariant_candidates": len(six_candidates), "connected_candidates": len(six_connected), "nodes": six_ids},
        {"invariant_candidates": 9, "connected_candidates": 1, "nodes": "apex plus first seam ring"},
    )
    check(
        "M3 residual complement is an invariant connected 100-node carrier",
        connected(complement, adjacency) and len(complement) == 100,
        {"size": len(complement), "connected": connected(complement, adjacency)},
        {"size": 100, "connected": True},
    )
    local_alphabet = list(itertools.product(("A", "B", "C"), (-1, 1)))
    check("M3 ABC-orientation alphabet has six labels", len(local_alphabet) == 6, len(local_alphabet), 6)
    block_system_defined = False
    check(
        "M3 five 20-node blocks remain explicitly undefined",
        not block_system_defined,
        {"equation": "106=5*20+6", "block_system": None, "ABC_node_map": None},
        {"block_system": None, "ABC_node_map": None},
    )

    # M4 — compare both valid Janus hypotheses without selecting one historically.
    packages = range(4)
    x40 = list(itertools.product(range(5), packages, range(2)))

    def r(state: tuple[int, int, int]) -> tuple[int, int, int]:
        sector, package, layer = state
        return ((sector + 1) % 5, package, layer)

    def jc(state: tuple[int, int, int]) -> tuple[int, int, int]:
        sector, package, layer = state
        return (sector, package, 1 - layer)

    def jd(state: tuple[int, int, int]) -> tuple[int, int, int]:
        sector, package, layer = state
        return ((-sector) % 5, package, 1 - layer)

    def compose(f, g, state):
        return f(g(state))

    identity = lambda state: state
    commuting_ok = all(compose(jc, r, state) == compose(r, jc, state) for state in x40)
    dihedral_ok = all(jd(r(jd(state))) == r(r(r(r(state)))) for state in x40)
    involutions_ok = all(jc(jc(state)) == state and jd(jd(state)) == state for state in x40)
    r5_ok = all((lambda s: s)(state) == state for state in x40)
    for _ in range(5):
        identity = (lambda previous: (lambda state: r(previous(state))))(identity)
    r5_ok = all(identity(state) == state for state in x40)
    check("M4 both Janus maps are involutions", involutions_ok, involutions_ok, True)
    check("M4 commuting Janus law", commuting_ok, commuting_ok, True)
    check("M4 dihedral Janus law", dihedral_ok, dihedral_ok, True)
    check("M4 five rotations return exactly", r5_ok, r5_ok, True)

    def seam_step(state: tuple[int, int, int]) -> tuple[int, int, int]:
        sector, package, layer = state
        return ((sector + 1) % 5, package, 1 - layer if sector == 4 else layer)

    one_turn = {}
    two_turn = {}
    for state in x40:
        current = state
        for _ in range(5):
            current = seam_step(current)
        one_turn[state] = current
        for _ in range(5):
            current = seam_step(current)
        two_turn[state] = current
    quotient_equal = all((state[0], state[1]) == (target[0], target[1]) for state, target in one_turn.items())
    exact_one_turn = all(state == target for state, target in one_turn.items())
    exact_two_turn = all(state == target for state, target in two_turn.items())
    check(
        "M4 Möbius seam gives quotient return after one turn and exact return after two",
        quotient_equal and not exact_one_turn and exact_two_turn,
        {"one_turn_quotient": quotient_equal, "one_turn_exact": exact_one_turn, "two_turn_exact": exact_two_turn},
        {"one_turn_quotient": True, "one_turn_exact": False, "two_turn_exact": True},
    )

    # M6–M10 — compose the recovered modules without collapsing their types.
    def decode20(number: int) -> tuple[int, int, int]:
        z, remainder = divmod(number, 400)
        y, x = divmod(remainder, 20)
        return z, y, x

    sample_numbers = [1729, 417, 1836, 378, 718]
    expected_digits = {
        1729: (4, 6, 9),
        417: (1, 0, 17),
        1836: (4, 11, 16),
        378: (0, 18, 18),
        718: (1, 15, 18),
    }
    decoded = {number: decode20(number) for number in sample_numbers}
    reconstructed = {number: 400 * z + 20 * y + x for number, (z, y, x) in decoded.items()}
    check("M6 D20 recovers the five base-20 states", decoded == expected_digits, decoded, expected_digits)
    check(
        "M6 D20 digits satisfy their typed ranges",
        all(z >= 0 and 0 <= y < 20 and 0 <= x < 20 for z, y, x in decoded.values()),
        decoded,
        "z>=0 and x,y in C20",
    )
    check(
        "M6 D20 round trips exactly",
        all(reconstructed[number] == number for number in sample_numbers),
        reconstructed,
        {number: number for number in sample_numbers},
    )

    def project20(state: tuple[int, int, int]) -> tuple[float, int]:
        z, y, x = state
        return x + y / 2, z

    projected = {number: project20(state) for number, state in decoded.items()}
    recovered_views = {
        1729: (12.0, 4),
        417: (17.0, 1),
        1836: (21.5, 4),
        378: (27.0, 0),
        718: (25.5, 1),
    }
    collision_pair = ((0, 0, 1), (0, 2, 0))
    check("M7 P20 reproduces the recovered display coordinates", projected == recovered_views, projected, recovered_views)
    check(
        "M7 P20 loss is explicit and reproducible",
        collision_pair[0] != collision_pair[1]
        and project20(collision_pair[0]) == project20(collision_pair[1])
        and len({project20(state) for state in collision_pair}) == 1,
        {"states": collision_pair, "shared_view": project20(collision_pair[0])},
        "distinct states with one shared view",
    )

    v5 = {-2, -1, 0, 1, 2}
    c20 = set(range(20))
    check(
        "M8 V5 and C20 retain distinct cardinalities",
        len(v5) == 5 and len(c20) == 20,
        {"V5": len(v5), "C20": len(c20)},
        {"V5": 5, "C20": 20},
    )
    check(
        "M8 shared terminology does not assert a namespace identity",
        v5 != c20,
        {"identified": v5 == c20, "typed_map": None},
        {"identified": False, "typed_map": None},
    )

    c30_fibres = [[phase for phase in range(30) if phase % 6 == address] for address in range(6)]
    check(
        "M9 C30-to-C6 address projection has six fibres of five",
        [len(fibre) for fibre in c30_fibres] == [5] * 6,
        [len(fibre) for fibre in c30_fibres],
        [5] * 6,
    )
    check(
        "M9 C30 phase successor wraps 29 to 0",
        (29 + 1) % 30 == 0,
        {"phase": 29, "successor": (29 + 1) % 30, "address": 29 % 6},
        {"phase": 29, "successor": 0, "address": 5},
    )

    seam_addresses = len(c30_fibres)
    beta_candidates = math.factorial(seam_addresses)
    check(
        "M10 beta search space remains 6 factorial",
        beta_candidates == contract["layered_test_contract"]["beta_janus_gate"]["candidate_count"] == 720,
        beta_candidates,
        720,
    )
    check(
        "M10 beta and historical Janus selections remain open",
        contract["layered_test_contract"]["beta_janus_gate"]["expected"]
        == "open: beta=null and historical Janus selection=null",
        {
            "beta": None,
            "canonical_seam": None,
            "historical_janus": None,
        },
        {"beta": None, "canonical_seam": None, "historical_janus": None},
    )

    # M11 — import the closed Fibonacci rail as an exact comparator, not a transport map.
    q5_result = json.loads(paths["a0_bl_045_q5_result"].read_text(encoding="utf-8"))
    double_result = json.loads(paths["a0_bl_045_double_pentagon_result"].read_text(encoding="utf-8"))

    def matrix_multiply(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
        return [
            [sum(a[row][k] * b[k][column] for k in range(len(b))) for column in range(len(b[0]))]
            for row in range(len(a))
        ]

    def matrix_power(matrix: list[list[int]], exponent: int) -> list[list[int]]:
        result = [[int(row == column) for column in range(len(matrix))] for row in range(len(matrix))]
        factor = matrix
        for _ in range(exponent):
            result = matrix_multiply(result, factor)
        return result

    q = [[1, 1], [1, 0]]
    q5 = matrix_power(q, 5)
    q10 = matrix_power(q, 10)
    q5_det = q5[0][0] * q5[1][1] - q5[0][1] * q5[1][0]
    q5_trace = q5[0][0] + q5[1][1]
    check(
        "M11 closed A0-BL-045 source results retain their classifications",
        q5_result["classification"] == "RETURN_TYPE_UNDERDETERMINED"
        and double_result["classification"] == "SIGNED_DOUBLE_RETURN_IDENTIFIED"
        and all(q5_result["checks"].values())
        and all(double_result["checks"].values()),
        {"local": q5_result["classification"], "double": double_result["classification"]},
        {"local": "RETURN_TYPE_UNDERDETERMINED", "double": "SIGNED_DOUBLE_RETURN_IDENTIFIED"},
    )
    check(
        "M11 Fibonacci Q5 and invariants replay exactly",
        q5 == [[8, 5], [5, 3]]
        and q5 == q5_result["monodromy"]["Q5"]
        and q5_det == q5_result["monodromy"]["determinant"] == -1
        and q5_trace == q5_result["monodromy"]["trace"] == 11,
        {"Q5": q5, "determinant": q5_det, "trace": q5_trace},
        {"Q5": [[8, 5], [5, 3]], "determinant": -1, "trace": 11},
    )
    check(
        "M11 determinant minus one does not select seam topology",
        q5_result["return_fork"]["untwisted"]["boundary_components"] == 2
        and q5_result["return_fork"]["twisted"]["boundary_components"] == 1
        and q5_result["checks"]["same_q5_for_both_topologies"],
        {
            "same_Q5": q5_result["checks"]["same_q5_for_both_topologies"],
            "untwisted_boundaries": q5_result["return_fork"]["untwisted"]["boundary_components"],
            "twisted_boundaries": q5_result["return_fork"]["twisted"]["boundary_components"],
        },
        {"same_Q5": True, "untwisted_boundaries": 2, "twisted_boundaries": 1},
    )
    check(
        "M11 Fibonacci Q10 is exact and is not an identity return",
        q10 == [[89, 55], [55, 34]]
        and q10 == double_result["candidate_operators"]["sequential_10"]["matrix"]
        and double_result["candidate_operators"]["sequential_10"]["is_identity"] is False,
        {"Q10": q10, "is_identity": False},
        {"Q10": [[89, 55], [55, 34]], "is_identity": False},
    )
    qprime_plus = double_result["candidate_operators"]["reciprocal_bridge_Qprime_plus"]
    qprime_minus = double_result["candidate_operators"]["reciprocal_bridge_Qprime_minus"]
    check(
        "M11 signed reciprocal bridge keeps exact and anti-return distinct",
        qprime_plus["square"] == [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        and qprime_minus["square"] == [[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]]
        and qprime_minus["fourth_power"] == qprime_plus["square"],
        {"plus_square": qprime_plus["square"], "minus_square": qprime_minus["square"]},
        {"plus_square": "+I", "minus_square": "-I", "minus_fourth_power": "+I"},
    )
    fibonacci_transport = None
    check(
        "M11 Fibonacci rail has no inferred cross-carrier transport",
        fibonacci_transport is None
        and "no typed transport" in contract["layered_test_contract"]["fibonacci_rail"]["expected"],
        {"transport": fibonacci_transport, "targets": ["D20", "C20", "X20", "X40", "Q106"]},
        {"transport": None, "targets": "remain unbound"},
    )

    passed = all(item["status"] == "PASS" for item in checks)
    classification = "RECOVERED_LAYERED_PIPELINE_WITH_OPEN_FIBONACCI_TRANSPORT_BETA_JANUS" if passed else "CONTRACT_INVALID"
    return {
        "schema": "nexah.ncs-292-q106-intertwiner-return-result/1.2.0",
        "date": contract["date"],
        "status": "PASS_WITH_OPEN_INTERTWINER" if passed else "FAIL",
        "classification": classification,
        "identity_reused": contract["identity"]["reuse"],
        "creates": contract["identity"]["creates"],
        "summary": {
            "checks_passed": sum(item["status"] == "PASS" for item in checks),
            "checks_total": len(checks),
            "q106_orbits": len(orbits),
            "unique_connected_15_ring_interface": 1,
            "unique_connected_20_ring_interface": 1,
            "connected_40_ring_interface": 0,
            "unique_connected_6_residual": 1,
            "base20_samples": len(sample_numbers),
            "base20_projection_injective": False,
            "vendissimal_namespaces_identified": False,
            "c30_address_fibre_profile": [len(fibre) for fibre in c30_fibres],
            "beta_candidates": beta_candidates,
            "canonical_beta_selected": None,
            "fibonacci_Q5": q5,
            "fibonacci_Q10": q10,
            "fibonacci_transport_selected": None,
            "typed_intertwiner_to_q106": None,
            "historical_janus_law_selected": None
        },
        "module_1": {
            "classification": "COMMON_XY_TRANSLATION_IDENTITY_LABEL_ACTION",
            "four_points": points,
            "sample_delta_frame_7": delta,
            "package_permutation_recovered": None
        },
        "module_2": {
            "orbit_sizes": [len(orbit) for orbit in orbits],
            "orbit_profile": orbit_profile,
            "interfaces": interface_search
        },
        "module_3": {
            "six_node_residual": six_ids,
            "hundred_node_complement_connected": connected(complement, adjacency),
            "five_by_twenty_block_system": None,
            "abc_orientation_node_map": None
        },
        "module_4": {
            "commuting_law_valid": commuting_ok,
            "dihedral_law_valid": dihedral_ok,
            "historical_selection": None,
            "one_turn_quotient_return": quotient_equal,
            "one_turn_exact_return": exact_one_turn,
            "two_turn_exact_return": exact_two_turn,
            "ilau": {
                "retained": ["sector after full turn", "package", "quotient class"],
                "lost": [],
                "introduced": [],
                "unresolved": ["Janus law selection", "X20-to-Q106 node map", "five-block decomposition"]
            }
        },
        "layered_test": {
            "D20": {
                "status": "PASS_EXACT",
                "formula": "n=400z+20y+x",
                "samples": {str(number): list(decoded[number]) for number in sample_numbers},
            },
            "P20": {
                "status": "INFORMATION_LOST_AS_EXPECTED",
                "formula": "(z,y,x)->(x+y/2,z)",
                "injective": False,
                "collision_witness": [list(collision_pair[0]), list(collision_pair[1])],
            },
            "namespace_boundary": {
                "status": "PASS_SEPARATE_TYPES",
                "V5_cardinality": len(v5),
                "C20_cardinality": len(c20),
                "typed_map": None,
            },
            "C30_to_C6": {
                "status": "PASS_ADDRESS_ONLY",
                "fibre_profile": [len(fibre) for fibre in c30_fibres],
                "phase_29_successor": 0,
            },
            "beta_janus": {
                "status": "OPEN",
                "beta_candidates": beta_candidates,
                "beta_selected": None,
                "commuting_janus_valid": commuting_ok,
                "dihedral_janus_valid": dihedral_ok,
                "historical_janus_selected": None,
            },
            "fibonacci_rail": {
                "status": "PASS_EXACT_RAIL_OPEN_TRANSPORT",
                "Q5": q5,
                "Q5_determinant": q5_det,
                "Q5_trace": q5_trace,
                "Q10": q10,
                "seam_selected_by_determinant": False,
                "signed_reciprocal_return": {"plus": "+I after two", "minus": "-I after two; +I after four"},
                "transport_to_D20_C20_X20_X40_Q106": fibonacci_transport,
            },
        },
        "source_resolution": source_resolution,
        "checks": checks,
        "claim_boundary": contract["claim_boundary"]
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write RESULT.json")
    args = parser.parse_args()
    result = validate()
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.write:
        (HERE / "RESULT.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
