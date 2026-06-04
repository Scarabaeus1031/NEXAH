#!/usr/bin/env python3

"""
EXP_44D — ATLAS STATE GRAPH RECONSTRUCTION
==================================================

Objective
---------
Reconstruct a directed state graph from
the discovered NEXAH atlas states.

Primary Dataset
---------------
EXP_34_CONTROL_EFFORT_ESTIMATION

Outputs
-------
exp44d_state_graph_nodes.csv
exp44d_state_graph_edges.csv
exp44d_graph_metrics.csv
exp44d_backbone_nodes.csv
exp44d_report.txt

Visuals
-------
exp44d_state_graph.png
exp44d_degree_distribution.png
exp44d_backbone_structure.png
exp44d_basin_connectivity.png
"""

from pathlib import Path

import pandas as pd
import numpy as np

import networkx as nx

import matplotlib.pyplot as plt

from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


# ==========================================================
# PATHS
# ==========================================================

POWER_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
)

OUTPUT_DIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44D_ATLAS_STATE_GRAPH_RECONSTRUCTION"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DATASET = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_34_CONTROL_EFFORT_ESTIMATION"
    / "exp34_control_effort_table.csv"
)

print("Dataset ->", DATASET)
print("Exists  ->", DATASET.exists())
print("Output  ->", OUTPUT_DIR)


# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv(DATASET)

print()
print("Rows:", len(df))
print("Cols:", len(df.columns))


# ==========================================================
# FEATURES
# ==========================================================

candidate_features = [
    "PC1",
    "PC2",
    "warning_index",
    "exit_risk",
    "recovery_length",
    "control_effort",
    "basin_distance",
    "axis_distance",
]

features = [c for c in candidate_features if c in df.columns]

print()
print("Features:")
for f in features:
    print(" -", f)

X = df[features].copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# ==========================================================
# KNN GRAPH
# ==========================================================

K = 5

nn = NearestNeighbors(
    n_neighbors=K + 1,
    metric="euclidean"
)

nn.fit(X_scaled)

distances, indices = nn.kneighbors(X_scaled)

G = nx.DiGraph()

for idx in range(len(df)):

    G.add_node(idx)

    for neighbor in indices[idx][1:]:

        G.add_edge(idx, int(neighbor))

print()
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())


# ==========================================================
# NODE TABLE
# ==========================================================

nodes = pd.DataFrame({
    "node_id": range(len(df))
})

if "basin" in df.columns:
    nodes["basin"] = df["basin"]

nodes.to_csv(
    OUTPUT / "exp44d_state_graph_nodes.csv",
    index=False
)


# ==========================================================
# EDGE TABLE
# ==========================================================

edge_rows = []

for u, v in G.edges():
    edge_rows.append([u, v])

edges = pd.DataFrame(
    edge_rows,
    columns=["source", "target"]
)

edges.to_csv(
    OUTPUT / "exp44d_state_graph_edges.csv",
    index=False
)


# ==========================================================
# GRAPH METRICS
# ==========================================================

degree = dict(G.degree())
betweenness = nx.betweenness_centrality(G)

try:
    eigenvector = nx.eigenvector_centrality(
        G,
        max_iter=1000
    )
except:
    eigenvector = {n: 0 for n in G.nodes()}

metrics = pd.DataFrame({
    "node_id": list(G.nodes()),
    "degree": [degree[n] for n in G.nodes()],
    "betweenness": [betweenness[n] for n in G.nodes()],
    "eigenvector": [eigenvector[n] for n in G.nodes()],
})

metrics.to_csv(
    OUTPUT / "exp44d_graph_metrics.csv",
    index=False
)


# ==========================================================
# BACKBONE NODES
# ==========================================================

threshold = metrics["betweenness"].quantile(0.95)

backbone = metrics[
    metrics["betweenness"] >= threshold
]

backbone.to_csv(
    OUTPUT / "exp44d_backbone_nodes.csv",
    index=False
)

print()
print("Backbone Nodes:", len(backbone))


# ==========================================================
# VISUAL 1
# ==========================================================

plt.figure(figsize=(10, 8))

pos = nx.spring_layout(
    G,
    seed=42
)

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=12
)

nx.draw_networkx_edges(
    G,
    pos,
    alpha=0.15,
    width=0.3
)

plt.title("EXP_44D Atlas State Graph")

plt.axis("off")

plt.tight_layout()

plt.savefig(
    OUTPUT / "exp44d_state_graph.png",
    dpi=300
)

plt.close()


# ==========================================================
# VISUAL 2
# ==========================================================

plt.figure(figsize=(8, 5))

plt.hist(
    metrics["degree"],
    bins=20
)

plt.title("EXP_44D Degree Distribution")

plt.xlabel("Degree")
plt.ylabel("Count")

plt.tight_layout()

plt.savefig(
    OUTPUT / "exp44d_degree_distribution.png",
    dpi=300
)

plt.close()


# ==========================================================
# VISUAL 3
# ==========================================================

plt.figure(figsize=(8, 5))

plt.scatter(
    metrics["degree"],
    metrics["betweenness"],
    s=15
)

plt.xlabel("Degree")
plt.ylabel("Betweenness")

plt.title("EXP_44D Backbone Structure")

plt.tight_layout()

plt.savefig(
    OUTPUT / "exp44d_backbone_structure.png",
    dpi=300
)

plt.close()


# ==========================================================
# VISUAL 4
# ==========================================================

if "basin" in df.columns:

    basin_counts = (
        df["basin"]
        .value_counts()
        .sort_index()
    )

    plt.figure(figsize=(10, 5))

    basin_counts.plot(kind="bar")

    plt.title(
        "EXP_44D Basin Connectivity Overview"
    )

    plt.xlabel("Basin")
    plt.ylabel("States")

    plt.tight_layout()

    plt.savefig(
        OUTPUT / "exp44d_basin_connectivity.png",
        dpi=300
    )

    plt.close()


# ==========================================================
# REPORT
# ==========================================================

report = f"""
EXP_44D ATLAS STATE GRAPH RECONSTRUCTION
==================================================

States
------
{G.number_of_nodes()}

Edges
-----
{G.number_of_edges()}

Backbone Nodes
--------------
{len(backbone)}

Features Used
-------------
{", ".join(features)}

Interpretation
--------------
Atlas states were transformed into a
directed nearest-neighbor graph.

The resulting graph provides the first
graph-theoretic representation of the
NEXAH Atlas and enables future:

- transition reconstruction
- transport analysis
- spectral analysis
- Koopman comparison
- navigation experiments
"""

with open(
    OUTPUT / "exp44d_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_44D complete.")
print()
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print("Backbone Nodes:", len(backbone))
