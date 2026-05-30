"""
run_exp18b_gate_usage_mapping.py

EXP_18B — GATE USAGE MAPPING

Goal
-----
Measure how frequently the discovered gate corridor
is used by optimal navigation paths.

Question:

Do shortest paths naturally route through

33
81
498
502

more often than expected?

If yes:

The corridor acts as a preferred transport channel.

Input
-----
EXP_08_REAL_FIELD_GEOMETRY
    exp08_field_states.csv

Output
------
outputs/EXP_18B_GATE_USAGE_MAPPING/

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
    / "EXP_18B_GATE_USAGE_MAPPING"
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
# Load Field
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
# Build Navigation Graph
# ============================================================

k_neighbors = 8

tree = KDTree(Z)

G = nx.Graph()

for i in range(len(Z)):
    G.add_node(i)

for i in range(len(Z)):

    distances, neighbors = tree.query(
        Z[i],
        k=k_neighbors + 1
    )

    for dist, j in zip(
        distances[1:],
        neighbors[1:]
    ):

        G.add_edge(
            i,
            j,
            weight=float(dist)
        )

largest_cc = max(
    nx.connected_components(G),
    key=len
)

G = G.subgraph(
    largest_cc
).copy()

print(
    f"Graph nodes: {G.number_of_nodes()}"
)

print(
    f"Graph edges: {G.number_of_edges()}"
)

print(
    f"Largest component size: {len(G.nodes())}"
)

print()


# ============================================================
# Gate Corridor
# ============================================================

gate_nodes = [
    33,
    81,
    498,
    502
]

print(
    "Gate Corridor:"
)

print(
    gate_nodes
)

print()


# ============================================================
# Sample Navigation Problems
# ============================================================

N_TRIALS = 1000

nodes = list(
    G.nodes()
)

gate_counts = {
    g: 0
    for g in gate_nodes
}

corridor_usage = 0

node_usage = {
    n: 0
    for n in nodes
}

valid_paths = 0

for _ in range(N_TRIALS):

    start, goal = random.sample(
        nodes,
        2
    )

    try:

        path = nx.shortest_path(
            G,
            source=start,
            target=goal,
            weight="weight"
        )

    except nx.NetworkXNoPath:
        continue

    valid_paths += 1

    path_set = set(path)

    corridor_hit = False

    for g in gate_nodes:

        if g in path_set:

            gate_counts[g] += 1
            corridor_hit = True

    if corridor_hit:
        corridor_usage += 1

    for n in path:
        node_usage[n] += 1


print(
    f"Valid paths: {valid_paths}"
)

print()


# ============================================================
# Statistics
# ============================================================

gate_frequency = {
    g: gate_counts[g] / valid_paths
    for g in gate_nodes
}

corridor_frequency = (
    corridor_usage / valid_paths
)

results = pd.DataFrame({

    "gate_node": gate_nodes,

    "usage_count": [
        gate_counts[g]
        for g in gate_nodes
    ],

    "usage_frequency": [
        gate_frequency[g]
        for g in gate_nodes
    ]
})

results.to_csv(
    OUTPUT_DIR /
    "exp18b_gate_usage.csv",
    index=False
)

summary_path = (
    OUTPUT_DIR /
    "exp18b_summary.txt"
)

with open(
    summary_path,
    "w"
) as f:

    f.write(
        "EXP_18B GATE USAGE MAPPING\n"
    )

    f.write(
        "=" * 40 + "\n\n"
    )

    f.write(
        f"Valid Paths: {valid_paths}\n\n"
    )

    for g in gate_nodes:

        f.write(
            f"Gate {g}: "
            f"{gate_frequency[g]:.4f}\n"
        )

    f.write("\n")

    f.write(
        f"Corridor Usage: "
        f"{corridor_frequency:.4f}\n"
    )


print(results)
print()

print(
    f"Corridor Usage: "
    f"{corridor_frequency:.4f}"
)

print()


# ============================================================
# Visual 1
# Gate Frequency
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.bar(
    [str(g) for g in gate_nodes],
    [gate_frequency[g] for g in gate_nodes]
)

plt.ylabel(
    "Usage Frequency"
)

plt.title(
    "EXP_18B — Gate Usage Frequency"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp18b_gate_usage_frequency.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Corridor Participation
# ============================================================

plt.figure(
    figsize=(6, 5)
)

plt.bar(
    ["Corridor", "No Corridor"],
    [
        corridor_frequency,
        1 - corridor_frequency
    ]
)

plt.ylabel(
    "Fraction of Paths"
)

plt.title(
    "EXP_18B — Corridor Participation"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp18b_corridor_participation.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# Field Usage Heat
# ============================================================

usage_values = np.array([
    node_usage[n]
    for n in nodes
])

plt.figure(
    figsize=(10, 7)
)

plt.scatter(
    Z[nodes, 0],
    Z[nodes, 1],
    c=usage_values,
    s=20,
    alpha=0.8
)

plt.colorbar(
    label="Path Usage Count"
)

plt.scatter(
    df.loc[gate_nodes, "pca_x"],
    df.loc[gate_nodes, "pca_y"],
    marker="*",
    s=400
)

for g in gate_nodes:

    x = df.loc[g, "pca_x"]
    y = df.loc[g, "pca_y"]

    plt.text(
        x,
        y,
        str(g)
    )

plt.title(
    "EXP_18B — Field Usage Heatmap"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp18b_field_usage_heatmap.png",
    dpi=300
)

plt.close()


print(
    "EXP_18B completed."
)
