"""
NEXAH Lorenz Regime Network

This script analyzes the Lorenz adapter on the regime level.

It builds:

1. a regime transition count matrix
2. a regime transition probability matrix
3. a regime-level network visualization

Artifacts are stored in:

APPLICATIONS/outputs/lorenz_network/

Outputs:
- lorenz_regime_transition_counts.csv
- lorenz_regime_transition_probabilities.csv
- lorenz_regime_network_report.txt
- lorenz_regime_network.png
"""

import os
import csv
import math
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

from APPLICATIONS.adapters.examples.lorenz_adapter import LorenzAdapter


# ---------------------------------------------------
# Output directory
# ---------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_network"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------
# Regime definitions
# ---------------------------------------------------

REGIMES = [
    "LEFT_ATTRACTOR",
    "TRANSITION",
    "RIGHT_ATTRACTOR",
    "ESCAPE",
]

REGIME_COLORS = {
    "LEFT_ATTRACTOR": "blue",
    "TRANSITION": "gold",
    "RIGHT_ATTRACTOR": "red",
    "ESCAPE": "black",
}


# ---------------------------------------------------
# Transition extraction
# ---------------------------------------------------

def extract_regime_sequence(adapter):
    """
    Convert sampled state sequence into regime sequence.
    """
    states = adapter.states()
    regime_map = adapter.regimes()

    return [regime_map[s] for s in states]


def build_transition_counts(regime_sequence):
    """
    Count transitions between consecutive regimes.
    """
    counts = {
        src: {dst: 0 for dst in REGIMES}
        for src in REGIMES
    }

    for i in range(len(regime_sequence) - 1):
        src = regime_sequence[i]
        dst = regime_sequence[i + 1]
        counts[src][dst] += 1

    return counts


def build_transition_probabilities(counts):
    """
    Normalize counts row-wise into probabilities.
    """
    probs = {}

    for src in REGIMES:
        total = sum(counts[src].values())
        probs[src] = {}

        for dst in REGIMES:
            if total > 0:
                probs[src][dst] = counts[src][dst] / total
            else:
                probs[src][dst] = 0.0

    return probs


# ---------------------------------------------------
# Saving utilities
# ---------------------------------------------------

def save_matrix_csv(matrix, filename, float_mode=False):
    """
    Save matrix dict-of-dicts as CSV.
    """
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["from"] + REGIMES)

        for src in REGIMES:
            row = [src]
            for dst in REGIMES:
                value = matrix[src][dst]
                if float_mode:
                    row.append(f"{value:.6f}")
                else:
                    row.append(value)
            writer.writerow(row)

    print("Saved:", path)


def save_report(regime_sequence, counts, probs):
    """
    Save text summary report.
    """
    path = os.path.join(OUTPUT_DIR, "lorenz_regime_network_report.txt")

    total_transitions = max(len(regime_sequence) - 1, 0)

    with open(path, "w") as f:
        f.write("NEXAH Lorenz Regime Network Report\n")
        f.write("=================================\n\n")

        f.write(f"Number of sampled regimes: {len(regime_sequence)}\n")
        f.write(f"Number of regime transitions: {total_transitions}\n\n")

        f.write("Regime counts:\n")
        for regime in REGIMES:
            c = regime_sequence.count(regime)
            f.write(f"  {regime}: {c}\n")

        f.write("\nTransition counts:\n")
        for src in REGIMES:
            for dst in REGIMES:
                if counts[src][dst] > 0:
                    f.write(f"  {src} -> {dst}: {counts[src][dst]}\n")

        f.write("\nTransition probabilities:\n")
        for src in REGIMES:
            for dst in REGIMES:
                if probs[src][dst] > 0:
                    f.write(f"  {src} -> {dst}: {probs[src][dst]:.4f}\n")

    print("Saved:", path)


# ---------------------------------------------------
# Visualization
# ---------------------------------------------------

def draw_arrow(ax, start, end, weight, label, is_loop=False):
    """
    Draw weighted directed arrow between two node positions.
    """
    if weight <= 0:
        return

    x1, y1 = start
    x2, y2 = end

    if is_loop:
        loop = FancyArrowPatch(
            (x1, y1),
            (x1 + 0.001, y1 + 0.001),
            connectionstyle="arc3,rad=1.6",
            arrowstyle="-|>",
            mutation_scale=12 + 20 * weight,
            linewidth=1 + 6 * weight,
        )
        ax.add_patch(loop)
        ax.text(x1 + 0.1, y1 + 0.18, label, fontsize=9)
        return

    arrow = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        connectionstyle="arc3,rad=0.15",
        arrowstyle="-|>",
        mutation_scale=12 + 20 * weight,
        linewidth=1 + 6 * weight,
    )
    ax.add_patch(arrow)

    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    ax.text(mx, my, label, fontsize=9)


def plot_regime_network(probs):
    """
    Draw regime-level network with edge thickness proportional
    to transition probability.
    """
    positions = {
        "LEFT_ATTRACTOR": (-1.2, 0.0),
        "TRANSITION": (0.0, 0.0),
        "RIGHT_ATTRACTOR": (1.2, 0.0),
        "ESCAPE": (0.0, 1.0),
    }

    plt.figure(figsize=(10, 6))
    ax = plt.gca()

    # Draw nodes
    for regime, (x, y) in positions.items():
        ax.scatter(
            x,
            y,
            s=1400,
            color=REGIME_COLORS[regime],
            edgecolors="black",
            zorder=3,
        )
        ax.text(
            x,
            y,
            regime,
            ha="center",
            va="center",
            fontsize=10,
            color="white" if regime in ["LEFT_ATTRACTOR", "RIGHT_ATTRACTOR", "ESCAPE"] else "black",
            zorder=4,
        )

    # Draw edges
    for src in REGIMES:
        for dst in REGIMES:
            p = probs[src][dst]

            # Only show meaningful transitions
            if p < 0.03:
                continue

            label = f"{p:.2f}"

            draw_arrow(
                ax=ax,
                start=positions[src],
                end=positions[dst],
                weight=p,
                label=label,
                is_loop=(src == dst),
            )

    ax.set_title("Lorenz Regime Network")
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-1.0, 1.8)
    ax.axis("off")

    path = os.path.join(OUTPUT_DIR, "lorenz_regime_network.png")
    plt.savefig(path, dpi=220, bbox_inches="tight")
    print("Saved:", path)

    plt.show()
    plt.close()


# ---------------------------------------------------
# Console summary
# ---------------------------------------------------

def print_summary(regime_sequence, counts, probs):
    """
    Print compact terminal summary.
    """
    print("\n==============================")
    print("NEXAH LORENZ REGIME NETWORK")
    print("==============================\n")

    print("Regime counts:")
    for regime in REGIMES:
        print(f"  {regime}: {regime_sequence.count(regime)}")

    print("\nTransition counts:")
    for src in REGIMES:
        for dst in REGIMES:
            if counts[src][dst] > 0:
                print(f"  {src} -> {dst}: {counts[src][dst]}")

    print("\nTransition probabilities:")
    for src in REGIMES:
        for dst in REGIMES:
            if probs[src][dst] > 0:
                print(f"  {src} -> {dst}: {probs[src][dst]:.3f}")


# ---------------------------------------------------
# Main pipeline
# ---------------------------------------------------

def main():
    adapter = LorenzAdapter()

    regime_sequence = extract_regime_sequence(adapter)
    counts = build_transition_counts(regime_sequence)
    probs = build_transition_probabilities(counts)

    print_summary(regime_sequence, counts, probs)

    save_matrix_csv(
        counts,
        "lorenz_regime_transition_counts.csv",
        float_mode=False,
    )

    save_matrix_csv(
        probs,
        "lorenz_regime_transition_probabilities.csv",
        float_mode=True,
    )

    save_report(regime_sequence, counts, probs)
    plot_regime_network(probs)

    print("\nLorenz regime network pipeline finished.\n")


if __name__ == "__main__":
    main()
