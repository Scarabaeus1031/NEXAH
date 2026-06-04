# ============================================================
# EXP_37D_ATLAS_INVARIANT_ANALYSIS
#
# Phase E — Atlas Universality
#
# Goal:
# Compare atlas invariants across systems.
#
# Input:
# EXP_37B_MULTI_SYSTEM_ATLAS_DISCOVERY_V2
#
# Output:
# EXP_37D_ATLAS_INVARIANT_ANALYSIS
#
# Thomas Hofmann / NEXAH
# ============================================================

from pathlib import Path
from collections import Counter

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

INPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_37B_MULTI_SYSTEM_ATLAS_DISCOVERY_V2"
)

OUTPUT_DIR = (
    ROOT
    / "outputs"
    / "EXP_37D_ATLAS_INVARIANT_ANALYSIS"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Input  ->", INPUT_DIR)
print("Output ->", OUTPUT_DIR)

# ============================================================
# Atlas Files
# ============================================================

ATLAS_FILES = {
    "IEEE9":
        INPUT_DIR / "ieee9_atlas.csv",

    "IEEE300":
        INPUT_DIR / "ieee300_atlas.csv",
}

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


def effective_states(labels):

    counts = Counter(labels)

    p = np.array(
        list(counts.values()),
        dtype=float
    )

    p /= p.sum()

    return float(
        1.0 / np.sum(p ** 2)
    )


# ============================================================
# Extraction
# ============================================================

rows = []

for system, file_path in ATLAS_FILES.items():

    print()
    print("=" * 50)
    print(system)
    print("=" * 50)

    if not file_path.exists():

        print("Missing:", file_path)

        continue

    df = pd.read_csv(file_path)

    print("Loaded:", file_path.name)
    print("Rows:", len(df))

    # --------------------------------------------------------
    # Find state column automatically
    # --------------------------------------------------------

    state_col = None

    for col in df.columns:

        c = col.lower()

        if (
            "state" in c or
            "class" in c or
            "cluster" in c or
            "basin" in c
        ):
            state_col = col
            break

    if state_col is None:

        state_col = df.columns[-1]

    labels = (
        df[state_col]
        .astype(str)
        .tolist()
    )

    counts = Counter(labels)

    total_states = len(labels)

    unique_states = len(counts)

    entropy = shannon_entropy(labels)

    dominant_fraction = (
        max(counts.values())
        / total_states
    )

    coverage = (
        unique_states
        / total_states
    )

    eff_states = effective_states(labels)

    complexity = (
        entropy
        * unique_states
    )

    rows.append({
        "system": system,
        "total_states": total_states,
        "unique_states": unique_states,
        "entropy": entropy,
        "coverage": coverage,
        "dominant_fraction": dominant_fraction,
        "effective_states": eff_states,
        "atlas_complexity": complexity
    })

    print(
        f"Classes: {unique_states}"
    )

    print(
        f"Entropy: {entropy:.3f}"
    )

# ============================================================
# Save Table
# ============================================================

results = pd.DataFrame(rows)

csv_file = (
    OUTPUT_DIR
    / "exp37d_invariant_table.csv"
)

results.to_csv(
    csv_file,
    index=False
)

print()
print("Saved:", csv_file)

# ============================================================
# Heatmap
# ============================================================

heatmap_df = (
    results
    .set_index("system")
)

plt.figure(figsize=(10,6))

sns.heatmap(
    heatmap_df,
    annot=True,
    cmap="viridis",
    fmt=".2f"
)

plt.title(
    "EXP_37D Atlas Invariants"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37d_invariant_heatmap.png",
    dpi=300
)

plt.close()

# ============================================================
# Entropy
# ============================================================

plt.figure(figsize=(8,5))

plt.bar(
    results["system"],
    results["entropy"]
)

plt.ylabel("Entropy")

plt.title(
    "Atlas Entropy Comparison"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37d_entropy_comparison.png",
    dpi=300
)

plt.close()

# ============================================================
# Complexity
# ============================================================

plt.figure(figsize=(8,5))

plt.bar(
    results["system"],
    results["atlas_complexity"]
)

plt.ylabel(
    "Complexity"
)

plt.title(
    "Atlas Complexity"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37d_complexity_comparison.png",
    dpi=300
)

plt.close()

# ============================================================
# Dominant Fraction
# ============================================================

plt.figure(figsize=(8,5))

plt.bar(
    results["system"],
    results["dominant_fraction"]
)

plt.ylabel(
    "Dominant Fraction"
)

plt.title(
    "Atlas Dominance"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37d_dominant_fraction.png",
    dpi=300
)

plt.close()

# ============================================================
# Effective States
# ============================================================

plt.figure(figsize=(8,5))

plt.bar(
    results["system"],
    results["effective_states"]
)

plt.ylabel(
    "Effective States"
)

plt.title(
    "Atlas Effective Diversity"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37d_effective_states.png",
    dpi=300
)

plt.close()

# ============================================================
# Dashboard
# ============================================================

fig = plt.figure(
    figsize=(10,6)
)

plt.axis("off")

lines = [
    "EXP_37D ATLAS INVARIANT ANALYSIS",
    "",
]

for _, row in results.iterrows():

    lines.append(
        f"{row['system']}: "
        f"classes={row['unique_states']}, "
        f"entropy={row['entropy']:.3f}, "
        f"complexity={row['atlas_complexity']:.3f}"
    )

plt.text(
    0.02,
    0.95,
    "\n".join(lines),
    fontsize=12,
    va="top"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp37d_dashboard.png",
    dpi=300
)

plt.close()

# ============================================================
# Report
# ============================================================

report = []

report.append(
    "EXP_37D ATLAS INVARIANT ANALYSIS"
)

report.append("=" * 40)
report.append("")

for _, row in results.iterrows():

    report.append(
        f"{row['system']}: "
        f"classes={row['unique_states']}, "
        f"entropy={row['entropy']:.3f}, "
        f"coverage={row['coverage']:.6f}, "
        f"effective_states={row['effective_states']:.3f}"
    )

report_file = (
    OUTPUT_DIR
    / "exp37d_report.txt"
)

with open(report_file, "w") as f:
    f.write(
        "\n".join(report)
    )

print("Saved:", report_file)

print()
print("EXP_37D complete.")
