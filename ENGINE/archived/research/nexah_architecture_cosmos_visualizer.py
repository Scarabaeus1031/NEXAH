"""
NEXAH Architecture Cosmos Visualizer

Builds a 3D map of the architecture universe discovered
by the NEXAH resilience experiments.

Axes:
X = nodes
Y = degree
Z = resilience

Color = resilience intensity
"""

import os
import json

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


RESULT_DIR = "results"


def load_results():

    data = []

    if not os.path.exists(RESULT_DIR):
        return data

    for f in os.listdir(RESULT_DIR):

        if not f.endswith(".json"):
            continue

        path = os.path.join(RESULT_DIR, f)

        try:

            with open(path) as file:

                r = json.load(file)

                if "nodes" not in r:
                    continue

                nodes = r["nodes"]
                edges = r["edges"]
                res = r["resilience_score"]

                degree = edges / nodes if nodes else 0

                data.append({
                    "nodes": nodes,
                    "edges": edges,
                    "degree": degree,
                    "resilience": res
                })

        except:
            continue

    return data


def build_arrays(data):

    xs = []
    ys = []
    zs = []
    colors = []

    for r in data:

        xs.append(r["nodes"])
        ys.append(r["degree"])
        zs.append(r["resilience"])
        colors.append(r["resilience"])

    return xs, ys, zs, colors


def plot_cosmos(xs, ys, zs, colors):

    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(
        xs,
        ys,
        zs,
        c=colors,
        cmap="plasma",
        s=40
    )

    ax.set_xlabel("Nodes")
    ax.set_ylabel("Degree")
    ax.set_zlabel("Resilience")

    fig.colorbar(scatter, label="Resilience")

    plt.title("NEXAH Architecture Cosmos")

    plt.show()


def run():

    print("\nNEXAH Architecture Cosmos Visualizer")
    print("------------------------------------")

    data = load_results()

    if len(data) == 0:

        print("No experiment data found.")

        return

    xs, ys, zs, colors = build_arrays(data)

    plot_cosmos(xs, ys, zs, colors)


if __name__ == "__main__":

    run()
