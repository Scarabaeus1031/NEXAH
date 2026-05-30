"""
run_exp11_separatrix_validation.py

EXP_11 — SEPARATRIX VALIDATION

Goal:
Test whether the discovered gate axis

    502 → 498 → 81 → 33

acts as a genuine field separatrix.

Idea:

If the axis is a separatrix:

    - flow directions should differ across sides
    - transport alignment should change
    - neighboring regions should belong to different regimes

NEXAH Validation Program
2026
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.neighbors import NearestNeighbors


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
    / "EXP_11_SEPARATRIX_VALIDATION"
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
# Load EXP_08 states
# ============================================================

df = pd.read_csv(
    INPUT_DIR / "exp08_field_states.csv"
)

Z = df[
    ["pca_x", "pca_y"]
].values

print(
    f"Loaded states: {len(Z)}"
)


# ============================================================
# Gate axis
# ============================================================

gate_axis = np.array([
    [-10.369392, 17.672372],   # 502
    [-17.767905, 14.031123],   # 498
    [ -0.118425,  8.917799],   # 81
    [ 14.986344, -1.566608]    # 33
])

axis_start = gate_axis[0]
axis_end   = gate_axis[-1]

axis_vec = axis_end - axis_start
axis_vec = axis_vec / np.linalg.norm(axis_vec)


# ============================================================
# Point-to-axis signed distance
# ============================================================

signed_side = []

for p in Z:

    rel = p - axis_start

    cross = (
        axis_vec[0] * rel[1]
        - axis_vec[1] * rel[0]
    )

    signed_side.append(cross)

signed_side = np.array(
    signed_side
)

df["side"] = np.sign(
    signed_side
)

left_mask = signed_side > 0
right_mask = signed_side < 0

print(
    f"Left side states: {left_mask.sum()}"
)

print(
    f"Right side states: {right_mask.sum()}"
)


# ============================================================
# Reconstruct local flow field
# ============================================================

K = 12

nbrs = NearestNeighbors(
    n_neighbors=K
)

nbrs.fit(Z)

distances, indices = nbrs.kneighbors(Z)

flow_vectors = []

for i in range(len(Z)):

    center = Z[i]

    neigh = Z[
        indices[i][1:]
    ]

    local_flow = np.mean(
        neigh - center,
        axis=0
    )

    flow_vectors.append(
        local_flow
    )

flow_vectors = np.array(
    flow_vectors
)


# ============================================================
# Alignment with gate axis
# ============================================================

axis_alignment = []

for vec in flow_vectors:

    mag = np.linalg.norm(vec)

    if mag < 1e-10:

        axis_alignment.append(
            0.0
        )

    else:

        align = np.dot(
            vec / mag,
            axis_vec
        )

        axis_alignment.append(
            align
        )

axis_alignment = np.array(
    axis_alignment
)

df["axis_alignment"] = (
    axis_alignment
)


# ============================================================
# Metrics
# ============================================================

left_mean = np.mean(
    axis_alignment[left_mask]
)

right_mean = np.mean(
    axis_alignment[right_mask]
)

alignment_gap = abs(
    left_mean - right_mean
)

print()
print(
    f"Left alignment : {left_mean:.4f}"
)

print(
    f"Right alignment: {right_mean:.4f}"
)

print(
    f"Alignment gap  : {alignment_gap:.4f}"
)
print()


# ============================================================
# Visual 1
# Gate Axis
# ============================================================

plt.figure(
    figsize=(10, 8)
)

plt.scatter(
    Z[:,0],
    Z[:,1],
    s=15,
    alpha=0.5
)

plt.plot(
    gate_axis[:,0],
    gate_axis[:,1],
    linewidth=4,
    color="red"
)

plt.scatter(
    gate_axis[:,0],
    gate_axis[:,1],
    s=250,
    color="red"
)

plt.title(
    "EXP_11 — Gate Axis"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp11_gate_axis.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Side Classification
# ============================================================

plt.figure(
    figsize=(10,8)
)

plt.scatter(
    Z[left_mask,0],
    Z[left_mask,1],
    s=20,
    label="Left"
)

plt.scatter(
    Z[right_mask,0],
    Z[right_mask,1],
    s=20,
    label="Right"
)

plt.plot(
    gate_axis[:,0],
    gate_axis[:,1],
    color="black",
    linewidth=3
)

plt.legend()

plt.title(
    "EXP_11 — Side Classification"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp11_side_classification.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# Alignment Split
# ============================================================

plt.figure(
    figsize=(10,8)
)

plt.scatter(
    Z[:,0],
    Z[:,1],
    c=axis_alignment,
    cmap="coolwarm",
    s=20
)

plt.colorbar(
    label="Axis Alignment"
)

plt.plot(
    gate_axis[:,0],
    gate_axis[:,1],
    color="black",
    linewidth=3
)

plt.title(
    "EXP_11 — Flow Direction Split"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp11_flow_direction_split.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 4
# Separatrix Score
# ============================================================

plt.figure(
    figsize=(8,5)
)

plt.bar(
    ["Alignment Gap"],
    [alignment_gap]
)

plt.title(
    "EXP_11 — Separatrix Score"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp11_separatrix_score.png",
    dpi=300
)

plt.close()


# ============================================================
# Metrics CSV
# ============================================================

metrics = pd.DataFrame({
    "metric": [
        "left_alignment",
        "right_alignment",
        "alignment_gap"
    ],
    "value": [
        left_mean,
        right_mean,
        alignment_gap
    ]
})

metrics.to_csv(
    OUTPUT_DIR /
    "exp11_axis_metrics.csv",
    index=False
)


# ============================================================
# Report
# ============================================================

report = f"""
EXP_11 SEPARATRIX VALIDATION
========================================

States:
{len(Z)}

Left Side States:
{left_mask.sum()}

Right Side States:
{right_mask.sum()}

Mean Left Alignment:
{left_mean:.6f}

Mean Right Alignment:
{right_mean:.6f}

Alignment Gap:
{alignment_gap:.6f}

Interpretation
----------------------------------------

Large alignment gap:

    candidate separatrix

Small alignment gap:

    transport corridor

Gate axis tested:

502 → 498 → 81 → 33
"""

with open(
    OUTPUT_DIR /
    "exp11_results.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_11 completed.")
print()
