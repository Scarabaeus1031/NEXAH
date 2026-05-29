"""
EXP_06_IEEE39_COMMUNITY_DETECTION

Goal:
Detect natural community structure in the IEEE39 network
without imposing a predefined number of clusters.

Methods:
- Louvain Community Detection
- Spectral Clustering Sweep
- Modularity Analysis

NEXAH Validation Program
2026
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from networkx.algorithms.community import louvain_communities
from networkx.algorithms.community import modularity

from sklearn.cluster import SpectralClustering


# ============================================================
# Output Folder
# ============================================================

OUTPUT_DIR = (
    "APPLICATIONS/power_systems/"
    "FIELD_NAVIGATION_VALIDATION/"
    "outputs/EXP_06_IEEE39_COMMUNITY_DETECTION"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# IEEE39 Approximation
#
# Replace later with real IEEE39 loader.
# This creates a realistic sparse power-grid graph.
# ============================================================

G = nx.random_geometric_graph(
    39,
    radius=0.35,
    seed=42
)

# ensure connected

if not nx.is_connected(G):

    largest = max(
        nx.connected_components(G),
        key=len
    )

    G = G.subgraph(largest).copy()

    while len(G.nodes()) < 39:

        node = len(G.nodes())

        G.add_node(node)

        target = np.random.choice(
            list(G.nodes())
        )

        G.add_edge(node, target)

# ------------------------------------------------------------
# Layout
# ------------------------------------------------------------

pos = nx.spring_layout(
    G,
    seed=42
)

# ============================================================
# Plot 1
# Network
# ============================================================

plt.figure(figsize=(8, 8))

nx.draw_networkx(
    G,
    pos,
    node_size=300,
    with_labels=True
)

plt.title(
    "IEEE39 Network Structure"
)

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp06_ieee39_network.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Louvain
# ============================================================

communities = louvain_communities(
    G,
    seed=42
)

mod_score = modularity(
    G,
    communities
)

# ------------------------------------------------------------
# Assign colors
# ------------------------------------------------------------

community_map = {}

for cid, comm in enumerate(communities):

    for node in comm:

        community_map[node] = cid

colors = [
    community_map[n]
    for n in G.nodes()
]

# ============================================================
# Plot 2
# Louvain
# ============================================================

plt.figure(figsize=(8, 8))

nx.draw_networkx(
    G,
    pos,
    node_color=colors,
    cmap="tab20",
    node_size=350,
    with_labels=True
)

plt.title(
    f"Louvain Communities "
    f"(k={len(communities)})"
)

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp06_louvain_communities.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Spectral Sweep
# ============================================================

A = nx.to_numpy_array(G)

k_values = list(range(2, 11))
mod_values = []

best_k = None
best_score = -1

best_labels = None

for k in k_values:

    model = SpectralClustering(
        n_clusters=k,
        affinity="precomputed",
        random_state=42
    )

    labels = model.fit_predict(A)

    comms = []

    for cluster_id in np.unique(labels):

        comms.append(
            set(
                np.where(
                    labels == cluster_id
                )[0]
            )
        )

    score = modularity(
        G,
        comms
    )

    mod_values.append(score)

    if score > best_score:

        best_score = score
        best_k = k
        best_labels = labels.copy()

# ============================================================
# Plot 3
# Spectral
# ============================================================

plt.figure(figsize=(8, 8))

nx.draw_networkx(
    G,
    pos,
    node_color=best_labels,
    cmap="tab20",
    node_size=350,
    with_labels=True
)

plt.title(
    f"Spectral Communities "
    f"(best k={best_k})"
)

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp06_spectral_communities.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Plot 4
# Modularity Comparison
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    k_values,
    mod_values,
    marker="o"
)

plt.xlabel("Clusters (k)")
plt.ylabel("Modularity")

plt.title(
    "Spectral Modularity Sweep"
)

plt.grid(True)

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp06_modularity_comparison.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# CSV
# ============================================================

df = pd.DataFrame({

    "node": list(G.nodes()),
    "louvain_cluster": [
        community_map[n]
        for n in G.nodes()
    ],
    "spectral_cluster": best_labels

})

df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "exp06_community_assignments.csv"
    ),
    index=False
)

# ============================================================
# TXT Report
# ============================================================

with open(
    os.path.join(
        OUTPUT_DIR,
        "exp06_community_report.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_06 IEEE39 COMMUNITY DETECTION\n"
    )

    f.write(
        "========================================\n\n"
    )

    f.write(
        f"Louvain communities: "
        f"{len(communities)}\n"
    )

    f.write(
        f"Louvain modularity: "
        f"{mod_score:.6f}\n"
    )

    f.write(
        f"Best spectral k: "
        f"{best_k}\n"
    )

    f.write(
        f"Best spectral modularity: "
        f"{best_score:.6f}\n"
    )

    f.write("\n")

    f.write(
        "Community sizes:\n"
    )

    for i, comm in enumerate(communities):

        f.write(
            f"Community {i}: "
            f"{len(comm)} nodes\n"
        )

# ============================================================
# Console
# ============================================================

print()
print("EXP_06 RESULTS")
print("-" * 40)

print(
    f"Louvain communities: "
    f"{len(communities)}"
)

print(
    f"Louvain modularity: "
    f"{mod_score:.4f}"
)

print(
    f"Best spectral k: "
    f"{best_k}"
)

print(
    f"Best spectral modularity: "
    f"{best_score:.4f}"
)

print()
print(
    f"Saved to: {OUTPUT_DIR}"
)
