"""
run_exp09b_gate_importance.py

EXP_09B — GATE IMPORTANCE

Goal:
Measure which gate nodes contribute most to field-navigation efficiency.

Method:
1. Load EXP_08 field states
2. Rebuild kNN graph
3. Detect gate nodes by betweenness
4. Compute baseline gate-aware path
5. Remove each gate individually
6. Recompute navigation path
7. Rank gates by contribution

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
    / "EXP_09B_GATE_IMPORTANCE"
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
# Load EXP_08 field states
# ============================================================

df = pd.read_csv(
    INPUT_DIR / "exp08_field_states.csv"
)

Z = df[
    ["pca_x", "pca_y"]
].values

print(f"Loaded states: {len(Z)}")


# ============================================================
# Rebuild kNN graph
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

    for j in indices[i][1:]:

        d = np.linalg.norm(
            Z[i] - Z[j]
        )

        G.add_edge(
            i,
            j,
            weight=d
        )

print(
    f"Graph nodes: {G.number_of_nodes()}"
)

print(
    f"Graph edges: {G.number_of_edges()}"
)


# ============================================================
# Largest Connected Component
# ============================================================

components = list(
    nx.connected_components(G)
)

largest_component = max(
    components,
    key=len
)

G = G.subgraph(
    largest_component
).copy()

component_nodes = np.array(
    sorted(G.nodes())
)

print(
    f"Largest component size: "
    f"{len(component_nodes)}"
)


# ============================================================
# Gate Detection
# ============================================================

bet = nx.betweenness_centrality(
    G,
    normalized=True
)

bet_arr = np.array(
    [
        bet[n]
        for n in component_nodes
    ]
)

gate_threshold = np.percentile(
    bet_arr,
    99
)

gate_nodes = component_nodes[
    bet_arr >= gate_threshold
]

print(
    f"Gate nodes: {len(gate_nodes)}"
)


# ============================================================
# Start / Goal
# ============================================================

comp_Z = Z[component_nodes]

start_local = np.argmin(
    comp_Z[:, 0]
)

goal_local = np.argmax(
    comp_Z[:, 0]
)

start_idx = component_nodes[
    start_local
]

goal_idx = component_nodes[
    goal_local
]

print(
    f"Start node: {start_idx}"
)

print(
    f"Goal node: {goal_idx}"
)


# ============================================================
# Build Gate-Aware Graph
# ============================================================

G_gate = G.copy()

for u, v in G_gate.edges():

    w = G_gate[u][v]["weight"]

    bonus = 1.0

    if u in gate_nodes:
        bonus *= 0.5

    if v in gate_nodes:
        bonus *= 0.5

    G_gate[u][v]["nav_weight"] = (
        w * bonus
    )


baseline_path = nx.shortest_path(
    G_gate,
    source=start_idx,
    target=goal_idx,
    weight="nav_weight"
)

baseline_length = nx.path_weight(
    G_gate,
    baseline_path,
    weight="nav_weight"
)

print(
    f"Baseline gate path: "
    f"{baseline_length:.4f}"
)


# ============================================================
# Gate Importance Analysis
# ============================================================

results = []

for gate in gate_nodes:

    G_test = G_gate.copy()

    if gate not in G_test:
        continue

    G_test.remove_node(gate)

    if (
        start_idx not in G_test
        or goal_idx not in G_test
    ):
        continue

    try:

        path = nx.shortest_path(
            G_test,
            source=start_idx,
            target=goal_idx,
            weight="nav_weight"
        )

        length = nx.path_weight(
            G_test,
            path,
            weight="nav_weight"
        )

        delta = (
            length
            - baseline_length
        )

        results.append({
            "gate_node": gate,
            "path_length": length,
            "impact": delta
        })

    except nx.NetworkXNoPath:

        results.append({
            "gate_node": gate,
            "path_length": np.nan,
            "impact": np.inf
        })


# ============================================================
# Ranking
# ============================================================

importance_df = pd.DataFrame(
    results
)

importance_df = (
    importance_df
    .sort_values(
        "impact",
        ascending=False
    )
)

importance_df.to_csv(
    OUTPUT_DIR /
    "exp09b_gate_importance.csv",
    index=False
)

print()
print("Gate Ranking")
print(
    importance_df.head(10)
)
print()


# ============================================================
# Visual
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plot_df = (
    importance_df
    .replace(
        np.inf,
        np.nan
    )
    .dropna()
)

plt.bar(
    plot_df["gate_node"].astype(str),
    plot_df["impact"]
)

plt.title(
    "EXP_09B — Gate Importance"
)

plt.xlabel(
    "Gate Node"
)

plt.ylabel(
    "Navigation Cost Increase"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp09b_gate_importance.png",
    dpi=300
)

plt.close()


# ============================================================
# Report
# ============================================================

top_gate = (
    importance_df.iloc[0]
)

report = f"""
EXP_09B GATE IMPORTANCE
========================================

Gate Nodes:
{len(gate_nodes)}

Baseline Gate Path:
{baseline_length:.6f}

Most Important Gate:
{int(top_gate.gate_node)}

Impact:
{top_gate.impact}

Interpretation
----------------------------------------

Higher impact means:

Removing the gate increases
navigation cost.

Very high impact suggests:

    bottleneck

    corridor controller

    transport bridge

Potential NEXAH Gate Candidate.
"""

with open(
    OUTPUT_DIR /
    "exp09b_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_09B completed.")
print()
