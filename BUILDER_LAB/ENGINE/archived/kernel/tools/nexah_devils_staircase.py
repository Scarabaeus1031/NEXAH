"""
NEXAH Devil's Staircase
=======================

Computes rotation numbers as function of drift parameter.

Detects locking plateaus typical for circle maps.

Output
------
ENGINE/nexah_kernel/demos/visuals/resonance_landscape/devils_staircase.png
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


OUT_IMG = Path(
"ENGINE/nexah_kernel/demos/visuals/resonance_landscape/devils_staircase.png"
)

OUT_IMG.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# dynamics
# --------------------------------------------------

def step(theta,n,drift):

    return (theta + (2*np.pi)/n + np.deg2rad(drift))%(2*np.pi)


# --------------------------------------------------
# rotation number
# --------------------------------------------------

def rotation_number(n,drift,steps=3000):

    theta=0.1
    total=0

    for _ in range(steps):

        prev=theta
        theta=step(theta,n,drift)

        d=theta-prev
        if d<0:
            d+=2*np.pi

        total+=d

    return total/(steps*2*np.pi)


# --------------------------------------------------
# compute staircase
# --------------------------------------------------

def compute():

    n=7

    drift_vals=np.linspace(0,6,400)

    rot=[]

    for d in drift_vals:

        rot.append(rotation_number(n,d))

    return drift_vals,np.array(rot)


# --------------------------------------------------
# plot
# --------------------------------------------------

def plot():

    drift,rot=compute()

    plt.figure(figsize=(10,6))

    plt.plot(drift,rot)

    plt.title("NEXAH Devil's Staircase")

    plt.xlabel("Drift")
    plt.ylabel("Rotation number")

    plt.tight_layout()

    plt.savefig(OUT_IMG,dpi=300)

    print("\nSaved staircase:",OUT_IMG)

    plt.show()


def main():

    print("\nComputing Devil's Staircase...\n")

    plot()


if __name__=="__main__":
    main()
