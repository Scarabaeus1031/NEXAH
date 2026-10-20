#!/usr/bin/env python3
"""PENT-02: regular-pentagon metric realization of the glued Pascal fan."""

from __future__ import annotations

import json
import math


DEPTH = 6
FACES = 5
TOL = 1e-10
PHI = (1 + math.sqrt(5)) / 2


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol


def pclose(a: tuple[float, float], b: tuple[float, float], tol: float = TOL) -> bool:
    return close(a[0], b[0], tol) and close(a[1], b[1], tol)


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def vertices() -> list[tuple[float, float]]:
    return [
        (math.cos(-math.pi / 2 + 2 * math.pi * face / FACES),
         math.sin(-math.pi / 2 + 2 * math.pi * face / FACES))
        for face in range(FACES)
    ]


VERTICES = vertices()


def nodes() -> set[tuple[int, int, int]]:
    return {(face, n, k) for face in range(FACES) for n in range(DEPTH + 1) for k in range(n + 1)}


def canonical(node: tuple[int, int, int]) -> tuple[object, ...]:
    face, n, k = node
    if n == 0:
        return ("apex",)
    if k == 0:
        return ("seam", n, (face - 1) % FACES)
    if k == n:
        return ("seam", n, face)
    return ("interior", face, n, k)


def position(node: tuple[int, int, int]) -> tuple[float, float]:
    face, n, k = node
    if n == 0:
        return (0.0, 0.0)
    t = n / DEPTH
    q = k / n
    a = VERTICES[face]
    b = VERTICES[(face + 1) % FACES]
    return (t * ((1 - q) * a[0] + q * b[0]), t * ((1 - q) * a[1] + q * b[1]))


def rotate_node(node: tuple[int, int, int], turns: int = 1) -> tuple[int, int, int]:
    face, n, k = node
    return ((face + turns) % FACES, n, k)


def mirror_node(node: tuple[int, int, int]) -> tuple[int, int, int]:
    face, n, k = node
    return ((-face) % FACES, n, n - k)


def rotate_point(point: tuple[float, float], turns: int = 1) -> tuple[float, float]:
    angle = turns * 2 * math.pi / FACES
    c, s = math.cos(angle), math.sin(angle)
    x, y = point
    return (c * x - s * y, s * x + c * y)


def mirror_point(point: tuple[float, float]) -> tuple[float, float]:
    # Reflection sending vertex j to vertex 1-j.
    axis = -math.pi / 2 + math.pi / FACES
    x, y = point
    return (math.cos(2 * axis) * x + math.sin(2 * axis) * y,
            math.sin(2 * axis) * x - math.cos(2 * axis) * y)


def line_intersection_parameter(
    a: tuple[float, float], b: tuple[float, float],
    c: tuple[float, float], d: tuple[float, float],
) -> float:
    rx, ry = b[0] - a[0], b[1] - a[1]
    sx, sy = d[0] - c[0], d[1] - c[1]
    denominator = rx * sy - ry * sx
    qpx, qpy = c[0] - a[0], c[1] - a[1]
    return (qpx * sy - qpy * sx) / denominator


def run() -> dict[str, object]:
    raw = nodes()
    quotient = {canonical(node) for node in raw}

    representatives: dict[tuple[object, ...], tuple[int, int, int]] = {}
    well_defined = True
    for node in raw:
        qnode = canonical(node)
        if qnode in representatives:
            well_defined = well_defined and pclose(position(node), position(representatives[qnode]))
        else:
            representatives[qnode] = node

    coordinate_groups: dict[tuple[int, int], set[tuple[object, ...]]] = {}
    for qnode, node in representatives.items():
        p = position(node)
        key = (round(p[0] / TOL), round(p[1] / TOL))
        coordinate_groups.setdefault(key, set()).add(qnode)
    injective = all(len(group) == 1 for group in coordinate_groups.values())

    rotation_equivariant = all(
        pclose(position(rotate_node(node)), rotate_point(position(node)))
        for node in raw
    )
    reflection_equivariant = all(
        pclose(position(mirror_node(node)), mirror_point(position(node)))
        for node in raw
    )

    vertex_distance_preserved = True
    for turns in range(FACES):
        transformed = [rotate_point(vertex, turns) for vertex in VERTICES]
        for i in range(FACES):
            for j in range(FACES):
                vertex_distance_preserved &= close(distance(VERTICES[i], VERTICES[j]), distance(transformed[i], transformed[j]))
    reflected = [mirror_point(vertex) for vertex in VERTICES]
    for i in range(FACES):
        for j in range(FACES):
            vertex_distance_preserved &= close(distance(VERTICES[i], VERTICES[j]), distance(reflected[i], reflected[j]))

    side = distance(VERTICES[0], VERTICES[1])
    diagonal = distance(VERTICES[0], VERTICES[2])
    diagonal_side_ratio = diagonal / side

    # Intersect diagonals V0--V2 and V1--V4. The intersection divides the
    # first diagonal into long and short parts with ratio phi.
    parameter = line_intersection_parameter(VERTICES[0], VERTICES[2], VERTICES[1], VERTICES[4])
    segment_a = diagonal * parameter
    segment_b = diagonal * (1 - parameter)
    golden_section_ratio = max(segment_a, segment_b) / min(segment_a, segment_b)

    nadirs = [position((face, DEPTH, DEPTH // 2)) for face in range(FACES)]
    nadir_rotation_orbit = all(pclose(rotate_point(nadirs[0], turns), nadirs[turns]) for turns in range(FACES))

    checks = {
        "quotient_embedding_is_well_defined": well_defined,
        "quotient_embedding_is_injective_for_106_nodes": injective and len(quotient) == 106,
        "rotation_is_equivariant_with_r": rotation_equivariant,
        "reflection_is_equivariant_with_m": reflection_equivariant,
        "d5_preserves_regular_pentagon_vertex_distances": vertex_distance_preserved,
        "diagonal_over_side_equals_phi": close(diagonal_side_ratio, PHI),
        "pentagram_intersection_is_golden_section": close(golden_section_ratio, PHI),
        "five_weight_20_base_centres_form_metric_c5_orbit": nadir_rotation_orbit,
    }

    return {
        "schema": "nexah.pascal-pentagon-metric-test/1.0.0",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "classification": "BOUNDED_CANDIDATE_EVIDENCE_NOT_ADMITTED",
        "parameters": {"faces": FACES, "depth": DEPTH, "layers": DEPTH + 1, "circumradius": 1.0, "tolerance": TOL},
        "result": {
            "working_object": "regular-pentagon realization of the five-face glued Pascal fan",
            "quotient_node_count": len(quotient),
            "side_length": side,
            "diagonal_length": diagonal,
            "diagonal_side_ratio": diagonal_side_ratio,
            "golden_section_ratio": golden_section_ratio,
            "phi": PHI,
            "metric_symmetry": "D5",
            "rotation_subgroup": "C5",
            "three_dimensional_lift": "NOT_DEFINED",
        },
        "checks": checks,
        "claim_ceiling": "Exact Euclidean realization of one finite declared carrier only; no prime-label, resonance, physical, generative or 3D-pyramid claim is established.",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)

