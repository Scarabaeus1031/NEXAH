"""
run_exp12_regime_transition_crossing.py

EXP_12 — REGIME TRANSITION CROSSING

Goal:
Test whether the separatrix-like gate axis discovered in EXP_11
corresponds to measurable physical regime differences in IEEE39.

Question:
Does the gate axis separate operating states with different
voltage, loading, angle, and stress characteristics?

Input:
EXP_08_REAL_FIELD_GEOMETRY / exp08_field_states.csv

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
    / "EXP_12_REGIME_TRANSITION_CROSSING"
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
# Load field states
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
# Gate Axis from EXP_11
#
# 502 → 498 → 81 → 33
# ============================================================

gate_nodes = [502, 498, 81, 33]

gate_axis = Z[
    gate_nodes
]

axis_start = gate_axis[0]
axis_end = gate_axis[-1]

axis_vec = axis_end - axis_start
axis_vec = axis_vec / np.linalg.norm(axis_vec)


# ============================================================
# Signed Side Classification
# ============================================================

signed_distance = []

for p in Z:

    rel = p - axis_start

    cross = (
        axis_vec[0] * rel[1]
        - axis_vec[1] * rel[0]
    )

    signed_distance.append(cross)

signed_distance = np.array(
    signed_distance
)

df["signed_distance_to_axis"] = signed_distance

df["side"] = np.where(
    signed_distance >= 0,
    "LEFT",
    "RIGHT"
)

left_df = df[
    df["side"] == "LEFT"
]

right_df = df[
    df["side"] == "RIGHT"
]

print(f"LEFT states:  {len(left_df)}")
print(f"RIGHT states: {len(right_df)}")


# ============================================================
# Physical Metrics
# ============================================================

candidate_metrics = [
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

metrics = [
    m for m in candidate_metrics
    if m in df.columns
]

rows = []

for metric in metrics:

    left_values = left_df[metric].dropna().values
    right_values = right_df[metric].dropna().values

    left_mean = float(np.mean(left_values))
    right_mean = float(np.mean(right_values))

    left_std = float(np.std(left_values))
    right_std = float(np.std(right_values))

    diff = right_mean - left_mean

    pooled_std = np.sqrt(
        0.5 * (left_std ** 2 + right_std ** 2)
    )

    effect_size = (
        diff / pooled_std
        if pooled_std > 1e-12
        else 0.0
    )

    rows.append({
        "metric": metric,
        "left_mean": left_mean,
        "right_mean": right_mean,
        "difference_right_minus_left": diff,
        "left_std": left_std,
        "right_std": right_std,
        "effect_size": effect_size
    })

metrics_df = pd.DataFrame(rows)

metrics_df.to_csv(
    OUTPUT_DIR / "exp12_regime_metrics.csv",
    index=False
)

print()
print("Metric split:")
print(metrics_df.to_string(index=False))
print()


# ============================================================
# Visual 1 — Side Regimes
# ============================================================

plt.figure(figsize=(10, 8))

plt.scatter(
    left_df["pca_x"],
    left_df["pca_y"],
    s=18,
    alpha=0.75,
    label="LEFT"
)

plt.scatter(
    right_df["pca_x"],
    right_df["pca_y"],
    s=18,
    alpha=0.75,
    label="RIGHT"
)

plt.plot(
    gate_axis[:, 0],
    gate_axis[:, 1],
    linewidth=4,
    color="black",
    label="Gate Axis"
)

plt.scatter(
    gate_axis[:, 0],
    gate_axis[:, 1],
    s=220,
    color="red",
    label="Gates"
)

for node in gate_nodes:

    plt.annotate(
        str(node),
        (
            Z[node, 0],
            Z[node, 1]
        )
    )

plt.title("EXP_12 — Regime Split by Gate Axis")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.legend()
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp12_side_regimes.png",
    dpi=300
)

plt.close()


# ============================================================
# Helper for Boxplots
# ============================================================

def save_boxplot(metric, filename, title, ylabel):

    if metric not in df.columns:
        return

    plt.figure(figsize=(7, 6))

    plt.boxplot(
        [
            left_df[metric].dropna().values,
            right_df[metric].dropna().values
        ],
        labels=[
            "LEFT",
            "RIGHT"
        ]
    )

    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(True, axis="y")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / filename,
        dpi=300
    )

    plt.close()


# ============================================================
# Visual 2–5 — Physical Splits
# ============================================================

save_boxplot(
    "max_loading",
    "exp12_loading_split.png",
    "EXP_12 — Maximum Line Loading Split",
    "Max Loading"
)

save_boxplot(
    "min_vm",
    "exp12_voltage_split.png",
    "EXP_12 — Minimum Voltage Split",
    "Minimum Voltage"
)

save_boxplot(
    "angle_span",
    "exp12_angle_split.png",
    "EXP_12 — Angle Span Split",
    "Angle Span"
)

save_boxplot(
    "global_scale",
    "exp12_load_scale_split.png",
    "EXP_12 — Load Scale Split",
    "Global Load Scale"
)


# ============================================================
# Visual 6 — Effect Size Ranking
# ============================================================

plot_df = metrics_df.copy()
plot_df["abs_effect"] = plot_df["effect_size"].abs()

plot_df = plot_df.sort_values(
    "abs_effect",
    ascending=False
)

plt.figure(figsize=(10, 6))

plt.bar(
    plot_df["metric"],
    plot_df["effect_size"]
)

plt.axhline(
    0,
    color="black",
    linewidth=1
)

plt.xticks(rotation=45, ha="right")
plt.ylabel("Effect Size")
plt.title("EXP_12 — Regime Difference Effect Sizes")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp12_effect_size_ranking.png",
    dpi=300
)

plt.close()


# ============================================================
# Report
# ============================================================

top_metric = plot_df.iloc[0]

report = f"""
EXP_12 REGIME TRANSITION CROSSING
========================================

States:
{len(df)}

Gate Axis:
502 -> 498 -> 81 -> 33

LEFT States:
{len(left_df)}

RIGHT States:
{len(right_df)}

Strongest Regime Difference:
{top_metric["metric"]}

Effect Size:
{top_metric["effect_size"]:.6f}

Difference Right Minus Left:
{top_metric["difference_right_minus_left"]:.6f}

Interpretation
----------------------------------------

This experiment tests whether the gate-axis
separation discovered in EXP_11 corresponds
to measurable physical regime differences.

A non-zero effect size indicates that the
two sides of the gate axis are not merely
geometrically separated, but differ in
operating characteristics.

Large effects suggest that the gate axis
may correspond to a transition boundary
between power-system regimes.
"""

with open(
    OUTPUT_DIR / "exp12_report.txt",
    "w"
) as f:
    f.write(report)


print()
print("EXP_12 completed.")
print()
print(f"Strongest metric: {top_metric['metric']}")
print(f"Effect size: {top_metric['effect_size']:.6f}")
print()
