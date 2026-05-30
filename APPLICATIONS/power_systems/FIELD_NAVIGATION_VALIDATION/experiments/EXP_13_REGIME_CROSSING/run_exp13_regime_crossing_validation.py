"""
run_exp13_regime_crossing_validation.py

EXP_13 — REGIME CROSSING VALIDATION

Goal
-----
Validate whether the gate-axis discovered in EXP_11 and
physically validated in EXP_12 is crossed by state-space
trajectories.

Important Note
--------------
The EXP_08 dataset is Monte-Carlo generated and is not
a true time series. Therefore EXP_13 should be interpreted
as a crossing-density experiment rather than a dynamical
trajectory experiment.

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
    / "EXP_13_REGIME_CROSSING"
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
# Gate Axis
# ============================================================

gate_ids = [502, 498, 81, 33]

max_idx = len(df) - 1

for g in gate_ids:

    if g > max_idx:

        raise ValueError(
            f"Gate {g} not present in dataframe "
            f"(max index={max_idx})"
        )

axis_points = np.array([
    df.loc[
        g,
        ["pca_x", "pca_y"]
    ].values.astype(float)
    for g in gate_ids
])

print()
print("Gate axis:")
print(gate_ids)
print()

A = axis_points[0]
B = axis_points[-1]

axis_vec = B - A

axis_norm = np.linalg.norm(
    axis_vec
)

if axis_norm < 1e-12:

    raise ValueError(
        "Gate axis length is zero."
    )

axis_unit = (
    axis_vec / axis_norm
)


# ============================================================
# Signed Distance
# ============================================================

signed_distance = []

for p in Z:

    rel = p - A

    cross = (
        axis_unit[0] * rel[1]
        -
        axis_unit[1] * rel[0]
    )

    signed_distance.append(
        cross
    )

signed_distance = np.array(
    signed_distance
)

df["signed_distance"] = (
    signed_distance
)

df["side"] = np.where(
    signed_distance >= 0,
    "LEFT",
    "RIGHT"
)

left_count = (
    df["side"] == "LEFT"
).sum()

right_count = (
    df["side"] == "RIGHT"
).sum()

print(
    f"LEFT states : {left_count}"
)

print(
    f"RIGHT states: {right_count}"
)


# ============================================================
# Crossing Detection
# ============================================================

crossings = []

sides = df["side"].values

for i in range(1, len(df)):

    if sides[i] == sides[i - 1]:
        continue

    crossings.append({

        "index_before":
            int(i - 1),

        "index_after":
            int(i),

        "from_side":
            str(sides[i - 1]),

        "to_side":
            str(sides[i]),

        "signed_before":
            float(
                signed_distance[i - 1]
            ),

        "signed_after":
            float(
                signed_distance[i]
            )
    })

cross_df = pd.DataFrame(
    crossings
)

cross_df.to_csv(
    OUTPUT_DIR /
    "exp13_crossings.csv",
    index=False
)

print()
print(
    f"Crossings detected: "
    f"{len(cross_df)}"
)
print()


# ============================================================
# Visual 1
# Regime Sequence
# ============================================================

regime_numeric = np.where(
    df["side"] == "LEFT",
    1,
    0
)

plt.figure(
    figsize=(12, 4)
)

plt.plot(
    regime_numeric,
    linewidth=1.5
)

plt.yticks(
    [0, 1],
    ["RIGHT", "LEFT"]
)

plt.xlabel(
    "Sample Index"
)

plt.ylabel(
    "Regime"
)

plt.title(
    "EXP_13 — Regime Sequence"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp13_regime_sequence.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Crossing Timeline
# ============================================================

plt.figure(
    figsize=(12, 4)
)

plt.plot(
    signed_distance,
    linewidth=1
)

plt.axhline(
    0,
    color="black",
    linestyle="--"
)

for c in crossings:

    plt.axvline(
        c["index_after"],
        color="red",
        alpha=0.15
    )

plt.xlabel(
    "Sample Index"
)

plt.ylabel(
    "Signed Distance"
)

plt.title(
    "EXP_13 — Crossing Timeline"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp13_crossing_timeline.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# Crossing Locations
# ============================================================

plt.figure(
    figsize=(10, 8)
)

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    color="lightgray",
    s=12
)

if len(cross_df) > 0:

    idx = cross_df[
        "index_after"
    ].values

    plt.scatter(
        Z[idx, 0],
        Z[idx, 1],
        color="red",
        s=60,
        label="Crossings"
    )

plt.plot(
    axis_points[:, 0],
    axis_points[:, 1],
    color="black",
    linewidth=3,
    label="Gate Axis"
)

plt.scatter(
    axis_points[:, 0],
    axis_points[:, 1],
    color="blue",
    s=150
)

plt.legend()

plt.title(
    "EXP_13 — Crossing Locations"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp13_crossing_locations.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 4
# Distance Histogram
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.hist(
    signed_distance,
    bins=40
)

plt.axvline(
    0,
    color="red",
    linestyle="--"
)

plt.xlabel(
    "Signed Distance"
)

plt.ylabel(
    "Count"
)

plt.title(
    "EXP_13 — Distance To Gate Axis"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp13_distance_histogram.png",
    dpi=300
)

plt.close()


# ============================================================
# Metrics
# ============================================================

metrics = pd.DataFrame({

    "metric": [

        "states",
        "left_states",
        "right_states",
        "crossings"

    ],

    "value": [

        len(df),
        left_count,
        right_count,
        len(cross_df)

    ]
})

metrics.to_csv(
    OUTPUT_DIR /
    "exp13_metrics.csv",
    index=False
)


# ============================================================
# Report
# ============================================================

report = f"""
EXP_13 REGIME CROSSING VALIDATION
========================================

States:
{len(df)}

LEFT States:
{left_count}

RIGHT States:
{right_count}

Crossings:
{len(cross_df)}

Interpretation
----------------------------------------

This experiment measures how frequently
samples switch sides relative to the
gate-axis:

502 -> 498 -> 81 -> 33

Because EXP_08 consists of Monte-Carlo
samples, crossing counts should be
interpreted as crossing density rather
than true temporal transitions.

A concentration of crossings near the
axis supports the hypothesis that the
gate corridor approximates a regime
boundary.
"""

with open(
    OUTPUT_DIR /
    "exp13_report.txt",
    "w"
) as f:

    f.write(report)

print()
print("EXP_13 completed.")
print()
