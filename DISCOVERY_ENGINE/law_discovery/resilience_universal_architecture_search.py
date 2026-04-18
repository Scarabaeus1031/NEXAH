# tools/resilience_universal_architecture_search.py

import sys
import os
import json
import random
import tempfile
import copy
import numpy as np
import networkx as nx

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_analyzer import analyze_system


SYSTEMS = [
    "APPLICATIONS/examples/energy_grid_control.json"
]


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

def generate_architecture(base, density_target, cycle_bias):

    nodes = base["nodes"]

    data = copy.deepcopy(base)

    data["transitions"] = {}

    for n in nodes:

        k = max(1, int(len(nodes) * density_target))

        targets = random.sample(nodes, min(k, len(nodes)))

        if random.random() < cycle_bias:

            targets.append(n)

        data["transitions"][n] = list(set(targets))

    return rebuild_edges(data)


# --------------------------------------------------
# universal search
# --------------------------------------------------

def universal_search(samples=1000):

    systems = [load_json(p) for p in SYSTEMS]

    best_arch = None
    best_score = -1

    for i in range(samples):

        density = random.uniform(0.1, 0.9)
        cycle = random.uniform(0.0, 1.0)

        scores = []

        for base in systems:

            arch = generate_architecture(base, density, cycle)

            try:
                s = score_system(arch)
            except:
                s = 0

            scores.append(s)

        avg = np.mean(scores)

        if avg > best_score:

            best_score = avg
            best_arch = (density, cycle)

            print("new best", best_score, "density", density, "cycle", cycle)

        if i % 50 == 0:

            print("sample", i)

    print("\nUniversal Architecture Result")
    print("------------------------------")

    print("best average resilience:", best_score)
    print("optimal density:", best_arch[0])
    print("optimal cycle ratio:", best_arch[1])


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    universal_search(samples=1500)
