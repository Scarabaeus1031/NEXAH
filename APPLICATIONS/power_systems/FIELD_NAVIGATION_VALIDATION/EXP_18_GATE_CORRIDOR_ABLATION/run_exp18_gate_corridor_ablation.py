"""
run_exp18_gate_corridor_ablation.py

EXP_18 — GATE CORRIDOR ABLATION

Goal
-----
Determine whether the discovered
gate corridor acts as a transport backbone.

Unlike EXP_17, which removed
individual gates, EXP_18 removes
entire gate chains and measures
the resulting degradation.

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
    / "EXP_18_GATE_CORRIDOR_ABLATION"
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

G_main = G.subgraph(
    largest_nodes
).copy()

print(
    f"Largest component: "
    f"{G_main.number_of_nodes()}"
)


# ============================================================
# Gate Corridor
# ============================================================

gate_axis = [
    33,
    81,
    498,
    502
]

print()
print("Gate Corridor:")
print(gate_axis)


# ============================================================
# Baseline Navigation
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

print()
print("Baseline Path:")
print(baseline_path)


# ============================================================
# Corridor Ablation Scenarios
# ============================================================

scenarios = {

    "Gate_33_81":
        [33, 81],

    "Gate_81_498":
        [81, 498],

    "Gate_498_502":
        [498, 502],

    "Main_Corridor":
        [33, 81, 498, 502],

    "All_Gates":
        [33, 81, 184, 250, 498, 502]
}


# ============================================================
# Run Scenarios
# ============================================================

results = []

for scenario_name, removed_nodes in scenarios.items():

    G_test = G_main.copy()

    existing = [
        n for n in removed_nodes
        if n in G_test.nodes
    ]

    G_test.remove_nodes_from(
        existing
    )

    connected_components = nx.number_connected_components(
        G_test
    )

    largest_component = max(
        len(c)
        for c in nx.connected_components(G_test)
    )

    try:

        length = nx.shortest_path_length(
            G_test,
            start_node,
            goal_node,
            weight="weight"
        )

        impact = (
            length
            - baseline_length
        )

        connected = True

    except nx.NetworkXNoPath:

        length = np.nan
        impact = np.nan
        connected = False

    results.append({

        "scenario":
            scenario_name,

        "removed_nodes":
            str(removed_nodes),

        "connected":
            connected,

        "path_length":
            length,

        "impact":
            impact,

        "components":
            connected_components,

        "largest_component":
            largest_component
    })


results_df = pd.DataFrame(
    results
)

print()
print(results_df)


# ============================================================
# Save Results
# ============================================================

results_df.to_csv(
    OUTPUT_DIR
    / "exp18_corridor_ablation_results.csv",
    index=False
)


# ============================================================
# Visual 1
# Navigation Impact
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plt.bar(
    results_df["scenario"],
    results_df["impact"]
)

plt.ylabel(
    "Path Length Increase"
)

plt.title(
    "EXP_18 — Corridor Ablation Impact"
)

plt.xticks(
    rotation=25
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp18_corridor_impact.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Connectivity
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plt.bar(
    results_df["scenario"],
    results_df["components"]
)

plt.ylabel(
    "Connected Components"
)

plt.title(
    "EXP_18 — Connectivity After Corridor Removal"
)

plt.xticks(
    rotation=25
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp18_connectivity.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# Largest Component
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plt.bar(
    results_df["scenario"],
    results_df["largest_component"]
)

plt.ylabel(
    "Largest Component Size"
)

plt.title(
    "EXP_18 — Largest Surviving Component"
)

plt.xticks(
    rotation=25
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp18_largest_component.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 4
# Corridor Geometry
# ============================================================

plt.figure(
    figsize=(10, 8)
)

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    s=12,
    alpha=0.25
)

corridor_nodes = [
    n for n in gate_axis
    if n < len(Z)
]

plt.scatter(
    Z[corridor_nodes, 0],
    Z[corridor_nodes, 1],
    s=220,
    marker="*"
)

for n in corridor_nodes:

    plt.text(
        Z[n, 0],
        Z[n, 1],
        str(n)
    )

plt.title(
    "EXP_18 — Gate Corridor"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp18_gate_corridor.png",
    dpi=300
)

plt.close()


# ============================================================
# Report
# ============================================================

report = f"""
EXP_18 GATE CORRIDOR ABLATION
========================================

States:
{len(Z)}

Baseline Length:
{baseline_length:.6f}

Baseline Nodes:
{len(baseline_path)}

Gate Corridor:
{gate_axis}

Interpretation
----------------------------------------

EXP_17 removed gates individually.

EXP_18 removes entire
transport segments.

Questions:

Does connectivity collapse?

Does navigation cost increase?

Does the field fragment?

This is the first direct test
of corridor-level causality.
"""

with open(
    OUTPUT_DIR
    / "exp18_report.txt",
    "w"
) as f:

    f.write(report)

print()
print("EXP_18 completed.")
print()
