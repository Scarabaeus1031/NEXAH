# ============================================================
# EXP_37C_ATLAS_UNIVERSALITY_VALIDATION
#
# Goal:
# Validate whether atlas structures exhibit
# consistent organization across discovered systems.
#
# Input:
# EXP_37B_MULTI_SYSTEM_ATLAS_DISCOVERY_V2
#
# Output:
# EXP_37C_ATLAS_UNIVERSALITY_VALIDATION
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

INPUT_DIR = (
    ROOT /
    "outputs" /
    "EXP_37B_MULTI_SYSTEM_ATLAS_DISCOVERY_V2"
)

OUTDIR = (
    ROOT /
    "outputs" /
    "EXP_37C_ATLAS_UNIVERSALITY_VALIDATION"
)

OUTDIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Input  ->", INPUT_DIR)
print("Output ->", OUTDIR)


# ============================================================
# Systems
# ============================================================

SYSTEMS = {
    "IEEE9":
        INPUT_DIR /
        "ieee9_atlas.csv",

    "IEEE300":
        INPUT_DIR /
        "ieee300_atlas.csv",
}


# ============================================================
# Helpers
# ============================================================

def load_states(path):

    if not path.exists():
        return []

    df = pd.read_csv(path)

    if "state" in df.columns:
        return (
            df["state"]
            .astype(str)
            .tolist()
        )

    if "class" in df.columns:
        return (
            df["class"]
            .astype(str)
            .tolist()
        )

    return []


def entropy(states):

    if len(states) == 0:
        return 0.0

    counts = Counter(states)

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
# Analysis
# ============================================================

rows = []

for system, file_path in SYSTEMS.items():

    print()
    print("=" * 40)
    print(system)
    print("=" * 40)

    states = load_states(file_path)

    print("File:", file_path.name)
    print("Loaded:", len(states))

    if len(states) == 0:

        rows.append({
            "system": system,
            "total_states": 0,
            "unique_states": 0,
            "coverage": 0,
            "entropy": 0,
            "dominant_fraction": 0,
            "universality_score": 0
        })

        continue

    counts = Counter(states)

    total_states = len(states)

    unique_states = len(counts)

    coverage = (
        unique_states /
        total_states
    )

    ent = entropy(states)

    dominant_fraction = (
        max(counts.values()) /
        total_states
    )

    score = 0

    if unique_states >= 3:
        score += 1

    if unique_states >= 2:
        score += 1

    if ent > 0:
        score += 1

    if dominant_fraction < 0.95:
        score += 1

    if total_states > 100:
        score += 1

    rows.append({
        "system": system,
        "total_states": total_states,
        "unique_states": unique_states,
        "coverage": coverage,
        "entropy": ent,
        "dominant_fraction": dominant_fraction,
        "universality_score": score
    })

    print(
        f"States: {total_states}"
    )

    print(
        f"Classes: {unique_states}"
    )

    print(
        f"Entropy: {ent:.3f}"
    )

    print(
        f"Dominant Fraction: {dominant_fraction:.3f}"
    )

    print(
        f"Score: {score}/5"
    )


# ============================================================
# Save Table
# ============================================================

df = pd.DataFrame(rows)

csv_file = (
    OUTDIR /
    "exp37c_universality_table.csv"
)

df.to_csv(
    csv_file,
    index=False
)

print()
print("Saved:", csv_file)


# ============================================================
# Visual 1
# Universality Score
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.bar(
    df["system"],
    df["universality_score"]
)

plt.ylabel("Score")

plt.title(
    "EXP_37C Universality Score"
)

plt.tight_layout()

plt.savefig(
    OUTDIR /
    "exp37c_score.png",
    dpi=200
)

plt.close()


# ============================================================
# Visual 2
# Entropy
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.bar(
    df["system"],
    df["entropy"]
)

plt.ylabel("Entropy")

plt.title(
    "EXP_37C State Entropy"
)

plt.tight_layout()

plt.savefig(
    OUTDIR /
    "exp37c_entropy.png",
    dpi=200
)

plt.close()


# ============================================================
# Visual 3
# Coverage
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.bar(
    df["system"],
    df["coverage"]
)

plt.ylabel("Coverage")

plt.title(
    "EXP_37C Atlas Coverage"
)

plt.tight_layout()

plt.savefig(
    OUTDIR /
    "exp37c_coverage.png",
    dpi=200
)

plt.close()


# ============================================================
# Visual 4
# Dashboard
# ============================================================

fig = plt.figure(
    figsize=(10, 6)
)

plt.axis("off")

lines = [
    "EXP_37C ATLAS UNIVERSALITY VALIDATION",
    "",
    f"Systems analyzed: {len(df)}",
    "",
]

for _, row in df.iterrows():

    lines.append(
        f"{row['system']}: "
        f"score={row['universality_score']}/5, "
        f"classes={row['unique_states']}, "
        f"entropy={row['entropy']:.3f}"
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
    OUTDIR /
    "exp37c_universality_dashboard.png",
    dpi=200
)

plt.close()


# ============================================================
# Report
# ============================================================

report = []

report.append(
    "EXP_37C ATLAS UNIVERSALITY VALIDATION"
)

report.append("=" * 40)
report.append("")

report.append(
    f"Systems analyzed: {len(df)}"
)

report.append("")

for _, row in df.iterrows():

    report.append(
        f"{row['system']}: "
        f"Score={row['universality_score']}/5, "
        f"Classes={row['unique_states']}, "
        f"Entropy={row['entropy']:.3f}"
    )

report_file = (
    OUTDIR /
    "exp37c_report.txt"
)

with open(
    report_file,
    "w"
) as f:
    f.write(
        "\n".join(report)
    )

print("Saved:", report_file)

print()
print("EXP_37C complete.")
