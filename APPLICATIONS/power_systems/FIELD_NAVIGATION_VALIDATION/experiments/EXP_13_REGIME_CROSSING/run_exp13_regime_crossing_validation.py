"""
run_exp13_regime_crossing_validation.py

EXP_13 — REGIME CROSSING VALIDATION

Goal
-----
Validate whether the gate-axis discovered in EXP_11 and
physically validated in EXP_12 is crossed by real system
trajectories.

Method
-------
1. Load EXP_08 state-space
2. Reconstruct gate-axis:
       502 -> 498 -> 81 -> 33
3. Compute signed side-distance for every state
4. Classify states:
       LEFT / RIGHT
5. Follow original simulation ordering
6. Detect regime crossings
7. Record crossing events
8. Visualize:
       - timeline
       - crossing locations
       - regime sequence

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
# Load data
# ============================================================

df = pd.read_csv(
    INPUT_DIR / "exp08_field_states.csv"
)

print(f"Loaded states: {len(df)}")


# ============================================================
# Gate axis
# ============================================================

gate_ids = [502, 498, 81, 33]

gate_df = df[
    df["state_id"].isin(gate_ids)
].copy()

gate_df = gate_df.set_index("state_id")

axis_points = np.array([
    gate_df.loc[g][["pca_x", "pca_y"]].values
    for g in gate_ids
])

A = axis_points[0]
B = axis_points[-1]

axis_vec = B - A

print("Gate axis:")
print(gate_ids)
print()


# ============================================================
# Signed distance
# ============================================================

points = df[
    ["pca_x", "pca_y"]
].values

rel = points - A

signed_dist = (
    axis_vec[0] * rel[:, 1]
    -
    axis_vec[1] * rel[:, 0]
)

df["side"] = np.where(
    signed_dist >= 0,
    "LEFT",
    "RIGHT"
)

df["signed_distance"] = signed_dist


# ============================================================
# Detect crossings
# ============================================================

crossings = []

sides = df["side"].values

for i in range(1, len(df)):

    if sides[i] != sides[i - 1]:

        crossings.append({
            "index_before": i - 1,
            "index_after": i,
            "from_side": sides[i - 1],
            "to_side": sides[i],
            "signed_before": signed_dist[i - 1],
            "signed_after": signed_dist[i]
        })

cross_df = pd.DataFrame(crossings)

cross_df.to_csv(
    OUTPUT_DIR / "exp13_crossings.csv",
    index=False
)

print(f"Crossings detected: {len(cross_df)}")


# ============================================================
# Regime sequence
# ============================================================

regime_numeric = np.where(
    df["side"] == "LEFT",
    1,
    0
)

plt.figure(figsize=(12, 4))

plt.plot(
    regime_numeric,
    lw=1.5
)

plt.yticks(
    [0, 1],
    ["RIGHT", "LEFT"]
)

plt.title(
    "EXP_13 — Regime Sequence"
)

plt.xlabel("Simulation State")
plt.ylabel("Regime")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp13_regime_sequence.png",
    dpi=300
)

plt.close()


# ============================================================
# Crossing timeline
# ============================================================

plt.figure(figsize=(12, 4))

plt.plot(
    signed_dist,
    lw=1.0,
    alpha=0.8
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

plt.title(
    "EXP_13 — Crossing Timeline"
)

plt.xlabel("Simulation State")
plt.ylabel("Signed Distance")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp13_crossing_timeline.png",
    dpi=300
)

plt.close()


# ============================================================
# Crossing locations
# ============================================================

plt.figure(figsize=(10, 8))

plt.scatter(
    df["pca_x"],
    df["pca_y"],
    c="lightgray",
    s=10
)

if len(cross_df) > 0:

    idx = cross_df["index_after"].values

    plt.scatter(
        df.iloc[idx]["pca_x"],
        df.iloc[idx]["pca_y"],
        s=80,
        c="red",
        label="Crossings"
    )

plt.plot(
    axis_points[:, 0],
    axis_points[:, 1],
    color="black",
    lw=3,
    label="Gate Axis"
)

plt.title(
    "EXP_13 — Crossing Locations"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp13_crossing_locations.png",
    dpi=300
)

plt.close()


# ============================================================
# Report
# ============================================================

with open(
    OUTPUT_DIR / "exp13_report.txt",
    "w"
) as f:

    f.write(
        "EXP_13 REGIME CROSSING VALIDATION\n"
    )

    f.write(
        "========================================\n\n"
    )

    f.write(
        f"States:\n{len(df)}\n\n"
    )

    f.write(
        f"Gate Axis:\n{' -> '.join(map(str, gate_ids))}\n\n"
    )

    f.write(
        f"Crossings:\n{len(cross_df)}\n\n"
    )

    if len(cross_df) > 0:

        f.write(
            "Interpretation\n"
        )

        f.write(
            "----------------------------------------\n\n"
        )

        f.write(
            "Detected trajectory transitions across\n"
        )

        f.write(
            "the gate-axis regime boundary.\n"
        )

print()
print("EXP_13 completed.")
print()
