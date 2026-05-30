# ============================================================
# EXP_21 — BLOCKED FIELD NAVIGATION
#
# Question:
# Can NEXAH still navigate successfully when parts
# of the discovered field are removed?
#
# We compare:
#   1. Original field
#   2. Damaged field
#
# Output:
#   exp21_navigation_success.png
#   exp21_arrival_steps.png
#   exp21_blocked_field.png
#   exp21_summary.txt
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
    "EXP_21_BLOCKED_FIELD_NAVIGATION"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("\nInput  ->", os.path.abspath(INPUT_DIR))
print("Output ->", os.path.abspath(OUTPUT_DIR))

# ------------------------------------------------------------
# Load states
# ------------------------------------------------------------

df = pd.read_csv(
    os.path.join(INPUT_DIR, "exp08_field_states.csv")
)

coords = df[["x", "y"]].values

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
# Define damaged region
# ------------------------------------------------------------

nodes = np.array(list(G.nodes()))

xs = coords[nodes, 0]
ys = coords[nodes, 1]

# central field region

blocked_mask = (
    (xs > -5)
    & (xs < 25)
    & (ys > -2)
    & (ys < 12)
)

blocked_nodes = nodes[blocked_mask]

print("\nBlocked nodes:", len(blocked_nodes))

G_blocked = G.copy()
G_blocked.remove_nodes_from(blocked_nodes)

# largest surviving component

largest_after = max(
    nx.connected_components(G_blocked),
    key=len
)

G_blocked = G_blocked.subgraph(
    largest_after
).copy()

print(
    "Remaining nodes:",
    G_blocked.number_of_nodes()
)

# ------------------------------------------------------------
# Region definitions
# ------------------------------------------------------------

left_region = [
    n for n in G.nodes()
    if coords[n, 0] < -25
]

right_region = [
    n for n in G.nodes()
    if coords[n, 0] > 40
]

left_region_blocked = [
    n for n in left_region
    if n in G_blocked
]

right_region_blocked = [
    n for n in right_region
    if n in G_blocked
]

print("Left region :", len(left_region_blocked))
print("Right region:", len(right_region_blocked))

# ------------------------------------------------------------
# Navigation function
# ------------------------------------------------------------

def field_navigation(graph, start, targets, max_steps=100):

    current = start
    visited = {current}

    for step in range(max_steps):

        if current in targets:
            return True, step

        nbrs = list(graph.neighbors(current))

        if not nbrs:
            break

        target_center = np.mean(
            coords[list(targets)],
            axis=0
        )

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
# Trials
# ------------------------------------------------------------

N = 500

success_original = 0
steps_original = []

success_blocked = 0
steps_blocked = []

for _ in range(N):

    s = random.choice(left_region)

    ok, st = field_navigation(
        G,
        s,
        set(right_region)
    )

    success_original += int(ok)
    steps_original.append(st)

for _ in range(N):

    if not left_region_blocked:
        break

    s = random.choice(
        left_region_blocked
    )

    ok, st = field_navigation(
        G_blocked,
        s,
        set(right_region_blocked)
    )

    success_blocked += int(ok)
    steps_blocked.append(st)

# ------------------------------------------------------------
# Metrics
# ------------------------------------------------------------

orig_rate = success_original / N

blocked_rate = (
    success_blocked /
    max(1, len(steps_blocked))
)

orig_steps = np.mean(steps_original)

blocked_steps = np.mean(steps_blocked)

print("\nOriginal Success:", round(orig_rate, 4))
print("Blocked Success :", round(blocked_rate, 4))

print("Original Steps :", round(orig_steps, 4))
print("Blocked Steps  :", round(blocked_steps, 4))

# ------------------------------------------------------------
# Plot 1
# ------------------------------------------------------------

plt.figure(figsize=(7, 5))

plt.bar(
    ["Original", "Blocked"],
    [orig_rate, blocked_rate]
)

plt.ylabel("Success Rate")
plt.title("EXP_21 — Navigation Success")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp21_navigation_success.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Plot 2
# ------------------------------------------------------------

plt.figure(figsize=(7, 5))

plt.bar(
    ["Original", "Blocked"],
    [orig_steps, blocked_steps]
)

plt.ylabel("Average Steps")
plt.title("EXP_21 — Arrival Steps")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp21_arrival_steps.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Plot 3
# ------------------------------------------------------------

plt.figure(figsize=(9, 7))

plt.scatter(
    coords[:, 0],
    coords[:, 1],
    s=20,
    alpha=0.25
)

plt.scatter(
    coords[blocked_nodes, 0],
    coords[blocked_nodes, 1],
    s=30
)

plt.title(
    "EXP_21 — Blocked Field Region"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp21_blocked_field.png"
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
        "exp21_summary.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_21 BLOCKED FIELD NAVIGATION\n"
    )
    f.write(
        "========================================\n\n"
    )

    f.write(
        f"Original Success: {orig_rate:.4f}\n"
    )
    f.write(
        f"Blocked Success : {blocked_rate:.4f}\n"
    )

    f.write(
        f"Original Steps  : {orig_steps:.4f}\n"
    )
    f.write(
        f"Blocked Steps   : {blocked_steps:.4f}\n"
    )

print("\nEXP_21 completed.")
