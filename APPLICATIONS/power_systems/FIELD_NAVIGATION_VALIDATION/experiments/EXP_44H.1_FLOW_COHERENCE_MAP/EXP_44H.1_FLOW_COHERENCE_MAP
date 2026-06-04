"""
EXP_44H.1
FLOW COHERENCE MAP

Goal
--------------------------------------------------
Measure local flow coherence across the reconstructed
NEXAH Atlas Flow Field.

This experiment asks:

Is global flow coherence low because the Atlas is random,
or because it contains multiple locally coherent
transport corridors?

Outputs
--------------------------------------------------
exp44h1_flow_coherence_map.png
exp44h1_coherence_histogram.png
exp44h1_coherence_table.csv
exp44h1_report.txt
"""

from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors


# ============================================================
# PATHS
# ============================================================

POWER_ROOT = (
    Path(__file__)
    .resolve()
    .parents[4]
)

GRAPH_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44D_ATLAS_STATE_GRAPH_RECONSTRUCTION"
    / "atlas_state_graph.graphml"
)

DATA_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_34_CONTROL_EFFORT_ESTIMATION"
    / "exp34_control_effort_table.csv"
)

OUTDIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44H1_FLOW_COHERENCE_MAP"
)

OUTDIR.mkdir(parents=True, exist_ok=True)

print()
print("POWER_ROOT ->", POWER_ROOT)
print()
print("Graph   ->", GRAPH_PATH)
print("Exists  ->", GRAPH_PATH.exists())
print()
print("Dataset ->", DATA_PATH)
print("Exists  ->", DATA_PATH.exists())
print()
print("Output  ->", OUTDIR)
print()


# ============================================================
# LOAD
# ============================================================

G = nx.read_graphml(GRAPH_PATH)
df = pd.read_csv(DATA_PATH)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print()

# ------------------------------------------------------------
# numeric matrix
# ------------------------------------------------------------

numeric_df = df.select_dtypes(include=[np.number]).fillna(0)

X = numeric_df.values

# ------------------------------------------------------------
# PCA projection
# ------------------------------------------------------------

pca = PCA(n_components=2)
XY = pca.fit_transform(X)

# ------------------------------------------------------------
# Atlas node mapping
# ------------------------------------------------------------

node_list = list(G.nodes())

N = min(len(node_list), len(XY))

XY = XY[:N]
node_list = node_list[:N]

node_to_idx = {
    n: i
    for i, n in enumerate(node_list)
}

# ============================================================
# FLOW VECTORS
# ============================================================

flow_vectors = np.zeros((N, 2))

for node in node_list:

    idx = node_to_idx[node]

    nbrs = list(G.neighbors(node))

    if len(nbrs) == 0:
        continue

    vecs = []

    for nbr in nbrs:

        if nbr not in node_to_idx:
            continue

        j = node_to_idx[nbr]

        vecs.append(
            XY[j] - XY[idx]
        )

    if len(vecs) == 0:
        continue

    flow_vectors[idx] = np.mean(vecs, axis=0)

# ============================================================
# LOCAL COHERENCE
# ============================================================

K = 10

nn = NearestNeighbors(
    n_neighbors=min(K, N)
)

nn.fit(XY)

indices = nn.kneighbors(
    XY,
    return_distance=False
)

coherence = np.zeros(N)

for i in range(N):

    local_idx = indices[i]

    local_vecs = flow_vectors[local_idx]

    norms = np.linalg.norm(
        local_vecs,
        axis=1
    )

    mask = norms > 1e-12

    if np.sum(mask) < 2:
        coherence[i] = 0
        continue

    unit_vecs = (
        local_vecs[mask]
        / norms[mask][:, None]
    )

    mean_dir = np.mean(
        unit_vecs,
        axis=0
    )

    coherence[i] = np.linalg.norm(
        mean_dir
    )

# ============================================================
# GLOBAL STATS
# ============================================================

mean_coherence = np.mean(coherence)

max_coherence = np.max(coherence)

median_coherence = np.median(coherence)

print("Mean Coherence  :", mean_coherence)
print("Median Coherence:", median_coherence)
print("Max Coherence   :", max_coherence)
print()

# ============================================================
# SAVE TABLE
# ============================================================

table = pd.DataFrame({
    "pc1": XY[:, 0],
    "pc2": XY[:, 1],
    "coherence": coherence
})

table.to_csv(
    OUTDIR / "exp44h1_coherence_table.csv",
    index=False
)

# ============================================================
# VISUAL 1
# ============================================================

plt.figure(figsize=(10, 8))

sc = plt.scatter(
    XY[:, 0],
    XY[:, 1],
    c=coherence,
    cmap="viridis",
    s=30
)

plt.colorbar(
    sc,
    label="Local Flow Coherence"
)

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.title(
    "EXP_44H.1 Flow Coherence Map"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44h1_flow_coherence_map.png",
    dpi=300
)

plt.close()

# ============================================================
# VISUAL 2
# ============================================================

plt.figure(figsize=(8, 5))

plt.hist(
    coherence,
    bins=30
)

plt.xlabel("Coherence")
plt.ylabel("Count")

plt.title(
    "EXP_44H.1 Coherence Distribution"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44h1_coherence_histogram.png",
    dpi=300
)

plt.close()

# ============================================================
# REPORT
# ============================================================

report = f"""
EXP_44H.1 FLOW COHERENCE MAP
==================================================

Nodes
------
{N}

Mean Coherence
--------------
{mean_coherence:.6f}

Median Coherence
----------------
{median_coherence:.6f}

Maximum Coherence
-----------------
{max_coherence:.6f}

Interpretation
--------------
Coherence near 1
indicates locally aligned transport.

Coherence near 0
indicates conflicting flow directions.

This experiment maps where transport
corridors emerge inside the Atlas.

44H:
Graph -> Flow

44H.1:
Flow -> Coherence Structure
"""

with open(
    OUTDIR / "exp44h1_report.txt",
    "w"
) as f:
    f.write(report)

print("EXP_44H.1 complete.")
print()
print("Mean Coherence :", mean_coherence)
print("Median         :", median_coherence)
print("Maximum        :", max_coherence)
print()
