#!/usr/bin/env python3
"""PENT-07: finite pentagon/hexagon coupling and modular-marker audit."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]

SOURCES = {
    "hub_fixture": ROOT / "EXPERIMENTAL/BUILDER_LAB/ARCHIVE_ENGINE/archived/research/experiments/symmetry_graph_experiment/symmetry_graph_3cycle.py",
    "no_hub_control": ROOT / "EXPERIMENTAL/BUILDER_LAB/ARCHIVE_ENGINE/archived/research/experiments/symmetry_graph_experiment/symmetry_graph_no_hub_experiment.py",
    "partition_control": ROOT / "EXPERIMENTAL/BUILDER_LAB/ARCHIVE_ENGINE/archived/research/experiments/symmetry_graph_experiment/symmetry_graph_cycle_balance_test.py",
    "interference_demo": ROOT / "EXPERIMENTAL/BUILDER_LAB/ARCHIVE_ENGINE/archived/kernel/demos/pentagon/pentagon_hexagon_interference_field_demo.py",
    "twelve_mode_demo": ROOT / "EXPERIMENTAL/BUILDER_LAB/ARCHIVE_ENGINE/archived/kernel/demos/pentagon/pentagon_hexagon_12_mode_resonance_demo.py",
    "draft_marker": ROOT / "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/Riemann_IEEE_Connection.md",
    "grid_history": ROOT / "RESEARCH/HISTORY/PRIME_BASE_MODE_ARCHAEOLOGY_2026-10-09.md",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cycle_edges(size: int) -> set[tuple[int, int]]:
    return {
        tuple(sorted((index, (index + 1) % size)))
        for index in range(size)
    }


def is_graph_homomorphism(source_size: int, target_size: int, mapping: tuple[int, ...]) -> bool:
    target_edges = cycle_edges(target_size)
    return all(
        tuple(sorted((mapping[left], mapping[right]))) in target_edges
        for left, right in cycle_edges(source_size)
    )


def graph_homomorphism_count(source_size: int, target_size: int) -> int:
    return sum(
        is_graph_homomorphism(source_size, target_size, mapping)
        for mapping in itertools.product(range(target_size), repeat=source_size)
    )


def cycle_isomorphism_count(size: int) -> int:
    return sum(
        is_graph_homomorphism(size, size, mapping)
        for mapping in itertools.permutations(range(size))
    )


def components(nodes: set[str], edges: set[tuple[str, str]]) -> int:
    adjacency = {node: set() for node in nodes}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(nodes)
    count = 0
    while unseen:
        count += 1
        stack = [unseen.pop()]
        while stack:
            current = stack.pop()
            for neighbor in adjacency[current]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
    return count


def hub_fixture() -> dict[str, int]:
    modules = (("P", 5), ("HA", 6), ("HB", 6))
    shell_nodes = {f"{prefix}{index}" for prefix, size in modules for index in range(size)}
    shell_edges = {
        tuple(sorted((f"{prefix}{index}", f"{prefix}{(index + 1) % size}")))
        for prefix, size in modules
        for index in range(size)
    }
    hub_nodes = shell_nodes | {"center"}
    hub_edges = shell_edges | {
        tuple(sorted(("center", node))) for node in shell_nodes
    }
    return {
        "shell_nodes": len(shell_nodes),
        "shell_edges": len(shell_edges),
        "shell_components": components(shell_nodes, shell_edges),
        "hub_nodes": len(hub_nodes),
        "hub_edges": len(hub_edges),
        "hub_components": components(hub_nodes, hub_edges),
    }


def shift_stabilizer(points: set[int], modulus: int) -> list[int]:
    return [
        shift
        for shift in range(modulus)
        if {(point + shift) % modulus for point in points} == points
    ]


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        while value % divisor == 0:
            factors.append(divisor)
            value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return factors


def run() -> dict[str, object]:
    c5_ticks = set(range(0, 30, 6))
    c6_ticks = set(range(0, 30, 5))
    shared_ticks = c5_ticks & c6_ticks
    c5_stabilizer = shift_stabilizer(c5_ticks, 30)
    c6_stabilizer = shift_stabilizer(c6_ticks, 30)
    joint_stabilizer = sorted(set(c5_stabilizer) & set(c6_stabilizer))

    fixture = hub_fixture()
    c5_to_c6_homomorphisms = graph_homomorphism_count(5, 6)
    c6_to_c5_homomorphisms = graph_homomorphism_count(6, 5)
    c6_pair_isomorphisms = cycle_isomorphism_count(6)

    interference_text = SOURCES["interference_demo"].read_text()
    twelve_mode_text = SOURCES["twelve_mode_demo"].read_text()
    source_records = {
        name: {
            "path": str(path.relative_to(ROOT)),
            "sha256": digest(path),
        }
        for name, path in SOURCES.items()
    }

    markers = {
        str(value): {
            "prime_factors": prime_factors(value),
            "mod_5": value % 5,
            "mod_6": value % 6,
            "mod_11": value % 11,
            "mod_12": value % 12,
            "mod_30": value % 30,
        }
        for value in (110, 111, 112)
    }

    checks = {
        "c5_plus_c6_is_11_and_c6_plus_c6_is_12": 5 + 6 == 11 and 6 + 6 == 12,
        "c5_and_c6_have_no_bijection": math.factorial(5) != math.factorial(6) and 5 != 6,
        "no_edge_preserving_graph_map_c5_to_c6": c5_to_c6_homomorphisms == 0,
        "c5_and_c6_embed_as_anchor_sets_in_c30": (
            len(c5_ticks) == 5 and len(c6_ticks) == 6 and shared_ticks == {0}
        ),
        "joint_c30_rotational_stabilizer_is_identity": joint_stabilizer == [0],
        "two_c6_cycles_have_12_dihedral_isomorphisms": c6_pair_isomorphisms == 12,
        "second_c6_needs_declared_correspondence": c6_pair_isomorphisms > 1,
        "hub_fixture_reconstructs_archived_counts": fixture == {
            "shell_nodes": 17,
            "shell_edges": 17,
            "shell_components": 3,
            "hub_nodes": 18,
            "hub_edges": 34,
            "hub_components": 1,
        },
        "interference_demo_declares_equations_but_no_random_seed": (
            "def flow(x,y):" in interference_text
            and "np.random.uniform" in interference_text
            and "np.random.seed" not in interference_text
        ),
        "twelve_mode_axes_are_drawn_reference_lines_not_measured_modes": (
            "Draw 12 resonance axes" in twelve_mode_text
            and "for i in range(12):" in twelve_mode_text
            and "reference lines" in twelve_mode_text
        ),
        "one_hundred_twelve_is_open_preclosure_count_not_5_6_sum": (
            112 not in {5 + 6, 6 + 6, 5 + 6 + 6}
        ),
        "modular_shadow_requires_declared_modulus": len({112 % modulus for modulus in (5, 6, 11, 12, 30)}) > 1,
        "historical_110_111_112_markers_have_distinct_factorizations": (
            markers["110"]["prime_factors"] == [2, 5, 11]
            and markers["111"]["prime_factors"] == [3, 37]
            and markers["112"]["prime_factors"] == [2, 2, 2, 2, 7]
        ),
        "all_declared_sources_exist_and_are_hashed": all(
            record["sha256"] for record in source_records.values()
        ),
    }

    return {
        "schema": "nexah.pascal-pentagon-hexagon-coupling-audit/1.0.0",
        "status": "PASS_WITH_BOUNDARY" if all(checks.values()) else "FAIL",
        "classification": "BOUNDED_CANDIDATE_EVIDENCE_NOT_ADMITTED",
        "identity": "PENT-07 under existing A0OE:PASCAL_PENTAGON_D5_TEST lens identity",
        "question": "Which existing pentagon/hexagon visuals instantiate a declared coupling, and which remain arithmetic, reference-axis or provenance markers?",
        "result": {
            "coupling_classes": {
                "direct_cycle_identification_C5_to_C6": "FAIL_CARDINALITY_AND_GRAPH_HOMOMORPHISM",
                "common_phase_cover_C30": "PASS_AS_ANCHOR_EMBEDDING_NOT_GRAPH_EDGE_EMBEDDING",
                "C6A_to_C6B": "PASS_ONLY_AFTER_SELECTING_ONE_OF_12_DIHEDRAL_ISOMORPHISMS",
                "C5_C6_C6_common_hub": "PASS_AS_ARCHIVED_HUB_COUPLING",
                "interference_field": "EQUATIONS_DEFINED_TRAJECTORY_SAMPLE_UNSEEDED",
                "twelve_mode_emergence": "UNDEFINED_REFERENCE_AXES_DRAWN_NOT_INFERRED",
                "pascal_carrier_intertwiner": "UNDEFINED_NO_NODE_EDGE_WEIGHT_OPERATOR_MAP",
            },
            "arithmetic_markers": {
                "5_plus_6": 11,
                "6_plus_6": 12,
                "5_plus_6_plus_6": 17,
                "interpretation": "cardinality ledger only; sums do not add coupling edges or define an operator",
            },
            "phase_cover": {
                "modulus": 30,
                "step_degrees": 12,
                "c5_ticks": sorted(c5_ticks),
                "c6_ticks": sorted(c6_ticks),
                "shared_ticks": sorted(shared_ticks),
                "c5_stabilizer": c5_stabilizer,
                "c6_stabilizer": c6_stabilizer,
                "joint_stabilizer": joint_stabilizer,
            },
            "map_counts": {
                "C5_to_C6_graph_homomorphisms": c5_to_c6_homomorphisms,
                "C6_to_C5_graph_homomorphisms": c6_to_c5_homomorphisms,
                "C6_to_C6_isomorphisms": c6_pair_isomorphisms,
            },
            "hub_fixture": fixture,
            "historical_number_markers": {
                "markers": markers,
                "one_over_112": 1 / 112,
                "classification": "PROVENANCE_AND_SEARCH_MARKERS_ONLY",
                "boundary": "A modular shadow is a function of a declared modulus. No canonical map connects 110, 111 or 112 to the C5/C6 coupling audit.",
            },
            "sources": source_records,
        },
        "checks": checks,
        "claim_ceiling": "Finite graph, cycle, phase-cover, source-code and arithmetic audit only. It establishes no resonance, 12-mode emergence, physical field, canonical role for 110/111/112, identity between the Pascal carrier and archived Core fixtures, or new NEXAH Family.",
    }


if __name__ == "__main__":
    result = run()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--write" in sys.argv[1:]:
        (Path(__file__).parent / "RESULT.json").write_text(rendered)
    print(rendered, end="")
    raise SystemExit(0 if result["status"] == "PASS_WITH_BOUNDARY" else 1)
