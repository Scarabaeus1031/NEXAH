#!/usr/bin/env python3
"""
EXP_33 — Control Vector Discovery

Goal
-----
Discover geometric recovery directions inside the NEXAH Atlas.

Question:
For WARNING / CRITICAL states, in which direction should the
state move in order to return toward a safer basin core?

Outputs
-------
exp33_control_vector_field.png
exp33_recovery_vectors.png
exp33_warning_recovery_overlay.png
exp33_vector_length_distribution.png
exp33_recovery_targets.png
exp33_control_table.csv
exp33_summary.txt
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler, StandardScaler


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
    / "EXP_33_CONTROL_VECTOR_DISCOVERY"
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

pca_variance = float(
    pca.explained_variance_ratio_.sum()
)

df["PC1"] = coords[:, 0]
df["PC2"] = coords[:, 1]

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

density_risk = (
    density_risk
    / density_risk.max()
)

basin_distance_norm = (
    basin_distance
    / basin_distance.max()
)

axis_distance_norm = (
    axis_distance
    / axis_distance.max()
)

exit_risk = (
    0.4 * density_risk
    + 0.4 * basin_distance_norm
    + 0.2 * axis_distance_norm
)

df["exit_risk"] = exit_risk


# ============================================================
# Early Warning Index
# ============================================================

warning_inputs = np.column_stack([
    density_risk,
    basin_distance_norm,
    axis_distance_norm,
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
# Control Vectors
# ============================================================

vectors = np.zeros_like(
    coords
)

vector_lengths = np.zeros(
    len(df)
)

for i in range(len(df)):

    basin = labels[i]

    target = centers[basin]

    vector = (
        target
        - coords[i]
    )

    vectors[i] = vector

    vector_lengths[i] = np.linalg.norm(
        vector
    )

df["control_dx"] = vectors[:, 0]
df["control_dy"] = vectors[:, 1]
df["control_length"] = vector_lengths


# ============================================================
# Control Candidates
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
    "\nControl candidates:",
    len(control_df)
)

# ============================================================
# Save Control Table
# ============================================================

control_cols = [
    "run_id",
    "basin",
    "warning_class",
    "warning_index",
    "exit_risk",
    "PC1",
    "PC2",
    "control_dx",
    "control_dy",
    "control_length",
    "max_loading",
    "angle_span",
    "std_vm"
]

available_cols = [
    col for col in control_cols
    if col in control_df.columns
]

control_df[
    available_cols
].to_csv(
    OUTPUT_DIR
    / "exp33_control_table.csv",
    index=False
)


# ============================================================
# Visual 1
# Full Control Vector Field
# ============================================================

plt.figure(
    figsize=(11, 8)
)

scatter = plt.scatter(
    coords[:, 0],
    coords[:, 1],
    c=warning_index,
    cmap="RdYlGn_r",
    s=25,
    alpha=0.75
)

plt.colorbar(
    scatter,
    label="Warning Index"
)

step = 8

plt.quiver(
    coords[::step, 0],
    coords[::step, 1],
    vectors[::step, 0],
    vectors[::step, 1],
    angles="xy",
    scale_units="xy",
    scale=1.5,
    width=0.003,
    alpha=0.55
)

plt.scatter(
    centers[:, 0],
    centers[:, 1],
    marker="x",
    s=180,
    c="black"
)

plt.title(
    "EXP_33 Control Vector Field"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp33_control_vector_field.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Recovery Vectors
# ============================================================

plt.figure(
    figsize=(11, 8)
)

plt.scatter(
    coords[:, 0],
    coords[:, 1],
    s=18,
    alpha=0.15
)

plt.scatter(
    control_df["PC1"],
    control_df["PC2"],
    c=control_df["warning_index"],
    cmap="autumn",
    s=60
)

plt.quiver(
    control_df["PC1"],
    control_df["PC2"],
    control_df["control_dx"],
    control_df["control_dy"],
    angles="xy",
    scale_units="xy",
    scale=1.2,
    width=0.003,
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
    "EXP_33 Recovery Vectors"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp33_recovery_vectors.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# Warning Recovery Overlay
# ============================================================

plt.figure(
    figsize=(11, 8)
)

scatter = plt.scatter(
    coords[:, 0],
    coords[:, 1],
    c=warning_index,
    cmap="RdYlGn_r",
    s=30,
    alpha=0.85
)

plt.colorbar(
    scatter,
    label="Warning Index"
)

plt.quiver(
    control_df["PC1"],
    control_df["PC2"],
    control_df["control_dx"],
    control_df["control_dy"],
    angles="xy",
    scale_units="xy",
    scale=1.2,
    width=0.003,
    alpha=0.80
)

plt.scatter(
    centers[:, 0],
    centers[:, 1],
    marker="x",
    s=180,
    c="black"
)

plt.title(
    "EXP_33 Warning Recovery Overlay"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp33_warning_recovery_overlay.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 4
# Vector Length Distribution
# ============================================================

plt.figure(
    figsize=(8, 6)
)

plt.hist(
    vector_lengths,
    bins=30
)

plt.xlabel(
    "Recovery Vector Length"
)

plt.ylabel(
    "States"
)

plt.title(
    "EXP_33 Vector Length Distribution"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp33_vector_length_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 5
# Recovery Targets
# ============================================================

plt.figure(
    figsize=(11, 8)
)

plt.scatter(
    coords[:, 0],
    coords[:, 1],
    c=labels,
    cmap="tab20",
    s=22,
    alpha=0.60
)

plt.scatter(
    centers[:, 0],
    centers[:, 1],
    marker="x",
    s=180,
    c="black"
)

for _, row in control_df.iterrows():

    source = np.array([
        row["PC1"],
        row["PC2"]
    ])

    target = source + np.array([
        row["control_dx"],
        row["control_dy"]
    ])

    plt.plot(
        [source[0], target[0]],
        [source[1], target[1]],
        alpha=0.25,
        linewidth=1.0
    )

plt.title(
    "EXP_33 Recovery Targets"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp33_recovery_targets.png",
    dpi=300
)

plt.close()


# ============================================================
# Summary
# ============================================================

safe_count = int(
    (df["warning_class"] == "SAFE").sum()
)

watch_count = int(
    (df["warning_class"] == "WATCH").sum()
)

warning_count = int(
    (df["warning_class"] == "WARNING").sum()
)

critical_count = int(
    (df["warning_class"] == "CRITICAL").sum()
)

mean_length = float(
    vector_lengths.mean()
)

max_length = float(
    vector_lengths.max()
)

with open(
    OUTPUT_DIR
    / "exp33_summary.txt",
    "w"
) as f:

    f.write(
        "EXP_33 CONTROL VECTOR DISCOVERY\n"
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

    f.write(
        f"SAFE: {safe_count}\n"
    )

    f.write(
        f"WATCH: {watch_count}\n"
    )

    f.write(
        f"WARNING: {warning_count}\n"
    )

    f.write(
        f"CRITICAL: {critical_count}\n\n"
    )

    f.write(
        f"Control Candidates: {len(control_df)}\n"
    )

    f.write(
        f"Mean Recovery Length: {mean_length:.4f}\n"
    )

    f.write(
        f"Max Recovery Length: {max_length:.4f}\n"
    )

print(
    "\nEXP_33 completed."
)
