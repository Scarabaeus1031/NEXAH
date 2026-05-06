"""
NEXAH Resonance Topology Map
============================

Builds a topological analysis of the resonance landscape.

Detects:
    peaks
    valleys
    ridge candidates
    gradient field

Input:
    resonance_scan_full.json

Output:
    resonance_topology.json
    resonance_topology_map.png
"""

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt


DATA_FILE = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_scan_full.json"
)

OUT_JSON = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_topology.json"
)

OUT_IMG = Path(
    "ENGINE/nexah_kernel/demos/visuals/resonance_landscape/resonance_topology_map.png"
)

OUT_IMG.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load data
# --------------------------------------------------

def load_scan():

    with open(DATA_FILE) as f:
        data = json.load(f)

    return data


# --------------------------------------------------
# Build grid
# --------------------------------------------------

def build_grid(data):

    n_vals = sorted({d["n"] for d in data})
    drift_vals = sorted({round(d["drift"], 4) for d in data})

    grid = np.zeros((len(drift_vals), len(n_vals)))

    for d in data:

        i = drift_vals.index(round(d["drift"],4))
        j = n_vals.index(d["n"])

        grid[i,j] = d["resonance_score"]

    return grid, n_vals, drift_vals


# --------------------------------------------------
# Neighborhood comparison
# --------------------------------------------------

def classify_points(grid):

    peaks = []
    valleys = []

    rows, cols = grid.shape

    for i in range(1, rows-1):
        for j in range(1, cols-1):

            center = grid[i,j]

            neighbors = [
                grid[i-1,j],
                grid[i+1,j],
                grid[i,j-1],
                grid[i,j+1],
                grid[i-1,j-1],
                grid[i-1,j+1],
                grid[i+1,j-1],
                grid[i+1,j+1]
            ]

            if center > max(neighbors):
                peaks.append((i,j,center))

            if center < min(neighbors):
                valleys.append((i,j,center))

    return peaks, valleys


# --------------------------------------------------
# Gradient field
# --------------------------------------------------

def compute_gradient(grid):

    gy, gx = np.gradient(grid)

    return gx, gy


# --------------------------------------------------
# Plot topology
# --------------------------------------------------

def plot_topology(grid, peaks, valleys, gx, gy, n_vals, drift_vals):

    plt.figure(figsize=(11,6))

    plt.imshow(grid, aspect="auto", origin="lower")

    plt.colorbar(label="Resonance Score")

    # peaks
    for i,j,_ in peaks:
        plt.scatter(j,i,color="red",s=40)

    # valleys
    for i,j,_ in valleys:
        plt.scatter(j,i,color="blue",s=30)

    # gradient arrows (subsample)
    step = 4

    y = np.arange(0,grid.shape[0],step)
    x = np.arange(0,grid.shape[1],step)

    X,Y = np.meshgrid(x,y)

    plt.quiver(
        X,
        Y,
        gx[::step,::step],
        gy[::step,::step],
        color="white",
        alpha=0.6
    )

    plt.xticks(range(len(n_vals)), n_vals)

    step_y = max(1,len(drift_vals)//10)

    plt.yticks(
        range(0,len(drift_vals),step_y),
        [round(d,2) for d in drift_vals[0::step_y]]
    )

    plt.xlabel("Symmetry (n)")
    plt.ylabel("Drift (degrees)")
    plt.title("NEXAH Resonance Topology Map")

    plt.tight_layout()

    plt.savefig(OUT_IMG,dpi=300)

    print("\nSaved topology map:",OUT_IMG)

    plt.show()


# --------------------------------------------------
# Convert results
# --------------------------------------------------

def convert_points(points, n_vals, drift_vals):

    out = []

    for i,j,score in points:

        out.append({
            "n": n_vals[j],
            "drift": drift_vals[i],
            "score": float(score)
        })

    return out


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("\nLoading scan data...")

    data = load_scan()

    print("Records:",len(data))

    grid, n_vals, drift_vals = build_grid(data)

    peaks, valleys = classify_points(grid)

    print("Peaks detected:",len(peaks))
    print("Valleys detected:",len(valleys))

    gx, gy = compute_gradient(grid)

    topology = {
        "peaks": convert_points(peaks,n_vals,drift_vals),
        "valleys": convert_points(valleys,n_vals,drift_vals)
    }

    with open(OUT_JSON,"w") as f:
        json.dump(topology,f,indent=2)

    print("Saved topology data:",OUT_JSON)

    plot_topology(grid,peaks,valleys,gx,gy,n_vals,drift_vals)


if __name__ == "__main__":
    main()
