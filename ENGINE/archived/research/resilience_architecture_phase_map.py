"""
NEXAH Resilience Architecture Phase Map

Builds a continuous resilience landscape from experiment data.

Axes:
X = nodes
Y = degree
Z = resilience

The script interpolates a grid from discrete experiment points
to visualize the architecture phase surface.
"""

import os
import json
import math
import numpy as np
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

                if nodes == 0:
                    continue

                degree = edges / nodes

                data.append((nodes, degree, res))

        except:
            continue

    return data


def interpolate_surface(data, resolution=30):

    nodes_vals = [d[0] for d in data]
    degree_vals = [d[1] for d in data]

    n_min, n_max = min(nodes_vals), max(nodes_vals)
    d_min, d_max = min(degree_vals), max(degree_vals)

    grid_nodes = np.linspace(n_min, n_max, resolution)
    grid_degree = np.linspace(d_min, d_max, resolution)

    X, Y = np.meshgrid(grid_nodes, grid_degree)
    Z = np.zeros_like(X)

    for i in range(resolution):
        for j in range(resolution):

            gx = X[i, j]
            gy = Y[i, j]

            weights = []
            values = []

            for n, d, r in data:

                dist = math.sqrt((gx-n)**2 + (gy-d)**2)

                if dist == 0:
                    weights = [1]
                    values = [r]
                    break

                w = 1/(dist+1e-6)

                weights.append(w)
                values.append(r)

            Z[i, j] = sum(w*v for w,v in zip(weights,values)) / sum(weights)

    return X, Y, Z


def run():

    print("\nNEXAH Architecture Phase Map")
    print("-----------------------------")

    data = load_results()

    if len(data) == 0:
        print("No experiment data found.")
        return

    X, Y, Z = interpolate_surface(data)

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')

    surface = ax.plot_surface(
        X,
        Y,
        Z,
        cmap="plasma",
        alpha=0.8
    )

    xs = [d[0] for d in data]
    ys = [d[1] for d in data]
    zs = [d[2] for d in data]

    ax.scatter(xs, ys, zs, c="black", s=30)

    ax.set_xlabel("Nodes")
    ax.set_ylabel("Degree")
    ax.set_zlabel("Resilience")

    fig.colorbar(surface, label="Resilience")

    plt.title("NEXAH Architecture Phase Surface")

    plt.show()


if __name__ == "__main__":

    run()
