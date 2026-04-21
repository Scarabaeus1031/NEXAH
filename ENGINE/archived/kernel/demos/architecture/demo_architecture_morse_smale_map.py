"""
NEXAH Architecture Morse-Smale Map

Computes a basin map of the architecture stability landscape.

Each grid cell flows via gradient ascent to a local attractor.
The resulting attractor defines the basin.

Run:
python -m ENGINE.nexah_kernel.demos.demo_architecture_morse_smale_map
"""

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from ENGINE.nexah_kernel.tools.nexah_spectral_stability_score import spectral_stability_score


# --------------------------------------------------
# stability field
# --------------------------------------------------

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
                field[i,j]=np.mean(vals)

    return nodes,probs,field


# --------------------------------------------------
# neighbors
# --------------------------------------------------

def neighbors(i,j,rows,cols):

    out=[]

    for di,dj in [(-1,0),(1,0),(0,-1),(0,1),
                  (-1,-1),(-1,1),(1,-1),(1,1)]:

        ni=i+di
        nj=j+dj

        if 0<=ni<rows and 0<=nj<cols:
            out.append((ni,nj))

    return out


# --------------------------------------------------
# gradient ascent
# --------------------------------------------------

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


# --------------------------------------------------
# basin map
# --------------------------------------------------

def compute_basins(field):

    rows,cols = field.shape

    basin = np.zeros((rows,cols),dtype=int)

    attractors={}
    counter=1

    for i in range(rows):
        for j in range(cols):

            a = attractor(field,(i,j))

            if a not in attractors:
                attractors[a]=counter
                counter+=1

            basin[i,j] = attractors[a]

    return basin,attractors


# --------------------------------------------------
# ridge detection
# --------------------------------------------------

def ridge_mask(basin):

    rows,cols = basin.shape
    mask = np.zeros_like(basin)

    for i in range(rows):
        for j in range(cols):

            b = basin[i,j]

            for n in neighbors(i,j,rows,cols):

                if basin[n] != b:
                    mask[i,j] = 1
                    break

    return mask


# --------------------------------------------------
# visualization
# --------------------------------------------------

def plot(nodes,probs,basin,ridge):

    os.makedirs("ENGINE/nexah_kernel/demos/visuals",exist_ok=True)

    extent=[probs.min(),probs.max(),nodes.min(),nodes.max()]

    plt.figure(figsize=(10,7))

    plt.imshow(
        basin,
        origin="lower",
        extent=extent,
        aspect="auto",
        cmap="tab20"
    )

    ys,xs = np.where(ridge==1)

    plt.scatter(
        probs[xs],
        nodes[ys],
        s=10,
        color="black"
    )

    plt.title("Architecture Morse-Smale Basin Map")

    plt.xlabel("Edge Probability")
    plt.ylabel("Number of Nodes")

    plt.tight_layout()

    out="ENGINE/nexah_kernel/demos/visuals/architecture_morse_smale_map.png"

    plt.savefig(out,dpi=180)

    print("\nSaved:",out)

    plt.show()


# --------------------------------------------------
# run
# --------------------------------------------------

def run():

    print("\ncomputing stability field...\n")

    nodes,probs,field = compute_field()

    print("computing basins...\n")

    basin,attr = compute_basins(field)

    ridge = ridge_mask(basin)

    print("attractors:",len(attr))

    plot(nodes,probs,basin,ridge)


if __name__=="__main__":
    run()
