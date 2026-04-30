"""
NEXAH Resonance Phase Diagram
=============================

Builds a phase diagram of the resonance parameter space.

Each (symmetry, drift) point is classified into a dynamical phase.

Input
-----
ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_scan_full.json

Output
------
phase_diagram.png
phase_diagram.json
"""

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt


SCAN_FILE = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_scan_full.json"
)

OUT_DIR = Path(
    "ENGINE/nexah_kernel/demos/visuals/phase_diagram"
)

OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_IMG = OUT_DIR / "phase_diagram.png"
OUT_JSON = OUT_DIR / "phase_diagram.json"


# --------------------------------------------------
# Load scan data
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
# Phase classification
# --------------------------------------------------

def classify_phase(score, local_variance):

    if score > 0.16:
        return 3  # chaotic resonance

    if score > 0.13:
        return 2  # multi-mode

    if local_variance < 0.001:
        return 0  # stable ring

    return 1  # spiral


# --------------------------------------------------
# Build phase map
# --------------------------------------------------

def compute_phase_map(grid):

    rows, cols = grid.shape

    phase = np.zeros_like(grid)

    for i in range(1, rows-1):
        for j in range(1, cols-1):

            neighborhood = grid[i-1:i+2, j-1:j+2]

            var = np.var(neighborhood)

            phase[i,j] = classify_phase(grid[i,j], var)

    return phase


# --------------------------------------------------
# Plot phase diagram
# --------------------------------------------------

def plot_phase_map(phase, n_vals, drift_vals):

    cmap = plt.get_cmap("tab10")

    plt.figure(figsize=(10,6))

    plt.imshow(
        phase,
        aspect="auto",
        origin="lower",
        cmap=cmap
    )

    cbar = plt.colorbar()

    cbar.set_ticks([0,1,2,3])
    cbar.set_ticklabels([
        "stable_ring",
        "spiral",
        "multi_mode",
        "chaotic"
    ])

    plt.xticks(range(len(n_vals)), n_vals)

    step = max(1,len(drift_vals)//10)

    plt.yticks(
        range(0,len(drift_vals),step),
        [round(d,2) for d in drift_vals[0::step]]
    )

    plt.xlabel("Symmetry (n)")
    plt.ylabel("Drift (degrees)")
    plt.title("NEXAH Resonance Phase Diagram")

    plt.tight_layout()

    plt.savefig(OUT_IMG, dpi=300)

    print("\nSaved phase diagram:", OUT_IMG)

    plt.show()


# --------------------------------------------------
# Save phase data
# --------------------------------------------------

def save_phase_data(phase, n_vals, drift_vals):

    out = []

    rows, cols = phase.shape

    for i in range(rows):
        for j in range(cols):

            out.append({
                "n": int(n_vals[j]),
                "drift": float(drift_vals[i]),
                "phase": int(phase[i,j])
            })

    with open(OUT_JSON,"w") as f:
        json.dump(out,f,indent=2)

    print("Saved phase data:", OUT_JSON)


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("\nBuilding NEXAH phase diagram...\n")

    data = load_scan()

    grid, n_vals, drift_vals = build_grid(data)

    phase = compute_phase_map(grid)

    save_phase_data(phase, n_vals, drift_vals)

    plot_phase_map(phase, n_vals, drift_vals)


# --------------------------------------------------

if __name__ == "__main__":
    main()
