"""

run_exp16_targeted_regime_steering.py

EXP_16 — TARGETED REGIME STEERING

Goal

-----

Test whether targeted steering toward the discovered gate corridor

can force regime transitions more efficiently than random steering.

This is the first experiment in Phase C:

Field Control & Intervention.

Input

-----

EXP_08_REAL_FIELD_GEOMETRY / exp08_field_states.csv

Output

------

outputs/EXP_16_TARGETED_REGIME_STEERING/

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

    / "EXP_16_TARGETED_REGIME_STEERING"

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

Z = df[

    ["pca_x", "pca_y"]

].values

print(

    f"Loaded states: {len(df)}"

)

# ============================================================

# Gate Axis

#

# Dominant transport corridor from EXP_09C–EXP_15:

# 502 -> 498 -> 81 -> 33

# ============================================================

gate_ids = [502, 498, 81, 33]

for g in gate_ids:
    if g >= len(df):
        raise ValueError(
            f"Gate index {g} not present in dataframe with length {len(df)}"
        )

gate_points = np.array([
    df.loc[g, ["pca_x", "pca_y"]].values.astype(float)
    for g in gate_ids
])

A = gate_points[0]
B = gate_points[-1]

axis_vec = B - A
axis_norm = np.linalg.norm(axis_vec)

if axis_norm < 1e-12:
    raise ValueError("Gate axis has zero length.")

axis_unit = axis_vec / axis_norm

normal_vec = np.array([
    -axis_unit[1],
    axis_unit[0]
])

def signed_distance(point):

    rel = point - A

    return (

        axis_unit[0] * rel[1]

        -

        axis_unit[1] * rel[0]

    )

def nearest_point_on_axis(point):

    rel = point - A

    t = np.dot(

        rel,

        axis_unit

    )

    return (

        A

        + t * axis_unit

    )

def gate_direction(point):

    proj = nearest_point_on_axis(point)

    direction = (

        proj - point

    )

    norm = np.linalg.norm(

        direction

    )

    if norm < 1e-12:

        return np.zeros(2)

    return direction / norm

# ============================================================

# Regime Classification

# ============================================================

initial_side = np.array([

    1 if signed_distance(p) >= 0 else -1

    for p in Z

])

left_count = np.sum(

    initial_side < 0

)

right_count = np.sum(

    initial_side > 0

)

print()

print(f"LEFT states : {left_count}")

print(f"RIGHT states: {right_count}")

# ============================================================

# Steering Simulation

# ============================================================

MAX_STEPS = 20

STEP_SIZE = 1.0

rng = np.random.default_rng(

    42

)

random_crossings = []

gate_crossings = []

random_effort = []

gate_effort = []

for idx in range(len(Z)):

    start = Z[idx]

    start_side = (

        initial_side[idx]

    )

    # --------------------------------------------------------

    # Random Steering

    # --------------------------------------------------------

    crossed = False

    for step in range(

        1,

        MAX_STEPS + 1

    ):

        direction = rng.normal(

            size=2

        )

        norm = np.linalg.norm(

            direction

        )

        if norm < 1e-12:

            continue

        direction = (

            direction / norm

        )

        candidate = (

            start

            + step * STEP_SIZE * direction

        )

        new_side = (

            1

            if signed_distance(candidate) >= 0

            else -1

        )

        if new_side != start_side:

            crossed = True

            random_crossings.append(

                1

            )

            random_effort.append(

                step * STEP_SIZE

            )

            break

    if not crossed:

        random_crossings.append(

            0

        )

        random_effort.append(

            MAX_STEPS * STEP_SIZE

        )

    # --------------------------------------------------------

    # Gate Steering

    # --------------------------------------------------------

    crossed = False

    gate_dir = gate_direction(

        start

    )

    if np.linalg.norm(gate_dir) < 1e-12:

        gate_crossings.append(

            0

        )

        gate_effort.append(

            MAX_STEPS * STEP_SIZE

        )

        continue

    for step in range(

        1,

        MAX_STEPS + 1

    ):

        candidate = (

            start

            + step * STEP_SIZE * gate_dir

        )

        new_side = (

            1

            if signed_distance(candidate) >= 0

            else -1

        )

        if new_side != start_side:

            crossed = True

            gate_crossings.append(

                1

            )

            gate_effort.append(

                step * STEP_SIZE

            )

            break

    if not crossed:

        gate_crossings.append(

            0

        )

        gate_effort.append(

            MAX_STEPS * STEP_SIZE

        )

# ============================================================

# Metrics

# ============================================================

random_success = np.mean(

    random_crossings

)

gate_success = np.mean(

    gate_crossings

)

mean_random_effort = np.mean(

    random_effort

)

mean_gate_effort = np.mean(

    gate_effort

)

control_gain = (

    mean_random_effort

    /

    max(

        mean_gate_effort,

        1e-9

    )

)

print()

print(

    f"Random success: "

    f"{random_success:.4f}"

)

print(

    f"Gate success  : "

    f"{gate_success:.4f}"

)

print(

    f"Random effort : "

    f"{mean_random_effort:.4f}"

)

print(

    f"Gate effort   : "

    f"{mean_gate_effort:.4f}"

)

print(

    f"Control gain  : "

    f"{control_gain:.4f}"

)

# ============================================================

# Visual 1

# ============================================================

plt.figure(

    figsize=(8, 6)

)

plt.bar(

    ["Random", "Gate"],

    [

        random_success,

        gate_success

    ]

)

plt.ylabel(

    "Crossing Success"

)

plt.title(

    "EXP_16 — Crossing Success"

)

plt.tight_layout()

plt.savefig(

    OUTPUT_DIR

    /

    "exp16_crossing_success.png",

    dpi=300

)

plt.close()

# ============================================================

# Visual 2

# ============================================================

plt.figure(

    figsize=(8, 6)

)

plt.bar(

    ["Random", "Gate"],

    [

        mean_random_effort,

        mean_gate_effort

    ]

)

plt.ylabel(

    "Required Displacement"

)

plt.title(

    "EXP_16 — Required Effort"

)

plt.tight_layout()

plt.savefig(

    OUTPUT_DIR

    /

    "exp16_required_effort.png",

    dpi=300

)

plt.close()

# ============================================================

# Visual 3

# ============================================================

plt.figure(

    figsize=(10, 8)

)

plt.scatter(

    Z[:, 0],

    Z[:, 1],

    c=gate_crossings,

    s=20

)

plt.scatter(

    gate_points[:, 0],

    gate_points[:, 1],

    s=150,

    marker="*"

)

plt.title(

    "EXP_16 — Transition Map"

)

plt.tight_layout()

plt.savefig(

    OUTPUT_DIR

    /

    "exp16_transition_map.png",

    dpi=300

)

plt.close()

# ============================================================

# Visual 4

# ============================================================

plt.figure(

    figsize=(8, 6)

)

plt.bar(

    ["Control Gain"],

    [control_gain]

)

plt.title(

    "EXP_16 — Control Advantage"

)

plt.tight_layout()

plt.savefig(

    OUTPUT_DIR

    /

    "exp16_control_advantage.png",

    dpi=300

)

plt.close()

# ============================================================

# Metrics CSV

# ============================================================

metrics = pd.DataFrame({

    "metric": [

        "random_success",

        "gate_success",

        "random_effort",

        "gate_effort",

        "control_gain"

    ],

    "value": [

        random_success,

        gate_success,

        mean_random_effort,

        mean_gate_effort,

        control_gain

    ]

})

metrics.to_csv(

    OUTPUT_DIR

    /

    "exp16_metrics.csv",

    index=False

)

# ============================================================

# Report

# ============================================================

report = f"""

EXP_16 TARGETED REGIME STEERING

========================================

States:

{len(Z)}

Random Success:

{random_success:.6f}

Gate Success:

{gate_success:.6f}

Random Effort:

{mean_random_effort:.6f}

Gate Effort:

{mean_gate_effort:.6f}

Control Gain:

{control_gain:.6f}

"""

with open(

    OUTPUT_DIR

    /

    "exp16_report.txt",

    "w"

) as f:

    f.write(report)

print()

print("EXP_16 completed.")

print()
