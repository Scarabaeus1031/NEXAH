"""
NEXAH Architecture Navigation Graph

Builds a navigation graph across the architecture stability landscape.

Nodes:
    local maxima (stable architectures)

Edges:
    gradient flow transitions between regions

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_navigation_graph
"""

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from ENGINE.nexah_kernel.tools.nexah_spectral_stability_score import spectral_stability_score


# ---------------------------------------------------------
# stability field
# ---------------------------------------------------------

def compute_stability_field():

    # reproducible Monte-Carlo runs
    np.random.seed(42)

    node_values = np.arange(4, 15)
    prob_values = np.linspace(0.05, 0.9, 17)

    stability = np.zeros((len(node_values), len(prob_values)))

    samples = 50

    for i, n in enumerate(node_values):
        for j, p in enumerate(prob_values):

            scores = []

            for _ in range(samples):

                G = nx.erdos_renyi_graph(int(n), float(p))

                if G.number_of_edges() == 0:
                    continue

                score = spectral_stability_score(G)
                scores.append(score)

            if scores:
                stability[i, j] = np.mean(scores)

    return node_values, prob_values, stability


# ---------------------------------------------------------
# neighbor helper
# ---------------------------------------------------------

def neighbors(i, j, rows, cols):

    neigh = []

    for di, dj in [
        (-1,0),(1,0),(0,-1),(0,1),
        (-1,-1),(-1,1),(1,-1),(1,1)
    ]:

        ni = i + di
        nj = j + dj

        if 0 <= ni < rows and 0 <= nj < cols:
            neigh.append((ni,nj))

    return neigh


# ---------------------------------------------------------
# detect maxima
# ---------------------------------------------------------

def detect_maxima(stability):

    rows, cols = stability.shape
    maxima = []

    for i in range(1,rows-1):
        for j in range(1,cols-1):

            v = stability[i,j]

            neigh = neighbors(i,j,rows,cols)
            neigh_vals = [stability[x,y] for x,y in neigh]

            if v >= max(neigh_vals) and v > np.mean(neigh_vals):

                maxima.append((i,j))

    return maxima


# ---------------------------------------------------------
# gradient flow
# ---------------------------------------------------------

def gradient_destination(stability,i,j):

    rows, cols = stability.shape

    current = (i,j)

    while True:

        neigh = neighbors(current[0],current[1],rows,cols)

        best = current
        best_val = stability[current]

        for n in neigh:

            if stability[n] > best_val:
                best = n
                best_val = stability[n]

        if best == current:
            return current

        current = best


# ---------------------------------------------------------
# build navigation graph
# ---------------------------------------------------------

def build_navigation_graph(stability,maxima):

    rows, cols = stability.shape

    G = nx.Graph()

    for m in maxima:
        G.add_node(m)

    for i in range(rows):
        for j in range(cols):

            dest = gradient_destination(stability,i,j)

            if dest in maxima:
                G.add_edge((i,j),dest)

    return G


# ---------------------------------------------------------
# visualization
# ---------------------------------------------------------

def plot_navigation_graph(node_values,prob_values,stability,maxima,G):

    output_dir = "ENGINE/nexah_kernel/demos/visuals"
    os.makedirs(output_dir,exist_ok=True)

    outfile = os.path.join(
        output_dir,
        "architecture_navigation_graph.png"
    )

    plt.figure(figsize=(10,7))

    extent = [
        prob_values.min(),
        prob_values.max(),
        node_values.min(),
        node_values.max()
    ]

    plt.imshow(
        stability,
        origin="lower",
        extent=extent,
        aspect="auto",
        cmap="viridis"
    )

    # draw flow edges

    for u,v in G.edges():

        x1 = prob_values[u[1]]
        y1 = node_values[u[0]]

        x2 = prob_values[v[1]]
        y2 = node_values[v[0]]

        plt.plot(
            [x1,x2],
            [y1,y2],
            color="white",
            alpha=0.2
        )

    # draw attractors

    if maxima:

        xs = [prob_values[j] for i,j in maxima]
        ys = [node_values[i] for i,j in maxima]

        plt.scatter(
            xs,ys,
            c="red",
            s=80,
            label="Stable architectures"
        )

        plt.legend()

    plt.title("Architecture Stability Navigation Graph")

    plt.xlabel("Edge Probability")
    plt.ylabel("Number of Nodes")

    plt.colorbar(label="λ₂ / λmax")

    plt.tight_layout()

    plt.savefig(outfile,dpi=180)

    print("\nSaved navigation graph:")
    print(outfile)

    plt.show()


# ---------------------------------------------------------
# run demo
# ---------------------------------------------------------

def run():

    print("\nComputing architecture navigation graph...\n")

    node_values,prob_values,stability = compute_stability_field()

    maxima = detect_maxima(stability)

    graph = build_navigation_graph(stability,maxima)

    plot_navigation_graph(
        node_values,
        prob_values,
        stability,
        maxima,
        graph
    )


if __name__ == "__main__":
    run()
