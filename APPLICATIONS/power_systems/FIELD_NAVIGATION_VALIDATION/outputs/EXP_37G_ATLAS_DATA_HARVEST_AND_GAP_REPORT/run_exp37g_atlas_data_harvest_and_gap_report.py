# ============================================================
# EXP_37G_ATLAS_DATA_HARVEST_AND_GAP_REPORT
#
# Phase E — Atlas Universality
#
# Goal:
# Inventory all available IEEE atlas datasets and
# identify missing components required for universality.
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

OUTPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_37G_ATLAS_DATA_HARVEST_AND_GAP_REPORT"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Output ->", OUTPUT_DIR)

# ============================================================
# Candidate Systems
# ============================================================

SYSTEMS = {
    "IEEE9": {
        "states":
            ROOT.parent
            / "nexah_ieee9"
            / "results"
            / "states.txt"
    },

    "IEEE14": {
        "states":
            ROOT.parent
            / "nexah_ieee14"
            / "results"
            / "states.txt"
    },

    "IEEE30": {
        "states":
            ROOT.parent
            / "nexah_ieee30"
            / "results"
            / "states.txt"
    },

    "IEEE39": {
        "states":
            ROOT.parent
            / "nexah_ieee39"
            / "results"
            / "states.txt"
    },

    "IEEE57": {
        "states":
            ROOT.parent
            / "nexah_ieee57"
            / "results"
            / "states.txt"
    },

    "IEEE118": {
        "states":
            ROOT.parent
            / "nexah_ieee118"
            / "results"
            / "states.txt"
    },

    "IEEE300": {
        "states":
            ROOT.parent
            / "nexah_ieeeX"
            / "results"
            / "run_ieee300_20260413_015843"
            / "states.txt"
    },

    "IEEE1354": {
        "states":
            ROOT.parent
            / "nexah_ieee1354"
            / "results"
            / "states.txt"
    },

    "PEGASE9241": {
        "states":
            ROOT.parent
            / "nexah_pegase9241"
            / "results"
            / "states.txt"
    }
}

# ============================================================
# Existing Atlas Outputs
# ============================================================

ATLAS_V2 = (
    ROOT
    / "outputs"
    / "EXP_37B_MULTI_SYSTEM_ATLAS_DISCOVERY_V2"
)

BASIN_V4 = (
    ROOT
    / "outputs"
    / "EXP_37B_MULTI_SYSTEM_BASIN_EXTRACTION"
)

# ============================================================
# Inventory
# ============================================================

rows = []

for system, paths in SYSTEMS.items():

    print()
    print("=" * 50)
    print(system)
    print("=" * 50)

    has_states = paths["states"].exists()

    atlas_file = (
        ATLAS_V2
        / f"{system.lower()}_atlas.csv"
    )

    basin_file = (
        BASIN_V4
        / f"{system.lower()}_basins.csv"
    )

    has_atlas = atlas_file.exists()
    has_basins = basin_file.exists()

    score = (
        int(has_states)
        + int(has_atlas)
        + int(has_basins)
    )

    if score == 3:
        status = "COMPLETE"

    elif score > 0:
        status = "PARTIAL"

    else:
        status = "MISSING"

    print("states :", has_states)
    print("atlas  :", has_atlas)
    print("basins :", has_basins)
    print("status :", status)

    rows.append({
        "system": system,
        "states": int(has_states),
        "atlas": int(has_atlas),
        "basins": int(has_basins),
        "completion_score": score,
        "status": status
    })

inventory = pd.DataFrame(rows)

# ============================================================
# Save Inventory
# ============================================================

inventory_csv = (
    OUTPUT_DIR
    / "exp37g_system_inventory.csv"
)

inventory.to_csv(
    inventory_csv,
    index=False
)

print()
print("Saved:", inventory_csv)

# ============================================================
# Gap Matrix
# ============================================================

gap_df = inventory.copy()

gap_df["missing_states"] = (
    1 - gap_df["states"]
)

gap_df["missing_atlas"] = (
    1 - gap_df["atlas"]
)

gap_df["missing_basins"] = (
    1 - gap_df["basins"]
)

gap_csv = (
    OUTPUT_DIR
    / "exp37g_gap_matrix.csv"
)

gap_df.to_csv(
    gap_csv,
    index=False
)

print("Saved:", gap_csv)

# ============================================================
# Visual 1
# Completeness Heatmap
# ============================================================

heatmap = inventory.set_index(
    "system"
)[
    ["states", "atlas", "basins"]
]

plt.figure(figsize=(8,6))

plt.imshow(
    heatmap.values,
    aspect="auto"
)

plt.yticks(
    np.arange(len(heatmap.index)),
    heatmap.index
)

plt.xticks(
    np.arange(3),
    heatmap.columns
)

plt.colorbar()

plt.title(
    "EXP_37G System Completeness"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37g_system_completeness.png",
    dpi=300
)

plt.close()

# ============================================================
# Visual 2
# Completion Score
# ============================================================

plt.figure(figsize=(8,5))

plt.bar(
    inventory["system"],
    inventory["completion_score"]
)

plt.ylabel("Score")

plt.title(
    "EXP_37G Completion Score"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37g_completion_score.png",
    dpi=300
)

plt.close()

# ============================================================
# Visual 3
# Missing Components
# ============================================================

missing_total = pd.DataFrame({
    "states":
        [gap_df["missing_states"].sum()],
    "atlas":
        [gap_df["missing_atlas"].sum()],
    "basins":
        [gap_df["missing_basins"].sum()]
})

plt.figure(figsize=(6,5))

plt.bar(
    missing_total.columns,
    missing_total.iloc[0]
)

plt.title(
    "EXP_37G Remaining Data Gaps"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37g_remaining_gaps.png",
    dpi=300
)

plt.close()

# ============================================================
# Report
# ============================================================

report = []

report.append(
    "EXP_37G ATLAS DATA HARVEST AND GAP REPORT"
)

report.append("=" * 50)
report.append("")

report.append(
    f"Systems discovered: {len(inventory)}"
)

report.append("")

complete = inventory[
    inventory["status"] == "COMPLETE"
]

partial = inventory[
    inventory["status"] == "PARTIAL"
]

missing = inventory[
    inventory["status"] == "MISSING"
]

report.append("COMPLETE:")
for x in complete["system"]:
    report.append(f"- {x}")

report.append("")
report.append("PARTIAL:")
for x in partial["system"]:
    report.append(f"- {x}")

report.append("")
report.append("MISSING:")
for x in missing["system"]:
    report.append(f"- {x}")

report.append("")
report.append("Recommended Targets:")

for x in missing["system"]:
    report.append(f"- {x}")

report_file = (
    OUTPUT_DIR
    / "exp37g_report.txt"
)

with open(report_file, "w") as f:
    f.write("\n".join(report))

print()
print("Saved:", report_file)

print()
print("EXP_37G complete.")
