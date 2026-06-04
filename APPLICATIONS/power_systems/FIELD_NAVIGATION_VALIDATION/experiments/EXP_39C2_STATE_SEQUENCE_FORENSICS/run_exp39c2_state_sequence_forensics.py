#!/usr/bin/env python3
"""
EXP_39C2 — STATE SEQUENCE FORENSICS

Goal:
Inspect historical states.txt files and determine whether they contain:

- warning-class labels
- basin IDs
- atlas states
- mixed labels
- degenerate constant sequences

Thomas Hofmann / NEXAH
"""

from pathlib import Path
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parents[3]

OUTPUT = (
    ROOT
    / "outputs"
    / "EXP_39C2_STATE_SEQUENCE_FORENSICS"
)

OUTPUT.mkdir(parents=True, exist_ok=True)

print("Repository ->", ROOT)
print("Output     ->", OUTPUT)


# ============================================================
# Helpers
# ============================================================

KNOWN_WARNING_LABELS = {
    "SAFE",
    "WATCH",
    "WARNING",
    "CRITICAL",
    "COLLAPSED",
    "UNSTABLE",
    "STABLE",
}


def load_states(path):
    states = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if s:
                    states.append(s)
    except Exception:
        return []

    return states


def classify_sequence(states):
    if not states:
        return "empty"

    unique = set(states)

    if unique.issubset(KNOWN_WARNING_LABELS):
        return "warning_label_sequence"

    numeric_like = True

    for s in unique:
        try:
            float(s)
        except ValueError:
            numeric_like = False
            break

    if numeric_like:
        return "numeric_state_sequence"

    if any("basin" in s.lower() for s in unique):
        return "basin_label_sequence"

    if len(unique) == 1:
        return "constant_sequence"

    return "mixed_or_unknown_sequence"


# ============================================================
# Discover states.txt files
# ============================================================

state_files = sorted(
    ROOT.rglob("states.txt")
)

print("State files discovered:", len(state_files))


# ============================================================
# Analyze files
# ============================================================

summary_rows = []
sample_rows = []
global_counter = Counter()

for file in state_files:

    states = load_states(file)

    if not states:
        continue

    counts = Counter(states)
    unique_states = len(counts)
    total_states = len(states)

    seq_type = classify_sequence(states)

    transitions = 0

    for i in range(len(states) - 1):
        if states[i] != states[i + 1]:
            transitions += 1

    transition_rate = (
        transitions / (total_states - 1)
        if total_states > 1
        else 0.0
    )

    dominant_state, dominant_count = counts.most_common(1)[0]

    dominant_fraction = dominant_count / total_states

    summary_rows.append({
        "file": str(file),
        "run": file.parent.name,
        "total_states": total_states,
        "unique_states": unique_states,
        "sequence_type": seq_type,
        "dominant_state": dominant_state,
        "dominant_fraction": dominant_fraction,
        "transitions": transitions,
        "transition_rate": transition_rate,
    })

    for step, state in enumerate(states[:100]):
        sample_rows.append({
            "file": str(file),
            "run": file.parent.name,
            "step": step,
            "state": state,
        })

    global_counter.update(states)


summary_df = pd.DataFrame(summary_rows)
sample_df = pd.DataFrame(sample_rows)

summary_file = OUTPUT / "exp39c2_state_sequence_summary.csv"
sample_file = OUTPUT / "exp39c2_state_sequence_samples.csv"

summary_df.to_csv(summary_file, index=False)
sample_df.to_csv(sample_file, index=False)

print("Saved:", summary_file)
print("Saved:", sample_file)


# ============================================================
# Global state counts
# ============================================================

global_df = pd.DataFrame([
    {
        "state": state,
        "count": count,
    }
    for state, count in global_counter.items()
]).sort_values(
    "count",
    ascending=False
)

global_file = OUTPUT / "exp39c2_global_state_counts.csv"
global_df.to_csv(global_file, index=False)

print("Saved:", global_file)


# ============================================================
# Visual 1 — Sequence type counts
# ============================================================

if len(summary_df):

    type_counts = (
        summary_df["sequence_type"]
        .value_counts()
        .reset_index()
    )

    type_counts.columns = [
        "sequence_type",
        "count"
    ]

    plt.figure(figsize=(10, 5))

    plt.bar(
        type_counts["sequence_type"],
        type_counts["count"]
    )

    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Files")
    plt.title("EXP_39C2 State Sequence Types")

    plt.tight_layout()

    fig_file = OUTPUT / "exp39c2_sequence_type_counts.png"
    plt.savefig(fig_file, dpi=300)
    plt.close()

    print("Saved:", fig_file)


# ============================================================
# Visual 2 — Global state distribution
# ============================================================

if len(global_df):

    plt.figure(figsize=(10, 5))

    plt.bar(
        global_df["state"],
        global_df["count"]
    )

    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Count")
    plt.title("EXP_39C2 Global State Distribution")

    plt.tight_layout()

    fig_file = OUTPUT / "exp39c2_global_state_distribution.png"
    plt.savefig(fig_file, dpi=300)
    plt.close()

    print("Saved:", fig_file)


# ============================================================
# Visual 3 — Transition rates by run
# ============================================================

if len(summary_df):

    plot_df = summary_df.sort_values(
        "transition_rate",
        ascending=False
    )

    plt.figure(figsize=(12, 6))

    plt.bar(
        plot_df["run"],
        plot_df["transition_rate"]
    )

    plt.xticks(rotation=90)
    plt.ylabel("Transition Rate")
    plt.title("EXP_39C2 Transition Rate by Run")

    plt.tight_layout()

    fig_file = OUTPUT / "exp39c2_transition_rate_by_run.png"
    plt.savefig(fig_file, dpi=300)
    plt.close()

    print("Saved:", fig_file)


# ============================================================
# Report
# ============================================================

report = []

report.append(
    "EXP_39C2 STATE SEQUENCE FORENSICS"
)

report.append("=" * 50)
report.append("")

report.append(
    f"State files discovered: {len(state_files)}"
)

report.append(
    f"State files analyzed: {len(summary_df)}"
)

report.append("")

report.append("Sequence Type Counts")
report.append("--------------------")

if len(summary_df):

    for seq_type, count in summary_df["sequence_type"].value_counts().items():
        report.append(
            f"{seq_type}: {count}"
        )

report.append("")
report.append("Global State Counts")
report.append("-------------------")

for _, row in global_df.iterrows():

    report.append(
        f"{row['state']}: {row['count']}"
    )

report.append("")
report.append("Top Runs By Transition Rate")
report.append("---------------------------")

if len(summary_df):

    for _, row in summary_df.sort_values(
        "transition_rate",
        ascending=False
    ).head(10).iterrows():

        report.append(
            f"{row['run']}: "
            f"type={row['sequence_type']}, "
            f"states={row['total_states']}, "
            f"unique={row['unique_states']}, "
            f"transition_rate={row['transition_rate']:.4f}, "
            f"dominant={row['dominant_state']} "
            f"({row['dominant_fraction']:.3f})"
        )

report.append("")
report.append("Interpretation")
report.append("--------------")
report.append(
    "If most sequences are classified as warning_label_sequence, "
    "the EXP_39C network represents transitions between warning classes "
    "rather than atlas basins."
)

report.append(
    "If numeric_state_sequence or basin_label_sequence files are found, "
    "those files are candidates for true atlas transition extraction."
)

report_file = OUTPUT / "exp39c2_report.txt"

with open(report_file, "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print("Saved:", report_file)

print()
print("EXP_39C2 complete.")
