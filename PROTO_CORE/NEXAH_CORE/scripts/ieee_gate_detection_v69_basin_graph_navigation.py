# ============================================================
# NEXAH — IEEE GATE DETECTION v69
# Basin Graph + Gate Navigation
# ============================================================
#
# PURPOSE:
# --------
# Build graph from v68 basins + saddles and compute navigation paths
#
# OUTPUT:
# --------
# v69_basin_graph.txt
# v69_shortest_paths.txt
#
# ============================================================

import os
import sys
import numpy as np
import heapq

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

# ------------------------------------------------------------
# LOAD v68 DATA MANUALLY (paste from summary or reuse pipeline)
# ------------------------------------------------------------

basins = [
    {"id": 0, "r": 0.8715, "theta": 0.6494},
    {"id": 1, "r": 0.9310, "theta": -2.3343},
    {"id": 2, "r": 1.8223, "theta": 2.6151},
    {"id": 3, "r": 1.6242, "theta": -1.3514},
    {"id": 4, "r": 1.7431, "theta": 0.5090},
]

gates = [
    (0, 1, 0.0482),
    (2, 3, 0.0401),
    (1, 2, 0.0341),
    (3, 4, 0.0253),
    (1, 4, 0.0191),
    (2, 4, 0.0190),
    (0, 2, 0.0171),
    (0, 3, 0.0150),
    (0, 4, 0.0104),
    (1, 3, 0.0017),
]

# ------------------------------------------------------------
# Build Graph
# ------------------------------------------------------------

def build_graph(gates):

    graph = {}

    for a, b, w in gates:

        graph.setdefault(a, []).append((b, w))
        graph.setdefault(b, []).append((a, w))

    return graph


# ------------------------------------------------------------
# Dijkstra shortest path
# ------------------------------------------------------------

def shortest_path(graph, start, end):

    queue = [(0, start, [])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)

        if node in visited:
            continue

        path = path + [node]
        visited.add(node)

        if node == end:
            return cost, path

        for neighbor, weight in graph.get(node, []):
            heapq.heappush(queue, (cost + weight, neighbor, path))

    return None, []


# ------------------------------------------------------------
# Rank gates
# ------------------------------------------------------------

def rank_gates(gates):

    return sorted(gates, key=lambda x: x[2])  # low barrier = easy


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    graph = build_graph(gates)

    # --------------------------------------------------------
    # Compute all shortest paths
    # --------------------------------------------------------

    paths = []

    for i in range(len(basins)):
        for j in range(len(basins)):
            if i != j:
                cost, path = shortest_path(graph, i, j)
                paths.append((i, j, cost, path))

    # --------------------------------------------------------
    # Rank gates
    # --------------------------------------------------------

    ranked = rank_gates(gates)

    # --------------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------------

    graph_path = os.path.join(OUT_DIR, "v69_basin_graph.txt")

    with open(graph_path, "w") as f:

        f.write("NEXAH v69 — Basin Graph\n")
        f.write("========================\n\n")

        for node, edges in graph.items():
            f.write(f"B{node}:\n")
            for e in edges:
                f.write(f"  -> B{e[0]} (barrier={e[1]:.4f})\n")
            f.write("\n")

    path_path = os.path.join(OUT_DIR, "v69_shortest_paths.txt")

    with open(path_path, "w") as f:

        f.write("NEXAH v69 — Shortest Paths\n")
        f.write("===========================\n\n")

        for i, j, cost, path in paths:
            f.write(f"B{i} -> B{j} | cost={cost:.4f} | path={path}\n")

    rank_path = os.path.join(OUT_DIR, "v69_gate_ranking.txt")

    with open(rank_path, "w") as f:

        f.write("NEXAH v69 — Gate Ranking (low barrier first)\n")
        f.write("============================================\n\n")

        for a, b, w in ranked:
            f.write(f"B{a} <-> B{b} | barrier={w:.4f}\n")

    print("NEXAH v69 complete")
    print(f"Saved: {graph_path}")
    print(f"Saved: {path_path}")
    print(f"Saved: {rank_path}")
