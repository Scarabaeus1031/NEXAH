"""
NEXAH Visual Database Builder
=============================

Scans all demo visual/data folders and builds a unified
visual pattern database.

Outputs:

demos/database/

    visual_catalog.csv
    atlas_index.json
    database_summary.txt
"""

from pathlib import Path
import pandas as pd
import json
import re

# --------------------------------------------------
# paths
# --------------------------------------------------

base_dir = Path(__file__).resolve().parent

visual_root = base_dir / "visuals"
data_root = base_dir / "data"

database_dir = base_dir / "database"
database_dir.mkdir(parents=True, exist_ok=True)

print("Scanning visual directories:", visual_root)
print("Scanning data directories:", data_root)
print("Database output:", database_dir)

# --------------------------------------------------
# pattern filename parser
# --------------------------------------------------

pattern = re.compile(r"sym_n(\d+)_drift_([0-9.]+)\.png")

records = []

# --------------------------------------------------
# scan visual folders
# --------------------------------------------------

for atlas_folder in visual_root.glob("*"):

    if not atlas_folder.is_dir():
        continue

    atlas_name = atlas_folder.name

    for img_file in atlas_folder.glob("*.png"):

        match = pattern.search(img_file.name)

        n = None
        drift = None

        if match:
            n = int(match.group(1))
            drift = float(match.group(2))

        records.append({
            "atlas": atlas_name,
            "file": img_file.name,
            "path": str(img_file),
            "symmetry_n": n,
            "drift_deg": drift
        })

print("Total visuals found:", len(records))

# --------------------------------------------------
# create dataframe
# --------------------------------------------------

df = pd.DataFrame(records)

catalog_file = database_dir / "visual_catalog.csv"
df.to_csv(catalog_file, index=False)

print("Visual catalog saved:", catalog_file)

# --------------------------------------------------
# scan data folders
# --------------------------------------------------

atlas_index = {}

for data_folder in data_root.glob("*"):

    if not data_folder.is_dir():
        continue

    atlas_name = data_folder.name

    atlas_index[atlas_name] = {}

    csv_files = list(data_folder.glob("*.csv"))
    json_files = list(data_folder.glob("*.json"))

    atlas_index[atlas_name]["csv_files"] = [f.name for f in csv_files]
    atlas_index[atlas_name]["json_files"] = [f.name for f in json_files]

    # load metrics if available
    metrics_file = data_folder / "resonance_metrics.csv"

    if metrics_file.exists():

        df_metrics = pd.read_csv(metrics_file)

        atlas_index[atlas_name]["num_patterns"] = len(df_metrics)

        top = df_metrics.sort_values("score", ascending=False).head(5)

        atlas_index[atlas_name]["top_patterns"] = top[
            ["n", "drift", "score"]
        ].to_dict(orient="records")

print("Atlas index created.")

# --------------------------------------------------
# save atlas index
# --------------------------------------------------

index_file = database_dir / "atlas_index.json"

with open(index_file, "w") as f:
    json.dump(atlas_index, f, indent=2)

print("Atlas index saved:", index_file)

# --------------------------------------------------
# summary report
# --------------------------------------------------

summary_file = database_dir / "database_summary.txt"

with open(summary_file, "w") as f:

    f.write("NEXAH VISUAL DATABASE SUMMARY\n")
    f.write("=============================\n\n")

    f.write(f"Total visual patterns: {len(records)}\n\n")

    f.write("Atlas collections:\n")

    for atlas_name in atlas_index:

        f.write(f"\n- {atlas_name}\n")

        if "num_patterns" in atlas_index[atlas_name]:
            f.write(f"  patterns: {atlas_index[atlas_name]['num_patterns']}\n")

        if "top_patterns" in atlas_index[atlas_name]:

            f.write("  top resonances:\n")

            for p in atlas_index[atlas_name]["top_patterns"]:

                f.write(
                    f"    n={p['n']}  drift={p['drift']:.2f}  score={p['score']:.4f}\n"
                )

print("Summary report saved:", summary_file)

print("\nDatabase build complete.")
