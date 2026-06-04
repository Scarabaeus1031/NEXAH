"""
EXP_44G
ATLAS PREDICTIVE VALIDATION

Goal:
Test whether local Atlas graph structure
contains predictive information about
future state geometry.

Author: NEXAH
"""

from pathlib import Path

import numpy as np
import pandas as pd

import networkx as nx

import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error


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
    / "EXP_44G_ATLAS_PREDICTIVE_VALIDATION"
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
# FEATURES
# ============================================================

FEATURES = [
    "PC1",
    "PC2",
    "warning_index",
    "exit_risk",
    "recovery_length",
    "control_effort",
    "basin_distance",
    "axis_distance"
]

X = df[FEATURES].copy()

scaler = StandardScaler()

Xs = scaler.fit_transform(X)

node_order = list(G.nodes())

node_order = [int(n) for n in node_order]

Xs = Xs[node_order]


# ============================================================
# PREDICT VIA GRAPH NEIGHBORS
# ============================================================

true_values = []
pred_values = []

for node in G.nodes():

    node_int = int(node)

    neighbors = list(G.successors(node))

    if len(neighbors) == 0:
        continue

    neighbors = [int(n) for n in neighbors]

    prediction = Xs[neighbors].mean(axis=0)

    truth = Xs[node_int]

    pred_values.append(prediction)
    true_values.append(truth)

pred_values = np.array(pred_values)
true_values = np.array(true_values)

errors = np.linalg.norm(
    pred_values - true_values,
    axis=1
)

mae = np.mean(
    np.abs(pred_values - true_values)
)

rmse = np.sqrt(
    mean_squared_error(
        true_values.flatten(),
        pred_values.flatten()
    )
)

accuracy = 1.0 / (1.0 + rmse)


# ============================================================
# SAVE TABLE
# ============================================================

results = pd.DataFrame()

results["prediction_error"] = errors

results.to_csv(
    OUTPUT_DIR /
    "exp44g_prediction_errors.csv",
    index=False
)


# ============================================================
# SCATTER
# ============================================================

plt.figure(figsize=(8,6))

plt.scatter(
    true_values[:,0],
    pred_values[:,0],
    alpha=0.6
)

plt.xlabel("True PC1")
plt.ylabel("Predicted PC1")

plt.title(
    "EXP_44G Atlas Prediction"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp44g_prediction_scatter.png",
    dpi=300
)

plt.close()


# ============================================================
# ERROR DISTRIBUTION
# ============================================================

plt.figure(figsize=(8,6))

plt.hist(
    errors,
    bins=30
)

plt.title(
    "EXP_44G Prediction Error Distribution"
)

plt.xlabel("Error")
plt.ylabel("Count")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp44g_prediction_error_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# ACCURACY BAR
# ============================================================

plt.figure(figsize=(6,5))

plt.bar(
    ["Atlas"],
    [accuracy]
)

plt.ylim(0,1)

plt.title(
    "EXP_44G Prediction Accuracy"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp44g_prediction_accuracy.png",
    dpi=300
)

plt.close()


# ============================================================
# REPORT
# ============================================================

report = f"""
EXP_44G ATLAS PREDICTIVE VALIDATION
==================================================

Nodes
------
{G.number_of_nodes()}

Edges
------
{G.number_of_edges()}

MAE
---
{mae:.6f}

RMSE
----
{rmse:.6f}

Prediction Accuracy
-------------------
{accuracy:.6f}

Interpretation
--------------
Atlas neighbors were used to predict
local state geometry.

High accuracy indicates that Atlas
structure contains predictive
information about future states.
"""

with open(
    OUTPUT_DIR /
    "exp44g_report.txt",
    "w"
) as f:
    f.write(report)

print("MAE      :", round(mae,6))
print("RMSE     :", round(rmse,6))
print("Accuracy :", round(accuracy,6))
print()

print("EXP_44G complete.")
print()
