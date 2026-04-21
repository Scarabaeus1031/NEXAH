"""
NEXAH Architecture Flow Rivers 3D
=================================

3D visualization of the architecture stability landscape
with gradient-flow trajectories ("rivers").

Axes
x = edge probability
y = number of nodes
z = mean spectral stability (λ₂ / λmax)

Run

python -m ENGINE.nexah_kernel.demos.demo_architecture_flow_rivers_3D
"""

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from ENGINE.nexah_kernel.tools.nexah_spectral_stability_score import spectral_stability_score


# --------------------------------------------------
# stability field
# --------------------------------------------------

def compute_stability():

    node_values = np.arange(4,15)
    prob_values = np.linspace(0.05,0.9,17)

    field = np.zeros((len(node_values),len(prob_values)))

    for i,n in enumerate(node_values):
        for j,p in enumerate(prob_values):

            vals = []

            for _ in range(20):

                G = nx.erdos_renyi_graph(int(n),float(p))

                if G.number_of_edges()==0:
                    continue

                vals.append(spectral_stability_score(G))

            if vals:
                field[i,j] = np.mean(vals)

    return node_values,prob_values,field


# --------------------------------------------------
# neighborhood
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
# gradient ascent path
# --------------------------------------------------

def flow_path(field,start):

    rows,cols=field.shape

    current=start
    path=[current]

    while True:

        neigh=neighbors(current[0],current[1],rows,cols)

        best=current
        best_val=field[current]

        for n in neigh:

            if field[n]>best_val:
                best=n
                best_val=field[n]

        if best==current:
            break

        current=best
        path.append(current)

    return path


# --------------------------------------------------
# sample start points
# --------------------------------------------------

def sample_points(rows,cols):

    pts=[]

    for i in range(0,rows,2):
        for j in range(0,cols,2):
            pts.append((i,j))

    return pts


# --------------------------------------------------
# visualization
# --------------------------------------------------

def plot_rivers(nodes,probs,field):

    os.makedirs("ENGINE/nexah_kernel/demos/visuals",exist_ok=True)

    P,N=np.meshgrid(probs,nodes)

    fig=plt.figure(figsize=(11,8))
    ax=fig.add_subplot(111,projection="3d")

    ax.plot_surface(
        P,N,field,
        cmap="viridis",
        alpha=0.8
    )

    rows,cols=field.shape

    starts=sample_points(rows,cols)

    for s in starts:

        path=flow_path(field,s)

        xs=[]
        ys=[]
        zs=[]

        for i,j in path:

            xs.append(probs[j])
            ys.append(nodes[i])
            zs.append(field[i,j])

        ax.plot(xs,ys,zs,color="white",linewidth=1)

    ax.set_title("Architecture Flow Rivers (3D)")
    ax.set_xlabel("Edge Probability")
    ax.set_ylabel("Number of Nodes")
    ax.set_zlabel("Spectral Stability")

    plt.tight_layout()

    out="ENGINE/nexah_kernel/demos/visuals/architecture_flow_rivers_3D.png"

    plt.savefig(out,dpi=180)

    print("\nSaved to:",out)

    plt.show()


# --------------------------------------------------
# run
# --------------------------------------------------

def run():

    print("\ncomputing stability field...\n")

    nodes,probs,field=compute_stability()

    print("rendering rivers...\n")

    plot_rivers(nodes,probs,field)


if __name__=="__main__":
    run()
