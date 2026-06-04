"""
EXP_44S
ATLAS SPINE ROBUSTNESS ANALYSIS

Goal
--------------------------------------------------
Evaluate how robust the Atlas Spine remains under
targeted removal of its most critical transport links.

The experiment progressively removes spine edges
according to their navigation importance and measures:

- connectivity degradation
- navigation degradation
- structural collapse threshold

Pipeline

Atlas Spine
 ->
Targeted Edge Removal
 ->
Connectivity Analysis
 ->
Navigation Analysis
 ->
Robustness Profile

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

SPINE_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44R_ATLAS_SPINE_IDENTIFICATION"
    / "atlas_spine.graphml"
)

OUTPUT_DIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44S_ATLAS_SPINE_ROBUSTNESS_ANALYSIS"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("\nSpine ->", SPINE_PATH)
print("Exists ->", SPINE_PATH.exists())
print("Output ->", OUTPUT_DIR)

if not SPINE_PATH.exists():
    raise FileNotFoundError(SPINE_PATH)


# ============================================================
# LOAD SPINE
# ============================================================

G = nx.read_graphml(SPINE_PATH)

print("\nSpine Nodes:", G.number_of_nodes())
print("Spine Edges:", G.number_of_edges())


# ============================================================
# NAVIGATION SCORE
# ============================================================

def navigation_score(graph):

    if graph.number_of_edges() == 0:
        return 0.0

    if not nx.is_connected(graph):
        largest = max(
            nx.connected_components(graph),
            key=len
        )

        graph = graph.subgraph(largest).copy()

    lengths = []

    nodes = list(graph.nodes())

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):

            try:
                d = nx.shortest_path_length(
                    graph,
                    nodes[i],
                    nodes[j]
                )
                lengths.append(d)

            except Exception:
                pass

    if len(lengths) == 0:
        return 0.0

    return 1.0 / np.mean(lengths)


baseline_navigation = navigation_score(G)

print("\nBaseline Navigation:", round(baseline_navigation, 6))


# ============================================================
# EDGE IMPORTANCE
# ============================================================

print("\nComputing edge criticality...")

edge_rows = []

for edge in G.edges():

    H = G.copy()
    H.remove_edge(*edge)

    nav = navigation_score(H)

    preservation = nav / baseline_navigation

    loss = 1.0 - preservation

    edge_rows.append(
        {
            "source": edge[0],
            "target": edge[1],
            "navigation_after": nav,
            "preservation": preservation,
            "loss": loss
        }
    )

edge_df = pd.DataFrame(edge_rows)

edge_df = edge_df.sort_values(
    "loss",
    ascending=False
)

edge_df.to_csv(
    OUTPUT_DIR / "exp44s_spine_failure_sequence.csv",
    index=False
)


# ============================================================
# PROGRESSIVE ATTACK
# ============================================================

print("\nRunning targeted attack simulation...")

H = G.copy()

removed = []
nav_curve = []
conn_curve = []

for idx, row in edge_df.iterrows():

    edge = (
        row["source"],
        row["target"]
    )

    if H.has_edge(*edge):

        H.remove_edge(*edge)

    removed.append(len(removed) + 1)

    nav_curve.append(
        navigation_score(H)
        / baseline_navigation
    )

    if H.number_of_nodes() > 0:

        largest = max(
            nx.connected_components(H),
            key=len
        )

        conn_curve.append(
            len(largest)
            / G.number_of_nodes()
        )

    else:

        conn_curve.append(0)


robustness_df = pd.DataFrame(
    {
        "removed_edges": removed,
        "navigation_preservation": nav_curve,
        "connectivity_preservation": conn_curve
    }
)

robustness_df.to_csv(
    OUTPUT_DIR / "exp44s_robustness_curve.csv",
    index=False
)


# ============================================================
# NAVIGATION DECAY
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    removed,
    nav_curve,
    marker="o"
)

plt.xlabel("Removed Critical Edges")
plt.ylabel("Navigation Preservation")
plt.title("EXP_44S Navigation Decay")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp44s_navigation_decay.png",
    dpi=300
)

plt.close()


# ============================================================
# CONNECTIVITY DECAY
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    removed,
    conn_curve,
    marker="o"
)

plt.xlabel("Removed Critical Edges")
plt.ylabel("Connectivity Preservation")
plt.title("EXP_44S Connectivity Decay")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp44s_connectivity_decay.png",
    dpi=300
)

plt.close()


# ============================================================
# ROBUSTNESS OVERLAY
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    removed,
    nav_curve,
    label="Navigation"
)

plt.plot(
    removed,
    conn_curve,
    label="Connectivity"
)

plt.xlabel("Removed Critical Edges")
plt.ylabel("Preservation")

plt.title("EXP_44S Spine Robustness Curve")

plt.legend()

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp44s_spine_robustness_curve.png",
    dpi=300
)

plt.close()


# ============================================================
# REPORT
# ============================================================

collapse_index = next(
    (
        i + 1
        for i, v in enumerate(conn_curve)
        if v < 0.5
    ),
    None
)

report = f"""
EXP_44S ATLAS SPINE ROBUSTNESS ANALYSIS
==================================================

Spine Nodes
-----------
{G.number_of_nodes()}

Spine Edges
-----------
{G.number_of_edges()}

Baseline Navigation
-------------------
{baseline_navigation:.6f}

Collapse Threshold
------------------
{collapse_index}

Interpretation
--------------
This experiment evaluates how robust
the Atlas Spine remains under targeted
removal of critical transport links.

Pipeline

Atlas Spine
 ->
Targeted Edge Removal
 ->
Connectivity Analysis
 ->
Navigation Analysis
 ->
Robustness Profile
"""

with open(
    OUTPUT_DIR / "exp44s_report.txt",
    "w"
) as f:
    f.write(report)

print(report)

print("\nEXP_44S COMPLETE\n")
