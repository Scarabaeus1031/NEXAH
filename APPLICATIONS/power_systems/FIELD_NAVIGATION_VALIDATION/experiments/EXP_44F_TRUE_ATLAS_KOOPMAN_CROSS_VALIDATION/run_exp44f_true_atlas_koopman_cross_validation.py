# ============================================================
# EXP_44F
# TRUE ATLAS-KOOPMAN CROSS VALIDATION
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
import networkx as nx

import matplotlib.pyplot as plt

from scipy.linalg import eig
from scipy.sparse import csgraph


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
    / "EXP_44F_TRUE_ATLAS_KOOPMAN_CROSS_VALIDATION"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

GRAPH_FILE = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44D_ATLAS_STATE_GRAPH_RECONSTRUCTION"
    / "atlas_state_graph.graphml"
)

DATASET = (
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
print("Dataset ->", DATASET)
print("Exists  ->", DATASET.exists())
print()
print("Output  ->", OUTPUT_DIR)
print()


# ============================================================
# LOAD GRAPH
# ============================================================

G = nx.read_graphml(GRAPH_FILE)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())


# ============================================================
# ATLAS SPECTRUM
# ============================================================

A = nx.to_numpy_array(G)

atlas_eigs = np.linalg.eigvals(A)

atlas_abs = np.sort(np.abs(atlas_eigs))[::-1]

atlas_radius = float(atlas_abs[0])

print()
print("Atlas Spectral Radius:", atlas_radius)


# ============================================================
# LOAD STATE DATA
# ============================================================

df = pd.read_csv(DATASET)

features = [
    "PC1",
    "PC2",
    "warning_index",
    "exit_risk",
    "recovery_length",
    "control_effort",
    "basin_distance",
    "axis_distance",
]

X = df[features].values

X1 = X[:-1].T
X2 = X[1:].T


# ============================================================
# SIMPLE DMD / KOOPMAN
# ============================================================

U, S, VT = np.linalg.svd(X1, full_matrices=False)

r = min(10, len(S))

Ur = U[:, :r]
Sr = np.diag(S[:r])
Vr = VT[:r, :]

A_tilde = Ur.T @ X2 @ Vr.T @ np.linalg.inv(Sr)

koopman_eigs, _ = eig(A_tilde)

koopman_abs = np.sort(np.abs(koopman_eigs))[::-1]

koopman_radius = float(np.max(np.abs(koopman_eigs)))

print("Koopman Spectral Radius:", koopman_radius)


# ============================================================
# ALIGNMENT SCORE
# ============================================================

k = min(
    len(atlas_abs),
    len(koopman_abs),
    10,
)

atlas_top = atlas_abs[:k]
koopman_top = koopman_abs[:k]

atlas_top = atlas_top / np.max(atlas_top)
koopman_top = koopman_top / np.max(koopman_top)

alignment_score = np.corrcoef(
    atlas_top,
    koopman_top
)[0, 1]

print()
print("Alignment Score:", alignment_score)


# ============================================================
# SAVE TABLE
# ============================================================

compare_df = pd.DataFrame({
    "atlas": atlas_top,
    "koopman": koopman_top,
})

compare_df.to_csv(
    OUTPUT_DIR / "exp44f_spectral_alignment.csv",
    index=False
)


# ============================================================
# VISUAL 1
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    atlas_top,
    marker="o",
    label="Atlas"
)

plt.plot(
    koopman_top,
    marker="s",
    label="Koopman"
)

plt.title(
    "EXP_44F Atlas vs Koopman Spectrum"
)

plt.xlabel("Mode")
plt.ylabel("Normalized Magnitude")

plt.legend()

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp44f_spectrum_comparison.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 2
# ============================================================

plt.figure(figsize=(6, 6))

plt.scatter(
    atlas_top,
    koopman_top
)

plt.xlabel("Atlas")
plt.ylabel("Koopman")

plt.title(
    "EXP_44F Spectral Alignment"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp44f_alignment_scatter.png",
    dpi=300
)

plt.close()


# ============================================================
# REPORT
# ============================================================

report = f"""
EXP_44F TRUE ATLAS-KOOPMAN CROSS VALIDATION
==================================================

Nodes
------
{G.number_of_nodes()}

Edges
------
{G.number_of_edges()}

Atlas Spectral Radius
---------------------
{atlas_radius:.6f}

Koopman Spectral Radius
-----------------------
{koopman_radius:.6f}

Alignment Score
---------------
{alignment_score:.6f}

Interpretation
--------------
Alignment close to +1

=> Atlas spectrum strongly agrees
   with Koopman dynamics.

Alignment near 0

=> weak correspondence.

Alignment negative

=> incompatible dominant modes.
"""

with open(
    OUTPUT_DIR / "exp44f_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_44F complete.")
print()
print("Atlas Radius   :", atlas_radius)
print("Koopman Radius :", koopman_radius)
print("Alignment      :", alignment_score)
print()
