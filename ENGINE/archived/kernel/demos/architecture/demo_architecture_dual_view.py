"""
NEXAH Architecture Dual View
============================

Creates TWO complementary visualizations:

1. Basin map (Morse-Smale style partition)
2. 3D stability landscape with attractor nodes

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_dual_view
"""

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from ENGINE.nexah_kernel.tools.nexah_spectral_stability_score import spectral_stability_score


# ---------------------------------------------------------
# stability field
# ---------------------------------------------------------

def compute_field():

    nodes = np.arange(4,15)
    probs = np.linspace(0.05,0.9,17)

    field = np.zeros((len(nodes),len(probs)))

    for i,n in enumerate(nodes):
        for j,p in enumerate(probs):

            vals=[]

            for _ in range(20):

                G = nx.erdos_renyi_graph(int(n),float(p))

                if G.number_of_edges()==0:
                    continue

                vals.append(spectral_stability_score(G))

            if vals:
                field[i,j] = np.mean(vals)

    return nodes,probs,field


# ---------------------------------------------------------
# neighbors
# ---------------------------------------------------------

def neighbors(i,j,rows,cols):

    out=[]

    for di,dj in [(-1,0),(1,0),(0,-1),(0,1),
                  (-1,-1),(-1,1),(1,-1),(1,1)]:

        ni=i+di
        nj=j+dj

        if 0<=ni<rows and 0<=nj<cols:
            out.append((ni,nj))

    return out


# ---------------------------------------------------------
# gradient attractor
# ---------------------------------------------------------

def attractor(field,start):

    rows,cols = field.shape
    cur = start

    while True:

        neigh = neighbors(cur[0],cur[1],rows,cols)

        best = cur
        best_val = field[cur]

        for n in neigh:
            if field[n] > best_val:
                best = n
                best_val = field[n]

        if best == cur:
            return cur

        cur = best


# ---------------------------------------------------------
# basin map
# ---------------------------------------------------------

def basin_map(field):

    rows,cols = field.shape
    basin = np.zeros((rows,cols),dtype=int)

    attractors={}
    idx=1

    for i in range(rows):
        for j in range(cols):

            a = attractor(field,(i,j))

            if a not in attractors:
                attractors[a]=idx
                idx+=1

            basin[i,j] = attractors[a]

    return basin,attractors


# ---------------------------------------------------------
# VISUAL 1
# ---------------------------------------------------------

def plot_basin(nodes,probs,basin):

    extent=[probs.min(),probs.max(),nodes.min(),nodes.max()]

    plt.figure(figsize=(9,6))

    plt.imshow(
        basin,
        origin="lower",
        extent=extent,
        aspect="auto",
        cmap="tab20"
    )

    plt.title("Architecture Basin Map")

    plt.xlabel("Edge Probability")
    plt.ylabel("Number of Nodes")

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# VISUAL 2
# ---------------------------------------------------------

def plot_landscape(nodes,probs,field,attractors):

    P,N = np.meshgrid(probs,nodes)

    fig=plt.figure(figsize=(10,7))
    ax=fig.add_subplot(111,projection="3d")

    ax.plot_surface(
        P,N,field,
        cmap="viridis",
        alpha=0.85
    )

    for (i,j) in attractors:

        ax.scatter(
            probs[j],
            nodes[i],
            field[i,j],
            color="red",
            s=80
        )

    ax.set_title("Architecture Stability Landscape")

    ax.set_xlabel("Edge Probability")
    ax.set_ylabel("Number of Nodes")
    ax.set_zlabel("Spectral Stability")

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# run
# ---------------------------------------------------------

def run():

    print("\ncomputing stability field\n")

    nodes,probs,field = compute_field()

    print("computing basins\n")

    basin,attractors = basin_map(field)

    print("attractors:",len(attractors))

    plot_basin(nodes,probs,basin)

    plot_landscape(nodes,probs,field,attractors)


if __name__=="__main__":
    run()
