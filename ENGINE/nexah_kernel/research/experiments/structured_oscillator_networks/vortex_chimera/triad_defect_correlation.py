"""
NEXAH Experiment Tool
Triad–Defect Correlation Analyzer

Purpose
-------
Measure the relationship between

    • phase defects (vortex slips)
    • triadic closure regions

Hypothesis
----------
Defects occur preferentially at
boundaries of triadic closure shells.

Outputs
-------
output/triad_defect_overlay.png
output/triad_defect_distance_hist.png
output/triad_defect_time_series.png
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ---------------------------------------------------------
# Load maps
# ---------------------------------------------------------

def load_maps():

    defect_map = np.load("output/defect_map.npy")
    triad_map = np.load("output/triadic_closure_map.npy")

    return defect_map, triad_map


# ---------------------------------------------------------
# Find triadic boundaries
# ---------------------------------------------------------

def compute_triad_boundaries(triad_map):

    boundaries = np.zeros_like(triad_map)

    T, N = triad_map.shape

    for t in range(T):
        for i in range(N):

            left = triad_map[t,(i-1)%N]
            right = triad_map[t,(i+1)%N]

            if triad_map[t,i] != left or triad_map[t,i] != right:
                boundaries[t,i] = 1

    return boundaries


# ---------------------------------------------------------
# Distance to nearest boundary
# ---------------------------------------------------------

def compute_defect_distances(defect_map, boundary_map):

    T, N = defect_map.shape

    distances = []

    for t in range(T):

        boundary_indices = np.where(boundary_map[t]==1)[0]

        if len(boundary_indices)==0:
            continue

        defect_indices = np.where(defect_map[t]==1)[0]

        for d in defect_indices:

            dist = np.min(np.abs(boundary_indices - d))
            distances.append(dist)

    return np.array(distances)


# ---------------------------------------------------------
# Plot overlay
# ---------------------------------------------------------

def plot_overlay(defect_map, triad_map):

    plt.figure(figsize=(10,5))

    plt.imshow(triad_map.T,aspect="auto",origin="lower",cmap="viridis")

    T,N = defect_map.shape

    xs,ys = [],[]

    for t in range(T):
        idx = np.where(defect_map[t]==1)[0]
        xs.extend([t]*len(idx))
        ys.extend(idx)

    plt.scatter(xs,ys,color="red",s=5,label="defects")

    plt.title("Triadic closure with defect overlay")
    plt.xlabel("time")
    plt.ylabel("ring index")

    plt.legend()

    plt.savefig("output/triad_defect_overlay.png",dpi=300)
    plt.show()


# ---------------------------------------------------------
# Histogram
# ---------------------------------------------------------

def plot_distance_hist(distances):

    plt.figure(figsize=(7,4))

    plt.hist(distances,bins=20)

    plt.xlabel("distance defect → triadic boundary")
    plt.ylabel("count")

    plt.title("Defect–Triad boundary distance distribution")

    plt.savefig("output/triad_defect_distance_hist.png",dpi=300)
    plt.show()


# ---------------------------------------------------------
# Time series correlation
# ---------------------------------------------------------

def plot_time_series(defect_map, triad_map):

    defect_count = defect_map.sum(axis=1)
    triad_count = triad_map.sum(axis=1)

    plt.figure(figsize=(10,4))

    plt.plot(defect_count,label="defects")
    plt.plot(triad_count,label="triadic closures")

    plt.xlabel("time step")
    plt.ylabel("count")

    plt.title("Triadic closure vs defects over time")

    plt.legend()

    plt.savefig("output/triad_defect_time_series.png",dpi=300)
    plt.show()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    Path("output").mkdir(exist_ok=True)

    defect_map, triad_map = load_maps()

    boundary_map = compute_triad_boundaries(triad_map)

    distances = compute_defect_distances(defect_map,boundary_map)

    plot_overlay(defect_map,triad_map)
    plot_distance_hist(distances)
    plot_time_series(defect_map,triad_map)

    print("Mean distance defect → triad boundary:",np.mean(distances))


if __name__ == "__main__":
    main()
