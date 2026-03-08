# tools/resilience_universal_constant_search.py

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

BASE_SYSTEM = "APPLICATIONS/examples/energy_grid_control.json"


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def write_temp(data):
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(data, tmp, indent=2)
    tmp.close()
    return tmp.name


def score_system(data):

    temp = write_temp(data)

    try:
        report = analyze_system(temp)
        return report["resilience_score"]

    finally:
        os.remove(temp)


def random_architecture(base):

    nodes = base["nodes"]

    data = copy.deepcopy(base)

    data["transitions"] = {}

    for n in nodes:

        k = random.randint(1, min(4, len(nodes)))

        targets = random.sample(nodes, k)

        data["transitions"][n] = targets

    return data


def edge_density(data):

    nodes = len(data["nodes"])

    edges = 0

    for t in data["transitions"].values():

        if isinstance(t, list):
            edges += len(t)
        else:
            edges += 1

    if nodes <= 1:
        return 0

    return edges / (nodes * (nodes - 1))


def cycle_ratio(data):

    G = nx.DiGraph()

    for s, targets in data["transitions"].items():

        if isinstance(targets, list):
            for t in targets:
                G.add_edge(s, t)
        else:
            G.add_edge(s, targets)

    scc = list(nx.strongly_connected_components(G))

    nodes_in_cycles = set()

    for comp in scc:
        if len(comp) > 1:
            nodes_in_cycles.update(comp)

    if len(G.nodes()) == 0:
        return 0

    return len(nodes_in_cycles) / len(G.nodes())


# --------------------------------------------------
# constant search
# --------------------------------------------------

def search_constant(system_path, samples=2000):

    base = load_json(system_path)

    constants = []

    for i in range(samples):

        arch = random_architecture(base)

        try:
            r = score_system(arch)
        except:
            r = 0

        d = edge_density(arch)
        c = cycle_ratio(arch)

        if d > 0 and c > 0:

            k = r / (d * c)

            constants.append(k)

        if i % 50 == 0:
            print("sample", i)

    constants = np.array(constants)

    print("\nConstant estimate")
    print("------------------")

    print("mean:", np.mean(constants))
    print("std:", np.std(constants))


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    search_constant(BASE_SYSTEM, samples=2000)
