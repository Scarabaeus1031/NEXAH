#!/usr/bin/env python3
"""Independently reconstruct and verify the SCC-003 reference package.

The verifier deliberately does not import the generator.  It builds the
quotient with union-find, reads every exported table, checks hashes, and
re-evaluates the finite propositions used by the reference object.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import defaultdict, deque
from pathlib import Path
from typing import Iterable


DEPTH = 6
FACES = 5
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "artifacts"

Raw = tuple[int, int, int]


class UnionFind:
    def __init__(self, items: Iterable[Raw]):
        self.parent = {item: item for item in items}

    def find(self, item: Raw) -> Raw:
        trail = []
        while self.parent[item] != item:
            trail.append(item)
            item = self.parent[item]
        for member in trail:
            self.parent[member] = item
        return item

    def union(self, left: Raw, right: Raw) -> None:
        a, b = self.find(left), self.find(right)
        if a != b:
            self.parent[max(a, b)] = min(a, b)


def all_raw(face_count: int = FACES) -> list[Raw]:
    return [(face, n, k) for face in range(face_count) for n in range(DEPTH + 1) for k in range(n + 1)]


def build_classes(face_count: int, closed: bool) -> list[list[Raw]]:
    raw = all_raw(face_count)
    uf = UnionFind(raw)
    for face in range(1, face_count):
        uf.union((0, 0, 0), (face, 0, 0))
    for face in range(face_count - 1):
        for n in range(1, DEPTH + 1):
            uf.union((face, n, n), (face + 1, n, 0))
    if closed:
        for n in range(1, DEPTH + 1):
            uf.union((face_count - 1, n, n), (0, n, 0))
    groups: dict[Raw, list[Raw]] = defaultdict(list)
    for item in raw:
        groups[uf.find(item)].append(item)
    return [sorted(group) for group in groups.values()]


def class_id(group: list[Raw]) -> str:
    if group[0][1] == 0:
        return "A"
    n = group[0][1]
    if len(group) == 2:
        right_members = [face for face, _, k in group if k == n]
        if len(right_members) != 1:
            raise AssertionError(f"cannot orient seam class {group}")
        return f"S_{n:02d}_{right_members[0]:02d}"
    if len(group) == 1:
        face, _, k = group[0]
        return f"I_{face:02d}_{n:02d}_{k:02d}"
    raise AssertionError(f"unexpected equivalence class {group}")


def canonical_order(node_id: str) -> tuple[int, int, int, int]:
    if node_id == "A":
        return (0, 0, 0, 0)
    kind, a, b, *tail = node_id.split("_")
    if kind == "S":
        return (int(a), 0, int(b), 0)
    return (int(b), 1, int(a), int(tail[0]))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(name: str) -> list[dict[str, str]]:
    with (OUT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def decode_graph6(value: str) -> tuple[int, set[tuple[int, int]]]:
    data = [ord(char) - 63 for char in value.strip()]
    if not data:
        raise ValueError("empty graph6 value")
    if data[0] <= 62:
        n, start = data[0], 1
    elif len(data) >= 4 and data[1] != 63:
        n = (data[1] << 12) | (data[2] << 6) | data[3]
        start = 4
    else:
        raise ValueError("unsupported graph6 order encoding")
    bits = []
    for encoded in data[start:]:
        bits.extend((encoded >> shift) & 1 for shift in range(5, -1, -1))
    edges = set()
    cursor = 0
    for right in range(1, n):
        for left in range(right):
            if bits[cursor]:
                edges.add((left, right))
            cursor += 1
    return n, edges


def connected(node_count: int, edges: set[tuple[int, int]]) -> bool:
    adjacency = [set() for _ in range(node_count)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = {0}
    queue = deque([0])
    while queue:
        current = queue.popleft()
        for neighbor in adjacency[current] - seen:
            seen.add(neighbor)
            queue.append(neighbor)
    return len(seen) == node_count


def cycle_automorphisms(size: int) -> set[tuple[int, ...]]:
    rotations = {tuple((item + shift) % size for item in range(size)) for shift in range(size)}
    reflections = {tuple((-item + shift) % size for item in range(size)) for shift in range(size)}
    return rotations | reflections


def main() -> int:
    checks: dict[str, bool] = {}
    failures: list[str] = []

    def check(name: str, condition: bool) -> None:
        checks[name] = bool(condition)
        if not condition:
            failures.append(name)

    manifest = json.loads((OUT / "manifest.json").read_text(encoding="utf-8"))
    for name, record in manifest["artifacts"].items():
        path = OUT / name
        check(f"manifest:{name}:exists", path.is_file())
        if path.is_file():
            check(f"manifest:{name}:sha256", file_sha256(path) == record["sha256"])
            check(f"manifest:{name}:bytes", path.stat().st_size == record["bytes"])

    sums = {}
    for line in (OUT / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        digest, name = line.split("  ", 1)
        sums[name] = digest
    for name, digest in sums.items():
        check(f"sha256sums:{name}", file_sha256(OUT / name) == digest)

    classes = build_classes(FACES, closed=True)
    class_by_id = {class_id(group): group for group in classes}
    ordered_ids = sorted(class_by_id, key=canonical_order)
    id_to_index = {node_id: index for index, node_id in enumerate(ordered_ids)}
    raw_to_id = {raw: node_id for node_id, group in class_by_id.items() for raw in group}

    node_rows = read_csv("nodes.csv")
    check("closed_quotient_has_106_nodes", len(classes) == 106 == len(node_rows))
    check("node_ids_and_order_match_independent_union_find", [row["node_id"] for row in node_rows] == ordered_ids)
    check("node_indices_are_contiguous", [int(row["index"]) for row in node_rows] == list(range(106)))

    expected_weights = {}
    for node_id, group in class_by_id.items():
        weights = {math.comb(n, k) for _, n, k in group}
        check(f"weight_class:{node_id}", len(weights) == 1)
        expected_weights[node_id] = next(iter(weights))
    check("node_weights_match", all(int(row["weight"]) == expected_weights[row["node_id"]] for row in node_rows))
    weight_rows = read_csv("weights.csv")
    check("weights_table_matches", [(int(row["index"]), row["node_id"], int(row["weight"])) for row in weight_rows] == [(index, node_id, expected_weights[node_id]) for index, node_id in enumerate(ordered_ids)])

    expected_edges = set()
    expected_face_edges = []
    for face in range(FACES):
        for n in range(DEPTH):
            for k in range(n + 1):
                source = raw_to_id[(face, n, k)]
                for branch, child_k in (("left", k), ("right", k + 1)):
                    target = raw_to_id[(face, n + 1, child_k)]
                    expected_edges.add((id_to_index[source], id_to_index[target]))
                    expected_face_edges.append((face, n, k, branch, id_to_index[source], source, id_to_index[target], target))
    edge_rows = read_csv("edges.csv")
    actual_edges = {(int(row["source_index"]), int(row["target_index"])) for row in edge_rows}
    check("directed_edge_count_is_180", len(expected_edges) == 180 == len(edge_rows))
    check("directed_edges_match_independent_reconstruction", actual_edges == expected_edges)

    face_rows = read_csv("face_incidence.csv")
    actual_face_positions = {
        (int(row["face"]), int(row["n"]), int(row["k"])): (row["quotient_node_id"], int(row["raw_weight"]))
        for row in face_rows
    }
    check("face_incidence_has_140_positions", len(face_rows) == 140)
    check(
        "face_incidence_matches_union_find",
        all(actual_face_positions[raw] == (raw_to_id[raw], math.comb(raw[1], raw[2])) for raw in all_raw()),
    )
    check(
        "facewise_pascal_recurrence_holds",
        all(
            actual_face_positions[(face, n, k)][1]
            == (actual_face_positions[(face, n - 1, k - 1)][1] if k > 0 else 0)
            + (actual_face_positions[(face, n - 1, k)][1] if k < n else 0)
            for face in range(FACES)
            for n in range(1, DEPTH + 1)
            for k in range(n + 1)
        ),
    )

    face_edge_rows = read_csv("face_edges.csv")
    actual_face_edges = [
        (int(row["face"]), int(row["parent_n"]), int(row["parent_k"]), row["branch"], int(row["source_index"]), row["source_id"], int(row["target_index"]), row["target_id"])
        for row in face_edge_rows
    ]
    check("face_edge_incidence_count_is_210", len(face_edge_rows) == 210)
    check("face_edge_incidences_match", actual_face_edges == expected_face_edges)

    seam_rows = read_csv("seam_classes.csv")
    expected_nontrivial = {node_id: group for node_id, group in class_by_id.items() if len(group) > 1}
    check("nontrivial_classes_are_apex_plus_30_seams", len(expected_nontrivial) == 31 == len(seam_rows))
    check(
        "seam_class_sizes_match",
        all(int(row["class_size"]) == len(expected_nontrivial[row["quotient_node_id"]]) for row in seam_rows),
    )

    matrix_rows = read_csv("adjacency_matrix.csv")
    check("adjacency_matrix_has_106_rows", len(matrix_rows) == 106)
    check(
        "adjacency_matrix_matches_directed_edges",
        all(
            int(matrix_rows[left][ordered_ids[right]]) == (1 if (left, right) in expected_edges else 0)
            for left in range(106)
            for right in range(106)
        ),
    )

    graph6_value = (OUT / "underlying_graph.g6").read_text(encoding="ascii").strip()
    graph_order, graph_edges = decode_graph6(graph6_value)
    expected_undirected = {tuple(sorted(edge)) for edge in expected_edges}
    check("graph6_order_is_106", graph_order == 106)
    check("graph6_matches_underlying_graph", graph_edges == expected_undirected)
    check("underlying_graph_is_connected", connected(106, expected_undirected))

    autos = json.loads((OUT / "automorphisms.json").read_text(encoding="utf-8"))
    permutations = [tuple(action["permutation_zero_based"]) for action in autos["actions"]]
    check("typed_group_is_D5_order_10", autos["typed_automorphism_group"] == "D5" and autos["order"] == 10 and len(set(permutations)) == 10)
    check("face_cycle_has_exactly_ten_automorphisms", len(cycle_automorphisms(FACES)) == 10)
    check(
        "all_declared_actions_preserve_weights_and_directed_edges",
        all(
            { (permutation[left], permutation[right]) for left, right in expected_edges } == expected_edges
            and all(expected_weights[ordered_ids[index]] == expected_weights[ordered_ids[permutation[index]]] for index in range(106))
            for permutation in permutations
        ),
    )
    identity = tuple(range(106))
    r = permutations[1]
    m = permutations[5]
    compose = lambda left, right: tuple(left[right[index]] for index in range(106))
    power = lambda permutation, exponent: identity if exponent == 0 else _power(permutation, exponent, compose, identity)
    check("r_power_5_is_identity", power(r, 5) == identity)
    check("m_power_2_is_identity", power(m, 2) == identity)
    inverse_r = power(r, 4)
    check("m_r_m_equals_r_inverse", compose(m, compose(r, m)) == inverse_r)

    open_counts = [len(build_classes(face_count, closed=False)) for face_count in range(1, FACES + 1)]
    check("open_counts_are_28_49_70_91_112", open_counts == [28, 49, 70, 91, 112])
    check("each_new_face_adds_21", all(b - a == 21 for a, b in zip(open_counts, open_counts[1:])))
    check("closure_identifies_exactly_six_nodes", open_counts[-1] - len(classes) == 6)

    metrics = json.loads((OUT / "expected_metrics.json").read_text(encoding="utf-8"))
    check("expected_metrics_counts_match", metrics["counts"]["quotient_nodes"] == 106 and metrics["counts"]["directed_quotient_edges"] == 180 and metrics["counts"]["open_nodes_by_face_count"] == open_counts)
    check("expected_metrics_graph6_matches", metrics["fingerprints"]["graph6"] == graph6_value)

    report = {
        "schema": "nexah.scc-003-reference-verification/1.0.0",
        "status": "PASS" if not failures else "FAIL",
        "identity": "SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST",
        "verification_mode": "independent union-find reconstruction; generator not imported",
        "checks": checks,
        "failures": failures,
        "summary": {
            "open_nodes": open_counts,
            "closed_nodes": len(classes),
            "directed_edges": len(expected_edges),
            "graph6_sha256": hashlib.sha256((graph6_value + "\n").encode("ascii")).hexdigest(),
            "typed_automorphism_group": "D5",
            "typed_automorphism_group_order": 10,
        },
        "claim_ceiling": "Verification of the deterministic bounded SCC-003 reference object only; not a novelty or publication determination.",
    }
    (OUT / "VERIFICATION.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checks": len(checks), "failures": failures}, sort_keys=True))
    return 0 if not failures else 1


def _power(permutation: tuple[int, ...], exponent: int, compose, identity: tuple[int, ...]) -> tuple[int, ...]:
    result = identity
    for _ in range(exponent):
        result = compose(permutation, result)
    return result


if __name__ == "__main__":
    raise SystemExit(main())
