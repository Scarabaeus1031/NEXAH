# ============================================================
# EXP_24D — LATENT CURVATURE ANALYSIS
#
# Question:
# Where are the gates, bottlenecks and escape regions
# inside the discovered NEXAH transport manifold?
#
# Outputs:
#   exp24d_curvature_map.png
#   exp24d_bottlenecks.png
#   exp24d_gate_candidates.png
#   exp24d_escape_vectors.png
#   exp24d_summary.txt
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
    "EXP_24D_LATENT_CURVATURE_ANALYSIS"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("\nInput  ->", os.path.abspath(INPUT_DIR))
print("Output ->", os.path.abspath(OUTPUT_DIR))

# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------

df = pd.read_csv(
    os.path.join(INPUT_DIR, "exp08_field_states.csv")
)

print("\nLoaded states:", len(df))

# ------------------------------------------------------------
# Feature set
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
# PCA 2D manifold
# ------------------------------------------------------------

pca = PCA(n_components=2)

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
# Build graph
# ------------------------------------------------------------

K = 8

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

largest = max(
    nx.connected_components(G),
    key=len
)

G = G.subgraph(largest).copy()

nodes = np.array(list(G.nodes()))

print("Graph nodes:", len(nodes))
print("Graph edges:", G.number_of_edges())

# ------------------------------------------------------------
# Curvature estimate
# ------------------------------------------------------------

curvature = np.zeros(len(coords))

for n in nodes:

    neigh = list(G.neighbors(n))

    if len(neigh) < 2:
        continue

    center = coords[n]

    dists = np.linalg.norm(
        coords[neigh] - center,
        axis=1
    )

    curvature[n] = np.std(dists)

# ------------------------------------------------------------
# Betweenness bottlenecks
# ------------------------------------------------------------

print("\nComputing betweenness...")

bet = nx.betweenness_centrality(
    G,
    normalized=True
)

bet_arr = np.zeros(len(coords))

for k, v in bet.items():
    bet_arr[k] = v

# ------------------------------------------------------------
# Gate score
# ------------------------------------------------------------

curv_norm = (
    curvature - curvature.min()
)

if curv_norm.max() > 0:
    curv_norm /= curv_norm.max()

bet_norm = (
    bet_arr - bet_arr.min()
)

if bet_norm.max() > 0:
    bet_norm /= bet_norm.max()

gate_score = (
    0.5 * curv_norm +
    0.5 * bet_norm
)

# ------------------------------------------------------------
# Top gate candidates
# ------------------------------------------------------------

top_n = 20

gate_nodes = np.argsort(
    gate_score
)[-top_n:]

# ------------------------------------------------------------
# Plot 1
# Curvature
# ------------------------------------------------------------

plt.figure(figsize=(9,7))

plt.scatter(
    coords[:,0],
    coords[:,1],
    c=curvature,
    s=30,
    cmap="viridis"
)

plt.colorbar(
    label="Curvature"
)

plt.title(
    "EXP_24D — Curvature Map"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp24d_curvature_map.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Plot 2
# Bottlenecks
# ------------------------------------------------------------

plt.figure(figsize=(9,7))

plt.scatter(
    coords[:,0],
    coords[:,1],
    c=bet_arr,
    s=30,
    cmap="plasma"
)

plt.colorbar(
    label="Betweenness"
)

plt.title(
    "EXP_24D — Bottlenecks"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp24d_bottlenecks.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Plot 3
# Gate candidates
# ------------------------------------------------------------

plt.figure(figsize=(10,8))

plt.scatter(
    coords[:,0],
    coords[:,1],
    s=20,
    alpha=0.3,
    label="Field"
)

plt.scatter(
    coords[gate_nodes,0],
    coords[gate_nodes,1],
    s=120,
    label="Gate Candidates"
)

plt.legend()

plt.title(
    "EXP_24D — Gate Candidates"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp24d_gate_candidates.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Plot 4
# Escape vectors
# ------------------------------------------------------------

plt.figure(figsize=(10,8))

plt.scatter(
    coords[:,0],
    coords[:,1],
    s=15,
    alpha=0.25
)

for n in gate_nodes:

    neigh = list(G.neighbors(n))

    if len(neigh) == 0:
        continue

    target = coords[neigh].mean(axis=0)

    dx = target[0] - coords[n,0]
    dy = target[1] - coords[n,1]

    plt.arrow(
        coords[n,0],
        coords[n,1],
        dx,
        dy,
        head_width=0.08,
        alpha=0.8
    )

plt.title(
    "EXP_24D — Escape Directions"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp24d_escape_vectors.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

top_gate_scores = np.sort(
    gate_score
)[-10:]

with open(
    os.path.join(
        OUTPUT_DIR,
        "exp24d_summary.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_24D LATENT CURVATURE ANALYSIS\n"
    )

    f.write(
        "========================================\n\n"
    )

    f.write(
        f"States: {len(df)}\n"
    )

    f.write(
        f"Graph Nodes: {len(nodes)}\n"
    )

    f.write(
        f"PCA Variance: "
        f"{np.sum(pca.explained_variance_ratio_):.4f}\n\n"
    )

    f.write(
        "Top Gate Scores\n"
    )

    for v in top_gate_scores:
        f.write(
            f"{v:.6f}\n"
        )

print("\nTop gate nodes:")
print(gate_nodes)

print("\nEXP_24D completed.")
