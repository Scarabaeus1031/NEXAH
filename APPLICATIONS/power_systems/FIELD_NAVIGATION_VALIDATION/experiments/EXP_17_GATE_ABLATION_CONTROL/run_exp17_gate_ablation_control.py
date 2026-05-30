"""
run_exp17_gate_ablation_control.py

EXP_17 — GATE ABLATION CONTROL

Goal
-----
Determine whether the discovered gate nodes are
causally responsible for navigation performance
and field connectivity.

Method
------
1. Load EXP_08 field states
2. Reconstruct field graph
3. Compute baseline navigation
4. Remove gates one by one
5. Recompute navigation
6. Measure degradation

NEXAH Validation Program
2026
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from sklearn.neighbors import NearestNeighbors


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
    / "EXP_17_GATE_ABLATION_CONTROL"
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
# Load Field States
# ============================================================

df = pd.read_csv(
    INPUT_DIR / "exp08_field_states.csv"
)

Z = df[
    ["pca_x", "pca_y"]
].values

print(
    f"Loaded states: {len(Z)}"
)


# ============================================================
# Build Graph
# ============================================================

K = 12

nbrs = NearestNeighbors(
    n_neighbors=K
)

nbrs.fit(Z)

distances, indices = nbrs.kneighbors(Z)

G = nx.Graph()

for i in range(len(Z)):
    G.add_node(i)

for i in range(len(Z)):

    for j, d in zip(
        indices[i][1:],
        distances[i][1:]
    ):

        G.add_edge(
            i,
            j,
            weight=float(d)
        )

print(
    f"Graph nodes: {G.number_of_nodes()}"
)

print(
    f"Graph edges: {G.number_of_edges()}"
)


# ============================================================
# Largest Component
# ============================================================

largest_nodes = max(
    nx.connected_components(G),
    key=len
)

largest_nodes = set(
    largest_nodes
)

G_main = G.subgraph(
    largest_nodes
).copy()

print(
    f"Largest component size: "
    f"{len(largest_nodes)}"
)


# ============================================================
# Gate Nodes
# ============================================================

gate_nodes = [
    33,
    81,
    184,
    250,
    498,
    502
]

gate_nodes = [
    g for g in gate_nodes
    if g in G_main.nodes
]

print()
print("Gate nodes:")
print(gate_nodes)


# ============================================================
# Start / Goal
# ============================================================

bet = nx.betweenness_centrality(
    G_main,
    normalized=True
)

sorted_nodes = sorted(
    bet,
    key=bet.get
)

start_node = sorted_nodes[20]
goal_node = sorted_nodes[-20]

print()
print(f"Start node: {start_node}")
print(f"Goal node : {goal_node}")


# ============================================================
# Baseline Path
# ============================================================

baseline_length = nx.shortest_path_length(
    G_main,
    start_node,
    goal_node,
    weight="weight"
)

baseline_path = nx.shortest_path(
    G_main,
    start_node,
    goal_node,
    weight="weight"
)

print()
print(
    f"Baseline path length: "
    f"{baseline_length:.4f}"
)

print(
    f"Baseline path nodes: "
    f"{len(baseline_path)}"
)


# ============================================================
# Gate Ablation
# ============================================================

results = []

for gate in gate_nodes:

    G_test = G_main.copy()

    if gate in G_test:
        G_test.remove_node(gate)

    try:

        length = nx.shortest_path_length(
            G_test,
            start_node,
            goal_node,
            weight="weight"
        )

        connected = True

        impact = (
            length
            - baseline_length
        )

    except nx.NetworkXNoPath:

        length = np.nan
        impact = np.nan
        connected = False

    component_count = nx.number_connected_components(
        G_test
    )

    largest_size = max(
        len(c)
        for c in nx.connected_components(G_test)
    )

    results.append({

        "gate_node": gate,

        "connected":
            connected,

        "path_length":
            length,

        "impact":
            impact,

        "components":
            component_count,

        "largest_component":
            largest_size
    })

results_df = pd.DataFrame(
    results
)

results_df = results_df.sort_values(
    "impact",
    ascending=False
)

print()
print("Gate Ablation Results")
print(results_df)


# ============================================================
# Save Results
# ============================================================

results_df.to_csv(
    OUTPUT_DIR
    / "exp17_gate_ablation_results.csv",
    index=False
)


# ============================================================
# Visual 1
# Gate Impact Ranking
# ============================================================

plt.figure(
    figsize=(8, 6)
)

plt.bar(
    results_df["gate_node"].astype(str),
    results_df["impact"]
)

plt.ylabel(
    "Path Length Increase"
)

plt.xlabel(
    "Removed Gate"
)

plt.title(
    "EXP_17 — Gate Impact Ranking"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp17_gate_impact_ranking.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Connectivity Impact
# ============================================================

plt.figure(
    figsize=(8, 6)
)

plt.bar(
    results_df["gate_node"].astype(str),
    results_df["components"]
)

plt.ylabel(
    "Connected Components"
)

plt.xlabel(
    "Removed Gate"
)

plt.title(
    "EXP_17 — Connectivity Impact"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp17_connectivity_impact.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# Largest Component
# ============================================================

plt.figure(
    figsize=(8, 6)
)

plt.bar(
    results_df["gate_node"].astype(str),
    results_df["largest_component"]
)

plt.ylabel(
    "Largest Component Size"
)

plt.xlabel(
    "Removed Gate"
)

plt.title(
    "EXP_17 — Largest Component After Ablation"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp17_largest_component.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 4
# Gate Map
# ============================================================

plt.figure(
    figsize=(10, 8)
)

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    s=12,
    alpha=0.3
)

plt.scatter(
    Z[gate_nodes, 0],
    Z[gate_nodes, 1],
    s=180,
    marker="*"
)

for g in gate_nodes:

    plt.text(
        Z[g, 0],
        Z[g, 1],
        str(g)
    )

plt.title(
    "EXP_17 — Gate Locations"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp17_gate_locations.png",
    dpi=300
)

plt.close()


# ============================================================
# Report
# ============================================================

top_gate = results_df.iloc[0]

report = f"""
EXP_17 GATE ABLATION CONTROL
========================================

States:
{len(Z)}

Baseline Path Length:
{baseline_length:.6f}

Gate Nodes:
{gate_nodes}

Most Critical Gate:
{int(top_gate['gate_node'])}

Impact:
{top_gate['impact']:.6f}

Interpretation
----------------------------------------

Ablation removes one gate
at a time and recomputes
navigation performance.

Large impact indicates:

    causal importance

for transport.

Small impact indicates:

    redundant structure

or secondary importance.

This is the first direct
causal test of gate function.
"""

with open(
    OUTPUT_DIR
    / "exp17_report.txt",
    "w"
) as f:

    f.write(report)

print()
print("EXP_17 completed.")
print()
