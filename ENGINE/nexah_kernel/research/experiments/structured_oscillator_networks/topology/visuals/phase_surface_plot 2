"""
NEXAH Experiment Tool
Phase Surface Visualization

Purpose
-------
Visualize the phase surface of each oscillator ring
over time to observe twist, shear and phase slips.

Inputs
------
output/phase_history.npy

Outputs
-------
output/phase_surface_inner.png
output/phase_surface_middle.png
output/phase_surface_outer.png
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------
# Utilities
# ------------------------------------------------
def wrap_angle(x):
    return (x + np.pi) % (2*np.pi) - np.pi


# ------------------------------------------------
# Load data
# ------------------------------------------------
def load_history():

    path = Path("output/phase_history.npy")

    if not path.exists():
        raise RuntimeError("Missing output/phase_history.npy")

    return np.load(path)


# ------------------------------------------------
# Split layers
# ------------------------------------------------
def split_layers(history, n_inner=16, n_middle=32, n_outer=16):

    inner = history[:, :n_inner]
    middle = history[:, n_inner:n_inner+n_middle]
    outer = history[:, n_inner+n_middle:n_inner+n_middle+n_outer]

    return inner, middle, outer


# ------------------------------------------------
# Plot surface
# ------------------------------------------------
def plot_surface(data, title, filename):

    plt.figure(figsize=(10,5))

    plt.imshow(
        wrap_angle(data).T,
        aspect="auto",
        origin="lower",
        cmap="twilight"
    )

    plt.xlabel("time step")
    plt.ylabel("ring index")

    plt.title(title)

    plt.colorbar(label="phase")

    plt.tight_layout()

    plt.savefig(filename, dpi=300)

    plt.show()


# ------------------------------------------------
# Main
# ------------------------------------------------
def main():

    Path("output").mkdir(exist_ok=True)

    history = load_history()

    inner, middle, outer = split_layers(history)

    plot_surface(inner,  "Inner ring phase surface",  "output/phase_surface_inner.png")
    plot_surface(middle, "Middle ring phase surface", "output/phase_surface_middle.png")
    plot_surface(outer,  "Outer ring phase surface",  "output/phase_surface_outer.png")

    print("Phase surface plots saved.")


if __name__ == "__main__":
    main()
