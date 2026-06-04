# ============================================================
# EXP_37B_MULTI_SYSTEM_ATLAS_DISCOVERY_V3
#
# Phase E — Atlas Universality
#
# Harvest atlas structures from all available IEEE systems
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

OUTDIR = (
    ROOT
    / "outputs"
    / "EXP_37B_MULTI_SYSTEM_ATLAS_DISCOVERY_V3"
)

OUTDIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Output ->", OUTDIR)

# ============================================================
# Candidate Atlas Files
# ============================================================

SYSTEMS = {

    "IEEE9":
        ROOT.parent /
        "nexah_ieee9" /
        "results" /
        "states.txt",

    "IEEE14":
        ROOT.parent /
        "nexah_ieee14" /
        "results" /
        "states.txt",

    "IEEE30":
        ROOT.parent /
        "nexah_ieee30" /
        "results" /
        "states.txt",

    "IEEE39":
        ROOT.parent /
        "nexah_ieee39" /
        "results" /
        "states.txt",

    "IEEE57":
        ROOT.parent /
        "nexah_ieee57" /
        "results" /
        "states.txt",

    "IEEE118":
        ROOT.parent /
        "nexah_ieee118" /
        "results" /
        "states.txt",

    "IEEE300":
        ROOT.parent /
        "nexah_ieeeX" /
        "results" /
        "run_ieee300_20260413_015843" /
        "states.txt",

    "IEEE1354":
        ROOT.parent /
        "nexah_ieee1354" /
        "results" /
        "states.txt",

    "PEGASE9241":
        ROOT.parent /
        "nexah_pegase9241" /
        "results" /
        "states.txt"
}

# ============================================================
# Helpers
# ============================================================

def load_states(path):

    if not path.exists():
        return []

    with open(path, "r") as f:

        return [
            line.strip()
            for line in f
            if line.strip()
        ]


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
# Discovery
# ============================================================

summary_rows = []

for system, path in SYSTEMS.items():

    print()
    print("=" * 50)
    print(system)
    print("=" * 50)

    states = load_states(path)

    if len(states) == 0:

        print("No atlas found.")

        continue

    counts = Counter(states)

    total_states = len(states)

    unique_states = len(counts)

    dominant_fraction = (
        max(counts.values())
        / total_states
    )

    ent = entropy(states)

    effective_states = (
        2 ** ent
    )

    atlas_complexity = (
        unique_states * ent
    )

    atlas_df = pd.DataFrame({

        "state":
            list(counts.keys()),

        "count":
            list(counts.values())
    })

    atlas_file = (
        OUTDIR /
        f"{system.lower()}_atlas.csv"
    )

    atlas_df.to_csv(
        atlas_file,
        index=False
    )

    print("Saved:", atlas_file.name)

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
