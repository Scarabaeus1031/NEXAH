"""
NEXAH Resilience Landscape Mapper (3D)

Visualizes the architecture resilience landscape.

Axes:
X = Nodes
Y = Edges
Z = Resilience
"""

import json
import os
import glob

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


RESULTS_DIR = "results"


def load_results():

    files = sorted(glob.glob(os.path.join(RESULTS_DIR, "*.json")))

    data = []

    for f in files:

        with open(f) as file:

            r = json.load(file)

            graph = r.get("graph", {})

            nodes = graph.get("num_nodes", None)
            edges = graph.get("num_edges", None)

            resilience = r.get("resilience", {}).get("resilience_score", None)

            if nodes is None or edges is None or resilience is None:
                continue

            data.append((nodes, edges, resilience))

    return data


def plot_landscape(data):

    nodes = [d[0] for d in data]
    edges = [d[1] for d in data]
    resilience = [d[2] for d in data]

    fig = plt.figure(figsize=(10, 7))

    ax = fig.add_subplot(111, projection="3d")

    sc = ax.scatter(
        nodes,
        edges,
        resilience,
        c=resilience,
        cmap="viridis",
        s=80
    )

    ax.set_xlabel("Nodes")
    ax.set_ylabel("Edges")
    ax.set_zlabel("Resilience")

    ax.set_title("NEXAH Resilience Landscape")

    fig.colorbar(sc, label="Resilience")

    plt.show()


def run():

    data = load_results()

    if not data:
        print("No experiment results found.")
        return

    plot_landscape(data)


if __name__ == "__main__":

    run()
