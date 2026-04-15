import sys
from pathlib import Path

# --- ensure local lorenz modules are importable ---
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

import numpy as np
import matplotlib.pyplot as plt

from analysis.lorenz_ftle_map import ftle_field
from regimes.lorenz_switch_heatmap import compute_switch_points
from attractor.lorenz_density_map import generate_trajectory


def chaos_navigation_map():

    print("Generating Chaos Navigation Map...")

    xs, zs, ftle = ftle_field()

    traj = generate_trajectory(20000)
    switch = compute_switch_points(traj)

    plt.figure(figsize=(8,8))

    # FTLE skeleton
    plt.imshow(
        ftle.T,
        extent=[xs.min(), xs.max(), zs.min(), zs.max()],
        origin="lower",
        cmap="inferno",
        alpha=0.6
    )

    # trajectory cloud
    plt.scatter(
        traj[:,0],
        traj[:,2],
        s=0.1,
        alpha=0.15,
        color="cyan"
    )

    # regime switches
    plt.scatter(
        switch[:,0],
        switch[:,2],
        s=5,
        color="red"
    )

    plt.title("NEXAH Chaos Navigation Map")
    plt.xlabel("x")
    plt.ylabel("z")

    plt.tight_layout()

    # save output
    out_dir = BASE_DIR / "../outputs/lorenz_navigation"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / "chaos_navigation_map.png"
    plt.savefig(out_file, dpi=300)

    print("Saved:", out_file)

    plt.show()


if __name__ == "__main__":
    chaos_navigation_map()
