from pathlib import Path
from collections import Counter, defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# --------------------------------------------------
# Paths
# --------------------------------------------------

ROOT = Path(__file__).resolve()

repo_root = None
for p in ROOT.parents:
    if p.name == "power_systems":
        repo_root = p
        break

if repo_root is None:
    raise RuntimeError("Could not locate power_systems root.")

OUTPUT_DIR = (
    repo_root
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_43_STATE_OSCILLATION_DISCOVERY"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Repository -> {repo_root}")
print(f"Output     -> {OUTPUT_DIR}")

# --------------------------------------------------
# Locate state files
# --------------------------------------------------

state_files = list(repo_root.rglob("states.txt"))

print(f"\nState files discovered: {len(state_files)}")

if len(state_files) == 0:
    raise RuntimeError("No states.txt files found.")

# --------------------------------------------------
# Analysis
# --------------------------------------------------

oscillation_counter = Counter()
loop_lengths = []
transition_counter = Counter()

G = nx.DiGraph()

for file in state_files:

    try:
        states = [
            x.strip().upper()
            for x in open(file).read().splitlines()
            if x.strip()
        ]

    except Exception:
        continue

    if len(states) < 2:
        continue

    # ------------------------------------------
    # transitions
    # ------------------------------------------

    for a, b in zip(states[:-1], states[1:]):

        transition_counter[(a, b)] += 1

        if G.has_edge(a, b):
            G[a][b]["weight"] += 1
        else:
            G.add_edge(a, b, weight=1)

    # ------------------------------------------
    # oscillations
    # A -> B -> A
    # ------------------------------------------

    for i in range(len(states) - 2):

        a = states[i]
        b = states[i + 1]
        c = states[i + 2]

        if a == c and a != b:

            key = f"{a} ↔ {b}"

            oscillation_counter[key] += 1

    # ------------------------------------------
    # longer loops
    # A ... A
    # ------------------------------------------

    for i in range(len(states)):

        for j in range(i + 2, min(i + 20, len(states))):

            if states[i] == states[j]:

                loop_lengths.append(j - i)

# --------------------------------------------------
# Save oscillations
# --------------------------------------------------

osc_df = pd.DataFrame(
    oscillation_counter.items(),
    columns=["oscillation", "count"]
).sort_values("count", ascending=False)

osc_df.to_csv(
    OUTPUT_DIR / "exp43_oscillation_counts.csv",
    index=False
)

print(
    f"Saved: {OUTPUT_DIR/'exp43_oscillation_counts.csv'}"
)

# --------------------------------------------------
# Loop lengths
# --------------------------------------------------

loop_df = pd.DataFrame(
    {"loop_length": loop_lengths}
)

loop_df.to_csv(
    OUTPUT_DIR / "exp43_loop_lengths.csv",
    index=False
)

print(
    f"Saved: {OUTPUT_DIR/'exp43_loop_lengths.csv'}"
)

# --------------------------------------------------
# Oscillation Frequency
# --------------------------------------------------

plt.figure(figsize=(10,5))

osc_df.head(10).plot(
    x="oscillation",
    y="count",
    kind="bar",
    legend=False
)

plt.title("EXP_43 Oscillation Frequencies")
plt.ylabel("Count")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp43_oscillation_frequency.png"
)

plt.close()

print(
    f"Saved: {OUTPUT_DIR/'exp43_oscillation_frequency.png'}"
)

# --------------------------------------------------
# Loop Length Histogram
# --------------------------------------------------

plt.figure(figsize=(8,5))

plt.hist(loop_lengths, bins=15)

plt.title("EXP_43 Loop Length Distribution")
plt.xlabel("Loop Length")
plt.ylabel("Count")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp43_loop_length_distribution.png"
)

plt.close()

print(
    f"Saved: {OUTPUT_DIR/'exp43_loop_length_distribution.png'}"
)

# --------------------------------------------------
# Oscillation Network
# --------------------------------------------------

plt.figure(figsize=(10,8))

pos = nx.spring_layout(
    G,
    seed=42
)

weights = [
    G[u][v]["weight"] * 0.03
    for u, v in G.edges()
]

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=3500
)

nx.draw_networkx_labels(
    G,
    pos,
    font_size=14
)

nx.draw_networkx_edges(
    G,
    pos,
    width=weights,
    arrows=True
)

plt.title("EXP_43 State Oscillation Network")

plt.axis("off")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp43_state_oscillation_network.png"
)

plt.close()

print(
    f"Saved: {OUTPUT_DIR/'exp43_state_oscillation_network.png'}"
)

# --------------------------------------------------
# Report
# --------------------------------------------------

with open(
    OUTPUT_DIR / "exp43_report.txt",
    "w"
) as f:

    f.write(
        "EXP_43 STATE OSCILLATION DISCOVERY\n"
    )

    f.write(
        "=========================================\n\n"
    )

    f.write(
        f"Runs Processed: {len(state_files)}\n\n"
    )

    f.write(
        f"Unique Oscillations: {len(oscillation_counter)}\n\n"
    )

    f.write(
        "Top Oscillations\n"
    )

    f.write(
        "-------------------------\n"
    )

    for k, v in oscillation_counter.most_common(10):

        f.write(
            f"{k}: {v}\n"
        )

    if loop_lengths:

        f.write(
            "\nLoop Statistics\n"
        )

        f.write(
            "-------------------------\n"
        )

        f.write(
            f"Mean Length: {sum(loop_lengths)/len(loop_lengths):.2f}\n"
        )

        f.write(
            f"Max Length: {max(loop_lengths)}\n"
        )

    f.write(
        "\nInterpretation\n"
    )

    f.write(
        "EXP_43 searches for recurrent oscillatory "
        "behavior inside historical warning-state "
        "dynamics.\n"
    )

print(
    f"Saved: {OUTPUT_DIR/'exp43_report.txt'}"
)

print("\nEXP_43 complete.")
