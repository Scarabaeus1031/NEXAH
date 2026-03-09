# tools/resilience_field_equation_discovery.py

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
        return 0.0

    return edges / (nodes * (nodes - 1))


def cycle_ratio(data):
    G = build_graph(data)

    scc = list(nx.strongly_connected_components(G))
    nodes_in_cycles = set()

    for comp in scc:
        if len(comp) > 1:
            nodes_in_cycles.update(comp)

    if len(G.nodes()) == 0:
        return 0.0

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
# feature engineering
# --------------------------------------------------

FEATURE_NAMES = [
    "1",
    "density",
    "cycle",
    "density2",
    "cycle2",
    "density_cycle",
    "density*(1-density)",
    "cycle*(1-density)"
]


def build_features(d, c):

    return [
        1.0,
        d,
        c,
        d * d,
        c * c,
        d * c,
        d * (1 - d),
        c * (1 - d)
    ]


# --------------------------------------------------
# dataset
# --------------------------------------------------

def collect_dataset(system_path, samples=2000):

    base = load_json(system_path)

    X = []
    y = []

    print("\nCollecting field dataset\n")

    for i in range(samples):

        candidate = random_architecture(base)

        try:
            score = score_system(candidate)
        except:
            score = 0.0

        d = edge_density(candidate)
        c = cycle_ratio(candidate)

        X.append(build_features(d, c))
        y.append(score)

        if i % 50 == 0:
            print("sample", i, "score", round(score, 3))

    return np.array(X), np.array(y)


# --------------------------------------------------
# regression
# --------------------------------------------------

def fit_equation(X, y):

    # Ridge regression (small regularization)
    lam = 1e-4

    XtX = X.T @ X
    I = np.eye(X.shape[1])

    beta = np.linalg.inv(XtX + lam * I) @ X.T @ y

    y_pred = X @ beta

    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)

    r2 = 1 - ss_res / ss_tot

    return beta, y_pred, r2


# --------------------------------------------------
# reporting
# --------------------------------------------------

def print_equation(beta):

    print("\nDiscovered Resilience Field Equation")
    print("------------------------------------")

    terms = []

    for coef, name in zip(beta, FEATURE_NAMES):

        if abs(coef) > 1e-4:

            if name == "1":
                terms.append(f"{coef:.4f}")
            else:
                terms.append(f"{coef:.4f}*{name}")

    equation = " + ".join(terms)

    print("\nR ≈", equation)


# --------------------------------------------------
# plot
# --------------------------------------------------

def plot_fit(y, y_pred):

    plt.figure(figsize=(6,6))

    plt.scatter(y, y_pred, alpha=0.5)

    max_val = max(max(y), max(y_pred))

    plt.plot([0, max_val], [0, max_val], linestyle="--")

    plt.xlabel("Observed Resilience")
    plt.ylabel("Predicted Resilience")

    plt.title("Field Equation Fit")

    plt.show()


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    X, y = collect_dataset(BASE_SYSTEM, samples=2000)

    beta, y_pred, r2 = fit_equation(X, y)

    print_equation(beta)

    print("\nModel fit R²:", r2)

    plot_fit(y, y_pred)
