# tools/resilience_universal_architecture_law.py

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
# architecture generator
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
# dataset collection
# --------------------------------------------------

def collect_dataset(system_path, samples=1500):

    base = load_json(system_path)

    dataset = []

    print("\nCollecting architecture dataset\n")

    for i in range(samples):

        candidate = random_architecture(base)

        try:
            score = score_system(candidate)
        except:
            score = 0

        d = edge_density(candidate)
        c = cycle_ratio(candidate)

        if score > 0:
            dataset.append((d, c, score))

        if i % 50 == 0:
            print("sample", i, "score", score)

    return dataset


# --------------------------------------------------
# power law fitting
# --------------------------------------------------

def fit_scaling_law(dataset):

    d = np.array([x[0] for x in dataset])
    c = np.array([x[1] for x in dataset])
    r = np.array([x[2] for x in dataset])

    mask = (d > 0) & (c > 0) & (r > 0)

    d = d[mask]
    c = c[mask]
    r = r[mask]

    X = np.column_stack([
        np.ones(len(d)),
        np.log(d),
        np.log(c)
    ])

    y = np.log(r)

    beta = np.linalg.lstsq(X, y, rcond=None)[0]

    logC = beta[0]
    a = beta[1]
    b = beta[2]

    C = np.exp(logC)

    r_pred = C * (d ** a) * (c ** b)

    ss_res = np.sum((r - r_pred) ** 2)
    ss_tot = np.sum((r - np.mean(r)) ** 2)

    r2 = 1 - ss_res / ss_tot

    return C, a, b, r2


# --------------------------------------------------
# visualization
# --------------------------------------------------

def plot_fit(dataset, C, a, b):

    d = np.array([x[0] for x in dataset])
    c = np.array([x[1] for x in dataset])
    r = np.array([x[2] for x in dataset])

    r_pred = C * (d ** a) * (c ** b)

    plt.figure(figsize=(6,6))

    plt.scatter(r, r_pred, alpha=0.6)

    plt.xlabel("Observed Resilience")
    plt.ylabel("Predicted Resilience")

    plt.title("Universal Architecture Law Fit")

    plt.plot([0, max(r)], [0, max(r)], linestyle="--")

    plt.show()


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    dataset = collect_dataset(BASE_SYSTEM, samples=1500)

    C, a, b, r2 = fit_scaling_law(dataset)

    print("\nUniversal Architecture Law")
    print("---------------------------")

    print("R ≈ C * density^a * cycle^b\n")

    print("C =", C)
    print("a =", a)
    print("b =", b)

    print("\nModel fit R²:", r2)

    plot_fit(dataset, C, a, b)
