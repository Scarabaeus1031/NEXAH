#!/usr/bin/env python3
"""
EXP_39C — REAL TRANSITION NETWORK EXTRACTION

Extracts real state-transition networks from historical NEXAH runs.

Inputs:
    nexah_ieee9/results/**
    nexah_ieeeX/results/**

Looks for:
    states.txt
    actions.txt
    controller_actions.txt

Outputs:
    exp39c_state_sequences.csv
    exp39c_transition_edges.csv
    exp39c_transition_matrix.csv
    exp39c_state_centrality.csv
    exp39c_transition_network.png
    exp39c_report.txt
"""

from pathlib import Path
from collections import Counter
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[3]

REPO = ROOT

OUTPUT = (
    ROOT
    / "outputs"
    / "EXP_39C_REAL_TRANSITION_NETWORK_EXTRACTION"
)

OUTPUT.mkdir(parents=True, exist_ok=True)

print(f"Repository -> {REPO}")
print(f"Output     -> {OUTPUT}")


# ============================================================
# HELPERS
# ============================================================

def load_states(path):
    """
    Reads states.txt

    Accepts:
        state names
        integers
        labels

    One state per line.
    """

    states = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:

                s = line.strip()

                if not s:
                    continue

                states.append(s)

    except Exception:
        return []

    return states


# ============================================================
# DISCOVER STATE FILES
# ============================================================

state_files = list(REPO.rglob("states.txt"))

print()
print("State files discovered:", len(state_files))

sequence_rows = []
edge_counter = Counter()

runs_processed = 0

# ============================================================
# EXTRACT SEQUENCES
# ============================================================

for state_file in state_files:

    states = load_states(state_file)

    if len(states) < 2:
        continue

    run_name = state_file.parent.name

    runs_processed += 1

    for step, state in enumerate(states):

        sequence_rows.append(
            {
                "run": run_name,
                "step": step,
                "state": state,
            }
        )

    for i in range(len(states) - 1):

        src = states[i]
        dst = states[i + 1]

        if src == dst:
            continue

        edge_counter[(src, dst)] += 1


# ============================================================
# SAVE SEQUENCES
# ============================================================

seq_df = pd.DataFrame(sequence_rows)

seq_file = OUTPUT / "exp39c_state_sequences.csv"
seq_df.to_csv(seq_file, index=False)

print("Saved:", seq_file)


# ============================================================
# EDGE TABLE
# ============================================================

edge_rows = []

for (src, dst), count in edge_counter.items():

    edge_rows.append(
        {
            "from": src,
            "to": dst,
            "count": count,
        }
    )

edges_df = pd.DataFrame(edge_rows)

edges_df = edges_df.sort_values(
    "count",
    ascending=False
)

edges_file = OUTPUT / "exp39c_transition_edges.csv"
edges_df.to_csv(edges_file, index=False)

print("Saved:", edges_file)


# ============================================================
# TRANSITION MATRIX
# ============================================================

states_all = sorted(
    set(edges_df["from"]).union(
        set(edges_df["to"])
    )
)

matrix = pd.DataFrame(
    0,
    index=states_all,
    columns=states_all
)

for _, row in edges_df.iterrows():

    matrix.loc[row["from"], row["to"]] = row["count"]

matrix_file = OUTPUT / "exp39c_transition_matrix.csv"
matrix.to_csv(matrix_file)

print("Saved:", matrix_file)


# ============================================================
# GRAPH
# ============================================================

G = nx.DiGraph()

for _, row in edges_df.iterrows():

    G.add_edge(
        row["from"],
        row["to"],
        weight=row["count"]
    )

# ============================================================
# CENTRALITY
# ============================================================

if len(G.nodes) > 0:

    indeg = dict(G.in_degree())
    outdeg = dict(G.out_degree())

    bet = nx.betweenness_centrality(G)

    centrality_rows = []

    for node in G.nodes:

        centrality_rows.append(
            {
                "state": node,
                "in_degree": indeg.get(node, 0),
                "out_degree": outdeg.get(node, 0),
                "betweenness": bet.get(node, 0),
            }
        )

    cent_df = pd.DataFrame(centrality_rows)

else:

    cent_df = pd.DataFrame(
        columns=[
            "state",
            "in_degree",
            "out_degree",
            "betweenness",
        ]
    )

centrality_file = OUTPUT / "exp39c_state_centrality.csv"
cent_df.to_csv(centrality_file, index=False)

print("Saved:", centrality_file)


# ============================================================
# NETWORK FIGURE
# ============================================================

plt.figure(figsize=(12, 8))

if len(G.nodes) > 0:

    pos = nx.spring_layout(
        G,
        seed=42
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=1400
    )

    nx.draw_networkx_labels(
        G,
        pos
    )

    nx.draw_networkx_edges(
        G,
        pos,
        arrows=True
    )

plt.title("EXP_39C Real Transition Network")
plt.tight_layout()

network_file = OUTPUT / "exp39c_transition_network.png"

plt.savefig(
    network_file,
    dpi=300
)

plt.close()

print("Saved:", network_file)


# ============================================================
# REPORT
# ============================================================

unique_states = len(states_all)
unique_transitions = len(edges_df)

if len(edges_df) > 0:

    top = edges_df.iloc[0]

    top_transition = (
        f"{top['from']} -> {top['to']} "
        f"({top['count']})"
    )

else:

    top_transition = "N/A"

if len(cent_df) > 0:

    hub = cent_df.sort_values(
        "betweenness",
        ascending=False
    ).iloc[0]["state"]

else:

    hub = "N/A"

density = 0

if unique_states > 1:

    density = (
        unique_transitions
        /
        (unique_states * (unique_states - 1))
    )

report = f"""
EXP_39C REAL TRANSITION NETWORK EXTRACTION
==================================================

Runs Processed: {runs_processed}

Unique States: {unique_states}

Unique Transitions: {unique_transitions}

Most Common Transition:
{top_transition}

Most Connected State:
{hub}

Transition Density:
{density:.4f}
"""

report_file = OUTPUT / "exp39c_report.txt"

with open(report_file, "w") as f:
    f.write(report)

print("Saved:", report_file)

print()
print("EXP_39C complete.")
