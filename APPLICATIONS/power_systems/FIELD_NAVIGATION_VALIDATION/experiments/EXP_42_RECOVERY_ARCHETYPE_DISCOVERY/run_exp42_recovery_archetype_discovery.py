#!/usr/bin/env python3
"""
EXP_42_RECOVERY_ARCHETYPE_DISCOVERY

Goal
-----
Discover recurring recovery archetypes inside historical
NEXAH warning-state sequences.

Example archetypes:

SAFE -> WARNING -> SAFE

SAFE -> CRITICAL -> SAFE

SAFE -> WARNING -> CRITICAL -> SAFE

SAFE -> WARNING -> CRITICAL -> COLLAPSED

Outputs
-------
exp42_recovery_archetypes.csv
exp42_archetype_counts.csv
exp42_archetype_lengths.csv
exp42_recovery_network.png
exp42_recovery_archetypes.png
exp42_recovery_funnel.png
exp42_report.txt
"""

from pathlib import Path
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

from pathlib import Path

ROOT = (
    Path(__file__)
    .resolve()
    .parents[4]
)

# ROOT zeigt bereits auf:
# .../NEXAH/APPLICATIONS

REPO = ROOT / "power_systems"

OUTDIR = (
    ROOT
    / "power_systems"
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_42_RECOVERY_ARCHETYPE_DISCOVERY"
)

OUTDIR.mkdir(
    parents=True,
    exist_ok=True
)

print(f"Repository -> {REPO}")
print(f"Output     -> {OUTDIR}")

print("\nChecking search path:")
print(REPO)
print("Exists:", REPO.exists())


# --------------------------------------------------
# FIND STATES FILES
# --------------------------------------------------

state_files = sorted(
    REPO.rglob("states.txt")
)

print(
    f"\nState files discovered: {len(state_files)}"
)

if not state_files:

    print("\nAvailable directories:")

    try:
        for p in REPO.iterdir():
            print(" -", p.name)
    except Exception:
        pass

    raise RuntimeError(
        "No states.txt files found."
    )


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

VALID = {
    "SAFE",
    "WARNING",
    "CRITICAL",
    "COLLAPSED"
}


def normalize(line):
    line = line.strip().upper()

    for s in VALID:
        if s in line:
            return s

    return None


def compress(seq):
    """
    Remove repeated consecutive states.

    SAFE SAFE SAFE WARNING WARNING SAFE

    ->
    SAFE WARNING SAFE
    """
    if not seq:
        return []

    out = [seq[0]]

    for s in seq[1:]:
        if s != out[-1]:
            out.append(s)

    return out


# --------------------------------------------------
# EXTRACT ARCHETYPES
# --------------------------------------------------

archetypes = []
lengths = []

for file in state_files:

    try:
        raw = file.read_text(errors="ignore").splitlines()

    except Exception:
        continue

    seq = []

    for line in raw:
        state = normalize(line)

        if state:
            seq.append(state)

    if len(seq) < 3:
        continue

    seq = compress(seq)

    pattern = " -> ".join(seq)

    archetypes.append(pattern)
    lengths.append(len(seq))


# --------------------------------------------------
# COUNTS
# --------------------------------------------------

arch_counter = Counter(archetypes)

arch_df = pd.DataFrame(
    [
        {
            "archetype": k,
            "count": v
        }
        for k, v in arch_counter.items()
    ]
).sort_values("count", ascending=False)

arch_df.to_csv(
    OUTDIR / "exp42_recovery_archetypes.csv",
    index=False
)

print(
    f"Saved: {OUTDIR/'exp42_recovery_archetypes.csv'}"
)

count_df = arch_df.copy()

count_df.to_csv(
    OUTDIR / "exp42_archetype_counts.csv",
    index=False
)

print(
    f"Saved: {OUTDIR/'exp42_archetype_counts.csv'}"
)

length_df = pd.DataFrame(
    {"length": lengths}
)

length_df.to_csv(
    OUTDIR / "exp42_archetype_lengths.csv",
    index=False
)

print(
    f"Saved: {OUTDIR/'exp42_archetype_lengths.csv'}"
)


# --------------------------------------------------
# NETWORK
# --------------------------------------------------

G = nx.DiGraph()

for pattern in archetypes:

    nodes = pattern.split(" -> ")

    for a, b in zip(nodes[:-1], nodes[1:]):

        if G.has_edge(a, b):
            G[a][b]["weight"] += 1
        else:
            G.add_edge(a, b, weight=1)

plt.figure(figsize=(10, 8))

pos = nx.spring_layout(
    G,
    seed=42
)

weights = [
    G[u][v]["weight"]
    for u, v in G.edges()
]

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=5000
)

nx.draw_networkx_labels(
    G,
    pos,
    font_size=18
)

nx.draw_networkx_edges(
    G,
    pos,
    width=[
        max(1, w / 5)
        for w in weights
    ],
    arrows=True
)

plt.title(
    "EXP_42 Recovery Archetype Network"
)

plt.axis("off")

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp42_recovery_network.png",
    dpi=300
)

plt.close()

print(
    f"Saved: {OUTDIR/'exp42_recovery_network.png'}"
)


# --------------------------------------------------
# TOP ARCHETYPES
# --------------------------------------------------

plt.figure(figsize=(12, 6))

top = arch_df.head(10)

plt.barh(
    top["archetype"],
    top["count"]
)

plt.title(
    "EXP_42 Recovery Archetypes"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp42_recovery_archetypes.png",
    dpi=300
)

plt.close()

print(
    f"Saved: {OUTDIR/'exp42_recovery_archetypes.png'}"
)


# --------------------------------------------------
# FUNNEL
# --------------------------------------------------

safe_count = 0
warning_count = 0
critical_count = 0
collapsed_count = 0

for pattern in archetypes:

    if "SAFE" in pattern:
        safe_count += 1

    if "WARNING" in pattern:
        warning_count += 1

    if "CRITICAL" in pattern:
        critical_count += 1

    if "COLLAPSED" in pattern:
        collapsed_count += 1

plt.figure(figsize=(8, 5))

plt.bar(
    [
        "SAFE",
        "WARNING",
        "CRITICAL",
        "COLLAPSED"
    ],
    [
        safe_count,
        warning_count,
        critical_count,
        collapsed_count
    ]
)

plt.title(
    "EXP_42 Recovery Funnel"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp42_recovery_funnel.png",
    dpi=300
)

plt.close()

print(
    f"Saved: {OUTDIR/'exp42_recovery_funnel.png'}"
)


# --------------------------------------------------
# REPORT
# --------------------------------------------------

report = []

report.append("")
report.append(
    "EXP_42 RECOVERY ARCHETYPE DISCOVERY"
)

report.append(
    "=" * 50
)

report.append("")
report.append(
    f"Runs Processed: {len(state_files)}"
)

report.append("")
report.append(
    f"Unique Archetypes: {len(arch_counter)}"
)

report.append("")

if len(arch_df):

    report.append(
        "Top Archetypes"
    )

    report.append(
        "--------------------"
    )

    for _, row in arch_df.head(10).iterrows():

        report.append(
            f"{row['archetype']} : {row['count']}"
        )

report.append("")
report.append(
    "Interpretation"
)
report.append(
    "--------------"
)
report.append(
    "EXP_42 searches for recurring recovery "
    "patterns inside historical warning-state "
    "dynamics."
)

report_path = (
    OUTDIR
    / "exp42_report.txt"
)

report_path.write_text(
    "\n".join(report)
)

print(f"Saved: {report_path}")

print("\nEXP_42 complete.")
