"""
NEXAH Experiment Tool
Triadic Closure Detector

Purpose
-------
Detect local triadic closure structures in a hub-ring oscillator network.

For each ring node i, we analyze the local triad:

    (i-1, i, i+1)

We measure whether the two adjacent phase differences are similar,
which indicates local triadic phase locking / closure.

This helps identify:

• triadic locking regions
• triadic shell structures
• closure bands
• relation between defects and local triads

Outputs
-------
output/triadic_closure_map.png
output/triadic_closure_count_vs_time.png
output/triadic_closure_snapshot.png

Usage
-----
cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python triadic_closure_detector.py
"""

"""
NEXAH Experiment Tool
Triadic Closure Detector
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

    theta = np.random.uniform(0, 2 * np.pi, nodes)
    omega = np.random.normal(0, 0.1, nodes)

    history = []

    for _ in range(steps):
        theta = kuramoto_step(theta, omega, A, K, dt)
        history.append(theta.copy())

    return np.array(history)


# -----------------------------
# Angle wrap
# -----------------------------
def wrap_angle(x):

    return (x + np.pi) % (2 * np.pi) - np.pi


# -----------------------------
# Triadic closure
# -----------------------------
def triadic_closure_scores(theta_ring):

    N = len(theta_ring)

    scores = []

    for i in range(N):

        im1 = (i - 1) % N
        ip1 = (i + 1) % N

        d_left = wrap_angle(theta_ring[i] - theta_ring[im1])
        d_right = wrap_angle(theta_ring[ip1] - theta_ring[i])

        mismatch = abs(d_left - d_right)
        mismatch = min(mismatch, 2*np.pi - mismatch)

        score = 1.0 - mismatch / np.pi
        score = max(0.0, score)

        scores.append(score)

    return np.array(scores)


# -----------------------------
# Detection
# -----------------------------
def detect_triadic_closure(theta_ring, threshold=0.8):

    scores = triadic_closure_scores(theta_ring)

    mask = scores > threshold

    return mask, scores


# -----------------------------
# Scan simulation
# -----------------------------
def compute_closure_history(history, threshold=0.8):

    ring_history = history[:,1:]

    closure_map = []
    closure_counts = []

    for theta in ring_history:

        mask, scores = detect_triadic_closure(theta, threshold)

        closure_map.append(mask.astype(float))
        closure_counts.append(np.sum(mask))

    return np.array(closure_map), np.array(closure_counts)


# -----------------------------
# Plot closure map
# -----------------------------
def plot_closure_map(closure_map):

    Path("output").mkdir(exist_ok=True)

    plt.figure(figsize=(10,5))

    plt.imshow(
        closure_map.T,
        aspect="auto",
        origin="lower",
        cmap="viridis"
    )

    plt.xlabel("time step")
    plt.ylabel("ring index")
    plt.title("Triadic closure map")

    plt.colorbar(label="closure")

    plt.savefig("output/triadic_closure_map.png", dpi=300)

    plt.show()


# -----------------------------
# Plot counts
# -----------------------------
def plot_closure_counts(closure_counts):

    plt.figure(figsize=(10,4))

    plt.plot(closure_counts)

    plt.xlabel("time step")
    plt.ylabel("triadic closure count")

    plt.title("Number of triadic closures over time")

    plt.savefig("output/triadic_closure_count_vs_time.png", dpi=300)

    plt.show()


# -----------------------------
# Main
# -----------------------------
def main():

    N = 60
    steps = 1200

    history = simulate_history(N, steps)

    closure_map, closure_counts = compute_closure_history(history)

    Path("output").mkdir(exist_ok=True)

    np.save("output/triadic_closure_map.npy", closure_map)

    plot_closure_map(closure_map)
    plot_closure_counts(closure_counts)

    print("Triadic closure detection completed.")
    print("Saved: output/triadic_closure_map.npy")


if __name__ == "__main__":
    main()
