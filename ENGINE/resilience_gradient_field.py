"""
NEXAH Resilience Gradient Field

Builds a local gradient field on top of the architecture landscape.

Axes:
X = nodes
Y = degree
Z = resilience

For each architecture point, the script estimates the local
gradient direction toward higher resilience using nearby points.
"""

import os
import json
import math

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


def compute_gradient_field(data):

    vectors = []

    for i, p in enumerate(data):

        x = p["nodes"]
        y = p["degree"]
        z = p["resilience"]

        gx = 0
        gy = 0

        for j, q in enumerate(data):

            if i == j:
                continue

            dx = q["nodes"] - x
            dy = q["degree"] - y
            dz = q["resilience"] - z

            dist = math.sqrt(dx*dx + dy*dy)

            if dist == 0:
                continue

            weight = dz / (dist + 1e-6)

            gx += weight * dx
            gy += weight * dy

        vectors.append((x, y, gx, gy, z))

    return vectors


def plot_gradient_field(vectors):

    xs = [v[0] for v in vectors]
    ys = [v[1] for v in vectors]
    colors = [v[4] for v in vectors]

    fig, ax = plt.subplots(figsize=(8,6))

    scatter = ax.scatter(xs, ys, c=colors, cmap="plasma", s=80)

    for x, y, gx, gy, z in vectors:

        ax.arrow(
            x,
            y,
            gx*0.1,
            gy*0.1,
            head_width=0.1,
            head_length=0.1,
            fc="black",
            ec="black",
            alpha=0.7
        )

    ax.set_xlabel("Nodes")
    ax.set_ylabel("Degree")
    ax.set_title("NEXAH Resilience Gradient Field")

    plt.colorbar(scatter, label="Resilience")

    plt.show()


def run():

    print("\nNEXAH Resilience Gradient Field")
    print("--------------------------------")

    data = load_results()

    if len(data) == 0:

        print("No experiment data found.")
        return

    vectors = compute_gradient_field(data)

    plot_gradient_field(vectors)


if __name__ == "__main__":

    run()
