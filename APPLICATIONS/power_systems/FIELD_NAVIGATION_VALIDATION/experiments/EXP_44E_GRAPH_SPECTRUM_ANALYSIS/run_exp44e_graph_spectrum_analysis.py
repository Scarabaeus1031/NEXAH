#!/usr/bin/env python3

"""
EXP_44E
GRAPH SPECTRUM ANALYSIS

Analyse the spectral structure of the reconstructed
NEXAH Atlas graph.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from networkx.algorithms.community import greedy_modularity_communities

# ============================================================
# PATHS
# ============================================================

POWER_ROOT = (
    Path(__file__)
    .resolve()
    .parents[4]
)

OUTPUT_DIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44E_GRAPH_SPECTRUM_ANALYSIS"
)

INPUT_DIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44D_ATLAS_STATE_GRAPH_RECONSTRUCTION"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

GRAPH_FILE = INPUT_DIR / "atlas_state_graph.graphml"

print()
print("Graph  ->", GRAPH_FILE)
print("Exists ->", GRAPH_FILE.exists())
print("Output ->", OUTPUT_DIR)
print()

# ============================================================
# LOAD GRAPH
# ============================================================

G = nx.read_graphml(GRAPH_FILE)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# ============================================================
# ADJACENCY MATRIX
# ============================================================

A = nx.to_numpy_array(G)

adj_eigs = np.linalg.eigvals(A)

adj_real = np.real(adj_eigs)

adj_df = pd.DataFrame({
    "eigenvalue_real": adj_real
})

adj_df.to_csv(
    OUTPUT_DIR / "exp44e_adjacency_spectrum.csv",
    index=False
)

spectral_radius = np.max(np.abs(adj_eigs))

# ============================================================
# LAPLACIAN
# ============================================================

UG = G.to_undirected()

L = nx.laplacian_matrix(UG).astype(float).toarray()

lap_eigs, lap_vecs = np.linalg.eigh(L)

lap_df = pd.DataFrame({
    "eigenvalue": lap_eigs
})

lap_df.to_csv(
    OUTPUT_DIR / "exp44e_laplacian_spectrum.csv",
    index=False
)

# ============================================================
# FIEDLER
# ============================================================

if len(lap_eigs) > 1:
    fiedler_value = float(lap_eigs[1])
    fiedler_vector = lap_vecs[:, 1]
else:
    fiedler_value = 0.0
    fiedler_vector = np.zeros(len(G.nodes()))

# ============================================================
# COMMUNITIES
# ============================================================

communities = list(
    greedy_modularity_communities(UG)
)

community_rows = []

for idx, comm in enumerate(communities):

    community_rows.append({
        "community": idx,
        "size": len(comm)
    })

community_df = pd.DataFrame(community_rows)

community_df.to_csv(
    OUTPUT_DIR / "exp44e_community_summary.csv",
    index=False
)

# ============================================================
# GRAPH METRICS
# ============================================================

metrics = pd.DataFrame([{
    "nodes": G.number_of_nodes(),
    "edges": G.number_of_edges(),
    "spectral_radius": spectral_radius,
    "fiedler_value": fiedler_value,
    "communities": len(communities)
}])

metrics.to_csv(
    OUTPUT_DIR / "exp44e_graph_metrics.csv",
    index=False
)

# ============================================================
# VISUAL 1
# ADJACENCY SPECTRUM
# ============================================================

plt.figure(figsize=(8, 5))

plt.hist(adj_real, bins=30)

plt.title("EXP_44E Adjacency Spectrum")
plt.xlabel("Eigenvalue")
plt.ylabel("Count")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp44e_adjacency_spectrum.png",
    dpi=300
)

plt.close()

# ============================================================
# VISUAL 2
# LAPLACIAN
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    np.arange(len(lap_eigs)),
    lap_eigs,
    marker="o"
)

plt.title("EXP_44E Laplacian Spectrum")
plt.xlabel("Index")
plt.ylabel("Eigenvalue")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp44e_laplacian_spectrum.png",
    dpi=300
)

plt.close()

# ============================================================
# VISUAL 3
# SPECTRAL GAP
# ============================================================

plt.figure(figsize=(6, 4))

vals = lap_eigs[:10]

plt.bar(
    np.arange(len(vals)),
    vals
)

plt.title("EXP_44E Spectral Gap")
plt.xlabel("Eigenvalue Index")
plt.ylabel("Value")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp44e_spectral_gap.png",
    dpi=300
)

plt.close()

# ============================================================
# POSITIONS
# ============================================================

pos = nx.spring_layout(
    UG,
    seed=42
)

# ============================================================
# VISUAL 4
# FIEDLER VECTOR
# ============================================================

plt.figure(figsize=(10, 8))

nx.draw_networkx_nodes(
    UG,
    pos,
    node_size=15,
    node_color=fiedler_vector,
    cmap="viridis"
)

nx.draw_networkx_edges(
    UG,
    pos,
    alpha=0.15
)

plt.title("EXP_44E Fiedler Vector")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp44e_fiedler_vector.png",
    dpi=300
)

plt.close()

# ============================================================
# VISUAL 5
# COMMUNITIES
# ============================================================

community_map = {}

for cid, comm in enumerate(communities):

    for node in comm:
        community_map[node] = cid

node_colors = [
    community_map[n]
    for n in UG.nodes()
]

plt.figure(figsize=(10, 8))

nx.draw_networkx_nodes(
    UG,
    pos,
    node_size=15,
    node_color=node_colors,
    cmap="tab20"
)

nx.draw_networkx_edges(
    UG,
    pos,
    alpha=0.15
)

plt.title("EXP_44E Community Structure")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp44e_community_structure.png",
    dpi=300
)

plt.close()

# ============================================================
# REPORT
# ============================================================

report = f"""
EXP_44E GRAPH SPECTRUM ANALYSIS
==================================================

Nodes
------
{G.number_of_nodes()}

Edges
------
{G.number_of_edges()}

Spectral Radius
---------------
{spectral_radius:.6f}

Fiedler Value
-------------
{fiedler_value:.6f}

Communities
-----------
{len(communities)}

Interpretation
--------------
Graph spectrum analysis reveals:

- dominant graph modes
- transport geometry
- community structure
- connectivity strength

This experiment prepares the direct
comparison between:

Atlas Spectrum
and
Koopman Spectrum.
"""

with open(
    OUTPUT_DIR / "exp44e_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_44E complete.")
print()
print("Spectral Radius :", round(spectral_radius, 6))
print("Fiedler Value   :", round(fiedler_value, 6))
print("Communities     :", len(communities))
print()
