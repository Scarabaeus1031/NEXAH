# ============================================================
# EXP_30 — BASIN EXIT FORECASTING
#
# Question:
# Can we identify states that are close to leaving
# their current basin?
#
# Goal:
# Estimate basin-exit risk using:
#
# - distance to attractor
# - local density
# - distance to nearest foreign basin
#
# Outputs:
#
# exp30_exit_risk_map.png
# exp30_exit_candidates.png
# exp30_density_vs_risk.png
# exp30_boundary_candidates.png
# exp30_exit_table.csv
# exp30_summary.txt
#
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
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
    "EXP_30_BASIN_EXIT_FORECASTING"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

print("\nInput  ->", os.path.abspath(INPUT_DIR))
print("Output ->", os.path.abspath(OUTPUT_DIR))

# ------------------------------------------------------------
# Load Data
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
# PCA
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
# kNN Graph
# ------------------------------------------------------------

K = 12

nbrs = NearestNeighbors(
    n_neighbors=K + 1
).fit(coords)

distances, indices = nbrs.kneighbors(coords)

# ------------------------------------------------------------
# Density
# ------------------------------------------------------------

mean_knn_distance = (
    distances[:, 1:]
    .mean(axis=1)
)

density = 1.0 / (
    mean_knn_distance + 1e-9
)

# ------------------------------------------------------------
# Reconstruct Basins
# (same logic as EXP_24E)
# ------------------------------------------------------------

attractor_of = {}

for node in range(len(coords)):

    current = node
    visited = set()

    while True:

        if current in visited:
            break

        visited.add(current)

        neighbors = indices[
            current,
            1:
        ]

        best = current
        best_density = density[current]

        for n in neighbors:

            if density[n] > best_density:

                best_density = density[n]
                best = int(n)

        if best == current:
            break

        current = best

    attractor_of[node] = current

attractors = sorted(
    list(
        set(
            attractor_of.values()
        )
    )
)

basin_lookup = {
    a: i
    for i, a in enumerate(attractors)
}

node_basin = np.array([
    basin_lookup[
        attractor_of[i]
    ]
    for i in range(len(coords))
])

n_basins = len(attractors)

print(
    "Basins:",
    n_basins
)

# ------------------------------------------------------------
# Basin Centers
# ------------------------------------------------------------

basin_centers = {}

for basin in range(n_basins):

    members = np.where(
        node_basin == basin
    )[0]

    center = coords[
        members
    ].mean(axis=0)

    basin_centers[
        basin
    ] = center

# ------------------------------------------------------------
# Distance To Attractor
# ------------------------------------------------------------

distance_to_center = np.zeros(
    len(coords)
)

for i in range(len(coords)):

    basin = node_basin[i]

    center = basin_centers[
        basin
    ]

    distance_to_center[i] = (
        np.linalg.norm(
            coords[i] - center
        )
    )

# ------------------------------------------------------------
# Distance To Nearest Foreign Basin
# ------------------------------------------------------------

foreign_distance = np.zeros(
    len(coords)
)

for i in range(len(coords)):

    basin = node_basin[i]

    foreign_nodes = np.where(
        node_basin != basin
    )[0]

    d = np.linalg.norm(
        coords[foreign_nodes]
        - coords[i],
        axis=1
    )

    foreign_distance[i] = d.min()

# ------------------------------------------------------------
# Normalize Metrics
# ------------------------------------------------------------

center_score = (
    distance_to_center
    /
    distance_to_center.max()
)

density_score = (
    1.0
    -
    density / density.max()
)

foreign_score = (
    1.0
    -
    foreign_distance
    /
    foreign_distance.max()
)

# ------------------------------------------------------------
# Exit Risk
# ------------------------------------------------------------

exit_risk = (
    0.4 * center_score
    +
    0.3 * density_score
    +
    0.3 * foreign_score
)

df["exit_risk"] = (
    exit_risk
)

# ------------------------------------------------------------
# Top Exit Candidates
# ------------------------------------------------------------

candidate_idx = np.argsort(
    exit_risk
)[::-1]

top_n = 25

top_candidates = candidate_idx[
    :top_n
]

exit_table = pd.DataFrame({
    "node": top_candidates,
    "basin": node_basin[
        top_candidates
    ],
    "exit_risk": exit_risk[
        top_candidates
    ]
})

exit_table.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "exp30_exit_table.csv"
    ),
    index=False
)

print(
    "Top candidates:",
    len(top_candidates)
)

# ------------------------------------------------------------
# Visual 1
# Exit Risk Map
# ------------------------------------------------------------

plt.figure(
    figsize=(10, 8)
)

scatter = plt.scatter(
    coords[:, 0],
    coords[:, 1],
    c=exit_risk,
    s=20
)

plt.colorbar(
    scatter,
    label="Exit Risk"
)

plt.title(
    "EXP_30 Basin Exit Risk Map"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp30_exit_risk_map.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Visual 2
# Exit Candidates
# ------------------------------------------------------------

plt.figure(
    figsize=(10, 8)
)

plt.scatter(
    coords[:, 0],
    coords[:, 1],
    alpha=0.25
)

plt.scatter(
    coords[
        top_candidates,
        0
    ],
    coords[
        top_candidates,
        1
    ],
    s=80
)

plt.title(
    "EXP_30 Exit Candidates"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp30_exit_candidates.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Visual 3
# Density vs Exit Risk
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 6)
)

plt.scatter(
    density,
    exit_risk,
    alpha=0.6
)

plt.xlabel(
    "Density"
)

plt.ylabel(
    "Exit Risk"
)

plt.title(
    "EXP_30 Density vs Exit Risk"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp30_density_vs_risk.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Visual 4
# Boundary Candidates
# ------------------------------------------------------------

plt.figure(
    figsize=(10, 8)
)

scatter = plt.scatter(
    coords[:, 0],
    coords[:, 1],
    c=foreign_distance,
    s=20
)

plt.colorbar(
    scatter,
    label="Nearest Foreign Basin Distance"
)

plt.title(
    "EXP_30 Basin Boundary Candidates"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp30_boundary_candidates.png"
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
        "exp30_summary.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_30 BASIN EXIT FORECASTING\n"
    )

    f.write(
        "========================================\n\n"
    )

    f.write(
        f"States: {len(coords)}\n"
    )

    f.write(
        f"Basins: {n_basins}\n"
    )

    f.write(
        f"Top Exit Candidates: {top_n}\n"
    )

print(
    "\nEXP_30 completed."
)
