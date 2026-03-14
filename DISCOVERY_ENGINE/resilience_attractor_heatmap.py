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

    if nodes == 0:
        return 0

    return edges / (nodes * nodes)


def cycle_ratio(data):

    G = build_graph(data)

    cycles = list(nx.simple_cycles(G))

    nodes_in_cycles = set()

    for c in cycles:
        for n in c:
            nodes_in_cycles.add(n)

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

        k = random.randint(1, len(nodes))

        targets = random.sample(nodes, k)

        data["transitions"][n] = targets

    return rebuild_edges(data)


# --------------------------------------------------
# heatmap
# --------------------------------------------------

def build_heatmap(system_path, samples=1000):

    base = load_json(system_path)

    grid = {}

    for i in range(samples):

        candidate = random_architecture(base)

        try:
            score = score_system(candidate)
        except:
            score = 0

        d = round(edge_density(candidate), 1)
        c = round(cycle_ratio(candidate), 1)

        key = (d, c)

        if key not in grid:
            grid[key] = []

        grid[key].append(score)

        if i % 50 == 0:
            print("sample", i)

    densities = sorted(list(set(k[0] for k in grid.keys())))
    cycles = sorted(list(set(k[1] for k in grid.keys())))

    heat = np.zeros((len(cycles), len(densities)))

    for (d, c), values in grid.items():

        x = densities.index(d)
        y = cycles.index(c)

        heat[y][x] = np.mean(values)

    plt.figure(figsize=(8,6))

    plt.imshow(
        heat,
        origin="lower",
        aspect="auto",
        extent=[min(densities), max(densities), min(cycles), max(cycles)]
    )

    plt.colorbar(label="Resilience Score")

    plt.xlabel("Edge Density")
    plt.ylabel("Cycle Ratio")

    plt.title("Resilience Architecture Landscape")

    plt.show()


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    build_heatmap(BASE_SYSTEM, samples=1200)
