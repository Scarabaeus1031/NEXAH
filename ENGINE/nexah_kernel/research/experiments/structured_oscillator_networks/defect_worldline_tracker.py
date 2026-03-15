"""
NEXAH Experiment Tool
Defect Worldline Tracker

Purpose
-------
Track phase-defect positions through time in a hub-ring oscillator system.

This tool detects local phase-slip defects and connects them across time
to build approximate worldlines.

Outputs
-------
output/defect_worldline_map.png
output/defect_worldline_overlay.png
output/defect_lifetime_histogram.png

Usage
-----
cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python defect_worldline_tracker.py
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
# Local phase jumps
# -----------------------------
def phase_diff_ring(theta_ring):

    diffs = np.roll(theta_ring, -1) - theta_ring
    diffs = (diffs + np.pi) % (2 * np.pi) - np.pi

    return diffs


# -----------------------------
# Defect detection
# -----------------------------
def detect_defects(theta_ring, threshold=2.2):

    diffs = phase_diff_ring(theta_ring)
    defects = np.where(np.abs(diffs) > threshold)[0]

    return defects, diffs


# -----------------------------
# Defect map
# -----------------------------
def compute_defect_history(history, threshold=2.2):

    ring_history = history[:, 1:]

    defect_positions = []
    defect_map = []

    for theta_ring in ring_history:

        defects, _ = detect_defects(theta_ring, threshold=threshold)

        row = np.zeros(len(theta_ring))
        row[defects] = 1

        defect_positions.append(defects.tolist())
        defect_map.append(row)

    return defect_positions, np.array(defect_map)


# -----------------------------
# Circular distance on ring
# -----------------------------
def ring_distance(a, b, N):

    d = abs(a - b)
    return min(d, N - d)


# -----------------------------
# Worldline tracking
# -----------------------------
def track_worldlines(defect_positions, N, max_jump=2):

    """
    Greedy nearest-neighbor worldline tracker.
    Each worldline is a list of (time, ring_index).
    """
    worldlines = []
    active = []

    for t, defects in enumerate(defect_positions):

        defects = list(defects)
        used = set()
        new_active = []

        # try to extend existing lines
        for line in active:

            last_t, last_pos = line[-1]

            best_idx = None
            best_dist = None

            for j, pos in enumerate(defects):
                if j in used:
                    continue

                dist = ring_distance(last_pos, pos, N)

                if dist <= max_jump:
                    if best_dist is None or dist < best_dist:
                        best_dist = dist
                        best_idx = j

            if best_idx is not None:
                pos = defects[best_idx]
                line.append((t, pos))
                used.add(best_idx)
                new_active.append(line)
            else:
                worldlines.append(line)

        # start new lines for unmatched defects
        for j, pos in enumerate(defects):
            if j not in used:
                new_active.append([(t, pos)])

        active = new_active

    # finalize remaining active lines
    worldlines.extend(active)

    return worldlines


# -----------------------------
# Plot raw defect map
# -----------------------------
def plot_defect_map(defect_map):

    Path("output").mkdir(exist_ok=True)

    plt.figure(figsize=(10, 5))

    plt.imshow(
        defect_map.T,
        aspect="auto",
        origin="lower",
        cmap="inferno"
    )

    plt.xlabel("time step")
    plt.ylabel("ring index")
    plt.title("Defect map")
    plt.colorbar(label="defect")

    plt.savefig("output/defect_worldline_map.png", dpi=300)

    plt.show()


# -----------------------------
# Plot worldlines
# -----------------------------
def plot_worldlines(defect_map, worldlines):

    plt.figure(figsize=(10, 5))

    plt.imshow(
        defect_map.T,
        aspect="auto",
        origin="lower",
        cmap="gray_r",
        alpha=0.35
    )

    for line in worldlines:
        if len(line) < 2:
            continue

        t_vals = [p[0] for p in line]
        x_vals = [p[1] for p in line]

        plt.plot(t_vals, x_vals, linewidth=1.2)

    plt.xlabel("time step")
    plt.ylabel("ring index")
    plt.title("Tracked defect worldlines")

    plt.savefig("output/defect_worldline_overlay.png", dpi=300)

    plt.show()


# -----------------------------
# Lifetime histogram
# -----------------------------
def plot_lifetimes(worldlines):

    lifetimes = [len(line) for line in worldlines if len(line) > 0]

    plt.figure(figsize=(8, 4))

    plt.hist(lifetimes, bins=30)

    plt.xlabel("worldline length")
    plt.ylabel("count")
    plt.title("Defect worldline lifetime distribution")

    plt.savefig("output/defect_lifetime_histogram.png", dpi=300)

    plt.show()


# -----------------------------
# Main
# -----------------------------
def main():

    N = 60
    steps = 1200
    threshold = 2.2

    history = simulate_history(N=N, steps=steps)

    defect_positions, defect_map = compute_defect_history(
        history,
        threshold=threshold
    )

    worldlines = track_worldlines(
        defect_positions,
        N=N,
        max_jump=2
    )

    plot_defect_map(defect_map)
    plot_worldlines(defect_map, worldlines)
    plot_lifetimes(worldlines)

    print("Defect worldline tracking completed.")
    print("Number of tracked worldlines:", len(worldlines))
    print("Longest worldline length:", max(len(w) for w in worldlines))


if __name__ == "__main__":
    main()
