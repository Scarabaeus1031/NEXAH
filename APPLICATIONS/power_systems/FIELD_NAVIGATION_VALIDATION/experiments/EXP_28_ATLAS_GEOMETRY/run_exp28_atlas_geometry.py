# ============================================================
# EXP_28 — ATLAS GEOMETRY
#
# Question:
# Does the Basin Atlas possess hidden geometric structure?
#
# Hypotheses:
#
# H1:
# Basins align along a dominant principal axis.
#
# H2:
# Secondary transverse axes exist.
#
# H3:
# Basin centroids form a ring / shell geometry.
#
# H4:
# High-traffic roads align with the dominant axis.
#
# Inputs:
#   EXP_08_REAL_FIELD_GEOMETRY / exp08_field_states.csv
#
# Outputs:
#   exp28_principal_axis.png
#   exp28_symmetry_map.png
#   exp28_ring_fit.png
#   exp28_transport_axis_overlay.png
#   exp28_geometric_modes.png
#   exp28_summary.txt
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
    "EXP_28_ATLAS_GEOMETRY"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

print("\nInput  ->", os.path.abspath(INPUT_DIR))
print("Output ->", os.path.abspath(OUTPUT_DIR))

# ------------------------------------------------------------
# Load States
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

# ------------------------------------------------------------
# PCA State Space
# ------------------------------------------------------------

pca_states = PCA(
    n_components=2
)

coords = pca_states.fit_transform(X)

print(
    "State-space variance:",
    round(
        np.sum(
            pca_states.explained_variance_ratio_
        ),
        4
    )
)

# ------------------------------------------------------------
# Build Graph
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
    "Basins:",
    n_basins
)

# ------------------------------------------------------------
# Basin Centroids
# ------------------------------------------------------------

basin_centroids = np.zeros(
    (n_basins, 2)
)

basin_sizes = []

for b in range(n_basins):

    members = np.where(
        node_basin == b
    )[0]

    basin_centroids[b] = (
        coords[members]
        .mean(axis=0)
    )

    basin_sizes.append(
        len(members)
    )

basin_sizes = np.array(
    basin_sizes
)

# ------------------------------------------------------------
# Atlas PCA
# ------------------------------------------------------------

atlas_pca = PCA(
    n_components=2
)

atlas_pca.fit(
    basin_centroids
)

center = basin_centroids.mean(
    axis=0
)

pc1 = atlas_pca.components_[0]
pc2 = atlas_pca.components_[1]

explained = (
    atlas_pca.explained_variance_ratio_
)

print(
    "\nAtlas PCA:",
    np.round(
        explained,
        4
    )
)

# ------------------------------------------------------------
# Visual 1
# Principal Axis
# ------------------------------------------------------------

plt.figure(
    figsize=(10, 8)
)

plt.scatter(
    basin_centroids[:, 0],
    basin_centroids[:, 1],
    s=basin_sizes * 10
)

scale = 8

plt.plot(
    [
        center[0] - pc1[0] * scale,
        center[0] + pc1[0] * scale
    ],
    [
        center[1] - pc1[1] * scale,
        center[1] + pc1[1] * scale
    ],
    linewidth=4,
    label="PC1"
)

plt.plot(
    [
        center[0] - pc2[0] * scale,
        center[0] + pc2[0] * scale
    ],
    [
        center[1] - pc2[1] * scale,
        center[1] + pc2[1] * scale
    ],
    linewidth=3,
    linestyle="--",
    label="PC2"
)

for i in range(n_basins):

    plt.text(
        basin_centroids[i, 0],
        basin_centroids[i, 1],
        str(i)
    )

plt.title(
    "EXP_28 Principal Geometry Axes"
)

plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp28_principal_axis.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Ring Fit
# ------------------------------------------------------------

cx = np.mean(
    basin_centroids[:, 0]
)

cy = np.mean(
    basin_centroids[:, 1]
)

radii = np.sqrt(
    (basin_centroids[:, 0] - cx) ** 2 +
    (basin_centroids[:, 1] - cy) ** 2
)

mean_radius = np.mean(
    radii
)

radius_std = np.std(
    radii
)

theta = np.linspace(
    0,
    2*np.pi,
    400
)

# ------------------------------------------------------------
# Visual 2
# Ring Geometry
# ------------------------------------------------------------

plt.figure(
    figsize=(10, 8)
)

plt.scatter(
    basin_centroids[:, 0],
    basin_centroids[:, 1],
    s=basin_sizes * 10
)

plt.plot(
    cx + mean_radius * np.cos(theta),
    cy + mean_radius * np.sin(theta),
    linewidth=3
)

plt.scatter(
    cx,
    cy,
    s=200
)

for i in range(n_basins):

    plt.text(
        basin_centroids[i,0],
        basin_centroids[i,1],
        str(i)
    )

plt.title(
    "EXP_28 Ring Fit"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp28_ring_fit.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Symmetry Projection
# ------------------------------------------------------------

projections = (
    basin_centroids - center
) @ pc1

# ------------------------------------------------------------
# Visual 3
# Symmetry Map
# ------------------------------------------------------------

plt.figure(
    figsize=(10, 6)
)

plt.bar(
    np.arange(n_basins),
    projections
)

plt.title(
    "EXP_28 Symmetry Projection"
)

plt.xlabel(
    "Basin"
)

plt.ylabel(
    "Projection on PC1"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp28_symmetry_map.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Geometric Modes
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 6)
)

plt.bar(
    ["PC1", "PC2"],
    explained
)

plt.title(
    "EXP_28 Geometric Modes"
)

plt.ylabel(
    "Explained Variance"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp28_geometric_modes.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Transport Overlay
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
# Visual 4
# Transport vs Geometry
# ------------------------------------------------------------

plt.figure(
    figsize=(10, 8)
)

plt.scatter(
    coords[:, 0],
    coords[:, 1],
    alpha=0.15
)

for i in range(n_basins):

    plt.scatter(
        basin_centroids[i,0],
        basin_centroids[i,1],
        s=basin_sizes[i] * 10
    )

for i in range(n_basins):

    for j in range(i + 1, n_basins):

        traffic = transition_matrix[i, j]

        if traffic > 0:

            plt.plot(
                [
                    basin_centroids[i,0],
                    basin_centroids[j,0]
                ],
                [
                    basin_centroids[i,1],
                    basin_centroids[j,1]
                ],
                linewidth=0.05 * traffic,
                alpha=0.5
            )

plt.plot(
    [
        center[0] - pc1[0] * scale,
        center[0] + pc1[0] * scale
    ],
    [
        center[1] - pc1[1] * scale,
        center[1] + pc1[1] * scale
    ],
    linewidth=4
)

plt.title(
    "EXP_28 Transport Axis Overlay"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp28_transport_axis_overlay.png"
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
        "exp28_summary.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_28 ATLAS GEOMETRY\n"
    )

    f.write(
        "=====================\n\n"
    )

    f.write(
        f"Basins: {n_basins}\n"
    )

    f.write(
        f"PC1 variance: {explained[0]:.4f}\n"
    )

    f.write(
        f"PC2 variance: {explained[1]:.4f}\n"
    )

    f.write(
        f"Mean radius: {mean_radius:.4f}\n"
    )

    f.write(
        f"Radius std: {radius_std:.4f}\n"
    )

print(
    "\nEXP_28 completed."
)
