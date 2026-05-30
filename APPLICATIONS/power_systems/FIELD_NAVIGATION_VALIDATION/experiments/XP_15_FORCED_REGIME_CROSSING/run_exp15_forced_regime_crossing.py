# ============================================================
# EXP_15 — FORCED REGIME CROSSING
#
# Goal:
# Measure how much displacement across the gate-axis
# is required to force a regime transition.
#
# Output:
#   exp15_crossing_probability.png
#   exp15_crossing_map.png
#   exp15_critical_distance_histogram.png
#   exp15_gate_sensitivity.png
#   exp15_summary.txt
#
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

INPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs",
    "EXP_08_REAL_FIELD_GEOMETRY"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs",
    "EXP_15_FORCED_REGIME_CROSSING"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\nInput  -> {INPUT_DIR}")
print(f"Output -> {OUTPUT_DIR}\n")

# ------------------------------------------------------------
# LOAD
# ------------------------------------------------------------

df = pd.read_csv(
    os.path.join(
        INPUT_DIR,
        "field_geometry_dataset.csv"
    )
)

print("Loaded states:", len(df))

# ------------------------------------------------------------
# GATE AXIS
# ------------------------------------------------------------

gate_points = np.array([
    [-11.0, 17.7],   # 502
    [-18.0, 14.0],   # 498
    [  0.0,  8.9],   # 81
    [ 15.0, -1.5]    # 33
])

# ------------------------------------------------------------
# DISTANCE TO POLYLINE
# ------------------------------------------------------------

def signed_distance_to_axis(point, polyline):

    best_dist = np.inf
    best_sign = 1.0

    p = np.asarray(point)

    for i in range(len(polyline)-1):

        a = polyline[i]
        b = polyline[i+1]

        ab = b - a
        ap = p - a

        t = np.dot(ap, ab) / np.dot(ab, ab)
        t = np.clip(t, 0, 1)

        proj = a + t * ab

        dvec = p - proj
        dist = np.linalg.norm(dvec)

        if dist < best_dist:

            best_dist = dist

            cross = (
                ab[0] * ap[1]
                -
                ab[1] * ap[0]
            )

            best_sign = np.sign(cross)

    return best_sign * best_dist


# ------------------------------------------------------------
# CLASSIFY REGIME
# ------------------------------------------------------------

distances = []

for _, row in df.iterrows():

    distances.append(
        signed_distance_to_axis(
            [row["pca_x"], row["pca_y"]],
            gate_points
        )
    )

df["signed_distance"] = distances

# ------------------------------------------------------------
# PERTURBATION TEST
# ------------------------------------------------------------

eps_values = np.linspace(
    0.1,
    10.0,
    40
)

crossing_prob = []

critical_distance = []

crossing_count_map = np.zeros(len(df))

for idx, row in df.iterrows():

    d0 = row["signed_distance"]

    found = False

    for eps in eps_values:

        d_new = d0 - np.sign(d0) * eps

        if np.sign(d_new) != np.sign(d0):

            critical_distance.append(eps)

            crossing_count_map[idx] += 1

            found = True
            break

    if not found:

        critical_distance.append(np.nan)

# ------------------------------------------------------------
# CROSSING PROBABILITY
# ------------------------------------------------------------

for eps in eps_values:

    crossings = 0

    for d0 in df["signed_distance"]:

        d_new = d0 - np.sign(d0) * eps

        if np.sign(d_new) != np.sign(d0):
            crossings += 1

    crossing_prob.append(
        crossings / len(df)
    )

# ------------------------------------------------------------
# VISUAL 1
# ------------------------------------------------------------

plt.figure(figsize=(8,5))

plt.plot(
    eps_values,
    crossing_prob,
    linewidth=2
)

plt.xlabel("Perturbation Size")
plt.ylabel("Crossing Probability")
plt.title("EXP_15 — Crossing Probability")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp15_crossing_probability.png"
    )
)

plt.close()

# ------------------------------------------------------------
# VISUAL 2
# ------------------------------------------------------------

plt.figure(figsize=(10,8))

plt.scatter(
    df["pca_x"],
    df["pca_y"],
    c=np.nan_to_num(
        critical_distance,
        nan=10
    ),
    cmap="viridis",
    s=25
)

plt.colorbar(
    label="Critical Distance"
)

plt.plot(
    gate_points[:,0],
    gate_points[:,1],
    color="red",
    linewidth=3
)

plt.title(
    "EXP_15 — Crossing Map"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp15_crossing_map.png"
    )
)

plt.close()

# ------------------------------------------------------------
# VISUAL 3
# ------------------------------------------------------------

plt.figure(figsize=(8,5))

vals = [
    x for x in critical_distance
    if not np.isnan(x)
]

plt.hist(
    vals,
    bins=20
)

plt.xlabel(
    "Critical Distance"
)

plt.ylabel(
    "Count"
)

plt.title(
    "EXP_15 — Critical Distance Histogram"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp15_critical_distance_histogram.png"
    )
)

plt.close()

# ------------------------------------------------------------
# VISUAL 4
# ------------------------------------------------------------

segment_sensitivity = []

for i in range(len(gate_points)-1):

    a = gate_points[i]
    b = gate_points[i+1]

    mid = (a+b)/2

    local = []

    for _, row in df.iterrows():

        d = np.linalg.norm(
            np.array(
                [row["pca_x"], row["pca_y"]]
            ) - mid
        )

        local.append(d)

    segment_sensitivity.append(
        np.mean(local)
    )

plt.figure(figsize=(8,5))

plt.bar(
    np.arange(len(segment_sensitivity)),
    segment_sensitivity
)

plt.xlabel("Gate Segment")
plt.ylabel("Mean Distance")
plt.title(
    "EXP_15 — Gate Sensitivity"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp15_gate_sensitivity.png"
    )
)

plt.close()

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

with open(
    os.path.join(
        OUTPUT_DIR,
        "exp15_summary.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_15 FORCED REGIME CROSSING\n"
    )
    f.write(
        "========================================\n\n"
    )

    f.write(
        f"States:\n{len(df)}\n\n"
    )

    f.write(
        f"Mean Critical Distance:\n"
        f"{np.nanmean(critical_distance):.6f}\n\n"
    )

    f.write(
        f"Median Critical Distance:\n"
        f"{np.nanmedian(critical_distance):.6f}\n\n"
    )

print("\nEXP_15 completed.\n")
