"""
NEXAH KAM Torus Detector
========================

Heuristic detector for KAM-like quasi-periodic regions
in the NEXAH symmetry/drift parameter space.

Input:
    ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_scan_full.json

Output:
    ENGINE/nexah_kernel/demos/data/resonance_discovery/kam_torus_candidates.json
    ENGINE/nexah_kernel/demos/visuals/resonance_landscape/kam_torus_map.png
"""

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt


SCAN_FILE = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_scan_full.json"
)

OUT_JSON = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/kam_torus_candidates.json"
)

OUT_IMG = Path(
    "ENGINE/nexah_kernel/demos/visuals/resonance_landscape/kam_torus_map.png"
)

OUT_IMG.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load data
# --------------------------------------------------

def load_scan():

    with open(SCAN_FILE) as f:
        data = json.load(f)

    return data


# --------------------------------------------------
# Build resonance grid
# --------------------------------------------------

def build_grid(data):

    n_vals = sorted({d["n"] for d in data})
    drift_vals = sorted({round(d["drift"],4) for d in data})

    grid = np.zeros((len(drift_vals), len(n_vals)))

    for d in data:

        i = drift_vals.index(round(d["drift"],4))
        j = n_vals.index(d["n"])

        grid[i,j] = d["resonance_score"]

    return grid, n_vals, drift_vals


# --------------------------------------------------
# KAM-like heuristic
# --------------------------------------------------

def detect_kam_regions(grid):

    rows, cols = grid.shape

    kam_points = []

    for i in range(1, rows-1):
        for j in range(1, cols-1):

            center = grid[i,j]

            neighborhood = grid[i-1:i+2, j-1:j+2]

            variance = np.var(neighborhood)

            gradient = abs(
                grid[i+1,j] - grid[i-1,j]
            ) + abs(
                grid[i,j+1] - grid[i,j-1]
            )

            if variance < 0.0008 and gradient < 0.05:

                kam_points.append((i,j,center))

    return kam_points


# --------------------------------------------------
# Convert to parameter space
# --------------------------------------------------

def convert_points(points, n_vals, drift_vals):

    out = []

    for i,j,score in points:

        out.append({
            "n": int(n_vals[j]),
            "drift": float(drift_vals[i]),
            "score": float(score)
        })

    return out


# --------------------------------------------------
# Plot map
# --------------------------------------------------

def plot_map(grid, kam_points):

    plt.figure(figsize=(10,6))

    plt.imshow(grid, origin="lower", aspect="auto")

    plt.colorbar(label="Resonance Score")

    for i,j,_ in kam_points:

        plt.scatter(j,i,color="cyan",s=70,edgecolor="black")

    plt.title("NEXAH KAM Torus Candidates")

    plt.tight_layout()

    plt.savefig(OUT_IMG, dpi=300)

    print("\nSaved KAM map:", OUT_IMG)

    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("\nDetecting KAM-like regions...\n")

    data = load_scan()

    grid, n_vals, drift_vals = build_grid(data)

    kam_points = detect_kam_regions(grid)

    print("KAM candidates:", len(kam_points))

    converted = convert_points(kam_points,n_vals,drift_vals)

    with open(OUT_JSON,"w") as f:

        json.dump(converted,f,indent=2)

    print("Saved KAM candidates:", OUT_JSON)

    plot_map(grid,kam_points)


if __name__ == "__main__":
    main()
