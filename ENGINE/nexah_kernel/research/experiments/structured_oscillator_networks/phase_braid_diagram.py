"""
NEXAH Experiment Tool
Phase Braid Diagram

Visualizes phase evolution of the hub-ring oscillator network.

Two visualizations:
1. Space-time braid diagram (node index vs time)
2. Phase wheel evolution (calendar-like radial cycles)

Outputs
-------
output/phase_braid_diagram.png
output/phase_wheel_cycles.png

Usage
-----
cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python phase_braid_diagram.py
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path


# -----------------------------
# Kuramoto step
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
# Simulation with history
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
# Braid diagram
# -----------------------------
def plot_braid(history):

    ring = history[:,1:]  # remove hub

    phase_colors = (ring % (2*np.pi)) / (2*np.pi)

    plt.figure(figsize=(10,5))

    plt.imshow(
        phase_colors,
        aspect="auto",
        cmap="hsv",
        origin="lower"
    )

    plt.xlabel("Ring index")
    plt.ylabel("Time")

    plt.title("Phase braid diagram")

    Path("output").mkdir(exist_ok=True)

    plt.savefig("output/phase_braid_diagram.png", dpi=300)

    plt.show()


# -----------------------------
# Phase wheel cycles
# -----------------------------
def plot_phase_wheel(history, frames=12):

    Path("output").mkdir(exist_ok=True)

    N = history.shape[1] - 1

    angles = np.linspace(0,2*np.pi,N,endpoint=False)

    x = np.cos(angles)
    y = np.sin(angles)

    plt.figure(figsize=(8,8))

    step = len(history)//frames

    for i in range(frames):

        theta = history[i*step,1:]

        colors = (theta % (2*np.pi))/(2*np.pi)

        r = 1 + i*0.15

        plt.scatter(
            r*x,
            r*y,
            c=colors,
            cmap="hsv",
            s=60
        )

    plt.axis("off")

    plt.title("Phase wheel cycles")

    plt.savefig("output/phase_wheel_cycles.png", dpi=300)

    plt.show()


# -----------------------------
# Main
# -----------------------------
def main():

    N = 60

    history = simulate_history(N)

    plot_braid(history)

    plot_phase_wheel(history)

    print("Phase braid visualization completed")


if __name__ == "__main__":
    main()
