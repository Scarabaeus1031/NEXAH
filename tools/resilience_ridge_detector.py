# tools/resilience_ridge_detector.py

import sys
import os
import json
import random
import tempfile
import copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_analyzer import analyze_system

BASE_SYSTEM = "APPLICATIONS/examples/energy_grid_control.json"


# --------------------------------------------------
# IO
# --------------------------------------------------

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def write_temp(data):
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(data, tmp, indent=2)
    tmp.close()
    return tmp.name


# --------------------------------------------------
# scoring
# --------------------------------------------------

def score_system(data):

    temp = write_temp(data)

    try:
        report = analyze_system(temp)
        return report["resilience_score"]

    finally:
        os.remove(temp)


# --------------------------------------------------
# graph helpers
# --------------------------------------------------

def rebuild_edges(data):

    edges = []

    for s, targets in data["transitions"].items():

        if isinstance(targets, list):

            for t in targets:
                edges.append([s, t])

        else:

            edges.append([s, targets])

    data["edges"] = edges

    return data


def build_graph(data):

    G = nx.DiGraph()

    for s, targets in data["transitions"].items():

        if isinstance(targets, list):

            for t in targets:
                G.add_edge(s, t)

        else:

            G.add_edge(s, targets)

    return G


# --------------------------------------------------
# metrics
# --------------------------------------------------

def edge_density(data):

    nodes = len(data["nodes"])
    edges = len(data["edges"])

    if nodes <= 1:
        return 0

    return edges / (nodes * (nodes - 1))


def cycle_ratio(data):

    G = build_graph(data)

    scc = list(nx.strongly_connected_components(G))

    nodes_in_cycles = set()

    for comp in scc:

        if len(comp) > 1:
            nodes_in_cycles.update(comp)

    if len(G.nodes()) == 0:
        return 0

    return len(nodes_in_cycles) / len(G.nodes())


# --------------------------------------------------
# random architecture
# --------------------------------------------------

def random_architecture(base):

    nodes = base["nodes"]

    data = copy.deepcopy(base)

    data["transitions"] = {}

    for n in nodes:

        k = random.randint(1, min(4, len(nodes)))

        targets = random.sample(nodes, k)

        data["transitions"][n] = targets

    return rebuild_edges(data)


# --------------------------------------------------
# dataset builder
# --------------------------------------------------

def collect_dataset(system_path, samples=1500):

    base = load_json(system_path)

    dataset = []

    for i in range(samples):

        candidate = random_architecture(base)

        try:
            score = score_system(candidate)
        except:
            score = 0

        d = edge_density(candidate)
        c = cycle_ratio(candidate)

        dataset.append((d, c, score))

        if i % 50 == 0:
            print("sample", i, "score", score)

    return dataset


# --------------------------------------------------
# ridge detection
# --------------------------------------------------

def detect_ridge(dataset):

    ridge = {}

    for d, c, s in dataset:

        key = round(d, 1)

        if key not in ridge:
            ridge[key] = []

        ridge[key].append((c, s))

    ridge_points = []

    for d, values in ridge.items():

        best = max(values, key=lambda x: x[1])

        ridge_points.append((d, best[0], best[1]))

    ridge_points.sort()

    return ridge_points


# --------------------------------------------------
# plotting
# --------------------------------------------------

def plot_ridge(dataset, ridge_points):

    densities = [x[0] for x in dataset]
    cycles = [x[1] for x in dataset]
    scores = [x[2] for x in dataset]

    plt.figure(figsize=(8,6))

    sc = plt.scatter(
        densities,
        cycles,
        c=scores,
        cmap="viridis",
        alpha=0.5
    )

    plt.colorbar(sc, label="Resilience Score")

    ridge_d = [x[0] for x in ridge_points]
    ridge_c = [x[1] for x in ridge_points]

    plt.plot(
        ridge_d,
        ridge_c,
        color="red",
        linewidth=3,
        label="Stability Ridge"
    )

    plt.xlabel("Edge Density")
    plt.ylabel("Cycle Ratio")

    plt.title("Resilience Stability Ridge")

    plt.legend()

    plt.show()


# --------------------------------------------------
# summary
# --------------------------------------------------

def print_ridge(ridge_points):

    print("\nStability Ridge")
    print("----------------")

    for d, c, s in ridge_points:

        print(
            f"density={d:.2f} cycle={c:.2f} score={s:.3f}"
        )


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    dataset = collect_dataset(BASE_SYSTEM, samples=1500)

    ridge = detect_ridge(dataset)

    print_ridge(ridge)

    plot_ridge(dataset, ridge)
