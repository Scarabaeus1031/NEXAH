"""
EXP_44K
NAVIGATION HUB DISCOVERY

Goal
--------------------------------------------------
Identify Atlas transport hubs and navigation
backbones from the navigation routes discovered
in EXP_44J.

Pipeline

Graph
 -> Flow
 -> Coherence
 -> Domains
 -> Geodesic Transport
 -> Navigation
 -> Hub Discovery

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

DOMAIN_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44H2_COHERENT_DOMAIN_EXTRACTION"
    / "exp44h2_domain_table.csv"
)

NAV_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44J_NAVIGATION_ENGINE"
    / "exp44j_navigation_routes.csv"
)

OUTDIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44K_NAVIGATION_HUB_DISCOVERY"
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

print("Domains ->", DOMAIN_PATH)
print("Exists  ->", DOMAIN_PATH.exists())
print()

print("Routes  ->", NAV_PATH)
print("Exists  ->", NAV_PATH.exists())
print()

print("Output  ->", OUTDIR)
print()


# ============================================================
# LOAD
# ============================================================

G = nx.read_graphml(GRAPH_PATH)

df = pd.read_csv(DATA_PATH)

domains = pd.read_csv(DOMAIN_PATH)

nav = pd.read_csv(NAV_PATH)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print("Domains:", len(domains))
print("Routes:", len(nav))
print()


# ============================================================
# COORDINATES
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
# DOMAIN ANCHORS
# ============================================================

domain_nodes = {}

for _, row in domains.iterrows():

    centroid = np.array([
        row["centroid_pc1"],
        row["centroid_pc2"]
    ])

    dists = np.linalg.norm(
        coords[:N] - centroid,
        axis=1
    )

    idx = np.argmin(dists)

    domain_nodes[int(row["domain_id"])] = node_list[idx]


# ============================================================
# NODE -> DOMAIN MAP
# ============================================================

node_to_domain = {}

for domain_id, node in domain_nodes.items():
    node_to_domain[node] = domain_id


# ============================================================
# HUB COUNTS
# ============================================================

traffic_count = {
    d: 0
    for d in domain_nodes.keys()
}

transit_count = {
    d: 0
    for d in domain_nodes.keys()
}


# ============================================================
# RECONSTRUCT ROUTES
# ============================================================

for _, row in nav.iterrows():

    source_node = row["source_node"]
    target_node = row["target_node"]

    try:

        path = nx.shortest_path(
            G,
            source=source_node,
            target=target_node
        )

    except:
        continue

    used_domains = []

    for node in path:

        if node in node_to_domain:
            used_domains.append(
                node_to_domain[node]
            )

    used_domains = list(
        dict.fromkeys(used_domains)
    )

    for d in used_domains:
        traffic_count[d] += 1

    if len(used_domains) > 2:

        for d in used_domains[1:-1]:
            transit_count[d] += 1


# ============================================================
# HUB TABLE
# ============================================================

hub_rows = []

max_transit = max(
    transit_count.values()
) if max(transit_count.values()) > 0 else 1

for domain_id in sorted(domain_nodes.keys()):

    hub_rows.append({
        "domain_id": domain_id,
        "traffic_count": traffic_count[domain_id],
        "transit_count": transit_count[domain_id],
        "hub_score":
        transit_count[domain_id] / max_transit
    })

hub_df = pd.DataFrame(
    hub_rows
)

hub_df = hub_df.sort_values(
    "hub_score",
    ascending=False
)

hub_df.to_csv(
    OUTDIR / "exp44k_hub_table.csv",
    index=False
)


# ============================================================
# CENTRALITY
# ============================================================

bet = nx.betweenness_centrality(
    G
)

centrality_rows = []

for domain_id, node in domain_nodes.items():

    centrality_rows.append({
        "domain_id": domain_id,
        "betweenness":
        bet.get(node, 0.0)
    })

centrality_df = pd.DataFrame(
    centrality_rows
)

centrality_df.to_csv(
    OUTDIR / "exp44k_domain_centrality.csv",
    index=False
)


# ============================================================
# VISUAL 1
# ============================================================

plt.figure(figsize=(11, 8))

plt.scatter(
    pc1,
    pc2,
    s=8,
    alpha=0.15
)

for _, row in hub_df.iterrows():

    d = int(row["domain_id"])

    node = domain_nodes[d]

    p = node_positions[node]

    size = 100 + 900 * row["hub_score"]

    plt.scatter(
        p[0],
        p[1],
        s=size
    )

    plt.text(
        p[0],
        p[1],
        str(d)
    )

plt.title(
    "EXP_44K Navigation Hub Map"
)

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44k_hub_map.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 2
# ============================================================

top = hub_df.head(15)

plt.figure(figsize=(12, 6))

plt.bar(
    top["domain_id"].astype(str),
    top["hub_score"]
)

plt.xlabel("Domain")
plt.ylabel("Hub Score")

plt.title(
    "EXP_44K Hub Ranking"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44k_hub_ranking.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 3
# ============================================================

top_hubs = hub_df.head(5)

plt.figure(figsize=(12, 6))

plt.bar(
    top_hubs["domain_id"].astype(str),
    top_hubs["traffic_count"]
)

plt.xlabel("Domain")
plt.ylabel("Traffic Count")

plt.title(
    "EXP_44K Navigation Backbone"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44k_navigation_backbone.png",
    dpi=300
)

plt.close()


# ============================================================
# REPORT
# ============================================================

best_domain = int(
    hub_df.iloc[0]["domain_id"]
)

best_score = float(
    hub_df.iloc[0]["hub_score"]
)

report = f"""
EXP_44K NAVIGATION HUB DISCOVERY
==================================================

Domains
-------
{len(domain_nodes)}

Navigation Routes
-----------------
{len(nav)}

Top Hub Domain
--------------
{best_domain}

Top Hub Score
-------------
{best_score:.3f}

Interpretation
--------------
Navigation routes were analyzed to identify
Atlas transport hubs.

Hub score measures how often a domain acts
as a transit corridor between other domains.

This experiment reveals the first Atlas
navigation backbone.

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
Navigation
 ->
Hub Discovery
"""

print(report)

with open(
    OUTDIR / "exp44k_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_44K complete.")
print()
