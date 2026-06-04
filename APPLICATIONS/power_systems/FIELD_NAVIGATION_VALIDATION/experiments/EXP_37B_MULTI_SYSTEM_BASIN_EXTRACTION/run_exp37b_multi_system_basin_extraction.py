# ============================================================
# EXP_37B V4
# MULTI-SYSTEM BASIN EXTRACTION
#
# Thomas Hofmann / NEXAH
# ============================================================

from pathlib import Path
from collections import Counter

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

import matplotlib.pyplot as plt


# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

INPUT_DIR = (
    ROOT /
    "outputs" /
    "EXP_37B_MULTI_SYSTEM_ATLAS_DISCOVERY_V2"
)

OUTPUT_DIR = (
    ROOT /
    "outputs" /
    "EXP_37B_MULTI_SYSTEM_BASIN_EXTRACTION"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Input  ->", INPUT_DIR)
print("Output ->", OUTPUT_DIR)


# ============================================================
# Files
# ============================================================

ATLAS_FILES = sorted(
    INPUT_DIR.glob("*_atlas.csv")
)

summary = []


# ============================================================
# Helpers
# ============================================================

def shannon_entropy(labels):

    counts = Counter(labels)

    p = np.array(
        list(counts.values()),
        dtype=float
    )

    p /= p.sum()

    return float(
        -np.sum(
            p * np.log2(p)
        )
    )


# ============================================================
# Extraction
# ============================================================

for file in ATLAS_FILES:

    system = file.stem.replace(
        "_atlas",
        ""
    ).upper()

    print()
    print("=" * 50)
    print(system)
    print("=" * 50)

    df = pd.read_csv(file)

    if "state" not in df.columns:
        continue

    labels = df["state"].astype(str)

    encoder = LabelEncoder()

    x = encoder.fit_transform(
        labels
    )

    # ------------------------------------
    # Window embedding
    # ------------------------------------

    window = 5

    vectors = []

    for i in range(
        len(x) - window
    ):

        vectors.append(
            x[i:i+window]
        )

    X = np.array(vectors)

    if len(X) < 20:
        continue

    # ------------------------------------
    # Basin discovery
    # ------------------------------------

    k = min(
        6,
        max(
            2,
            len(np.unique(x))
        )
    )

    km = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=20
    )

    basin_id = km.fit_predict(X)

    basin_counts = (
        pd.Series(basin_id)
        .value_counts()
        .sort_index()
    )

    basin_entropy = shannon_entropy(
        basin_id
    )

    effective_basins = (
        2 ** basin_entropy
    )

    largest_fraction = (
        basin_counts.max()
        / basin_counts.sum()
    )

    basin_df = pd.DataFrame({
        "basin_id":
            basin_counts.index,
        "count":
            basin_counts.values
    })

    basin_file = (
        OUTPUT_DIR /
        f"{system.lower()}_basins.csv"
    )

    basin_df.to_csv(
        basin_file,
        index=False
    )

    print(
        "Basins:",
        len(basin_counts)
    )

    print(
        "Entropy:",
        round(
            basin_entropy,
            3
        )
    )

    summary.append({

        "system":
            system,

        "n_basins":
            len(basin_counts),

        "basin_entropy":
            basin_entropy,

        "effective_basins":
            effective_basins,

        "largest_basin_fraction":
            largest_fraction
    })


# ============================================================
# Summary
# ============================================================

summary_df = pd.DataFrame(
    summary
)

summary_csv = (
    OUTPUT_DIR /
    "exp37b_v4_basin_summary.csv"
)

summary_df.to_csv(
    summary_csv,
    index=False
)

print()
print("Saved:", summary_csv)


# ============================================================
# Visual
# ============================================================

if len(summary_df):

    plt.figure(
        figsize=(8,5)
    )

    plt.bar(
        summary_df["system"],
        summary_df["n_basins"]
    )

    plt.title(
        "EXP_37B V4 Basin Count"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR /
        "exp37b_v4_basin_count.png",
        dpi=300
    )

    plt.close()


# ============================================================
# Report
# ============================================================

report = []

report.append(
    "EXP_37B V4 MULTI-SYSTEM BASIN EXTRACTION"
)

report.append(
    "=" * 50
)

report.append("")

for _, row in summary_df.iterrows():

    report.append(
        f"{row['system']}: "
        f"basins={row['n_basins']}, "
        f"entropy={row['basin_entropy']:.3f}, "
        f"effective={row['effective_basins']:.3f}"
    )

report_file = (
    OUTPUT_DIR /
    "exp37b_v4_report.txt"
)

with open(report_file, "w") as f:
    f.write(
        "\n".join(report)
    )

print("Saved:", report_file)

print()
print("EXP_37B V4 complete.")
