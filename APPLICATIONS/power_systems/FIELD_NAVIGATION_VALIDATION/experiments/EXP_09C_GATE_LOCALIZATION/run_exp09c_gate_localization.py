"""
run_exp09c_gate_localization.py

EXP_09C — GATE LOCALIZATION

Goal:
Localize and characterize the gate nodes discovered in EXP_09B.

Questions:

- Where are the gates located?
- Are 498 and 502 neighbors?
- Do gates sit on corridor structures?
- Do gates connect distinct field regions?

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
    / "EXP_09C_GATE_LOCALIZATION"
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
# Rebuild kNN Graph
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
# Betweenness
# ============================================================

print(
    "Computing betweenness..."
)

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

threshold = np.percentile(
    bet_arr,
    99
)

gate_nodes = component_nodes[
    bet_arr >= threshold
]

print(
    f"Gate nodes: {len(gate_nodes)}"
)

print(
    f"Gate list: {list(gate_nodes)}"
)


# ============================================================
# Gate Coordinates
# ============================================================

gate_records = []

for gate in gate_nodes:

    gate_records.append({
        "gate_node": gate,
        "pca_x": Z[gate, 0],
        "pca_y": Z[gate, 1],
        "betweenness": bet[gate],
        "degree": G.degree(gate)
    })

gate_df = pd.DataFrame(
    gate_records
)

gate_df.to_csv(
    OUTPUT_DIR /
    "exp09c_gate_coordinates.csv",
    index=False
)


# ============================================================
# Pairwise Distances
# ============================================================

pairs = []

for i in range(len(gate_nodes)):

    for j in range(i + 1, len(gate_nodes)):

        g1 = gate_nodes[i]
        g2 = gate_nodes[j]

        d = np.linalg.norm(
            Z[g1] - Z[g2]
        )

        pairs.append({
            "gate_a": g1,
            "gate_b": g2,
            "distance": d
        })

pair_df = pd.DataFrame(
    pairs
)

pair_df = pair_df.sort_values(
    "distance"
)

pair_df.to_csv(
    OUTPUT_DIR /
    "exp09c_gate_distances.csv",
    index=False
)

print()
print("Closest Gate Pairs")
print(pair_df.head())
print()


# ============================================================
# Neighbor Overlap
# ============================================================

neighbor_records = []

for gate in gate_nodes:

    neighbors = set(
        G.neighbors(gate)
    )

    neighbor_records.append({
        "gate_node": gate,
        "neighbors": len(neighbors)
    })

neighbor_df = pd.DataFrame(
    neighbor_records
)

neighbor_df.to_csv(
    OUTPUT_DIR /
    "exp09c_gate_neighbors.csv",
    index=False
)


# ============================================================
# Visual 1
# ============================================================

plt.figure(
    figsize=(12, 10)
)

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    color="lightgray",
    s=15
)

plt.scatter(
    Z[gate_nodes, 0],
    Z[gate_nodes, 1],
    s=250,
    color="red"
)

for gate in gate_nodes:

    plt.annotate(
        str(gate),
        (
            Z[gate, 0],
            Z[gate, 1]
        )
    )

plt.title(
    "EXP_09C — Gate Localization"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp09c_gate_localization.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# ============================================================

plt.figure(
    figsize=(12, 10)
)

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    color="lightgray",
    s=15
)

for gate in gate_nodes:

    neighbors = list(
        G.neighbors(gate)
    )

    plt.scatter(
        Z[neighbors, 0],
        Z[neighbors, 1],
        s=20,
        alpha=0.5
    )

plt.scatter(
    Z[gate_nodes, 0],
    Z[gate_nodes, 1],
    s=300,
    color="red"
)

plt.title(
    "EXP_09C — Gate Neighborhoods"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp09c_gate_neighborhoods.png",
    dpi=300
)

plt.close()


# ============================================================
# Report
# ============================================================

closest_pair = pair_df.iloc[0]

report = f"""
EXP_09C GATE LOCALIZATION
========================================

Gate Nodes:
{len(gate_nodes)}

Gate List:
{list(gate_nodes)}

Closest Gate Pair:
{int(closest_pair.gate_a)}
<-> 
{int(closest_pair.gate_b)}

Distance:
{closest_pair.distance:.6f}

Purpose
----------------------------------------

Determine whether gate nodes:

1. Cluster together

2. Form corridor structures

3. Occupy transition regions

4. Connect distinct field regimes
"""

with open(
    OUTPUT_DIR /
    "exp09c_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_09C completed.")
print()
