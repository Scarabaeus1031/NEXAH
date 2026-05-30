# ============================================================
# EXP_21B — CRITICAL BACKBONE REMOVAL
#
# Question:
# What happens if we remove the most important
# transport nodes in the discovered field?
#
# Scenarios:
#   Top 1% Betweenness
#   Top 3% Betweenness
#   Top 5% Betweenness
#
# Output:
#   exp21b_success.png
#   exp21b_steps.png
#   exp21b_component_size.png
#   exp21b_backbone_nodes.png
#   exp21b_results.csv
#   exp21b_summary.txt
# ============================================================

import os
import random
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from sklearn.neighbors import NearestNeighbors

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

INPUT_DIR = (
    "APPLICATIONS/power_systems/"
    "FIELD_NAVIGATION_VALIDATION/outputs/"
    "EXP_08_REAL_FIELD_GEOMETRY"
)

OUTPUT_DIR = (
    "APPLICATIONS/power_systems/"
    "FIELD_NAVIGATION_VALIDATION/outputs/"
    "EXP_21B_CRITICAL_BACKBONE_REMOVAL"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("\nInput  ->", os.path.abspath(INPUT_DIR))
print("Output ->", os.path.abspath(OUTPUT_DIR))

# ------------------------------------------------------------
# Load field
# ------------------------------------------------------------

df = pd.read_csv(
    os.path.join(INPUT_DIR, "exp08_field_states.csv")
)

coords = df[["pca_x", "pca_y"]].values

print("\nLoaded states:", len(coords))

# ------------------------------------------------------------
# Build graph
# ------------------------------------------------------------

K = 8

nbrs = NearestNeighbors(
    n_neighbors=K + 1
).fit(coords)

distances, indices = nbrs.kneighbors(coords)

G = nx.Graph()

for i in range(len(coords)):
    G.add_node(i)

for i in range(len(coords)):
    for j, d in zip(indices[i][1:], distances[i][1:]):
        G.add_edge(i, j, weight=float(d))

largest_component = max(
    nx.connected_components(G),
    key=len
)

G = G.subgraph(largest_component).copy()

print("Graph nodes:", G.number_of_nodes())
print("Graph edges:", G.number_of_edges())

# ------------------------------------------------------------
# Betweenness backbone
# ------------------------------------------------------------

print("\nComputing betweenness...")

bet = nx.betweenness_centrality(
    G,
    normalized=True
)

bet_df = pd.DataFrame({
    "node": list(bet.keys()),
    "betweenness": list(bet.values())
})

bet_df = bet_df.sort_values(
    "betweenness",
    ascending=False
)

# ------------------------------------------------------------
# Regions
# ------------------------------------------------------------

left_region = [
    n for n in G.nodes()
    if coords[n, 0] < -25
]

right_region = [
    n for n in G.nodes()
    if coords[n, 0] > 40
]

print("Left region :", len(left_region))
print("Right region:", len(right_region))

# ------------------------------------------------------------
# Navigation
# ------------------------------------------------------------

def field_navigation(
    graph,
    start,
    targets,
    max_steps=100
):

    current = start
    visited = {current}

    target_center = np.mean(
        coords[list(targets)],
        axis=0
    )

    for step in range(max_steps):

        if current in targets:
            return True, step

        nbrs = list(graph.neighbors(current))

        if not nbrs:
            break

        best = None
        best_score = np.inf

        for n in nbrs:

            if n in visited:
                continue

            score = np.linalg.norm(
                coords[n] - target_center
            )

            if score < best_score:
                best_score = score
                best = n

        if best is None:
            break

        current = best
        visited.add(current)

    return False, max_steps

# ------------------------------------------------------------
# Test scenarios
# ------------------------------------------------------------

SCENARIOS = [
    ("Top_1pct", 0.01),
    ("Top_3pct", 0.03),
    ("Top_5pct", 0.05),
]

results = []

# ------------------------------------------------------------
# Baseline
# ------------------------------------------------------------

N = 500

base_success = 0
base_steps = []

for _ in range(N):

    s = random.choice(left_region)

    ok, st = field_navigation(
        G,
        s,
        set(right_region)
    )

    base_success += int(ok)
    base_steps.append(st)

base_success /= N
base_steps = np.mean(base_steps)

print("\nBaseline Success:", round(base_success,4))
print("Baseline Steps  :", round(base_steps,4))

# ------------------------------------------------------------
# Ablations
# ------------------------------------------------------------

for name, frac in SCENARIOS:

    count = max(
        1,
        int(frac * G.number_of_nodes())
    )

    removed_nodes = (
        bet_df.head(count)["node"]
        .astype(int)
        .tolist()
    )

    G2 = G.copy()
    G2.remove_nodes_from(
        removed_nodes
    )

    if G2.number_of_nodes() == 0:
        continue

    largest_after = max(
        nx.connected_components(G2),
        key=len
    )

    G2 = G2.subgraph(
        largest_after
    ).copy()

    left2 = [
        n for n in left_region
        if n in G2
    ]

    right2 = [
        n for n in right_region
        if n in G2
    ]

    if len(left2) == 0 or len(right2) == 0:
        continue

    success = 0
    steps = []

    for _ in range(N):

        s = random.choice(left2)

        ok, st = field_navigation(
            G2,
            s,
            set(right2)
        )

        success += int(ok)
        steps.append(st)

    success /= N
    steps = np.mean(steps)

    results.append({
        "scenario": name,
        "removed_nodes": count,
        "success_rate": success,
        "avg_steps": steps,
        "remaining_nodes": G2.number_of_nodes()
    })

    print(
        f"\n{name}"
        f" | removed={count}"
        f" | success={success:.4f}"
        f" | steps={steps:.2f}"
    )

# ------------------------------------------------------------
# Results table
# ------------------------------------------------------------

res_df = pd.DataFrame(results)

res_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "exp21b_results.csv"
    ),
    index=False
)

# ------------------------------------------------------------
# Plot 1 Success
# ------------------------------------------------------------

plt.figure(figsize=(8,5))

plt.bar(
    res_df["scenario"],
    res_df["success_rate"]
)

plt.ylabel("Success Rate")
plt.title(
    "EXP_21B — Backbone Removal Success"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp21b_success.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Plot 2 Steps
# ------------------------------------------------------------

plt.figure(figsize=(8,5))

plt.bar(
    res_df["scenario"],
    res_df["avg_steps"]
)

plt.ylabel("Average Steps")
plt.title(
    "EXP_21B — Navigation Cost"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp21b_steps.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Plot 3 Component Size
# ------------------------------------------------------------

plt.figure(figsize=(8,5))

plt.bar(
    res_df["scenario"],
    res_df["remaining_nodes"]
)

plt.ylabel("Remaining Nodes")
plt.title(
    "EXP_21B — Surviving Backbone"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp21b_component_size.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Plot 4 Backbone nodes
# ------------------------------------------------------------

top_nodes = (
    bet_df.head(25)["node"]
    .astype(int)
    .tolist()
)

plt.figure(figsize=(9,7))

plt.scatter(
    coords[:,0],
    coords[:,1],
    s=20,
    alpha=0.25
)

plt.scatter(
    coords[top_nodes,0],
    coords[top_nodes,1],
    s=80
)

plt.title(
    "EXP_21B — Critical Backbone Nodes"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp21b_backbone_nodes.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

with open(
    os.path.join(
        OUTPUT_DIR,
        "exp21b_summary.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_21B CRITICAL BACKBONE REMOVAL\n"
    )

    f.write(
        "========================================\n\n"
    )

    f.write(
        f"Baseline Success: {base_success:.4f}\n"
    )

    f.write(
        f"Baseline Steps  : {base_steps:.4f}\n\n"
    )

    f.write(
        res_df.to_string(index=False)
    )

print("\nEXP_21B completed.")
