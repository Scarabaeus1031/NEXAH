"""
EXP_44J
NAVIGATION ENGINE

Goal
--------------------------------------------------
Perform actual Atlas navigation between coherent
transport domains discovered in EXP_44H.2 and
connected through EXP_44I geodesic transport.

Pipeline

Graph
 -> Flow
 -> Coherence
 -> Domains
 -> Geodesic Transport
 -> Navigation Engine

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

ROUTES_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44I_ATLAS_GEODESIC_TRANSPORT"
    / "exp44i_geodesic_routes.csv"
)

OUTDIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44J_NAVIGATION_ENGINE"
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

print("Routes  ->", ROUTES_PATH)
print("Exists  ->", ROUTES_PATH.exists())
print()

print("Output  ->", OUTDIR)
print()


# ============================================================
# LOAD
# ============================================================

G = nx.read_graphml(GRAPH_PATH)

df = pd.read_csv(DATA_PATH)

domains = pd.read_csv(DOMAIN_PATH)

routes = pd.read_csv(ROUTES_PATH)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print("Domains:", len(domains))
print("Routes:", len(routes))
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

    idx = int(np.argmin(dists))

    domain_nodes[int(row["domain_id"])] = node_list[idx]


# ============================================================
# NAVIGATION TESTS
# ============================================================

navigation_records = []

domain_ids = sorted(domain_nodes.keys())

for i in range(len(domain_ids)):
    for j in range(i + 1, len(domain_ids)):

        source_domain = domain_ids[i]
        target_domain = domain_ids[j]

        source_node = domain_nodes[source_domain]
        target_node = domain_nodes[target_domain]

        try:

            path = nx.shortest_path(
                G,
                source=source_node,
                target=target_node
            )

            navigation_records.append({
                "source_domain": source_domain,
                "target_domain": target_domain,
                "source_node": source_node,
                "target_node": target_node,
                "hop_count": len(path) - 1,
                "path_length": len(path),
                "path": " -> ".join(path)
            })

        except nx.NetworkXNoPath:
            continue


navigation_df = pd.DataFrame(
    navigation_records
)

navigation_df.to_csv(
    OUTDIR / "exp44j_navigation_routes.csv",
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

summary = pd.DataFrame({
    "metric": [
        "domains",
        "routes",
        "mean_hops",
        "min_hops",
        "max_hops"
    ],
    "value": [
        len(domain_ids),
        len(navigation_df),
        navigation_df["hop_count"].mean(),
        navigation_df["hop_count"].min(),
        navigation_df["hop_count"].max()
    ]
})

summary.to_csv(
    OUTDIR / "exp44j_navigation_summary.csv",
    index=False
)


# ============================================================
# VISUAL 1
# ============================================================

plt.figure(figsize=(10, 8))

plt.scatter(
    pc1,
    pc2,
    s=10,
    alpha=0.2
)

for domain_id, node in domain_nodes.items():

    p = node_positions[node]

    plt.scatter(
        p[0],
        p[1],
        s=120
    )

    plt.text(
        p[0],
        p[1],
        str(domain_id)
    )

plt.title(
    "EXP_44J Navigation Domain Anchors"
)

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44j_navigation_map.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 2
# ============================================================

best_routes = (
    navigation_df
    .sort_values("hop_count")
    .head(20)
)

plt.figure(figsize=(12, 6))

labels = [
    f"{r.source_domain}->{r.target_domain}"
    for _, r in best_routes.iterrows()
]

plt.bar(
    labels,
    best_routes["hop_count"]
)

plt.xticks(
    rotation=90
)

plt.ylabel("Hop Count")

plt.title(
    "EXP_44J Best Navigation Routes"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44j_best_routes.png",
    dpi=300
)

plt.close()


# ============================================================
# REPORT
# ============================================================

report = f"""
EXP_44J NAVIGATION ENGINE
==================================================

Domains
-------
{len(domain_ids)}

Routes Tested
-------------
{len(navigation_df)}

Mean Hop Count
--------------
{navigation_df['hop_count'].mean():.3f}

Shortest Route
--------------
{navigation_df['hop_count'].min()}

Longest Route
-------------
{navigation_df['hop_count'].max()}

Interpretation
--------------
The Atlas was used as an actual navigation
system between coherent transport domains.

Navigation routes were computed directly
through Atlas geometry.

This is the first operational navigation
experiment of the EXP_44 campaign.

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
Navigation Engine
"""

print(report)

with open(
    OUTDIR / "exp44j_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_44J complete.")
print()
