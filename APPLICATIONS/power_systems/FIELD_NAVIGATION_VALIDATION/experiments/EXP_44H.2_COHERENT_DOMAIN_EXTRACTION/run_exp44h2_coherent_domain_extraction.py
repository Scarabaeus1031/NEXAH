"""
EXP_44H.2
COHERENT DOMAIN EXTRACTION

Goal
--------------------------------------------------
Extract coherent transport domains from the
Atlas Flow Field discovered in EXP_44H.1.

Pipeline

Graph
 -> Flow
 -> Coherence
 -> Domains

Author
--------------------------------------------------
NEXAH / FIELD NAVIGATION VALIDATION
"""

from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.neighbors import NearestNeighbors


# ============================================================
# PATHS
# ============================================================

POWER_ROOT = Path(__file__).resolve().parents[3]

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
    / "EXP_44H2_COHERENT_DOMAIN_EXTRACTION"
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
# PARAMETERS
# ============================================================

K_NEIGHBORS = 10
COHERENCE_THRESHOLD = 0.80


# ============================================================
# LOAD
# ============================================================

G = nx.read_graphml(GRAPH_PATH)
df = pd.read_csv(DATA_PATH)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print()

# ------------------------------------------------------------
# PCA coordinates
# ------------------------------------------------------------

pc1_col = None
pc2_col = None

for c in df.columns:
    cl = c.lower()

    if pc1_col is None and ("pc1" in cl):
        pc1_col = c

    if pc2_col is None and ("pc2" in cl):
        pc2_col = c

if pc1_col is None or pc2_col is None:
    raise ValueError(
        "Could not locate PC1 / PC2 columns."
    )

coords = df[[pc1_col, pc2_col]].values

N = min(len(coords), G.number_of_nodes())

coords = coords[:N]

nodes = list(G.nodes())[:N]

node_to_index = {
    node: i
    for i, node in enumerate(nodes)
}


# ============================================================
# FLOW RECONSTRUCTION
# ============================================================

flow_vectors = np.zeros((N, 2))

for node in nodes:

    idx = node_to_index[node]

    nbrs = list(G.successors(node))

    if len(nbrs) == 0:
        continue

    vecs = []

    for nbr in nbrs:

        if nbr not in node_to_index:
            continue

        j = node_to_index[nbr]

        vecs.append(coords[j] - coords[idx])

    if len(vecs):
        flow_vectors[idx] = np.mean(vecs, axis=0)


# ============================================================
# LOCAL COHERENCE
# ============================================================

nbrs_model = NearestNeighbors(
    n_neighbors=min(K_NEIGHBORS + 1, N)
)

nbrs_model.fit(coords)

indices = nbrs_model.kneighbors(
    coords,
    return_distance=False
)

coherence = np.zeros(N)

for i in range(N):

    v = flow_vectors[i]

    vn = np.linalg.norm(v)

    if vn < 1e-12:
        continue

    scores = []

    for j in indices[i][1:]:

        u = flow_vectors[j]

        un = np.linalg.norm(u)

        if un < 1e-12:
            continue

        score = np.dot(v, u) / (vn * un)

        scores.append(score)

    if len(scores):
        coherence[i] = np.mean(scores)

coherence = np.clip(coherence, 0, 1)


# ============================================================
# DOMAIN NODES
# ============================================================

domain_mask = coherence >= COHERENCE_THRESHOLD

domain_nodes = [
    nodes[i]
    for i in range(N)
    if domain_mask[i]
]

print("Threshold:", COHERENCE_THRESHOLD)
print("Domain Nodes:", len(domain_nodes))
print()

subG = G.subgraph(domain_nodes).copy()

components = list(
    nx.connected_components(subG.to_undirected())
)

print("Domains Found:", len(components))
print()


# ============================================================
# DOMAIN TABLE
# ============================================================

domain_records = []

domain_id_map = {}

for domain_id, comp in enumerate(
    components,
    start=1
):

    comp = list(comp)

    idxs = [
        node_to_index[n]
        for n in comp
        if n in node_to_index
    ]

    if len(idxs) == 0:
        continue

    centroid = coords[idxs].mean(axis=0)

    domain_records.append({
        "domain_id": domain_id,
        "nodes": len(idxs),
        "mean_coherence":
            float(np.mean(coherence[idxs])),
        "max_coherence":
            float(np.max(coherence[idxs])),
        "centroid_pc1":
            float(centroid[0]),
        "centroid_pc2":
            float(centroid[1]),
    })

    for idx in idxs:
        domain_id_map[idx] = domain_id

domain_df = pd.DataFrame(domain_records)

domain_df.to_csv(
    OUTDIR / "exp44h2_domain_table.csv",
    index=False
)


# ============================================================
# VISUAL 1
# ============================================================

plt.figure(figsize=(10, 8))

colors = np.full(N, -1)

for idx, dom in domain_id_map.items():
    colors[idx] = dom

plt.scatter(
    coords[:, 0],
    coords[:, 1],
    c="lightgray",
    alpha=0.25,
    s=25
)

mask = colors > 0

plt.scatter(
    coords[mask, 0],
    coords[mask, 1],
    c=colors[mask],
    cmap="tab20",
    s=45
)

plt.title(
    "EXP_44H.2 Coherent Domains"
)

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44h2_domain_map.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 2
# ============================================================

if len(domain_df):

    plt.figure(figsize=(10, 5))

    plt.bar(
        domain_df["domain_id"].astype(str),
        domain_df["nodes"]
    )

    plt.title(
        "EXP_44H.2 Domain Sizes"
    )

    plt.xlabel("Domain ID")
    plt.ylabel("Node Count")

    plt.tight_layout()

    plt.savefig(
        OUTDIR / "exp44h2_domain_sizes.png",
        dpi=300
    )

    plt.close()


# ============================================================
# REPORT
# ============================================================

largest_domain = 0

if len(domain_df):
    largest_domain = int(
        domain_df["nodes"].max()
    )

report = f"""
EXP_44H.2 COHERENT DOMAIN EXTRACTION
==================================================

Coherence Threshold
-------------------
{COHERENCE_THRESHOLD:.2f}

Total Nodes
-----------
{N}

Domain Nodes
------------
{len(domain_nodes)}

Domains Found
-------------
{len(domain_df)}

Largest Domain
--------------
{largest_domain}

Interpretation
--------------
Nodes with local coherence above the threshold
were extracted from the Atlas Flow Field.

Connected coherent regions were then identified
as transport domains.

This experiment represents the first automatic
segmentation of the Atlas into coherent
transport structures.

Pipeline

Graph
  ->
Flow
  ->
Coherence
  ->
Domains
"""

with open(
    OUTDIR / "exp44h2_domain_report.txt",
    "w"
) as f:
    f.write(report)

print(report)

print()
print("EXP_44H.2 complete.")
print()
