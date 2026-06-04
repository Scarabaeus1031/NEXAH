# ============================================================
# EXP_37_ATLAS_UNIVERSALITY_TEST
#
# Phase E — Universality & Scaling
#
# Goal:
# Determine whether atlas structures
# persist across IEEE benchmark systems.
#
# Questions:
# - Do basins persist?
# - Do gates persist?
# - Do corridors persist?
# - Does a backbone emerge?
# - Does recovery structure emerge?
#
# Input:
# Multi-system IEEE atlas outputs
#
# Output:
# EXP_37_ATLAS_UNIVERSALITY_TEST
#
# Thomas Hofmann / NEXAH
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_37_ATLAS_UNIVERSALITY_TEST"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Output ->", OUTPUT_DIR)


# ============================================================
# Systems
# ============================================================

SYSTEMS = [
    ("IEEE9", 9),
    ("IEEE14", 14),
    ("IEEE30", 30),
    ("IEEE39", 39),
    ("IEEE57", 57),
    ("IEEE118", 118),
    ("IEEE300", 300),
    ("IEEE1354", 1354),
    ("PEGASE9241", 9241),
]


# ============================================================
# Atlas Structure Detection
# ============================================================

def detect_structure(system_name):

    result = {
        "system": system_name,
        "basins": 0,
        "gates": 0,
        "corridors": 0,
        "backbone": 0,
        "recovery": 0,
    }

    # --------------------------------------------------------
    # Current implementation:
    #
    # IEEE39 already validated through
    # EXP_06 - EXP_36.
    #
    # Additional systems can later be connected
    # to their own atlas outputs.
    # --------------------------------------------------------

    if system_name == "IEEE39":

        result["basins"] = 1
        result["gates"] = 1
        result["corridors"] = 1
        result["backbone"] = 1
        result["recovery"] = 1

    result["score"] = (
        result["basins"]
        + result["gates"]
        + result["corridors"]
        + result["backbone"]
        + result["recovery"]
    )

    return result


# ============================================================
# Evaluate Systems
# ============================================================

rows = []

for system_name, bus_count in SYSTEMS:

    row = detect_structure(system_name)

    row["bus_count"] = bus_count

    rows.append(row)

df = pd.DataFrame(rows)

print("\nResults")
print(df)


# ============================================================
# Save CSV
# ============================================================

csv_path = (
    OUTPUT_DIR
    / "exp37_universality_table.csv"
)

df.to_csv(
    csv_path,
    index=False
)

print("\nSaved:", csv_path.name)


# ============================================================
# Visual 1
# Universality Matrix
# ============================================================

matrix_cols = [
    "basins",
    "gates",
    "corridors",
    "backbone",
    "recovery",
]

matrix = df[matrix_cols].values

plt.figure(figsize=(10, 6))

plt.imshow(
    matrix,
    aspect="auto"
)

plt.colorbar(
    label="Presence"
)

plt.xticks(
    range(len(matrix_cols)),
    matrix_cols
)

plt.yticks(
    range(len(df)),
    df["system"]
)

plt.title(
    "EXP_37 Atlas Universality Matrix"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37_universality_matrix.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Universality Score
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    df["system"],
    df["score"]
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
# Visual 3
# Structure Frequency
# ============================================================

freq = []

for col in matrix_cols:

    freq.append(
        100
        * df[col].sum()
        / len(df)
    )

plt.figure(figsize=(8, 5))

plt.bar(
    matrix_cols,
    freq
)

plt.ylabel(
    "Presence (%)"
)

plt.ylim(0, 100)

plt.title(
    "EXP_37 Structure Frequency"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37_structure_frequency.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 4
# Size vs Score
# ============================================================

plt.figure(figsize=(8, 6))

plt.plot(
    df["bus_count"],
    df["score"],
    marker="o"
)

plt.xscale("log")

plt.xlabel(
    "Bus Count"
)

plt.ylabel(
    "Universality Score"
)

plt.title(
    "EXP_37 Atlas Persistence vs Size"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37_size_vs_score.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 5
# Summary Dashboard
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 5)
)

ax.axis("off")

summary = [
    f"Systems analyzed: {len(df)}",
    "",
    f"Mean Score: {df['score'].mean():.2f}",
    f"Max Score: {df['score'].max()}",
    "",
    f"Basins: {df['basins'].sum()}",
    f"Gates: {df['gates'].sum()}",
    f"Corridors: {df['corridors'].sum()}",
    f"Backbone: {df['backbone'].sum()}",
    f"Recovery: {df['recovery'].sum()}",
]

ax.text(
    0.05,
    0.95,
    "\n".join(summary),
    va="top",
    fontsize=12
)

plt.title(
    "EXP_37 Summary Dashboard"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37_summary_dashboard.png",
    dpi=300
)

plt.close()


# ============================================================
# TXT Report
# ============================================================

report_path = (
    OUTPUT_DIR
    / "exp37_report.txt"
)

with open(
    report_path,
    "w"
) as f:

    f.write(
        "EXP_37 ATLAS UNIVERSALITY TEST\n"
    )

    f.write(
        "=============================\n\n"
    )

    f.write(
        f"Systems analyzed: {len(df)}\n\n"
    )

    f.write(
        "Structures evaluated:\n"
    )

    for s in matrix_cols:

        f.write(
            f"- {s}\n"
        )

    f.write("\n")

    for s in matrix_cols:

        f.write(
            f"{s}: "
            f"{int(df[s].sum())}/"
            f"{len(df)} systems\n"
        )

    f.write("\n")

    f.write(
        f"Mean Universality Score: "
        f"{df['score'].mean():.2f}/5\n\n"
    )

    f.write(
        "Current Status:\n"
    )

    f.write(
        "IEEE39 populated.\n"
    )

    f.write(
        "Remaining systems pending atlas extraction.\n"
    )

print(
    "\nSaved:",
    report_path.name
)

print("\nEXP_37 complete.")
