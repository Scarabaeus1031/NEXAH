"""
Lorenz FTLE Map
Part of the NEXAH Chaos Navigator
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


OUTPUT_DIR = Path("../../outputs/lorenz_navigation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    """
    Entry point used by the NEXAH Chaos Navigator.
    """

    print("Running Lorenz FTLE map")

    # Dummy FTLE field (placeholder)
    x = np.linspace(-20, 20, 200)
    y = np.linspace(-30, 30, 200)
    X, Y = np.meshgrid(x, y)

    Z = np.sin(X / 5) * np.cos(Y / 7)

    plt.figure(figsize=(8, 6))
    plt.imshow(
        Z,
        origin="lower",
        extent=[x.min(), x.max(), y.min(), y.max()],
        cmap="inferno",
        aspect="auto",
    )

    plt.colorbar(label="FTLE")
    plt.title("Lorenz FTLE Field")

    output_file = OUTPUT_DIR / "lorenz_ftle_map.png"
    plt.savefig(output_file, dpi=200)
    plt.close()

    print("FTLE map saved to:", output_file)


if __name__ == "__main__":
    main()
