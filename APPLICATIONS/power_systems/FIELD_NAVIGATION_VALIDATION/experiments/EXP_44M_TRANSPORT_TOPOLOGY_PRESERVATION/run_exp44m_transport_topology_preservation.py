"""
EXP_44M
TRANSPORT TOPOLOGY PRESERVATION

Goal
--------------------------------------------------
Validate whether the large-scale transport topology
observed in EXP_44I is preserved after compression
into the EXP_44L Domain Supergraph.

This experiment tests the Atlas Shadow Matrix
observation.

Pipeline

Domain Transport Matrix
 ->
Domain Supergraph Matrix
 ->
Topology Preservation Metrics

Author
--------------------------------------------------
NEXAH / FIELD NAVIGATION VALIDATION
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import pearsonr, spearmanr


# ============================================================
# PATH DISCOVERY
# ============================================================

CURRENT = Path(__file__).resolve()

POWER_ROOT = next(
    p for p in CURRENT.parents
    if p.name == "power_systems"
)

TRANSPORT_MATRIX_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44I_ATLAS_GEODESIC_TRANSPORT"
    / "exp44i_domain_transport_matrix.csv"
)

SUPERGRAPH_MATRIX_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44L_DOMAIN_SUPERGRAPH_CONSTRUCTION"
    / "exp44l_supergraph_matrix.csv"
)

OUTDIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44M_TRANSPORT_TOPOLOGY_PRESERVATION"
)

OUTDIR.mkdir(parents=True, exist_ok=True)

print()
print("POWER_ROOT ->", POWER_ROOT)
print("Transport Matrix ->", TRANSPORT_MATRIX_PATH)
print("Exists          ->", TRANSPORT_MATRIX_PATH.exists())
print()

print("Supergraph Matrix ->", SUPERGRAPH_MATRIX_PATH)
print("Exists           ->", SUPERGRAPH_MATRIX_PATH.exists())
print()

print("Output ->", OUTDIR)
print()


# ============================================================
# LOAD MATRICES
# ============================================================

transport = pd.read_csv(
    TRANSPORT_MATRIX_PATH,
    index_col=0
)

supergraph = pd.read_csv(
    SUPERGRAPH_MATRIX_PATH,
    index_col=0
)

print("Transport Shape :", transport.shape)
print("Supergraph Shape:", supergraph.shape)
print()


# ============================================================
# ALIGN INDICES
# ============================================================

transport.index = transport.index.astype(str)
transport.columns = transport.columns.astype(str)

supergraph.index = supergraph.index.astype(str)
supergraph.columns = supergraph.columns.astype(str)

common = sorted(
    set(transport.index)
    & set(supergraph.index)
)

transport = transport.loc[common, common]
supergraph = supergraph.loc[common, common]


# ============================================================
# ============================================================
# FLATTEN MATRICES
# ============================================================

T = transport.values.astype(float)
S = supergraph.values.astype(float)

# remove diagonal

diag_mask = ~np.eye(
    T.shape[0],
    dtype=bool
)

t_vals = T[diag_mask]
s_vals = S[diag_mask]

# remove NaN / Inf pairs

valid_mask = (
    np.isfinite(t_vals)
    &
    np.isfinite(s_vals)
)

t_vals = t_vals[valid_mask]
s_vals = s_vals[valid_mask]

print("Valid Comparisons:", len(t_vals))
print()

# ============================================================
# CORRELATIONS
# ============================================================

pearson_corr, pearson_p = pearsonr(
    t_vals,
    s_vals
)

spearman_corr, spearman_p = spearmanr(
    t_vals,
    s_vals
)

frobenius = np.linalg.norm(
    np.nan_to_num(T)
    -
    np.nan_to_num(S)
)

print("Pearson  :", pearson_corr)
print("Spearman :", spearman_corr)
print("Frobenius:", frobenius)
print()


# ============================================================
# VISUAL 1
# MATRIX DIFFERENCE
# ============================================================

plt.figure(figsize=(10, 8))

difference_matrix = (
    np.nan_to_num(T)
    -
    np.nan_to_num(S)
)

plt.imshow(
    difference_matrix,
    aspect="auto"
)

plt.colorbar(
    label="Difference"
)

plt.title(
    "EXP_44M Matrix Difference"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44m_matrix_difference.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 2
# CORRELATION SCATTER
# ============================================================

plt.figure(figsize=(8, 8))

plt.scatter(
    t_vals,
    s_vals,
    alpha=0.7
)

plt.xlabel(
    "Transport Matrix"
)

plt.ylabel(
    "Supergraph Matrix"
)

plt.title(
    "EXP_44M Topology Preservation"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44m_correlation_scatter.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 3
# SHADOW OVERLAY
# ============================================================

T_clean = np.nan_to_num(T)
S_clean = np.nan_to_num(S)

overlay = (
    T_clean / np.nanmax(T_clean)
    +
    S_clean / np.nanmax(S_clean)
)

plt.figure(figsize=(10, 8))

plt.imshow(
    overlay,
    aspect="auto"
)

plt.colorbar(
    label="Overlay Intensity"
)

plt.title(
    "EXP_44M Atlas Shadow Validation"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44m_shadow_validation.png",
    dpi=300
)

plt.close()


# ============================================================
# SAVE TABLE
# ============================================================

results = pd.DataFrame([
    {
        "pearson": pearson_corr,
        "pearson_p": pearson_p,
        "spearman": spearman_corr,
        "spearman_p": spearman_p,
        "frobenius": frobenius
    }
])

results.to_csv(
    OUTDIR / "exp44m_metrics.csv",
    index=False
)


# ============================================================
# REPORT
# ============================================================

report = f"""
EXP_44M TRANSPORT TOPOLOGY PRESERVATION
==================================================

Domains
-------
{len(common)}

Pearson Correlation
-------------------
{pearson_corr:.6f}

Spearman Correlation
--------------------
{spearman_corr:.6f}

Frobenius Distance
------------------
{frobenius:.6f}

Interpretation
--------------
The Domain Transport Matrix from EXP_44I
was compared against the Domain Supergraph
Matrix from EXP_44L.

This experiment evaluates whether transport
topology survives domain-level compression.

Atlas Shadow Matrix hypothesis:
under investigation.
"""

print(report)

with open(
    OUTDIR / "exp44m_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_44M complete.")
print()
