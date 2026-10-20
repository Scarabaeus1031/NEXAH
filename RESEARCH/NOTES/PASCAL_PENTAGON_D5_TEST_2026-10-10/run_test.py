#!/usr/bin/env python3
"""Finite five-face Pascal fan and D5 action test."""

from __future__ import annotations

import json
import math
from collections import defaultdict, deque


DEPTH = 6
FACES = 5


def choose(n: int, k: int) -> int:
    return math.comb(n, k)


def nodes() -> set[tuple[int, int, int]]:
    return {(face, n, k) for face in range(FACES) for n in range(DEPTH + 1) for k in range(n + 1)}


def edges() -> set[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    result = set()
    for face in range(FACES):
        for n in range(DEPTH):
            for k in range(n + 1):
                parent = (face, n, k)
                result.add((parent, (face, n + 1, k)))
                result.add((parent, (face, n + 1, k + 1)))
    return result


def canonical(node: tuple[int, int, int]) -> tuple[object, ...]:
    face, n, k = node
    if n == 0:
        return ("apex",)
    if k == 0:
        return ("seam", n, (face - 1) % FACES)
    if k == n:
        return ("seam", n, face)
    return ("interior", face, n, k)


def rotate(node: tuple[int, int, int], turns: int = 1) -> tuple[int, int, int]:
    face, n, k = node
    return ((face + turns) % FACES, n, k)


def mirror(node: tuple[int, int, int]) -> tuple[int, int, int]:
    face, n, k = node
    return ((-face) % FACES, n, n - k)


def action(node: tuple[int, int, int], turns: int, reflected: bool) -> tuple[int, int, int]:
    moved = rotate(node, turns)
    return mirror(moved) if reflected else moved


def quotient_nodes() -> set[tuple[object, ...]]:
    return {canonical(node) for node in nodes()}


def quotient_edges() -> set[tuple[tuple[object, ...], tuple[object, ...]]]:
    return {(canonical(parent), canonical(child)) for parent, child in edges()}


def quotient_action(qnode: tuple[object, ...], turns: int, reflected: bool) -> tuple[object, ...]:
    if qnode == ("apex",):
        return qnode
    kind = qnode[0]
    if kind == "seam":
        _, n, seam = qnode
        seam = (int(seam) + turns) % FACES
        if reflected:
            seam = (-seam - 1) % FACES
        return ("seam", n, seam)
    _, face, n, k = qnode
    representative = (int(face), int(n), int(k))
    return canonical(action(representative, turns, reflected))


def qweight(qnode: tuple[object, ...]) -> int:
    if qnode == ("apex",):
        return 1
    if qnode[0] == "seam":
        return 1
    _, _, n, k = qnode
    return choose(int(n), int(k))


def component_count(qnodes: set[tuple[object, ...]], qedges: set[tuple[tuple[object, ...], tuple[object, ...]]]) -> int:
    adjacency: dict[tuple[object, ...], set[tuple[object, ...]]] = defaultdict(set)
    for parent, child in qedges:
        adjacency[parent].add(child)
        adjacency[child].add(parent)
    unseen = set(qnodes)
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


def permutation_signature(turns: int, reflected: bool, qnodes: list[tuple[object, ...]]) -> tuple[int, ...]:
    index = {node: position for position, node in enumerate(qnodes)}
    return tuple(index[quotient_action(node, turns, reflected)] for node in qnodes)


def run() -> dict[str, object]:
    raw_nodes = nodes()
    qnodes = quotient_nodes()
    qedges = quotient_edges()
    qnode_list = sorted(qnodes, key=repr)

    actions = [(turns, reflected) for reflected in (False, True) for turns in range(FACES)]
    signatures = {permutation_signature(turns, reflected, qnode_list) for turns, reflected in actions}

    preserves = []
    for turns, reflected in actions:
        mapped_nodes = {quotient_action(node, turns, reflected) for node in qnodes}
        mapped_edges = {
            (quotient_action(parent, turns, reflected), quotient_action(child, turns, reflected))
            for parent, child in qedges
        }
        preserves.append(
            mapped_nodes == qnodes
            and mapped_edges == qedges
            and all(qweight(node) == qweight(quotient_action(node, turns, reflected)) for node in qnodes)
        )

    r5 = all(quotient_action(node, 5, False) == node for node in qnodes)
    m2 = all(
        quotient_action(quotient_action(node, 0, True), 0, True) == node
        for node in qnodes
    )
    mrm = all(
        quotient_action(
            quotient_action(quotient_action(node, 0, True), 1, False),
            0,
            True,
        ) == quotient_action(node, -1, False)
        for node in qnodes
    )

    seam_compatible = all(
        choose(n, n) == choose(n, 0) == 1
        for n in range(1, DEPTH + 1)
    )
    nadirs = {("interior", face, DEPTH, DEPTH // 2) for face in range(FACES)}
    nadir_orbit = {
        quotient_action(("interior", 0, DEPTH, DEPTH // 2), turns, False)
        for turns in range(FACES)
    }
    nadir_set_preserved = all(
        {quotient_action(node, turns, reflected) for node in nadirs} == nadirs
        for turns, reflected in actions
    )

    checks = {
        "five_raw_faces_have_140_nodes": len(raw_nodes) == 140,
        "glued_fan_has_106_unique_nodes": len(qnodes) == 106,
        "glued_fan_is_connected": component_count(qnodes, qedges) == 1,
        "all_ten_d5_actions_are_distinct": len(signatures) == 10,
        "r_pow_5_is_identity": r5,
        "m_pow_2_is_identity": m2,
        "m_r_m_equals_r_inverse": mrm,
        "all_d5_actions_preserve_weights_and_recurrence_edges": all(preserves),
        "pascal_side_chains_are_weight_compatible_for_gluing": seam_compatible,
        "five_nadir_20_nodes_form_one_rotation_orbit": nadir_orbit == nadirs and all(qweight(node) == 20 for node in nadirs),
        "nadir_20_set_is_preserved_by_d5": nadir_set_preserved,
    }

    return {
        "schema": "nexah.pascal-pentagon-d5-test/1.0.0",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "classification": "BOUNDED_CANDIDATE_EVIDENCE_NOT_ADMITTED",
        "parameters": {"faces": FACES, "depth": DEPTH, "layers": DEPTH + 1},
        "result": {
            "working_object": "five-face glued Pascal fan",
            "working_label": "Pascal pentagon",
            "raw_node_count": len(raw_nodes),
            "quotient_node_count": len(qnodes),
            "quotient_edge_count": len(qedges),
            "component_count_after_gluing": component_count(qnodes, qedges),
            "operator_group": "D5",
            "operator_group_order": len(signatures),
            "rotation_subgroup": "C5",
            "base_center_weight": choose(DEPTH, DEPTH // 2),
            "base_center_orbit_size": len(nadir_orbit),
            "four_inner_layers_interpretation": "UNDEFINED_IN_CURRENT_CONTRACT",
        },
        "checks": checks,
        "claim_ceiling": "Finite binomial face-complex and D5 symmetry fixture only; no universal Pascal algebra, physical five-stage mechanism, or four-layer interior is established.",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)

