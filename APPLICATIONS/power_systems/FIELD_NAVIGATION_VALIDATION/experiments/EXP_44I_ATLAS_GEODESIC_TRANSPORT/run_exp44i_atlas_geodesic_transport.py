"""
EXP_44I
ATLAS GEODESIC TRANSPORT

Goal
--------------------------------------------------
Compute geodesic transport routes between coherent
Atlas domains discovered in EXP_44H.2.

Pipeline

Graph
 -> Flow
 -> Coherence
 -> Domains
 -> Geodesic Transport

Author
--------------------------------------------------
NEXAH / FIELD NAVIGATION VALIDATION
"""

from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PATH DISCOVERY
# ============================================================

CURRENT = Path(__file__).resolve()

POWER_ROOT = next(
    p for p in CURRENT.parents
    if p.name == "power_systems"
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

DOMAIN_TABLE_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44H2_COHERENT_DOMAIN_EXTRACTION"
    / "exp44h2_domain_table.csv"
)

COHERENCE_TABLE_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44H1_FLOW_COHERENCE_MAP"
    / "exp44h1_coherence_table.csv"
)

OUTDIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44I_ATLAS_GEODESIC_TRANSPORT"
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

print("Domains ->", DOMAIN_TABLE_PATH)
print("Exists  ->", DOMAIN_TABLE_PATH.exists())
print()

print("Coherence ->", COHERENCE_TABLE_PATH)
print("Exists    ->", COHERENCE_TABLE_PATH.exists())
print()

print("Output ->", OUTDIR)
print()


# ============================================================
# LOAD
# ============================================================

G = nx.read_graphml(GRAPH_PATH)

df = pd.read_csv(DATA_PATH)

domains = pd.read_csv(DOMAIN_TABLE_PATH)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print()


# ============================================================
# PCA COORDINATES
# ============================================================

pc1 = df["PC1"].values
pc2 = df["PC2"].values

coords = np.column_stack([pc1, pc2])

node_list = list(G.nodes())

N = min(len(node_list), len(coords))

node_positions = {
    node_list[i]: coords[i]
    for i in range(N)
}


# ============================================================
# DOMAIN CENTROIDS
# ============================================================

domain_nodes = {}

for _, row in domains.iterrows():

    centroid = np.array([
        row["centroid_pc1"],
        row["centroid_pc2"]
    ])

    dists = np.linalg.norm(coords[:N] - centroid, axis=1)

    idx = np.argmin(dists)

    domain_nodes[int(row["domain_id"])] = node_list[idx]


# ============================================================
# GEODESIC ROUTES
# ============================================================

routes = []

domain_ids = sorted(domain_nodes.keys())

for i in range(len(domain_ids)):
    for j in range(i + 1, len(domain_ids)):

        d1 = domain_ids[i]
        d2 = domain_ids[j]

        n1 = domain_nodes[d1]
        n2 = domain_nodes[d2]

        try:

            path = nx.shortest_path(
                G,
                source=n1,
                target=n2
            )

            routes.append({
                "domain_a": d1,
                "domain_b": d2,
                "path_length": len(path),
                "source_node": n1,
                "target_node": n2
            })

        except nx.NetworkXNoPath:
            pass


routes_df = pd.DataFrame(routes)

routes_df.to_csv(
    OUTDIR / "exp44i_geodesic_routes.csv",
    index=False
)


# ============================================================
# TRANSPORT MATRIX
# ============================================================

matrix = np.full(
    (len(domain_ids), len(domain_ids)),
    np.nan
)

id_to_idx = {
    d: i
    for i, d in enumerate(domain_ids)
}

for _, row in routes_df.iterrows():

    i = id_to_idx[row["domain_a"]]
    j = id_to_idx[row["domain_b"]]

    matrix[i, j] = row["path_length"]
    matrix[j, i] = row["path_length"]

np.fill_diagonal(matrix, 0)

matrix_df = pd.DataFrame(
    matrix,
    index=domain_ids,
    columns=domain_ids
)

matrix_df.to_csv(
    OUTDIR / "exp44i_domain_transport_matrix.csv"
)


# ============================================================
# VISUAL 1
# ============================================================

plt.figure(figsize=(10, 8))

plt.imshow(
    matrix,
    aspect="auto"
)

plt.colorbar(
    label="Geodesic Length"
)

plt.title(
    "EXP_44I Domain Transport Matrix"
)

plt.xlabel("Domain")
plt.ylabel("Domain")

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44i_transport_matrix.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 2
# ============================================================

plt.figure(figsize=(10, 8))

plt.scatter(
    pc1,
    pc2,
    s=10,
    alpha=0.25
)

for domain_id, node in domain_nodes.items():

    if node not in node_positions:
        continue

    p = node_positions[node]

    plt.scatter(
        p[0],
        p[1],
        s=80
    )

    plt.text(
        p[0],
        p[1],
        str(domain_id)
    )

plt.title(
    "EXP_44I Domain Geodesic Anchors"
)

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44i_domain_anchors.png",
    dpi=300
)

plt.close()


# ============================================================
# REPORT
# ============================================================

mean_length = routes_df["path_length"].mean()

min_length = routes_df["path_length"].min()

max_length = routes_df["path_length"].max()

report = f"""
EXP_44I ATLAS GEODESIC TRANSPORT
==================================================

Domains
-------
{len(domain_ids)}

Routes
------
{len(routes_df)}

Mean Geodesic Length
--------------------
{mean_length:.3f}

Shortest Route
--------------
{min_length}

Longest Route
-------------
{max_length}

Interpretation
--------------
Shortest graph routes were computed
between coherent Atlas domains.

This experiment establishes the first
Atlas transport metric.

Pipeline

Graph
 ->
Flow
 ->
Coherence
 ->
Domains
 ->
Geodesic Transport
"""

print(report)

with open(
    OUTDIR / "exp44i_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_44I complete.")
print()
