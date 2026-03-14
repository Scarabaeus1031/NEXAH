import sys
from pathlib import Path

# --- make project root importable ---
ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

import numpy as np
import matplotlib.pyplot as plt

from APPLICATIONS.dynamical_systems.lorenz.analysis.lorenz_ftle_map import ftle_field
from APPLICATIONS.dynamical_systems.lorenz.regimes.lorenz_switch_heatmap import compute_switch_points
from APPLICATIONS.dynamical_systems.lorenz.attractor.lorenz_density_map import generate_trajectory


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

    # save image
    out = ROOT / "APPLICATIONS/outputs/lorenz_navigation/chaos_navigation_map.png"
    plt.savefig(out, dpi=300)

    print("Saved:", out)

    plt.show()


if __name__ == "__main__":
    chaos_navigation_map()
