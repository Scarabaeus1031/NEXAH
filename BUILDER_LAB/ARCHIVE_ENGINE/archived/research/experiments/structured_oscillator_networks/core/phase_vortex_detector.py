"""
NEXAH Experiment Tool
Phase Vortex Detector

Purpose
-------
Detect local phase defects / vortex-like slip events in a hub-ring oscillator network.

This tool identifies ring positions where the local phase jump is unusually large,
which often corresponds to:

• phase slips
• defect cores
• braid onset regions
• chirality transition precursors

Outputs
-------
output/vortex_defect_map.png
output/vortex_count_vs_time.png
output/vortex_example_snapshot.png

Usage
-----
cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python phase_vortex_detector.py
"""

"""
NEXAH Experiment Tool
Phase Vortex Detector
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
# Graph generator
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
def simulate_history(N, steps=1200, dt=0.02, K=1.0):

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
# Phase difference (wrapped)
# -----------------------------
def phase_diff_ring(theta_ring):

    diffs = np.roll(theta_ring, -1) - theta_ring
    diffs = (diffs + np.pi) % (2*np.pi) - np.pi

    return diffs


# -----------------------------
# Vortex detection
# -----------------------------
def detect_vortex_defects(theta_ring, threshold=2.2):

    diffs = phase_diff_ring(theta_ring)

    defects = np.where(np.abs(diffs) > threshold)[0]

    return defects, diffs


# -----------------------------
# Scan simulation
# -----------------------------
def vortex_scan(history, threshold=2.2):

    ring_history = history[:, 1:]

    defect_map = []
    defect_counts = []

    for theta in ring_history:

        defects, diffs = detect_vortex_defects(theta, threshold)

        row = np.zeros(len(theta))

        row[defects] = 1

        defect_map.append(row)
        defect_counts.append(len(defects))

    return np.array(defect_map), np.array(defect_counts)


# -----------------------------
# Plot defect map
# -----------------------------
def plot_defect_map(defect_map):

    Path("output").mkdir(exist_ok=True)

    plt.figure(figsize=(10,5))

    plt.imshow(
        defect_map.T,
        aspect="auto",
        origin="lower",
        cmap="inferno"
    )

    plt.xlabel("time step")
    plt.ylabel("ring index")
    plt.title("Phase vortex defect map")

    plt.colorbar(label="defect")

    plt.savefig("output/vortex_defect_map.png", dpi=300)
    plt.show()


# -----------------------------
# Plot defect counts
# -----------------------------
def plot_vortex_counts(defect_counts):

    plt.figure(figsize=(10,4))

    plt.plot(defect_counts)

    plt.xlabel("time step")
    plt.ylabel("defect count")
    plt.title("Number of vortex defects over time")

    plt.savefig("output/vortex_count_vs_time.png", dpi=300)
    plt.show()


# -----------------------------
# Snapshot
# -----------------------------
def plot_example_snapshot(history, threshold=2.2, t_index=600):

    theta_ring = history[t_index,1:]

    defects, diffs = detect_vortex_defects(theta_ring, threshold)

    N = len(theta_ring)

    angles = np.linspace(0,2*np.pi,N,endpoint=False)

    x = np.cos(angles)
    y = np.sin(angles)

    plt.figure(figsize=(6,6))

    plt.scatter(x,y,c=theta_ring,cmap="hsv",s=80)

    if len(defects)>0:
        plt.scatter(x[defects],y[defects],c="black",s=140)

    plt.title(f"Phase vortex snapshot t={t_index}")

    plt.axis("equal")
    plt.axis("off")

    plt.savefig("output/vortex_example_snapshot.png", dpi=300)
    plt.show()


# -----------------------------
# Main
# -----------------------------
def main():

    N = 60
    steps = 1200

    history = simulate_history(N, steps)

    defect_map, defect_counts = vortex_scan(history)

    Path("output").mkdir(exist_ok=True)

    np.save("output/defect_map.npy", defect_map)

    plot_defect_map(defect_map)
    plot_vortex_counts(defect_counts)
    plot_example_snapshot(history)

    print("Phase vortex analysis completed.")
    print("Saved: output/defect_map.npy")


if __name__ == "__main__":
    main()
