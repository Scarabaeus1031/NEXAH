# ============================================================
# EXP_37B_MULTI_SYSTEM_ATLAS_DISCOVERY_V2
#
# Goal:
# Build first multi-system atlas candidates from
# available IEEE run outputs.
#
# Input:
# nexah_ieee9/results/
# nexah_ieeeX/results/
#
# Output:
# EXP_37B_MULTI_SYSTEM_ATLAS_DISCOVERY_V2
#
# Thomas Hofmann / NEXAH
# ============================================================

from pathlib import Path

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

IEEE9_DIR = (
    ROOT.parent
    / "nexah_ieee9"
    / "results"
)

IEEEX_DIR = (
    ROOT.parent
    / "nexah_ieeeX"
    / "results"
)

OUTPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_37B_MULTI_SYSTEM_ATLAS_DISCOVERY_V2"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Output ->", OUTPUT_DIR)


# ============================================================
# Discover state files
# ============================================================

systems = {}

# ------------------------------------------------------------
# IEEE9
# ------------------------------------------------------------

ieee9_files = list(
    IEEE9_DIR.rglob("states.txt")
)

if ieee9_files:
    systems["IEEE9"] = ieee9_files

# ------------------------------------------------------------
# IEEE X
# ------------------------------------------------------------

for system in [
    "ieee118",
    "ieee300",
    "ieee1354",
    "ieee9241"
]:

    files = list(
        IEEEX_DIR.glob(
            f"run_{system}_*/states.txt"
        )
    )

    if files:
        systems[system.upper()] = files


# ============================================================
# Build Atlas Tables
# ============================================================

summary = []

for system, files in systems.items():

    print("\n===================================")
    print(system)
    print("===================================")

    labels = []

    for file in files:

        try:

            with open(file, "r") as f:

                lines = [
                    x.strip()
                    for x in f.readlines()
                    if x.strip()
                ]

            labels.extend(lines)

        except Exception:
            pass

    if len(labels) == 0:
        continue

    atlas = pd.DataFrame({
        "system": system,
        "state": labels
    })

    atlas["state_id"] = np.arange(
        len(atlas)
    )

    atlas["state_frequency"] = (
        atlas.groupby("state")["state"]
        .transform("count")
    )

    atlas_path = (
        OUTPUT_DIR
        / f"{system.lower()}_atlas.csv"
    )

    atlas.to_csv(
        atlas_path,
        index=False
    )

    print(
        "Saved:",
        atlas_path.name
    )

    summary.append({
        "system": system,
        "n_states": len(atlas),
        "n_unique_states":
            atlas["state"].nunique()
    })


# ============================================================
# Summary Table
# ============================================================

summary_df = pd.DataFrame(summary)

summary_csv = (
    OUTPUT_DIR
    / "exp37b_v2_system_summary.csv"
)

summary_df.to_csv(
    summary_csv,
    index=False
)

print("\nSaved:", summary_csv)


# ============================================================
# Visual 1
# State Counts
# ============================================================

if len(summary_df):

    plt.figure(figsize=(8,5))

    plt.bar(
        summary_df["system"],
        summary_df["n_states"]
    )

    plt.title(
        "EXP_37B V2 State Count"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / "exp37b_v2_state_distribution.png",
        dpi=300
    )

    plt.close()


# ============================================================
# Visual 2
# Unique States
# ============================================================

if len(summary_df):

    plt.figure(figsize=(8,5))

    plt.bar(
        summary_df["system"],
        summary_df["n_unique_states"]
    )

    plt.title(
        "EXP_37B V2 Unique States"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / "exp37b_v2_system_comparison.png",
        dpi=300
    )

    plt.close()


# ============================================================
# Visual 3
# Coverage
# ============================================================

if len(summary_df):

    coverage = (
        summary_df["n_unique_states"]
        /
        summary_df["n_states"]
    )

    plt.figure(figsize=(8,5))

    plt.bar(
        summary_df["system"],
        coverage
    )

    plt.title(
        "EXP_37B V2 Atlas Coverage"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / "exp37b_v2_atlas_coverage.png",
        dpi=300
    )

    plt.close()


# ============================================================
# Report
# ============================================================

report = []

report.append(
    "EXP_37B MULTI SYSTEM ATLAS DISCOVERY V2"
)

report.append(
    "======================================"
)

report.append("")

report.append(
    f"Systems analyzed: {len(summary_df)}"
)

report.append("")

for _, row in summary_df.iterrows():

    report.append(
        f"{row.system}: "
        f"{row.n_states} states, "
        f"{row.n_unique_states} classes"
    )

report_path = (
    OUTPUT_DIR
    / "exp37b_v2_report.txt"
)

with open(
    report_path,
    "w"
) as f:

    f.write(
        "\n".join(report)
    )

print("\nSaved:", report_path)

print("\nEXP_37B V2 complete.")
