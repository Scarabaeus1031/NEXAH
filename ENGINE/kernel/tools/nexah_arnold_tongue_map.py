"""
NEXAH Arnold Tongue Map
=======================

Detects frequency locking regions (Arnold tongues)
from the rotation number field.

Input
-----
rotation_numbers.json

Output
------
arnold_tongues.png
"""

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction


ROT_FILE = Path(
    "ENGINE/nexah_kernel/demos/data/resonance_discovery/rotation_numbers.json"
)

OUT_IMG = Path(
    "ENGINE/nexah_kernel/demos/visuals/resonance_landscape/arnold_tongues.png"
)

OUT_IMG.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load rotation numbers
# --------------------------------------------------

def load_data():

    with open(ROT_FILE) as f:
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

        grid[i,j] = d["rotation_number"]

    return grid, n_vals, drift_vals


# --------------------------------------------------
# Detect rational locking
# --------------------------------------------------

def rational_lock(value, tol=1e-4):

    frac = Fraction(value).limit_denominator(10)

    if abs(value - frac.numerator/frac.denominator) < tol:
        return frac.numerator, frac.denominator

    return None


def build_locking_map(rot_grid):

    lock_grid = np.zeros_like(rot_grid)

    rows, cols = rot_grid.shape

    for i in range(rows):
        for j in range(cols):

            r = rot_grid[i,j]

            lock = rational_lock(r)

            if lock:

                p,q = lock
                lock_grid[i,j] = q

    return lock_grid


# --------------------------------------------------
# Plot
# --------------------------------------------------

def plot_map(lock_grid):

    plt.figure(figsize=(10,6))

    plt.imshow(lock_grid, origin="lower", aspect="auto")

    plt.colorbar(label="Locking denominator (q)")

    plt.title("NEXAH Arnold Tongue Map")

    plt.xlabel("Symmetry (n)")
    plt.ylabel("Drift")

    plt.tight_layout()

    plt.savefig(OUT_IMG, dpi=300)

    print("Saved Arnold tongue map:", OUT_IMG)

    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("\nDetecting Arnold tongues...\n")

    data = load_data()

    rot_grid, n_vals, drift_vals = build_grid(data)

    lock_grid = build_locking_map(rot_grid)

    plot_map(lock_grid)


if __name__ == "__main__":
    main()
