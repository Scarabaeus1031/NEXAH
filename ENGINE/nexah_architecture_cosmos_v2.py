"""
NEXAH Architecture Cosmos Visualizer 2.0

Enhanced visualization of the architecture landscape.

Features:

• architecture scatter
• detected stability ridge
• transition region highlight
"""

import os
import json
import statistics

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

                data.append({
                    "nodes": nodes,
                    "degree": degree,
                    "resilience": res
                })

        except:
            continue

    return data


def detect_regions(data):

    sorted_data = sorted(data, key=lambda x: x["resilience"], reverse=True)

    ridge = sorted_data[:max(3, len(sorted_data)//5)]

    mean_res = statistics.mean([x["resilience"] for x in data])

    transition = []

    for x in data:

        if abs(x["resilience"] - mean_res) < 0.05:
            transition.append(x)

    return ridge, transition


def run():

    print("\nNEXAH Architecture Cosmos 2.0")
    print("-----------------------------")

    data = load_results()

    if len(data) == 0:

        print("No data found.")
        return

    ridge, transition = detect_regions(data)

    xs = [x["nodes"] for x in data]
    ys = [x["degree"] for x in data]
    zs = [x["resilience"] for x in data]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(xs, ys, zs, c=zs, cmap="plasma", s=40, alpha=0.8)

    # Ridge points
    rx = [x["nodes"] for x in ridge]
    ry = [x["degree"] for x in ridge]
    rz = [x["resilience"] for x in ridge]

    ax.scatter(rx, ry, rz, c="red", s=120, label="Stability Ridge")

    # Transition region
    tx = [x["nodes"] for x in transition]
    ty = [x["degree"] for x in transition]
    tz = [x["resilience"] for x in transition]

    ax.scatter(tx, ty, tz, c="cyan", s=100, label="Transition Region")

    ax.set_xlabel("Nodes")
    ax.set_ylabel("Degree")
    ax.set_zlabel("Resilience")

    plt.title("NEXAH Architecture Cosmos 2.0")

    ax.legend()

    plt.show()


if __name__ == "__main__":

    run()
