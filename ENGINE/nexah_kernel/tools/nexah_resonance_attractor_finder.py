"""
NEXAH Resonance Attractor Finder
================================

Detects stable resonance attractors in the symmetry/drift parameter space.

Input
-----
ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_scan_full.json

Output
------
resonance_attractors.json
resonance_attractors_map.png
"""

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt


SCAN_FILE = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_scan_full.json"
)

OUT_DIR = Path(
    "ENGINE/nexah_kernel/demos/visuals/attractors"
)

OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_JSON = OUT_DIR / "resonance_attractors.json"
OUT_IMG = OUT_DIR / "resonance_attractors_map.png"


# --------------------------------------------------
# Load data
# --------------------------------------------------

def load_scan():

    with open(SCAN_FILE) as f:
        data = json.load(f)

    return data


# --------------------------------------------------
# Build grid
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
# Local maxima detection
# --------------------------------------------------

def detect_local_maxima(grid):

    rows, cols = grid.shape

    maxima = []

    for i in range(1, rows-1):
        for j in range(1, cols-1):

            center = grid[i,j]

            neighborhood = grid[i-1:i+2, j-1:j+2]

            if center == np.max(neighborhood) and np.sum(neighborhood == center) == 1:

                maxima.append((i,j,center))

    return maxima


# --------------------------------------------------
# Attractor stability score
# --------------------------------------------------

def compute_stability(grid, i, j):

    neighborhood = grid[i-1:i+2, j-1:j+2]

    variance = np.var(neighborhood)

    stability = 1 / (1 + variance)

    return stability


# --------------------------------------------------
# Detect attractors
# --------------------------------------------------

def find_attractors(grid):

    maxima = detect_local_maxima(grid)

    attractors = []

    for i,j,val in maxima:

        stability = compute_stability(grid,i,j)

        if stability > 0.95:

            attractors.append((i,j,val,stability))

    return attractors


# --------------------------------------------------
# Convert to parameter space
# --------------------------------------------------

def convert(attractors, n_vals, drift_vals):

    out = []

    for i,j,val,stab in attractors:

        out.append({

            "n": int(n_vals[j]),
            "drift": float(drift_vals[i]),
            "score": float(val),
            "stability": float(stab)
        })

    return out


# --------------------------------------------------
# Plot attractor map
# --------------------------------------------------

def plot_map(grid, attractors):

    plt.figure(figsize=(10,6))

    plt.imshow(
        grid,
        origin="lower",
        aspect="auto"
    )

    plt.colorbar(label="Resonance Score")

    for i,j,val,stab in attractors:

        plt.scatter(j,i,color="white",s=80,edgecolor="black")

    plt.title("NEXAH Resonance Attractors")

    plt.tight_layout()

    plt.savefig(OUT_IMG,dpi=300)

    print("\nSaved attractor map:",OUT_IMG)

    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("\nSearching resonance attractors...\n")

    data = load_scan()

    grid, n_vals, drift_vals = build_grid(data)

    attractors = find_attractors(grid)

    print("Attractors found:",len(attractors))

    converted = convert(attractors,n_vals,drift_vals)

    with open(OUT_JSON,"w") as f:

        json.dump(converted,f,indent=2)

    print("Saved attractor data:",OUT_JSON)

    plot_map(grid,attractors)


if __name__ == "__main__":
    main()
