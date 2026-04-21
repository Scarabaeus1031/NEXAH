"""
NEXAH Resilience Landscape Surface AI

Builds a continuous resilience surface from experiment data.

Axes:
X = nodes
Y = degree
Z = resilience
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


RESULT_DIR = "results"


def load_results():

    xs = []
    ys = []
    zs = []

    if not os.path.exists(RESULT_DIR):
        return xs, ys, zs

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

                xs.append(nodes)
                ys.append(degree)
                zs.append(res)

        except:
            continue

    return xs, ys, zs


def build_surface(xs, ys, zs):

    xi = np.linspace(min(xs), max(xs), 50)
    yi = np.linspace(min(ys), max(ys), 50)

    X, Y = np.meshgrid(xi, yi)

    Z = griddata((xs, ys), zs, (X, Y), method="cubic")

    return X, Y, Z


def plot_surface(xs, ys, zs, X, Y, Z):

    fig = plt.figure()

    ax = fig.add_subplot(111, projection="3d")

    ax.plot_surface(X, Y, Z, alpha=0.6)

    ax.scatter(xs, ys, zs)

    ax.set_xlabel("Nodes")
    ax.set_ylabel("Degree")
    ax.set_zlabel("Resilience")

    plt.title("NEXAH Resilience Landscape Surface")

    plt.show()


def run_surface_ai():

    print("\nNEXAH Resilience Landscape Surface AI")
    print("-------------------------------------")

    xs, ys, zs = load_results()

    if len(xs) < 5:
        print("Not enough data.")
        return

    X, Y, Z = build_surface(xs, ys, zs)

    plot_surface(xs, ys, zs, X, Y, Z)


if __name__ == "__main__":

    run_surface_ai()
