#!/usr/bin/env python3
"""Audit intrinsic Z2 holonomy on the frozen SCC-003 Pascal carrier.

This is deterministic formal-fixture validation, not an admitted Lab run.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict, deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
DESIGN = HERE.parent
ARTIFACTS = DESIGN.parent / "SCC_003_REFERENCE" / "artifacts"
D30_RESULT = DESIGN / "D30_BRANCH_WORD_AUDIT_2026-10-11" / "RESULT.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parity(value: int) -> int:
    return bin(value).count("1") % 2


def gf2_rank(vectors: list[int]) -> int:
    pivots: dict[int, int] = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in pivots:
                vector ^= pivots[pivot]
            else:
                pivots[pivot] = vector
                break
    return len(pivots)


def solve_gf2(rows: list[tuple[int, int]], variable_count: int) -> tuple[bool, int, int]:
    """Return consistency, one free-zero solution, and matrix rank."""
    pivots: dict[int, tuple[int, int]] = {}
    for bits, rhs in rows:
        while bits:
            pivot = bits.bit_length() - 1
            if pivot in pivots:
                bits ^= pivots[pivot][0]
                rhs ^= pivots[pivot][1]
            else:
                pivots[pivot] = (bits, rhs)
                break
        else:
            if rhs:
                return False, 0, len(pivots)

    solution = 0
    for pivot in sorted(pivots):
        bits, rhs = pivots[pivot]
        if parity(bits & solution) != rhs:
            solution |= 1 << pivot
    assert all(parity(bits & solution) == rhs for bits, rhs in rows)
    return True, solution, len(pivots)


def load_fixture():
    with (ARTIFACTS / "nodes.csv").open(newline="", encoding="utf-8") as handle:
        nodes = list(csv.DictReader(handle))
    with (ARTIFACTS / "edges.csv").open(newline="", encoding="utf-8") as handle:
        edge_rows = list(csv.DictReader(handle))
    with (ARTIFACTS / "face_incidence.csv").open(newline="", encoding="utf-8") as handle:
        incidence_rows = list(csv.DictReader(handle))
    automorphisms = json.loads((ARTIFACTS / "automorphisms.json").read_text(encoding="utf-8"))["actions"]

    edges = [
        tuple(sorted((int(row["source_index"]), int(row["target_index"]))))
        for row in edge_rows
    ]
    edge_index = {edge: index for index, edge in enumerate(edges)}
    raw_to_quotient = {
        (int(row["face"]), int(row["n"]), int(row["k"])): int(row["quotient_index"])
        for row in incidence_rows
    }
    return nodes, edges, edge_index, raw_to_quotient, automorphisms


def build_diamonds(raw_to_quotient, edge_index):
    diamonds = []
    for face in range(5):
        for depth in range(5):
            for branch_index in range(depth + 1):
                a = raw_to_quotient[(face, depth, branch_index)]
                b = raw_to_quotient[(face, depth + 1, branch_index)]
                c = raw_to_quotient[(face, depth + 1, branch_index + 1)]
                d = raw_to_quotient[(face, depth + 2, branch_index + 1)]
                vector = 0
                boundary_edges = [(a, b), (b, d), (a, c), (c, d)]
                for edge in boundary_edges:
                    vector ^= 1 << edge_index[tuple(sorted(edge))]
                diamonds.append({
                    "index": (face, depth, branch_index),
                    "vector": vector,
                    "vertices": (a, b, d, c),
                })
    return diamonds


def connected_components(vertex_count: int, edges: list[tuple[int, int]]) -> int:
    adjacency = defaultdict(set)
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(range(vertex_count))
    components = 0
    while unseen:
        components += 1
        queue = deque([unseen.pop()])
        while queue:
            node = queue.popleft()
            for neighbour in adjacency[node]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    queue.append(neighbour)
    return components


def vertex_coboundaries(vertex_count: int, edges: list[tuple[int, int]]) -> list[int]:
    vectors = []
    for vertex in range(vertex_count):
        vector = 0
        for edge_index, edge in enumerate(edges):
            if vertex in edge:
                vector ^= 1 << edge_index
        vectors.append(vector)
    return vectors


def edge_permutation(action, edges, edge_index):
    permutation = action["permutation_zero_based"]
    return [
        edge_index[tuple(sorted((permutation[left], permutation[right])))]
        for left, right in edges
    ]


def permute_vector(vector: int, permutation: list[int]) -> int:
    result = 0
    for source, target in enumerate(permutation):
        if (vector >> source) & 1:
            result ^= 1 << target
    return result


def orbit_partition(diamonds, edge_permutations):
    vector_to_index = {item["vector"]: index for index, item in enumerate(diamonds)}
    unseen = set(range(len(diamonds)))
    orbits = []
    while unseen:
        seed = min(unseen)
        orbit = {
            vector_to_index[permute_vector(diamonds[seed]["vector"], permutation)]
            for permutation in edge_permutations
        }
        unseen -= orbit
        orbits.append(sorted(orbit))
    return sorted(orbits, key=lambda orbit: (diamonds[orbit[0]]["index"][1:], len(orbit)))


def invariant_rows(generator_permutations, edge_count):
    rows = []
    for permutation in generator_permutations:
        for source, target in enumerate(permutation):
            if source != target:
                rows.append(((1 << source) ^ (1 << target), 0))
    return rows


def validate() -> dict[str, object]:
    contract_path = HERE / "CONTRACT.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    nodes, edges, edge_index, raw_to_quotient, automorphisms = load_fixture()
    diamonds = build_diamonds(raw_to_quotient, edge_index)
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, observed: object, expected: object) -> None:
        checks.append({
            "name": name,
            "status": "PASS" if passed else "FAIL",
            "observed": observed,
            "expected": expected,
        })

    components = connected_components(len(nodes), edges)
    check(
        "frozen Q106 graph counts and connectivity",
        len(nodes) == 106 and len(edges) == len(set(edges)) == 180 and components == 1,
        {"vertices": len(nodes), "edges": len(edges), "components": components},
        {"vertices": 106, "edges": 180, "components": 1},
    )
    check(
        "identity reused without creation",
        contract["identity"]["reuse"] == "A0OE:PASCAL_PENTAGON_D5_TEST"
        and contract["identity"]["creates"] == [],
        contract["identity"],
        {"reuse": "A0OE:PASCAL_PENTAGON_D5_TEST", "creates": []},
    )

    diamond_vectors = [item["vector"] for item in diamonds]
    diamond_rank = gf2_rank(diamond_vectors)
    check(
        "75 nondegenerate Pascal diamond cells",
        len(diamonds) == 75 and all(parity(item["vector"]) == 0 and bin(item["vector"]).count("1") == 4 for item in diamonds),
        {"diamonds": len(diamonds), "edge_counts": dict(Counter(bin(item["vector"]).count("1") for item in diamonds))},
        {"diamonds": 75, "edge_counts": {4: 75}},
    )

    cycle_rank = len(edges) - len(nodes) + components
    check("graph-only cycle rank", cycle_rank == 75, cycle_rank, 75)
    check("diamond boundaries are independent", diamond_rank == 75, diamond_rank, 75)
    check(
        "diamond boundaries span the complete graph cycle space",
        diamond_rank == cycle_rank,
        {"diamond_rank": diamond_rank, "cycle_rank": cycle_rank},
        {"diamond_rank": 75, "cycle_rank": 75},
    )

    coboundaries = vertex_coboundaries(len(nodes), edges)
    coboundary_rank = gf2_rank(coboundaries)
    closed_dimension = len(edges) - diamond_rank
    h1_dimension = closed_dimension - coboundary_rank
    check("vertex coboundary rank", coboundary_rank == 105, coboundary_rank, 105)
    check(
        "intrinsic Z2 cohomology is trivial",
        closed_dimension == 105 and h1_dimension == 0,
        {"closed_edge_labelings_dimension": closed_dimension, "H1_dimension": h1_dimension},
        {"closed_edge_labelings_dimension": 105, "H1_dimension": 0},
    )

    edge_permutations = [edge_permutation(action, edges, edge_index) for action in automorphisms]
    diamond_set = set(diamond_vectors)
    graph_actions_valid = all(sorted(permutation) == list(range(len(edges))) for permutation in edge_permutations)
    cells_preserved = all(
        permute_vector(vector, permutation) in diamond_set
        for vector in diamond_vectors
        for permutation in edge_permutations
    )
    check(
        "all ten D5 actions preserve graph and diamond cells",
        len(edge_permutations) == 10 and graph_actions_valid and cells_preserved,
        {"actions": len(edge_permutations), "graph": graph_actions_valid, "diamonds": cells_preserved},
        {"actions": 10, "graph": True, "diamonds": True},
    )

    orbits = orbit_partition(diamonds, edge_permutations)
    orbit_profile = dict(sorted(Counter(len(orbit) for orbit in orbits).items()))
    check(
        "diamond D5 orbit profile",
        len(orbits) == 9 and orbit_profile == {5: 3, 10: 6},
        {"orbits": len(orbits), "profile": orbit_profile},
        {"orbits": 9, "profile": {5: 3, 10: 6}},
    )

    single_cut_h1 = []
    for removed in range(len(diamonds)):
        retained_rank = gf2_rank([
            item["vector"] for index, item in enumerate(diamonds) if index != removed
        ])
        single_cut_h1.append(len(edges) - retained_rank - coboundary_rank)
    check(
        "every single unsymmetrized diamond cut creates one holonomy degree",
        set(single_cut_h1) == {1},
        dict(Counter(single_cut_h1)),
        {1: 75},
    )

    rotation = next(action for action in automorphisms if action["name"] == "r^1")
    reflection = next(
        action for action in automorphisms
        if action["reflected"] and action["turns"] == 0
    )
    generator_permutations = [
        edge_permutation(rotation, edges, edge_index),
        edge_permutation(reflection, edges, edge_index),
    ]
    invariance = invariant_rows(generator_permutations, len(edges))

    orbit_results = []
    for orbit_number, orbit in enumerate(orbits, start=1):
        removed = set(orbit)
        equations = list(invariance)
        equations.extend(
            (item["vector"], 0)
            for index, item in enumerate(diamonds)
            if index not in removed
        )
        equations.append((diamonds[orbit[0]]["vector"], 1))
        compatible, witness, matrix_rank = solve_gf2(equations, len(edges))
        removed_parities = [parity(witness & diamonds[index]["vector"]) for index in orbit] if compatible else []
        retained_failures = sum(
            parity(witness & item["vector"])
            for index, item in enumerate(diamonds)
            if index not in removed
        ) if compatible else None
        invariant_failures = sum(
            parity(bits & witness) != rhs for bits, rhs in invariance
        ) if compatible else None
        orbit_results.append({
            "orbit": orbit_number,
            "size": len(orbit),
            "representative": list(diamonds[orbit[0]]["index"]),
            "members": [list(diamonds[index]["index"]) for index in orbit],
            "compatible_odd_invariant_seam": compatible,
            "matrix_rank": matrix_rank,
            "witness_weight": bin(witness).count("1") if compatible else None,
            "witness_edge_indices": [index for index in range(len(edges)) if (witness >> index) & 1] if compatible else [],
            "removed_cell_parities": removed_parities,
            "retained_cell_failures": retained_failures,
            "invariance_failures": invariant_failures,
        })

    compatible_orbits = [item for item in orbit_results if item["compatible_odd_invariant_seam"]]
    incompatible_orbits = [item for item in orbit_results if not item["compatible_odd_invariant_seam"]]
    check(
        "centered size-five orbits reject odd invariant seam",
        len(incompatible_orbits) == 3 and {item["size"] for item in incompatible_orbits} == {5},
        {"count": len(incompatible_orbits), "sizes": [item["size"] for item in incompatible_orbits]},
        {"count": 3, "sizes": [5, 5, 5]},
    )
    check(
        "six off-center size-ten orbits admit an invariant added seam",
        len(compatible_orbits) == 6
        and {item["size"] for item in compatible_orbits} == {10}
        and all(item["removed_cell_parities"] == [1] * 10 for item in compatible_orbits)
        and all(item["retained_cell_failures"] == 0 for item in compatible_orbits)
        and all(item["invariance_failures"] == 0 for item in compatible_orbits),
        {"count": len(compatible_orbits), "sizes": [item["size"] for item in compatible_orbits]},
        {"count": 6, "sizes": [10] * 6},
    )
    minimum_d5_seam = min(item["size"] for item in compatible_orbits)
    check("minimal D5-compatible seam orbit has size ten", minimum_d5_seam == 10, minimum_d5_seam, 10)

    d30 = json.loads(D30_RESULT.read_text(encoding="utf-8"))
    observed_phases = d30["summary"]["observed_phases"]
    check(
        "frozen source still supplies only partial D30 phase coverage",
        observed_phases == 13,
        observed_phases,
        13,
    )

    passed = all(item["status"] == "PASS" for item in checks)
    classification = (
        "ONLY_AFTER_ADDED_SEAM_SIX_NONCANONICAL_D5_COMPATIBLE_ORBITS"
        if passed else "INVALID_FIXTURE"
    )
    return {
        "schema": "nexah.pascal-intrinsic-seam-holonomy-audit-result/1.0.0",
        "status": "PASS_WITH_VALIDATED_NEGATIVE_RESULT" if passed else "FAIL",
        "classification": classification,
        "identity_reused": contract["identity"]["reuse"],
        "creates": [],
        "summary": {
            "checks_passed": sum(item["status"] == "PASS" for item in checks),
            "checks_total": len(checks),
            "vertices": len(nodes),
            "edges": len(edges),
            "graph_cycle_rank": cycle_rank,
            "pascal_diamonds": len(diamonds),
            "diamond_boundary_rank": diamond_rank,
            "intrinsic_H1_dimension": h1_dimension,
            "d5_diamond_orbits": len(orbits),
            "compatible_added_seam_orbits": len(compatible_orbits),
            "minimum_d5_compatible_seam_size": minimum_d5_seam,
        },
        "orbit_results": orbit_results,
        "checks": checks,
        "input_hashes": {
            "contract": sha256(contract_path),
            "nodes": sha256(ARTIFACTS / "nodes.csv"),
            "edges": sha256(ARTIFACTS / "edges.csv"),
            "face_incidence": sha256(ARTIFACTS / "face_incidence.csv"),
            "automorphisms": sha256(ARTIFACTS / "automorphisms.json"),
            "d30_result": sha256(D30_RESULT),
        },
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = validate()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        (HERE / "RESULT.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["status"] == "PASS_WITH_VALIDATED_NEGATIVE_RESULT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
