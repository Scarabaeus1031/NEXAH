"""
==================================================
EXP_44C — ATLAS TRAJECTORY RECONSTRUCTION
==================================================

Python File:
run_exp44c_atlas_trajectory_reconstruction.py

Objective
--------------------------------------------------
Search existing NEXAH Power Systems outputs and
attempt to reconstruct usable trajectory matrices
for future Koopman analysis.

Author:
NEXAH Experimental Validation Program

Phase:
EXP_44C

Follow-up:
EXP_44D TRUE ATLAS-KOOPMAN CROSS VALIDATION
==================================================
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PATHS
# --------------------------------------------------

ROOT = Path(__file__).resolve()

while ROOT.name != "NEXAH":
    ROOT = ROOT.parent

POWER_ROOT = ROOT / "APPLICATIONS" / "power_systems"

OUTPUT_DIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44C_ATLAS_TRAJECTORY_RECONSTRUCTION"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Repository -> {POWER_ROOT}")
print(f"Output     -> {OUTPUT_DIR}")

# --------------------------------------------------
# SEARCH CONFIG
# --------------------------------------------------

TARGET_EXTENSIONS = {
    ".csv",
    ".txt",
    ".npy",
    ".npz",
    ".pkl"
}

TRAJECTORY_KEYWORDS = [
    "time",
    "step",
    "timestamp",
    "iteration",
    "frame",
    "sample",
    "trajectory",
    "history",
    "state",
    "states",
    "voltage",
    "voltages",
    "angle",
    "angles",
    "frequency",
    "frequencies"
]

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def detect_system(path_str):
    p = path_str.upper()

    if "IEEE300" in p:
        return "IEEE300"

    if "IEEE118" in p:
        return "IEEE118"

    if "IEEE39" in p:
        return "IEEE39"

    if "IEEE14" in p:
        return "IEEE14"

    if "IEEE9" in p:
        return "IEEE9"

    return "unknown"


def keyword_hits(path_str):
    path_str = path_str.lower()
    return sum(k in path_str for k in TRAJECTORY_KEYWORDS)


def numerical_ratio(df):
    try:
        numeric = df.select_dtypes(include=np.number)

        if numeric.shape[1] == 0:
            return 0.0

        return numeric.shape[1] / df.shape[1]

    except Exception:
        return 0.0


def classify_dataset(rows, cols, numeric_ratio_value):

    if rows > 100 and cols >= 2 and numeric_ratio_value > 0.8:
        return "READY"

    if rows > 20 and cols >= 2:
        return "PARTIAL"

    return "MISSING"


# --------------------------------------------------
# DISCOVERY
# --------------------------------------------------

records = []

for file in POWER_ROOT.rglob("*"):

    if not file.is_file():
        continue

    if file.suffix.lower() not in TARGET_EXTENSIONS:
        continue

    try:
        size_mb = file.stat().st_size / 1024 / 1024

        rec = {
            "path": str(file),
            "system": detect_system(str(file)),
            "extension": file.suffix.lower(),
            "size_mb": round(size_mb, 4),
            "keyword_hits": keyword_hits(str(file)),
            "rows": np.nan,
            "cols": np.nan,
            "numeric_ratio": np.nan,
            "suitability": "MISSING"
        }

        if file.suffix.lower() == ".csv":

            try:
                df = pd.read_csv(file)

                rows, cols = df.shape

                nr = numerical_ratio(df)

                suitability = classify_dataset(
                    rows,
                    cols,
                    nr
                )

                rec.update({
                    "rows": rows,
                    "cols": cols,
                    "numeric_ratio": nr,
                    "suitability": suitability
                })

            except Exception:
                pass

        records.append(rec)

    except Exception:
        continue

inventory = pd.DataFrame(records)

if inventory.empty:
    print("No assets discovered.")
    raise SystemExit

# --------------------------------------------------
# RECONSTRUCTABLE TRAJECTORIES
# --------------------------------------------------

trajectory_candidates = inventory[
    (
        inventory["suitability"].isin(
            ["READY", "PARTIAL"]
        )
    )
].copy()

trajectory_candidates = trajectory_candidates.sort_values(
    [
        "suitability",
        "rows",
        "cols",
        "keyword_hits"
    ],
    ascending=False
)

# --------------------------------------------------
# EXPORTS
# --------------------------------------------------

inventory.to_csv(
    OUTPUT_DIR / "exp44c_asset_inventory.csv",
    index=False
)

trajectory_candidates.to_csv(
    OUTPUT_DIR / "exp44c_reconstructed_trajectories.csv",
    index=False
)

trajectory_candidates.to_csv(
    OUTPUT_DIR / "exp44c_candidate_state_matrices.csv",
    index=False
)

ready_only = trajectory_candidates[
    trajectory_candidates["suitability"] == "READY"
]

ready_only.to_csv(
    OUTPUT_DIR / "exp44c_koopman_ready_datasets.csv",
    index=False
)

# --------------------------------------------------
# VISUAL 1
# DATASET RECOVERY
# --------------------------------------------------

plt.figure(figsize=(8,5))

inventory["suitability"].value_counts().plot(
    kind="bar"
)

plt.title(
    "EXP_44C Dataset Recovery"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "exp44c_dataset_recovery.png",
    dpi=300
)

plt.close()

# --------------------------------------------------
# VISUAL 2
# STATE DIMENSIONS
# --------------------------------------------------

dims = inventory["cols"].dropna()

if len(dims):

    plt.figure(figsize=(8,5))

    plt.hist(
        dims,
        bins=20
    )

    plt.title(
        "EXP_44C State Dimension Distribution"
    )

    plt.xlabel("Columns")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR /
        "exp44c_state_dimension_distribution.png",
        dpi=300
    )

    plt.close()

# --------------------------------------------------
# VISUAL 3
# TRAJECTORY LENGTHS
# --------------------------------------------------

lengths = inventory["rows"].dropna()

if len(lengths):

    plt.figure(figsize=(8,5))

    plt.hist(
        lengths,
        bins=20
    )

    plt.title(
        "EXP_44C Trajectory Length Distribution"
    )

    plt.xlabel("Rows")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR /
        "exp44c_trajectory_length_distribution.png",
        dpi=300
    )

    plt.close()

# --------------------------------------------------
# REPORT
# --------------------------------------------------

systems = (
    trajectory_candidates["system"]
    .value_counts()
    .to_dict()
)

with open(
    OUTPUT_DIR / "exp44c_report.txt",
    "w"
) as f:

    f.write(
        "EXP_44C ATLAS TRAJECTORY RECONSTRUCTION\n"
    )
    f.write("=" * 60 + "\n\n")

    f.write(
        f"Assets Discovered: {len(inventory)}\n"
    )

    f.write(
        f"Trajectory Candidates: {len(trajectory_candidates)}\n"
    )

    f.write(
        f"READY Datasets: {len(ready_only)}\n\n"
    )

    f.write("Systems\n")
    f.write("-" * 30 + "\n")

    for k, v in systems.items():
        f.write(f"{k}: {v}\n")

    f.write("\n")

    if len(ready_only):

        f.write(
            "Recommended Next Step:\n"
        )

        f.write(
            "EXP_44D TRUE ATLAS-KOOPMAN CROSS VALIDATION\n"
        )

    else:

        f.write(
            "No fully Koopman-ready datasets detected.\n"
        )

        f.write(
            "Additional trajectory generation may be required.\n"
        )

print()
print("EXP_44C complete.")
print()
print(
    f"Assets discovered: {len(inventory)}"
)
print(
    f"Trajectory candidates: {len(trajectory_candidates)}"
)
print(
    f"READY datasets: {len(ready_only)}"
)
