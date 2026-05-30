"""
run_exp15_forced_regime_crossing.py

EXP_15 — FORCED REGIME CROSSING

Goal
-----
Determine how much displacement is required
to force a state across the discovered gate-axis.

Uses:
- EXP_08 field geometry
- EXP_09B gate ranking
- EXP_09C gate localization

NEXAH Validation Program
2026
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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
    / "EXP_15_FORCED_REGIME_CROSSING"
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
# Load Data
# ============================================================

df = pd.read_csv(
    INPUT_DIR / "exp08_field_states.csv"
)

print(
    f"Loaded states: {len(df)}"
)

Z = df[
    ["pca_x", "pca_y"]
].values


# ============================================================
# Gate Nodes
# ============================================================

gate_ids = [
    33,
    81,
    184,
    250,
    498,
    502
]

gate_points = np.array([
    df.loc[
        g,
        ["pca_x", "pca_y"]
    ].values.astype(float)
    for g in gate_ids
])

print()
print("Gate Nodes:")
print(gate_ids)
print()


# ============================================================
# Gate Axis
# ============================================================

A = gate_points[4]     # 498
B = gate_points[0]     # 33

axis = B - A

axis_norm = np.linalg.norm(
    axis
)

axis_unit = (
    axis / axis_norm
)

normal = np.array([
    -axis_unit[1],
     axis_unit[0]
])


# ============================================================
# Signed Distance
# ============================================================

signed_dist = []

for p in Z:

    rel = p - A

    d = (
        axis_unit[0] * rel[1]
        -
        axis_unit[1] * rel[0]
    )

    signed_dist.append(d)

signed_dist = np.array(
    signed_dist
)

df["signed_distance"] = (
    signed_dist
)


# ============================================================
# Crossing Search
# ============================================================

eps_values = np.linspace(
    0.0,
    20.0,
    200
)

critical_distance = []

for d0 in signed_dist:

    found = False

    for eps in eps_values:

        if d0 > 0:

            d_new = d0 - eps

        else:

            d_new = d0 + eps

        if np.sign(d_new) != np.sign(d0):

            critical_distance.append(
                eps
            )

            found = True
            break

    if not found:

        critical_distance.append(
            np.nan
        )

critical_distance = np.array(
    critical_distance
)

df["critical_distance"] = (
    critical_distance
)


# ============================================================
# Crossing Probability Curve
# ============================================================

crossing_probability = []

for eps in eps_values:

    crossed = 0

    for d0 in signed_dist:

        if abs(d0) <= eps:

            crossed += 1

    crossing_probability.append(
        crossed / len(signed_dist)
    )


# ============================================================
# Visual 1
# ============================================================

plt.figure(
    figsize=(8,5)
)

plt.plot(
    eps_values,
    crossing_probability,
    linewidth=3
)

plt.xlabel(
    "Forced Displacement"
)

plt.ylabel(
    "Crossing Probability"
)

plt.title(
    "EXP_15 — Crossing Probability"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp15_crossing_probability.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# ============================================================

plt.figure(
    figsize=(10,8)
)

plt.scatter(
    df["pca_x"],
    df["pca_y"],
    c=np.nan_to_num(
        critical_distance,
        nan=20
    ),
    s=25
)

plt.colorbar(
    label="Critical Distance"
)

plt.plot(
    gate_points[:,0],
    gate_points[:,1],
    linewidth=3
)

plt.scatter(
    gate_points[:,0],
    gate_points[:,1],
    s=150
)

plt.title(
    "EXP_15 — Crossing Map"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp15_crossing_map.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# ============================================================

plt.figure(
    figsize=(8,5)
)

vals = critical_distance[
    ~np.isnan(
        critical_distance
    )
]

plt.hist(
    vals,
    bins=30
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
    OUTPUT_DIR /
    "exp15_critical_distance_histogram.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 4
# ============================================================

segment_scores = []

for gp in gate_points:

    dist = np.linalg.norm(
        Z - gp,
        axis=1
    )

    segment_scores.append(
        np.mean(dist)
    )

plt.figure(
    figsize=(8,5)
)

plt.bar(
    range(len(gate_points)),
    segment_scores
)

plt.xlabel(
    "Gate Node Index"
)

plt.ylabel(
    "Mean Distance"
)

plt.title(
    "EXP_15 — Gate Sensitivity"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp15_gate_sensitivity.png",
    dpi=300
)

plt.close()


# ============================================================
# Metrics
# ============================================================

mean_cd = float(
    np.nanmean(
        critical_distance
    )
)

median_cd = float(
    np.nanmedian(
        critical_distance
    )
)

metrics = pd.DataFrame({

    "metric": [

        "states",
        "mean_critical_distance",
        "median_critical_distance"

    ],

    "value": [

        len(df),
        mean_cd,
        median_cd

    ]
})

metrics.to_csv(
    OUTPUT_DIR /
    "exp15_metrics.csv",
    index=False
)


# ============================================================
# Report
# ============================================================

report = f"""
EXP_15 FORCED REGIME CROSSING
========================================

States:
{len(df)}

Mean Critical Distance:
{mean_cd:.6f}

Median Critical Distance:
{median_cd:.6f}

Gate Nodes:
{gate_ids}

Interpretation
----------------------------------------

Critical distance measures
how much displacement is required
to force a state across the
discovered gate-axis.

Small values indicate
high regime sensitivity.

Large values indicate
deep basin stability.
"""

with open(
    OUTPUT_DIR /
    "exp15_report.txt",
    "w"
) as f:

    f.write(report)

print()
print("EXP_15 completed.")
print()

print(
    f"Mean Critical Distance: "
    f"{mean_cd:.4f}"
)

print(
    f"Median Critical Distance: "
    f"{median_cd:.4f}"
)
