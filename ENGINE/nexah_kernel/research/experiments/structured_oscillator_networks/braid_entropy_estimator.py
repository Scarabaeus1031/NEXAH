"""
NEXAH Experiment Tool
Braid Entropy Estimator

Purpose
-------
Estimate topological complexity of braid worldlines
produced by phase defects.

We approximate braid entropy using crossing growth.

h ≈ log(C + 1) / T

where

    C = number of braid crossings
    T = total simulation time

Inputs
------
output/braid_crossings.npy
output/defect_worldlines.npy

Outputs
-------
output/braid_entropy_report.txt
output/braid_crossing_growth.png
output/braid_entropy_estimate.png

Usage
-----
cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python braid_entropy_estimator.py
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ------------------------------------------------
# Load data
# ------------------------------------------------

def load_data():

    crossings = np.load("output/braid_crossings.npy")
    worldlines = np.load("output/defect_worldlines.npy")

    return crossings, worldlines


# ------------------------------------------------
# Estimate entropy
# ------------------------------------------------

def estimate_entropy(crossings, worldlines):

    T = worldlines.shape[0]

    C = len(crossings)

    entropy = np.log(C + 1) / T

    return entropy, C, T


# ------------------------------------------------
# Crossing growth curve
# ------------------------------------------------

def crossing_growth(crossings, T):

    growth = np.zeros(T)

    for c in crossings:

        t = int(c[0])

        if t < T:
            growth[t:] += 1

    return growth


# ------------------------------------------------
# Plot results
# ------------------------------------------------

def plot_results(growth, entropy):

    fig, ax = plt.subplots(2, 1, figsize=(8, 8))

    ax[0].plot(growth)
    ax[0].set_title("Braid crossing accumulation")
    ax[0].set_xlabel("time step")
    ax[0].set_ylabel("crossings")

    ax[1].bar([0], [entropy])
    ax[1].set_title("Estimated braid entropy")
    ax[1].set_ylabel("h_braid")

    plt.tight_layout()

    Path("output").mkdir(exist_ok=True)

    plt.savefig("output/braid_entropy_estimate.png")

    plt.close()


# ------------------------------------------------
# Save report
# ------------------------------------------------

def save_report(entropy, C, T):

    text = f"""
Braid Entropy Estimate
----------------------

Total crossings: {C}
Simulation length: {T}

Estimated braid entropy:

h_braid ≈ {entropy:.6f}

Interpretation:

h ≈ 0       → laminar structure
h small     → weakly chaotic
h moderate  → braid turbulence
h large     → strong mixing
"""

    with open("output/braid_entropy_report.txt", "w") as f:
        f.write(text)


# ------------------------------------------------
# Main
# ------------------------------------------------

def main():

    crossings, worldlines = load_data()

    entropy, C, T = estimate_entropy(crossings, worldlines)

    growth = crossing_growth(crossings, T)

    plot_results(growth, entropy)

    save_report(entropy, C, T)

    print("Braid entropy:", entropy)
    print("Total crossings:", C)


if __name__ == "__main__":
    main()
