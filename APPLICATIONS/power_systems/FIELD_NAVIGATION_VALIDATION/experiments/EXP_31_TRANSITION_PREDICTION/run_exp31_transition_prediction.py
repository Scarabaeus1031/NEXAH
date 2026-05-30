#!/usr/bin/env python3
"""
EXP_31 — Transition Prediction

Goal:
Predict likely basin-to-basin transitions
using atlas geometry alone.

Builds on:
EXP_24E  Basin Structure
EXP_28   Atlas Geometry
EXP_30   Basin Exit Forecasting

Outputs
-------
exp31_predicted_transition_map.png
exp31_transition_target_map.png
exp31_transition_matrix.png
exp31_exit_to_target_overlay.png
exp31_prediction_table.csv
exp31_summary.txt
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors


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
    / "EXP_31_TRANSITION_PREDICTION"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Input  -> {INPUT_DIR}")
print(f"Output -> {OUTPUT_DIR}")


# ============================================================
# Load
# ============================================================

states_file = INPUT_DIR / "state_features.csv"

df = pd.read_csv(states_file)

numeric_cols = df.select_dtypes(include=[np.number]).columns

X = df[numeric_cols].values

print(f"\nLoaded states: {len(df)}")


# ============================================================
# PCA Atlas
# ============================================================

pca = PCA(n_components=2)
X2 = pca.fit_transform(X)

print(
    "PCA variance:",
    round(pca.explained_variance_ratio_.sum(), 4)
)

df["PC1"] = X2[:, 0]
df["PC2"] = X2[:, 1]


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

nn = NearestNeighbors(n_neighbors=10)
nn.fit(X2)

distances, indices = nn.kneighbors(X2)

density = 1.0 / (
    distances[:, 1:].mean(axis=1) + 1e-6
)

df["density"] = density


# ============================================================
# Exit Risk
# ============================================================

risk = (
    density.max() - density
)

risk /= risk.max()

df["exit_risk"] = risk


# ============================================================
# Predict Transition Target
# ============================================================

targets = []
target_distances = []

for i in range(len(df)):

    basin_i = labels[i]
    point = X2[i]

    foreign = centers[
        np.arange(len(centers)) != basin_i
    ]

    foreign_ids = np.arange(len(centers))[
        np.arange(len(centers)) != basin_i
    ]

    d = np.linalg.norm(
        foreign - point,
        axis=1
    )

    j = np.argmin(d)

    targets.append(
        int(foreign_ids[j])
    )

    target_distances.append(
        float(d[j])
    )

df["target_basin"] = targets
df["target_distance"] = target_distances


# ============================================================
# High Risk Candidates
# ============================================================

N_TOP = 40

top_idx = (
    df["exit_risk"]
    .sort_values(ascending=False)
    .head(N_TOP)
    .index
)

top_df = df.loc[top_idx].copy()

print(
    f"Top transition candidates: {len(top_df)}"
)


# ============================================================
# Transition Matrix
# ============================================================

matrix = np.zeros(
    (N_BASINS, N_BASINS),
    dtype=int
)

for _, row in top_df.iterrows():

    a = int(row["basin"])
    b = int(row["target_basin"])

    matrix[a, b] += 1


# ============================================================
# Save Table
# ============================================================

table_cols = [
    "basin",
    "target_basin",
    "exit_risk",
    "target_distance",
    "PC1",
    "PC2",
]

top_df[table_cols].to_csv(
    OUTPUT_DIR / "exp31_prediction_table.csv",
    index=False
)


# ============================================================
# Visual 1
# Predicted Transition Map
# ============================================================

plt.figure(figsize=(10, 8))

plt.scatter(
    X2[:, 0],
    X2[:, 1],
    s=18,
    alpha=0.25
)

plt.scatter(
    top_df["PC1"],
    top_df["PC2"],
    s=90,
    c=top_df["exit_risk"],
    cmap="autumn"
)

plt.title(
    "EXP_31 Predicted Transition States"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp31_predicted_transition_map.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Target Basin Map
# ============================================================

plt.figure(figsize=(10, 8))

plt.scatter(
    X2[:, 0],
    X2[:, 1],
    c=labels,
    cmap="tab20",
    s=25
)

plt.scatter(
    centers[:, 0],
    centers[:, 1],
    s=300,
    c="black",
    marker="x"
)

plt.title(
    "EXP_31 Transition Target Map"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp31_transition_target_map.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# Transition Matrix
# ============================================================

plt.figure(figsize=(8, 7))

plt.imshow(
    matrix,
    cmap="viridis"
)

plt.colorbar(
    label="Predicted Transitions"
)

plt.xlabel("Target Basin")
plt.ylabel("Source Basin")

plt.title(
    "EXP_31 Transition Matrix"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp31_transition_matrix.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 4
# Exit -> Target Overlay
# ============================================================

plt.figure(figsize=(11, 8))

plt.scatter(
    X2[:, 0],
    X2[:, 1],
    alpha=0.15
)

for _, row in top_df.iterrows():

    src = np.array([
        row["PC1"],
        row["PC2"]
    ])

    tgt = centers[
        int(row["target_basin"])
    ]

    plt.plot(
        [src[0], tgt[0]],
        [src[1], tgt[1]],
        alpha=0.35,
        linewidth=1.5
    )

plt.scatter(
    centers[:, 0],
    centers[:, 1],
    s=200,
    c="red"
)

plt.title(
    "EXP_31 Exit To Target Overlay"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp31_exit_to_target_overlay.png",
    dpi=300
)

plt.close()


# ============================================================
# Summary
# ============================================================

with open(
    OUTPUT_DIR / "exp31_summary.txt",
    "w"
) as f:

    f.write(
        "EXP_31 TRANSITION PREDICTION\n"
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
        f"Top Transition Candidates: {N_TOP}\n"
    )

print("\nEXP_31 completed.")
