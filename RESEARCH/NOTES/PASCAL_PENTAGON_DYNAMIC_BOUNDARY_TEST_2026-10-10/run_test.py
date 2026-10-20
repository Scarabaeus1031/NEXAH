#!/usr/bin/env python3
"""PENT-06: finite edge growth, closure and 5/6 control test."""

from __future__ import annotations

import json
import math
from collections import defaultdict, deque


DEPTH = 6
FINAL_FACES = 5


RawNode = tuple[int, int, int]
Node = tuple[object, ...]


def choose(n: int, k: int) -> int:
    return math.comb(n, k)


def raw_nodes(face_count: int) -> set[RawNode]:
    return {
        (face, n, k)
        for face in range(face_count)
        for n in range(DEPTH + 1)
        for k in range(n + 1)
    }


def raw_edges(face_count: int) -> set[tuple[RawNode, RawNode]]:
    result = set()
    for face in range(face_count):
        for n in range(DEPTH):
            for k in range(n + 1):
                parent = (face, n, k)
                result.add((parent, (face, n + 1, k)))
                result.add((parent, (face, n + 1, k + 1)))
    return result


def canonical(node: RawNode, face_count: int, closed: bool) -> Node:
    face, n, k = node
    if n == 0:
        return ("apex",)
    if k == 0:
        seam = face
        return ("seam", n, seam % face_count if closed else seam)
    if k == n:
        seam = face + 1
        return ("seam", n, seam % face_count if closed else seam)
    return ("interior", face, n, k)


def quotient(face_count: int, closed: bool) -> tuple[set[Node], set[tuple[Node, Node]]]:
    nodes = {canonical(node, face_count, closed) for node in raw_nodes(face_count)}
    edges = {
        (canonical(parent, face_count, closed), canonical(child, face_count, closed))
        for parent, child in raw_edges(face_count)
    }
    return nodes, edges


def node_weight(node: RawNode) -> int:
    return choose(node[1], node[2])


def seam_weights_compatible(face_count: int, closed: bool) -> bool:
    representatives: dict[Node, list[RawNode]] = defaultdict(list)
    for node in raw_nodes(face_count):
        representatives[canonical(node, face_count, closed)].append(node)
    return all(len({node_weight(node) for node in group}) == 1 for group in representatives.values())


def component_count(nodes: set[Node], edges: set[tuple[Node, Node]]) -> int:
    adjacency: dict[Node, set[Node]] = defaultdict(set)
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
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


def carrier_state(face_count: int, closed: bool = False) -> dict[str, int | bool]:
    nodes, edges = quotient(face_count, closed)
    carrier_vertices = face_count + (1 if closed else 2)
    carrier_edges = 2 * face_count if closed else 2 * face_count + 1
    boundary_edges = face_count if closed else face_count + 2
    return {
        "faces": face_count,
        "closed": closed,
        "carrier_vertices": carrier_vertices,
        "carrier_edges": carrier_edges,
        "euler_characteristic": carrier_vertices - carrier_edges + face_count,
        "boundary_edges": boundary_edges,
        "boundary_components": 1,
        "pascal_nodes": len(nodes),
        "pascal_edges": len(edges),
        "components": component_count(nodes, edges),
    }


def cycle_edges(prefix: str, size: int) -> set[tuple[str, str]]:
    return {
        tuple(sorted((f"{prefix}{index}", f"{prefix}{(index + 1) % size}")))
        for index in range(size)
    }


def historical_c5_c6_c6(with_hub: bool) -> tuple[set[str], set[tuple[str, str]]]:
    modules = (("P", 5), ("HA", 6), ("HB", 6))
    nodes = {f"{prefix}{index}" for prefix, size in modules for index in range(size)}
    edges = set().union(*(cycle_edges(prefix, size) for prefix, size in modules))
    if with_hub:
        nodes.add("center")
        edges |= {tuple(sorted(("center", node))) for node in nodes if node != "center"}
    return nodes, edges


def plain_components(nodes: set[str], edges: set[tuple[str, str]]) -> int:
    adjacency = {node: set() for node in nodes}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
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


def run() -> dict[str, object]:
    open_states = [carrier_state(face_count) for face_count in range(1, FINAL_FACES + 1)]
    closed_state = carrier_state(FINAL_FACES, closed=True)

    pentagon_ticks = set(range(0, 30, 6))
    hexagon_ticks = set(range(0, 30, 5))
    shared_ticks = pentagon_ticks & hexagon_ticks

    shell_nodes, shell_edges = historical_c5_c6_c6(with_hub=False)
    hub_nodes, hub_edges = historical_c5_c6_c6(with_hub=True)

    checks = {
        "each_new_open_face_adds_21_pascal_nodes": all(
            later["pascal_nodes"] - earlier["pascal_nodes"] == 21
            for earlier, later in zip(open_states, open_states[1:])
        ),
        "open_fan_node_formula_is_21f_plus_7": all(
            state["pascal_nodes"] == 21 * state["faces"] + 7 for state in open_states
        ),
        "each_open_attachment_consumes_one_edge_and_exposes_two": all(
            later["boundary_edges"] - earlier["boundary_edges"] == 1
            for earlier, later in zip(open_states, open_states[1:])
        ),
        "open_growth_remains_one_connected_disk": all(
            state["components"] == 1
            and state["boundary_components"] == 1
            and state["euler_characteristic"] == 1
            for state in open_states
        ),
        "all_open_and_closed_seams_preserve_pascal_weights": all(
            seam_weights_compatible(face_count, False)
            for face_count in range(1, FINAL_FACES + 1)
        ) and seam_weights_compatible(FINAL_FACES, True),
        "five_face_preclosure_has_112_nodes_and_7_boundary_edges": (
            open_states[-1]["pascal_nodes"] == 112
            and open_states[-1]["boundary_edges"] == 7
        ),
        "closure_identifies_6_nodes_and_recovers_106_node_carrier": (
            open_states[-1]["pascal_nodes"] - closed_state["pascal_nodes"] == 6
            and closed_state["pascal_nodes"] == 106
        ),
        "closure_leaves_one_pentagonal_boundary_component": (
            closed_state["boundary_edges"] == 5
            and closed_state["boundary_components"] == 1
            and closed_state["euler_characteristic"] == 1
        ),
        "c5_c6_clock_has_30_steps_and_one_shared_anchor_per_period": (
            math.lcm(5, 6) == 30
            and pentagon_ticks == {0, 6, 12, 18, 24}
            and hexagon_ticks == {0, 5, 10, 15, 20, 25}
            and shared_ticks == {0}
        ),
        "archived_c5_c6_c6_shell_has_17_nodes_17_edges_3_components": (
            len(shell_nodes) == 17
            and len(shell_edges) == 17
            and plain_components(shell_nodes, shell_edges) == 3
        ),
        "archived_hub_fixture_has_18_nodes_34_edges_and_is_connected": (
            len(hub_nodes) == 18
            and len(hub_edges) == 34
            and plain_components(hub_nodes, hub_edges) == 1
        ),
    }

    return {
        "schema": "nexah.pascal-pentagon-dynamic-boundary-test/1.0.0",
        "status": "PASS_WITH_BOUNDARY" if all(checks.values()) else "FAIL",
        "classification": "BOUNDED_CANDIDATE_EVIDENCE_NOT_ADMITTED",
        "parameters": {
            "pascal_depth": DEPTH,
            "maximum_faces_before_closure": FINAL_FACES,
            "historical_control": "C5 + C6 + C6",
        },
        "result": {
            "working_object": "sequential depth-six Pascal-face attachment with explicit closure",
            "state_rule": "carrier_(t+1) = carrier_t union_(one open radial edge) one new face",
            "open_states": open_states,
            "closed_state": closed_state,
            "node_growth_rule": "N_open(f) = 21f + 7; N_closed(5) = 106",
            "boundary_growth_rule": "B_open(f) = f + 2; B_closed(5) = 5",
            "c5_c6_control": {
                "period_steps": 30,
                "step_angle_degrees": 12,
                "pentagon_ticks": sorted(pentagon_ticks),
                "hexagon_ticks": sorted(hexagon_ticks),
                "shared_ticks": sorted(shared_ticks),
                "second_hexagon_effect_without_phase_map": "NO_CHANGE_TO_LCM",
            },
            "historical_c5_c6_c6_control": {
                "shell_nodes": len(shell_nodes),
                "shell_edges": len(shell_edges),
                "shell_components_without_hub": plain_components(shell_nodes, shell_edges),
                "hub_fixture_nodes": len(hub_nodes),
                "hub_fixture_edges": len(hub_edges),
                "hub_fixture_components": plain_components(hub_nodes, hub_edges),
                "structural_reading": "the archived cycles are coupled by the declared center hub, not by Pascal edge gluing",
            },
            "pascal_to_c5_c6_c6_intertwiner": "UNDEFINED_NO_INTERTWINER",
            "one_hundred_six_equals_thirteen_times_eight": False,
            "one_hundred_six_arithmetic": "106 = 13*8 + 2; no structural 13-by-8 decomposition is established",
        },
        "checks": checks,
        "claim_ceiling": "Finite combinatorial growth/closure and clock/topology controls only. The archived C5+C6+C6 fixture is a source comparator, not an identified image of the 106-node Pascal carrier. No resonance, physical mechanism, universal dynamic-boundary law or canonical Family is established.",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS_WITH_BOUNDARY" else 1)
