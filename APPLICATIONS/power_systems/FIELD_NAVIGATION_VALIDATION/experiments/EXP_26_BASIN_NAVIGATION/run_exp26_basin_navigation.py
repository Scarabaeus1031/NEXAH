# ============================================================
# EXP_26 — BASIN NAVIGATION
#
# Question:
# How does one navigate between attractor basins?
#
# Goal:
# Build the first NEXAH Navigator
#
# Basin A
#    ↓
# Basin B
#    ↓
# Basin C
#
# Inputs:
#   EXP_25 Basin Transition Graph
#
# Outputs:
#   exp26_navigation_routes.png
#   exp26_atlas_backbone.png
#   exp26_distance_matrix.png
#   exp26_navigation_centrality.csv
#   exp26_shortest_paths.csv
#   exp26_summary.txt
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
    "EXP_26_BASIN_NAVIGATION"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

print("\nInput  ->", os.path.abspath(INPUT_DIR))
print("Output ->", os.path.abspath(OUTPUT_DIR))

# ------------------------------------------------------------
# Load Field States
# ------------------------------------------------------------

df = pd.read_csv(
    os.path.join(
        INPUT_DIR,
        "exp08_field_states.csv"
    )
)

print(
    "\nLoaded states:",
    len(df)
)

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

# ------------------------------------------------------------
# PCA Coordinates
# ------------------------------------------------------------

pca = PCA(
    n_components=2
)

coords = pca.fit_transform(X)

print(
    "PCA variance:",
    round(
        np.sum(
            pca.explained_variance_ratio_
        ),
        4
    )
)

# ------------------------------------------------------------
# Build kNN Graph
# ------------------------------------------------------------

K = 12

nbrs = NearestNeighbors(
    n_neighbors=K + 1
)

nbrs.fit(coords)

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
# Density
# ------------------------------------------------------------

density = 1.0 / (
    distances[:, 1:].mean(axis=1)
    + 1e-9
)

# ------------------------------------------------------------
# Basin Reconstruction
# ------------------------------------------------------------

attractor_of = {}

for node in G.nodes():

    current = node
    visited = set()

    while True:

        if current in visited:
            break

        visited.add(current)

        best = current
        best_density = density[current]

        for n in G.neighbors(current):

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
    "\nBasins:",
    n_basins
)

# ------------------------------------------------------------
# Basin Sizes
# ------------------------------------------------------------

basin_sizes = np.array([
    np.sum(
        node_basin == b
    )
    for b in range(n_basins)
])

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
# Transition Matrix
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

# ------------------------------------------------------------
# Basin Atlas Graph
# ------------------------------------------------------------

BG = nx.Graph()

for b in range(n_basins):

    BG.add_node(
        b,
        size=int(
            basin_sizes[b]
        )
    )

for i in range(n_basins):

    for j in range(i + 1, n_basins):

        weight = transition_matrix[i, j]

        if weight > 0:

            BG.add_edge(
                i,
                j,
                weight=int(weight),
                distance=1.0 / weight
            )

print(
    "Atlas edges:",
    BG.number_of_edges()
)

# ------------------------------------------------------------
# Navigation Centrality
# ------------------------------------------------------------

centrality = nx.betweenness_centrality(
    BG,
    weight="distance"
)

centrality_df = pd.DataFrame({
    "basin": list(
        centrality.keys()
    ),
    "navigation_centrality":
        list(
            centrality.values()
        ),
    "basin_size":
        basin_sizes
})

centrality_df = (
    centrality_df
    .sort_values(
        "navigation_centrality",
        ascending=False
    )
)

centrality_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "exp26_navigation_centrality.csv"
    ),
    index=False
)

# ------------------------------------------------------------
# All Shortest Paths
# ------------------------------------------------------------

rows = []

for source in BG.nodes():

    for target in BG.nodes():

        if source >= target:
            continue

        try:

            path = nx.shortest_path(
                BG,
                source,
                target,
                weight="distance"
            )

            length = nx.shortest_path_length(
                BG,
                source,
                target,
                weight="distance"
            )

            rows.append({
                "source": source,
                "target": target,
                "path": str(path),
                "distance": float(length)
            })

        except:

            pass

paths_df = pd.DataFrame(rows)

paths_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "exp26_shortest_paths.csv"
    ),
    index=False
)

print(
    "Shortest paths:",
    len(paths_df)
)

# ------------------------------------------------------------
# Distance Matrix
# ------------------------------------------------------------

distance_matrix = np.zeros(
    (n_basins, n_basins)
)

for i in range(n_basins):

    for j in range(n_basins):

        try:

            distance_matrix[i, j] = (
                nx.shortest_path_length(
                    BG,
                    i,
                    j,
                    weight="distance"
                )
            )

        except:

            distance_matrix[i, j] = np.nan

# ------------------------------------------------------------
# Visual 1
# Atlas Backbone
# ------------------------------------------------------------

plt.figure(
    figsize=(10, 8)
)

pos = {
    b: basin_centroids[b]
    for b in BG.nodes()
}

edge_widths = [
    0.5 + BG[u][v]["weight"] * 0.08
    for u, v in BG.edges()
]

nx.draw_networkx_edges(
    BG,
    pos,
    width=edge_widths,
    alpha=0.35
)

nx.draw_networkx_nodes(
    BG,
    pos,
    node_size=[
        100 + basin_sizes[b] * 8
        for b in BG.nodes()
    ]
)

nx.draw_networkx_labels(
    BG,
    pos
)

plt.title(
    "EXP_26 Atlas Backbone"
)

plt.axis("off")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp26_atlas_backbone.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Visual 2
# Distance Matrix
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 6)
)

plt.imshow(
    distance_matrix,
    aspect="auto"
)

plt.colorbar(
    label="Navigation Distance"
)

plt.title(
    "EXP_26 Distance Matrix"
)

plt.xlabel("Target Basin")
plt.ylabel("Source Basin")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp26_distance_matrix.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Visual 3
# Navigation Routes
# ------------------------------------------------------------

plt.figure(
    figsize=(12, 8)
)

plt.scatter(
    coords[:, 0],
    coords[:, 1],
    s=10,
    alpha=0.15
)

top_paths = (
    paths_df
    .sort_values(
        "distance"
    )
    .head(20)
)

for _, row in top_paths.iterrows():

    path = eval(
        row["path"]
    )

    pts = np.array([
        basin_centroids[p]
        for p in path
    ])

    plt.plot(
        pts[:, 0],
        pts[:, 1],
        linewidth=2
    )

plt.title(
    "EXP_26 Navigation Routes"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp26_navigation_routes.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

with open(
    os.path.join(
        OUTPUT_DIR,
        "exp26_summary.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_26 BASIN NAVIGATION\n"
    )

    f.write(
        "========================\n\n"
    )

    f.write(
        f"Basins: {n_basins}\n"
    )

    f.write(
        f"Atlas Edges: {BG.number_of_edges()}\n"
    )

    f.write(
        f"Shortest Paths: {len(paths_df)}\n"
    )

    f.write(
        "\nTop Navigation Hubs\n"
    )

    for _, row in (
        centrality_df.head(10)
        .iterrows()
    ):

        f.write(
            f"Basin {int(row['basin'])}"
            f" : {row['navigation_centrality']:.4f}\n"
        )

print(
    "\nEXP_26 completed."
)
