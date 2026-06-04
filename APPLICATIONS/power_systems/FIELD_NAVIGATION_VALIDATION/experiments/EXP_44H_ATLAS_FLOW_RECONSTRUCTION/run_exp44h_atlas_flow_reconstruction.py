"""
EXP_44H
ATLAS FLOW RECONSTRUCTION

Goal
--------------------------------------------------
Reconstruct a local flow field directly from
the Atlas State Graph.

Author: NEXAH
"""

from pathlib import Path

import numpy as np
import pandas as pd
import networkx as nx

import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler


# ============================================================
# PATHS
# ============================================================

POWER_ROOT = (
    Path(__file__)
    .resolve()
    .parents[3]
)

OUTPUT_DIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44H_ATLAS_FLOW_RECONSTRUCTION"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

GRAPH_FILE = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44D_ATLAS_STATE_GRAPH_RECONSTRUCTION"
    / "atlas_state_graph.graphml"
)

DATA_FILE = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_34_CONTROL_EFFORT_ESTIMATION"
    / "exp34_control_effort_table.csv"
)

print()
print("POWER_ROOT ->", POWER_ROOT)
print()

print("Graph   ->", GRAPH_FILE)
print("Exists  ->", GRAPH_FILE.exists())
print()

print("Dataset ->", DATA_FILE)
print("Exists  ->", DATA_FILE.exists())
print()

print("Output  ->", OUTPUT_DIR)
print()


# ============================================================
# LOAD
# ============================================================

G = nx.read_graphml(GRAPH_FILE)

df = pd.read_csv(DATA_FILE)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print()


# ============================================================
# FEATURE SPACE
# ============================================================

FEATURES = [
    "PC1",
    "PC2"
]

X = df[FEATURES].copy()

scaler = StandardScaler()

Xs = scaler.fit_transform(X)

coords = pd.DataFrame(
    Xs,
    columns=["PC1", "PC2"]
)

coords["node"] = np.arange(len(coords))


# ============================================================
# FLOW VECTOR RECONSTRUCTION
# ============================================================

flow_records = []

for node in G.nodes():

    i = int(node)

    neighbors = list(G.successors(node))

    if len(neighbors) == 0:
        continue

    neighbors = [int(n) for n in neighbors]

    x0 = coords.loc[i, "PC1"]
    y0 = coords.loc[i, "PC2"]

    dx = []
    dy = []

    for j in neighbors:

        dx.append(
            coords.loc[j, "PC1"] - x0
        )

        dy.append(
            coords.loc[j, "PC2"] - y0
        )

    vx = np.mean(dx)
    vy = np.mean(dy)

    magnitude = np.sqrt(
        vx**2 + vy**2
    )

    flow_records.append(
        [
            i,
            x0,
            y0,
            vx,
            vy,
            magnitude
        ]
    )

flow_df = pd.DataFrame(
    flow_records,
    columns=[
        "node",
        "PC1",
        "PC2",
        "vx",
        "vy",
        "velocity"
    ]
)

flow_df.to_csv(
    OUTPUT_DIR /
    "exp44h_flow_vectors.csv",
    index=False
)

print("Flow vectors:", len(flow_df))


# ============================================================
# METRICS
# ============================================================

mean_velocity = (
    flow_df["velocity"]
    .mean()
)

max_velocity = (
    flow_df["velocity"]
    .max()
)

vectors = flow_df[
    ["vx", "vy"]
].values

norms = np.linalg.norm(
    vectors,
    axis=1
)

valid = norms > 0

unit_vectors = (
    vectors[valid]
    / norms[valid][:, None]
)

mean_direction = unit_vectors.mean(axis=0)

flow_coherence = np.linalg.norm(
    mean_direction
)

dominant_angle = np.degrees(
    np.arctan2(
        mean_direction[1],
        mean_direction[0]
    )
)


# ============================================================
# VISUAL 1
# FLOW FIELD
# ============================================================

plt.figure(figsize=(10, 8))

plt.quiver(
    flow_df["PC1"],
    flow_df["PC2"],
    flow_df["vx"],
    flow_df["vy"],
    angles="xy",
    scale_units="xy",
    scale=1,
    alpha=0.7
)

plt.title(
    "EXP_44H Atlas Flow Field"
)

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp44h_flow_field.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 2
# VELOCITY MAGNITUDE
# ============================================================

plt.figure(figsize=(10, 8))

plt.scatter(
    flow_df["PC1"],
    flow_df["PC2"],
    c=flow_df["velocity"],
    s=25
)

plt.colorbar(
    label="Velocity Magnitude"
)

plt.title(
    "EXP_44H Velocity Magnitude"
)

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp44h_velocity_magnitude.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 3
# TRANSPORT BACKBONE
# ============================================================

threshold = np.percentile(
    flow_df["velocity"],
    90
)

backbone = flow_df[
    flow_df["velocity"] >= threshold
]

plt.figure(figsize=(10, 8))

plt.quiver(
    backbone["PC1"],
    backbone["PC2"],
    backbone["vx"],
    backbone["vy"],
    angles="xy",
    scale_units="xy",
    scale=1
)

plt.title(
    "EXP_44H Transport Backbone"
)

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp44h_transport_backbone.png",
    dpi=300
)

plt.close()


# ============================================================
# REPORT
# ============================================================

report = f"""
EXP_44H ATLAS FLOW RECONSTRUCTION
==================================================

Nodes
------
{G.number_of_nodes()}

Edges
------
{G.number_of_edges()}

Flow Vectors
------------
{len(flow_df)}

Mean Velocity
-------------
{mean_velocity:.6f}

Maximum Velocity
----------------
{max_velocity:.6f}

Flow Coherence
--------------
{flow_coherence:.6f}

Dominant Direction (deg)
------------------------
{dominant_angle:.6f}

Interpretation
--------------
Local graph transport structure was
converted into a continuous vector field.

The Atlas is now represented as:

State Graph
      ↓
Flow Field
      ↓
Navigation Geometry

This is the first direct flow reconstruction
experiment within the EXP_44 campaign.
"""

with open(
    OUTPUT_DIR /
    "exp44h_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("Mean Velocity :", round(mean_velocity, 6))
print("Max Velocity  :", round(max_velocity, 6))
print("Flow Coherence:", round(flow_coherence, 6))
print("Direction Deg :", round(dominant_angle, 6))
print()

print("EXP_44H complete.")
print()
