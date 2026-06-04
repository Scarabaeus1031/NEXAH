# ============================================================
# EXP_39B_TRANSITION_DATA_AUDIT
#
# Goal:
# Determine whether real transition / trajectory data
# exists anywhere inside the repository.
#
# EXP_39 revealed that current basin files contain
# basin inventories but not necessarily temporal dynamics.
#
# This audit searches for:
#
# - state sequences
# - controller replays
# - trajectories
# - actions
# - transition logs
# - histories
#
# Thomas Hofmann / NEXAH
# ============================================================

from pathlib import Path
import pandas as pd

# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parents[4]

OUTPUT_DIR = (
    ROOT
    / "APPLICATIONS"
    / "power_systems"
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_39B_TRANSITION_DATA_AUDIT"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Repository ->", ROOT)
print("Output     ->", OUTPUT_DIR)

# ============================================================
# Search Definitions
# ============================================================

KEYWORDS = [

    "state",
    "states",
    "trajectory",
    "trajectories",
    "transition",
    "transitions",
    "history",
    "sequence",
    "timeline",
    "controller",
    "replay",
    "action",
    "actions",
]

FILE_PATTERNS = [

    "*.txt",
    "*.csv",
    "*.json",
    "*.pkl",
    "*.npy",
]

# ============================================================
# Harvest
# ============================================================

rows = []

for pattern in FILE_PATTERNS:

    for file in ROOT.rglob(pattern):

        name = file.name.lower()

        matched = []

        for key in KEYWORDS:

            if key in name:
                matched.append(key)

        if matched:

            rows.append({

                "file":
                    str(file),

                "name":
                    file.name,

                "suffix":
                    file.suffix,

                "keywords":
                    ",".join(matched),

                "size_kb":
                    round(
                        file.stat().st_size / 1024,
                        2
                    )
            })

audit_df = pd.DataFrame(rows)

# ============================================================
# Save inventory
# ============================================================

inventory_file = (
    OUTPUT_DIR
    / "exp39b_transition_inventory.csv"
)

audit_df.to_csv(
    inventory_file,
    index=False
)

print(
    f"Assets discovered: {len(audit_df)}"
)

print("Saved:", inventory_file)

# ============================================================
# Candidate ranking
# ============================================================

if len(audit_df):

    audit_df["score"] = (

        audit_df["keywords"]
        .str.count(",")
        + 1

    )

    candidates = (
        audit_df
        .sort_values(
            "score",
            ascending=False
        )
        .head(100)
    )

else:

    candidates = pd.DataFrame()

candidate_file = (
    OUTPUT_DIR
    / "exp39b_top_candidates.csv"
)

candidates.to_csv(
    candidate_file,
    index=False
)

print("Saved:", candidate_file)

# ============================================================
# Category counts
# ============================================================

summary = []

for key in KEYWORDS:

    count = audit_df["keywords"].str.contains(
        key,
        na=False
    ).sum()

    summary.append({

        "keyword":
            key,

        "count":
            count
    })

summary_df = pd.DataFrame(summary)

summary_file = (
    OUTPUT_DIR
    / "exp39b_keyword_summary.csv"
)

summary_df.to_csv(
    summary_file,
    index=False
)

print("Saved:", summary_file)

# ============================================================
# Report
# ============================================================

report = []

report.append(
    "EXP_39B TRANSITION DATA AUDIT"
)

report.append("=" * 50)
report.append("")

report.append(
    f"Assets Found: {len(audit_df)}"
)

report.append("")

report.append(
    "Keyword Counts"
)

report.append(
    "--------------"
)

for _, row in summary_df.iterrows():

    report.append(
        f"{row['keyword']}: "
        f"{row['count']}"
    )

report.append("")
report.append(
    "Top Candidate Files"
)
report.append(
    "-------------------"
)

for _, row in candidates.head(20).iterrows():

    report.append(
        row["file"]
    )

report_path = (
    OUTPUT_DIR
    / "exp39b_report.txt"
)

with open(
    report_path,
    "w"
) as f:

    f.write(
        "\n".join(report)
    )

print("Saved:", report_path)

print("\nEXP_39B complete.")
