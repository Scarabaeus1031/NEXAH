"""
run_exp14_regime_navigation_validation.py

EXP_14 — REGIME NAVIGATION VALIDATION

Goal
-----
Test whether the reconstructed flow field
naturally transports states toward the
gate corridor and across the regime boundary.

Input
-----
EXP_08_REAL_FIELD_GEOMETRY

Outputs
-------
exp14_navigation_paths.png
exp14_gate_attraction.png
exp14_regime_switches.png
exp14_transition_statistics.png
exp14_navigation_metrics.csv
exp14_report.txt

NEXAH Validation Program
2026
"""

from pathlib import Path

import numpy as np
import pandas as pd
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
    / "EXP_14_REGIME_NAVIGATION_VALIDATION"
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
# Load States
# ============================================================

df = pd.read_csv(
    INPUT_DIR / "exp08_field_states.csv"
)

Z = df[
    ["pca_x", "pca_y"]
].values

print(
    f"Loaded states: {len(Z)}"
)


# ============================================================
# Gate Axis
# ============================================================

gate_ids = [502, 498, 81, 33]

gate_points = np.array([
    df.loc[
        g,
        ["pca_x", "pca_y"]
    ].values.astype(float)
    for g in gate_ids
])

A = gate_points[0]
B = gate_points[-1]

axis_vec = B - A
axis_vec /= np.linalg.norm(axis_vec)


# ============================================================
# Signed Distance Function
# ============================================================

def signed_distance(point):

    rel = point - A

    return (
        axis_vec[0] * rel[1]
        -
        axis_vec[1] * rel[0]
    )


# ============================================================
# Flow Reconstruction
# ============================================================

K = 12

nbrs = NearestNeighbors(
    n_neighbors=K
)

nbrs.fit(Z)

distances, indices = nbrs.kneighbors(Z)

flow_vectors = []

for i in range(len(Z)):

    neighbors = Z[
        indices[i][1:]
    ]

    center = Z[i]

    vec = np.mean(
        neighbors - center,
        axis=0
    )

    flow_vectors.append(vec)

flow_vectors = np.array(
    flow_vectors
)

print(
    "Flow field reconstructed."
)


# ============================================================
# Navigation Step
# ============================================================

STEP_SIZE = 1.0

new_positions = (
    Z
    + STEP_SIZE * flow_vectors
)

old_side = np.array([
    np.sign(
        signed_distance(p)
    )
    for p in Z
])

new_side = np.array([
    np.sign(
        signed_distance(p)
    )
    for p in new_positions
])

switch_mask = (
    old_side != new_side
)

switch_count = int(
    np.sum(switch_mask)
)

print(
    f"Regime switches: {switch_count}"
)


# ============================================================
# Distance Change
# ============================================================

old_dist = np.abs([
    signed_distance(p)
    for p in Z
])

new_dist = np.abs([
    signed_distance(p)
    for p in new_positions
])

distance_change = (
    new_dist - old_dist
)

mean_change = float(
    np.mean(distance_change)
)

toward_gate = int(
    np.sum(
        distance_change < 0
    )
)

away_from_gate = int(
    np.sum(
        distance_change > 0
    )
)

print(
    f"Toward gate : {toward_gate}"
)

print(
    f"Away gate   : {away_from_gate}"
)


# ============================================================
# Visual 1
# Navigation Paths
# ============================================================

plt.figure(
    figsize=(10, 8)
)

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    s=10,
    alpha=0.4
)

sample_idx = np.arange(
    0,
    len(Z),
    10
)

for i in sample_idx:

    plt.arrow(
        Z[i, 0],
        Z[i, 1],
        flow_vectors[i, 0],
        flow_vectors[i, 1],
        alpha=0.5,
        length_includes_head=True
    )

plt.plot(
    gate_points[:, 0],
    gate_points[:, 1],
    linewidth=3
)

plt.scatter(
    gate_points[:, 0],
    gate_points[:, 1],
    s=150
)

plt.title(
    "EXP_14 — Navigation Paths"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp14_navigation_paths.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Gate Attraction
# ============================================================

plt.figure(
    figsize=(8, 6)
)

plt.hist(
    distance_change,
    bins=40
)

plt.axvline(
    0,
    color="red",
    linestyle="--"
)

plt.title(
    "EXP_14 — Gate Attraction"
)

plt.xlabel(
    "Distance Change"
)

plt.ylabel(
    "Count"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp14_gate_attraction.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# Regime Switches
# ============================================================

plt.figure(
    figsize=(10, 8)
)

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    color="lightgray",
    s=10
)

plt.scatter(
    Z[switch_mask, 0],
    Z[switch_mask, 1],
    color="red",
    s=50,
    label="Switches"
)

plt.plot(
    gate_points[:, 0],
    gate_points[:, 1],
    linewidth=3,
    label="Gate Axis"
)

plt.legend()

plt.title(
    "EXP_14 — Regime Switches"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp14_regime_switches.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 4
# Statistics
# ============================================================

metrics_names = [
    "switches",
    "toward_gate",
    "away_from_gate"
]

metrics_values = [
    switch_count,
    toward_gate,
    away_from_gate
]

plt.figure(
    figsize=(7, 5)
)

plt.bar(
    metrics_names,
    metrics_values
)

plt.title(
    "EXP_14 — Transition Statistics"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp14_transition_statistics.png",
    dpi=300
)

plt.close()


# ============================================================
# Metrics CSV
# ============================================================

metrics_df = pd.DataFrame({

    "metric": [

        "states",
        "switches",
        "toward_gate",
        "away_from_gate",
        "mean_distance_change"

    ],

    "value": [

        len(Z),
        switch_count,
        toward_gate,
        away_from_gate,
        mean_change

    ]
})

metrics_df.to_csv(
    OUTPUT_DIR /
    "exp14_navigation_metrics.csv",
    index=False
)


# ============================================================
# Report
# ============================================================

report = f"""
EXP_14 REGIME NAVIGATION VALIDATION
========================================

States:
{len(Z)}

Regime Switches:
{switch_count}

Toward Gate:
{toward_gate}

Away From Gate:
{away_from_gate}

Mean Distance Change:
{mean_change:.6f}

Interpretation
----------------------------------------

If more states move toward the gate
than away from it, the reconstructed
flow field exhibits gate attraction.

If regime switches occur near the
gate corridor, the gate structure
acts as a transport interface
between operating regimes.
"""

with open(
    OUTPUT_DIR /
    "exp14_report.txt",
    "w"
) as f:

    f.write(report)

print()
print("EXP_14 completed.")
print()
