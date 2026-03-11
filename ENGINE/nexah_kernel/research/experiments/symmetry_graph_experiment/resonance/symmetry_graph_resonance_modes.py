"""
NEXAH Symmetry Graph – Resonance Modes
--------------------------------------

Computes spectral modes of the symmetry graph using the graph Laplacian.

Outputs:
- Laplacian eigenvalues
- resonance mode visualizations
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


# --------------------------------------------------
# Build symmetry graph
# --------------------------------------------------

def build_symmetry_graph():

    G = nx.Graph()

    G.add_node("hub_A")
    G.add_node("hub_B")
    G.add_edge("hub_A","hub_B")

    C5 = [f"C5_{i}" for i in range(5)]
    for i in range(5):
        G.add_edge(C5[i],C5[(i+1)%5])

    C6A = [f"C6A_{i}" for i in range(6)]
    for i in range(6):
        G.add_edge(C6A[i],C6A[(i+1)%6])

    C6B = [f"C6B_{i}" for i in range(6)]
    for i in range(6):
        G.add_edge(C6B[i],C6B[(i+1)%6])

    for n in C5:
        G.add_edge("hub_A",n)

    for n in C6A:
        G.add_edge("hub_A",n)

    for n in C6B:
        G.add_edge("hub_B",n)

    return G


# --------------------------------------------------
# Resonance modes
# --------------------------------------------------

def compute_resonance_modes(G):

    nodes=list(G.nodes())

    L=nx.laplacian_matrix(G,nodelist=nodes).todense()

    eigenvals,eigenvecs=np.linalg.eigh(L)

    return eigenvals,eigenvecs,nodes


# --------------------------------------------------
# Visualization
# --------------------------------------------------

def plot_modes(G,eigenvals,eigenvecs,nodes,num_modes=6):

    pos=nx.spring_layout(G,seed=42)

    fig,axs=plt.subplots(2,3,figsize=(12,8))

    axs=axs.flatten()

    for m in range(num_modes):

        ax=axs[m]

        mode=eigenvecs[:,m]

        nx.draw_networkx_edges(G,pos,ax=ax,alpha=0.4)

        nx.draw_networkx_nodes(
            G,
            pos,
            node_color=mode,
            cmap="coolwarm",
            node_size=400,
            ax=ax
        )

        nx.draw_networkx_labels(G,pos,font_size=8,ax=ax)

        ax.set_title(f"Mode {m}  λ={eigenvals[m]:.3f}")
        ax.axis("off")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Eigenvalue spectrum
# --------------------------------------------------

def plot_spectrum(eigenvals):

    plt.figure(figsize=(6,4))

    plt.plot(eigenvals,"o-")

    plt.xlabel("mode index")
    plt.ylabel("eigenvalue")
    plt.title("Symmetry Graph Laplacian Spectrum")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__=="__main__":

    print("\nComputing symmetry graph resonance modes...\n")

    G=build_symmetry_graph()

    eigenvals,eigenvecs,nodes=compute_resonance_modes(G)

    print("Eigenvalues:\n")
    for i,v in enumerate(eigenvals):
        print(i,":",v)

    plot_spectrum(eigenvals)

    plot_modes(G,eigenvals,eigenvecs,nodes)
