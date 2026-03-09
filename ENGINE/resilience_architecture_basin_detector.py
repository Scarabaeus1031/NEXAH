"""
NEXAH Resilience Architecture Basin Detector

Detects architecture basins (regions of similar resilience).

Basins detected:
- stability basin
- transition basin
- low-resilience basin

Axes:
nodes
degree
resilience
"""

import os
import json
import statistics

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


def classify_basins(data):

    res_values = [d["resilience"] for d in data]

    mean_res = statistics.mean(res_values)
    max_res = max(res_values)

    basins = {
        "stability": [],
        "transition": [],
        "low": []
    }

    for d in data:

        r = d["resilience"]

        if r > mean_res + 0.15*(max_res - mean_res):
            basins["stability"].append(d)

        elif r < mean_res - 0.15*(max_res - mean_res):
            basins["low"].append(d)

        else:
            basins["transition"].append(d)

    return basins


def plot_basins(basins):

    plt.figure(figsize=(8,6))

    if basins["stability"]:
        xs = [d["nodes"] for d in basins["stability"]]
        ys = [d["degree"] for d in basins["stability"]]
        plt.scatter(xs, ys, c="gold", s=120, label="Stability Basin")

    if basins["transition"]:
        xs = [d["nodes"] for d in basins["transition"]]
        ys = [d["degree"] for d in basins["transition"]]
        plt.scatter(xs, ys, c="cyan", s=80, label="Transition Basin")

    if basins["low"]:
        xs = [d["nodes"] for d in basins["low"]]
        ys = [d["degree"] for d in basins["low"]]
        plt.scatter(xs, ys, c="purple", s=80, label="Low Resilience Basin")

    plt.xlabel("Nodes")
    plt.ylabel("Degree")
    plt.title("NEXAH Architecture Basins")

    plt.legend()

    plt.show()


def print_stats(basins):

    print("\nArchitecture Basin Statistics")
    print("-----------------------------")

    for name, points in basins.items():

        if not points:
            print(f"{name}: no points")
            continue

        nodes = [p["nodes"] for p in points]
        deg = [p["degree"] for p in points]
        res = [p["resilience"] for p in points]

        print(f"\n{name.upper()} BASIN")

        print("points:", len(points))
        print("nodes ≈", round(statistics.mean(nodes),2))
        print("degree ≈", round(statistics.mean(deg),2))
        print("resilience ≈", round(statistics.mean(res),3))


def run():

    print("\nNEXAH Architecture Basin Detector")
    print("---------------------------------")

    data = load_results()

    if len(data) == 0:
        print("No experiment data found.")
        return

    basins = classify_basins(data)

    print_stats(basins)

    plot_basins(basins)


if __name__ == "__main__":

    run()
