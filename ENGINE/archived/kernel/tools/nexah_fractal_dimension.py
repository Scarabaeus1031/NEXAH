"""
NEXAH Fractal Dimension
=======================

Estimates fractal dimension of resonance attractor.

Output
------
ENGINE/nexah_kernel/demos/visuals/resonance_landscape/fractal_dimension.png
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


OUT_IMG = Path(
"ENGINE/nexah_kernel/demos/visuals/resonance_landscape/fractal_dimension.png"
)

OUT_IMG.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# dynamics
# --------------------------------------------------

def step(theta,n,drift):

    return (theta + (2*np.pi)/n + np.deg2rad(drift))%(2*np.pi)


# --------------------------------------------------
# trajectory
# --------------------------------------------------

def simulate(n,drift,steps=10000):

    theta=np.random.rand()*2*np.pi

    traj=[]

    for _ in range(steps):

        theta=step(theta,n,drift)
        traj.append(theta)

    return np.array(traj)


# --------------------------------------------------
# box counting
# --------------------------------------------------

def fractal_dimension(data):

    sizes=np.logspace(-2,-0.2,10)

    counts=[]

    for s in sizes:

        bins=int(1/s)

        hist,_=np.histogram(data,bins=bins)

        counts.append(np.sum(hist>0))

    sizes=np.array(sizes)
    counts=np.array(counts)

    coeff=np.polyfit(np.log(1/sizes),np.log(counts),1)

    return coeff[0],sizes,counts


# --------------------------------------------------
# plot
# --------------------------------------------------

def plot():

    data=simulate(9,2.5)

    D,sizes,counts=fractal_dimension(data)

    plt.figure(figsize=(8,6))

    plt.scatter(np.log(1/sizes),np.log(counts))

    plt.title(f"NEXAH Fractal Dimension ≈ {D:.3f}")

    plt.xlabel("log(1/box size)")
    plt.ylabel("log(box count)")

    plt.tight_layout()

    plt.savefig(OUT_IMG,dpi=300)

    print("\nFractal dimension ≈",D)

    print("Saved:",OUT_IMG)

    plt.show()


def main():

    print("\nEstimating fractal dimension...\n")

    plot()


if __name__=="__main__":
    main()
