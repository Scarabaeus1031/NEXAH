# ============================================================
# EXP_21 — BLOCKED FIELD NAVIGATION
#
# Can NEXAH still navigate when parts of the
# discovered field are removed?
#
# NEXAH Validation Program
# ============================================================

from pathlib import Path

import random
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from sklearn.neighbors import NearestNeighbors

# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_DIR = (
    BASE_DIR
    / "outputs"
    / "EXP_08_REAL_FIELD_GEOMETRY"
)

OUTPUT_DIR = (
    BASE_DIR
    / "outputs"
    / "EXP_21_BLOCKED_FIELD_NAVIGATION"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print()
print(f"Input  -> {INPUT_DIR}")
print(f"Output -> {OUTPUT_DIR}")
print()

# ============================================================
# Load Data
# ============================================================

df = pd.read_csv(
    INPUT_DIR / "exp08_field_states.csv"
)

coords = df[
    ["pca_x", "pca_y"]
].values

print(
    f"Loaded states: {len(coords)}"
)

# ============================================================
# Build kNN Graph
# ============================================================

K = 8

nbrs = NearestNeighbors(
    n_neighbors=K + 1
).fit(coords)

distances, indices = nbrs.kneighbors(coords)

G = nx.Graph()

for i in range(len(coords)):
    G.add_node(i)

for i in range(len(coords)):

    for j, d in zip(
        indices[i][1:],
        distances[i][1:]
    ):

        G.add_edge(
            i,
            j,
            weight=float(d)
        )

largest_component = max(
    nx.connected_components(G),
    key=len
)

G = G.subgraph(
    largest_component
).copy()

print(
    f"Graph nodes: {G.number_of_nodes()}"
)

print(
    f"Graph edges: {G.number_of_edges()}"
)

# ============================================================
# Create Damage Region
# ============================================================

nodes = np.array(
    list(G.nodes())
)

xs = coords[nodes, 0]
ys = coords[nodes, 1]

# ------------------------------------------------------------
# Adaptive central corridor damage
# ------------------------------------------------------------

x_min = np.percentile(xs, 35)
x_max = np.percentile(xs, 65)

y_min = np.percentile(ys, 35)
y_max = np.percentile(ys, 65)

blocked_mask = (
    (xs > x_min)
    & (xs < x_max)
    & (ys > y_min)
    & (ys < y_max)
)

blocked_nodes = nodes[
    blocked_mask
]

print()
print(
    f"Blocked nodes: {len(blocked_nodes)}"
)

G_blocked = G.copy()

G_blocked.remove_nodes_from(
    blocked_nodes
)

if G_blocked.number_of_nodes() == 0:
    raise RuntimeError(
        "Blocked graph became empty."
    )

largest_after = max(
    nx.connected_components(G_blocked),
    key=len
)

G_blocked = G_blocked.subgraph(
    largest_after
).copy()

print(
    f"Remaining nodes: {G_blocked.number_of_nodes()}"
)

# ============================================================
# Define Left / Right Regions
# ============================================================

left_threshold = np.percentile(
    coords[:, 0],
    20
)

right_threshold = np.percentile(
    coords[:, 0],
    80
)

left_region = [
    n for n in G.nodes()
    if coords[n, 0] < left_threshold
]

right_region = [
    n for n in G.nodes()
    if coords[n, 0] > right_threshold
]

left_region_blocked = [
    n for n in left_region
    if n in G_blocked
]

right_region_blocked = [
    n for n in right_region
    if n in G_blocked
]

print(
    f"Left region : {len(left_region_blocked)}"
)

print(
    f"Right region: {len(right_region_blocked)}"
)

# ============================================================
# Navigation
# ============================================================

def field_navigation(
    graph,
    start,
    targets,
    max_steps=100
):

    if len(targets) == 0:
        return False, max_steps

    current = start

    visited = {current}

    target_center = np.mean(
        coords[list(targets)],
        axis=0
    )

    for step in range(max_steps):

        if current in targets:
            return True, step

        neighbors = list(
            graph.neighbors(current)
        )

        if len(neighbors) == 0:
            return False, max_steps

        best_node = None
        best_score = np.inf

        for n in neighbors:

            if n in visited:
                continue

            score = np.linalg.norm(
                coords[n] - target_center
            )

            if score < best_score:

                best_score = score
                best_node = n

        if best_node is None:
            return False, max_steps

        current = best_node

        visited.add(current)

    return False, max_steps

# ============================================================
# Trials
# ============================================================

random.seed(42)
np.random.seed(42)

N = 500

success_original = 0
success_blocked = 0

steps_original = []
steps_blocked = []

# ------------------------------------------------------------
# Original Field
# ------------------------------------------------------------

for _ in range(N):

    start = random.choice(
        left_region
    )

    ok, steps = field_navigation(
        G,
        start,
        set(right_region)
    )

    success_original += int(ok)

    steps_original.append(steps)

# ------------------------------------------------------------
# Damaged Field
# ------------------------------------------------------------

for _ in range(N):

    if (
        len(left_region_blocked) == 0
        or len(right_region_blocked) == 0
    ):
        break

    start = random.choice(
        left_region_blocked
    )

    ok, steps = field_navigation(
        G_blocked,
        start,
        set(right_region_blocked)
    )

    success_blocked += int(ok)

    steps_blocked.append(steps)

# ============================================================
# Metrics
# ============================================================

orig_rate = (
    success_original / N
)

blocked_rate = (
    success_blocked
    / max(1, len(steps_blocked))
)

orig_steps = np.mean(
    steps_original
)

blocked_steps = (
    np.mean(steps_blocked)
    if len(steps_blocked) > 0
    else np.nan
)

print()
print(
    f"Original Success: {orig_rate:.4f}"
)

print(
    f"Blocked Success : {blocked_rate:.4f}"
)

print()

print(
    f"Original Steps : {orig_steps:.4f}"
)

print(
    f"Blocked Steps  : {blocked_steps:.4f}"
)

# ============================================================
# Plot 1
# ============================================================

plt.figure(
    figsize=(7, 5)
)

plt.bar(
    ["Original", "Blocked"],
    [orig_rate, blocked_rate]
)

plt.ylabel(
    "Success Rate"
)

plt.title(
    "EXP_21 Navigation Success"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp21_navigation_success.png",
    dpi=300
)

plt.close()

# ============================================================
# Plot 2
# ============================================================

plt.figure(
    figsize=(7, 5)
)

plt.bar(
    ["Original", "Blocked"],
    [orig_steps, blocked_steps]
)

plt.ylabel(
    "Average Steps"
)

plt.title(
    "EXP_21 Arrival Steps"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp21_arrival_steps.png",
    dpi=300
)

plt.close()

# ============================================================
# Plot 3
# ============================================================

plt.figure(
    figsize=(9, 7)
)

plt.scatter(
    coords[:, 0],
    coords[:, 1],
    s=20,
    alpha=0.25,
    label="Field"
)

if len(blocked_nodes) > 0:

    plt.scatter(
        coords[blocked_nodes, 0],
        coords[blocked_nodes, 1],
        s=30,
        label="Blocked"
    )

plt.legend()

plt.title(
    "EXP_21 Blocked Field Region"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp21_blocked_field.png",
    dpi=300
)

plt.close()

# ============================================================
# Summary
# ============================================================

with open(
    OUTPUT_DIR / "exp21_summary.txt",
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

    f.write(
        f"Blocked Nodes   : {len(blocked_nodes)}\n"
    )

    f.write(
        f"Remaining Nodes : {G_blocked.number_of_nodes()}\n"
    )

print()
print("EXP_21 completed.")
print()
