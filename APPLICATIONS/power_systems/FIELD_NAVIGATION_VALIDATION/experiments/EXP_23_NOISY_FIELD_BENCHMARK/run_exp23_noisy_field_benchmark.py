# ============================================================
# EXP_23 — NOISY FIELD BENCHMARK
#
# Question:
# How robust is NEXAH navigation when the field
# geometry becomes increasingly inaccurate?
#
# We compare:
#   Random
#   0% Noise
#   10% Noise
#   20% Noise
#   30% Noise
#   40% Noise
#   50% Noise
#
# Output:
#   exp23_success_vs_noise.png
#   exp23_steps_vs_noise.png
#   exp23_noisy_field_examples.png
#   exp23_summary.txt
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
    "EXP_23_NOISY_FIELD_BENCHMARK"
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

print("\nLeft region :", len(left_region))
print("Right region:", len(right_region))

target_center = np.mean(
    coords[right_region],
    axis=0
)

# ------------------------------------------------------------
# Navigation
# ------------------------------------------------------------

def field_navigation(
    graph,
    noisy_coords,
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
            break

        best = None
        best_score = np.inf

        for n in neighbors:

            if n in visited:
                continue

            score = np.linalg.norm(
                noisy_coords[n]
                - target_center
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
# Noise levels
# ------------------------------------------------------------

noise_levels = [
    0,
    10,
    20,
    30,
    40,
    50
]

results = []

# ------------------------------------------------------------
# Random baseline
# ------------------------------------------------------------

success = 0
steps = []

N = 500

for _ in range(N):

    current = random.choice(
        left_region
    )

    visited = {current}

    for step in range(100):

        if current in right_region:
            success += 1
            steps.append(step)
            break

        nbrs = list(
            G.neighbors(current)
        )

        nbrs = [
            n for n in nbrs
            if n not in visited
        ]

        if not nbrs:
            steps.append(100)
            break

        current = random.choice(nbrs)
        visited.add(current)

    else:
        steps.append(100)

results.append([
    "Random",
    success / N,
    np.mean(steps)
])

print("\nRandom Success:",
      round(success / N, 4))

# ------------------------------------------------------------
# Noise benchmark
# ------------------------------------------------------------

examples = {}

for noise_pct in noise_levels:

    noisy_coords = coords.copy()

    n_noise = int(
        len(noisy_coords)
        * noise_pct
        / 100
    )

    idx = np.random.choice(
        len(noisy_coords),
        n_noise,
        replace=False
    )

    sigma = 15.0

    noisy_coords[idx] += (
        np.random.randn(
            n_noise,
            2
        ) * sigma
    )

    if noise_pct in [10, 30, 50]:
        examples[noise_pct] = noisy_coords.copy()

    success = 0
    steps = []

    for _ in range(N):

        start = random.choice(
            left_region
        )

        ok, st = field_navigation(
            G,
            noisy_coords,
            start,
            set(right_region)
        )

        success += int(ok)
        steps.append(st)

    rate = success / N
    avg_steps = np.mean(steps)

    results.append([
        f"{noise_pct}%",
        rate,
        avg_steps
    ])

    print(
        f"\nNoise {noise_pct}%"
    )

    print(
        "Success:",
        round(rate, 4)
    )

    print(
        "Steps  :",
        round(avg_steps, 4)
    )

# ------------------------------------------------------------
# DataFrame
# ------------------------------------------------------------

res = pd.DataFrame(
    results,
    columns=[
        "noise",
        "success",
        "steps"
    ]
)

# ------------------------------------------------------------
# Plot 1
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.bar(
    res["noise"],
    res["success"]
)

plt.ylabel("Success Rate")

plt.title(
    "EXP_23 Success vs Noise"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp23_success_vs_noise.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Plot 2
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.bar(
    res["noise"],
    res["steps"]
)

plt.ylabel("Average Steps")

plt.title(
    "EXP_23 Steps vs Noise"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp23_steps_vs_noise.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Plot 3
# ------------------------------------------------------------

fig, axes = plt.subplots(
    1,
    3,
    figsize=(15, 5)
)

for ax, noise in zip(
    axes,
    [10, 30, 50]
):

    ax.scatter(
        coords[:, 0],
        coords[:, 1],
        alpha=0.2
    )

    noisy = examples[noise]

    ax.scatter(
        noisy[:, 0],
        noisy[:, 1],
        s=10
    )

    ax.set_title(
        f"{noise}% Noise"
    )

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp23_noisy_field_examples.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

res.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "exp23_summary.csv"
    ),
    index=False
)

with open(
    os.path.join(
        OUTPUT_DIR,
        "exp23_summary.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_23 NOISY FIELD BENCHMARK\n"
    )

    f.write(
        "========================================\n\n"
    )

    f.write(
        res.to_string(index=False)
    )

print("\nEXP_23 completed.")
