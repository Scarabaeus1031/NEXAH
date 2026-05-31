#!/usr/bin/env python3
"""
EXP_34 — Control Effort Estimation

Goal
-----
Estimate how difficult it is to recover a state
once instability has begun.

Question:
How much control effort is required to move a state
back toward a stable basin core?

Outputs
-------
exp34_control_effort_map.png
exp34_control_effort_vs_warning.png
exp34_control_effort_vs_vector_length.png
exp34_control_effort_distribution.png
exp34_high_cost_regions.png
exp34_control_effort_table.csv
exp34_summary.txt
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler, MinMaxScaler


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
    / "EXP_34_CONTROL_EFFORT_ESTIMATION"
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

X_scaled = StandardScaler().fit_transform(X)

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

df["PC1"] = coords[:, 0]
df["PC2"] = coords[:, 1]

pca_variance = float(
    pca.explained_variance_ratio_.sum()
)

print(
    "PCA variance:",
    round(pca_variance, 4)
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

nn.fit(coords)

distances, _ = nn.kneighbors(
    coords
)

density = 1.0 / (
    distances[:, 1:].mean(axis=1)
    + 1e-6
)

df["density_local"] = density


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
    density.max()
    - density
)

density_risk /= density_risk.max()

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

warning_scaled = MinMaxScaler().fit_transform(
    warning_inputs
)

warning_index = warning_scaled.mean(
    axis=1
)

df["warning_index"] = warning_index


# ============================================================
# Recovery Vector
# ============================================================

vectors = np.zeros_like(
    coords
)

vector_lengths = np.zeros(
    len(df)
)

for i in range(len(df)):

    center = centers[
        labels[i]
    ]

    vector = (
        center
        - coords[i]
    )

    vectors[i] = vector

    vector_lengths[i] = np.linalg.norm(
        vector
    )

df["recovery_length"] = vector_lengths


# ============================================================
# Control Effort Index
# ============================================================

control_effort = (
    vector_lengths
    * (1.0 + warning_index)
    * (1.0 + exit_risk)
)

control_effort = (
    control_effort
    / control_effort.max()
)

df["control_effort"] = control_effort


# ============================================================
# Effort Classes
# ============================================================

effort_class = []

for value in control_effort:

    if value < 0.25:
        effort_class.append(
            "LOW"
        )

    elif value < 0.50:
        effort_class.append(
            "MEDIUM"
        )

    elif value < 0.75:
        effort_class.append(
            "HIGH"
        )

    else:
        effort_class.append(
            "EXTREME"
        )

df["effort_class"] = effort_class

print("\nControl Effort Classes")

for label in [
    "LOW",
    "MEDIUM",
    "HIGH",
    "EXTREME"
]:
    count = (
        df["effort_class"]
        == label
    ).sum()

    print(
        f"{label}:",
        count
    )


# ============================================================
# Save Table
# ============================================================

df.to_csv(
    OUTPUT_DIR
    / "exp34_control_effort_table.csv",
    index=False
)


# ============================================================
# Visual 1
# Control Effort Map
# ============================================================

plt.figure(figsize=(10,8))

plt.scatter(
    df["PC1"],
    df["PC2"],
    c=df["control_effort"],
    cmap="RdYlGn_r",
    s=45
)

plt.colorbar(
    label="Control Effort"
)

plt.title(
    "EXP_34 Control Effort Map"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp34_control_effort_map.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Effort vs Warning
# ============================================================

plt.figure(figsize=(8,6))

plt.scatter(
    warning_index,
    control_effort,
    alpha=0.7
)

plt.xlabel(
    "Warning Index"
)

plt.ylabel(
    "Control Effort"
)

plt.title(
    "EXP_34 Control Effort vs Warning"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp34_control_effort_vs_warning.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# Effort vs Recovery Length
# ============================================================

plt.figure(figsize=(8,6))

plt.scatter(
    vector_lengths,
    control_effort,
    alpha=0.7
)

plt.xlabel(
    "Recovery Length"
)

plt.ylabel(
    "Control Effort"
)

plt.title(
    "EXP_34 Control Effort vs Recovery Length"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp34_control_effort_vs_vector_length.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 4
# Distribution
# ============================================================

plt.figure(figsize=(8,6))

plt.hist(
    control_effort,
    bins=25
)

plt.xlabel(
    "Control Effort"
)

plt.ylabel(
    "States"
)

plt.title(
    "EXP_34 Control Effort Distribution"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp34_control_effort_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 5
# High Cost Regions
# ============================================================

threshold = np.percentile(
    control_effort,
    90
)

high_cost = df[
    df["control_effort"]
    >= threshold
]

plt.figure(figsize=(10,8))

plt.scatter(
    df["PC1"],
    df["PC2"],
    alpha=0.15
)

plt.scatter(
    high_cost["PC1"],
    high_cost["PC2"],
    c=high_cost["control_effort"],
    cmap="autumn",
    s=100
)

plt.title(
    "EXP_34 High Cost Regions"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp34_high_cost_regions.png",
    dpi=300
)

plt.close()


# ============================================================
# Summary
# ============================================================

with open(
    OUTPUT_DIR
    / "exp34_summary.txt",
    "w"
) as f:

    f.write(
        "EXP_34 CONTROL EFFORT ESTIMATION\n"
    )

    f.write(
        "========================================\n\n"
    )

    f.write(
        f"States: {len(df)}\n"
    )

    f.write(
        f"Basins: {N_BASINS}\n"
    )

    f.write(
        f"PCA Variance: {pca_variance:.4f}\n\n"
    )

    for label in [
        "LOW",
        "MEDIUM",
        "HIGH",
        "EXTREME"
    ]:

        count = (
            df["effort_class"]
            == label
        ).sum()

        f.write(
            f"{label}: {count}\n"
        )

    f.write("\n")

    f.write(
        f"Mean Control Effort: "
        f"{control_effort.mean():.4f}\n"
    )

    f.write(
        f"Max Control Effort: "
        f"{control_effort.max():.4f}\n"
    )

print(
    "\nEXP_34 completed."
)
