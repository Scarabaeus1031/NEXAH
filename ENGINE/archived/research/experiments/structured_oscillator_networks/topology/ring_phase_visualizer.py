"""
NEXAH Experiment Tool
Ring Phase Visualizer

Purpose
-------
Visualize oscillator phases on a hub–ring network after Kuramoto dynamics.

This tool helps identify:

• phase gradients
• vortex structures
• synchronization clusters
• frustration patterns

Network topology
----------------
1 center node
N ring oscillators

Outputs
-------
output/ring_phase_visualization.png

Usage
-----
Run from experiment directory:

python ring_phase_visualizer.py
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
def simulate(N=60, steps=4000, dt=0.02, K=1.0):

    G = build_hub_ring(N)

    A = nx.to_numpy_array(G)

    nodes = len(A)

    theta = np.random.uniform(0, 2*np.pi, nodes)

    omega = np.random.normal(0, 0.1, nodes)

    for _ in range(steps):

        theta = kuramoto_step(theta, omega, A, K, dt)

    return theta


# -----------------------------
# Phase visualization
# -----------------------------
def plot_ring(theta):

    ring_theta = theta[1:]

    N = len(ring_theta)

    angles = np.linspace(0, 2*np.pi, N, endpoint=False)

    x = np.cos(angles)
    y = np.sin(angles)

    colors = (ring_theta % (2*np.pi)) / (2*np.pi)

    plt.figure(figsize=(6, 6))

    plt.scatter(x, y, c=colors, cmap="hsv", s=150)

    for i in range(N):

        plt.text(x[i]*1.15, y[i]*1.15, str(i+1), fontsize=8)

    plt.gca().set_aspect("equal")

    plt.title("Ring Phase Configuration")

    plt.axis("off")

    # create output folder
    Path("output").mkdir(exist_ok=True)

    plt.savefig("output/ring_phase_visualization.png", dpi=300)

    plt.show()


# -----------------------------
# Main
# -----------------------------
def main():

    N = 60

    theta = simulate(N)

    plot_ring(theta)

    print("Visualization saved to output/ring_phase_visualization.png")


if __name__ == "__main__":
    main()
