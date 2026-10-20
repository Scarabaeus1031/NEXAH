#!/usr/bin/env python3
"""Exact finite Pascal-carrier / quaternion-orientation boundary test."""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction


MAX_DEPTH = 11


def weight(point: tuple[int, int, int]) -> int:
    i, j, k = point
    n = i + j + k
    return math.factorial(n) // (math.factorial(i) * math.factorial(j) * math.factorial(k))


def carrier(depth: int) -> set[tuple[int, int, int]]:
    return {
        (i, j, n - i - j)
        for n in range(depth + 1)
        for i in range(n + 1)
        for j in range(n - i + 1)
    }


def recurrence_edges(points: set[tuple[int, int, int]], depth: int) -> set[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    steps = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    return {
        (point, tuple(point[index] + step[index] for index in range(3)))
        for point in points
        if sum(point) < depth
        for step in steps
    }


def parity(permutation: tuple[int, int, int]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(3)
        for right in range(left + 1, 3)
    )
    return 1 if inversions % 2 == 0 else -1


def permute(point: tuple[int, int, int], permutation: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(point[index] for index in permutation)


def quaternion(axis: tuple[float, float, float], degrees: float) -> tuple[float, float, float, float]:
    norm = math.sqrt(sum(value * value for value in axis))
    half = math.radians(degrees) / 2
    scale = math.sin(half) / norm
    return (math.cos(half), *(value * scale for value in axis))


def rotate(vector: tuple[float, float, float], q: tuple[float, float, float, float]) -> tuple[float, float, float]:
    w, x, y, z = q
    vx, vy, vz = vector
    tx = 2 * (y * vz - z * vy)
    ty = 2 * (z * vx - x * vz)
    tz = 2 * (x * vy - y * vx)
    return (
        vx + w * tx + y * tz - z * ty,
        vy + w * ty + z * tx - x * tz,
        vz + w * tz + x * ty - y * tx,
    )


def permutation_result(depth: int, permutation: tuple[int, int, int]) -> dict[str, bool | int | list[int]]:
    points = carrier(depth)
    edges = recurrence_edges(points, depth)
    mapped_points = {permute(point, permutation) for point in points}
    mapped_edges = {(permute(a, permutation), permute(b, permutation)) for a, b in edges}
    return {
        "permutation": list(permutation),
        "determinant": parity(permutation),
        "carrier_preserved": mapped_points == points,
        "weights_preserved": all(weight(point) == weight(permute(point, permutation)) for point in points),
        "recurrence_edges_preserved": mapped_edges == edges,
    }


def quaternion_cycle_matches(permutation: tuple[int, int, int], degrees: float) -> bool:
    q = quaternion((1.0, 1.0, 1.0), degrees)
    basis = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    for vector in basis:
        actual = rotate(vector, q)
        expected = permute(tuple(int(value) for value in vector), permutation)
        if any(abs(a - b) > 1e-12 for a, b in zip(actual, expected)):
            return False
    return True


def generic_rotation_is_lattice_automorphism(depth: int) -> bool:
    points = carrier(depth)
    center = Fraction(depth, 4)
    q = quaternion((1.0, 2.0, 3.0), 37.0)
    for point in points:
        shifted = tuple(float(Fraction(value) - center) for value in point)
        rotated = rotate(shifted, q)
        mapped = tuple(value + float(center) for value in rotated)
        rounded = tuple(round(value) for value in mapped)
        if any(abs(value - integer) > 1e-9 for value, integer in zip(mapped, rounded)):
            return False
        if rounded not in points or weight(point) != weight(rounded):
            return False
    return True


def run() -> dict[str, object]:
    permutations = list(itertools.permutations(range(3)))
    by_depth = []
    for depth in range(MAX_DEPTH + 1):
        results = [permutation_result(depth, permutation) for permutation in permutations]
        by_depth.append({
            "depth": depth,
            "node_count": len(carrier(depth)),
            "layer_sum": sum(weight(point) for point in carrier(depth) if sum(point) == depth),
            "expected_layer_sum": 3 ** depth,
            "all_s3_preserve_carrier_weight_and_edges": all(
                item["carrier_preserved"] and item["weights_preserved"] and item["recurrence_edges_preserved"]
                for item in results
            ),
            "proper_rotation_count": sum(item["determinant"] == 1 for item in results),
            "generic_rotation_is_lattice_automorphism": generic_rotation_is_lattice_automorphism(depth) if depth >= 1 else None,
        })

    cycle_120 = (2, 0, 1)
    cycle_240 = (1, 2, 0)
    checks = {
        "all_depths_have_layer_sum_3_pow_n": all(item["layer_sum"] == item["expected_layer_sum"] for item in by_depth),
        "all_s3_coordinate_permutations_preserve_the_weighted_recurrence_carrier": all(item["all_s3_preserve_carrier_weight_and_edges"] for item in by_depth),
        "proper_coordinate_permutation_subgroup_has_order_3": all(item["proper_rotation_count"] == 3 for item in by_depth),
        "q120_matches_first_axis_cycle": quaternion_cycle_matches(cycle_120, 120.0),
        "q240_matches_inverse_axis_cycle": quaternion_cycle_matches(cycle_240, 240.0),
        "generic_q37_fails_integer_lattice_membership_for_all_nontrivial_depths": all(
            item["generic_rotation_is_lattice_automorphism"] is False for item in by_depth[1:]
        ),
    }
    return {
        "schema": "nexah.pascal-quaternion-carrier-test/1.0.0",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "classification": "BOUNDED_CANDIDATE_EVIDENCE_NOT_ADMITTED",
        "depths_tested": [0, MAX_DEPTH],
        "result": {
            "full_coordinate_permutation_group": "S3",
            "full_group_order": 6,
            "quaternion_realizable_proper_subgroup": "C3",
            "proper_subgroup_order": 3,
            "generic_quaternion_rotation_is_discrete_lattice_automorphism": False,
            "quaternion_generation_of_pascal_recurrence": "NOT_ESTABLISHED",
        },
        "checks": checks,
        "depth_records": by_depth,
        "claim_ceiling": "Exact finite carrier automorphism fixture only; no quaternion generation of Pascal coefficients, algebra identity, or physical mechanism is established.",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)

