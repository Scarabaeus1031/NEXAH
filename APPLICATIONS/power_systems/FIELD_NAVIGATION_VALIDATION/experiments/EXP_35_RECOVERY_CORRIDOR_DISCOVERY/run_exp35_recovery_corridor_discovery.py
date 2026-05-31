#!/usr/bin/env python3
"""
EXP_35 — Recovery Corridor Discovery

Goal
-----
Discover preferred recovery paths inside the NEXAH Atlas.

Question
--------
Do unstable states converge toward basin cores
through common geometric corridors?

Outputs
-------
exp35_recovery_corridors.png
exp35_corridor_density.png
exp35_recovery_path_lengths.png
exp35_corridor_network.png
exp35_safe_arrivals.png

exp35_recovery_paths.csv
exp35_corridor_statistics.csv

exp35_summary.txt
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler
)


# ============================================================
# Paths
# ============================================================

FIELD_ROOT = Path(__file__).resolve().parents[2]

INPUT_DIR = (
    FIELD_ROOT
    / "outputs"
    / "EXP_08_REAL_FIELD_GEOMETRY"
)

OUTPUT_DIR = (
    FIELD_ROOT
    / "outputs"
    / "EXP_35_RECOVERY_CORRIDOR_DISCOVERY"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print(f"Input  -> {INPUT_DIR}")
print(f"Output -> {OUTPUT_DIR}")


# ============================================================
# Load Data
# ============================================================

states_file = (
    INPUT_DIR
    / "exp08_field_states.csv"
)

print(
    "\nUsing:",
    states_file.name
)

df = pd.read_csv(
    states_file
)

print(
    "Loaded states:",
    len(df)
)


# ============================================================
# Feature Space
# ============================================================

features = [
    "global_scale",
    "min_vm",
    "mean_vm",
    "std_vm",
    "angle_span",
    "max_loading",
    "mean_loading",
    "density",
    "betweenness"
]

X = df[features].values

X_scaled = StandardScaler().fit_transform(
    X
)

print(
    "Features:",
    len(features)
)


# ============================================================
# PCA Atlas
# ============================================================

pca = PCA(
    n_components=2
)

coords = pca.fit_transform(
    X_scaled
)

pca_variance = float(
    pca.explained_variance_ratio_.sum()
)

df["PC1"] = coords[:, 0]
df["PC2"] = coords[:, 1]

print(
    "PCA variance:",
    round(
        pca_variance,
        4
    )
)


# ============================================================
# Basin Reconstruction
# ============================================================

N_BASINS = 18

kmeans = KMeans(
    n_clusters=N_BASINS,
    random_state=42,
    n_init=20
)

labels = kmeans.fit_predict(
    coords
)

df["basin"] = labels

centers = kmeans.cluster_centers_

print(
    "Basins:",
    N_BASINS
)


# ============================================================
# Local Density
# ============================================================

nn = NearestNeighbors(
    n_neighbors=10
)

nn.fit(
    coords
)

distances, _ = nn.kneighbors(
    coords
)

density_local = 1.0 / (
    distances[:, 1:].mean(axis=1)
    + 1e-6
)

df["density_local"] = density_local


# ============================================================
# Basin Distance
# ============================================================

basin_distance = np.zeros(
    len(df)
)

for i in range(len(df)):

    basin_distance[i] = np.linalg.norm(
        coords[i]
        - centers[labels[i]]
    )

df["basin_distance"] = basin_distance


# ============================================================
# Axis Distance
# ============================================================

axis_distance = np.abs(
    coords[:, 1]
)

df["axis_distance"] = axis_distance


# ============================================================
# Exit Risk
# ============================================================

density_risk = (
    density_local.max()
    - density_local
)

density_risk /= (
    density_risk.max()
)

basin_norm = (
    basin_distance
    / basin_distance.max()
)

axis_norm = (
    axis_distance
    / axis_distance.max()
)

exit_risk = (
    0.4 * density_risk
    + 0.4 * basin_norm
    + 0.2 * axis_norm
)

df["exit_risk"] = exit_risk


# ============================================================
# Warning Index
# ============================================================

warning_inputs = np.column_stack([
    density_risk,
    basin_norm,
    axis_norm,
    exit_risk
])

warning_scaled = (
    MinMaxScaler()
    .fit_transform(
        warning_inputs
    )
)

warning_index = (
    warning_scaled.mean(
        axis=1
    )
)

df["warning_index"] = warning_index


# ============================================================
# Warning Classes
# ============================================================

warning_class = []

for value in warning_index:

    if value < 0.25:

        warning_class.append(
            "SAFE"
        )

    elif value < 0.50:

        warning_class.append(
            "WATCH"
        )

    elif value < 0.75:

        warning_class.append(
            "WARNING"
        )

    else:

        warning_class.append(
            "CRITICAL"
        )

df["warning_class"] = warning_class

print("\nWarning Classes")

for label in [
    "SAFE",
    "WATCH",
    "WARNING",
    "CRITICAL"
]:

    count = (
        df["warning_class"]
        == label
    ).sum()

    print(
        f"{label}:",
        count
    )


# ============================================================
# Recovery Candidates
# ============================================================

control_mask = df[
    "warning_class"
].isin([
    "WARNING",
    "CRITICAL"
])

control_df = df[
    control_mask
].copy()

print(
    "\nRecovery candidates:",
    len(control_df)
)

# ============================================================
# Recovery Corridor Construction
# ============================================================

print("\nBuilding recovery corridors...")

MAX_STEPS = 25
STEP_FACTOR = 0.35

paths = []
path_records = []

for idx, row in control_df.iterrows():

    current_x = row["PC1"]
    current_y = row["PC2"]

    basin = int(row["basin"])

    target_x = centers[basin][0]
    target_y = centers[basin][1]

    path_x = [current_x]
    path_y = [current_y]

    total_length = 0.0

    for step in range(MAX_STEPS):

        dx = target_x - current_x
        dy = target_y - current_y

        dist = np.sqrt(
            dx**2 + dy**2
        )

        if dist < 0.05:
            break

        step_dx = STEP_FACTOR * dx
        step_dy = STEP_FACTOR * dy

        current_x += step_dx
        current_y += step_dy

        total_length += np.sqrt(
            step_dx**2 + step_dy**2
        )

        path_x.append(
            current_x
        )

        path_y.append(
            current_y
        )

    paths.append(
        {
            "run_id": idx,
            "basin": basin,
            "path_x": path_x,
            "path_y": path_y,
            "steps": len(path_x) - 1,
            "path_length": total_length
        }
    )

    path_records.append(
        {
            "run_id": idx,
            "basin": basin,
            "steps": len(path_x) - 1,
            "path_length": total_length
        }
    )

print(
    "Recovery paths:",
    len(paths)
)


# ============================================================
# Save Recovery Path Table
# ============================================================

path_table = pd.DataFrame(
    path_records
)

path_table.to_csv(
    OUTPUT_DIR
    / "exp35_recovery_paths.csv",
    index=False
)


# ============================================================
# Corridor Statistics
# ============================================================

corridor_stats = pd.DataFrame(
    {
        "steps": [
            p["steps"]
            for p in paths
        ],
        "path_length": [
            p["path_length"]
            for p in paths
        ]
    }
)

corridor_stats.to_csv(
    OUTPUT_DIR
    / "exp35_corridor_statistics.csv",
    index=False
)


# ============================================================
# Visual 1
# Recovery Corridors
# ============================================================

plt.figure(figsize=(12, 8))

plt.scatter(
    df["PC1"],
    df["PC2"],
    c="lightblue",
    s=20,
    alpha=0.30
)

for path in paths:

    plt.plot(
        path["path_x"],
        path["path_y"],
        linewidth=1.2,
        alpha=0.70
    )

plt.scatter(
    centers[:, 0],
    centers[:, 1],
    marker="x",
    s=180,
    c="black"
)

plt.title(
    "EXP_35 Recovery Corridors"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp35_recovery_corridors.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Corridor Density
# ============================================================

corridor_points_x = []
corridor_points_y = []

for path in paths:

    corridor_points_x.extend(
        path["path_x"]
    )

    corridor_points_y.extend(
        path["path_y"]
    )

plt.figure(figsize=(12, 8))

plt.hist2d(
    corridor_points_x,
    corridor_points_y,
    bins=40
)

plt.colorbar(
    label="Corridor Usage"
)

plt.title(
    "EXP_35 Corridor Density"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp35_corridor_density.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# Recovery Path Lengths
# ============================================================

path_lengths = [
    p["path_length"]
    for p in paths
]

plt.figure(figsize=(10, 6))

plt.hist(
    path_lengths,
    bins=20
)

plt.xlabel(
    "Recovery Path Length"
)

plt.ylabel(
    "Paths"
)

plt.title(
    "EXP_35 Recovery Path Lengths"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp35_recovery_path_lengths.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 4
# Corridor Network
# ============================================================

plt.figure(figsize=(12, 8))

for path in paths:

    plt.plot(
        path["path_x"],
        path["path_y"],
        alpha=0.25
    )

plt.scatter(
    centers[:, 0],
    centers[:, 1],
    s=200,
    marker="x",
    c="black"
)

plt.title(
    "EXP_35 Corridor Network"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp35_corridor_network.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 5
# Safe Arrivals
# ============================================================

plt.figure(figsize=(12, 8))

plt.scatter(
    df["PC1"],
    df["PC2"],
    c="lightgray",
    s=15,
    alpha=0.25
)

for path in paths:

    plt.scatter(
        path["path_x"][0],
        path["path_y"][0],
        c="red",
        s=35
    )

    plt.scatter(
        path["path_x"][-1],
        path["path_y"][-1],
        c="green",
        s=35
    )

plt.title(
    "EXP_35 Safe Arrivals"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp35_safe_arrivals.png",
    dpi=300
)

plt.close()


# ============================================================
# Summary
# ============================================================

summary = f"""
EXP_35 RECOVERY CORRIDOR DISCOVERY
========================================

States: {len(df)}
Basins: {N_BASINS}
PCA Variance: {pca_variance:.4f}

Recovery Paths: {len(paths)}

Mean Corridor Length:
{np.mean(path_lengths):.4f}

Max Corridor Length:
{np.max(path_lengths):.4f}

Min Corridor Length:
{np.min(path_lengths):.4f}
"""

with open(
    OUTPUT_DIR
    / "exp35_summary.txt",
    "w"
) as f:

    f.write(
        summary
    )

print(summary)

print(
    "\nEXP_35 completed."
)
