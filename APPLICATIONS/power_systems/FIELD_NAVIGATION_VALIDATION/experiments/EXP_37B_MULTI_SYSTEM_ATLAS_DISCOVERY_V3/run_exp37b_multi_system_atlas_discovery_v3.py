# ============================================================
# EXP_37B_MULTI_SYSTEM_ATLAS_DISCOVERY_V3
#
# Phase E — Atlas Universality
#
# Aggregate atlas metrics from EXP_37B V2 outputs
#
# Thomas Hofmann / NEXAH
# ============================================================

from pathlib import Path
from collections import Counter

import numpy as np
import pandas as pd

# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

INPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_37B_MULTI_SYSTEM_ATLAS_DISCOVERY_V2"
)

OUTDIR = (
    ROOT
    / "outputs"
    / "EXP_37B_MULTI_SYSTEM_ATLAS_DISCOVERY_V3"
)

OUTDIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Input  ->", INPUT_DIR)
print("Output ->", OUTDIR)

# ============================================================
# Atlas Files From V2
# ============================================================

ATLAS_FILES = {
    "IEEE9":
        INPUT_DIR / "ieee9_atlas.csv",

    "IEEE300":
        INPUT_DIR / "ieee300_atlas.csv",
}

# ============================================================
# Entropy
# ============================================================

def entropy_from_counts(counts):

    counts = np.array(
        counts,
        dtype=float
    )

    p = counts / counts.sum()

    return float(
        -np.sum(
            p * np.log2(p)
        )
    )

# ============================================================
# Discovery
# ============================================================

summary_rows = []

for system, csv_file in ATLAS_FILES.items():

    print()
    print("=" * 50)
    print(system)
    print("=" * 50)

    if not csv_file.exists():

        print("Atlas file missing.")
        continue

    atlas = pd.read_csv(csv_file)

    if len(atlas) == 0:

        print("Atlas file empty.")
        continue

    counts = atlas["count"].values

    total_states = int(counts.sum())

    unique_states = len(atlas)

    dominant_fraction = (
        counts.max()
        / total_states
    )

    ent = entropy_from_counts(counts)

    effective_states = (
        2 ** ent
    )

    atlas_complexity = (
        unique_states * ent
    )

    print(f"Rows: {total_states}")
    print(f"Classes: {unique_states}")
    print(f"Entropy: {ent:.3f}")
    print(f"Effective States: {effective_states:.3f}")

    summary_rows.append({

        "system":
            system,

        "total_states":
            total_states,

        "unique_states":
            unique_states,

        "entropy":
            ent,

        "effective_states":
            effective_states,

        "dominant_fraction":
            dominant_fraction,

        "atlas_complexity":
            atlas_complexity
    })

# ============================================================
# Summary
# ============================================================

summary_df = pd.DataFrame(
    summary_rows
)

summary_file = (
    OUTDIR /
    "exp37b_v3_system_summary.csv"
)

summary_df.to_csv(
    summary_file,
    index=False
)

print()
print("Saved:", summary_file)

# ============================================================
# Report
# ============================================================

report = []

report.append(
    "EXP_37B MULTI-SYSTEM ATLAS DISCOVERY V3"
)

report.append("=" * 50)
report.append("")

for _, row in summary_df.iterrows():

    report.append(
        f"{row['system']}: "
        f"classes={row['unique_states']}, "
        f"entropy={row['entropy']:.3f}, "
        f"effective={row['effective_states']:.3f}"
    )

report_file = (
    OUTDIR /
    "exp37b_v3_report.txt"
)

with open(report_file, "w") as f:
    f.write(
        "\n".join(report)
    )

print("Saved:", report_file)

print()
print("EXP_37B V3 complete.")
