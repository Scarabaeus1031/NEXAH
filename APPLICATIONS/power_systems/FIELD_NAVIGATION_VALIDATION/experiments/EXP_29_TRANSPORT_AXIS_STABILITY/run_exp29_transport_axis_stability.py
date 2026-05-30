# ============================================================
# EXP_29 — TRANSPORT AXIS STABILITY
#
# Question:
# Does distance from the dominant transport axis
# correlate with operating stress?
#
# Hypothesis:
#
# States located far from the atlas transport axis
# exhibit higher stress indicators:
#
# - angle_span
# - max_loading
# - voltage variability
#
# Inputs:
#   EXP_08_REAL_FIELD_GEOMETRY / exp08_field_states.csv
#
# Outputs:
#   exp29_axis_distance_distribution.png
#   exp29_axis_vs_loading.png
#   exp29_axis_vs_angle_span.png
#   exp29_axis_vs_voltage_std.png
#   exp29_axis_stability_map.png
#   exp29_summary.txt
#
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

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
    "EXP_29_TRANSPORT_AXIS_STABILITY"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

print("\nInput  ->", os.path.abspath(INPUT_DIR))
print("Output ->", os.path.abspath(OUTPUT_DIR))

# ------------------------------------------------------------
# Load States
# ------------------------------------------------------------

df = pd.read_csv(
    os.path.join(
        INPUT_DIR,
        "exp08_field_states.csv"
    )
)

print(
    "\nLoaded states:",
    len(df)
)

# ------------------------------------------------------------
# Feature Space
# ------------------------------------------------------------

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

X = StandardScaler().fit_transform(X)

# ------------------------------------------------------------
# PCA Atlas Geometry
# ------------------------------------------------------------

pca = PCA(
    n_components=2
)

coords = pca.fit_transform(X)

variance = float(
    np.sum(
        pca.explained_variance_ratio_
    )
)

print(
    "PCA variance:",
    round(variance, 4)
)

# ------------------------------------------------------------
# Transport Axis
# ------------------------------------------------------------

center = coords.mean(
    axis=0
)

pc1 = pca.components_[0]

# ------------------------------------------------------------
# Distance To Transport Axis
# ------------------------------------------------------------

axis_distances = []

for p in coords:

    v = p - center

    projection = (
        np.dot(v, pc1)
    ) * pc1

    orthogonal = (
        v - projection
    )

    axis_distances.append(
        np.linalg.norm(
            orthogonal
        )
    )

axis_distances = np.array(
    axis_distances
)

df["axis_distance"] = (
    axis_distances
)

# ------------------------------------------------------------
# Correlations
# ------------------------------------------------------------

corr_loading = np.corrcoef(
    axis_distances,
    df["max_loading"]
)[0, 1]

corr_angle = np.corrcoef(
    axis_distances,
    df["angle_span"]
)[0, 1]

corr_voltage = np.corrcoef(
    axis_distances,
    df["std_vm"]
)[0, 1]

print(
    "\nCorrelation Results"
)

print(
    "axis vs loading:",
    round(corr_loading, 4)
)

print(
    "axis vs angle_span:",
    round(corr_angle, 4)
)

print(
    "axis vs std_vm:",
    round(corr_voltage, 4)
)

# ------------------------------------------------------------
# Visual 1
# Axis Distance Distribution
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 6)
)

plt.hist(
    axis_distances,
    bins=30
)

plt.title(
    "EXP_29 Axis Distance Distribution"
)

plt.xlabel(
    "Distance From Transport Axis"
)

plt.ylabel(
    "Count"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp29_axis_distance_distribution.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Visual 2
# Axis vs Loading
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 6)
)

plt.scatter(
    axis_distances,
    df["max_loading"],
    alpha=0.6
)

plt.xlabel(
    "Distance From Axis"
)

plt.ylabel(
    "Max Loading"
)

plt.title(
    "EXP_29 Axis Distance vs Loading"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp29_axis_vs_loading.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Visual 3
# Axis vs Angle Span
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 6)
)

plt.scatter(
    axis_distances,
    df["angle_span"],
    alpha=0.6
)

plt.xlabel(
    "Distance From Axis"
)

plt.ylabel(
    "Angle Span"
)

plt.title(
    "EXP_29 Axis Distance vs Angle Span"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp29_axis_vs_angle_span.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Visual 4
# Axis vs Voltage Spread
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 6)
)

plt.scatter(
    axis_distances,
    df["std_vm"],
    alpha=0.6
)

plt.xlabel(
    "Distance From Axis"
)

plt.ylabel(
    "Voltage Std"
)

plt.title(
    "EXP_29 Axis Distance vs Voltage Std"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp29_axis_vs_voltage_std.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Visual 5
# Stability Map
# ------------------------------------------------------------

plt.figure(
    figsize=(10, 8)
)

scatter = plt.scatter(
    coords[:, 0],
    coords[:, 1],
    c=axis_distances,
    s=20
)

plt.colorbar(
    scatter,
    label="Axis Distance"
)

scale = 8

plt.plot(
    [
        center[0] - pc1[0] * scale,
        center[0] + pc1[0] * scale
    ],
    [
        center[1] - pc1[1] * scale,
        center[1] + pc1[1] * scale
    ],
    linewidth=4
)

plt.title(
    "EXP_29 Transport Axis Stability Map"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp29_axis_stability_map.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

with open(
    os.path.join(
        OUTPUT_DIR,
        "exp29_summary.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_29 TRANSPORT AXIS STABILITY\n"
    )

    f.write(
        "================================\n\n"
    )

    f.write(
        f"States: {len(df)}\n"
    )

    f.write(
        f"PCA Variance: {variance:.4f}\n\n"
    )

    f.write(
        f"Axis vs Loading: {corr_loading:.4f}\n"
    )

    f.write(
        f"Axis vs Angle Span: {corr_angle:.4f}\n"
    )

    f.write(
        f"Axis vs Voltage Std: {corr_voltage:.4f}\n"
    )

print(
    "\nEXP_29 completed."
)
