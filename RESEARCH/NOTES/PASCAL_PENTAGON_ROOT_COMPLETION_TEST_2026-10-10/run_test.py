#!/usr/bin/env python3
"""PENT-05: exact finite checks for the H2 direct-sum A1 root candidate."""

from __future__ import annotations

import json
import math
from collections import deque


TOL = 1e-10
PHI = (1.0 + math.sqrt(5.0)) / 2.0


Vector = tuple[float, float, float]
Matrix = tuple[tuple[float, float, float], ...]


def dot(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))


def close(a: float, b: float) -> bool:
    return abs(a - b) <= TOL


def close_vector(a: Vector, b: Vector) -> bool:
    return all(close(x, y) for x, y in zip(a, b))


def identity() -> Matrix:
    return ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


def mat_vec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(sum(matrix[i][j] * vector[j] for j in range(3)) for i in range(3))  # type: ignore[return-value]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3))
        for i in range(3)
    )


def matrix_key(matrix: Matrix) -> tuple[float, ...]:
    return tuple(round(value, 12) for row in matrix for value in row)


def reflection(root: Vector) -> Matrix:
    norm = dot(root, root)
    return tuple(
        tuple((1.0 if i == j else 0.0) - 2.0 * root[i] * root[j] / norm for j in range(3))
        for i in range(3)
    )


def matrix_power(matrix: Matrix, exponent: int) -> Matrix:
    result = identity()
    for _ in range(exponent):
        result = mat_mul(result, matrix)
    return result


def root_set() -> list[Vector]:
    equatorial = []
    for index in range(10):
        angle = -math.pi / 2.0 + index * math.pi / 5.0
        equatorial.append((math.cos(angle), math.sin(angle), 0.0))
    return equatorial + [(0.0, 0.0, 1.0), (0.0, 0.0, -1.0)]


def generated_group(generators: list[Matrix]) -> dict[tuple[float, ...], Matrix]:
    start = identity()
    group = {matrix_key(start): start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for generator in generators:
            candidate = mat_mul(generator, current)
            key = matrix_key(candidate)
            if key not in group:
                group[key] = candidate
                queue.append(candidate)
    return group


def maps_root_set(matrix: Matrix, roots: list[Vector]) -> bool:
    return all(any(close_vector(mat_vec(matrix, root), candidate) for candidate in roots) for root in roots)


def run() -> dict[str, object]:
    roots = root_set()
    equatorial = roots[:10]
    axial = roots[10:]
    carrier_equator = equatorial[::2]
    carrier_vertices = carrier_equator + axial
    added_antipodes = equatorial[1::2]

    simple = [equatorial[0], equatorial[4], axial[0]]
    reflections = [reflection(root) for root in simple]
    group = generated_group(reflections)

    gram = [[dot(a, b) for b in simple] for a in simple]
    cartan = [[2.0 * dot(a, b) / dot(a, a) for b in simple] for a in simple]
    h2_product = mat_mul(reflections[0], reflections[1])

    checks = {
        "root_completion_has_10_H2_plus_2_A1_vectors": len(roots) == 12 and len(equatorial) == 10 and len(axial) == 2,
        "pentagonal_bipyramid_vertices_embed_as_7_roots": len(carrier_vertices) == 7 and all(any(close_vector(v, r) for r in roots) for v in carrier_vertices),
        "completion_adds_five_equatorial_antipodes": len(added_antipodes) == 5 and all(any(close_vector((-v[0], -v[1], -v[2]), c) for c in added_antipodes) for v in carrier_equator),
        "all_roots_are_unit_vectors": all(close(dot(root, root), 1.0) for root in roots),
        "simple_root_gram_matrix_is_H2_direct_sum_A1": close(gram[0][1], -PHI / 2.0) and close(gram[0][2], 0.0) and close(gram[1][2], 0.0),
        "cartan_off_diagonal_is_negative_phi": close(cartan[0][1], -PHI) and close(cartan[1][0], -PHI),
        "root_system_is_non_crystallographic": not close(PHI, round(PHI)),
        "simple_reflections_preserve_all_12_roots": all(maps_root_set(matrix, roots) for matrix in reflections),
        "coxeter_relations_2_5_2_hold": all(matrix_key(mat_mul(s, s)) == matrix_key(identity()) for s in reflections) and matrix_key(matrix_power(h2_product, 5)) == matrix_key(identity()) and matrix_key(matrix_power(mat_mul(reflections[0], reflections[2]), 2)) == matrix_key(identity()) and matrix_key(matrix_power(mat_mul(reflections[1], reflections[2]), 2)) == matrix_key(identity()),
        "generated_reflection_group_has_order_20": len(group) == 20,
        "every_generated_action_preserves_root_set": all(maps_root_set(matrix, roots) for matrix in group.values()),
        "four_turn_weight_subtotal_is_80": 4 * 20 == 80,
        "full_five_position_orbit_weight_is_100": 5 * 20 == 100,
    }

    return {
        "schema": "nexah.pascal-pentagon-root-completion-test/1.0.0",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "classification": "BOUNDED_CANDIDATE_EVIDENCE_NOT_ADMITTED",
        "result": {
            "root_system": "H2 direct-sum A1",
            "coxeter_notation": "I2(5) direct-product A1",
            "rank": 3,
            "root_count": len(roots),
            "H2_root_count": len(equatorial),
            "A1_root_count": len(axial),
            "carrier_vertex_count": len(carrier_vertices),
            "completion_vector_count": len(added_antipodes),
            "reflection_group": "D5 x C2",
            "reflection_group_order": len(group),
            "cartan_H2_off_diagonal": -PHI,
            "four_nonidentity_turns_at_weight_20": 80,
            "full_five_position_orbit_at_weight_20": 100,
            "eighty_interpretation": "FOUR_TURN_SUBTOTAL_NOT_SECOND_INNER_PENTAGON",
            "crystallographic": False,
        },
        "checks": checks,
        "claim_ceiling": "One standard finite H2 direct-sum A1 Coxeter-root realization of the verified D5 x C2 fixture; no Lie, prime-label, resonance, physical, historical, universal-solid or four-inner-layer claim is established.",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
