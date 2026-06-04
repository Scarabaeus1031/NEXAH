# ============================================================
# EXP_38_IEEE39_ATLAS_RECONSTRUCTION
#
# Goal:
# Discover and reconstruct all available IEEE39 atlas assets.
#
# Phase E -> Atlas Expansion
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
    / "EXP_38_IEEE39_ATLAS_RECONSTRUCTION"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Output ->", OUTPUT_DIR)

# ============================================================
# Search Space
# ============================================================

SEARCH_ROOT = ROOT.parent.parent

print("Scanning:", SEARCH_ROOT)

# ============================================================
# Keywords
# ============================================================

KEYWORDS = [
    "ieee39",
    "IEEE39",
    "exp24e",
    "basin",
    "atlas",
    "transition",
    "field",
    "geometry",
    "pca",
]

# ============================================================
# Harvest
# ============================================================

records = []

for path in SEARCH_ROOT.rglob("*"):

    if not path.is_file():
        continue

    name = path.name.lower()

    if any(k.lower() in str(path).lower()
           for k in KEYWORDS):

        records.append({
            "file": path.name,
            "path": str(path),
            "suffix": path.suffix,
            "size_kb":
                round(
                    path.stat().st_size / 1024,
                    2
                )
        })

# ============================================================
# Table
# ============================================================

df = pd.DataFrame(records)

harvest_csv = (
    OUTPUT_DIR
    / "exp38_ieee39_asset_inventory.csv"
)

df.to_csv(
    harvest_csv,
    index=False
)

print(
    f"Assets found: {len(df)}"
)

print("Saved:", harvest_csv)

# ============================================================
# Categorization
# ============================================================

categories = {
    "atlas": 0,
    "basin": 0,
    "transition": 0,
    "field": 0,
    "geometry": 0,
    "pca": 0,
}

for p in df["path"] if len(df) else []:

    low = p.lower()

    for c in categories:

        if c in low:
            categories[c] += 1

cat_df = pd.DataFrame({
    "category": categories.keys(),
    "count": categories.values()
})

cat_csv = (
    OUTPUT_DIR
    / "exp38_ieee39_category_summary.csv"
)

cat_df.to_csv(
    cat_csv,
    index=False
)

# ============================================================
# Gap Analysis
# ============================================================

required = [
    "states",
    "atlas",
    "basins",
    "transition",
    "pca"
]

gap_rows = []

all_text = " ".join(
    df["path"].astype(str)
) if len(df) else ""

for item in required:

    gap_rows.append({
        "component": item,
        "present":
            item.lower()
            in all_text.lower()
    })

gap_df = pd.DataFrame(gap_rows)

gap_csv = (
    OUTPUT_DIR
    / "exp38_ieee39_gap_report.csv"
)

gap_df.to_csv(
    gap_csv,
    index=False
)

# ============================================================
# Report
# ============================================================

report = []

report.append(
    "EXP_38 IEEE39 ATLAS RECONSTRUCTION"
)

report.append("=" * 50)
report.append("")

report.append(
    f"Assets discovered: {len(df)}"
)

report.append("")

report.append(
    "Category Summary"
)

report.append("----------------")
report.append("")

for _, row in cat_df.iterrows():

    report.append(
        f"{row['category']}: "
        f"{row['count']}"
    )

report.append("")
report.append("Gap Analysis")
report.append("------------")
report.append("")

for _, row in gap_df.iterrows():

    report.append(
        f"{row['component']}: "
        f"{'FOUND' if row['present'] else 'MISSING'}"
    )

report_path = (
    OUTPUT_DIR
    / "exp38_report.txt"
)

with open(report_path, "w") as f:

    f.write(
        "\n".join(report)
    )

print("Saved:", cat_csv)
print("Saved:", gap_csv)
print("Saved:", report_path)

print()
print("EXP_38 complete.")
