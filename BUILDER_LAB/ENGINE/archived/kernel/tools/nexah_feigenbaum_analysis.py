"""
NEXAH Feigenbaum Analysis
=========================

Searches for period doubling sequences
and estimates Feigenbaum delta.

Input
-----
rotation_numbers.json

Output
------
feigenbaum_estimate.json
feigenbaum_plot.png
"""

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt


ROT_FILE = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/rotation_numbers.json"
)

OUT_JSON = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/feigenbaum_estimate.json"
)

OUT_IMG = Path(
    "ENGINE/nexah_kernel/demos/visuals/resonance_landscape/feigenbaum_plot.png"
)

OUT_IMG.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load data
# --------------------------------------------------

def load_data():

    with open(ROT_FILE) as f:
        return json.load(f)


# --------------------------------------------------
# Extract drift slices
# --------------------------------------------------

def extract_series(data):

    drifts = sorted({d["drift"] for d in data})

    series = {}

    for drift in drifts:

        seq = [d["rotation_number"] for d in data if d["drift"] == drift]

        series[drift] = seq

    return series


# --------------------------------------------------
# Detect period changes
# --------------------------------------------------

def detect_periods(seq):

    diffs = np.abs(np.diff(seq))

    peaks = np.where(diffs > np.mean(diffs)*2)[0]

    return peaks


# --------------------------------------------------
# Estimate Feigenbaum delta
# --------------------------------------------------

def estimate_delta(points):

    deltas = []

    for i in range(len(points)-2):

        a = points[i]
        b = points[i+1]
        c = points[i+2]

        if (b-a) != 0:
            delta = (c-b)/(b-a)
            deltas.append(delta)

    return deltas


# --------------------------------------------------
# Plot
# --------------------------------------------------

def plot_series(series):

    plt.figure(figsize=(10,6))

    for drift, seq in list(series.items())[:10]:

        plt.plot(seq, alpha=0.6)

    plt.title("NEXAH Period Evolution")

    plt.xlabel("Symmetry index")
    plt.ylabel("Rotation number")

    plt.tight_layout()

    plt.savefig(OUT_IMG, dpi=300)

    print("Saved Feigenbaum plot:", OUT_IMG)

    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("\nRunning Feigenbaum analysis...\n")

    data = load_data()

    series = extract_series(data)

    all_deltas = []

    for drift, seq in series.items():

        peaks = detect_periods(seq)

        deltas = estimate_delta(peaks)

        all_deltas += deltas

    if all_deltas:

        estimate = np.mean(all_deltas)

    else:

        estimate = None

    result = {
        "feigenbaum_estimate": estimate,
        "samples": len(all_deltas)
    }

    with open(OUT_JSON,"w") as f:

        json.dump(result,f,indent=2)

    print("\nFeigenbaum estimate:", estimate)

    plot_series(series)


if __name__ == "__main__":
    main()
