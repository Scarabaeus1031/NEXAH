# tools/resilience_meta_learning_engine.py

import sys
import os
import json
import random
import tempfile
import copy
import math
import numpy as np
import networkx as nx
from sklearn.metrics import r2_score

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
# architecture generator
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
# dataset generation
# --------------------------------------------------

def generate_dataset(samples=600):

    base = load_json(BASE_SYSTEM)

    X = []
    y = []

    for i in range(samples):

        candidate = random_architecture(base)

        try:
            score = score_system(candidate)
        except:
            score = 0

        d = edge_density(candidate)
        c = cycle_ratio(candidate)

        X.append((d, c))
        y.append(score)

        if i % 50 == 0:
            print("dataset sample", i)

    return np.array(X), np.array(y)


# --------------------------------------------------
# symbolic formula generation
# --------------------------------------------------

def random_formula():

    ops = ["+", "-", "*", "/"]
    funcs = ["sqrt", "log", "none"]

    op = random.choice(ops)
    func = random.choice(funcs)

    structure = random.choice([
        "d op c",
        "(d op c)",
        "func(d)",
        "func(c)",
        "func(d op c)"
    ])

    return structure, op, func


def evaluate_formula(structure, op, func, d, c):

    try:

        expr = structure.replace("op", op)

        if "func" in expr:

            if func == "sqrt":
                expr = expr.replace("func", "math.sqrt")

            elif func == "log":
                expr = expr.replace("func", "math.log")

            else:
                expr = expr.replace("func", "")

        value = eval(expr)

        if isinstance(value, complex) or math.isnan(value):
            return 0

        return value

    except:
        return 0


# --------------------------------------------------
# search
# --------------------------------------------------

def search_symbolic_law():

    X, y = generate_dataset()

    best_r2 = -1
    best_formula = None

    for i in range(2000):

        structure, op, func = random_formula()

        preds = []

        for d, c in X:

            v = evaluate_formula(structure, op, func, d, c)
            preds.append(v)

        preds = np.array(preds)

        if np.std(preds) == 0:
            continue

        r2 = r2_score(y, preds)

        if r2 > best_r2:

            best_r2 = r2
            best_formula = (structure, op, func)

            print("new best R2:", r2, "formula:", best_formula)

    print("\nBest discovered symbolic law:")
    print(best_formula)
    print("R2:", best_r2)


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    search_symbolic_law()
