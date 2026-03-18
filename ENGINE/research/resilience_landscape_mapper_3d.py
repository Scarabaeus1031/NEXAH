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


RESULTS_DIR = "results"


def load_results():

    files = sorted(glob.glob(os.path.join(RESULTS_DIR, "*.json")))

    data = []

    for f in files:

        try:

            with open(f) as file:

                r = json.load(file)

            graph = r.get("graph", {})

            nodes = None
            edges = None

            # variant 1
            if "num_nodes" in graph:
                nodes = graph["num_nodes"]

            if "num_edges" in graph:
                edges = graph["num_edges"]

            # variant 2
            if nodes is None and "nodes" in graph:
                nodes = len(graph["nodes"])

            if edges is None and "edges" in graph:
                edges = len(graph["edges"])

            resilience = r.get("resilience", {}).get("resilience_score")

            if nodes is None or edges is None or resilience is None:
                continue

            data.append((nodes, edges, resilience))

        except Exception:
            continue

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

    print(f"Loaded {len(data)} experiments")

    plot_landscape(data)


if __name__ == "__main__":

    run()
