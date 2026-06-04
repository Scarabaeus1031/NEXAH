"""
==================================================
EXP_44C.1 — READY DATASET INSPECTION
==================================================

Python File:
run_exp44c1_ready_dataset_inspection.py

Objective
--------------------------------------------------
Inspect all READY datasets discovered in EXP_44C
and determine whether they represent:

- TRUE_TRAJECTORY
- STATE_MATRIX
- EVENT_LOG
- SUMMARY_TABLE
- UNKNOWN

This experiment serves as the final validation
step before EXP_44D TRUE ATLAS-KOOPMAN
CROSS VALIDATION.

==================================================
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PATHS
# --------------------------------------------------

ROOT = Path(__file__).resolve()

while ROOT.name != "NEXAH":
    ROOT = ROOT.parent

POWER_ROOT = ROOT / "APPLICATIONS" / "power_systems"

INPUT_DIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44C_ATLAS_TRAJECTORY_RECONSTRUCTION"
)

OUTPUT_DIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44C1_READY_DATASET_INSPECTION"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

READY_FILE = (
    INPUT_DIR /
    "exp44c_koopman_ready_datasets.csv"
)

print(f"Input  -> {READY_FILE}")
print(f"Output -> {OUTPUT_DIR}")

# --------------------------------------------------
# LOAD READY DATASETS
# --------------------------------------------------

if not READY_FILE.exists():
    raise FileNotFoundError(
        "exp44c_koopman_ready_datasets.csv not found."
    )

ready_df = pd.read_csv(READY_FILE)

if ready_df.empty:
    raise RuntimeError(
        "No READY datasets found."
    )

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

TIME_COLUMNS = [
    "time",
    "t",
    "step",
    "steps",
    "timestamp",
    "iteration",
    "frame",
    "sample"
]

def classify_dataset(df):

    cols = [c.lower() for c in df.columns]

    has_time = any(
        t in cols
        for t in TIME_COLUMNS
    )

    numeric_cols = (
        df.select_dtypes(include=np.number)
        .shape[1]
    )

    rows, columns = df.shape

    if has_time and rows > 100:
        return "TRUE_TRAJECTORY"

    if numeric_cols >= 2 and rows > 100:
        return "STATE_MATRIX"

    if rows < 100 and columns < 10:
        return "SUMMARY_TABLE"

    return "UNKNOWN"

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

inventory_records = []
column_records = []

report_lines = []

report_lines.append(
    "EXP_44C.1 READY DATASET INSPECTION\n"
)
report_lines.append("=" * 60 + "\n")

for idx, row in ready_df.iterrows():

    path = Path(row["path"])

    report_lines.append(
        f"\n{'='*80}\n"
    )

    report_lines.append(
        f"DATASET {idx+1}\n"
    )

    report_lines.append(
        f"PATH:\n{path}\n"
    )

    if not path.exists():

        report_lines.append(
            "FILE NOT FOUND\n"
        )

        continue

    try:

        df = pd.read_csv(path)

        rows, cols = df.shape

        numeric_cols = (
            df.select_dtypes(include=np.number)
            .shape[1]
        )

        missing = int(
            df.isna().sum().sum()
        )

        size_mb = (
            path.stat().st_size
            / 1024
            / 1024
        )

        dataset_class = classify_dataset(df)

        lower_cols = [
            str(c).lower()
            for c in df.columns
        ]

        has_time_axis = any(
            c in lower_cols
            for c in TIME_COLUMNS
        )

        inventory_records.append({

            "path": str(path),

            "rows": rows,

            "columns": cols,

            "numeric_columns": numeric_cols,

            "missing_values": missing,

            "size_mb": round(size_mb, 4),

            "has_time_axis": has_time_axis,

            "classification": dataset_class

        })

        # --------------------------
        # REPORT
        # --------------------------

        report_lines.append(
            f"Rows              : {rows}\n"
        )

        report_lines.append(
            f"Columns           : {cols}\n"
        )

        report_lines.append(
            f"Numeric Columns   : {numeric_cols}\n"
        )

        report_lines.append(
            f"Missing Values    : {missing}\n"
        )

        report_lines.append(
            f"Size MB           : {size_mb:.4f}\n"
        )

        report_lines.append(
            f"Time Axis         : {has_time_axis}\n"
        )

        report_lines.append(
            f"Classification    : {dataset_class}\n"
        )

        report_lines.append(
            "\nCOLUMN NAMES\n"
        )

        for col in df.columns:

            report_lines.append(
                f" - {col}\n"
            )

            column_records.append({

                "dataset": path.name,
                "column": col

            })

        report_lines.append(
            "\nFIRST 5 ROWS\n"
        )

        report_lines.append(
            df.head().to_string()
        )

        report_lines.append("\n")

        report_lines.append(
            "\nLAST 5 ROWS\n"
        )

        report_lines.append(
            df.tail().to_string()
        )

        report_lines.append("\n")

    except Exception as e:

        report_lines.append(
            f"ERROR: {e}\n"
        )

# --------------------------------------------------
# EXPORT TABLES
# --------------------------------------------------

inventory_df = pd.DataFrame(
    inventory_records
)

columns_df = pd.DataFrame(
    column_records
)

inventory_df.to_csv(
    OUTPUT_DIR /
    "exp44c1_ready_dataset_inventory.csv",
    index=False
)

columns_df.to_csv(
    OUTPUT_DIR /
    "exp44c1_dataset_columns.csv",
    index=False
)

# --------------------------------------------------
# VISUAL 1
# DATASET SIZE
# --------------------------------------------------

if not inventory_df.empty:

    plt.figure(figsize=(8,5))

    plt.bar(
        range(len(inventory_df)),
        inventory_df["rows"]
    )

    plt.xticks(
        range(len(inventory_df)),
        [f"D{i+1}" for i in range(len(inventory_df))]
    )

    plt.ylabel("Rows")

    plt.title(
        "EXP_44C1 Ready Dataset Sizes"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR /
        "exp44c1_ready_dataset_sizes.png",
        dpi=300
    )

    plt.close()

# --------------------------------------------------
# VISUAL 2
# DIMENSIONS
# --------------------------------------------------

if not inventory_df.empty:

    plt.figure(figsize=(8,5))

    plt.bar(
        range(len(inventory_df)),
        inventory_df["columns"]
    )

    plt.xticks(
        range(len(inventory_df)),
        [f"D{i+1}" for i in range(len(inventory_df))]
    )

    plt.ylabel("Columns")

    plt.title(
        "EXP_44C1 Ready Dataset Dimensions"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR /
        "exp44c1_ready_dataset_dimensions.png",
        dpi=300
    )

    plt.close()

# --------------------------------------------------
# REPORT
# --------------------------------------------------

with open(
    OUTPUT_DIR /
    "exp44c1_ready_dataset_report.txt",
    "w"
) as f:

    f.writelines(report_lines)

# --------------------------------------------------
# FINAL SUMMARY
# --------------------------------------------------

print()
print("EXP_44C.1 COMPLETE")
print()

if not inventory_df.empty:

    print(
        inventory_df[
            [
                "rows",
                "columns",
                "classification"
            ]
        ]
    )

print()
print(
    f"Datasets inspected: {len(inventory_df)}"
)
print()
print(
    "Next candidate: EXP_44D TRUE ATLAS-KOOPMAN CROSS VALIDATION"
)
