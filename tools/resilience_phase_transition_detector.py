# tools/resilience_phase_transition_detector.py

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_landscape import compute_landscape, SYSTEM_PATH


# -----------------------------
# phase transition detection
# -----------------------------

def detect_transitions(densities, noise_levels, landscape):

    transitions = []

    for i in range(len(noise_levels)):

        row = landscape[i]

        gradient = np.gradient(row)

        for j in range(1, len(gradient)):

            if abs(gradient[j] - gradient[j-1]) > 0.08:

                transitions.append({
                    "noise": noise_levels[i],
                    "density": densities[j],
                    "score": row[j]
                })

    return transitions


# -----------------------------
# optimal region detection
# -----------------------------

def find_optimal_region(densities, noise_levels, landscape):

    idx = np.unravel_index(np.argmax(landscape), landscape.shape)

    return {
        "noise": noise_levels[idx[0]],
        "density": densities[idx[1]],
        "score": landscape[idx]
    }


# -----------------------------
# visualization
# -----------------------------

def visualize_transitions(densities, noise_levels, landscape, transitions):

    plt.figure(figsize=(8,6))

    plt.imshow(
        landscape,
        origin="lower",
        aspect="auto",
        extent=[
            densities[0],
            densities[-1],
            noise_levels[0],
            noise_levels[-1]
        ]
    )

    plt.colorbar(label="Resilience Score")

    for t in transitions:

        plt.scatter(
            t["density"],
            t["noise"],
            color="red",
            s=30
        )

    plt.xlabel("Edge Density")
    plt.ylabel("Noise Level")

    plt.title("Phase Transitions in Resilience Landscape")

    plt.show()


# -----------------------------
# main
# -----------------------------

if __name__ == "__main__":

    densities, noise_levels, landscape = compute_landscape(SYSTEM_PATH)

    transitions = detect_transitions(densities, noise_levels, landscape)

    optimal = find_optimal_region(densities, noise_levels, landscape)

    print("\nDetected Phase Transitions:\n")

    for t in transitions:
        print(
            f"noise={t['noise']:.2f} density={t['density']:.2f} score={t['score']:.3f}"
        )

    print("\nOptimal Architecture:\n")

    print(
        f"density={optimal['density']:.2f} noise={optimal['noise']:.2f} score={optimal['score']:.3f}"
    )

    visualize_transitions(densities, noise_levels, landscape, transitions)
