# ============================================================
# EXP_37_ATLAS_INVARIANT_STUDY
#
# Phase E — Atlas Universality
#
# Goal:
# Determine whether atlas structures emerge
# consistently across IEEE benchmark systems.
#
# Input:
# Existing IEEE benchmark outputs
#
# Output:
# EXP_37_ATLAS_INVARIANT_STUDY
#
# Thomas Hofmann / NEXAH
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_37_ATLAS_INVARIANT_STUDY"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Output ->", OUTPUT_DIR)

# ============================================================
# IEEE Systems
# ============================================================

systems = [
    ("IEEE9", 9),
    ("IEEE14", 14),
    ("IEEE30", 30),
    ("IEEE39", 39),
    ("IEEE57", 57),
    ("IEEE118", 118),
    ("IEEE300", 300),
    ("IEEE1354", 1354),
    ("PEGASE9241", 9241)
]

# ============================================================
# Placeholder Results
#
# Replace progressively with real measurements
# extracted from each benchmark pipeline.
# ============================================================

atlas_results = []

for name, buses in systems:

    record = {
        "system": name,
        "buses": buses,

        "basins": np.nan,
        "gates": np.nan,
        "corridors": np.nan,

        "backbone": np.nan,
        "recovery": np.nan,

        "pc1_variance": np.nan
    }

    atlas_results.append(record)

df = pd.DataFrame(atlas_results)

# ============================================================
# IEEE39 Known Result
# ============================================================

df.loc[
    df.system == "IEEE39",
    [
        "basins",
        "gates",
        "corridors",
        "backbone",
        "recovery",
        "pc1_variance"
    ]
] = [
    18,
    6,
    29,
    1,
    1,
    87.85
]

# ============================================================
# Save Table
# ============================================================

csv_path = (
    OUTPUT_DIR
    / "exp37_atlas_invariants.csv"
)

df.to_csv(
    csv_path,
    index=False
)

print("\nSaved:", csv_path)

# ============================================================
# Visual 1
# Atlas Invariant Heatmap
# ============================================================

heatmap_df = df.copy()

heatmap_df["backbone"] = (
    heatmap_df["backbone"]
    .fillna(0)
)

heatmap_df["recovery"] = (
    heatmap_df["recovery"]
    .fillna(0)
)

heatmap_df = heatmap_df.set_index(
    "system"
)

cols = [
    "basins",
    "gates",
    "corridors",
    "backbone",
    "recovery"
]

plt.figure(figsize=(10,6))

sns.heatmap(
    heatmap_df[cols],
    annot=True,
    cmap="viridis"
)

plt.title(
    "EXP_37 Atlas Invariants"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37_atlas_invariants.png",
    dpi=300
)

plt.close()

# ============================================================
# Visual 2
# Scaling Laws
# ============================================================

plt.figure(figsize=(8,6))

valid = df["basins"].notna()

plt.plot(
    df.loc[valid, "buses"],
    df.loc[valid, "basins"],
    marker="o",
    label="Basins"
)

plt.plot(
    df.loc[valid, "buses"],
    df.loc[valid, "gates"],
    marker="s",
    label="Gates"
)

plt.plot(
    df.loc[valid, "buses"],
    df.loc[valid, "corridors"],
    marker="^",
    label="Corridors"
)

plt.xscale("log")

plt.xlabel("Bus Count")
plt.ylabel("Count")

plt.title(
    "EXP_37 Atlas Scaling"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37_scaling_laws.png",
    dpi=300
)

plt.close()

# ============================================================
# Visual 3
# PCA Dominance Comparison
# ============================================================

plt.figure(figsize=(8,6))

valid = df["pc1_variance"].notna()

plt.bar(
    df.loc[valid, "system"],
    df.loc[valid, "pc1_variance"]
)

plt.ylabel(
    "PC1 Variance (%)"
)

plt.title(
    "EXP_37 Dominant Geometry Mode"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37_pca_variance_comparison.png",
    dpi=300
)

plt.close()

# ============================================================
# Universality Score
# ============================================================

score = []

for _, row in df.iterrows():

    s = 0

    if pd.notna(row["basins"]):
        s += 1

    if pd.notna(row["gates"]):
        s += 1

    if pd.notna(row["corridors"]):
        s += 1

    if row["backbone"] == 1:
        s += 1

    if row["recovery"] == 1:
        s += 1

    score.append(s)

df["universality_score"] = score

# ============================================================
# Visual 4
# Universality Score
# ============================================================

plt.figure(figsize=(8,6))

plt.bar(
    df["system"],
    df["universality_score"]
)

plt.ylabel(
    "Universality Score"
)

plt.title(
    "EXP_37 Atlas Universality Score"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37_universality_score.png",
    dpi=300
)

plt.close()

# ============================================================
# Summary
# ============================================================

summary_path = (
    OUTPUT_DIR
    / "exp37_summary.txt"
)

with open(summary_path, "w") as f:

    f.write(
        "EXP_37 ATLAS INVARIANT STUDY\n"
    )

    f.write(
        "===========================\n\n"
    )

    f.write(
        "Objective:\n"
    )

    f.write(
        "Investigate whether atlas "
        "structures persist across "
        "multiple IEEE benchmark systems.\n\n"
    )

    f.write(
        "Questions:\n"
    )

    f.write(
        "- Do basins persist?\n"
        "- Do gates persist?\n"
        "- Do transport corridors persist?\n"
        "- Does a backbone emerge?\n"
        "- Does recovery structure emerge?\n\n"
    )

    f.write(
        "Current status:\n"
    )

    f.write(
        "IEEE39 populated.\n"
    )

    f.write(
        "Remaining systems pending extraction.\n"
    )

print("\nEXP_37 complete.")
