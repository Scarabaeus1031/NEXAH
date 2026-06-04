"""
EXP_44L
DOMAIN SUPERGRAPH CONSTRUCTION

Goal
--------------------------------------------------
Construct a weighted supergraph whose nodes are
coherent Atlas domains and whose edges represent
geodesic transport distances.

Pipeline

Graph
 -> Flow
 -> Coherence
 -> Domains
 -> Geodesic Transport
 -> Domain Supergraph

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

DOMAIN_TABLE_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44H2_COHERENT_DOMAIN_EXTRACTION"
    / "exp44h2_domain_table.csv"
)

TRANSPORT_MATRIX_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44I_ATLAS_GEODESIC_TRANSPORT"
    / "exp44i_domain_transport_matrix.csv"
)

OUTDIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44L_DOMAIN_SUPERGRAPH_CONSTRUCTION"
)

OUTDIR.mkdir(parents=True, exist_ok=True)

print()
print("POWER_ROOT ->", POWER_ROOT)
print()

print("Domains ->", DOMAIN_TABLE_PATH)
print("Exists  ->", DOMAIN_TABLE_PATH.exists())
print()

print("Transport Matrix ->", TRANSPORT_MATRIX_PATH)
print("Exists           ->", TRANSPORT_MATRIX_PATH.exists())
print()

print("Output ->", OUTDIR)
print()


# ============================================================
# LOAD
# ============================================================

domains = pd.read_csv(DOMAIN_TABLE_PATH)

transport = pd.read_csv(
    TRANSPORT_MATRIX_PATH,
    index_col=0
)

# ------------------------------------------------
# normalize matrix labels
# rows = int
# cols = int
# ------------------------------------------------

transport.index = transport.index.astype(int)
transport.columns = transport.columns.astype(int)

domain_ids = sorted(
    transport.index.tolist()
)

print("Domains:", len(domain_ids))
print()

print("Transport Index Type  :", transport.index.dtype)
print("Transport Column Type :", transport.columns.dtype)
print()


# ============================================================
# BUILD SUPERGRAPH
# ============================================================

G = nx.Graph()

for _, row in domains.iterrows():

    d = int(row["domain_id"])

    G.add_node(
        d,
        size=row["nodes"],
        coherence=row["mean_coherence"],
        pc1=row["centroid_pc1"],
        pc2=row["centroid_pc2"]
    )

for i in domain_ids:
    for j in domain_ids:

        if j <= i:
            continue

        dist = transport.loc[i, j]

        if pd.isna(dist):
            continue

        G.add_edge(
            i,
            j,
            weight=float(dist)
        )

print("Supergraph Nodes:", G.number_of_nodes())
print("Supergraph Edges:", G.number_of_edges())
print()


# ============================================================
# CENTRALITY
# ============================================================

betweenness = nx.betweenness_centrality(
    G,
    weight="weight"
)

closeness = nx.closeness_centrality(
    G,
    distance="weight"
)

eigenvector = nx.eigenvector_centrality(
    G,
    weight="weight",
    max_iter=1000
)

centrality_rows = []

for d in G.nodes():

    centrality_rows.append({
        "domain_id": d,
        "betweenness": betweenness[d],
        "closeness": closeness[d],
        "eigenvector": eigenvector[d]
    })

centrality_df = pd.DataFrame(
    centrality_rows
).sort_values(
    "betweenness",
    ascending=False
)

centrality_df.to_csv(
    OUTDIR / "exp44l_domain_centrality.csv",
    index=False
)


# ============================================================
# SAVE GRAPH
# ============================================================

nx.write_graphml(
    G,
    OUTDIR / "exp44l_domain_supergraph.graphml"
)


# ============================================================
# EDGE TABLE
# ============================================================

edge_rows = []

for u, v, data in G.edges(data=True):

    edge_rows.append({
        "domain_a": u,
        "domain_b": v,
        "distance": data["weight"]
    })

pd.DataFrame(edge_rows).to_csv(
    OUTDIR / "exp44l_domain_supergraph_edges.csv",
    index=False
)


# ============================================================
# VISUAL 1
# ============================================================

plt.figure(figsize=(10, 8))

pos = {}

for _, row in domains.iterrows():

    pos[int(row["domain_id"])] = (
        row["centroid_pc1"],
        row["centroid_pc2"]
    )

nx.draw_networkx_edges(
    G,
    pos,
    alpha=0.35
)

sizes = [
    G.nodes[n]["size"] * 6
    for n in G.nodes()
]

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=sizes
)

nx.draw_networkx_labels(
    G,
    pos
)

plt.title(
    "EXP_44L Domain Supergraph"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44l_supergraph_map.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 2
# ============================================================

plt.figure(figsize=(10, 8))

matrix = nx.to_numpy_array(
    G,
    weight="weight"
)

plt.imshow(
    matrix,
    aspect="auto"
)

plt.colorbar(
    label="Transport Distance"
)

plt.title(
    "EXP_44L Supergraph Matrix"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44l_supergraph_matrix.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 3
# ============================================================

top = centrality_df.sort_values(
    "betweenness",
    ascending=False
)

plt.figure(figsize=(10, 6))

plt.bar(
    top["domain_id"].astype(str),
    top["betweenness"]
)

plt.title(
    "EXP_44L Betweenness Centrality"
)

plt.xlabel("Domain")
plt.ylabel("Betweenness")

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44l_domain_centrality_ranking.png",
    dpi=300
)

plt.close()


# ============================================================
# REPORT
# ============================================================

top_b = top.iloc[0]

report = f"""
EXP_44L DOMAIN SUPERGRAPH CONSTRUCTION
==================================================

Domains
-------
{G.number_of_nodes()}

Edges
-----
{G.number_of_edges()}

Density
-------
{nx.density(G):.4f}

Connected Components
--------------------
{nx.number_connected_components(G)}

Top Betweenness Domain
----------------------
{int(top_b['domain_id'])}

Betweenness
-----------
{top_b['betweenness']:.6f}

Interpretation
--------------
The coherent Atlas domains were elevated
into a higher-order transport graph.

This experiment represents the first
Atlas Supergraph.

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
 ->
Domain Supergraph
"""

print(report)

with open(
    OUTDIR / "exp44l_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_44L complete.")
print()
