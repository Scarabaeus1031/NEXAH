# ============================================================
# EXP_39_ATLAS_TRANSITION_NETWORK
#
# Goal:
# Build the first basin-to-basin transition network
# from reconstructed atlas basin sequences.
#
# Input:
# EXP_37B_MULTI_SYSTEM_BASIN_EXTRACTION
#
# Output:
# EXP_39_ATLAS_TRANSITION_NETWORK
#
# Thomas Hofmann / NEXAH
# ============================================================

from pathlib import Path

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import networkx as nx


# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

INPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_37B_MULTI_SYSTEM_BASIN_EXTRACTION"
)

OUTPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_39_ATLAS_TRANSITION_NETWORK"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Input  ->", INPUT_DIR)
print("Output ->", OUTPUT_DIR)


# ============================================================
# Discover basin files
# ============================================================

basin_files = sorted(
    INPUT_DIR.glob("*_basins.csv")
)

if not basin_files:
    raise FileNotFoundError(
        "No basin files found."
    )


# ============================================================
# Containers
# ============================================================

all_edges = []
centrality_rows = []

G_global = nx.DiGraph()


# ============================================================
# Process Systems
# ============================================================

for file in basin_files:

    system = (
        file.stem
        .replace("_basins", "")
        .upper()
    )

    print("\n" + "=" * 50)
    print(system)
    print("=" * 50)

    df = pd.read_csv(file)

    basin_col = None

    for candidate in [
        "basin",
        "basin_id",
        "cluster",
        "state"
    ]:
        if candidate in df.columns:
            basin_col = candidate
            break

    if basin_col is None:
        print("No basin column found.")
        continue

    sequence = (
        df[basin_col]
        .astype(str)
        .tolist()
    )

    transitions = []

    for i in range(
        len(sequence) - 1
    ):

        src = sequence[i]
        dst = sequence[i + 1]

        if src == dst:
            continue

        transitions.append(
            (src, dst)
        )

    if len(transitions) == 0:
        continue

    edge_df = (
        pd.DataFrame(
            transitions,
            columns=[
                "source",
                "target"
            ]
        )
        .groupby(
            ["source", "target"]
        )
        .size()
        .reset_index(
            name="count"
        )
    )

    edge_df["system"] = system

    all_edges.append(edge_df)

    # ----------------------------------------
    # Transition Matrix
    # ----------------------------------------

    matrix = pd.pivot_table(
        edge_df,
        index="source",
        columns="target",
        values="count",
        fill_value=0
    )

    matrix.to_csv(
        OUTPUT_DIR
        / f"{system.lower()}_transition_matrix.csv"
    )

    # ----------------------------------------
    # Graph
    # ----------------------------------------

    G = nx.DiGraph()

    for _, row in edge_df.iterrows():

        G.add_edge(
            row["source"],
            row["target"],
            weight=row["count"]
        )

        G_global.add_edge(
            f"{system}_{row['source']}",
            f"{system}_{row['target']}",
            weight=row["count"]
        )

    # ----------------------------------------
    # Centrality
    # ----------------------------------------

    deg = dict(
        G.degree()
    )

    indeg = dict(
        G.in_degree()
    )

    outdeg = dict(
        G.out_degree()
    )

    btw = nx.betweenness_centrality(
        G
    )

    for node in G.nodes():

        centrality_rows.append({

            "system":
                system,

            "basin":
                node,

            "degree":
                deg.get(node, 0),

            "in_degree":
                indeg.get(node, 0),

            "out_degree":
                outdeg.get(node, 0),

            "betweenness":
                btw.get(node, 0)
        })

    # ----------------------------------------
    # Network Plot
    # ----------------------------------------

    plt.figure(
        figsize=(8, 6)
    )

    pos = nx.spring_layout(
        G,
        seed=42
    )

    weights = [
        G[u][v]["weight"]
        for u, v in G.edges()
    ]

    nx.draw_networkx(
        G,
        pos,
        with_labels=True,
        node_size=1500,
        width=np.array(weights) / max(weights) * 5
    )

    plt.title(
        f"{system} Transition Network"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / f"{system.lower()}_transition_network.png",
        dpi=300
    )

    plt.close()

    print(
        f"Basins: {len(G.nodes())}"
    )
    print(
        f"Transitions: {len(edge_df)}"
    )


# ============================================================
# Merge Edge Tables
# ============================================================

if all_edges:

    edge_master = pd.concat(
        all_edges,
        ignore_index=True
    )

    edge_master.to_csv(
        OUTPUT_DIR
        / "exp39_transition_edges.csv",
        index=False
    )

    print(
        "\nSaved:",
        OUTPUT_DIR
        / "exp39_transition_edges.csv"
    )


# ============================================================
# Centrality Table
# ============================================================

centrality_df = pd.DataFrame(
    centrality_rows
)

centrality_df.to_csv(
    OUTPUT_DIR
    / "exp39_basin_centrality.csv",
    index=False
)

print(
    "Saved:",
    OUTPUT_DIR
    / "exp39_basin_centrality.csv"
)


# ============================================================
# Global Network
# ============================================================

if len(G_global.nodes()) > 0:

    plt.figure(
        figsize=(10, 8)
    )

    pos = nx.spring_layout(
        G_global,
        seed=42
    )

    nx.draw_networkx(
        G_global,
        pos,
        node_size=1200,
        font_size=8
    )

    plt.title(
        "EXP_39 Global Atlas Transition Network"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / "exp39_global_transition_network.png",
        dpi=300
    )

    plt.close()


# ============================================================
# Report
# ============================================================

report = []

report.append(
    "EXP_39 ATLAS TRANSITION NETWORK"
)

report.append(
    "=" * 50
)

report.append("")

report.append(
    f"Systems analyzed: "
    f"{centrality_df['system'].nunique()}"
)

report.append("")

for system in sorted(
    centrality_df["system"].unique()
):

    n_basins = len(
        centrality_df[
            centrality_df["system"] == system
        ]
    )

    report.append(
        f"{system}: "
        f"{n_basins} basins"
    )

report_path = (
    OUTPUT_DIR
    / "exp39_report.txt"
)

with open(
    report_path,
    "w"
) as f:

    f.write(
        "\n".join(report)
    )

print(
    "Saved:",
    report_path
)

print(
    "\nEXP_39 complete."
)
