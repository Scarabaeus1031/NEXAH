# ⚡ NEXAH — Mass Conservation Test (Halvorsen)
# ------------------------------------------------------------
# This script demonstrates the transition from inconsistent
# transition weights to a mass-conserving, closed system.
#
# Purpose:
# - enforce ΣP = 1
# - validate transition consistency
# - prepare for NEXAH control layer integration
#
# Output:
# - .txt report (raw vs normalized)
# - .png visualization (bar chart comparison)
#
# Location:
# APPLICATIONS/dynamical_systems/halvorsen/outputs/
# ------------------------------------------------------------

import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt


# -----------------------------
# Example raw transitions
# -----------------------------

raw_transitions = {
    "B1": {"B2": 0.6, "B3": 0.7, "B4": 0.3}
}


# -----------------------------
# Normalize transitions
# -----------------------------

def normalize_transitions(transitions):
    normalized = {}

    for state, edges in transitions.items():
        total = sum(edges.values())

        if total == 0:
            raise ValueError(f"No outgoing transitions from {state}")

        normalized[state] = {
            target: value / total
            for target, value in edges.items()
        }

    return normalized


# -----------------------------
# Check mass conservation
# -----------------------------

def check_mass(transitions):
    results = {}

    for state, edges in transitions.items():
        total = sum(edges.values())
        results[state] = total

    return results


# -----------------------------
# Save TXT report
# -----------------------------

def save_txt(raw, normalized, raw_check, norm_check, base_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(base_dir, f"mass_conservation_{timestamp}.txt")

    with open(filepath, "w") as f:
        f.write("NEXAH — Mass Conservation Report\n")
        f.write("="*50 + "\n\n")

        f.write("RAW TRANSITIONS:\n")
        for k, v in raw.items():
            f.write(f"{k} -> {v}\n")

        f.write("\nRAW SUMS:\n")
        for k, v in raw_check.items():
            f.write(f"{k}: {v:.6f}\n")

        f.write("\nNORMALIZED TRANSITIONS:\n")
        for k, v in normalized.items():
            f.write(f"{k} -> {v}\n")

        f.write("\nNORMALIZED SUMS:\n")
        for k, v in norm_check.items():
            f.write(f"{k}: {v:.6f}\n")

    print(f"[✓] TXT saved: {filepath}")


# -----------------------------
# Save PNG visualization
# -----------------------------

def save_plot(raw, normalized, base_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(base_dir, f"mass_conservation_{timestamp}.png")

    state = list(raw.keys())[0]

    raw_vals = list(raw[state].values())
    norm_vals = list(normalized[state].values())
    labels = list(raw[state].keys())

    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(6,4))

    ax.bar(x - 0.15, raw_vals, width=0.3, label="Raw")
    ax.bar(x + 0.15, norm_vals, width=0.3, label="Normalized")

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Mass Conservation: Raw vs Normalized")
    ax.legend()

    plt.tight_layout()
    fig.savefig(filepath, dpi=300)

    print(f"[✓] PNG saved: {filepath}")


# -----------------------------
# Run
# -----------------------------

if __name__ == "__main__":

    # output directory
    base_dir = os.path.join(
        "APPLICATIONS",
        "dynamical_systems",
        "halvorsen",
        "outputs"
    )
    os.makedirs(base_dir, exist_ok=True)

    # compute
    normalized = normalize_transitions(raw_transitions)

    raw_check = check_mass(raw_transitions)
    norm_check = check_mass(normalized)

    # print console
    print("\n--- RAW ---")
    print(raw_check)

    print("\n--- NORMALIZED ---")
    print(norm_check)

    print("\nTransitions:")
    print(normalized)

    # save outputs
    save_txt(raw_transitions, normalized, raw_check, norm_check, base_dir)
    save_plot(raw_transitions, normalized, base_dir)
