# ============================================================
# EXP_38C_IEEE39_ATLAS_CAPABILITY_AUDIT
#
# Goal:
# Determine which atlas layers can be reconstructed
# from currently available IEEE39 assets.
#
# Thomas Hofmann / NEXAH
# ============================================================

from pathlib import Path

import pandas as pd
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
    / "EXP_38C_IEEE39_ATLAS_CAPABILITY_AUDIT"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Input  ->", INPUT_DIR)
print("Output ->", OUTPUT_DIR)

# ============================================================
# Load Asset Inventory
# ============================================================

asset_file = (
    INPUT_DIR
    / "exp38b_asset_inventory.csv"
)

if not asset_file.exists():

    raise FileNotFoundError(
        f"Missing: {asset_file}"
    )

assets = pd.read_csv(asset_file)

# ============================================================
# Atlas Layers
# ============================================================

LAYERS = {

    "Atlas Structure": [
        "atlas"
    ],

    "Basin Detection": [
        "basin"
    ],

    "State Classification": [
        "states"
    ],

    "Transition Network": [
        "transition"
    ],

    "PCA Geometry": [
        "pca"
    ],

    "Field Geometry": [
        "field",
        "geometry"
    ],

    "Early Warning": [
        "warning"
    ],

    "Recovery Layer": [
        "recovery"
    ]
}

# ============================================================
# Capability Evaluation
# ============================================================

rows = []

available_categories = set(
    assets["category"].unique()
)

for layer, requirements in LAYERS.items():

    found = sum(
        r in available_categories
        for r in requirements
    )

    completeness = (
        found / len(requirements)
    )

    if completeness == 1.0:
        status = "READY"

    elif completeness >= 0.5:
        status = "PARTIAL"

    else:
        status = "MISSING"

    rows.append({

        "layer":
            layer,

        "requirements":
            ", ".join(requirements),

        "completeness":
            completeness,

        "status":
            status
    })

audit = pd.DataFrame(rows)

# ============================================================
# Save Audit Table
# ============================================================

audit_csv = (
    OUTPUT_DIR
    / "exp38c_capability_audit.csv"
)

audit.to_csv(
    audit_csv,
    index=False
)

print("Saved:", audit_csv)

# ============================================================
# Visual
# ============================================================

score_map = {

    "READY": 2,
    "PARTIAL": 1,
    "MISSING": 0
}

audit["score"] = (
    audit["status"]
    .map(score_map)
)

plt.figure(figsize=(10,6))

bars = plt.bar(
    audit["layer"],
    audit["score"]
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.yticks(
    [0,1,2],
    ["Missing", "Partial", "Ready"]
)

plt.title(
    "EXP_38C IEEE39 Atlas Capability Audit"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp38c_capability_audit.png",
    dpi=300
)

plt.close()

# ============================================================
# Summary Report
# ============================================================

report = []

report.append(
    "EXP_38C IEEE39 ATLAS CAPABILITY AUDIT"
)

report.append("=" * 50)
report.append("")

ready = (
    audit["status"] == "READY"
).sum()

partial = (
    audit["status"] == "PARTIAL"
).sum()

missing = (
    audit["status"] == "MISSING"
).sum()

report.append(
    f"Ready Layers: {ready}"
)

report.append(
    f"Partial Layers: {partial}"
)

report.append(
    f"Missing Layers: {missing}"
)

report.append("")
report.append(
    "Layer Status"
)

report.append(
    "------------"
)

for _, row in audit.iterrows():

    report.append(

        f"{row['layer']}: "
        f"{row['status']}"
    )

report.append("")
report.append(
    "Interpretation"
)

report.append(
    "--------------"
)

report.append(
    "READY   -> reconstruction possible"
)

report.append(
    "PARTIAL -> reconstruction possible with gaps"
)

report.append(
    "MISSING -> missing source assets"
)

report_path = (
    OUTPUT_DIR
    / "exp38c_report.txt"
)

with open(report_path, "w") as f:

    f.write(
        "\n".join(report)
    )

print("Saved:", report_path)

print()
print("EXP_38C complete.")
