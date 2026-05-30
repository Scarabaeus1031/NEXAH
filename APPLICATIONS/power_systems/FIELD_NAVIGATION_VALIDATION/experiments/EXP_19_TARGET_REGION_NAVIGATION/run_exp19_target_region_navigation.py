"""
run_exp19_target_region_navigation.py

EXP_19 — TARGET REGION NAVIGATION

Goal
-----
Test whether field-aware steering can navigate
from the left field region into the right field region
more efficiently than random motion.

This is the first direct navigation experiment.

Question:

Can NEXAH use discovered field geometry
to reach desired target regions?

Input
-----
EXP_08_REAL_FIELD_GEOMETRY
    exp08_field_states.csv

Output
------
outputs/EXP_19_TARGET_REGION_NAVIGATION/

NEXAH Validation Program
2026
"""

from pathlib import Path

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import networkx as nx
from scipy.spatial import KDTree


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
    / "EXP_19_TARGET_REGION_NAVIGATION"
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
# Load Field
# ============================================================

df = pd.read_csv(
    INPUT_DIR / "exp08_field_states.csv"
)

Z = df[
    ["pca_x", "pca_y"]
].values

print(
    f"Loaded states: {len(df)}"
)


# ============================================================
# Build Graph
# ============================================================

k_neighbors = 8

tree = KDTree(Z)

G = nx.Graph()

for i in range(len(Z)):
    G.add_node(i)

for i in range(len(Z)):

    distances, neighbors = tree.query(
        Z[i],
        k=k_neighbors + 1
    )

    for dist, j in zip(
        distances[1:],
        neighbors[1:]
    ):
        G.add_edge(
            i,
            j,
            weight=float(dist)
        )

largest_cc = max(
    nx.connected_components(G),
    key=len
)

G = G.subgraph(
    largest_cc
).copy()

nodes = list(
    G.nodes()
)

print(
    f"Graph nodes: {G.number_of_nodes()}"
)

print(
    f"Graph edges: {G.number_of_edges()}"
)

print()


# ============================================================
# Define Regions
# ============================================================

left_region = [
    n
    for n in nodes
    if Z[n, 0] < -25
]

right_region = [
    n
    for n in nodes
    if Z[n, 0] > 40
]

print(
    f"Left region : {len(left_region)}"
)

print(
    f"Right region: {len(right_region)}"
)

print()

if len(left_region) == 0:
    raise RuntimeError(
        "Left region empty."
    )

if len(right_region) == 0:
    raise RuntimeError(
        "Right region empty."
    )


# ============================================================
# Region Center
# ============================================================

target_center = np.mean(
    Z[right_region],
    axis=0
)


# ============================================================
# Navigation Models
# ============================================================

MAX_STEPS = 100

N_TRIALS = 500


def run_random_navigation(start):

    current = start

    for step in range(MAX_STEPS):

        if current in right_region:
            return True, step

        neighbors = list(
            G.neighbors(current)
        )

        if not neighbors:
            break

        current = random.choice(
            neighbors
        )

    return False, MAX_STEPS


def run_nexah_navigation(start):

    current = start

    for step in range(MAX_STEPS):

        if current in right_region:
            return True, step

        neighbors = list(
            G.neighbors(current)
        )

        if not neighbors:
            break

        best_neighbor = None
        best_distance = np.inf

        for n in neighbors:

            d = np.linalg.norm(
                Z[n] - target_center
            )

            if d < best_distance:
                best_distance = d
                best_neighbor = n

        current = best_neighbor

    return False, MAX_STEPS


# ============================================================
# Execute Trials
# ============================================================

random_success = 0
nexah_success = 0

random_steps = []
nexah_steps = []

trajectory_examples = []

for i in range(N_TRIALS):

    start = random.choice(
        left_region
    )

    success_r, steps_r = run_random_navigation(
        start
    )

    success_n, steps_n = run_nexah_navigation(
        start
    )

    random_success += int(success_r)
    nexah_success += int(success_n)

    random_steps.append(
        steps_r
    )

    nexah_steps.append(
        steps_n
    )

    if len(trajectory_examples) < 10:
        trajectory_examples.append(
            start
        )


random_success_rate = (
    random_success / N_TRIALS
)

nexah_success_rate = (
    nexah_success / N_TRIALS
)

random_mean_steps = np.mean(
    random_steps
)

nexah_mean_steps = np.mean(
    nexah_steps
)

navigation_gain = (
    nexah_success_rate /
    max(random_success_rate, 1e-9)
)


# ============================================================
# Save Results
# ============================================================

summary = pd.DataFrame({

    "metric": [

        "random_success_rate",
        "nexah_success_rate",
        "random_mean_steps",
        "nexah_mean_steps",
        "navigation_gain"
    ],

    "value": [

        random_success_rate,
        nexah_success_rate,
        random_mean_steps,
        nexah_mean_steps,
        navigation_gain
    ]
})

summary.to_csv(
    OUTPUT_DIR /
    "exp19_navigation_summary.csv",
    index=False
)

with open(
    OUTPUT_DIR /
    "exp19_summary.txt",
    "w"
) as f:

    f.write(
        "EXP_19 TARGET REGION NAVIGATION\n"
    )

    f.write(
        "=" * 40 + "\n\n"
    )

    f.write(
        f"Random Success: {random_success_rate:.4f}\n"
    )

    f.write(
        f"NEXAH Success : {nexah_success_rate:.4f}\n"
    )

    f.write(
        f"Random Steps  : {random_mean_steps:.4f}\n"
    )

    f.write(
        f"NEXAH Steps   : {nexah_mean_steps:.4f}\n"
    )

    f.write(
        f"Navigation Gain: {navigation_gain:.4f}\n"
    )


print()
print(
    f"Random Success: {random_success_rate:.4f}"
)

print(
    f"NEXAH Success : {nexah_success_rate:.4f}"
)

print()

print(
    f"Random Steps: {random_mean_steps:.4f}"
)

print(
    f"NEXAH Steps : {nexah_mean_steps:.4f}"
)

print()

print(
    f"Navigation Gain: {navigation_gain:.4f}"
)

print()


# ============================================================
# Visual 1
# Region Map
# ============================================================

plt.figure(
    figsize=(10, 7)
)

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    s=15,
    alpha=0.4
)

plt.scatter(
    Z[left_region, 0],
    Z[left_region, 1],
    s=25,
    label="Left Region"
)

plt.scatter(
    Z[right_region, 0],
    Z[right_region, 1],
    s=25,
    label="Right Region"
)

plt.legend()

plt.title(
    "EXP_19 — Target Regions"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp19_region_map.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Success Rates
# ============================================================

plt.figure(
    figsize=(7, 5)
)

plt.bar(
    ["Random", "NEXAH"],
    [
        random_success_rate,
        nexah_success_rate
    ]
)

plt.ylabel(
    "Success Rate"
)

plt.title(
    "EXP_19 — Navigation Success"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp19_navigation_success.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# Arrival Steps
# ============================================================

plt.figure(
    figsize=(7, 5)
)

plt.bar(
    ["Random", "NEXAH"],
    [
        random_mean_steps,
        nexah_mean_steps
    ]
)

plt.ylabel(
    "Average Steps"
)

plt.title(
    "EXP_19 — Arrival Steps"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp19_arrival_steps.png",
    dpi=300
)

plt.close()

print(
    "EXP_19 completed."
)
