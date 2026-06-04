#!/usr/bin/env python3

"""
EXP_44A
TRAJECTORY ASSET DISCOVERY

Objective:
Discover numerical trajectory assets suitable for
future Koopman / EDMD / DMD analysis.
"""

import os
import csv
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ==================================================
# PATHS
# ==================================================

REPO_ROOT = Path(
    os.path.expanduser(
        "~/Documents/GitHub/NEXAH/APPLICATIONS/power_systems"
    )
)

OUTPUT_DIR = (
    REPO_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44A_TRAJECTORY_ASSET_DISCOVERY"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Repository -> {REPO_ROOT}")
print(f"Output     -> {OUTPUT_DIR}")
print()


# ==================================================
# CONFIG
# ==================================================

EXTENSIONS = {
    ".csv",
    ".txt",
    ".npy",
    ".npz",
    ".pkl"
}

KEYWORDS = [
    "trajectory",
    "trajectories",
    "timeseries",
    "time_series",
    "history",
    "state_vector",
    "state_vectors",
    "voltage",
    "voltages",
    "angle",
    "angles",
    "frequency",
    "frequencies",
    "observation",
    "observations",
    "state",
    "states",
    "bus",
    "buses",
]

SYSTEMS = [
    "ieee9",
    "ieee39",
    "ieee300"
]


# ==================================================
# HELPERS
# ==================================================

def detect_numeric_csv(path):
    try:
        df = pd.read_csv(path, nrows=500)

        rows = len(df)
        cols = len(df.columns)

        numeric_cols = df.select_dtypes(
            include=np.number
        ).shape[1]

        numeric_ratio = (
            numeric_cols / max(cols, 1)
        )

        return rows, cols, numeric_ratio

    except Exception:
        return None, None, 0.0


def classify_asset(
    extension,
    rows,
    cols,
    numeric_ratio,
    keyword_count,
):
    score = 0

    if keyword_count > 0:
        score += 1

    if rows and rows > 50:
        score += 1

    if cols and cols > 2:
        score += 1

    if numeric_ratio > 0.5:
        score += 2

    if extension in [".npy", ".npz"]:
        score += 2

    if score >= 5:
        return "READY"

    if score >= 3:
        return "PARTIAL"

    return "MISSING"


# ==================================================
# SCAN
# ==================================================

records = []

for path in REPO_ROOT.rglob("*"):

    if not path.is_file():
        continue

    ext = path.suffix.lower()

    if ext not in EXTENSIONS:
        continue

    path_str = str(path).lower()

    keyword_hits = [
        k for k in KEYWORDS
        if k in path_str
    ]

    rows = None
    cols = None
    numeric_ratio = 0.0

    if ext in [".csv", ".txt"]:
        rows, cols, numeric_ratio = detect_numeric_csv(path)

    size_mb = path.stat().st_size / 1024**2

    suitability = classify_asset(
        ext,
        rows,
        cols,
        numeric_ratio,
        len(keyword_hits),
    )

    system = "unknown"

    for s in SYSTEMS:
        if s in path_str:
            system = s.upper()
            break

    records.append({
        "path": str(path),
        "system": system,
        "extension": ext,
        "size_mb": round(size_mb, 3),
        "rows": rows,
        "cols": cols,
        "keyword_hits": len(keyword_hits),
        "numeric_ratio": round(numeric_ratio, 3),
        "suitability": suitability,
    })

inventory = pd.DataFrame(records)

print(
    f"Assets discovered: {len(inventory)}"
)


# ==================================================
# SAVE INVENTORY
# ==================================================

inventory_file = (
    OUTPUT_DIR
    / "exp44a_asset_inventory.csv"
)

inventory.to_csv(
    inventory_file,
    index=False
)

print(f"Saved: {inventory_file}")


# ==================================================
# KOOPMAN CANDIDATES
# ==================================================

candidates = inventory[
    inventory["suitability"] != "MISSING"
]

candidate_file = (
    OUTPUT_DIR
    / "exp44a_koopman_candidates.csv"
)

candidates.to_csv(
    candidate_file,
    index=False
)

print(f"Saved: {candidate_file}")


# ==================================================
# SUMMARY
# ==================================================

summary = (
    inventory
    .groupby(
        ["system", "suitability"]
    )
    .size()
    .reset_index(name="count")
)

summary_file = (
    OUTPUT_DIR
    / "exp44a_dataset_summary.csv"
)

summary.to_csv(
    summary_file,
    index=False
)

print(f"Saved: {summary_file}")


# ==================================================
# VISUAL 1
# ==================================================

inventory["extension"].value_counts().plot(
    kind="bar"
)

plt.title("Asset Types")
plt.tight_layout()

fig1 = (
    OUTPUT_DIR
    / "exp44a_asset_types.png"
)

plt.savefig(fig1, dpi=300)
plt.close()

print(f"Saved: {fig1}")


# ==================================================
# VISUAL 2
# ==================================================

system_counts = (
    candidates["system"]
    .value_counts()
)

system_counts.plot(
    kind="bar"
)

plt.title(
    "Trajectory Candidates by System"
)

plt.tight_layout()

fig2 = (
    OUTPUT_DIR
    / "exp44a_candidate_systems.png"
)

plt.savefig(fig2, dpi=300)
plt.close()

print(f"Saved: {fig2}")


# ==================================================
# VISUAL 3
# ==================================================

pivot = (
    summary
    .pivot(
        index="system",
        columns="suitability",
        values="count"
    )
    .fillna(0)
)

pivot.plot(
    kind="bar",
    stacked=True
)

plt.title(
    "Koopman Readiness"
)

plt.tight_layout()

fig3 = (
    OUTPUT_DIR
    / "exp44a_koopman_readiness.png"
)

plt.savefig(fig3, dpi=300)
plt.close()

print(f"Saved: {fig3}")


# ==================================================
# REPORT
# ==================================================

report = []

report.append(
    "EXP_44A TRAJECTORY ASSET DISCOVERY"
)

report.append("=" * 50)
report.append("")

report.append(
    f"Assets Discovered: {len(inventory)}"
)

report.append(
    f"Candidates: {len(candidates)}"
)

report.append("")

for system in SYSTEMS:

    subset = candidates[
        candidates["system"] == system.upper()
    ]

    report.append(
        f"{system.upper()}: "
        f"{len(subset)} candidates"
    )

report.append("")
report.append(
    "Recommended Next Step:"
)

report.append(
    "EXP_44B ATLAS-KOOPMAN "
    "CROSS VALIDATION"
)

report_file = (
    OUTPUT_DIR
    / "exp44a_report.txt"
)

with open(
    report_file,
    "w"
) as f:
    f.write("\n".join(report))

print(f"Saved: {report_file}")
print()
print("EXP_44A complete.")
