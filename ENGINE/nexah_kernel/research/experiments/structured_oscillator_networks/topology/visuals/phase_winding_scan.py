"""
NEXAH Experiment Tool
Phase Winding Scan

Purpose
-------
Measure phase winding number in hub–ring oscillator networks.

The winding number detects topological phase waves:

k = (1 / 2π) Σ_i (θ_{i+1} - θ_i)

k = 0  → synchronization
k = ±1 → single phase wave
k = ±2 → double wave
etc.

Outputs
-------
output/winding_vs_shell.png
output/example_ring_phases.png

Usage
-----

cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python phase_winding_scan.py
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
# Winding number
# -----------------------------
def winding_number(theta_ring):

    N = len(theta_ring)

    total = 0

    for i in range(N):

        dphi = theta_ring[(i+1) % N] - theta_ring[i]

        dphi = np.arctan2(np.sin(dphi), np.cos(dphi))

        total += dphi

    return total / (2*np.pi)


# -----------------------------
# Simulation
# -----------------------------
def simulate(N, steps=4000, dt=0.02, K=1.0):

    G = build_hub_ring(N)
    A = nx.to_numpy_array(G)

    nodes = len(A)

    theta = np.random.uniform(0, 2*np.pi, nodes)
    omega = np.random.normal(0, 0.1, nodes)

    for _ in range(steps):

        theta = kuramoto_step(theta, omega, A, K, dt)

    return theta


# -----------------------------
# Shell scan
# -----------------------------
def shell_scan():

    shell_sizes = list(range(8, 120))

    windings = []

    example_theta = None

    for N in shell_sizes:

        print(f"Running shell size {N}")

        theta = simulate(N)

        ring_theta = theta[1:]

        k = winding_number(ring_theta)

        windings.append(k)

        if N == 60:
            example_theta = ring_theta

    return shell_sizes, windings, example_theta


# -----------------------------
# Ring visualization
# -----------------------------
def plot_ring(theta):

    N = len(theta)

    angles = np.linspace(0, 2*np.pi, N, endpoint=False)

    x = np.cos(angles)
    y = np.sin(angles)

    colors = (theta % (2*np.pi)) / (2*np.pi)

    plt.figure(figsize=(6,6))

    plt.scatter(x, y, c=colors, cmap="hsv", s=150)

    plt.title("Example Ring Phase State")

    plt.axis("off")

    Path("output").mkdir(exist_ok=True)

    plt.savefig("output/example_ring_phases.png", dpi=300)

    plt.show()


# -----------------------------
# Plot winding scan
# -----------------------------
def plot_results(shell_sizes, windings):

    Path("output").mkdir(exist_ok=True)

    plt.figure()

    plt.plot(shell_sizes, windings)

    plt.xlabel("Shell Size N")
    plt.ylabel("Winding Number k")

    plt.title("Phase Winding vs Shell Size")

    plt.savefig("output/winding_vs_shell.png", dpi=300)

    plt.show()


# -----------------------------
# Main
# -----------------------------
def main():

    shell_sizes, windings, example_theta = shell_scan()

    plot_results(shell_sizes, windings)

    if example_theta is not None:
        plot_ring(example_theta)

    print("Phase winding scan completed")


if __name__ == "__main__":
    main()
