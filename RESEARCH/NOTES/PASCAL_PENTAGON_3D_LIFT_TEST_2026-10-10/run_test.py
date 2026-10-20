#!/usr/bin/env python3
"""PENT-04: depth-six Pascal lattices on a pentagonal bipyramid."""

from __future__ import annotations

import json
import math
from collections import defaultdict, deque


DEPTH = 6
FACES_PER_HEMISPHERE = 5
TOL = 1e-10


RawNode = tuple[int, int, int, int]
CanonicalNode = tuple[tuple[str, int], ...]


def choose(n: int, k: int) -> int:
    return math.comb(n, k)


def face_vertices(hemisphere: int, face: int) -> tuple[str, str, str]:
    if hemisphere == 1:
        return ("Z", f"V{face}", f"V{(face + 1) % 5}")
    return ("N", f"V{(face + 1) % 5}", f"V{face}")


def raw_nodes() -> set[RawNode]:
    return {
        (hemisphere, face, n, k)
        for hemisphere in (-1, 1)
        for face in range(FACES_PER_HEMISPHERE)
        for n in range(DEPTH + 1)
        for k in range(n + 1)
    }


def raw_edges() -> set[tuple[RawNode, RawNode]]:
    result = set()
    for hemisphere in (-1, 1):
        for face in range(FACES_PER_HEMISPHERE):
            for n in range(DEPTH):
                for k in range(n + 1):
                    parent = (hemisphere, face, n, k)
                    result.add((parent, (hemisphere, face, n + 1, k)))
                    result.add((parent, (hemisphere, face, n + 1, k + 1)))
    return result


def canonical(node: RawNode) -> CanonicalNode:
    hemisphere, face, n, k = node
    apex, left, right = face_vertices(hemisphere, face)
    weights = {apex: DEPTH - n, left: n - k, right: k}
    return tuple(sorted((name, value) for name, value in weights.items() if value))


def node_weight(node: RawNode) -> int:
    return choose(node[2], node[3])


def vertex_coordinates() -> dict[str, tuple[float, float, float]]:
    result = {"Z": (0.0, 0.0, 1.0), "N": (0.0, 0.0, -1.0)}
    for index in range(5):
        angle = -math.pi / 2 + index * 2 * math.pi / 5
        result[f"V{index}"] = (math.cos(angle), math.sin(angle), 0.0)
    return result


COORDINATES = vertex_coordinates()


def position(qnode: CanonicalNode) -> tuple[float, float, float]:
    x = y = z = 0.0
    for name, weight in qnode:
        vx, vy, vz = COORDINATES[name]
        x += weight * vx / DEPTH
        y += weight * vy / DEPTH
        z += weight * vz / DEPTH
    return (x, y, z)


def transform_vertex(name: str, turns: int, mirrored: bool, swapped: bool) -> str:
    if name in {"Z", "N"}:
        if swapped:
            return "N" if name == "Z" else "Z"
        return name
    index = int(name[1:])
    index = (index + turns) % 5
    if mirrored:
        index = (1 - index) % 5
    return f"V{index}"


def action(qnode: CanonicalNode, turns: int = 0, mirrored: bool = False, swapped: bool = False) -> CanonicalNode:
    return tuple(sorted((transform_vertex(name, turns, mirrored, swapped), weight) for name, weight in qnode))


def rotate_point(point: tuple[float, float, float], turns: int) -> tuple[float, float, float]:
    angle = turns * 2 * math.pi / 5
    c, s = math.cos(angle), math.sin(angle)
    x, y, z = point
    return (c * x - s * y, s * x + c * y, z)


def mirror_point(point: tuple[float, float, float]) -> tuple[float, float, float]:
    axis = -math.pi / 2 + math.pi / 5
    x, y, z = point
    return (
        math.cos(2 * axis) * x + math.sin(2 * axis) * y,
        math.sin(2 * axis) * x - math.cos(2 * axis) * y,
        z,
    )


def swap_point(point: tuple[float, float, float]) -> tuple[float, float, float]:
    return (point[0], point[1], -point[2])


def transformed_point(point: tuple[float, float, float], turns: int, mirrored: bool, swapped: bool) -> tuple[float, float, float]:
    result = rotate_point(point, turns)
    if mirrored:
        result = mirror_point(result)
    if swapped:
        result = swap_point(result)
    return result


def close_points(a: tuple[float, float, float], b: tuple[float, float, float]) -> bool:
    return all(abs(x - y) <= TOL for x, y in zip(a, b))


def component_count(nodes: set[CanonicalNode], edges: set[tuple[CanonicalNode, CanonicalNode]]) -> int:
    adjacency: dict[CanonicalNode, set[CanonicalNode]] = defaultdict(set)
    for parent, child in edges:
        adjacency[parent].add(child)
        adjacency[child].add(parent)
    unseen = set(nodes)
    count = 0
    while unseen:
        count += 1
        queue = deque([unseen.pop()])
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    queue.append(neighbor)
    return count


def signature(nodes: list[CanonicalNode], turns: int, mirrored: bool, swapped: bool) -> tuple[int, ...]:
    index = {node: position for position, node in enumerate(nodes)}
    return tuple(index[action(node, turns, mirrored, swapped)] for node in nodes)


def projected_hemisphere_nodes(hemisphere: int) -> set[tuple[int, int]]:
    projected = set()
    for node in raw_nodes():
        if node[0] != hemisphere:
            continue
        x, y, _ = position(canonical(node))
        projected.add((round(x / TOL), round(y / TOL)))
    return projected


def run() -> dict[str, object]:
    raw = raw_nodes()
    qnodes = {canonical(node) for node in raw}
    qedges = {(canonical(parent), canonical(child)) for parent, child in raw_edges()}
    ordered = sorted(qnodes, key=repr)

    representatives: dict[CanonicalNode, list[RawNode]] = defaultdict(list)
    for node in raw:
        representatives[canonical(node)].append(node)
    seam_weights_compatible = all(len({node_weight(node) for node in reps}) == 1 for reps in representatives.values())
    qweights = {qnode: node_weight(reps[0]) for qnode, reps in representatives.items()}

    actions = [(turns, mirrored, swapped) for turns in range(5) for mirrored in (False, True) for swapped in (False, True)]
    signatures = {signature(ordered, *group_action) for group_action in actions}

    preserves = []
    equivariant = []
    for group_action in actions:
        mapped_nodes = {action(node, *group_action) for node in qnodes}
        mapped_edges = {(action(parent, *group_action), action(child, *group_action)) for parent, child in qedges}
        preserves.append(
            mapped_nodes == qnodes
            and mapped_edges == qedges
            and all(qweights[node] == qweights[action(node, *group_action)] for node in qnodes)
        )
        equivariant.append(all(close_points(position(action(node, *group_action)), transformed_point(position(node), *group_action)) for node in qnodes))

    identity = lambda node: node
    r5 = all(action(node, 5, False, False) == identity(node) for node in qnodes)
    m2 = all(action(action(node, 0, True, False), 0, True, False) == node for node in qnodes)
    h2 = all(action(action(node, 0, False, True), 0, False, True) == node for node in qnodes)
    mrm = all(action(action(action(node, 0, True, False), 1, False, False), 0, True, False) == action(node, -1, False, False) for node in qnodes)
    hr = all(action(action(node, 1, False, False), 0, False, True) == action(action(node, 0, False, True), 1, False, False) for node in qnodes)
    hm = all(action(action(node, 0, True, False), 0, False, True) == action(action(node, 0, False, True), 0, True, False) for node in qnodes)

    orientation_preserving = {
        signature(ordered, turns, reflected, reflected)
        for turns in range(5)
        for reflected in (False, True)
    }

    top_projection = projected_hemisphere_nodes(1)
    bottom_projection = projected_hemisphere_nodes(-1)
    equatorial_midpoints = {
        tuple(sorted(((f"V{face}", 3), (f"V{(face + 1) % 5}", 3))))
        for face in range(5)
    }

    vertex_names = set(COORDINATES)
    carrier_edges = set()
    carrier_faces = set()
    for hemisphere in (-1, 1):
        for face in range(5):
            face_set = frozenset(face_vertices(hemisphere, face))
            carrier_faces.add(face_set)
            members = list(face_set)
            for i in range(3):
                carrier_edges.add(frozenset((members[i], members[(i + 1) % 3])))

    checks = {
        "carrier_has_7_vertices_15_edges_10_faces": len(vertex_names) == 7 and len(carrier_edges) == 15 and len(carrier_faces) == 10,
        "carrier_euler_characteristic_is_2": len(vertex_names) - len(carrier_edges) + len(carrier_faces) == 2,
        "ten_raw_faces_have_280_nodes": len(raw) == 280,
        "glued_bipyramid_has_182_unique_nodes": len(qnodes) == 182,
        "glued_bipyramid_is_connected": component_count(qnodes, qedges) == 1,
        "all_radial_and_equatorial_seam_weights_are_compatible": seam_weights_compatible,
        "twenty_full_actions_are_distinct": len(signatures) == 20,
        "all_full_actions_preserve_weights_and_recurrence": all(preserves),
        "all_full_actions_are_euclidean_isometries_on_embedded_nodes": all(equivariant),
        "group_relations_hold": r5 and m2 and h2 and mrm and hr and hm,
        "orientation_preserving_subgroup_has_order_10": len(orientation_preserving) == 10,
        "both_hemispheres_project_to_same_106_node_carrier": top_projection == bottom_projection and len(top_projection) == 106,
        "five_shared_equatorial_midpoints_retain_weight_20": len(equatorial_midpoints) == 5 and equatorial_midpoints.issubset(qnodes) and all(qweights[node] == 20 for node in equatorial_midpoints),
    }

    return {
        "schema": "nexah.pascal-pentagon-3d-lift-test/1.0.0",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "classification": "BOUNDED_CANDIDATE_EVIDENCE_NOT_ADMITTED",
        "parameters": {"depth": DEPTH, "layers_per_hemisphere": DEPTH + 1, "equatorial_vertices": 5, "height": 1.0, "tolerance": TOL},
        "result": {
            "working_object": "depth-six Pascal lattice on a regular pentagonal bipyramid",
            "carrier_vertices": len(vertex_names),
            "carrier_edges": len(carrier_edges),
            "carrier_faces": len(carrier_faces),
            "euler_characteristic": len(vertex_names) - len(carrier_edges) + len(carrier_faces),
            "raw_face_local_node_count": len(raw),
            "quotient_node_count": len(qnodes),
            "quotient_edge_count": len(qedges),
            "component_count": component_count(qnodes, qedges),
            "full_symmetry_fixture": "D5 x C2",
            "full_action_count": len(signatures),
            "orientation_preserving_subgroup": "D5",
            "orientation_preserving_action_count": len(orientation_preserving),
            "projected_node_count_per_hemisphere": len(top_projection),
            "shared_equatorial_weight_20_orbit_size": len(equatorial_midpoints),
            "four_inner_layers_interpretation": "UNDEFINED_IN_CURRENT_CONTRACT",
        },
        "checks": checks,
        "claim_ceiling": "One finite declared combinatorial and Euclidean 3D lift only; no prime-label, resonance, physical, historical, universal-solid or four-inner-layer claim is established.",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)

