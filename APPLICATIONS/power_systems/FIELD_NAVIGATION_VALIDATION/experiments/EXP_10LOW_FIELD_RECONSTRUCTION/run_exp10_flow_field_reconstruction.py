"""
run_exp10_flow_field_reconstruction.py

EXP_10 — FLOW FIELD RECONSTRUCTION

Goal:
Reconstruct a continuous flow field from the real IEEE39
state-space and determine whether gate nodes lie on
coherent transport structures.

Data:
EXP_08_REAL_FIELD_GEOMETRY

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
    / "EXP_10_FLOW_FIELD_RECONSTRUCTION"
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
# Load EXP_08 States
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
# Gate Nodes from EXP_09C
# ============================================================

gate_nodes = np.array(
    [33, 81, 184, 250, 498, 502]
)

print(
    f"Gate nodes: {len(gate_nodes)}"
)


# ============================================================
# Local Flow Reconstruction
# ============================================================

K = 15

nbrs = NearestNeighbors(
    n_neighbors=K
)

nbrs.fit(Z)

distances, indices = nbrs.kneighbors(Z)

flow_vectors = []

for i in range(len(Z)):

    neighbors = indices[i][1:]

    local_vectors = (
        Z[neighbors]
        - Z[i]
    )

    flow = np.mean(
        local_vectors,
        axis=0
    )

    flow_vectors.append(flow)

flow_vectors = np.array(
    flow_vectors
)

flow_mag = np.linalg.norm(
    flow_vectors,
    axis=1
)

df["flow_x"] = flow_vectors[:, 0]
df["flow_y"] = flow_vectors[:, 1]
df["flow_magnitude"] = flow_mag


# ============================================================
# Local Flow Alignment
# ============================================================

alignment_scores = []

for i in range(len(Z)):

    neighbors = indices[i][1:]

    v0 = flow_vectors[i]

    n0 = np.linalg.norm(v0)

    if n0 < 1e-12:
        alignment_scores.append(0.0)
        continue

    local_align = []

    for j in neighbors:

        v1 = flow_vectors[j]

        n1 = np.linalg.norm(v1)

        if n1 < 1e-12:
            continue

        cos_theta = (
            np.dot(v0, v1)
            / (n0 * n1)
        )

        local_align.append(
            cos_theta
        )

    if len(local_align) == 0:
        alignment_scores.append(0.0)

    else:
        alignment_scores.append(
            np.mean(local_align)
        )

alignment_scores = np.array(
    alignment_scores
)

df["flow_alignment"] = (
    alignment_scores
)


# ============================================================
# Gate Metrics
# ============================================================

gate_records = []

for gate in gate_nodes:

    gate_records.append({
        "gate_node": int(gate),
        "pca_x": Z[gate, 0],
        "pca_y": Z[gate, 1],
        "flow_magnitude":
            flow_mag[gate],
        "flow_alignment":
            alignment_scores[gate]
    })

gate_df = pd.DataFrame(
    gate_records
)

gate_df.to_csv(
    OUTPUT_DIR /
    "exp10_gate_flow_metrics.csv",
    index=False
)


# ============================================================
# Visual 1
# ============================================================

plt.figure(
    figsize=(12, 10)
)

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    c=flow_mag,
    s=12,
    cmap="viridis"
)

plt.quiver(
    Z[:, 0],
    Z[:, 1],
    flow_vectors[:, 0],
    flow_vectors[:, 1],
    alpha=0.5
)

plt.colorbar(
    label="Flow Magnitude"
)

plt.title(
    "EXP_10 — Flow Vectors"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp10_flow_vectors.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# ============================================================

plt.figure(
    figsize=(12, 10)
)

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    c=alignment_scores,
    cmap="plasma",
    s=12
)

plt.scatter(
    Z[gate_nodes, 0],
    Z[gate_nodes, 1],
    s=250,
    color="red",
    label="Gate Nodes"
)

for gate in gate_nodes:

    plt.annotate(
        str(gate),
        (
            Z[gate, 0],
            Z[gate, 1]
        )
    )

plt.colorbar(
    label="Flow Alignment"
)

plt.legend()

plt.title(
    "EXP_10 — Gate Flow Overlay"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp10_gate_flow_overlay.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# ============================================================

plt.figure(
    figsize=(12, 10)
)

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    c=flow_mag,
    cmap="viridis",
    s=10,
    alpha=0.5
)

step = 4

plt.quiver(
    Z[::step, 0],
    Z[::step, 1],
    flow_vectors[::step, 0],
    flow_vectors[::step, 1],
    alpha=0.7
)

plt.scatter(
    Z[gate_nodes, 0],
    Z[gate_nodes, 1],
    s=250,
    color="red"
)

plt.title(
    "EXP_10 — Transport Structure"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp10_transport_structure.png",
    dpi=300
)

plt.close()


# ============================================================
# Metrics
# ============================================================

metrics = pd.DataFrame({
    "metric": [
        "mean_flow_magnitude",
        "max_flow_magnitude",
        "mean_alignment",
        "max_alignment"
    ],
    "value": [
        np.mean(flow_mag),
        np.max(flow_mag),
        np.mean(alignment_scores),
        np.max(alignment_scores)
    ]
})

metrics.to_csv(
    OUTPUT_DIR /
    "exp10_flow_metrics.csv",
    index=False
)


# ============================================================
# Report
# ============================================================

report = f"""
EXP_10 FLOW FIELD RECONSTRUCTION
========================================

States:
{len(Z)}

Gate Nodes:
{len(gate_nodes)}

Mean Flow Magnitude:
{np.mean(flow_mag):.6f}

Max Flow Magnitude:
{np.max(flow_mag):.6f}

Mean Flow Alignment:
{np.mean(alignment_scores):.6f}

Max Flow Alignment:
{np.max(alignment_scores):.6f}

Purpose
----------------------------------------

Determine whether the reconstructed
IEEE39 state-space contains coherent
flow structures and whether gate nodes
sit on transport-aligned regions.
"""

with open(
    OUTPUT_DIR /
    "exp10_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_10 completed.")
print()
print(gate_df)
print()
