# ============================================================
# EXP_38B_IEEE39_ASSET_MAPPING
#
# Goal:
# Identify reconstructable IEEE39 atlas assets.
#
# Thomas Hofmann / NEXAH
# ============================================================

from pathlib import Path
import pandas as pd

# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_38B_IEEE39_ASSET_MAPPING"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

SEARCH_ROOT = ROOT.parent.parent

print("Output ->", OUTPUT_DIR)
print("Scanning ->", SEARCH_ROOT)

# ============================================================
# Keywords
# ============================================================

ASSET_TYPES = {

    "states": [
        "states"
    ],

    "atlas": [
        "atlas"
    ],

    "basin": [
        "basin"
    ],

    "transition": [
        "transition"
    ],

    "pca": [
        "pca"
    ],

    "warning": [
        "warning"
    ],

    "recovery": [
        "recovery"
    ],

    "geometry": [
        "geometry"
    ],

    "field": [
        "field"
    ]
}

# ============================================================
# Harvest
# ============================================================

rows = []

for path in SEARCH_ROOT.rglob("*"):

    if not path.is_file():
        continue

    full = str(path).lower()

    if "39" not in full:
        continue

    for category, keys in ASSET_TYPES.items():

        if any(
            k in full
            for k in keys
        ):

            rows.append({

                "category":
                    category,

                "file":
                    path.name,

                "suffix":
                    path.suffix,

                "size_kb":
                    round(
                        path.stat().st_size / 1024,
                        2
                    ),

                "path":
                    str(path)
            })

            break

# ============================================================
# Table
# ============================================================

df = pd.DataFrame(rows)

asset_csv = (
    OUTPUT_DIR
    / "exp38b_asset_inventory.csv"
)

df.to_csv(
    asset_csv,
    index=False
)

print(
    f"Assets: {len(df)}"
)

# ============================================================
# Category Summary
# ============================================================

summary = (
    df.groupby("category")
      .size()
      .reset_index(name="count")
      .sort_values(
          "count",
          ascending=False
      )
)

summary_csv = (
    OUTPUT_DIR
    / "exp38b_category_summary.csv"
)

summary.to_csv(
    summary_csv,
    index=False
)

# ============================================================
# Reconstruction Readiness
# ============================================================

required = [
    "states",
    "atlas",
    "basin",
    "transition",
    "pca"
]

ready_rows = []

present_categories = set(
    df["category"]
) if len(df) else set()

for item in required:

    ready_rows.append({

        "component":
            item,

        "available":
            item in present_categories
    })

ready_df = pd.DataFrame(
    ready_rows
)

ready_csv = (
    OUTPUT_DIR
    / "exp38b_reconstruction_readiness.csv"
)

ready_df.to_csv(
    ready_csv,
    index=False
)

# ============================================================
# Candidate Files
# ============================================================

candidates = df.sort_values(
    "size_kb",
    ascending=False
)

candidate_csv = (
    OUTPUT_DIR
    / "exp38b_candidate_assets.csv"
)

candidates.to_csv(
    candidate_csv,
    index=False
)

# ============================================================
# Report
# ============================================================

report = []

report.append(
    "EXP_38B IEEE39 ASSET MAPPING"
)

report.append("=" * 50)
report.append("")

report.append(
    f"Assets Found: {len(df)}"
)

report.append("")
report.append(
    "Category Counts"
)
report.append("----------------")

for _, row in summary.iterrows():

    report.append(
        f"{row['category']}: "
        f"{row['count']}"
    )

report.append("")
report.append(
    "Reconstruction Readiness"
)
report.append("------------------------")

for _, row in ready_df.iterrows():

    report.append(
        f"{row['component']}: "
        f"{'YES' if row['available'] else 'NO'}"
    )

report_path = (
    OUTPUT_DIR
    / "exp38b_report.txt"
)

with open(report_path, "w") as f:

    f.write(
        "\n".join(report)
    )

print("Saved:", asset_csv)
print("Saved:", summary_csv)
print("Saved:", ready_csv)
print("Saved:", candidate_csv)
print("Saved:", report_path)

print()
print("EXP_38B complete.")
