"""
NEXAH Resilience Landscape Surface

Builds a continuous surface from architecture experiments.

Axes:
X = Nodes
Y = Edges
Z = Resilience
"""

import json
import os
import glob

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


RESULTS_DIR = "results"


def load_results():

    files = sorted(glob.glob(os.path.join(RESULTS_DIR, "*.json")))

    nodes = []
    edges = []
    resilience = []

    for f in files:

        try:

            with open(f) as file:

                r = json.load(file)

            graph = r.get("graph", {})

            n = None
            e = None

            if "num_nodes" in graph:
                n = graph["num_nodes"]

            if "num_edges" in graph:
                e = graph["num_edges"]

            if n is None and "nodes" in graph:
                n = len(graph["nodes"])

            if e is None and "edges" in graph:
                e = len(graph["edges"])

            rscore = r.get("resilience", {}).get("resilience_score")

            if n is None or e is None or rscore is None:
                continue

            nodes.append(n)
            edges.append(e)
            resilience.append(rscore)

        except Exception:
            continue

    return np.array(nodes), np.array(edges), np.array(resilience)


def build_surface(nodes, edges, resilience):

    grid_x, grid_y = np.mgrid[
        nodes.min():nodes.max():40j,
        edges.min():edges.max():40j
    ]

    grid_z = griddata(
        (nodes, edges),
        resilience,
        (grid_x, grid_y),
        method="cubic"
    )

    return grid_x, grid_y, grid_z


def plot_surface(nodes, edges, resilience, grid_x, grid_y, grid_z):

    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_surface(
        grid_x,
        grid_y,
        grid_z,
        cmap="viridis",
        alpha=0.7
    )

    ax.scatter(
        nodes,
        edges,
        resilience,
        color="black",
        s=40
    )

    ax.set_xlabel("Nodes")
    ax.set_ylabel("Edges")
    ax.set_zlabel("Resilience")

    ax.set_title("NEXAH Resilience Landscape Surface")

    plt.show()


def run():

    nodes, edges, resilience = load_results()

    if len(nodes) == 0:
        print("No experiment results found.")
        return

    grid_x, grid_y, grid_z = build_surface(nodes, edges, resilience)

    plot_surface(nodes, edges, resilience, grid_x, grid_y, grid_z)


if __name__ == "__main__":

    run()
