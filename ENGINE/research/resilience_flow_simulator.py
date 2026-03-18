"""
NEXAH Resilience Flow Simulator

Simulates dynamic flow in the architecture landscape.

Starting from random architectures, the system moves
step-by-step toward higher resilience using local gradient
information.

Axes:
X = nodes
Y = degree
Z = resilience
"""

import os
import json
import math
import random

import matplotlib.pyplot as plt


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


def estimate_gradient(point, data):

    gx = 0
    gy = 0

    x = point["nodes"]
    y = point["degree"]
    z = point["resilience"]

    for p in data:

        dx = p["nodes"] - x
        dy = p["degree"] - y
        dz = p["resilience"] - z

        dist = math.sqrt(dx*dx + dy*dy)

        if dist == 0:
            continue

        weight = dz / (dist + 1e-6)

        gx += weight * dx
        gy += weight * dy

    return gx, gy


def simulate_flow(data, steps=15):

    start = random.choice(data)

    path = []

    x = start["nodes"]
    y = start["degree"]

    for _ in range(steps):

        # estimate resilience locally
        nearest = min(
            data,
            key=lambda p: (p["nodes"]-x)**2 + (p["degree"]-y)**2
        )

        gx, gy = estimate_gradient(nearest, data)

        x += gx * 0.05
        y += gy * 0.05

        path.append((x, y))

    return path


def plot_flow(data, flows):

    xs = [d["nodes"] for d in data]
    ys = [d["degree"] for d in data]
    colors = [d["resilience"] for d in data]

    plt.figure(figsize=(8,6))

    plt.scatter(xs, ys, c=colors, cmap="plasma", s=80)

    for path in flows:

        px = [p[0] for p in path]
        py = [p[1] for p in path]

        plt.plot(px, py, color="white", linewidth=2)

    plt.xlabel("Nodes")
    plt.ylabel("Degree")

    plt.title("NEXAH Architecture Flow Simulation")

    plt.colorbar(label="Resilience")

    plt.show()


def run():

    print("\nNEXAH Resilience Flow Simulator")
    print("--------------------------------")

    data = load_results()

    if len(data) < 5:

        print("Not enough experiment data.")
        return

    flows = []

    for _ in range(6):

        flows.append(simulate_flow(data))

    plot_flow(data, flows)


if __name__ == "__main__":

    run()
