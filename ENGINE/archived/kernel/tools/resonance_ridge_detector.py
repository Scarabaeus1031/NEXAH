"""
Resonance Ridge Detector
========================

Detects resonance ridges and local maxima in symmetry/drift space.

Reads:
    ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_scan_full.json

Writes:
    ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_ridges.json
    ENGINE/nexah_kernel/demos/visuals/resonance_landscape/resonance_ridges.png
"""

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Paths
# --------------------------------------------------

DATA_FILE = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_scan_full.json"
)

OUTPUT_JSON = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_ridges.json"
)

OUTPUT_IMG = Path(
    "ENGINE/nexah_kernel/demos/visuals/resonance_landscape/resonance_ridges.png"
)

OUTPUT_IMG.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load scan data
# --------------------------------------------------

def load_data():

    with open(DATA_FILE) as f:
        data = json.load(f)

    return data


# --------------------------------------------------
# Build parameter grid
# --------------------------------------------------

def build_grid(data):

    n_vals = sorted({d["n"] for d in data})
    drift_vals = sorted({round(d["drift"], 4) for d in data})

    grid = np.zeros((len(drift_vals), len(n_vals)))

    for d in data:

        i = drift_vals.index(round(d["drift"], 4))
        j = n_vals.index(d["n"])

        grid[i, j] = d["resonance_score"]

    return grid, n_vals, drift_vals


# --------------------------------------------------
# Local maxima detection
# --------------------------------------------------

def find_ridges(grid):

    ridges = []

    rows, cols = grid.shape

    for i in range(1, rows-1):
        for j in range(1, cols-1):

            center = grid[i, j]

            neighbors = [
                grid[i-1, j],
                grid[i+1, j],
                grid[i, j-1],
                grid[i, j+1],
                grid[i-1, j-1],
                grid[i-1, j+1],
                grid[i+1, j-1],
                grid[i+1, j+1],
            ]

            if center > max(neighbors):

                ridges.append((i, j, center))

    return ridges


# --------------------------------------------------
# Convert ridge indices to parameters
# --------------------------------------------------

def ridge_parameters(ridges, n_vals, drift_vals):

    results = []

    for i, j, score in ridges:

        results.append({
            "n": n_vals[j],
            "drift": drift_vals[i],
            "score": float(score)
        })

    return results


# --------------------------------------------------
# Plot heatmap + ridge markers
# --------------------------------------------------

def plot_ridges(grid, ridges, n_vals, drift_vals):

    plt.figure(figsize=(10,6))

    plt.imshow(
        grid,
        aspect="auto",
        origin="lower"
    )

    plt.colorbar(label="Resonance Score")

    # ridge markers
    for i, j, _ in ridges:
        plt.scatter(j, i, color="red", s=40)

    plt.xticks(range(len(n_vals)), n_vals)

    step = max(1, len(drift_vals)//10)

    plt.yticks(
        range(0, len(drift_vals), step),
        [round(d,2) for d in drift_vals[0::step]]
    )

    plt.xlabel("Symmetry (n)")
    plt.ylabel("Drift (degrees)")
    plt.title("NEXAH Resonance Landscape — Ridge Detection")

    plt.tight_layout()

    plt.savefig(OUTPUT_IMG, dpi=300)

    print("\nSaved ridge map:", OUTPUT_IMG)

    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("\nLoading resonance scan...")

    data = load_data()

    print("Records:", len(data))

    grid, n_vals, drift_vals = build_grid(data)

    print("Grid shape:", grid.shape)

    ridges = find_ridges(grid)

    print("\nDetected ridges:", len(ridges))

    ridge_params = ridge_parameters(ridges, n_vals, drift_vals)

    with open(OUTPUT_JSON, "w") as f:
        json.dump(ridge_params, f, indent=2)

    print("Saved ridge data:", OUTPUT_JSON)

    plot_ridges(grid, ridges, n_vals, drift_vals)


if __name__ == "__main__":
    main()
