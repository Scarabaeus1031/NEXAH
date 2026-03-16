"""
Resonance Landscape Map
=======================

Visualizes resonance scores over symmetry/drift parameter space.

Run:
    python -m ENGINE.nexah_kernel.tools.resonance_landscape_map
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


DATA_FILE = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_scan_full.json"
)

OUTPUT_DIR = Path(
    "ENGINE/nexah_kernel/demos/visuals/resonance_landscape"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data():

    with open(DATA_FILE) as f:
        data = json.load(f)

    return data


def build_grid(data):

    n_vals = sorted({d["n"] for d in data})
    drift_vals = sorted({round(d["drift"], 3) for d in data})

    grid = np.zeros((len(drift_vals), len(n_vals)))

    for d in data:

        i = drift_vals.index(round(d["drift"], 3))
        j = n_vals.index(d["n"])

        grid[i, j] = d["resonance_score"]

    return grid, n_vals, drift_vals


def plot_heatmap(grid, n_vals, drift_vals):

    plt.figure(figsize=(10, 6))

    plt.imshow(
        grid,
        aspect="auto",
        origin="lower"
    )

    plt.colorbar(label="Resonance Score")

    plt.xticks(
        range(len(n_vals)),
        n_vals
    )

    drift_labels = [round(d, 1) for d in drift_vals]

    step = max(1, len(drift_labels)//10)

    plt.yticks(
        range(0, len(drift_vals), step),
        drift_labels[0::step]
    )

    plt.xlabel("Symmetry (n)")
    plt.ylabel("Drift (degrees)")
    plt.title("NEXAH Resonance Landscape")

    outfile = OUTPUT_DIR / "resonance_landscape.png"

    plt.tight_layout()
    plt.savefig(outfile, dpi=300)

    print("\nSaved map:", outfile)

    plt.show()


def main():

    print("\nLoading resonance scan data...")

    data = load_data()

    print("Records:", len(data))

    grid, n_vals, drift_vals = build_grid(data)

    plot_heatmap(grid, n_vals, drift_vals)


if __name__ == "__main__":
    main()
