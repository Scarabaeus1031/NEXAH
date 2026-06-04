"""
EXP_44P
ATLAS HIGHWAY DETECTION

Goal
--------------------------------------------------
Identify preferential transport corridors
inside the Atlas Domain Supergraph.

These corridors represent domain pairs
whose navigation efficiency is significantly
higher than the global Atlas average.

Pipeline

Atlas Supergraph
 ->
Navigation Efficiency Matrix
 ->
Highway Extraction
 ->
Corridor Network

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

SUPERGRAPH_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44L_DOMAIN_SUPERGRAPH_CONSTRUCTION"
    / "exp44l_domain_supergraph.graphml"
)

EFFICIENCY_MATRIX_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44O_ATLAS_NAVIGATION_ACCURACY_VALIDATION"
    / "exp44o_efficiency_matrix.csv"
)

DOMAIN_TABLE_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44H2_COHERENT_DOMAIN_EXTRACTION"
    / "exp44h2_domain_table.csv"
)

OUTDIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44P_ATLAS_HIGHWAY_DETECTION"
)

OUTDIR.mkdir(parents=True, exist_ok=True)

print()
print("POWER_ROOT ->", POWER_ROOT)
print()

print("Supergraph ->", SUPERGRAPH_PATH)
print("Exists     ->", SUPERGRAPH_PATH.exists())
print()

print("Efficiency ->", EFFICIENCY_MATRIX_PATH)
print("Exists     ->", EFFICIENCY_MATRIX_PATH.exists())
print()

print("Domains    ->", DOMAIN_TABLE_PATH)
print("Exists     ->", DOMAIN_TABLE_PATH.exists())
print()

print("Output     ->", OUTDIR)
print()


# ============================================================
# LOAD
# ============================================================

G = nx.read_graphml(SUPERGRAPH_PATH)

eff = pd.read_csv(
    EFFICIENCY_MATRIX_PATH,
    index_col=0
)

domains = pd.read_csv(
    DOMAIN_TABLE_PATH
)

eff.index = eff.index.astype(str)
eff.columns = eff.columns.astype(str)

print("Domains:", len(eff))
print()


# ============================================================
# HIGHWAY THRESHOLD
# ============================================================

vals = []

for i in eff.index:
    for j in eff.columns:

        if i == j:
            continue

        vals.append(
            eff.loc[i, j]
        )

vals = np.array(vals)

mean_eff = np.mean(vals)
std_eff = np.std(vals)

threshold = mean_eff + std_eff

print("Mean Efficiency :", mean_eff)
print("Std Efficiency  :", std_eff)
print("Threshold       :", threshold)
print()


# ============================================================
# EXTRACT HIGHWAYS
# ============================================================

highways = []

for i in eff.index:
    for j in eff.columns:

        if int(j) <= int(i):
            continue

        value = eff.loc[i, j]

        if value >= threshold:

            highways.append({
                "domain_a": int(i),
                "domain_b": int(j),
                "efficiency": value
            })

highway_df = pd.DataFrame(
    highways
).sort_values(
    "efficiency",
    ascending=False
)

highway_df.to_csv(
    OUTDIR / "exp44p_highway_table.csv",
    index=False
)

print("Highways Found:", len(highway_df))
print()


# ============================================================
# HIGHWAY GRAPH
# ============================================================

H = nx.Graph()

for _, row in highway_df.iterrows():

    H.add_edge(
        int(row["domain_a"]),
        int(row["domain_b"]),
        weight=float(row["efficiency"])
    )

nx.write_graphml(
    H,
    OUTDIR / "exp44p_highway_network.graphml"
)


# ============================================================
# VISUAL 1
# HIGHWAY MATRIX
# ============================================================

highway_matrix = np.zeros_like(
    eff.values,
    dtype=float
)

for _, row in highway_df.iterrows():

    a = eff.index.get_loc(
        str(int(row["domain_a"]))
    )

    b = eff.columns.get_loc(
        str(int(row["domain_b"]))
    )

    highway_matrix[a, b] = row["efficiency"]
    highway_matrix[b, a] = row["efficiency"]

plt.figure(figsize=(10, 8))

plt.imshow(
    highway_matrix,
    aspect="auto"
)

plt.colorbar(
    label="Highway Strength"
)

plt.title(
    "EXP_44P Atlas Highways"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44p_highway_matrix.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 2
# HIGHWAY NETWORK
# ============================================================

plt.figure(figsize=(10, 8))

pos = {}

for _, row in domains.iterrows():

    pos[int(row["domain_id"])] = (
        row["centroid_pc1"],
        row["centroid_pc2"]
    )

if H.number_of_edges() > 0:

    widths = [
        H[u][v]["weight"] / threshold * 4
        for u, v in H.edges()
    ]

    nx.draw_networkx_edges(
        H,
        pos,
        width=widths,
        alpha=0.8
    )

    nx.draw_networkx_nodes(
        H,
        pos,
        node_size=300
    )

    nx.draw_networkx_labels(
        H,
        pos
    )

plt.title(
    "EXP_44P Atlas Highway Network"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44p_highway_network.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 3
# HIGHWAY STRENGTHS
# ============================================================

top = highway_df.head(20)

plt.figure(figsize=(10, 6))

labels = [
    f"{a}-{b}"
    for a, b in zip(
        top["domain_a"],
        top["domain_b"]
    )
]

plt.bar(
    labels,
    top["efficiency"]
)

plt.xticks(rotation=60)

plt.ylabel(
    "Efficiency"
)

plt.title(
    "EXP_44P Strongest Atlas Highways"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44p_highway_ranking.png",
    dpi=300
)

plt.close()

# ============================================================
# REPORT
# ============================================================

best = highway_df.iloc[0]

report = f"""
EXP_44P ATLAS HIGHWAY DETECTION
==================================================

Domains
-------
{len(eff)}

Mean Efficiency
---------------
{mean_eff:.6f}

Efficiency Threshold
--------------------
{threshold:.6f}

Detected Highways
-----------------
{len(highway_df)}

Strongest Highway
-----------------
{int(best['domain_a'])}
<
>
{int(best['domain_b'])}

Efficiency
----------
{best['efficiency']:.6f}

Interpretation
--------------
Atlas navigation is not homogeneous.

Specific domain pairs form
preferential transport corridors.

These corridors constitute the first
Atlas Highway Network.

Pipeline

Atlas Supergraph
 ->
Navigation Efficiency
 ->
Highway Detection
 ->
Transport Corridors
"""

print(report)

with open(
    OUTDIR / "exp44p_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_44P complete.")
print()
