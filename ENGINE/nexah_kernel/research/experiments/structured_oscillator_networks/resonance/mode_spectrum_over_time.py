"""
NEXAH Experiment Tool
Mode Spectrum Over Time

Purpose
-------
Analyze the dominant Fourier mode of a hub–ring oscillator network over time.

This tool computes the spatial mode spectrum of the ring phase field
for each simulation step.

It helps reveal:

• dominant winding / wave modes
• mode switching events
• transitions between coherent and drifting phase structures

Outputs
-------
output/mode_spectrum_over_time.png
output/dominant_mode_over_time.png
output/example_mode_profile.png

Usage
-----
cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python mode_spectrum_over_time.py
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

    for i in range(1, N + 1):
        G.add_edge(center, i)

    for i in range(1, N + 1):
        G.add_edge(i, 1 + (i % N))

    return G


# -----------------------------
# Simulation with history
# -----------------------------
def simulate_history(N, steps=1500, dt=0.02, K=1.0):

    G = build_hub_ring(N)
    A = nx.to_numpy_array(G)

    nodes = len(A)

    theta = np.random.uniform(0, 2 * np.pi, nodes)
    omega = np.random.normal(0, 0.1, nodes)

    history = []

    for _ in range(steps):
        theta = kuramoto_step(theta, omega, A, K, dt)
        history.append(theta.copy())

    return np.array(history)


# -----------------------------
# Spatial mode spectrum
# -----------------------------
def ring_mode_spectrum(theta_ring, max_mode=12):

    """
    Compute Fourier-like spatial mode amplitudes on the ring.

    theta_ring: phases of ring oscillators
    returns: amplitudes for k = 0..max_mode
    """
    N = len(theta_ring)
    z = np.exp(1j * theta_ring)

    amps = []

    indices = np.arange(N)

    for k in range(max_mode + 1):
        basis = np.exp(-2j * np.pi * k * indices / N)
        ak = np.abs(np.sum(z * basis)) / N
        amps.append(ak)

    return np.array(amps)


# -----------------------------
# Spectrum over time
# -----------------------------
def compute_mode_history(history, max_mode=12):

    ring_history = history[:, 1:]  # remove hub

    spectra = []

    for theta_ring in ring_history:
        amps = ring_mode_spectrum(theta_ring, max_mode=max_mode)
        spectra.append(amps)

    return np.array(spectra)


# -----------------------------
# Plot spectrum heatmap
# -----------------------------
def plot_mode_heatmap(mode_history):

    Path("output").mkdir(exist_ok=True)

    plt.figure(figsize=(10, 5))

    plt.imshow(
        mode_history.T,
        aspect="auto",
        origin="lower",
        cmap="viridis"
    )

    plt.xlabel("Time step")
    plt.ylabel("Mode k")
    plt.title("Mode spectrum over time")
    plt.colorbar(label="Mode amplitude")

    plt.savefig("output/mode_spectrum_over_time.png", dpi=300)
    plt.show()


# -----------------------------
# Plot dominant mode
# -----------------------------
def plot_dominant_mode(mode_history):

    dominant = np.argmax(mode_history, axis=1)

    plt.figure(figsize=(10, 4))
    plt.plot(dominant)

    plt.xlabel("Time step")
    plt.ylabel("Dominant mode k")
    plt.title("Dominant spatial mode over time")

    Path("output").mkdir(exist_ok=True)

    plt.savefig("output/dominant_mode_over_time.png", dpi=300)
    plt.show()

    return dominant


# -----------------------------
# Plot example mode profile
# -----------------------------
def plot_example_profile(mode_history, t_index=None):

    if t_index is None:
        t_index = len(mode_history) // 2

    profile = mode_history[t_index]

    plt.figure(figsize=(8, 4))
    plt.bar(np.arange(len(profile)), profile)

    plt.xlabel("Mode k")
    plt.ylabel("Amplitude")
    plt.title(f"Mode profile at time step {t_index}")

    Path("output").mkdir(exist_ok=True)

    plt.savefig("output/example_mode_profile.png", dpi=300)
    plt.show()


# -----------------------------
# Main
# -----------------------------
def main():

    N = 60
    steps = 1500
    max_mode = 12

    history = simulate_history(N=N, steps=steps)

    mode_history = compute_mode_history(history, max_mode=max_mode)

    plot_mode_heatmap(mode_history)
    dominant = plot_dominant_mode(mode_history)
    plot_example_profile(mode_history)

    print("Mode spectrum analysis completed.")
    print("Unique dominant modes found:", sorted(set(dominant)))


if __name__ == "__main__":
    main()
