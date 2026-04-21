"""
NEXAH Symmetry Graph – Kernel Bridge
------------------------------------

Integrated bridge script for the symmetry graph experiments.

Modes:
    spectral   -> Laplacian spectrum
    dynamics   -> Kuramoto synchronization
    energy     -> reduced resonance energy landscape
    basin      -> basin-of-attraction map

Usage:
    python -m ENGINE.nexah_kernel.research.experiments.symmetry_graph_experiment.symmetry_graph_kernel_bridge
    python -m ENGINE.nexah_kernel.research.experiments.symmetry_graph_experiment.symmetry_graph_kernel_bridge --mode spectral
    python -m ENGINE.nexah_kernel.research.experiments.symmetry_graph_experiment.symmetry_graph_kernel_bridge --mode dynamics
    python -m ENGINE.nexah_kernel.research.experiments.symmetry_graph_experiment.symmetry_graph_kernel_bridge --mode energy
    python -m ENGINE.nexah_kernel.research.experiments.symmetry_graph_experiment.symmetry_graph_kernel_bridge --mode basin
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


# --------------------------------------------------
# Graph construction
# --------------------------------------------------

def build_symmetry_graph():

    G = nx.Graph()

    hubs = ["hub_A", "hub_B"]
    ringA = [f"A{i}" for i in range(8)]
    ringB = [f"B{i}" for i in range(8)]

    G.add_nodes_from(hubs + ringA + ringB)

    for i in range(8):
        G.add_edge(ringA[i], ringA[(i+1)%8])
        G.add_edge(ringB[i], ringB[(i+1)%8])

    for n in ringA:
        G.add_edge("hub_A", n)

    for n in ringB:
        G.add_edge("hub_B", n)

    for i in range(8):
        G.add_edge(ringA[i], ringB[i])

    G.add_edge("hub_A", "hub_B")

    return G


# --------------------------------------------------
# Spectral mode
# --------------------------------------------------

def spectral_mode(G):

    L = nx.laplacian_matrix(G).toarray()

    vals, vecs = np.linalg.eigh(L)

    plt.figure(figsize=(6,4))
    plt.plot(vals, "o-")
    plt.title("Laplacian Spectrum")
    plt.xlabel("mode index")
    plt.ylabel("eigenvalue")
    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Kuramoto dynamics
# --------------------------------------------------

def kuramoto_dynamics(G, steps=400, dt=0.05, K=0.8):

    N = len(G.nodes())
    nodes = list(G.nodes())
    index = {n:i for i,n in enumerate(nodes)}

    theta = np.random.uniform(-np.pi, np.pi, N)
    omega = np.random.normal(0, 0.1, N)

    edges = [(index[a], index[b]) for a,b in G.edges()]

    R = []

    for _ in range(steps):

        dtheta = omega.copy()

        for i,j in edges:
            dtheta[i] += K * np.sin(theta[j]-theta[i])
            dtheta[j] += K * np.sin(theta[i]-theta[j])

        theta += dt*dtheta

        r = abs(np.mean(np.exp(1j*theta)))
        R.append(r)

    plt.figure(figsize=(6,4))
    plt.plot(R)
    plt.title("Kuramoto Synchronization R(t)")
    plt.xlabel("step")
    plt.ylabel("order parameter")
    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Resonance energy
# --------------------------------------------------

def resonance_energy(phi_a, phi_b):

    K11 = 1.0
    K21 = 0.25
    K32 = 0.18
    K53 = 0.10

    Ea = -0.7*np.cos(phi_a)
    Eb = -0.7*np.cos(phi_b)

    E11 = -K11*np.cos(phi_a-phi_b)
    E21 = -K21*np.cos(2*phi_a-phi_b)
    E32 = -K32*np.cos(3*phi_a-2*phi_b)
    E53 = -K53*np.cos(5*phi_a-3*phi_b)

    return Ea+Eb+E11+E21+E32+E53


# --------------------------------------------------
# Energy landscape
# --------------------------------------------------

def energy_mode():

    n = 200

    phi = np.linspace(-np.pi, np.pi, n)
    X,Y = np.meshgrid(phi,phi)

    Z = resonance_energy(X,Y)

    plt.figure(figsize=(6,5))

    plt.contourf(X,Y,Z,levels=40)
    plt.colorbar(label="energy")

    plt.xlabel("phi_A")
    plt.ylabel("phi_B")
    plt.title("Resonance Energy Landscape")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Basin flow helpers
# --------------------------------------------------

def wrap(x):
    return (x + np.pi) % (2*np.pi) - np.pi


def gradient(phi_a, phi_b):

    K11=1.0
    K21=0.25
    K32=0.18
    K53=0.10

    dA = (
        0.7*np.sin(phi_a)
        + K11*np.sin(phi_a-phi_b)
        + 2*K21*np.sin(2*phi_a-phi_b)
        + 3*K32*np.sin(3*phi_a-2*phi_b)
        + 5*K53*np.sin(5*phi_a-3*phi_b)
    )

    dB = (
        0.7*np.sin(phi_b)
        - K11*np.sin(phi_a-phi_b)
        - K21*np.sin(2*phi_a-phi_b)
        - 2*K32*np.sin(3*phi_a-2*phi_b)
        - 3*K53*np.sin(5*phi_a-3*phi_b)
    )

    return dA,dB


# --------------------------------------------------
# Basin map
# --------------------------------------------------

def basin_mode():

    n = 120
    phi = np.linspace(-np.pi, np.pi, n)

    basin = np.zeros((n,n))

    for i,a in enumerate(phi):
        for j,b in enumerate(phi):

            pa=a
            pb=b

            for _ in range(120):

                dA,dB = gradient(pa,pb)

                pa -= 0.05*dA
                pb -= 0.05*dB

                pa = wrap(pa)
                pb = wrap(pb)

            basin[j,i] = 1 if abs(pa-pb) < 0.2 else 0

    plt.figure(figsize=(6,5))

    plt.imshow(
        basin,
        origin="lower",
        extent=[-np.pi,np.pi,-np.pi,np.pi],
        interpolation="nearest"
    )

    plt.xlabel("phi_A")
    plt.ylabel("phi_B")
    plt.title("Basin of Attraction Map")

    plt.colorbar(label="lock")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="energy")

    args = parser.parse_args()

    G = build_symmetry_graph()

    if args.mode=="spectral":
        spectral_mode(G)

    elif args.mode=="dynamics":
        kuramoto_dynamics(G)

    elif args.mode=="energy":
        energy_mode()

    elif args.mode=="basin":
        basin_mode()

    else:
        print("Unknown mode")


if __name__ == "__main__":
    main()
