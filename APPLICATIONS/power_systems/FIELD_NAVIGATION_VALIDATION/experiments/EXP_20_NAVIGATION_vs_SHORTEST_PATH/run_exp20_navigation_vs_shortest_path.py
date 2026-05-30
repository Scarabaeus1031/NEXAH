"""
run_exp20_navigation_vs_shortest_path.py

EXP_20 — NAVIGATION VS SHORTEST PATH

Goal
-----

Compare NEXAH field navigation against
classical shortest-path routing.

Question:

Does NEXAH provide navigation advantages
beyond standard graph shortest paths?

Input
-----

EXP_08_REAL_FIELD_GEOMETRY
exp08_field_states.csv

Output
------

outputs/EXP_20_NAVIGATION_VS_SHORTEST_PATH/

NEXAH Validation Program
2026
"""

from pathlib import Path

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import networkx as nx
from scipy.spatial import KDTree

# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_DIR = (
    BASE_DIR
    / "outputs"
    / "EXP_08_REAL_FIELD_GEOMETRY"
)

OUTPUT_DIR = (
    BASE_DIR
    / "outputs"
    / "EXP_20_NAVIGATION_VS_SHORTEST_PATH"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print()
print(f"Input  -> {INPUT_DIR}")
print(f"Output -> {OUTPUT_DIR}")
print()

# ============================================================
# Load Data
# ============================================================

df = pd.read_csv(
    INPUT_DIR / "exp08_field_states.csv"
)

Z = df[
    ["pca_x", "pca_y"]
].values

print(
    f"Loaded states: {len(df)}"
)

# ============================================================
# Build Graph
# ============================================================

k = 8

tree = KDTree(Z)

G = nx.Graph()

for i in range(len(Z)):
    G.add_node(i)

for i in range(len(Z)):

    distances, indices = tree.query(
        Z[i],
        k=k + 1
    )

    for d, j in zip(
        distances[1:],
        indices[1:]
    ):
        G.add_edge(
            i,
            j,
            weight=float(d)
        )

largest_component = max(
    nx.connected_components(G),
    key=len
)

G = G.subgraph(
    largest_component
).copy()

valid_nodes = list(G.nodes())

print(
    f"Graph nodes: {G.number_of_nodes()}"
)

print(
    f"Graph edges: {G.number_of_edges()}"
)

# ============================================================
# NEXAH Navigation
# ============================================================

def nexah_navigation(
    graph,
    start,
    goal,
    max_steps=200
):
    """
    Greedy field navigation.
    """

    current = start

    visited = {current}

    for step in range(max_steps):

        if current == goal:
            return True, step

        neighbors = list(
            graph.neighbors(current)
        )

        candidates = []

        for n in neighbors:

            if n in visited:
                continue

            dist = np.linalg.norm(
                Z[n] - Z[goal]
            )

            candidates.append(
                (dist, n)
            )

        if len(candidates) == 0:
            return False, max_steps

        candidates.sort()

        current = candidates[0][1]

        visited.add(current)

    return False, max_steps

# ============================================================
# Experiment
# ============================================================

N_TRIALS = 500

shortest_success = 0
nexah_success = 0

shortest_lengths = []
nexah_lengths = []

for _ in range(N_TRIALS):

    start = random.choice(valid_nodes)
    goal = random.choice(valid_nodes)

    if start == goal:
        continue

    # --------------------------------------------------------
    # Shortest Path
    # --------------------------------------------------------

    try:

        path = nx.shortest_path(
            G,
            start,
            goal,
            weight="weight"
        )

        shortest_success += 1

        shortest_lengths.append(
            len(path)
        )

    except nx.NetworkXNoPath:
        pass

    # --------------------------------------------------------
    # NEXAH Navigation
    # --------------------------------------------------------

    success, steps = nexah_navigation(
        G,
        start,
        goal
    )

    if success:

        nexah_success += 1

        nexah_lengths.append(
            steps
        )

# ============================================================
# Metrics
# ============================================================

shortest_success_rate = (
    shortest_success / N_TRIALS
)

nexah_success_rate = (
    nexah_success / N_TRIALS
)

shortest_avg = (
    np.mean(shortest_lengths)
    if shortest_lengths else 0
)

nexah_avg = (
    np.mean(nexah_lengths)
    if nexah_lengths else 0
)

print()
print(
    f"Shortest Success: {shortest_success_rate:.4f}"
)

print(
    f"NEXAH Success   : {nexah_success_rate:.4f}"
)

print()

print(
    f"Shortest Length : {shortest_avg:.4f}"
)

print(
    f"NEXAH Length    : {nexah_avg:.4f}"
)

print()

# ============================================================
# Save Summary
# ============================================================

summary = OUTPUT_DIR / "exp20_summary.txt"

with open(summary, "w") as f:

    f.write(
        "EXP_20 NAVIGATION VS SHORTEST PATH\n"
    )

    f.write(
        "========================================\n\n"
    )

    f.write(
        f"Shortest Success: {shortest_success_rate:.4f}\n"
    )

    f.write(
        f"NEXAH Success   : {nexah_success_rate:.4f}\n"
    )

    f.write(
        f"Shortest Length : {shortest_avg:.4f}\n"
    )

    f.write(
        f"NEXAH Length    : {nexah_avg:.4f}\n"
    )

# ============================================================
# Plot 1
# ============================================================

plt.figure(figsize=(7, 5))

plt.bar(
    ["Shortest", "NEXAH"],
    [
        shortest_success_rate,
        nexah_success_rate
    ]
)

plt.ylabel("Success Rate")

plt.title(
    "EXP_20 — Navigation Success"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp20_navigation_success.png",
    dpi=300
)

plt.close()

# ============================================================
# Plot 2
# ============================================================

plt.figure(figsize=(7, 5))

plt.bar(
    ["Shortest", "NEXAH"],
    [
        shortest_avg,
        nexah_avg
    ]
)

plt.ylabel("Average Path Length")

plt.title(
    "EXP_20 — Path Efficiency"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp20_path_efficiency.png",
    dpi=300
)

plt.close()

# ============================================================
# Plot 3
# ============================================================

plt.figure(figsize=(8, 7))

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    s=15,
    alpha=0.5
)

plt.title(
    "EXP_20 — Navigation Field"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp20_navigation_field.png",
    dpi=300
)

plt.close()

print()
print("EXP_20 completed.")
print()
