"""
EXP_44R
ATLAS SPINE IDENTIFICATION

Goal
--------------------------------------------------
Identify the critical transport spine inside the
Atlas Transport Skeleton.

The spine consists of skeleton edges whose removal
causes the strongest degradation of navigation
preservation.

Pipeline

Domain Supergraph
 ->
Transport Skeleton
 ->
Edge Removal Impact
 ->
Atlas Spine

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

SKELETON_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44Q_TRANSPORT_SKELETON_EXTRACTION"
    / "atlas_transport_skeleton.graphml"
)
OUTDIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44R_ATLAS_SPINE_IDENTIFICATION"
)

OUTDIR.mkdir(parents=True, exist_ok=True)


print()
print("Skeleton ->", SKELETON_PATH)
print("Exists   ->", SKELETON_PATH.exists())
print("Output   ->", OUTDIR)
print()


# ============================================================
# LOAD GRAPH
# ============================================================

G = nx.read_graphml(SKELETON_PATH)

print("Skeleton Nodes:", G.number_of_nodes())
print("Skeleton Edges:", G.number_of_edges())
print()


# ============================================================
# NAVIGATION SCORE
# ============================================================

def navigation_score(graph):

    nodes = list(graph.nodes())
    values = []

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):

            a = nodes[i]
            b = nodes[j]

            try:
                d = nx.shortest_path_length(
                    graph,
                    a,
                    b,
                    weight="weight"
                )

                if d > 0:
                    values.append(1.0 / d)

            except nx.NetworkXNoPath:
                values.append(0.0)

    if len(values) == 0:
        return 0.0

    return float(np.mean(values))


BASELINE = navigation_score(G)

print("Baseline Navigation:", round(BASELINE, 6))
print()


# ============================================================
# EDGE IMPACT ANALYSIS
# ============================================================

print("Computing edge removal impacts...")
print()

records = []

for edge in G.edges():

    H = G.copy()
    H.remove_edge(*edge)

    nav_after = navigation_score(H)

    preservation = nav_after / BASELINE

    loss = 1.0 - preservation

    records.append(
        {
            "source": edge[0],
            "target": edge[1],
            "navigation_after": nav_after,
            "preservation": preservation,
            "loss": loss,
        }
    )

impact_df = pd.DataFrame(records)

impact_df = impact_df.sort_values(
    "loss",
    ascending=False
)

impact_df.to_csv(
    OUTDIR / "exp44r_spine_ranking.csv",
    index=False
)

print("Top Spine Edges")
print()
print(impact_df.head(10))
print()


# ============================================================
# SPINE EXTRACTION
# ============================================================

print("Extracting Atlas Spine...")
print()

TOP_PERCENT = 0.25

n_spine = max(
    1,
    int(len(impact_df) * TOP_PERCENT)
)

spine_edges = impact_df.head(n_spine)

SPINE = nx.Graph()

for node, attrs in G.nodes(data=True):
    SPINE.add_node(node, **attrs)

for _, row in spine_edges.iterrows():

    if G.has_edge(row.source, row.target):

        SPINE.add_edge(
            row.source,
            row.target,
            **G[row.source][row.target]
        )

# Connectivity repair

if not nx.is_connected(SPINE):

    print("Spine disconnected -> repairing")
    print()

    mst = nx.minimum_spanning_tree(
        G,
        weight="weight"
    )

    for u, v in mst.edges():

        if not SPINE.has_edge(u, v):

            SPINE.add_edge(
                u,
                v,
                **G[u][v]
            )


# ============================================================
# SAVE GRAPHML
# ============================================================

nx.write_graphml(
    SPINE,
    OUTDIR / "atlas_spine.graphml"
)


# ============================================================
# METRICS
# ============================================================

spine_nav = navigation_score(SPINE)

preservation = spine_nav / BASELINE

compression_ratio = (
    G.number_of_edges()
    /
    SPINE.number_of_edges()
)

metrics = pd.DataFrame(
    [
        {
            "original_edges": G.number_of_edges(),
            "spine_edges": SPINE.number_of_edges(),
            "compression_ratio": compression_ratio,
            "navigation_preservation": preservation,
            "components": nx.number_connected_components(SPINE),
        }
    ]
)

metrics.to_csv(
    OUTDIR / "exp44r_metrics.csv",
    index=False
)


# ============================================================
# VISUAL 1
# SPINE NETWORK
# ============================================================

print("Rendering spine network...")
print()

plt.figure(figsize=(10, 8))

pos = nx.spring_layout(
    SPINE,
    seed=42
)

nx.draw_networkx(
    SPINE,
    pos,
    node_size=900,
    font_size=10
)

plt.title("EXP_44R Atlas Spine")
plt.axis("off")

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44r_spine_network.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 2
# EDGE LOSS RANKING
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    impact_df["loss"].values,
    linewidth=2
)

plt.title("EXP_44R Edge Removal Impact")
plt.xlabel("Edge Rank")
plt.ylabel("Navigation Loss")

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44r_edge_loss_ranking.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 3
# TOP SPINE EDGES
# ============================================================

top10 = impact_df.head(10).copy()

labels = [
    f"{s}-{t}"
    for s, t in zip(
        top10.source,
        top10.target
    )
]

plt.figure(figsize=(10, 5))

plt.bar(
    labels,
    top10["loss"]
)

plt.xticks(rotation=45)

plt.ylabel("Navigation Loss")
plt.title("EXP_44R Critical Spine Edges")

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44r_top_spine_edges.png",
    dpi=300
)

plt.close()


# ============================================================
# REPORT
# ============================================================

report = f"""
EXP_44R ATLAS SPINE IDENTIFICATION
==================================================

Original Skeleton Edges
-----------------------
{G.number_of_edges()}

Spine Edges
-----------
{SPINE.number_of_edges()}

Compression Ratio
-----------------
{compression_ratio:.2f}

Navigation Preservation
-----------------------
{preservation:.6f}

Connected Components
--------------------
{nx.number_connected_components(SPINE)}

Interpretation
--------------
The Atlas Spine represents the minimal
set of transport links carrying the
largest fraction of Atlas navigability.

Pipeline

Domain Supergraph
 ->
Transport Skeleton
 ->
Edge Impact Analysis
 ->
Atlas Spine

The experiment identifies the critical
transport backbone of the reconstructed
Atlas.
"""

with open(
    OUTDIR / "exp44r_report.txt",
    "w"
) as f:
    f.write(report)

print(report)

print()
print("EXP_44R COMPLETE")
print()
