# ============================================================
# EXP_36_RECOVERY_ANCHOR_DISCOVERY
#
# Phase D — Prediction, Navigation & Control
#
# Goal:
# Determine whether recovery trajectories converge
# toward recurring stabilization anchors.
#
# Input:
# EXP_08_REAL_FIELD_GEOMETRY
#
# Output:
# EXP_36_RECOVERY_ANCHOR_DISCOVERY
#
# Thomas Hofmann / NEXAH
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

import matplotlib.pyplot as plt


# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

INPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_08_REAL_FIELD_GEOMETRY"
)

OUTPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_36_RECOVERY_ANCHOR_DISCOVERY"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Input  ->", INPUT_DIR)
print("Output ->", OUTPUT_DIR)


# ============================================================
# Load Field States
# ============================================================

csv_files = list(
    INPUT_DIR.glob("*.csv")
)

if not csv_files:
    raise FileNotFoundError(
        "No CSV files found in EXP_08 output."
    )

csv_path = csv_files[0]

print("\nUsing:", csv_path.name)

df = pd.read_csv(csv_path)

print("Loaded states:", len(df))


# ============================================================
# Feature Selection
# ============================================================

numeric_cols = (
    df.select_dtypes(include=np.number)
      .columns
      .tolist()
)

exclude = [
    c for c in numeric_cols
    if "time" in c.lower()
]

features = [
    c for c in numeric_cols
    if c not in exclude
]

X = df[features].fillna(0.0)

print("Features:", len(features))


# ============================================================
# Scaling + PCA
# ============================================================

scaler = StandardScaler()

Xs = scaler.fit_transform(X)

pca = PCA(n_components=2)

Xp = pca.fit_transform(Xs)

df["pc1"] = Xp[:, 0]
df["pc2"] = Xp[:, 1]

print(
    "PCA variance:",
    round(
        pca.explained_variance_ratio_.sum(),
        4
    )
)


# ============================================================
# Basin Structure
# ============================================================

kmeans = KMeans(
    n_clusters=18,
    random_state=42,
    n_init=20
)

basins = kmeans.fit_predict(Xp)

df["basin"] = basins

print(
    "Basins:",
    len(np.unique(basins))
)
# ============================================================
# Warning / Risk Layer
# ============================================================

from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler


nn = NearestNeighbors(
    n_neighbors=10
)

nn.fit(
    Xp
)

distances, _ = nn.kneighbors(
    Xp
)

density_local = 1.0 / (
    distances[:, 1:].mean(axis=1)
    + 1e-6
)

df["density_local"] = density_local


# ------------------------------------------------------------
# Basin Distance
# ------------------------------------------------------------

centers = kmeans.cluster_centers_

basin_distance = np.zeros(
    len(df)
)

for i in range(len(df)):

    basin_distance[i] = np.linalg.norm(
        Xp[i]
        - centers[basins[i]]
    )

df["basin_distance"] = basin_distance


# ------------------------------------------------------------
# Axis Distance
# ------------------------------------------------------------

axis_distance = np.abs(
    Xp[:, 1]
)

df["axis_distance"] = axis_distance


# ------------------------------------------------------------
# Exit Risk + Warning Index
# ------------------------------------------------------------

density_risk = (
    density_local.max()
    - density_local
)

density_risk = (
    density_risk
    - density_risk.min()
) / (
    density_risk.max()
    - density_risk.min()
    + 1e-9
)

basin_risk = MinMaxScaler().fit_transform(
    basin_distance.reshape(-1, 1)
).flatten()

axis_risk = MinMaxScaler().fit_transform(
    axis_distance.reshape(-1, 1)
).flatten()

warning_index = (
    0.40 * basin_risk
    + 0.35 * axis_risk
    + 0.25 * density_risk
)

df["warning_index"] = warning_index


# ============================================================
# Warning Classes
# ============================================================

warning_class = []

for w in warning_index:

    if w < 0.25:
        warning_class.append("SAFE")

    elif w < 0.50:
        warning_class.append("WATCH")

    elif w < 0.70:
        warning_class.append("WARNING")

    else:
        warning_class.append("CRITICAL")

df["warning_class"] = warning_class

print("\nWarning Classes")

for cls in [
    "SAFE",
    "WATCH",
    "WARNING",
    "CRITICAL"
]:
    print(
        cls + ":",
        np.sum(df["warning_class"] == cls)
    )


# ============================================================
# Recovery Targets
# ============================================================

safe_states = df[
    df["warning_class"] == "SAFE"
].copy()

danger_states = df[
    df["warning_class"].isin(
        ["WARNING", "CRITICAL"]
    )
].copy()

print(
    "\nRecovery candidates:",
    len(danger_states)
)

safe_points = safe_states[
    ["pc1", "pc2"]
].values

danger_points = danger_states[
    ["pc1", "pc2"]
].values


# ============================================================
# Nearest Safe Arrival
# ============================================================

nn_safe = NearestNeighbors(
    n_neighbors=1
)

nn_safe.fit(
    safe_points
)

dist,
idx = nn_safe.kneighbors(
    danger_points
)

arrival_points = safe_points[
    idx.flatten()
]

danger_states["arrival_x"] = (
    arrival_points[:, 0]
)

danger_states["arrival_y"] = (
    arrival_points[:, 1]
)

danger_states["arrival_dist"] = (
    dist.flatten()
)


# ============================================================
# Recovery Anchor Discovery
# ============================================================

anchor_points = np.column_stack([
    danger_states["arrival_x"],
    danger_states["arrival_y"]
])

db = DBSCAN(
    eps=0.35,
    min_samples=2
)

anchor_labels = db.fit_predict(
    anchor_points
)

danger_states["anchor_id"] = (
    anchor_labels
)

valid = anchor_labels >= 0

n_anchors = len(
    np.unique(
        anchor_labels[valid]
    )
)

print(
    "\nRecovery Anchors:",
    n_anchors
)


# ============================================================
# Anchor Centers
# ============================================================

anchor_centers = []

for aid in np.unique(anchor_labels):

    if aid < 0:
        continue

    cluster = anchor_points[
        anchor_labels == aid
    ]

    center = cluster.mean(
        axis=0
    )

    anchor_centers.append(
        center
    )

anchor_centers = np.array(
    anchor_centers
)


# ============================================================
# Visual 1
# Recovery Anchor Clusters
# ============================================================

plt.figure(
    figsize=(10, 8)
)

plt.scatter(
    df["pc1"],
    df["pc2"],
    s=25,
    alpha=0.15,
    color="lightgray"
)

for aid in np.unique(anchor_labels):

    if aid < 0:
        continue

    subset = danger_states[
        danger_states["anchor_id"] == aid
    ]

    plt.scatter(
        subset["arrival_x"],
        subset["arrival_y"],
        s=80,
        label=f"A{aid}"
    )

plt.title(
    "EXP_36 Recovery Anchor Clusters"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp36_recovery_anchor_clusters.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Anchor Centers
# ============================================================

plt.figure(
    figsize=(10, 8)
)

plt.scatter(
    df["pc1"],
    df["pc2"],
    s=20,
    alpha=0.10,
    color="lightgray"
)

plt.scatter(
    anchor_centers[:, 0],
    anchor_centers[:, 1],
    s=350,
    marker="*",
    color="red"
)

plt.title(
    "EXP_36 Recovery Anchor Centers"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp36_recovery_anchor_centers.png",
    dpi=300
)

plt.close()
