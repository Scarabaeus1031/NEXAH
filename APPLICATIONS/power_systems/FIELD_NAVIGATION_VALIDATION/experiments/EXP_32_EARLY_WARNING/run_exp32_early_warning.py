#!/usr/bin/env python3
"""
EXP_32 — Early Warning

Goal
-----
Construct a geometric Early Warning Index (EWI)
for the NEXAH Atlas.

Question:
Can we identify states approaching
a basin exit BEFORE the transition occurs?

Outputs
-------
exp32_warning_map.png
exp32_warning_vs_density.png
exp32_warning_vs_axis_distance.png
exp32_warning_vs_basin_distance.png
exp32_warning_classes.png
exp32_warning_table.csv
exp32_summary.txt
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler


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
    / "EXP_32_EARLY_WARNING"
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
# Feature Selection
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

print(f"Features: {len(features)}")


# ============================================================
# PCA Atlas
# ============================================================

pca = PCA(n_components=2)

X2 = pca.fit_transform(X)

df["PC1"] = X2[:, 0]
df["PC2"] = X2[:, 1]

print(
    "PCA variance:",
    round(
        pca.explained_variance_ratio_.sum(),
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

labels = kmeans.fit_predict(X2)

df["basin"] = labels

centers = kmeans.cluster_centers_

print(f"Basins: {N_BASINS}")


# ============================================================
# Local Density
# ============================================================

nn = NearestNeighbors(
    n_neighbors=10
)

nn.fit(X2)

distances, _ = nn.kneighbors(X2)

density = 1.0 / (
    distances[:, 1:].mean(axis=1)
    + 1e-6
)

df["density"] = density


# ============================================================
# Basin Distance
# ============================================================

basin_distance = np.zeros(len(df))

for i in range(len(df)):

    basin_distance[i] = np.linalg.norm(
        X2[i]
        - centers[labels[i]]
    )

df["basin_distance"] = basin_distance


# ============================================================
# Transport Axis Distance
# ============================================================

axis_distance = np.abs(
    X2[:, 1]
)

df["axis_distance"] = axis_distance


# ============================================================
# Exit Risk
# ============================================================

exit_risk = (
    density.max() - density
)

exit_risk /= exit_risk.max()

df["exit_risk"] = exit_risk


# ============================================================
# Early Warning Index
# ============================================================

scaler = MinMaxScaler()

scaled = scaler.fit_transform(
    np.column_stack([
        exit_risk,
        basin_distance,
        axis_distance
    ])
)

warning_index = scaled.mean(axis=1)

df["warning_index"] = warning_index


# ============================================================
# Warning Classes
# ============================================================

classes = []

for x in warning_index:

    if x < 0.25:
        classes.append("SAFE")

    elif x < 0.50:
        classes.append("WATCH")

    elif x < 0.75:
        classes.append("WARNING")

    else:
        classes.append("CRITICAL")

df["warning_class"] = classes

print("\nWarning Classes")

for c in [
    "SAFE",
    "WATCH",
    "WARNING",
    "CRITICAL"
]:
    print(
        f"{c}:",
        (df["warning_class"] == c).sum()
    )


# ============================================================
# Save Table
# ============================================================

df.to_csv(
    OUTPUT_DIR /
    "exp32_warning_table.csv",
    index=False
)


# ============================================================
# Visual 1
# Warning Map
# ============================================================

plt.figure(figsize=(10, 8))

plt.scatter(
    df["PC1"],
    df["PC2"],
    c=df["warning_index"],
    cmap="RdYlGn_r",
    s=40
)

plt.colorbar(
    label="Warning Index"
)

plt.title(
    "EXP_32 Early Warning Map"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp32_warning_map.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Density
# ============================================================

plt.figure(figsize=(8, 6))

plt.scatter(
    density,
    warning_index,
    alpha=0.7
)

plt.xlabel("Density")
plt.ylabel("Warning Index")

plt.title(
    "EXP_32 Warning vs Density"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp32_warning_vs_density.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# Axis Distance
# ============================================================

plt.figure(figsize=(8, 6))

plt.scatter(
    axis_distance,
    warning_index,
    alpha=0.7
)

plt.xlabel("Axis Distance")
plt.ylabel("Warning Index")

plt.title(
    "EXP_32 Warning vs Axis Distance"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp32_warning_vs_axis_distance.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 4
# Basin Distance
# ============================================================

plt.figure(figsize=(8, 6))

plt.scatter(
    basin_distance,
    warning_index,
    alpha=0.7
)

plt.xlabel("Basin Distance")
plt.ylabel("Warning Index")

plt.title(
    "EXP_32 Warning vs Basin Distance"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp32_warning_vs_basin_distance.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 5
# Warning Classes
# ============================================================

counts = [
    (df["warning_class"] == c).sum()
    for c in [
        "SAFE",
        "WATCH",
        "WARNING",
        "CRITICAL"
    ]
]

plt.figure(figsize=(8, 5))

plt.bar(
    [
        "SAFE",
        "WATCH",
        "WARNING",
        "CRITICAL"
    ],
    counts
)

plt.ylabel("States")

plt.title(
    "EXP_32 Warning Classes"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp32_warning_classes.png",
    dpi=300
)

plt.close()


# ============================================================
# Summary
# ============================================================

with open(
    OUTPUT_DIR /
    "exp32_summary.txt",
    "w"
) as f:

    f.write(
        "EXP_32 EARLY WARNING\n"
    )

    f.write(
        "========================================\n\n"
    )

    f.write(
        f"States: {len(df)}\n"
    )

    f.write(
        f"Basins: {N_BASINS}\n\n"
    )

    for c in [
        "SAFE",
        "WATCH",
        "WARNING",
        "CRITICAL"
    ]:
        f.write(
            f"{c}: "
            f"{(df['warning_class']==c).sum()}\n"
        )

print("\nEXP_32 completed.")
