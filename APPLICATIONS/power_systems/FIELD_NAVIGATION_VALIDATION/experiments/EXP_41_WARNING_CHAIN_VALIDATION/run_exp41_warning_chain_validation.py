"""
EXP_41 — WARNING CHAIN VALIDATION

Purpose
-------
Validate whether historical NEXAH warning sequences follow
a structured degradation chain:

SAFE -> WARNING -> CRITICAL -> COLLAPSED

or whether collapse occurs through alternative pathways.

Outputs
-------
exp41_chain_counts.csv
exp41_chain_probabilities.csv
exp41_chain_lengths.csv

exp41_chain_network.png
exp41_chain_frequency.png
exp41_degradation_sankey.png

exp41_report.txt
"""

from pathlib import Path
from collections import Counter, defaultdict

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# ============================================================
# Paths
# ============================================================

REPO_ROOT = (
    Path(__file__)
    .resolve()
    .parents[4]
    / "power_systems"
)

OUTPUT_DIR = (
    REPO_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_41_WARNING_CHAIN_VALIDATION"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Repository -> {REPO_ROOT}")
print(f"Output     -> {OUTPUT_DIR}")

# ============================================================
# Discover state files
# ============================================================

state_files = list(REPO_ROOT.rglob("states.txt"))

print()
print(f"State files discovered: {len(state_files)}")

if len(state_files) == 0:
    raise RuntimeError("No states.txt files found.")

# ============================================================
# Helpers
# ============================================================

VALID_STATES = {
    "SAFE",
    "WARNING",
    "CRITICAL",
    "COLLAPSED"
}


def load_states(path):
    states = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:

                text = line.strip().upper()

                for s in VALID_STATES:
                    if s in text:
                        states.append(s)
                        break

    except Exception:
        pass

    return states


def contains_chain(sequence, chain):
    n = len(chain)

    for i in range(len(sequence) - n + 1):
        if sequence[i:i+n] == chain:
            return True

    return False


# ============================================================
# Analysis
# ============================================================

transition_counter = Counter()

chain_counter = Counter()

chain_lengths = []

warning_total = 0
warning_to_safe = 0
warning_to_critical = 0
warning_to_collapsed = 0

critical_total = 0
critical_to_safe = 0
critical_to_collapsed = 0

runs_processed = 0

FULL_CHAIN = [
    "SAFE",
    "WARNING",
    "CRITICAL",
    "COLLAPSED"
]

for file in state_files:

    states = load_states(file)

    if len(states) < 2:
        continue

    runs_processed += 1

    # --------------------------------------------------------
    # transitions
    # --------------------------------------------------------

    for a, b in zip(states[:-1], states[1:]):

        transition_counter[(a, b)] += 1

        if a == "WARNING":
            warning_total += 1

            if b == "SAFE":
                warning_to_safe += 1

            elif b == "CRITICAL":
                warning_to_critical += 1

            elif b == "COLLAPSED":
                warning_to_collapsed += 1

        if a == "CRITICAL":
            critical_total += 1

            if b == "SAFE":
                critical_to_safe += 1

            elif b == "COLLAPSED":
                critical_to_collapsed += 1

    # --------------------------------------------------------
    # chain validation
    # --------------------------------------------------------

    if contains_chain(states, FULL_CHAIN):
        chain_counter["SAFE_WARNING_CRITICAL_COLLAPSED"] += 1

    if contains_chain(states, ["SAFE", "COLLAPSED"]):
        chain_counter["SAFE_COLLAPSED"] += 1

    if contains_chain(states, ["SAFE", "CRITICAL", "SAFE"]):
        chain_counter["SAFE_CRITICAL_SAFE"] += 1

    if contains_chain(states, ["WARNING", "CRITICAL"]):
        chain_counter["WARNING_CRITICAL"] += 1

    if contains_chain(states, ["CRITICAL", "COLLAPSED"]):
        chain_counter["CRITICAL_COLLAPSED"] += 1

    chain_lengths.append(len(states))

# ============================================================
# Probabilities
# ============================================================

prob_rows = []

if warning_total > 0:

    prob_rows.append({
        "metric": "warning_to_safe",
        "probability": warning_to_safe / warning_total
    })

    prob_rows.append({
        "metric": "warning_to_critical",
        "probability": warning_to_critical / warning_total
    })

    prob_rows.append({
        "metric": "warning_to_collapsed",
        "probability": warning_to_collapsed / warning_total
    })

if critical_total > 0:

    prob_rows.append({
        "metric": "critical_to_safe",
        "probability": critical_to_safe / critical_total
    })

    prob_rows.append({
        "metric": "critical_to_collapsed",
        "probability": critical_to_collapsed / critical_total
    })

# ============================================================
# Save CSVs
# ============================================================

df_counts = pd.DataFrame(
    [
        {"chain": k, "count": v}
        for k, v in chain_counter.items()
    ]
)

df_probs = pd.DataFrame(prob_rows)

df_lengths = pd.DataFrame({
    "sequence_length": chain_lengths
})

counts_csv = OUTPUT_DIR / "exp41_chain_counts.csv"
probs_csv = OUTPUT_DIR / "exp41_chain_probabilities.csv"
lengths_csv = OUTPUT_DIR / "exp41_chain_lengths.csv"

df_counts.to_csv(counts_csv, index=False)
df_probs.to_csv(probs_csv, index=False)
df_lengths.to_csv(lengths_csv, index=False)

print("Saved:", counts_csv)
print("Saved:", probs_csv)
print("Saved:", lengths_csv)

# ============================================================
# Network Plot
# ============================================================

G = nx.DiGraph()

for (a, b), w in transition_counter.items():
    G.add_edge(a, b, weight=w)

plt.figure(figsize=(8, 6))

pos = nx.spring_layout(G, seed=42)

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=2500
)

nx.draw_networkx_labels(
    G,
    pos,
    font_size=12
)

nx.draw_networkx_edges(
    G,
    pos,
    arrows=True
)

plt.title("EXP_41 Warning Chain Network")
plt.axis("off")

network_png = OUTPUT_DIR / "exp41_chain_network.png"

plt.savefig(network_png, dpi=300, bbox_inches="tight")
plt.close()

print("Saved:", network_png)

# ============================================================
# Chain Frequency
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    list(chain_counter.keys()),
    list(chain_counter.values())
)

plt.xticks(rotation=35)
plt.ylabel("Count")
plt.title("EXP_41 Chain Frequency")

freq_png = OUTPUT_DIR / "exp41_chain_frequency.png"

plt.tight_layout()
plt.savefig(freq_png, dpi=300)
plt.close()

print("Saved:", freq_png)

# ============================================================
# Simple Sankey Substitute
# ============================================================

flow = {
    "WARNING→SAFE": warning_to_safe,
    "WARNING→CRITICAL": warning_to_critical,
    "WARNING→COLLAPSED": warning_to_collapsed,
    "CRITICAL→SAFE": critical_to_safe,
    "CRITICAL→COLLAPSED": critical_to_collapsed
}

plt.figure(figsize=(8, 5))

plt.barh(
    list(flow.keys()),
    list(flow.values())
)

plt.title("EXP_41 Degradation Flow")

sankey_png = OUTPUT_DIR / "exp41_degradation_sankey.png"

plt.tight_layout()
plt.savefig(sankey_png, dpi=300)
plt.close()

print("Saved:", sankey_png)

# ============================================================
# Report
# ============================================================

report = OUTPUT_DIR / "exp41_report.txt"

with open(report, "w") as f:

    f.write("\n")
    f.write("EXP_41 WARNING CHAIN VALIDATION\n")
    f.write("==================================================\n\n")

    f.write(f"Runs Processed: {runs_processed}\n\n")

    f.write("Chain Counts\n")
    f.write("--------------------\n")

    for k, v in chain_counter.items():
        f.write(f"{k}: {v}\n")

    f.write("\n")

    f.write("Warning Survival\n")
    f.write("--------------------\n")

    if warning_total > 0:
        f.write(
            f"WARNING -> SAFE: "
            f"{warning_to_safe / warning_total:.3f}\n"
        )

        f.write(
            f"WARNING -> CRITICAL: "
            f"{warning_to_critical / warning_total:.3f}\n"
        )

    f.write("\n")

    f.write("Critical Survival\n")
    f.write("--------------------\n")

    if critical_total > 0:
        f.write(
            f"CRITICAL -> SAFE: "
            f"{critical_to_safe / critical_total:.3f}\n"
        )

        f.write(
            f"CRITICAL -> COLLAPSED: "
            f"{critical_to_collapsed / critical_total:.3f}\n"
        )

    f.write("\n")

    f.write("Interpretation\n")
    f.write("--------------\n")
    f.write(
        "EXP_41 validates whether historical "
        "warning-state sequences form a "
        "structured degradation chain.\n"
    )

print("Saved:", report)

print()
print("EXP_41 complete.")
