"""
NEXAH Experiment Tool
Braid Topology Extractor

Purpose
-------
Extract braid-like structures from defect worldlines
in a hub-ring oscillator network.

We treat defects as particles moving along ring index over time.

Outputs
-------
output/braid_worldlines.png
output/braid_crossings.png
output/braid_statistics.txt
output/braid_crossings.npy
output/defect_worldlines.npy
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ------------------------------------------------
# Load defect map
# ------------------------------------------------
def load_defects():

    defect_map = np.load("output/defect_map.npy")

    return defect_map


# ------------------------------------------------
# Extract worldlines
# ------------------------------------------------
def extract_worldlines(defect_map):

    T, N = defect_map.shape

    worldlines = []
    visited = np.zeros_like(defect_map)

    for t in range(T):
        for i in range(N):

            if defect_map[t, i] == 1 and visited[t, i] == 0:

                line = []
                tt = t
                ii = i

                while tt < T and defect_map[tt, ii] == 1:
                    line.append((tt, ii))
                    visited[tt, ii] = 1
                    tt += 1

                worldlines.append(line)

    return worldlines


# ------------------------------------------------
# Detect crossings
# ------------------------------------------------
def detect_crossings(worldlines):

    crossings = []

    for i in range(len(worldlines)):
        for j in range(i + 1, len(worldlines)):

            w1 = worldlines[i]
            w2 = worldlines[j]

            times1 = {t: r for t, r in w1}
            times2 = {t: r for t, r in w2}

            common_times = set(times1.keys()) & set(times2.keys())

            for t in common_times:
                if abs(times1[t] - times2[t]) <= 1:
                    crossings.append((t, times1[t]))

    return crossings


# ------------------------------------------------
# Save arrays
# ------------------------------------------------
def save_arrays(worldlines, crossings, T):

    Path("output").mkdir(exist_ok=True)

    max_len = max(len(w) for w in worldlines) if worldlines else 0

    arr = np.full((T, len(worldlines)), np.nan)

    for j, line in enumerate(worldlines):
        for t, r in line:
            arr[t, j] = r

    np.save("output/defect_worldlines.npy", arr)
    np.save("output/braid_crossings.npy", np.array(crossings, dtype=float))


# ------------------------------------------------
# Plot worldlines
# ------------------------------------------------
def plot_worldlines(worldlines):

    plt.figure(figsize=(10, 6))

    for line in worldlines:
        t = [p[0] for p in line]
        r = [p[1] for p in line]
        plt.plot(t, r)

    plt.xlabel("time")
    plt.ylabel("ring index")
    plt.title("Defect braid worldlines")

    plt.savefig("output/braid_worldlines.png", dpi=300)
    plt.show()


# ------------------------------------------------
# Plot crossings
# ------------------------------------------------
def plot_crossings(worldlines, crossings):

    plt.figure(figsize=(10, 6))

    for line in worldlines:
        t = [p[0] for p in line]
        r = [p[1] for p in line]
        plt.plot(t, r, alpha=0.5)

    if crossings:
        tx = [c[0] for c in crossings]
        rx = [c[1] for c in crossings]
        plt.scatter(tx, rx, color="red", s=30, label="crossings")

    plt.xlabel("time")
    plt.ylabel("ring index")
    plt.title("Braid crossings")
    plt.legend()

    plt.savefig("output/braid_crossings.png", dpi=300)
    plt.show()


# ------------------------------------------------
# Statistics
# ------------------------------------------------
def save_statistics(worldlines, crossings):

    lengths = [len(w) for w in worldlines] if worldlines else [0]

    with open("output/braid_statistics.txt", "w", encoding="utf-8") as f:
        f.write(f"Number of worldlines: {len(worldlines)}\n")
        f.write(f"Mean length: {np.mean(lengths):.2f}\n")
        f.write(f"Max length: {np.max(lengths)}\n")
        f.write(f"Crossings detected: {len(crossings)}\n")


# ------------------------------------------------
# Main
# ------------------------------------------------
def main():

    Path("output").mkdir(exist_ok=True)

    defect_map = load_defects()
    T = defect_map.shape[0]

    worldlines = extract_worldlines(defect_map)
    crossings = detect_crossings(worldlines)

    save_arrays(worldlines, crossings, T)
    plot_worldlines(worldlines)
    plot_crossings(worldlines, crossings)
    save_statistics(worldlines, crossings)

    print("Worldlines:", len(worldlines))
    print("Crossings:", len(crossings))
    print("Saved: output/defect_worldlines.npy")
    print("Saved: output/braid_crossings.npy")


if __name__ == "__main__":
    main()
