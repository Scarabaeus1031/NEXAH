# ============================================================
# EXP_22 — PARTIAL KNOWLEDGE BENCHMARK
#
# Question:
# How much field knowledge is required before
# NEXAH navigation becomes effective?
#
# Compare:
#   Random Navigation
#   NEXAH 25%
#   NEXAH 50%
#   NEXAH 75%
#   NEXAH 100%
#
# Output:
#   exp22_success_vs_knowledge.png
#   exp22_steps_vs_knowledge.png
#   exp22_known_field_examples.png
#   exp22_summary.txt
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
    / "EXP_22_PARTIAL_KNOWLEDGE_BENCHMARK"
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
# Build Graph
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
# Regions
# ============================================================

left_region = [
    n for n in G.nodes()
    if coords[n, 0] < -25
]

right_region = [
    n for n in G.nodes()
    if coords[n, 0] > 40
]

print()
print(
    f"Left region : {len(left_region)}"
)

print(
    f"Right region: {len(right_region)}"
)

target_center = np.mean(
    coords[right_region],
    axis=0
)

# ============================================================
# Random Navigation
# ============================================================

def random_navigation(
    graph,
    start,
    targets,
    max_steps=100
):

    current = start

    visited = {current}

    for step in range(max_steps):

        if current in targets:
            return True, step

        neighbors = list(
            graph.neighbors(current)
        )

        if not neighbors:
            return False, max_steps

        neighbors = [
            n for n in neighbors
            if n not in visited
        ]

        if not neighbors:
            return False, max_steps

        current = random.choice(
            neighbors
        )

        visited.add(current)

    return False, max_steps

# ============================================================
# Partial Knowledge Navigation
# ============================================================

def partial_navigation(
    graph,
    start,
    targets,
    known_nodes,
    max_steps=100
):

    current = start

    visited = {current}

    for step in range(max_steps):

        if current in targets:
            return True, step

        neighbors = list(
            graph.neighbors(current)
        )

        if not neighbors:
            return False, max_steps

        candidates = []

        for n in neighbors:

            if n in visited:
                continue

            if n in known_nodes:

                score = np.linalg.norm(
                    coords[n]
                    - target_center
                )

            else:
                score = 1e6

            candidates.append(
                (score, n)
            )

        if not candidates:
            return False, max_steps

        candidates.sort()

        current = candidates[0][1]

        visited.add(current)

    return False, max_steps

# ============================================================
# Benchmark
# ============================================================

random.seed(42)
np.random.seed(42)

N = 500

knowledge_levels = [
    0.25,
    0.50,
    0.75,
    1.00
]

results = []

# ============================================================
# Random Baseline
# ============================================================

success = 0
steps = []

for _ in range(N):

    start = random.choice(
        left_region
    )

    ok, st = random_navigation(
        G,
        start,
        set(right_region)
    )

    success += int(ok)
    steps.append(st)

random_success = success / N
random_steps = np.mean(steps)

results.append({
    "knowledge": "Random",
    "success": random_success,
    "steps": random_steps
})

print(
    f"\nRandom Success: {random_success:.4f}"
)

print(
    f"Random Steps  : {random_steps:.4f}"
)

# ============================================================
# Partial Knowledge Tests
# ============================================================

all_nodes = np.array(
    list(G.nodes())
)

for frac in knowledge_levels:

    n_known = int(
        frac * len(all_nodes)
    )

    known_nodes = set(
        np.random.choice(
            all_nodes,
            size=n_known,
            replace=False
        )
    )

    success = 0
    steps = []

    for _ in range(N):

        start = random.choice(
            left_region
        )

        ok, st = partial_navigation(
            G,
            start,
            set(right_region),
            known_nodes
        )

        success += int(ok)
        steps.append(st)

    success_rate = success / N
    mean_steps = np.mean(steps)

    results.append({
        "knowledge": f"{int(frac*100)}%",
        "success": success_rate,
        "steps": mean_steps
    })

    print()

    print(
        f"Knowledge {int(frac*100)}%"
    )

    print(
        f"Success : {success_rate:.4f}"
    )

    print(
        f"Steps   : {mean_steps:.4f}"
    )

# ============================================================
# Results Table
# ============================================================

res_df = pd.DataFrame(
    results
)

res_df.to_csv(
    OUTPUT_DIR
    / "exp22_results.csv",
    index=False
)

# ============================================================
# Plot 1
# ============================================================

plt.figure(
    figsize=(8,5)
)

plt.bar(
    res_df["knowledge"],
    res_df["success"]
)

plt.ylabel(
    "Success Rate"
)

plt.title(
    "EXP_22 Success vs Knowledge"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp22_success_vs_knowledge.png",
    dpi=300
)

plt.close()

# ============================================================
# Plot 2
# ============================================================

plt.figure(
    figsize=(8,5)
)

plt.bar(
    res_df["knowledge"],
    res_df["steps"]
)

plt.ylabel(
    "Average Steps"
)

plt.title(
    "EXP_22 Steps vs Knowledge"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp22_steps_vs_knowledge.png",
    dpi=300
)

plt.close()

# ============================================================
# Plot 3
# ============================================================

fig, axes = plt.subplots(
    2,
    2,
    figsize=(10,8)
)

for ax, frac in zip(
    axes.flatten(),
    knowledge_levels
):

    n_known = int(
        frac * len(all_nodes)
    )

    known_nodes = set(
        np.random.choice(
            all_nodes,
            size=n_known,
            replace=False
        )
    )

    ax.scatter(
        coords[:,0],
        coords[:,1],
        s=10,
        alpha=0.15
    )

    ax.scatter(
        coords[list(known_nodes),0],
        coords[list(known_nodes),1],
        s=12
    )

    ax.set_title(
        f"{int(frac*100)}% Known"
    )

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp22_known_field_examples.png",
    dpi=300
)

plt.close()

# ============================================================
# Summary
# ============================================================

with open(
    OUTPUT_DIR
    / "exp22_summary.txt",
    "w"
) as f:

    f.write(
        "EXP_22 PARTIAL KNOWLEDGE BENCHMARK\n"
    )

    f.write(
        "========================================\n\n"
    )

    f.write(
        res_df.to_string(index=False)
    )

print()
print("EXP_22 completed.")
print()
