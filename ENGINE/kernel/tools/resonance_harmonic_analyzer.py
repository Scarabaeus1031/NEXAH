"""
NEXAH Resonance Harmonic Analyzer
=================================

Analyzes harmonic structures in the resonance landscape.

Detects:

- peak spacing
- symmetry periodicities
- drift periodicities
- Fourier spectrum of the resonance field

Input:
    resonance_scan_full.json
    resonance_ridges.json

Output:
    resonance_harmonic_analysis.json
"""

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt


SCAN_FILE = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_scan_full.json"
)

RIDGE_FILE = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_ridges.json"
)

OUT_JSON = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/resonance_harmonics.json"
)

OUT_PLOT = Path(
    "ENGINE/nexah_kernel/demos/visuals/resonance_landscape/resonance_harmonic_spectrum.png"
)

OUT_PLOT.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load data
# --------------------------------------------------

def load_data():

    with open(SCAN_FILE) as f:
        scan = json.load(f)

    with open(RIDGE_FILE) as f:
        ridges = json.load(f)

    return scan, ridges


# --------------------------------------------------
# Build resonance grid
# --------------------------------------------------

def build_grid(scan):

    n_vals = sorted({d["n"] for d in scan})
    drift_vals = sorted({round(d["drift"],4) for d in scan})

    grid = np.zeros((len(drift_vals), len(n_vals)))

    for d in scan:

        i = drift_vals.index(round(d["drift"],4))
        j = n_vals.index(d["n"])

        grid[i,j] = d["resonance_score"]

    return grid, n_vals, drift_vals


# --------------------------------------------------
# Peak spacing analysis
# --------------------------------------------------

def analyze_peak_spacing(ridges):

    ns = sorted([r["n"] for r in ridges])
    drifts = sorted([r["drift"] for r in ridges])

    n_diffs = np.diff(ns)
    drift_diffs = np.diff(drifts)

    return n_diffs.tolist(), drift_diffs.tolist()


# --------------------------------------------------
# Fourier analysis
# --------------------------------------------------

def compute_fft(grid):

    fft = np.fft.fft2(grid)

    power = np.abs(fft)

    return power


# --------------------------------------------------
# Dominant frequencies
# --------------------------------------------------

def dominant_modes(power, top_n=10):

    flat = power.flatten()

    idx = np.argsort(flat)[::-1][:top_n]

    modes = []

    rows, cols = power.shape

    for i in idx:

        r = i // cols
        c = i % cols

        modes.append({
            "row_mode": int(r),
            "col_mode": int(c),
            "strength": float(flat[i])
        })

    return modes


# --------------------------------------------------
# Plot spectrum
# --------------------------------------------------

def plot_fft(power):

    plt.figure(figsize=(8,6))

    plt.imshow(
        np.log(power + 1),
        origin="lower",
        aspect="auto"
    )

    plt.colorbar(label="log spectral power")

    plt.title("Resonance Field Fourier Spectrum")

    plt.tight_layout()

    plt.savefig(OUT_PLOT, dpi=300)

    print("\nSaved spectrum:", OUT_PLOT)

    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("\nLoading resonance data...")

    scan, ridges = load_data()

    print("Scan records:", len(scan))
    print("Ridges:", len(ridges))

    grid, n_vals, drift_vals = build_grid(scan)

    print("Grid shape:", grid.shape)

    n_diffs, drift_diffs = analyze_peak_spacing(ridges)

    power = compute_fft(grid)

    modes = dominant_modes(power)

    print("\nDominant Harmonic Modes\n")

    for m in modes[:10]:

        print(
            f"mode_n={m['col_mode']}  "
            f"mode_drift={m['row_mode']}  "
            f"strength={m['strength']:.3f}"
        )

    results = {

        "peak_spacing_n": n_diffs,
        "peak_spacing_drift": drift_diffs,
        "dominant_modes": modes
    }

    with open(OUT_JSON,"w") as f:

        json.dump(results,f,indent=2)

    print("\nSaved harmonic analysis:", OUT_JSON)

    plot_fft(power)


if __name__ == "__main__":
    main()
