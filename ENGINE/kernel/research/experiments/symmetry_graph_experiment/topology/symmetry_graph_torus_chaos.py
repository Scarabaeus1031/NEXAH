"""
NEXAH Symmetry Graph – Chaotic Arnold Web
-----------------------------------------
Demonstrates resonance overlap and fractal phase space.
"""

import numpy as np
import matplotlib.pyplot as plt


def energy(a,b):

    eps = 0.6

    return (
        -np.cos(a-b)
        -0.5*np.cos(2*a-b)
        -eps*np.cos(3*a-2*b)
    )


def gradient(a,b):

    eps = 0.6

    dA = (
        np.sin(a-b)
        +2*np.sin(2*a-b)
        +3*eps*np.sin(3*a-2*b)
    )

    dB = (
        -np.sin(a-b)
        -np.sin(2*a-b)
        -2*eps*np.sin(3*a-2*b)
    )

    return dA,dB


def simulate(start,steps=800,dt=0.03):

    a,b=start

    traj=[]

    for _ in range(steps):

        dA,dB=gradient(a,b)

        a=(a-dt*dA+np.pi)%(2*np.pi)-np.pi
        b=(b-dt*dB+np.pi)%(2*np.pi)-np.pi

        traj.append((a,b))

    return np.array(traj)


def main():

    seeds=[
        (0.1,0.2),
        (1.3,-1.0),
        (-2.0,1.5),
        (2.5,2.2)
    ]

    plt.figure(figsize=(6,6))

    for s in seeds:

        traj=simulate(s)

        plt.plot(
            traj[:,0],
            traj[:,1],
            linewidth=1
        )

    plt.xlabel("phi_A")
    plt.ylabel("phi_B")
    plt.title("Chaotic Arnold Web")

    plt.show()


if __name__=="__main__":
    main()
