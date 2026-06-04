#!/usr/bin/env python3

"""
EXP_40 — EARLY WARNING RECONSTRUCTION

Objective
---------
Reconstruct historical early-warning behavior from archived
warning-state sequences.

This experiment estimates:

- transition probabilities
- collapse pathways
- warning lead times
- pathway frequencies

Inputs
------
Searches recursively for:

    states.txt

inside:

    APPLICATIONS/power_systems

Outputs
-------
exp40_transition_probabilities.csv
exp40_collapse_pathways.csv
exp40_warning_lead_times.csv
exp40_state_pathway_matrix.png
exp40_early_warning_dashboard.png
exp40_report.txt
"""

from pathlib import Path
from collections import Counter, defaultdict

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[4]

SEARCH_ROOT = ROOT / "APPLICATIONS" / "power_systems"

OUTPUT_DIR = (
    ROOT
    / "APPLICATIONS"
    / "power_systems"
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_40_EARLY_WARNING_RECONSTRUCTION"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Repository -> {SEARCH_ROOT}")
print(f"Output     -> {OUTPUT_DIR}")


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

VALID_STATES = {
    "SAFE",
    "WARNING",
    "CRITICAL",
    "COLLAPSED"
}


def load_states(path):
    seq = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip().upper()

                if s in VALID_STATES:
                    seq.append(s)

    except Exception:
        return []

    return seq


# --------------------------------------------------
# DISCOVER FILES
# --------------------------------------------------

state_files = sorted(SEARCH_ROOT.rglob("states.txt"))

print()
print(f"State files discovered: {len(state_files)}")

if not state_files:
    raise RuntimeError("No states.txt files found.")


# --------------------------------------------------
# GLOBAL COLLECTIONS
# --------------------------------------------------

transition_counter = Counter()

pathway_counter = Counter()

lead_times = []

collapse_paths = []

total_sequences = 0


# --------------------------------------------------
# PROCESS FILES
# --------------------------------------------------

for sf in state_files:

    seq = load_states(sf)

    if len(seq) < 2:
        continue

    total_sequences += 1

    # ------------------------------------------
    # transitions
    # ------------------------------------------

    for a, b in zip(seq[:-1], seq[1:]):
        transition_counter[(a, b)] += 1

    # ------------------------------------------
    # collapse pathways
    # ------------------------------------------

    for i in range(len(seq)):

        if seq[i] != "COLLAPSED":
            continue

        start = max(0, i - 3)

        path = tuple(seq[start:i + 1])

        pathway_counter[path] += 1

        collapse_paths.append(
            {
                "file": str(sf),
                "pathway": " -> ".join(path)
            }
        )

    # ------------------------------------------
    # warning lead times
    # ------------------------------------------

    warning_idx = None

    for i, s in enumerate(seq):

        if s == "WARNING" and warning_idx is None:
            warning_idx = i

        if s == "COLLAPSED" and warning_idx is not None:

            lead_times.append(i - warning_idx)

            break


# --------------------------------------------------
# TRANSITION PROBABILITIES
# --------------------------------------------------

state_totals = defaultdict(int)

for (a, b), c in transition_counter.items():
    state_totals[a] += c

transition_rows = []

for (a, b), c in sorted(transition_counter.items()):

    prob = c / state_totals[a]

    transition_rows.append(
        {
            "from_state": a,
            "to_state": b,
            "count": c,
            "probability": prob
        }
    )

df_trans = pd.DataFrame(transition_rows)

trans_file = OUTPUT_DIR / "exp40_transition_probabilities.csv"
df_trans.to_csv(trans_file, index=False)

print(f"Saved: {trans_file}")


# --------------------------------------------------
# COLLAPSE PATHWAYS
# --------------------------------------------------

df_paths = pd.DataFrame(
    [
        {
            "pathway": " -> ".join(k),
            "count": v
        }
        for k, v in pathway_counter.most_common()
    ]
)

paths_file = OUTPUT_DIR / "exp40_collapse_pathways.csv"
df_paths.to_csv(paths_file, index=False)

print(f"Saved: {paths_file}")


# --------------------------------------------------
# LEAD TIMES
# --------------------------------------------------

df_lead = pd.DataFrame(
    {
        "warning_to_collapse_steps": lead_times
    }
)

lead_file = OUTPUT_DIR / "exp40_warning_lead_times.csv"
df_lead.to_csv(lead_file, index=False)

print(f"Saved: {lead_file}")


# --------------------------------------------------
# MATRIX VISUAL
# --------------------------------------------------

states = ["SAFE", "WARNING", "CRITICAL", "COLLAPSED"]

matrix = np.zeros((4, 4))

for _, row in df_trans.iterrows():

    i = states.index(row["from_state"])
    j = states.index(row["to_state"])

    matrix[i, j] = row["probability"]

plt.figure(figsize=(7, 6))

plt.imshow(matrix)

plt.xticks(range(4), states)
plt.yticks(range(4), states)

plt.colorbar(label="Transition Probability")

plt.title("EXP40 State Pathway Matrix")

plt.tight_layout()

matrix_png = OUTPUT_DIR / "exp40_state_pathway_matrix.png"

plt.savefig(matrix_png, dpi=200)
plt.close()

print(f"Saved: {matrix_png}")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

fig = plt.figure(figsize=(12, 8))

# Transition counts
ax1 = fig.add_subplot(221)

top = df_trans.sort_values(
    "count",
    ascending=False
).head(8)

ax1.bar(
    range(len(top)),
    top["count"]
)

ax1.set_xticks(range(len(top)))
ax1.set_xticklabels(
    [
        f"{a}->{b}"
        for a, b in zip(
            top["from_state"],
            top["to_state"]
        )
    ],
    rotation=45
)

ax1.set_title("Top Transitions")

# Pathways
ax2 = fig.add_subplot(222)

top_paths = df_paths.head(8)

ax2.barh(
    range(len(top_paths)),
    top_paths["count"]
)

ax2.set_yticks(range(len(top_paths)))
ax2.set_yticklabels(
    top_paths["pathway"]
)

ax2.set_title("Collapse Pathways")

# Lead times
ax3 = fig.add_subplot(223)

if lead_times:
    ax3.hist(lead_times, bins=15)

ax3.set_title("Warning Lead Times")

# State totals
ax4 = fig.add_subplot(224)

state_counts = Counter()

for (a, b), c in transition_counter.items():
    state_counts[a] += c

ax4.bar(
    state_counts.keys(),
    state_counts.values()
)

ax4.set_title("State Activity")

plt.tight_layout()

dashboard_png = OUTPUT_DIR / "exp40_early_warning_dashboard.png"

plt.savefig(dashboard_png, dpi=200)
plt.close()

print(f"Saved: {dashboard_png}")


# --------------------------------------------------
# REPORT
# --------------------------------------------------

report = OUTPUT_DIR / "exp40_report.txt"

most_transition = (
    df_trans.sort_values(
        "count",
        ascending=False
    )
    .iloc[0]
)

with open(report, "w") as f:

    f.write("\n")
    f.write("EXP_40 EARLY WARNING RECONSTRUCTION\n")
    f.write("=" * 50 + "\n\n")

    f.write(f"Runs Processed: {total_sequences}\n\n")

    f.write(
        f"Unique Transitions: {len(df_trans)}\n"
    )

    f.write(
        f"Collapse Pathways: {len(df_paths)}\n\n"
    )

    f.write("Most Common Transition:\n")
    f.write(
        f"{most_transition['from_state']} -> "
        f"{most_transition['to_state']} "
        f"({int(most_transition['count'])})\n\n"
    )

    if lead_times:

        f.write("Warning Lead Times\n")
        f.write("------------------\n")
        f.write(
            f"Mean: {np.mean(lead_times):.2f}\n"
        )
        f.write(
            f"Median: {np.median(lead_times):.2f}\n"
        )
        f.write(
            f"Max: {max(lead_times)}\n\n"
        )

    f.write("Interpretation\n")
    f.write("--------------\n")
    f.write(
        "EXP_40 reconstructs historical "
        "warning-to-collapse behavior from "
        "archived NEXAH state sequences.\n"
    )

print(f"Saved: {report}")

print()
print("EXP_40 complete.")
