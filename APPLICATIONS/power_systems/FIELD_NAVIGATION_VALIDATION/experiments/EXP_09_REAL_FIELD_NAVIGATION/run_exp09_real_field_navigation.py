"""
run_exp09_real_field_navigation.py

EXP_09 — REAL FIELD NAVIGATION

Goal:
Test whether navigation through the real IEEE39
state-space can exploit gate structures discovered
in EXP_08.

NEXAH Validation Program
2026
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


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
    / "EXP_09_REAL_FIELD_NAVIGATION"
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
# Load EXP_08 Results
# ============================================================

df = pd.read_csv(
    INPUT_DIR / "exp08_field_states.csv"
)

print(
    f"Loaded states: {len(df)}"
)

Z = df[
    ["pca_x", "pca_y"]
].values


# ============================================================
# Rebuild Field Graph
# ============================================================

from sklearn.neighbors import NearestNeighbors

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
# Gate Candidates
# ============================================================

bet = nx.betweenness_centrality(
    G,
    normalized=True
)

bet_arr = np.array(
    [bet[i] for i in range(len(Z))]
)

gate_threshold = np.percentile(
    bet_arr,
    99
)

gate_nodes = np.where(
    bet_arr >= gate_threshold
)[0]

print(
    f"Gate nodes: {len(gate_nodes)}"
)


# ============================================================
# Connected Components
# ============================================================

components = list(
    nx.connected_components(G)
)

print(
    f"Connected components: "
    f"{len(components)}"
)

largest_component = max(
    components,
    key=len
)

largest_component = np.array(
    list(largest_component)
)

print(
    f"Largest component size: "
    f"{len(largest_component)}"
)


# ============================================================
# Start / Goal Selection
# ============================================================

component_x = Z[
    largest_component,
    0
]

start_idx = largest_component[
    np.argmin(component_x)
]

goal_idx = largest_component[
    np.argmax(component_x)
]

print(
    f"Start node: {start_idx}"
)

print(
    f"Goal node: {goal_idx}"
)

assert nx.has_path(
    G,
    start_idx,
    goal_idx
)

# ============================================================
# Shortest Path
# ============================================================

shortest_path = nx.shortest_path(
    G,
    source=start_idx,
    target=goal_idx,
    weight="weight"
)

shortest_length = nx.path_weight(
    G,
    shortest_path,
    weight="weight"
)

print(
    f"Shortest path length: "
    f"{shortest_length:.4f}"
)

print(
    f"Shortest path nodes: "
    f"{len(shortest_path)}"
)

# ============================================================
# Gate-Aware Graph
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


gate_path = nx.shortest_path(
    G_gate,
    source=start_idx,
    target=goal_idx,
    weight="nav_weight"
)

gate_length = nx.path_weight(
    G_gate,
    gate_path,
    weight="nav_weight"
)

print(
    f"Gate path length: "
    f"{gate_length:.4f}"
)


# ============================================================
# Visual 1
# ============================================================

plt.figure(
    figsize=(10, 8)
)

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    color="lightgray",
    s=15
)

sp = np.array(
    [Z[i] for i in shortest_path]
)

plt.plot(
    sp[:, 0],
    sp[:, 1],
    linewidth=3,
    label="Shortest Path"
)

plt.scatter(
    Z[start_idx, 0],
    Z[start_idx, 1],
    s=150,
    marker="o",
    label="Start"
)

plt.scatter(
    Z[goal_idx, 0],
    Z[goal_idx, 1],
    s=150,
    marker="*",
    label="Goal"
)

plt.legend()

plt.title(
    "EXP_09 — Shortest Navigation"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp09_shortest_path.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# ============================================================

plt.figure(
    figsize=(10, 8)
)

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    color="lightgray",
    s=15
)

gp = np.array(
    [Z[i] for i in gate_path]
)

plt.plot(
    gp[:, 0],
    gp[:, 1],
    linewidth=3,
    label="Gate Navigation"
)

plt.scatter(
    Z[gate_nodes, 0],
    Z[gate_nodes, 1],
    s=120,
    label="Gate Nodes"
)

plt.scatter(
    Z[start_idx, 0],
    Z[start_idx, 1],
    s=150,
    marker="o"
)

plt.scatter(
    Z[goal_idx, 0],
    Z[goal_idx, 1],
    s=150,
    marker="*"
)

plt.legend()

plt.title(
    "EXP_09 — Gate Navigation"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp09_gate_navigation.png",
    dpi=300
)

plt.close()


# ============================================================
# Metrics
# ============================================================

metrics = pd.DataFrame({
    "metric": [
        "shortest_length",
        "gate_length",
        "gate_nodes"
    ],
    "value": [
        shortest_length,
        gate_length,
        len(gate_nodes)
    ]
})

metrics.to_csv(
    OUTPUT_DIR /
    "exp09_path_metrics.csv",
    index=False
)


# ============================================================
# Report
# ============================================================

report = f"""
EXP_09 REAL FIELD NAVIGATION
========================================

States:
{len(Z)}

Gate Nodes:
{len(gate_nodes)}

Shortest Path Length:
{shortest_length:.6f}

Gate Path Length:
{gate_length:.6f}
"""

with open(
    OUTPUT_DIR /
    "exp09_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_09 completed.")
print()

report = f"""
EXP_09 REAL FIELD NAVIGATION
========================================

States:
{len(Z)}

Gate Nodes:
{len(gate_nodes)}

Shortest Path Length:
{shortest_length:.6f}

Gate Path Length:
{gate_length:.6f}
"""
