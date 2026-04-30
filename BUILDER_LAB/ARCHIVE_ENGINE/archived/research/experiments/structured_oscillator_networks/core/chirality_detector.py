"""
NEXAH Experiment Tool
Chirality Detector

Purpose
-------
Detect left/right chiral rotation states in a ring oscillator network.

This tool measures the global chirality of the phase field:

    C = sum_i sin(theta_{i+1} - theta_i)

Interpretation:

C > 0  → left-handed rotation
C < 0  → right-handed rotation
C ≈ 0  → symmetric / mixed / chimera

It also detects flip events where the system switches chirality.

Outputs
-------
output/chirality_vs_time.png
output/chirality_histogram.png
output/chirality_flip_events.png

Usage
-----
cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python chirality_detector.py
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path


# -----------------------------
# Kuramoto dynamics
# -----------------------------

def kuramoto_step(theta, omega, A, K, dt):

    phase_diff = theta[:, None] - theta[None, :]
    coupling = np.sum(A * np.sin(-phase_diff), axis=1)

    dtheta = omega + (K / len(theta)) * coupling

    return theta + dt * dtheta


# -----------------------------
# Hub + Ring Graph
# -----------------------------

def build_hub_ring(N):

    G = nx.Graph()

    center = 0

    for i in range(1, N + 1):
        G.add_edge(center, i)

    for i in range(1, N + 1):
        G.add_edge(i, 1 + (i % N))

    return G


# -----------------------------
# Simulation
# -----------------------------

def simulate_history(N, steps=1500, dt=0.02, K=1.0):

    G = build_hub_ring(N)
    A = nx.to_numpy_array(G)

    nodes = len(A)

    theta = np.random.uniform(0, 2*np.pi, nodes)
    omega = np.random.normal(0, 0.1, nodes)

    history = []

    for _ in range(steps):
        theta = kuramoto_step(theta, omega, A, K, dt)
        history.append(theta.copy())

    return np.array(history)


# -----------------------------
# Chirality
# -----------------------------

def compute_chirality(theta_ring):

    diffs = np.roll(theta_ring, -1) - theta_ring

    return np.sum(np.sin(diffs))


# -----------------------------
# Chirality over time
# -----------------------------

def chirality_timeseries(history):

    ring_history = history[:, 1:]

    C = []

    for theta in ring_history:
        C.append(compute_chirality(theta))

    return np.array(C)


# -----------------------------
# Flip detection
# -----------------------------

def detect_flips(C):

    flips = []

    for i in range(1, len(C)):

        if C[i-1] * C[i] < 0:
            flips.append(i)

    return flips


# -----------------------------
# Plot chirality vs time
# -----------------------------

def plot_chirality(C):

    Path("output").mkdir(exist_ok=True)

    plt.figure(figsize=(10,4))

    plt.plot(C)

    plt.axhline(0, linestyle="--")

    plt.title("Chirality vs time")
    plt.xlabel("Time step")
    plt.ylabel("Chirality")

    plt.savefig("output/chirality_vs_time.png", dpi=300)

    plt.show()


# -----------------------------
# Histogram
# -----------------------------

def plot_histogram(C):

    plt.figure(figsize=(6,4))

    plt.hist(C, bins=40)

    plt.title("Chirality distribution")
    plt.xlabel("C value")
    plt.ylabel("count")

    plt.savefig("output/chirality_histogram.png", dpi=300)

    plt.show()


# -----------------------------
# Flip plot
# -----------------------------

def plot_flips(C, flips):

    plt.figure(figsize=(10,4))

    plt.plot(C)

    for f in flips:
        plt.axvline(f, color="red", alpha=0.4)

    plt.axhline(0, linestyle="--")

    plt.title("Chirality flip events")
    plt.xlabel("Time step")
    plt.ylabel("Chirality")

    plt.savefig("output/chirality_flip_events.png", dpi=300)

    plt.show()


# -----------------------------
# Main
# -----------------------------

def main():

    N = 60
    steps = 1500

    history = simulate_history(N, steps)

    C = chirality_timeseries(history)

    flips = detect_flips(C)

    print("Detected flips:", len(flips))

    plot_chirality(C)
    plot_histogram(C)
    plot_flips(C, flips)


if __name__ == "__main__":
    main()
