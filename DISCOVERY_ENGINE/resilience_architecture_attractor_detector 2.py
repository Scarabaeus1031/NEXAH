# tools/resilience_architecture_attractor_detector.py

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
# attractor detection
# --------------------------------------------------

def detect_attractors(system_path, samples=1000):

    base = load_json(system_path)

    regions = {}

    for i in range(samples):

        candidate = random_architecture(base)

        try:
            score = score_system(candidate)
        except:
            score = 0

        d = edge_density(candidate)
        c = cycle_ratio(candidate)

        key = (round(d, 1), round(c, 1))

        if key not in regions:
            regions[key] = []

        regions[key].append(score)

        if i % 50 == 0:
            print("sample", i, "score", score)

    print("\nArchitecture Attractors")
    print("-------------------------")

    summary = []

    for k, v in regions.items():

        avg = np.mean(v)

        summary.append((avg, k, len(v)))

    summary.sort(reverse=True)

    print("\nTop Stability Islands\n")

    for s, (d, c), count in summary[:10]:

        print(f"density={d} cycle={c} avg_score={s:.3f} samples={count}")

    print("\nCollapse Basins\n")

    for s, (d, c), count in summary[-10:]:

        print(f"density={d} cycle={c} avg_score={s:.3f} samples={count}")


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    detect_attractors(BASE_SYSTEM, samples=1200)
