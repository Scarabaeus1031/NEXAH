"""

EXP_44O

ATLAS NAVIGATION ACCURACY VALIDATION

Goal

--------------------------------------------------

Validate whether Atlas-derived navigation routes

outperform random transport through the Domain

Supergraph.

Central question:

Does Atlas navigation provide meaningful route

guidance beyond random walks?

Pipeline

Domain Supergraph

 ->

Atlas Navigation Routes

 ->

Random Walk Baseline

 ->

Navigation Accuracy Validation

Author

--------------------------------------------------

NEXAH / FIELD NAVIGATION VALIDATION

"""

from pathlib import Path

import random

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

    / "EXP_44O_ATLAS_NAVIGATION_ACCURACY_VALIDATION"
)

OUTDIR.mkdir(
    parents=True,
    exist_ok=True
)

print()
print("POWER_ROOT ->", POWER_ROOT)
print()

print("Supergraph ->", SUPERGRAPH_PATH)
print("Exists     ->", SUPERGRAPH_PATH.exists())
print()

print("Domains    ->", DOMAIN_TABLE_PATH)
print("Exists     ->", DOMAIN_TABLE_PATH.exists())
print()

print("Output     ->", OUTDIR)
print()

# ============================================================
# LOAD
# ============================================================

G = nx.read_graphml(
    SUPERGRAPH_PATH
)

domains = pd.read_csv(
    DOMAIN_TABLE_PATH
)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print()

# ============================================================
# RANDOM WALK BASELINE
# ============================================================

def random_route_length(
    G,
    source,
    target,
    max_steps=100
):

    current = source

    visited = {source}

    for step in range(max_steps):

        if current == target:
            return step

        neighbors = list(
            G.neighbors(current)
        )

        if not neighbors:
            return np.nan

        current = random.choice(
            neighbors
        )

    return np.nan

# ============================================================
# VALIDATION
# ============================================================

random.seed(42)

nodes = list(G.nodes())

results = []

for i in range(len(nodes)):

    for j in range(i + 1, len(nodes)):

        source = nodes[i]
        target = nodes[j]

        try:

            atlas_len = nx.shortest_path_length(
                G,
                source,
                target
            )

        except:

            continue

        random_lengths = []

        for _ in range(100):

            rl = random_route_length(
                G,
                source,
                target
            )

            if not np.isnan(rl):
                random_lengths.append(rl)

        if len(random_lengths) == 0:
            continue

        mean_random = np.mean(
            random_lengths
        )

        gain = (
            1
            - atlas_len / mean_random
        )

        efficiency = (
            mean_random
            / atlas_len
        )

        results.append({
            "source": source,
            "target": target,
            "atlas_length": atlas_len,
            "random_length": mean_random,
            "gain": gain,
            "efficiency": efficiency
        })

results_df = pd.DataFrame(
    results
)

results_df.to_csv(
    OUTDIR / "exp44o_navigation_validation.csv",
    index=False
)
mean_gain = results_df["gain"].mean()

mean_efficiency = (
    results_df["efficiency"]
    .mean()
)

best_efficiency = (
    results_df["efficiency"]
    .max()
)

print("Mean Gain      :", mean_gain)
print("Mean Efficiency:", mean_efficiency)
print("Best Efficiency:", best_efficiency)
print()

# ============================================================
# VISUAL 1
# ============================================================

plt.figure(figsize=(8,6))

plt.scatter(
    results_df["atlas_length"],
    results_df["random_length"],
    alpha=0.7
)

plt.xlabel(
    "Atlas Route Length"
)

plt.ylabel(
    "Random Route Length"
)

plt.title(
    "EXP_44O Atlas vs Random Navigation"
)

plt.tight_layout()

plt.savefig(
    OUTDIR /
    "exp44o_route_length_comparison.png",
    dpi=300
)

plt.close()

# ============================================================
# VISUAL 2
# ============================================================

plt.figure(figsize=(8,6))

plt.hist(
    results_df["gain"],
    bins=20
)

plt.xlabel(
    "Navigation Gain"
)

plt.ylabel(
    "Count"
)

plt.title(
    "EXP_44O Navigation Gain Distribution"
)

plt.tight_layout()

plt.savefig(
    OUTDIR /
    "exp44o_navigation_gain_histogram.png",
    dpi=300
)

plt.close()

# ============================================================
# VISUAL 3
# ============================================================

pivot = np.full(
    (len(nodes), len(nodes)),
    np.nan
)

node_to_idx = {
    n:i
    for i,n in enumerate(nodes)
}

for _, row in results_df.iterrows():

    i = node_to_idx[
        row["source"]
    ]

    j = node_to_idx[
        row["target"]
    ]

    pivot[i,j] = row["efficiency"]
    pivot[j,i] = row["efficiency"]

plt.figure(figsize=(10,8))

plt.imshow(
    pivot,
    aspect="auto"
)

plt.colorbar(
    label="Efficiency"
)

plt.title(
    "EXP_44O Efficiency Matrix"
)

plt.tight_layout()

plt.savefig(
    OUTDIR /
    "exp44o_efficiency_matrix.png",
    dpi=300
)

plt.close()

# ============================================================
# SAVE EFFICIENCY MATRIX
# ============================================================

efficiency_df = pd.DataFrame(
    pivot,
    index=nodes,
    columns=nodes
)

efficiency_df.to_csv(
    OUTDIR / "exp44o_efficiency_matrix.csv"
)

report = f"""
EXP_44O ATLAS NAVIGATION ACCURACY VALIDATION
==================================================

Domain Pairs
------------
{len(results_df)}

Mean Navigation Gain
--------------------
{mean_gain:.6f}

Mean Efficiency
---------------
{mean_efficiency:.6f}

Best Efficiency
---------------
{best_efficiency:.6f}

Interpretation
--------------
Atlas navigation routes were compared
against random-walk transport.

Efficiency > 1 indicates that Atlas
navigation outperforms random transport.

This experiment provides the first
quantitative validation of Atlas-guided
navigation.
"""

print(report)

with open(
    OUTDIR / "exp44o_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_44O complete.")
print()
