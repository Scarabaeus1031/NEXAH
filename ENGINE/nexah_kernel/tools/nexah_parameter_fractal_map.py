"""
NEXAH Parameter Fractal Map
===========================

Scans parameter space (symmetry n, drift)
and measures trajectory complexity.

Produces Mandelbrot-like parameter fractal.

Output
------
ENGINE/nexah_kernel/demos/visuals/resonance_landscape/parameter_fractal_map.png
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


OUT_IMG = Path(
"ENGINE/nexah_kernel/demos/visuals/resonance_landscape/parameter_fractal_map.png"
)

OUT_IMG.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# NEXAH dynamics
# --------------------------------------------------

def step(theta,n,drift):

    return (theta + (2*np.pi)/n + np.deg2rad(drift))%(2*np.pi)


# --------------------------------------------------
# complexity metric
# --------------------------------------------------

def complexity(n,drift,steps=3000):

    theta=0.1

    traj=[]

    for _ in range(steps):

        theta=step(theta,n,drift)
        traj.append(theta)

    traj=np.array(traj)

    # variance = rough complexity estimate
    return np.var(traj)


# --------------------------------------------------
# parameter scan
# --------------------------------------------------

def compute():

    n_vals=np.linspace(3,20,200)

    drift_vals=np.linspace(0,6,200)

    grid=np.zeros((len(drift_vals),len(n_vals)))

    for i,drift in enumerate(drift_vals):

        for j,n in enumerate(n_vals):

            grid[i,j]=complexity(n,drift)

    return grid,n_vals,drift_vals


# --------------------------------------------------
# plot
# --------------------------------------------------

def plot():

    grid,n_vals,drift_vals=compute()

    plt.figure(figsize=(10,6))

    im=plt.imshow(
        grid,
        origin="lower",
        aspect="auto",
        cmap="inferno"
    )

    plt.colorbar(im,label="Trajectory complexity")

    plt.xlabel("Symmetry (n)")
    plt.ylabel("Drift")

    plt.title("NEXAH Parameter Fractal Map")

    plt.tight_layout()

    plt.savefig(OUT_IMG,dpi=300)

    print("\nSaved parameter fractal:",OUT_IMG)

    plt.show()


def main():

    print("\nComputing parameter fractal map...\n")

    plot()


if __name__=="__main__":
    main()
