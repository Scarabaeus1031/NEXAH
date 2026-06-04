# ============================================================
# EXP_37H_ATLAS_EXPANSION_CAMPAIGN
#
# Goal:
# Harvest atlas information from all available IEEE systems
# and build a unified atlas database for scaling analysis.
#
# Thomas Hofmann / NEXAH
# ============================================================

from pathlib import Path
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_37H_ATLAS_EXPANSION_CAMPAIGN"
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
        "buses": 9,
        "path":
            ROOT.parent
            / "nexah_ieee9"
            / "results"
    },

    "IEEE14": {
        "buses": 14,
        "path":
            ROOT.parent
            / "nexah_ieee14"
            / "results"
    },

    "IEEE30": {
        "buses": 30,
        "path":
            ROOT.parent
            / "nexah_ieee30"
            / "results"
    },

    "IEEE39": {
        "buses": 39,
        "path":
            ROOT.parent
            / "nexah_ieee39"
            / "results"
    },

    "IEEE57": {
        "buses": 57,
        "path":
            ROOT.parent
            / "nexah_ieee57"
            / "results"
    },

    "IEEE118": {
        "buses": 118,
        "path":
            ROOT.parent
            / "nexah_ieee118"
            / "results"
    },

    "IEEE300": {
        "buses": 300,
        "path":
            ROOT.parent
            / "nexah_ieeeX"
            / "results"
    },

    "IEEE1354": {
        "buses": 1354,
        "path":
            ROOT.parent
            / "nexah_ieee1354"
            / "results"
    },

    "PEGASE9241": {
        "buses": 9241,
        "path":
            ROOT.parent
            / "nexah_pegase9241"
            / "results"
    }
}


# ============================================================
# Helpers
# ============================================================

def shannon_entropy(labels):

    if len(labels) == 0:
        return 0.0

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


def load_states(result_dir):

    files = list(
        result_dir.rglob("states.txt")
    )

    labels = []

    for file in files:

        try:

            with open(file, "r") as f:

                labels.extend(
                    [
                        x.strip()
                        for x in f.readlines()
                        if x.strip()
                    ]
                )

        except Exception:
            pass

    return labels


# ============================================================
# Harvest
# ============================================================

master_rows = []

coverage_rows = []

for system, info in SYSTEMS.items():

    print()
    print("=" * 50)
    print(system)
    print("=" * 50)

    labels = load_states(
        info["path"]
    )

    complete = len(labels) > 0

    coverage_rows.append({

        "system": system,

        "states":
            int(complete),

        "atlas":
            int(complete),

        "basins":
            int(complete)
    })

    if not complete:

        print("No data found.")
        continue

    counts = Counter(labels)

    entropy = shannon_entropy(
        labels
    )

    effective_basins = (
        2 ** entropy
    )

    largest_fraction = (
        max(counts.values())
        /
        len(labels)
    )

    master_rows.append({

        "system":
            system,

        "buses":
            info["buses"],

        "n_samples":
            len(labels),

        "n_basins":
            len(counts),

        "entropy":
            entropy,

        "effective_basins":
            effective_basins,

        "largest_basin_fraction":
            largest_fraction,

        "compression_ratio":
            (
                info["buses"]
                /
                effective_basins
            )
    })

    print(
        f"Basins: {len(counts)}"
    )


# ============================================================
# Save Tables
# ============================================================

master_df = pd.DataFrame(
    master_rows
)

coverage_df = pd.DataFrame(
    coverage_rows
)

master_csv = (
    OUTPUT_DIR
    / "exp37h_atlas_master_database.csv"
)

coverage_csv = (
    OUTPUT_DIR
    / "exp37h_system_coverage.csv"
)

master_df.to_csv(
    master_csv,
    index=False
)

coverage_df.to_csv(
    coverage_csv,
    index=False
)

print()
print("Saved:", master_csv)
print("Saved:", coverage_csv)


# ============================================================
# Visual 1
# Coverage Heatmap
# ============================================================

if len(coverage_df):

    plt.figure(
        figsize=(7, 5)
    )

    plt.imshow(
        coverage_df[
            [
                "states",
                "atlas",
                "basins"
            ]
        ],
        aspect="auto"
    )

    plt.yticks(
        range(len(coverage_df)),
        coverage_df["system"]
    )

    plt.xticks(
        [0, 1, 2],
        [
            "states",
            "atlas",
            "basins"
        ]
    )

    plt.title(
        "EXP_37H System Coverage"
    )

    plt.colorbar()

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / "exp37h_system_coverage.png",
        dpi=300
    )

    plt.close()


# ============================================================
# Visual 2
# Compression Scaling
# ============================================================

if len(master_df) >= 2:

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        master_df["buses"],
        master_df["compression_ratio"],
        marker="o"
    )

    plt.xscale("log")

    plt.title(
        "EXP_37H Atlas Compression Scaling"
    )

    plt.xlabel(
        "Bus Count"
    )

    plt.ylabel(
        "Compression Ratio"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / "exp37h_compression_scaling.png",
        dpi=300
    )

    plt.close()


# ============================================================
# Scaling Dataset
# ============================================================

scaling_csv = (
    OUTPUT_DIR
    / "exp37h_scaling_dataset.csv"
)

master_df.to_csv(
    scaling_csv,
    index=False
)

print(
    "Saved:",
    scaling_csv
)


# ============================================================
# Report
# ============================================================

report = []

report.append(
    "EXP_37H ATLAS EXPANSION CAMPAIGN"
)

report.append(
    "=" * 50
)

report.append("")

report.append(
    f"Systems discovered: {len(SYSTEMS)}"
)

report.append(
    f"Systems completed: {len(master_df)}"
)

report.append("")

for _, row in master_df.iterrows():

    report.append(

        f"{row['system']}: "
        f"buses={row['buses']}, "
        f"basins={row['n_basins']}, "
        f"entropy={row['entropy']:.3f}, "
        f"effective={row['effective_basins']:.3f}"
    )

report_file = (
    OUTPUT_DIR
    / "exp37h_report.txt"
)

with open(
    report_file,
    "w"
) as f:

    f.write(
        "\n".join(report)
    )

print(
    "Saved:",
    report_file
)

print()
print("EXP_37H complete.")
