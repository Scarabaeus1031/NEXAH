#!/usr/bin/env python3
# ==========================================================
# EXP_44Q — ATLAS TRANSPORT SKELETON EXTRACTION
#
# Goal:
# Extract the minimal transport backbone of the Atlas
# while preserving navigation capability.
#
# Pipeline:
#
# Domain Supergraph
#        ↓
# Highway Network
#        ↓
# Transport Skeleton
#
# ==========================================================

import os
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from pathlib import Path

# ==========================================================
# PATHS
# ==========================================================

OUTPUT_DIR = Path(
    "APPLICATIONS/power_systems/FIELD_NAVIGATION_VALIDATION/"
    "outputs/EXP_44Q_TRANSPORT_SKELETON_EXTRACTION"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SUPERGRAPH_PATH = (
    "APPLICATIONS/power_systems/FIELD_NAVIGATION_VALIDATION/"
    "outputs/EXP_44L_DOMAIN_SUPERGRAPH_CONSTRUCTION/"
    "exp44l_domain_supergraph.graphml"
)

# ==========================================================
# LOAD SUPERGRAPH
# ==========================================================

print("\nLoading Domain Supergraph...")

G = nx.read_graphml(SUPERGRAPH_PATH)

print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")

# ==========================================================
# EDGE IMPORTANCE
# ==========================================================

print("\nComputing edge importance...")

edge_betweenness = nx.edge_betweenness_centrality(
    G,
    normalized=True,
    weight="weight"
)

edge_table = []

for (u, v), score in edge_betweenness.items():

    weight = G[u][v].get("weight", 1.0)

    edge_table.append(
        {
            "source": u,
            "target": v,
            "betweenness": score,
            "weight": weight
        }
    )

edge_df = pd.DataFrame(edge_table)
edge_df = edge_df.sort_values(
    "betweenness",
    ascending=False
)

edge_df.to_csv(
    OUTPUT_DIR / "exp44q_skeleton_edges.csv",
    index=False
)

# ==========================================================
# EDGE IMPORTANCE PLOT
# ==========================================================

plt.figure(figsize=(10, 5))

plt.plot(
    np.arange(len(edge_df)),
    edge_df["betweenness"].values
)

plt.title("EXP_44Q Edge Importance Ranking")
plt.xlabel("Edge Rank")
plt.ylabel("Betweenness")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "exp44q_edge_importance.png",
    dpi=300
)
plt.close()

# ==========================================================
# SKELETON EXTRACTION
# ==========================================================

print("\nExtracting transport skeleton...")

TARGET_KEEP = 0.30

n_keep = max(
    G.number_of_nodes() - 1,
    int(len(edge_df) * TARGET_KEEP)
)

selected_edges = edge_df.head(n_keep)

S = nx.Graph()
S.add_nodes_from(G.nodes(data=True))

for _, row in selected_edges.iterrows():

    S.add_edge(
        row["source"],
        row["target"],
        weight=row["weight"],
        betweenness=row["betweenness"]
    )

# ensure connectivity

if not nx.is_connected(S):

    print("Skeleton disconnected -> repairing")

    mst = nx.minimum_spanning_tree(
        nx.Graph(G),
        weight="weight"
    )

    for u, v, data in mst.edges(data=True):

        if not S.has_edge(u, v):

            S.add_edge(u, v, **data)

# ==========================================================
# NAVIGATION PRESERVATION
# ==========================================================

print("\nEvaluating navigation preservation...")

original_lengths = dict(
    nx.all_pairs_shortest_path_length(
        nx.Graph(G)
    )
)

skeleton_lengths = dict(
    nx.all_pairs_shortest_path_length(
        S
    )
)

ratios = []

for a in original_lengths:

    for b in original_lengths[a]:

        if a == b:
            continue

        lo = original_lengths[a][b]
        ls = skeleton_lengths[a][b]

        ratios.append(lo / max(ls, 1))

navigation_preservation = np.mean(ratios)

# ==========================================================
# COMPRESSION CURVE
# ==========================================================

print("\nComputing compression curve...")

fractions = np.linspace(
    0.10,
    1.00,
    10
)

preservation_scores = []

for frac in fractions:

    n_edges = max(
        G.number_of_nodes() - 1,
        int(len(edge_df) * frac)
    )

    H = nx.Graph()
    H.add_nodes_from(G.nodes())

    subset = edge_df.head(n_edges)

    for _, row in subset.iterrows():

        H.add_edge(
            row["source"],
            row["target"]
        )

    if not nx.is_connected(H):

        mst = nx.minimum_spanning_tree(
            nx.Graph(G)
        )

        for u, v in mst.edges():

            H.add_edge(u, v)

    lengths_H = dict(
        nx.all_pairs_shortest_path_length(H)
    )

    local_scores = []

    for a in original_lengths:

        for b in original_lengths[a]:

            if a == b:
                continue

            lo = original_lengths[a][b]
            lh = lengths_H[a][b]

            local_scores.append(
                lo / max(lh, 1)
            )

    preservation_scores.append(
        np.mean(local_scores)
    )

# ==========================================================
# COMPRESSION CURVE PLOT
# ==========================================================

plt.figure(figsize=(8, 5))

plt.plot(
    fractions * 100,
    preservation_scores,
    marker="o"
)

plt.title("EXP_44Q Skeleton Compression")
plt.xlabel("Retained Edges (%)")
plt.ylabel("Navigation Preservation")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp44q_skeleton_compression.png",
    dpi=300
)

plt.close()

# ==========================================================
# TRANSPORT SKELETON VISUAL
# ==========================================================

print("\nRendering skeleton network...")

pos = nx.spring_layout(
    S,
    seed=42
)

plt.figure(figsize=(10, 8))

nx.draw_networkx_nodes(
    S,
    pos,
    node_size=500
)

nx.draw_networkx_edges(
    S,
    pos,
    width=2
)

nx.draw_networkx_labels(
    S,
    pos,
    font_size=8
)

plt.title(
    "EXP_44Q Atlas Transport Skeleton"
)

plt.axis("off")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp44q_transport_skeleton.png",
    dpi=300
)

plt.close()

# ==========================================================
# NAVIGATION PRESERVATION PLOT
# ==========================================================

plt.figure(figsize=(6, 4))

plt.bar(
    ["Skeleton"],
    [navigation_preservation]
)

plt.ylabel("Preservation")

plt.title(
    "EXP_44Q Navigation Preservation"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp44q_navigation_preservation.png",
    dpi=300
)

plt.close()

# ==========================================================
# SAVE GRAPHML
# ==========================================================

nx.write_graphml(
    S,
    OUTPUT_DIR / "atlas_transport_skeleton.graphml"
)

# ==========================================================
# METRICS
# ==========================================================

metrics = {
    "original_edges": G.number_of_edges(),
    "skeleton_edges": S.number_of_edges(),
    "compression_ratio":
        G.number_of_edges() /
        max(S.number_of_edges(), 1),
    "navigation_preservation":
        navigation_preservation,
    "connected_components":
        nx.number_connected_components(S)
}

pd.DataFrame(
    [metrics]
).to_csv(
    OUTPUT_DIR / "exp44q_skeleton_metrics.csv",
    index=False
)

# ==========================================================
# REPORT
# ==========================================================

report = f"""
EXP_44Q TRANSPORT SKELETON EXTRACTION
==================================================

Original Edges
--------------
{G.number_of_edges()}

Skeleton Edges
--------------
{S.number_of_edges()}

Compression Ratio
-----------------
{metrics['compression_ratio']:.2f}

Navigation Preservation
------------------------
{navigation_preservation:.6f}

Connected Components
--------------------
{metrics['connected_components']}

Interpretation
--------------
A sparse transport skeleton was extracted
from the Atlas Domain Supergraph.

Pipeline

Domain Supergraph
 ->
Highway Network
 ->
Transport Skeleton

The experiment evaluates whether Atlas
navigation can be preserved under
aggressive transport compression.
"""

with open(
    OUTPUT_DIR / "exp44q_report.txt",
    "w"
) as f:
    f.write(report)

print("\nEXP_44Q COMPLETE")
print(report)
