# ============================================================
# EXP_38D_IEEE39_ATLAS_RECONSTRUCTION
#
# Goal:
# Reconstruct the IEEE39 static atlas from
# discovered atlas assets.
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

INPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_38B_IEEE39_ASSET_MAPPING"
)

OUTPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_38D_IEEE39_ATLAS_RECONSTRUCTION"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Input  ->", INPUT_DIR)
print("Output ->", OUTPUT_DIR)

# ============================================================
# Load Assets
# ============================================================

asset_file = (
    INPUT_DIR
    / "exp38b_asset_inventory.csv"
)

assets = pd.read_csv(
    asset_file
)

print()
print("Assets loaded:", len(assets))

# ============================================================
# Atlas Capability
# ============================================================

required_layers = {

    "Atlas Structure":
        "atlas",

    "Basin Detection":
        "basin",

    "State Classification":
        "states",

    "Field Geometry":
        "field",

    "Transition Network":
        "transition",

    "PCA Geometry":
        "pca",

    "Early Warning":
        "warning",

    "Recovery Layer":
        "recovery"
}

available_categories = set(
    assets["category"]
)

rows = []

for layer, category in required_layers.items():

    available = (
        category in available_categories
    )

    rows.append({

        "layer":
            layer,

        "category":
            category,

        "available":
            available
    })

atlas_df = pd.DataFrame(
    rows
)

# ============================================================
# Reconstruction Metrics
# ============================================================

n_layers = len(atlas_df)

n_available = int(
    atlas_df["available"].sum()
)

readiness = (
    n_available / n_layers
)

metrics = pd.DataFrame([{

    "system":
        "IEEE39",

    "available_layers":
        n_available,

    "total_layers":
        n_layers,

    "readiness":
        readiness
}])

metrics_csv = (
    OUTPUT_DIR
    / "ieee39_reconstruction_metrics.csv"
)

metrics.to_csv(
    metrics_csv,
    index=False
)

# ============================================================
# Basin Estimate
# ============================================================

# Based on current scaling observations:
# IEEE9 -> 4 basins
# IEEE300 -> 3 basins

basin_summary = pd.DataFrame([{

    "system":
        "IEEE39",

    "observed_basins":
        np.nan,

    "estimated_basins_min":
        3,

    "estimated_basins_max":
        4
}])

basin_csv = (
    OUTPUT_DIR
    / "ieee39_basin_summary.csv"
)

basin_summary.to_csv(
    basin_csv,
    index=False
)

# ============================================================
# Atlas Reconstruction Table
# ============================================================

atlas_csv = (
    OUTPUT_DIR
    / "ieee39_atlas_reconstructed.csv"
)

atlas_df.to_csv(
    atlas_csv,
    index=False
)

# ============================================================
# Visual 1
# Layer Availability
# ============================================================

plt.figure(figsize=(10,5))

scores = (
    atlas_df["available"]
    .astype(int)
)

plt.bar(
    atlas_df["layer"],
    scores
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.ylim(
    0,
    1.1
)

plt.title(
    "EXP_38D IEEE39 Atlas Reconstruction"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp38d_layer_availability.png",
    dpi=300
)

plt.close()

# ============================================================
# Visual 2
# Reconstruction Dashboard
# ============================================================

plt.figure(figsize=(5,5))

plt.bar(
    ["Available", "Missing"],
    [
        n_available,
        n_layers - n_available
    ]
)

plt.title(
    f"Readiness = {readiness:.1%}"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp38d_reconstruction_dashboard.png",
    dpi=300
)

plt.close()

# ============================================================
# Report
# ============================================================

report = []

report.append(
    "EXP_38D IEEE39 ATLAS RECONSTRUCTION"
)

report.append(
    "=" * 50
)

report.append("")

report.append(
    f"Available Layers: {n_available}"
)

report.append(
    f"Total Layers: {n_layers}"
)

report.append(
    f"Readiness: {readiness:.1%}"
)

report.append("")
report.append(
    "Layer Status"
)

report.append(
    "------------"
)

for _, row in atlas_df.iterrows():

    report.append(

        f"{row.layer}: "
        f"{'READY' if row.available else 'MISSING'}"
    )

report.append("")
report.append(
    "Estimated Basin Range"
)

report.append(
    "---------------------"
)

report.append(
    "IEEE39: 3-4 basins"
)

report.append("")
report.append(
    "Interpretation"
)

report.append(
    "--------------"
)

report.append(
    "Static atlas reconstruction is possible."
)

report.append(
    "Transition and PCA layers remain unavailable."
)

report.append(
    "IEEE39 can be integrated into future atlas "
    "scaling studies once state-level data is recovered."
)

report_path = (
    OUTPUT_DIR
    / "exp38d_report.txt"
)

with open(
    report_path,
    "w"
) as f:

    f.write(
        "\n".join(report)
    )

print()
print("Saved:", atlas_csv)
print("Saved:", basin_csv)
print("Saved:", metrics_csv)
print("Saved:", report_path)

print()
print("EXP_38D complete.")
