# tools/resilience_symbolic_equation_search.py

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


def largest_scc_ratio(data):

    G = build_graph(data)

    if len(G.nodes()) == 0:
        return 0.0

    comps = list(nx.strongly_connected_components(G))

    if not comps:
        return 0.0

    largest = max(len(comp) for comp in comps)

    return largest / len(G.nodes())


def mean_out_degree(data):

    G = build_graph(data)

    if len(G.nodes()) == 0:
        return 0.0

    return float(np.mean([G.out_degree(n) for n in G.nodes()]))


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
# dataset
# --------------------------------------------------

def collect_dataset(system_path, samples=2000):

    base = load_json(system_path)

    dataset = []

    print("\nCollecting symbolic dataset\n")

    for i in range(samples):

        candidate = random_architecture(base)

        try:
            score = score_system(candidate)
        except:
            score = 0.0

        d = edge_density(candidate)
        c = cycle_ratio(candidate)
        s = largest_scc_ratio(candidate)
        k = mean_out_degree(candidate)

        dataset.append((d, c, s, k, score))

        if i % 50 == 0:
            print("sample", i, "score", round(score, 3))

    return dataset


# --------------------------------------------------
# symbolic candidate library
# --------------------------------------------------

def candidate_library():

    return [

        ("c*(1-d)", lambda d,c,s,k: c*(1-d)),

        ("c^2", lambda d,c,s,k: c*c),

        ("d*(1-d)", lambda d,c,s,k: d*(1-d)),

        ("c^2/(1+d)", lambda d,c,s,k: (c*c)/(1+d)),

        ("c/(1+d)", lambda d,c,s,k: c/(1+d)),

        ("(c-d)^2", lambda d,c,s,k: (c-d)**2),

        ("s*(1-d)", lambda d,c,s,k: s*(1-d)),

        ("s*c", lambda d,c,s,k: s*c),

        ("s^2", lambda d,c,s,k: s*s),

        ("k/(1+d)", lambda d,c,s,k: k/(1+d)),

        ("c/(1+d^2)", lambda d,c,s,k: c/(1+d*d)),

        ("c^2/(1+d^2)", lambda d,c,s,k: (c*c)/(1+d*d)),

        ("(c*(1-d))^2", lambda d,c,s,k: (c*(1-d))**2),

    ]


# --------------------------------------------------
# evaluation
# --------------------------------------------------

def evaluate_formula(dataset, func):

    X = []
    y = []

    for d,c,s,k,r in dataset:

        try:
            val = func(d,c,s,k)
        except:
            continue

        if np.isnan(val) or np.isinf(val):
            continue

        X.append(val)
        y.append(r)

    if len(X) < 10:
        return None

    X = np.array(X)
    y = np.array(y)

    A = np.vstack([X, np.ones(len(X))]).T

    coef, intercept = np.linalg.lstsq(A, y, rcond=None)[0]

    pred = coef*X + intercept

    ss_res = np.sum((y-pred)**2)
    ss_tot = np.sum((y-np.mean(y))**2)

    r2 = 1 - ss_res/ss_tot if ss_tot>0 else 0

    return coef, intercept, r2


# --------------------------------------------------
# search
# --------------------------------------------------

def symbolic_search(dataset):

    formulas = candidate_library()

    results = []

    for name,func in formulas:

        res = evaluate_formula(dataset, func)

        if res is None:
            continue

        coef,intercept,r2 = res

        results.append((r2,name,coef,intercept))

    results.sort(reverse=True)

    return results


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    dataset = collect_dataset(BASE_SYSTEM, samples=2000)

    results = symbolic_search(dataset)

    print("\nBest Symbolic Laws\n")
    print("-------------------\n")

    for r2,name,coef,intercept in results[:5]:

        print(f"R ≈ {coef:.4f} * {name} + {intercept:.4f}")
        print(f"R² = {r2:.4f}\n")
