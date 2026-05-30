# ============================================================
# EXP_24 — OUT OF DISTRIBUTION NAVIGATION
#
# Can NEXAH navigate into unseen field regions?
#
# Training Field:
#     x < 20
#
# Hidden Region:
#     x >= 20
#
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
    "EXP_24_OUT_OF_DISTRIBUTION_NAVIGATION"
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
# Graph
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
# Training / Hidden split
# ------------------------------------------------------------

nodes = np.array(list(G.nodes()))

known_nodes = [
    n for n in nodes
    if coords[n,0] < 20
]

hidden_nodes = [
    n for n in nodes
    if coords[n,0] >= 20
]

print("\nKnown nodes :", len(known_nodes))
print("Hidden nodes:", len(hidden_nodes))

# ------------------------------------------------------------
# Regions
# ------------------------------------------------------------

start_nodes = [
    n for n in known_nodes
    if coords[n,0] < -25
]

target_nodes = [
    n for n in hidden_nodes
    if coords[n,0] > 40
]

print("Start nodes :", len(start_nodes))
print("Target nodes:", len(target_nodes))

# ------------------------------------------------------------
# Navigation
# ------------------------------------------------------------

def navigate(start, targets):

    current = start
    visited = {current}

    target_center = np.mean(
        coords[list(targets)],
        axis=0
    )

    for step in range(100):

        if current in targets:
            return True, step

        nbrs = list(G.neighbors(current))

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

    return False, 100

# ------------------------------------------------------------
# Trials
# ------------------------------------------------------------

N = 500

success = 0
steps = []

for _ in range(N):

    s = random.choice(start_nodes)

    ok, st = navigate(
        s,
        set(target_nodes)
    )

    success += int(ok)
    steps.append(st)

success_rate = success / N
avg_steps = np.mean(steps)

print("\nSuccess:", round(success_rate,4))
print("Steps  :", round(avg_steps,4))

# ------------------------------------------------------------
# Visual
# ------------------------------------------------------------

plt.figure(figsize=(10,7))

plt.scatter(
    coords[:,0],
    coords[:,1],
    s=25,
    alpha=0.2,
    label="Field"
)

plt.scatter(
    coords[known_nodes,0],
    coords[known_nodes,1],
    s=20,
    label="Known"
)

plt.axvline(
    20,
    linestyle="--"
)

plt.title(
    "EXP_24 Out-of-Distribution Split"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp24_ood_split.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Success
# ------------------------------------------------------------

plt.figure(figsize=(6,5))

plt.bar(
    ["OOD Navigation"],
    [success_rate]
)

plt.ylim(0,1.05)

plt.ylabel("Success Rate")

plt.title(
    "EXP_24 Success"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp24_success.png"
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
        "exp24_summary.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_24 OUT OF DISTRIBUTION NAVIGATION\n"
    )
    f.write(
        "========================================\n\n"
    )

    f.write(
        f"Known Nodes  : {len(known_nodes)}\n"
    )

    f.write(
        f"Hidden Nodes : {len(hidden_nodes)}\n"
    )

    f.write(
        f"Success Rate : {success_rate:.4f}\n"
    )

    f.write(
        f"Average Steps: {avg_steps:.4f}\n"
    )

print("\nEXP_24 completed.")
