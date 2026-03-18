"""
NEXAH Experiment Tool
Phase Mode Map

Purpose
-------
Measure the dominant phase-winding mode (k) of a hub–ring oscillator system
for different shell sizes.

This identifies which topological phase-wave state the system settles into.

Outputs
-------
output/phase_mode_vs_shell.png
output/example_phase_ring.png

Usage
-----
cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python phase_mode_map.py
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

    for i in range(1, N+1):
        G.add_edge(center, i)

    for i in range(1, N+1):
        G.add_edge(i, 1 + (i % N))

    return G


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
# Winding number
# -----------------------------
def winding_number(theta_ring):

    N = len(theta_ring)

    total = 0

    for i in range(N):

        dphi = theta_ring[(i+1) % N] - theta_ring[i]

        dphi = np.arctan2(np.sin(dphi), np.cos(dphi))

        total += dphi

    k = total / (2*np.pi)

    return int(np.round(k))


# -----------------------------
# Shell scan
# -----------------------------
def shell_scan():

    shell_sizes = list(range(8,120))

    modes = []

    example_theta = None

    for N in shell_sizes:

        print(f"Running shell size {N}")

        theta = simulate(N)

        ring_theta = theta[1:]

        k = winding_number(ring_theta)

        modes.append(k)

        if N == 60:
            example_theta = ring_theta

    return shell_sizes, modes, example_theta


# -----------------------------
# Plot mode map
# -----------------------------
def plot_modes(shell_sizes, modes):

    plt.figure()

    plt.plot(shell_sizes, modes, marker="o")

    plt.xlabel("Shell size N")
    plt.ylabel("Phase winding mode k")

    plt.title("Topological phase mode vs shell size")

    Path("output").mkdir(exist_ok=True)

    plt.savefig("output/phase_mode_vs_shell.png", dpi=300)

    plt.show()


# -----------------------------
# Plot example ring
# -----------------------------
def plot_ring(theta):

    N = len(theta)

    angles = np.linspace(0, 2*np.pi, N, endpoint=False)

    x = np.cos(angles)
    y = np.sin(angles)

    colors = (theta % (2*np.pi)) / (2*np.pi)

    plt.figure(figsize=(6,6))

    plt.scatter(x, y, c=colors, cmap="hsv", s=150)

    plt.axis("off")

    plt.title("Example Phase Ring")

    Path("output").mkdir(exist_ok=True)

    plt.savefig("output/example_phase_ring.png", dpi=300)

    plt.show()


# -----------------------------
# Main
# -----------------------------
def main():

    shell_sizes, modes, example_theta = shell_scan()

    plot_modes(shell_sizes, modes)

    if example_theta is not None:
        plot_ring(example_theta)

    print("Phase mode mapping completed")


if __name__ == "__main__":
    main()
