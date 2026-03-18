"""
NEXAH Symmetry Graph – Torus Resonance
--------------------------------------

Visualizes a resonance flow on a torus surface.

Phases:
    phi_A
    phi_B
    phi_C

phi_A, phi_B define the torus coordinates
phi_C modulates the resonance structure.

Energy:
    -cos(phi_A - phi_B)
    -cos(phi_A - phi_C)
    -cos(phi_B - phi_C)
    -cos(phi_A + phi_B - phi_C)

Output:
- 3D torus
- resonance color field
- phase trajectories
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# energy
# --------------------------------------------------

def resonance_energy(a,b,c):

    return (
        -np.cos(a-b)
        -0.8*np.cos(a-c)
        -0.8*np.cos(b-c)
        -1.2*np.cos(a+b-c)
    )


# --------------------------------------------------
# torus geometry
# --------------------------------------------------

def torus_coordinates(u,v,R=3,r=1):

    x=(R+r*np.cos(v))*np.cos(u)
    y=(R+r*np.cos(v))*np.sin(u)
    z=r*np.sin(v)

    return x,y,z


# --------------------------------------------------
# trajectory simulation
# --------------------------------------------------

def simulate(start,steps=600,dt=0.04):

    a,b,c=start

    traj=[]

    for _ in range(steps):

        dA= np.sin(a-b)+np.sin(a-c)+np.sin(a+b-c)
        dB=-np.sin(a-b)+np.sin(b-c)+np.sin(a+b-c)
        dC=-np.sin(a-c)-np.sin(b-c)-np.sin(a+b-c)

        a=(a-dt*dA+np.pi)%(2*np.pi)-np.pi
        b=(b-dt*dB+np.pi)%(2*np.pi)-np.pi
        c=(c-dt*dC+np.pi)%(2*np.pi)-np.pi

        traj.append((a,b,c))

    return np.array(traj)


# --------------------------------------------------
# main
# --------------------------------------------------

def main():

    print("Computing torus resonance...")

    grid=140

    u=np.linspace(-np.pi,np.pi,grid)
    v=np.linspace(-np.pi,np.pi,grid)

    U,V=np.meshgrid(u,v)

    phi_c=0.8

    E=resonance_energy(U,V,phi_c)

    X,Y,Z=torus_coordinates(U,V)

    fig=plt.figure(figsize=(10,8))
    ax=fig.add_subplot(111,projection='3d')

    surf=ax.plot_surface(
        X,Y,Z,
        facecolors=plt.cm.viridis((E-E.min())/(E.max()-E.min())),
        rstride=1,
        cstride=1,
        linewidth=0,
        antialiased=False,
        alpha=0.9
    )

    # trajectories

    seeds=[
        (0.2,-1.5,1.2),
        (-2.1,0.4,-1.0),
        (1.3,2.2,-2.0)
    ]

    for s in seeds:

        traj=simulate(s)

        a=traj[:,0]
        b=traj[:,1]

        x,y,z=torus_coordinates(a,b)

        ax.plot(x,y,z,linewidth=2)

    ax.set_title("Resonance Flow on Torus")

    plt.show()


if __name__=="__main__":
    main()
