#!/usr/bin/env python3
"""
==========================================================
EXP_44B — ATLAS–KOOPMAN CROSS VALIDATION
==========================================================

Goal
-----
Compare NEXAH atlas structure against Koopman operator
structure using discovered trajectory datasets.

Outputs
-------
exp44b_koopman_modes.csv
exp44b_basin_mode_alignment.csv
exp44b_prediction_comparison.csv
exp44b_report.txt

Visuals
-------
exp44b_koopman_spectrum.png
exp44b_mode_energy.png
exp44b_prediction_accuracy.png

Author
------
Thomas Hofmann / NEXAH
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error


# ==========================================================
# PATHS
# ==========================================================

ROOT = Path(__file__).resolve()

for p in ROOT.parents:
    if (p / "APPLICATIONS").exists():
        REPO_ROOT = p
        break
else:
    raise RuntimeError("Repository root not found")

POWER_ROOT = REPO_ROOT / "APPLICATIONS" / "power_systems"

OUTPUT_DIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44B_ATLAS_KOOPMAN_CROSS_VALIDATION"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Repository -> {POWER_ROOT}")
print(f"Output     -> {OUTPUT_DIR}")


# ==========================================================
# DISCOVER CANDIDATE DATASETS
# ==========================================================

extensions = [".csv", ".txt"]

candidate_files = []

for ext in extensions:
    candidate_files.extend(POWER_ROOT.rglob(f"*{ext}"))

candidate_files = sorted(candidate_files)

print()
print(f"Files discovered: {len(candidate_files)}")


# ==========================================================
# LOAD NUMERICAL DATA
# ==========================================================

datasets = []

for file in candidate_files:

    try:

        if file.suffix == ".csv":
            df = pd.read_csv(file)

        else:
            df = pd.read_csv(file, sep=None, engine="python")

        numeric = df.select_dtypes(include=[np.number])

        if numeric.shape[0] < 20:
            continue

        if numeric.shape[1] < 2:
            continue

        datasets.append((file, numeric))

    except Exception:
        continue

print(f"Numerical datasets: {len(datasets)}")

if len(datasets) == 0:
    raise RuntimeError(
        "No numerical trajectory datasets found."
    )


# ==========================================================
# SELECT BEST DATASET
# ==========================================================

best_file = None
best_df = None
best_score = -1

for file, df in datasets:

    score = df.shape[0] * df.shape[1]

    if score > best_score:
        best_score = score
        best_file = file
        best_df = df

print()
print("Selected Dataset")
print(best_file)
print(best_df.shape)


# ==========================================================
# BUILD STATE MATRICES
# ==========================================================

X = best_df.values

X0 = X[:-1]
X1 = X[1:]

print()
print("State matrix shapes:")
print("X0:", X0.shape)
print("X1:", X1.shape)


# ==========================================================
# KOOPMAN OPERATOR
# ==========================================================

K = np.linalg.pinv(X0) @ X1

eigvals, eigvecs = np.linalg.eig(K)

koopman_df = pd.DataFrame(
    {
        "real": eigvals.real,
        "imag": eigvals.imag,
        "magnitude": np.abs(eigvals),
    }
)

koopman_df.to_csv(
    OUTPUT_DIR / "exp44b_koopman_modes.csv",
    index=False,
)

print("Saved Koopman modes")


# ==========================================================
# PCA ATLAS SPACE
# ==========================================================

pca = PCA(n_components=2)

coords = pca.fit_transform(X)

atlas_df = pd.DataFrame(
    {
        "pc1": coords[:, 0],
        "pc2": coords[:, 1],
    }
)

atlas_df["radius"] = np.sqrt(
    atlas_df.pc1**2 + atlas_df.pc2**2
)

atlas_df["basin"] = pd.qcut(
    atlas_df.radius,
    q=5,
    labels=False,
    duplicates="drop",
)

basin_summary = (
    atlas_df.groupby("basin")
    .agg(
        count=("basin", "size"),
        mean_radius=("radius", "mean"),
    )
    .reset_index()
)

basin_summary.to_csv(
    OUTPUT_DIR / "exp44b_basin_mode_alignment.csv",
    index=False,
)


# ==========================================================
# FORECAST TEST
# ==========================================================

X_pred = X0 @ K

rmse = np.sqrt(
    mean_squared_error(
        X1.flatten(),
        X_pred.flatten(),
    )
)

prediction_df = pd.DataFrame(
    {
        "metric": ["RMSE"],
        "value": [rmse],
    }
)

prediction_df.to_csv(
    OUTPUT_DIR / "exp44b_prediction_comparison.csv",
    index=False,
)


# ==========================================================
# VISUAL 1
# KOOPMAN SPECTRUM
# ==========================================================

plt.figure(figsize=(8, 6))

plt.scatter(
    eigvals.real,
    eigvals.imag,
)

plt.axhline(0, color="black")
plt.axvline(0, color="black")

plt.title("EXP_44B Koopman Spectrum")
plt.xlabel("Real")
plt.ylabel("Imaginary")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp44b_koopman_spectrum.png",
    dpi=300,
)

plt.close()


# ==========================================================
# VISUAL 2
# MODE ENERGY
# ==========================================================

energy = np.abs(eigvals)

energy = np.sort(energy)[::-1]

plt.figure(figsize=(8, 6))

plt.bar(
    np.arange(len(energy)),
    energy,
)

plt.title("EXP_44B Mode Energy")
plt.xlabel("Mode")
plt.ylabel("Magnitude")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp44b_mode_energy.png",
    dpi=300,
)

plt.close()


# ==========================================================
# VISUAL 3
# PREDICTION ACCURACY
# ==========================================================

plt.figure(figsize=(6, 5))

plt.bar(
    ["Koopman RMSE"],
    [rmse],
)

plt.title("EXP_44B Prediction Error")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp44b_prediction_accuracy.png",
    dpi=300,
)

plt.close()


# ==========================================================
# REPORT
# ==========================================================

report = f"""
EXP_44B ATLAS-KOOPMAN CROSS VALIDATION
==================================================

Dataset
--------
{best_file}

Shape
--------
Rows    : {best_df.shape[0]}
Columns : {best_df.shape[1]}

Koopman Modes
--------
Count : {len(eigvals)}

Forecast
--------
RMSE : {rmse:.6f}

Interpretation
--------
EXP_44B compares atlas-derived structure
against Koopman operator structure.

This is the first operator-theoretic
cross-validation experiment in the
NEXAH Power Systems program.
"""

with open(
    OUTPUT_DIR / "exp44b_report.txt",
    "w",
) as f:
    f.write(report)

print()
print("Saved report")

print()
print("EXP_44B complete.")
