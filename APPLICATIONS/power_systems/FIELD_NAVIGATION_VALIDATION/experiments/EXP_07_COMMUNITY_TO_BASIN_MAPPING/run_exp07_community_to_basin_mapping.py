"""
run_exp07_community_to_basin_mapping.py

EXP_07 — COMMUNITY TO BASIN MAPPING

Goal:
Investigate whether graph communities
correspond to dynamical stability basins.

NEXAH Validation Program
2026
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from networkx.algorithms.community import (
    louvain_communities,
    modularity
)

from sklearn.metrics import (
    normalized_mutual_info_score
)

from scipy.stats import entropy


# ============================================================
# Output Directory
# ============================================================

OUTPUT_DIR = (
    "APPLICATIONS/power_systems/"
    "FIELD_NAVIGATION_VALIDATION/"
    "outputs/EXP_07_COMMUNITY_TO_BASIN_MAPPING"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

print()
print("Output folder:")
print(OUTPUT_DIR)
print()


# ============================================================
# IEEE39 Placeholder Graph
#
# Replace later with real IEEE39 loader.
# ============================================================

G = nx.random_geometric_graph(
    39,
    radius=0.35,
    seed=42
)

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

pos = nx.spring_layout(
    G,
    seed=42
)


# ============================================================
# Communities
# ============================================================

communities = louvain_communities(
    G,
    seed=42
)

community_labels = {}

for cid, comm in enumerate(communities):

    for node in comm:

        community_labels[node] = cid

community_vector = np.array(
    [
        community_labels[n]
        for n in G.nodes()
    ]
)

mod_score = modularity(
    G,
    communities
)


# ============================================================
# Synthetic Basin Assignment
#
# Simulates:
#
# Stable Basin
# Transition Basin
# Collapse Basin
#
# Later replaced by actual basin extraction.
# ============================================================

basin_labels = []

for node in G.nodes():

    c = community_labels[node]

    if c == 0:

        basin = np.random.choice(
            [0, 1],
            p=[0.85, 0.15]
        )

    elif c == 1:

        basin = np.random.choice(
            [1, 2],
            p=[0.80, 0.20]
        )

    elif c == 2:

        basin = np.random.choice(
            [0, 2],
            p=[0.75, 0.25]
        )

    else:

        basin = np.random.choice(
            [1, 2],
            p=[0.40, 0.60]
        )

    basin_labels.append(basin)

basin_vector = np.array(
    basin_labels
)

basin_names = {
    0: "Stable",
    1: "Transition",
    2: "Collapse"
}


# ============================================================
# Alignment Metrics
# ============================================================

nmi = normalized_mutual_info_score(
    community_vector,
    basin_vector
)

purities = []

for cid in np.unique(
    community_vector
):

    idx = (
        community_vector == cid
    )

    basins = basin_vector[idx]

    counts = np.bincount(
        basins
    )

    purity = (
        counts.max()
        / counts.sum()
    )

    purities.append(purity)

mean_purity = np.mean(
    purities
)


# ============================================================
# Alignment Matrix
# ============================================================

n_communities = len(
    np.unique(community_vector)
)

n_basins = len(
    np.unique(basin_vector)
)

alignment = np.zeros(
    (
        n_communities,
        n_basins
    )
)

for c in range(n_communities):

    idx = (
        community_vector == c
    )

    total = np.sum(idx)

    for b in range(n_basins):

        alignment[c, b] = (
            np.sum(
                basin_vector[idx] == b
            )
            / total
        )


# ============================================================
# Plot 1
# Community Basin Overlay
# ============================================================

plt.figure(figsize=(8, 8))

node_colors = basin_vector

nx.draw_networkx(
    G,
    pos,
    node_color=node_colors,
    cmap="viridis",
    node_size=350,
    with_labels=True
)

plt.title(
    "Community → Basin Overlay"
)

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp07_community_basin_overlay.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Plot 2
# Basin Map
# ============================================================

plt.figure(figsize=(8, 8))

nx.draw_networkx(
    G,
    pos,
    node_color=basin_vector,
    cmap="plasma",
    node_size=350,
    with_labels=True
)

plt.title(
    "Dynamical Basin Assignment"
)

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp07_basin_map.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Plot 3
# Alignment Matrix
# ============================================================

plt.figure(figsize=(7, 5))

plt.imshow(
    alignment,
    aspect="auto"
)

plt.colorbar(
    label="Occupancy"
)

plt.xlabel(
    "Basin"
)

plt.ylabel(
    "Community"
)

plt.title(
    "Community ↔ Basin Alignment"
)

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp07_alignment_matrix.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Plot 4
# Dashboard
# ============================================================

fig = plt.figure(
    figsize=(10, 6)
)

plt.axis("off")

summary = (
    f"EXP_07 COMMUNITY TO BASIN MAPPING\n\n"
    f"Louvain Communities : {n_communities}\n"
    f"Modularity          : {mod_score:.4f}\n\n"
    f"Mean Basin Purity   : {mean_purity:.4f}\n"
    f"NMI                 : {nmi:.4f}\n\n"
    f"Interpretation:\n"
    f"Higher values indicate stronger\n"
    f"community-basin correspondence."
)

plt.text(
    0.05,
    0.95,
    summary,
    fontsize=12,
    va="top"
)

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp07_summary_dashboard.png"
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
    "community": community_vector,
    "basin": basin_vector

})

df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "exp07_assignments.csv"
    ),
    index=False
)


# ============================================================
# TXT REPORT
# ============================================================

with open(
    os.path.join(
        OUTPUT_DIR,
        "exp07_results.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_07 COMMUNITY TO BASIN MAPPING\n"
    )

    f.write(
        "========================================\n\n"
    )

    f.write(
        f"Louvain communities: "
        f"{n_communities}\n"
    )

    f.write(
        f"Modularity: "
        f"{mod_score:.6f}\n"
    )

    f.write(
        f"Mean basin purity: "
        f"{mean_purity:.6f}\n"
    )

    f.write(
        f"NMI: "
        f"{nmi:.6f}\n"
    )

    f.write("\n")

    for i, purity in enumerate(
        purities
    ):

        f.write(
            f"Community {i} purity: "
            f"{purity:.4f}\n"
        )


# ============================================================
# Console
# ============================================================

print()
print("EXP_07 RESULTS")
print("-" * 40)

print(
    f"Louvain communities: "
    f"{n_communities}"
)

print(
    f"Modularity: "
    f"{mod_score:.4f}"
)

print(
    f"Mean basin purity: "
    f"{mean_purity:.4f}"
)

print(
    f"NMI: "
    f"{nmi:.4f}"
)

print()
print(
    f"Saved to: {OUTPUT_DIR}"
)
