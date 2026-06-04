# ============================================================
# EXP_37F_ATLAS_SCALING_ANALYSIS
#
# Phase E — Atlas Universality
#
# Goal:
# Investigate how atlas complexity scales
# with network size.
#
# Input:
# EXP_37B_MULTI_SYSTEM_BASIN_EXTRACTION
#
# Output:
# EXP_37F_ATLAS_SCALING_ANALYSIS
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

INPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_37B_MULTI_SYSTEM_BASIN_EXTRACTION"
)

OUTPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_37F_ATLAS_SCALING_ANALYSIS"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Input  ->", INPUT_DIR)
print("Output ->", OUTPUT_DIR)


# ============================================================
# Load Basin Summary
# ============================================================

summary_file = (
    INPUT_DIR
    / "exp37b_v4_basin_summary.csv"
)

if not summary_file.exists():

    raise FileNotFoundError(
        f"Missing: {summary_file}"
    )

df = pd.read_csv(summary_file)

print()
print(df)


# ============================================================
# System Sizes
# ============================================================

BUS_COUNTS = {

    "IEEE9": 9,
    "IEEE14": 14,
    "IEEE30": 30,
    "IEEE39": 39,
    "IEEE57": 57,
    "IEEE118": 118,
    "IEEE300": 300,
    "IEEE1354": 1354,
    "PEGASE9241": 9241
}

df["buses"] = (
    df["system"]
    .map(BUS_COUNTS)
)

df = df.dropna(
    subset=["buses"]
)

df["buses"] = (
    df["buses"]
    .astype(int)
)


# ============================================================
# Compression Metrics
# ============================================================

df["compression_ratio"] = (
    df["buses"]
    /
    df["effective_basins"]
)

df["entropy_per_bus"] = (
    df["basin_entropy"]
    /
    df["buses"]
)

df["basins_per_bus"] = (
    df["n_basins"]
    /
    df["buses"]
)


# ============================================================
# Save Table
# ============================================================

table_file = (
    OUTPUT_DIR
    / "exp37f_scaling_table.csv"
)

df.to_csv(
    table_file,
    index=False
)

print()
print("Saved:", table_file)


# ============================================================
# Visual 1
# Basin Scaling
# ============================================================

plt.figure(figsize=(8, 6))

plt.plot(
    df["buses"],
    df["n_basins"],
    marker="o"
)

plt.xscale("log")

plt.xlabel("Bus Count")
plt.ylabel("Basins")

plt.title(
    "Atlas Basin Scaling"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37f_basin_scaling.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Effective Basin Scaling
# ============================================================

plt.figure(figsize=(8, 6))

plt.plot(
    df["buses"],
    df["effective_basins"],
    marker="o"
)

plt.xscale("log")

plt.xlabel("Bus Count")
plt.ylabel("Effective Basins")

plt.title(
    "Atlas Effective Basin Scaling"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37f_effective_scaling.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# Entropy Scaling
# ============================================================

plt.figure(figsize=(8, 6))

plt.plot(
    df["buses"],
    df["basin_entropy"],
    marker="o"
)

plt.xscale("log")

plt.xlabel("Bus Count")
plt.ylabel("Entropy")

plt.title(
    "Atlas Entropy Scaling"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37f_entropy_scaling.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 4
# Compression Ratio
# ============================================================

plt.figure(figsize=(8, 6))

plt.plot(
    df["buses"],
    df["compression_ratio"],
    marker="o"
)

plt.xscale("log")

plt.xlabel("Bus Count")
plt.ylabel("Compression Ratio")

plt.title(
    "Atlas Compression Ratio"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37f_compression_ratio.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 5
# Scaling Heatmap
# ============================================================

heatmap_df = df[
    [
        "system",
        "buses",
        "n_basins",
        "basin_entropy",
        "effective_basins",
        "compression_ratio"
    ]
].copy()

heatmap_df = heatmap_df.set_index(
    "system"
)

plt.figure(figsize=(10, 6))

sns.heatmap(
    heatmap_df,
    annot=True,
    fmt=".2f",
    cmap="viridis"
)

plt.title(
    "EXP_37F Atlas Scaling Metrics"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37f_scaling_heatmap.png",
    dpi=300
)

plt.close()


# ============================================================
# Optional Scaling Exponent
# ============================================================

alpha = np.nan

if len(df) >= 2:

    x = np.log10(
        df["buses"].values
    )

    y = np.log10(
        df["effective_basins"].values
    )

    slope, intercept = np.polyfit(
        x,
        y,
        1
    )

    alpha = slope


# ============================================================
# Report
# ============================================================

report = []

report.append(
    "EXP_37F ATLAS SCALING ANALYSIS"
)

report.append("=" * 50)
report.append("")

report.append(
    f"Systems analyzed: {len(df)}"
)

report.append("")

if not np.isnan(alpha):

    report.append(
        f"Estimated Scaling Exponent α = {alpha:.4f}"
    )

    report.append("")

for _, row in df.iterrows():

    report.append(

        f"{row['system']}: "
        f"buses={row['buses']}, "
        f"basins={row['n_basins']}, "
        f"entropy={row['basin_entropy']:.3f}, "
        f"effective={row['effective_basins']:.3f}, "
        f"compression={row['compression_ratio']:.3f}"
    )

report_file = (
    OUTPUT_DIR
    / "exp37f_report.txt"
)

with open(report_file, "w") as f:

    f.write(
        "\n".join(report)
    )

print(
    "Saved:",
    report_file
)

print()
print("EXP_37F complete.")
