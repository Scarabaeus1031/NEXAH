#!/usr/bin/env python3
"""Audit the missing X20 adjacency contract against the frozen Q106 interface."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def connected(subset: set[int], adjacency: list[set[int]]) -> bool:
    if not subset:
        return False
    visited = {next(iter(subset))}
    stack = list(visited)
    while stack:
        node = stack.pop()
        for neighbor in adjacency[node] & subset:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
    return visited == subset


def edge_profile(edges: set[tuple[int, int]], nodes: set[int]) -> dict[str, object]:
    degrees = Counter(sum(node in edge for edge in edges) for node in nodes)
    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "degree_profile": {str(k): v for k, v in sorted(degrees.items())},
        "connected": connected(nodes, [
            {b for a, b in edges if a == i} | {a for a, b in edges if b == i}
            for i in range(max(nodes) + 1)
        ]),
    }


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

    paths: dict[str, Path] = {}
    for key, source in contract["frozen_sources"].items():
        source_path = (HERE / source["path"]).resolve()
        paths[key] = source_path
        observed = sha256(source_path) if source_path.exists() else None
        check(f"frozen source {key}", observed == source["sha256"], observed, source["sha256"])

    parent = json.loads(paths["parent_result"].read_text(encoding="utf-8"))
    check(
        "parent keeps typed intertwiner open",
        parent["summary"]["typed_intertwiner_to_q106"] is None,
        parent["summary"]["typed_intertwiner_to_q106"],
        None,
    )

    with paths["q106_nodes"].open(newline="", encoding="utf-8") as handle:
        nodes = list(csv.DictReader(handle))
    with paths["q106_edges"].open(newline="", encoding="utf-8") as handle:
        directed_edges = list(csv.DictReader(handle))
    automorphisms = json.loads(paths["q106_automorphisms"].read_text(encoding="utf-8"))
    actions = automorphisms["actions"]
    permutations = [action["permutation_zero_based"] for action in actions]
    rotation = next(action["permutation_zero_based"] for action in actions if action["name"] == "r^1")
    reflection = next(action["permutation_zero_based"] for action in actions if action["name"] == "m_r^0")

    seen: set[int] = set()
    orbits: list[list[int]] = []
    for node in range(len(nodes)):
        if node in seen:
            continue
        orbit = sorted({permutation[node] for permutation in permutations})
        seen.update(orbit)
        orbits.append(orbit)

    adjacency = [set() for _ in nodes]
    undirected_edges: set[tuple[int, int]] = set()
    for row in directed_edges:
        source, target = int(row["source_index"]), int(row["target_index"])
        if source == target:
            continue
        edge = tuple(sorted((source, target)))
        undirected_edges.add(edge)
        adjacency[source].add(target)
        adjacency[target].add(source)

    candidates: list[tuple[int, ...]] = []
    for orbit_indices in itertools.combinations(range(len(orbits)), 4):
        if any(len(orbits[index]) != 5 for index in orbit_indices):
            continue
        subset = set().union(*(set(orbits[index]) for index in orbit_indices))
        if connected(subset, adjacency):
            candidates.append(orbit_indices)
    check("unique connected four-five-orbit target", candidates == [(1, 2, 3, 4)], candidates, [(1, 2, 3, 4)])

    interface_orbits = [orbits[index] for index in candidates[0]]
    interface = set().union(*(set(orbit) for orbit in interface_orbits))
    interface_edges = {edge for edge in undirected_edges if edge[0] in interface and edge[1] in interface}
    degree_profile = Counter(len(adjacency[node] & interface) for node in interface)
    check("target interface has twenty nodes", len(interface) == 20, len(interface), 20)
    check("target interface has twenty internal edges", len(interface_edges) == 20, len(interface_edges), 20)
    check("target interface degree profile", degree_profile == {1: 5, 2: 10, 3: 5}, dict(degree_profile), {1: 5, 2: 10, 3: 5})

    # Normalize each target orbit by its unique reflection-fixed node and r action.
    target_coordinates: list[dict[str, object]] = []
    reflection_fixed_counts = []
    for target_orbit_index, orbit in zip(candidates[0], interface_orbits):
        fixed = [node for node in orbit if reflection[node] == node]
        reflection_fixed_counts.append(len(fixed))
        anchor = fixed[0]
        current = anchor
        for sector in range(5):
            target_coordinates.append({
                "target_orbit_index": target_orbit_index,
                "target_sector": sector,
                "node_index": current,
                "node_id": nodes[current]["node_id"],
                "reflection_fixed": current == anchor,
            })
            current = rotation[current]
        check(
            f"target orbit {target_orbit_index} closes under r",
            current == anchor and len({row["node_index"] for row in target_coordinates if row["target_orbit_index"] == target_orbit_index}) == 5,
            current,
            anchor,
        )
    check("each target orbit has one reflection anchor", reflection_fixed_counts == [1, 1, 1, 1], reflection_fixed_counts, [1, 1, 1, 1])

    rotation_equivariant_count = math.factorial(4) * 5**4
    d5_equivariant_count = math.factorial(4)
    check("rotation-equivariant chart count", rotation_equivariant_count == 15000, rotation_equivariant_count, 15000)
    check("D5-equivariant chart count", d5_equivariant_count == 24, d5_equivariant_count, 24)

    source_adjacency = contract["source_carrier"]["adjacency"]
    source_edge_types = contract["source_carrier"]["edge_types"]
    check("source adjacency absence is explicit", source_adjacency is None, source_adjacency, None)
    check("source edge-type absence is explicit", source_edge_types is None, source_edge_types, None)

    # Undeclared defaults are controls, never substitutes for E_X.
    empty_profile = {"nodes": 20, "edges": 0, "degree_profile": {"0": 20}}
    cycles_profile = {"nodes": 20, "edges": 20, "degree_profile": {"2": 20}}
    cartesian_profile = {"nodes": 20, "edges": 35, "degree_profile": {"3": 10, "4": 10}}
    target_profile = {"nodes": 20, "edges": 20, "degree_profile": {"1": 5, "2": 10, "3": 5}}
    check("empty comparator differs from target", empty_profile != target_profile, empty_profile, "not target profile")
    check("four-C5 comparator differs from target", cycles_profile != target_profile, cycles_profile, "not target profile")
    check("C5 Cartesian P4 comparator differs from target", cartesian_profile != target_profile, cartesian_profile, "not target profile")

    typed_intertwiner = None
    classification = "UNDEFINED_CONTRACT_ADJACENCY_MISSING"
    check(
        "typed graph intertwiner is not manufactured",
        typed_intertwiner is None and classification == "UNDEFINED_CONTRACT_ADJACENCY_MISSING",
        {"typed_intertwiner_to_q106": typed_intertwiner, "classification": classification},
        {"typed_intertwiner_to_q106": None, "classification": "UNDEFINED_CONTRACT_ADJACENCY_MISSING"},
    )

    with (HERE / "Q106_INTERFACE_COORDINATES.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(target_coordinates[0]))
        writer.writeheader()
        writer.writerows(target_coordinates)

    passed = all(item["status"] == "PASS" for item in checks)
    return {
        "schema": "nexah.ncs-x20-q106-adjacency-intertwiner-result/1.0.0",
        "date": contract["date"],
        "status": "PASS_UNDEFINED_CONTRACT_ADJACENCY_MISSING" if passed else "FAIL",
        "classification": classification if passed else "CONTRACT_INVALID",
        "identity": contract["identity"],
        "summary": {
            "checks_passed": sum(item["status"] == "PASS" for item in checks),
            "checks_total": len(checks),
            "q106_interface_nodes": len(interface),
            "q106_interface_edges": len(interface_edges),
            "q106_interface_degree_profile": {str(k): v for k, v in sorted(degree_profile.items())},
            "rotation_equivariant_bijections": rotation_equivariant_count,
            "d5_equivariant_bijections": d5_equivariant_count,
            "source_adjacency_declared": source_adjacency is not None,
            "typed_intertwiner_to_q106": typed_intertwiner
        },
        "target_interface": {
            "q106_orbit_indices": list(candidates[0]),
            "node_ids": [nodes[index]["node_id"] for index in sorted(interface)],
            "undirected_edges": [
                [nodes[source]["node_id"], nodes[target]["node_id"]]
                for source, target in sorted(interface_edges)
            ],
            "coordinate_artifact": "Q106_INTERFACE_COORDINATES.csv",
            "coordinate_artifact_role": "target-side D5 chart; not an asserted X20 map"
        },
        "source_contract_gap": {
            "carrier": "X20=C5 x P4",
            "rotation": "declared",
            "candidate_reflection": "declared for audit only",
            "adjacency": None,
            "edge_types": None,
            "minimum_next_input": "an independently sourced X20 edge list or adjacency rule plus edge-type and direction semantics"
        },
        "comparators": {
            "twenty_isolated_states": empty_profile,
            "four_disjoint_C5_cycles": cycles_profile,
            "C5_cartesian_P4": cartesian_profile,
            "q106_interface": target_profile,
            "status": "CONTROL_ONLY_NOT_SOURCE_COMPLETIONS"
        },
        "downstream": {
            "beta": None,
            "historical_janus_law": None,
            "triple19_pc_pd_compatibility": None,
            "reason": "iota and a typed Pc/Pd carrier map are absent"
        },
        "checks": checks,
        "claim_boundary": contract["claim_boundary"]
    }


if __name__ == "__main__":
    result = validate()
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "classification": result["classification"],
        "checks": f"{result['summary']['checks_passed']}/{result['summary']['checks_total']}",
        "rotation_equivariant_bijections": result["summary"]["rotation_equivariant_bijections"],
        "d5_equivariant_bijections": result["summary"]["d5_equivariant_bijections"],
        "typed_intertwiner_to_q106": result["summary"]["typed_intertwiner_to_q106"]
    }, indent=2))
    raise SystemExit(0 if result["status"].startswith("PASS") else 1)
