# ============================================================
# EXP_24E — LATENT ATTRACTOR & BASIN DETECTION
#
# Question:
# Does the discovered NEXAH manifold contain
# attractors and basin structures?
#
# Idea:
# Each state follows the local density gradient
# until it reaches a local attractor.
#
# Outputs:
#   exp24e_basin_map.png
#   exp24e_attractors.png
#   exp24e_basin_sizes.png
#   exp24e_flow_graph.png
#   exp24e_summary.txt
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
    "EXP_24E_LATENT_ATTRACTOR_BASIN_DETECTION"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

print("\nInput  ->", os.path.abspath(INPUT_DIR))
print("Output ->", os.path.abspath(OUTPUT_DIR))

# ------------------------------------------------------------
# Load
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
# PCA Manifold
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
# kNN Graph
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
            j,
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
# Local Density
# ------------------------------------------------------------

density = np.zeros(
    len(coords)
)

for i in range(len(coords)):

    neigh = indices[i][1:]

    d = np.mean(
        distances[i][1:]
    )

    density[i] = 1.0 / (
        d + 1e-9
    )

# ------------------------------------------------------------
# Flow to Local Attractor
# ------------------------------------------------------------

attractor_of = {}

for node in G.nodes():

    current = node

    visited = set()

    while True:

        if current in visited:
            break

        visited.add(current)

        neigh = list(
            G.neighbors(current)
        )

        best = current
        best_density = density[current]

        for n in neigh:

            if density[n] > best_density:

                best_density = density[n]
                best = n

        if best == current:
            break

        current = best

    attractor_of[node] = current

# ------------------------------------------------------------
# Basin Assignment
# ------------------------------------------------------------

attractors = sorted(
    list(
        set(
            attractor_of.values()
        )
    )
)

basin_id = {}

for i, a in enumerate(attractors):
    basin_id[a] = i

node_basin = np.array([
    basin_id[
        attractor_of[n]
    ]
    for n in range(len(coords))
])

print(
    "\nAttractors found:",
    len(attractors)
)

# ------------------------------------------------------------
# Basin Sizes
# ------------------------------------------------------------

basin_sizes = []

for a in attractors:

    size = sum(
        attractor_of[n] == a
        for n in attractor_of
    )

    basin_sizes.append(size)

# ------------------------------------------------------------
# Plot 1
# Basin Map
# ------------------------------------------------------------

plt.figure(
    figsize=(10,8)
)

plt.scatter(
    coords[:,0],
    coords[:,1],
    c=node_basin,
    s=30,
    cmap="tab20"
)

plt.title(
    "EXP_24E — Basin Map"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp24e_basin_map.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Plot 2
# Attractors
# ------------------------------------------------------------

plt.figure(
    figsize=(10,8)
)

plt.scatter(
    coords[:,0],
    coords[:,1],
    s=15,
    alpha=0.25
)

plt.scatter(
    coords[attractors,0],
    coords[attractors,1],
    s=180,
    marker="*"
)

plt.title(
    "EXP_24E — Attractors"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp24e_attractors.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Plot 3
# Basin Sizes
# ------------------------------------------------------------

plt.figure(
    figsize=(10,5)
)

plt.bar(
    np.arange(
        len(basin_sizes)
    ),
    basin_sizes
)

plt.xlabel(
    "Basin ID"
)

plt.ylabel(
    "States"
)

plt.title(
    "EXP_24E — Basin Sizes"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp24e_basin_sizes.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Plot 4
# Flow Graph
# ------------------------------------------------------------

sample_nodes = np.random.choice(
    len(coords),
    min(150, len(coords)),
    replace=False
)

plt.figure(
    figsize=(10,8)
)

plt.scatter(
    coords[:,0],
    coords[:,1],
    s=10,
    alpha=0.2
)

for n in sample_nodes:

    a = attractor_of[n]

    plt.plot(
        [
            coords[n,0],
            coords[a,0]
        ],
        [
            coords[n,1],
            coords[a,1]
        ],
        alpha=0.15
    )

plt.title(
    "EXP_24E — Basin Flow Structure"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp24e_flow_graph.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

summary = pd.DataFrame({
    "attractor_node": attractors,
    "basin_size": basin_sizes
})

summary = summary.sort_values(
    "basin_size",
    ascending=False
)

summary.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "exp24e_basins.csv"
    ),
    index=False
)

with open(
    os.path.join(
        OUTPUT_DIR,
        "exp24e_summary.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_24E LATENT ATTRACTOR & BASIN DETECTION\n"
    )

    f.write(
        "========================================\n\n"
    )

    f.write(
        f"States: {len(df)}\n"
    )

    f.write(
        f"Attractors: {len(attractors)}\n\n"
    )

    f.write(
        "Largest Basins\n"
    )

    for _, row in summary.head(15).iterrows():

        f.write(
            f"Node {int(row.attractor_node)} : "
            f"{int(row.basin_size)}\n"
        )

print("\nLargest basins:")
print(summary.head(10))

print("\nEXP_24E completed.")
