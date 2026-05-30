# ============================================================
# EXP_25 — BASIN TRANSITION GRAPH
#
# Question:
# How are the attractor basins discovered in EXP_24E
# connected to each other?
#
# Goal:
# Build the first NEXAH State-Space Atlas:
#
#     Basin A -> Basin B -> Basin C
#
# Inputs:
#   EXP_08_REAL_FIELD_GEOMETRY / exp08_field_states.csv
#
# Outputs:
#   exp25_basin_transition_network.png
#   exp25_transition_matrix.png
#   exp25_transition_strength_overlay.png
#   exp25_basin_atlas_overlay.png
#   exp25_transition_table.csv
#   exp25_summary.txt
#
# ============================================================

import os
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

INPUT_DIR = (
    "APPLICATIONS/power_systems/"
    "FIELD_NAVIGATION_VALIDATION/outputs/"
    "EXP_08_REAL_FIELD_GEOMETRY"
)

OUTPUT_DIR = (
    "APPLICATIONS/power_systems/"
    "FIELD_NAVIGATION_VALIDATION/outputs/"
    "EXP_25_BASIN_TRANSITION_GRAPH"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

print("\nInput  ->", os.path.abspath(INPUT_DIR))
print("Output ->", os.path.abspath(OUTPUT_DIR))

# ------------------------------------------------------------
# Load Data
# ------------------------------------------------------------

df = pd.read_csv(
    os.path.join(
        INPUT_DIR,
        "exp08_field_states.csv"
    )
)

print("\nLoaded states:", len(df))

# ------------------------------------------------------------
# Feature Space
# ------------------------------------------------------------

features = [
    "global_scale",
    "min_vm",
    "mean_vm",
    "std_vm",
    "angle_span",
    "max_loading",
    "mean_loading",
    "density",
    "betweenness"
]

X = df[features].values
X = StandardScaler().fit_transform(X)

pca = PCA(
    n_components=2
)

coords = pca.fit_transform(X)

pca_variance = float(
    np.sum(
        pca.explained_variance_ratio_
    )
)

print(
    "PCA variance:",
    round(pca_variance, 4)
)

# ------------------------------------------------------------
# Build kNN Graph
# ------------------------------------------------------------

K = 12

nbrs = NearestNeighbors(
    n_neighbors=K + 1
).fit(coords)

distances, indices = nbrs.kneighbors(coords)

G = nx.Graph()

for i in range(len(coords)):
    G.add_node(i)

for i in range(len(coords)):
    for j, d in zip(
        indices[i][1:],
        distances[i][1:]
    ):
        G.add_edge(
            i,
            int(j),
            weight=float(d)
        )

print(
    "Graph nodes:",
    G.number_of_nodes()
)

print(
    "Graph edges:",
    G.number_of_edges()
)

# ------------------------------------------------------------
# Density Estimate
# ------------------------------------------------------------

mean_knn_distance = (
    distances[:, 1:]
    .mean(axis=1)
)

density = 1.0 / (
    mean_knn_distance + 1e-9
)

# ------------------------------------------------------------
# Reconstruct EXP_24E Basins
# ------------------------------------------------------------

attractor_of = {}

for node in G.nodes():

    current = node
    visited = set()

    while True:

        if current in visited:
            break

        visited.add(current)

        neighbors = list(
            G.neighbors(current)
        )

        best = current
        best_density = density[current]

        for n in neighbors:

            if density[n] > best_density:

                best_density = density[n]
                best = n

        if best == current:
            break

        current = best

    attractor_of[node] = current

attractors = sorted(
    list(
        set(
            attractor_of.values()
        )
    )
)

basin_lookup = {
    a: i
    for i, a in enumerate(attractors)
}

node_basin = np.array([
    basin_lookup[
        attractor_of[n]
    ]
    for n in range(len(coords))
])

n_basins = len(attractors)

print(
    "\nBasins detected:",
    n_basins
)

# ------------------------------------------------------------
# Basin Sizes
# ------------------------------------------------------------

basin_sizes = []

for b in range(n_basins):

    basin_sizes.append(
        np.sum(
            node_basin == b
        )
    )

basin_sizes = np.array(
    basin_sizes
)

# ------------------------------------------------------------
# Basin Centroids
# ------------------------------------------------------------

basin_centroids = np.zeros(
    (n_basins, 2)
)

for b in range(n_basins):

    members = np.where(
        node_basin == b
    )[0]

    basin_centroids[b] = (
        coords[members]
        .mean(axis=0)
    )
# ------------------------------------------------------------
# Basin Transition Matrix
# ------------------------------------------------------------

transition_matrix = np.zeros(
    (n_basins, n_basins),
    dtype=int
)

for u, v in G.edges():

    bu = node_basin[u]
    bv = node_basin[v]

    if bu != bv:

        transition_matrix[bu, bv] += 1
        transition_matrix[bv, bu] += 1

print(
    "Cross-basin edges:",
    transition_matrix.sum() // 2
)

# ------------------------------------------------------------
# Transition Table
# ------------------------------------------------------------

rows = []

for i in range(n_basins):
    for j in range(i + 1, n_basins):

        if transition_matrix[i, j] > 0:

            rows.append({
                "source_basin": i,
                "target_basin": j,
                "transition_count":
                    int(
                        transition_matrix[i, j]
                    )
            })

transition_table = pd.DataFrame(rows)

transition_table = transition_table.sort_values(
    "transition_count",
    ascending=False
)

transition_table.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "exp25_transition_table.csv"
    ),
    index=False
)

print(
    "\nTransitions:",
    len(transition_table)
)
