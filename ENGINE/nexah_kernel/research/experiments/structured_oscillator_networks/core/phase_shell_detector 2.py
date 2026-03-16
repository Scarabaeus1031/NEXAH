"""
NEXAH Experiment Tool
Phase Shell Detector

Detect regions of constant phase gradient (phase shells)
in hub–ring oscillator systems.

Outputs
-------
output/phase_gradient_map.png
output/shell_structure.png

Usage
-----
cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python phase_shell_detector.py
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
# Graph
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
# Phase gradient
# -----------------------------
def phase_gradients(theta_ring):

    N = len(theta_ring)

    grads = []

    for i in range(N):

        dphi = theta_ring[(i+1) % N] - theta_ring[i]

        dphi = np.arctan2(np.sin(dphi), np.cos(dphi))

        grads.append(dphi)

    return np.array(grads)


# -----------------------------
# Shell detection
# -----------------------------
def detect_shells(grads, threshold=0.2):

    shells = []

    current_shell = [0]

    for i in range(1, len(grads)):

        if abs(grads[i] - grads[i-1]) < threshold:

            current_shell.append(i)

        else:

            shells.append(current_shell)

            current_shell = [i]

    shells.append(current_shell)

    return shells


# -----------------------------
# Plot gradients
# -----------------------------
def plot_gradients(grads):

    plt.figure()

    plt.plot(grads)

    plt.xlabel("Ring index")

    plt.ylabel("Phase gradient")

    plt.title("Local phase gradients")

    Path("output").mkdir(exist_ok=True)

    plt.savefig("output/phase_gradient_map.png", dpi=300)

    plt.show()


# -----------------------------
# Plot shell structure
# -----------------------------
def plot_shells(grads, shells):

    colors = np.zeros(len(grads))

    for i, shell in enumerate(shells):

        for idx in shell:

            colors[idx] = i

    plt.figure()

    plt.scatter(range(len(grads)), grads, c=colors, cmap="tab20")

    plt.xlabel("Ring index")

    plt.ylabel("Phase gradient")

    plt.title("Detected phase shells")

    Path("output").mkdir(exist_ok=True)

    plt.savefig("output/shell_structure.png", dpi=300)

    plt.show()


# -----------------------------
# Main
# -----------------------------
def main():

    N = 60

    theta = simulate(N)

    ring_theta = theta[1:]

    grads = phase_gradients(ring_theta)

    shells = detect_shells(grads)

    print("Detected shells:", shells)

    plot_gradients(grads)

    plot_shells(grads, shells)


if __name__ == "__main__":

    main()
