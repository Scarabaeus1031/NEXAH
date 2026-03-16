"""
NEXAH Rotation Number Analysis
==============================

Computes rotation numbers over the NEXAH symmetry/drift parameter space.

This is the first core diagnostic for circle-map-like behavior.

Input
-----
ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_scan_full.json

Output
------
ENGINE/nexah_kernel/demos/data/resonance_discovery/rotation_numbers.json
ENGINE/nexah_kernel/demos/visuals/resonance_landscape/rotation_number_map.png
"""

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt


SCAN_FILE = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_scan_full.json"
)

OUT_JSON = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/rotation_numbers.json"
)

OUT_IMG = Path(
    "ENGINE/nexah_kernel/demos/visuals/resonance_landscape/rotation_number_map.png"
)

OUT_IMG.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load scan data
# --------------------------------------------------

def load_scan():

    with open(SCAN_FILE) as f:
        data = json.load(f)

    return data


# --------------------------------------------------
# Build parameter grid
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
# Rotation number computation
# --------------------------------------------------

def compute_rotation_number(n, drift, steps=2000):

    theta = 0.0
    theta0 = 0.0

    for _ in range(steps):

        theta += (2*np.pi)/n + drift*np.pi/180.0
        theta = theta % (2*np.pi)

    rotation = (theta - theta0) / (2*np.pi*steps)

    return rotation


# --------------------------------------------------
# Scan rotation numbers
# --------------------------------------------------

def rotation_scan(n_vals, drift_vals):

    rot_grid = np.zeros((len(drift_vals), len(n_vals)))

    for i, drift in enumerate(drift_vals):

        for j, n in enumerate(n_vals):

            rot_grid[i,j] = compute_rotation_number(n, drift)

    return rot_grid


# --------------------------------------------------
# Plot
# --------------------------------------------------

def plot_rotation_map(rot_grid, n_vals, drift_vals):

    plt.figure(figsize=(10,6))

    plt.imshow(
        rot_grid,
        origin="lower",
        aspect="auto"
    )

    plt.colorbar(label="Rotation Number")

    plt.title("NEXAH Rotation Number Map")

    plt.xlabel("Symmetry (n)")
    plt.ylabel("Drift (deg)")

    plt.tight_layout()

    plt.savefig(OUT_IMG, dpi=300)

    print("\nSaved rotation map:", OUT_IMG)

    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("\nComputing rotation numbers...\n")

    data = load_scan()

    grid, n_vals, drift_vals = build_grid(data)

    rot_grid = rotation_scan(n_vals, drift_vals)

    output = []

    for i, drift in enumerate(drift_vals):
        for j, n in enumerate(n_vals):

            output.append({
                "n": int(n),
                "drift": float(drift),
                "rotation_number": float(rot_grid[i,j])
            })

    with open(OUT_JSON,"w") as f:

        json.dump(output,f,indent=2)

    print("Saved rotation numbers:", OUT_JSON)

    plot_rotation_map(rot_grid, n_vals, drift_vals)


if __name__ == "__main__":
    main()
