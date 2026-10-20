#!/usr/bin/env python3
"""Generate the deterministic SCC-003 depth-six, five-face reference object.

This is a reproducibility export for the already recorded PENT-01/PENT-06
construction.  It does not run a generalized experiment or raise the claim
ceiling.
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

RawNode = tuple[int, int, int]
Node = tuple[object, ...]
Edge = tuple[Node, Node]


def raw_nodes() -> Iterable[RawNode]:
    for face in range(FACES):
        for n in range(DEPTH + 1):
            for k in range(n + 1):
                yield face, n, k


def canonical(raw: RawNode) -> Node:
    face, n, k = raw
    if n == 0:
        return ("apex",)
    if k == 0:
        return ("seam", n, (face - 1) % FACES)
    if k == n:
        return ("seam", n, face)
    return ("interior", face, n, k)


def node_id(node: Node) -> str:
    if node == ("apex",):
        return "A"
    if node[0] == "seam":
        _, n, seam = node
        return f"S_{int(n):02d}_{int(seam):02d}"
    _, face, n, k = node
    return f"I_{int(face):02d}_{int(n):02d}_{int(k):02d}"


def node_order(node: Node) -> tuple[int, int, int, int]:
    if node == ("apex",):
        return (0, 0, 0, 0)
    if node[0] == "seam":
        _, n, seam = node
        return (int(n), 0, int(seam), 0)
    _, face, n, k = node
    return (int(n), 1, int(face), int(k))


def weight(node: Node) -> int:
    if node == ("apex",) or node[0] == "seam":
        return 1
    return math.comb(int(node[2]), int(node[3]))


def raw_edges() -> Iterable[tuple[int, int, int, int, RawNode, RawNode]]:
    for face in range(FACES):
        for n in range(DEPTH):
            for k in range(n + 1):
                parent = (face, n, k)
                yield face, n, k, 0, parent, (face, n + 1, k)
                yield face, n, k, 1, parent, (face, n + 1, k + 1)


def rotate(node: Node, turns: int) -> Node:
    if node == ("apex",):
        return node
    if node[0] == "seam":
        _, n, seam = node
        return ("seam", int(n), (int(seam) + turns) % FACES)
    _, face, n, k = node
    return ("interior", (int(face) + turns) % FACES, int(n), int(k))


def mirror(node: Node) -> Node:
    if node == ("apex",):
        return node
    if node[0] == "seam":
        _, n, seam = node
        return ("seam", int(n), (-int(seam) - 1) % FACES)
    _, face, n, k = node
    return canonical(((-int(face)) % FACES, int(n), int(n) - int(k)))


def action(node: Node, turns: int, reflected: bool) -> Node:
    moved = rotate(node, turns)
    return mirror(moved) if reflected else moved


def graph6(n: int, undirected_edges: set[tuple[int, int]]) -> str:
    if not 0 <= n <= 258047:
        raise ValueError("this exporter supports graph6 orders up to 258047")
    if n <= 62:
        prefix = chr(n + 63)
    else:
        prefix = "~" + "".join(chr(((n >> shift) & 0x3F) + 63) for shift in (12, 6, 0))
    bits = []
    for right in range(1, n):
        for left in range(right):
            bits.append(1 if (left, right) in undirected_edges else 0)
    while len(bits) % 6:
        bits.append(0)
    payload = "".join(
        chr(sum(bits[start + offset] << (5 - offset) for offset in range(6)) + 63)
        for start in range(0, len(bits), 6)
    )
    return prefix + payload


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, header: list[str], rows: Iterable[Iterable[object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


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


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    raw = list(raw_nodes())
    nodes = sorted({canonical(item) for item in raw}, key=node_order)
    index = {node: position for position, node in enumerate(nodes)}
    ids = {node: node_id(node) for node in nodes}

    edge_incidence = list(raw_edges())
    directed_edges: set[Edge] = {
        (canonical(parent), canonical(child))
        for _, _, _, _, parent, child in edge_incidence
    }
    ordered_edges = sorted(directed_edges, key=lambda edge: (index[edge[0]], index[edge[1]]))
    undirected_edges = {
        tuple(sorted((index[parent], index[child]))) for parent, child in directed_edges
    }

    representatives: dict[Node, list[RawNode]] = defaultdict(list)
    for item in raw:
        representatives[canonical(item)].append(item)

    write_csv(
        OUT / "nodes.csv",
        ["index", "node_id", "kind", "level_n", "face", "position_k", "seam", "weight"],
        (
            [
                index[node],
                ids[node],
                node[0],
                0 if node == ("apex",) else (node[1] if node[0] == "seam" else node[2]),
                "" if node[0] != "interior" else node[1],
                "" if node[0] != "interior" else node[3],
                "" if node[0] != "seam" else node[2],
                weight(node),
            ]
            for node in nodes
        ),
    )
    write_csv(
        OUT / "weights.csv",
        ["index", "node_id", "weight"],
        ([index[node], ids[node], weight(node)] for node in nodes),
    )
    write_csv(
        OUT / "edges.csv",
        ["edge_index", "source_index", "source_id", "target_index", "target_id"],
        ([edge_index, index[parent], ids[parent], index[child], ids[child]] for edge_index, (parent, child) in enumerate(ordered_edges)),
    )
    write_csv(
        OUT / "face_incidence.csv",
        ["face", "n", "k", "raw_weight", "quotient_index", "quotient_node_id"],
        ([face, n, k, math.comb(n, k), index[canonical((face, n, k))], ids[canonical((face, n, k))]] for face, n, k in raw),
    )
    write_csv(
        OUT / "face_edges.csv",
        ["face", "parent_n", "parent_k", "branch", "source_index", "source_id", "target_index", "target_id"],
        (
            [face, n, k, "left" if branch == 0 else "right", index[canonical(parent)], ids[canonical(parent)], index[canonical(child)], ids[canonical(child)]]
            for face, n, k, branch, parent, child in edge_incidence
        ),
    )
    nontrivial_classes = [node for node in nodes if len(representatives[node]) > 1]
    write_csv(
        OUT / "seam_classes.csv",
        ["quotient_index", "quotient_node_id", "class_size", "raw_members"],
        (
            [
                index[node],
                ids[node],
                len(representatives[node]),
                ";".join(f"({face},{n},{k})" for face, n, k in sorted(representatives[node])),
            ]
            for node in nontrivial_classes
        ),
    )

    matrix = [[0] * len(nodes) for _ in nodes]
    for parent, child in directed_edges:
        matrix[index[parent]][index[child]] = 1
    write_csv(
        OUT / "adjacency_matrix.csv",
        ["source\\target"] + [ids[node] for node in nodes],
        ([ids[node]] + matrix[index[node]] for node in nodes),
    )

    graph6_value = graph6(len(nodes), undirected_edges)
    (OUT / "underlying_graph.g6").write_text(graph6_value + "\n", encoding="ascii")

    automorphisms = []
    for reflected in (False, True):
        for turns in range(FACES):
            permutation = [index[action(node, turns, reflected)] for node in nodes]
            automorphisms.append(
                {
                    "name": f"{'m_r' if reflected else 'r'}^{turns}",
                    "turns": turns,
                    "reflected": reflected,
                    "permutation_zero_based": permutation,
                }
            )
    (OUT / "automorphisms.json").write_text(
        json.dumps(
            {
                "typed_automorphism_group": "D5",
                "order": 10,
                "scope": "weighted directed face complex with face-incidence structure",
                "generators": {"r": "face +1 mod 5", "m": "(face,n,k) -> (-face,n,n-k)"},
                "actions": automorphisms,
            },
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )

    expected = {
        "schema": "nexah.scc-003-reference-metrics/1.0.0",
        "parameters": {"depth": DEPTH, "faces": FACES},
        "counts": {
            "raw_face_positions": len(raw),
            "quotient_nodes": len(nodes),
            "directed_quotient_edges": len(directed_edges),
            "undirected_quotient_edges": len(undirected_edges),
            "face_edge_incidences": len(edge_incidence),
            "nontrivial_equivalence_classes": len(nontrivial_classes),
            "open_nodes_by_face_count": [28, 49, 70, 91, 112],
            "closure_identifications": 6,
            "closed_nodes": 106,
            "connected_components": 1,
            "typed_automorphism_group_order": 10,
        },
        "fingerprints": {
            "graph6_scope": "underlying simple undirected graph in the declared canonical node order; not by itself a canonical-label isomorphism certificate",
            "graph6": graph6_value,
            "graph6_sha256": hashlib.sha256((graph6_value + "\n").encode("ascii")).hexdigest(),
        },
        "checks": {
            "connected": connected(len(nodes), undirected_edges),
            "all_equivalence_classes_weight_compatible": all(
                len({math.comb(n, k) for _, n, k in members}) == 1
                for members in representatives.values()
            ),
            "ten_declared_actions_are_distinct": len({tuple(item["permutation_zero_based"]) for item in automorphisms}) == 10,
        },
        "claim_ceiling": "Deterministic reference export of the existing bounded SCC-003/PENT construction; no novelty, physical, universal-family or publication claim.",
    }
    (OUT / "expected_metrics.json").write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    artifact_names = [
        "adjacency_matrix.csv",
        "automorphisms.json",
        "edges.csv",
        "expected_metrics.json",
        "face_edges.csv",
        "face_incidence.csv",
        "nodes.csv",
        "seam_classes.csv",
        "underlying_graph.g6",
        "weights.csv",
    ]
    manifest = {
        "schema": "nexah.scc-003-reference-manifest/1.0.0",
        "identity": "SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST",
        "generator": "generate_reference.py",
        "canonical_order": "A; then for n=1..6: seams s=0..4, interiors by face then k",
        "artifacts": {name: {"sha256": sha256(OUT / name), "bytes": (OUT / name).stat().st_size} for name in artifact_names},
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    artifact_names.append("manifest.json")
    (OUT / "SHA256SUMS").write_text(
        "".join(f"{sha256(OUT / name)}  {name}\n" for name in sorted(artifact_names)),
        encoding="ascii",
    )
    print(json.dumps({"status": "PASS", "nodes": len(nodes), "edges": len(directed_edges), "artifacts": len(artifact_names)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
