# ============================================================
# EXP_27 — TRANSITION DYNAMICS
#
# Question:
# Which atlas roads are actually used most often?
#
# Goal:
# Convert the basin atlas into a traffic map.
#
# EXP_24E:
#     Territories
#
# EXP_25:
#     Roads
#
# EXP_26:
#     Navigation
#
# EXP_27:
#     Traffic Flow
#
# Outputs:
#
#   exp27_transition_flow_map.png
#   exp27_road_usage.png
#   exp27_transition_directionality.png
#   exp27_dominant_routes.png
#   exp27_transition_table.csv
#   exp27_summary.txt
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
    "EXP_27_TRANSITION_DYNAMICS"
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
# Features
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
# PCA
# ------------------------------------------------------------

pca = PCA(
    n_components=2
)

coords = pca.fit_transform(X)

print(
    "PCA variance:",
    round(
        pca.explained_variance_ratio_.sum(),
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

                best = n
                best_density = density[n]

        if best == current:
            break

        current = best

    attractor_of[node] = current

attractors = sorted(
    set(
        attractor_of.values()
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
# Basin Centroids
# ------------------------------------------------------------

centroids = np.zeros(
    (n_basins, 2)
)

sizes = []

for b in range(n_basins):

    members = np.where(
        node_basin == b
    )[0]

    sizes.append(
        len(members)
    )

    centroids[b] = (
        coords[members]
        .mean(axis=0)
    )

sizes = np.array(sizes)

# ------------------------------------------------------------
# Road Usage Matrix
# ------------------------------------------------------------

traffic = np.zeros(
    (n_basins, n_basins),
    dtype=int
)

for u, v in G.edges():

    bu = node_basin[u]
    bv = node_basin[v]

    if bu != bv:

        traffic[bu, bv] += 1
        traffic[bv, bu] += 1

# ------------------------------------------------------------
# Atlas Graph
# ------------------------------------------------------------

AG = nx.Graph()

for b in range(n_basins):

    AG.add_node(
        b,
        size=int(sizes[b])
    )

for i in range(n_basins):

    for j in range(i + 1, n_basins):

        if traffic[i, j] > 0:

            AG.add_edge(
                i,
                j,
                weight=int(
                    traffic[i, j]
                )
            )

print(
    "Atlas roads:",
    AG.number_of_edges()
)

# ------------------------------------------------------------
# Road Usage Table
# ------------------------------------------------------------

rows = []

for u, v, d in AG.edges(data=True):

    rows.append({
        "source": u,
        "target": v,
        "traffic": d["weight"]
    })

table = pd.DataFrame(rows)

table = table.sort_values(
    "traffic",
    ascending=False
)

table.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "exp27_transition_table.csv"
    ),
    index=False
)

# ------------------------------------------------------------
# Visual 1
# Traffic Map
# ------------------------------------------------------------

plt.figure(
    figsize=(11, 8)
)

plt.scatter(
    coords[:, 0],
    coords[:, 1],
    s=15,
    alpha=0.15
)

for u, v, d in AG.edges(data=True):

    x1, y1 = centroids[u]
    x2, y2 = centroids[v]

    plt.plot(
        [x1, x2],
        [y1, y2],
        linewidth=0.3 + d["weight"] * 0.15,
        alpha=0.6
    )

plt.scatter(
    centroids[:, 0],
    centroids[:, 1],
    s=120 + sizes * 8
)

plt.title(
    "EXP_27 Transition Flow Map"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp27_transition_flow_map.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Visual 2
# Road Usage Histogram
# ------------------------------------------------------------

plt.figure(
    figsize=(10, 5)
)

plt.hist(
    table["traffic"],
    bins=15
)

plt.title(
    "EXP_27 Road Usage Distribution"
)

plt.xlabel(
    "Traffic"
)

plt.ylabel(
    "Road Count"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp27_road_usage.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Visual 3
# Transition Matrix
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 7)
)

plt.imshow(
    traffic,
    aspect="auto"
)

plt.colorbar(
    label="Traffic"
)

plt.title(
    "EXP_27 Transition Directionality"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp27_transition_directionality.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Visual 4
# Dominant Routes
# ------------------------------------------------------------

top = table.head(10)

plt.figure(
    figsize=(11, 8)
)

plt.scatter(
    coords[:, 0],
    coords[:, 1],
    s=10,
    alpha=0.12
)

for _, row in top.iterrows():

    u = int(row["source"])
    v = int(row["target"])

    x1, y1 = centroids[u]
    x2, y2 = centroids[v]

    plt.plot(
        [x1, x2],
        [y1, y2],
        linewidth=3,
        alpha=0.9
    )

plt.scatter(
    centroids[:, 0],
    centroids[:, 1],
    s=120
)

plt.title(
    "EXP_27 Dominant Routes"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp27_dominant_routes.png"
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
        "exp27_summary.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_27 TRANSITION DYNAMICS\n"
    )

    f.write(
        "=========================\n\n"
    )

    f.write(
        f"Basins: {n_basins}\n"
    )

    f.write(
        f"Roads: {AG.number_of_edges()}\n"
    )

    f.write(
        f"States: {len(coords)}\n\n"
    )

    f.write(
        "Top Roads\n"
    )

    for _, row in top.iterrows():

        f.write(
            f"{int(row['source'])}"
            f" -> "
            f"{int(row['target'])}"
            f" : "
            f"{int(row['traffic'])}\n"
        )

print("\nEXP_27 completed.")
