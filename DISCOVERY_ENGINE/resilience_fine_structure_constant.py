# tools/resilience_fine_structure_constant.py

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

    if nodes == 0:
        return 0.0

    return edges / (nodes * nodes)


def cycle_ratio(data):
    G = build_graph(data)

    cycles = list(nx.simple_cycles(G))

    nodes_in_cycles = set()

    for c in cycles:
        for n in c:
            nodes_in_cycles.add(n)

    if len(G.nodes()) == 0:
        return 0.0

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
# candidate constants
# --------------------------------------------------

def candidate_constants(d, c):
    eps = 1e-6

    return {
        "density/cycle": d / (c + eps),
        "density*cycle": d * c,
        "(density+cycle)/2": (d + c) / 2.0,
        "density/(1+cycle)": d / (1.0 + c),
        "cycle/(1+density)": c / (1.0 + d),
        "density^2+cycle^2": d * d + c * c,
        "sqrt(density*cycle)": np.sqrt(max(d * c, 0.0)),
        "(density*cycle)/(density+cycle)": (d * c) / (d + c + eps),
    }


# --------------------------------------------------
# search
# --------------------------------------------------

def search_fine_structure_constant(samples=2000, score_threshold=0.40):

    base = load_json(BASE_SYSTEM)

    collected = {}

    good_count = 0

    for i in range(samples):

        candidate = random_architecture(base)

        try:
            score = score_system(candidate)
        except:
            score = 0.0

        if score < score_threshold:
            continue

        d = edge_density(candidate)
        c = cycle_ratio(candidate)

        consts = candidate_constants(d, c)

        for name, value in consts.items():
            collected.setdefault(name, []).append(value)

        good_count += 1

        if i % 100 == 0:
            print("sample", i, "score", round(score, 3))

    if good_count == 0:
        print("\nNo architectures exceeded the threshold.")
        print("Try lowering score_threshold (e.g. 0.35).")
        return

    print("\nResilience Fine Structure Constant Search")
    print("------------------------------------------")
    print("qualified architectures:", good_count)

    results = []

    for name, values in collected.items():

        arr = np.array(values)

        mean = np.mean(arr)
        std = np.std(arr)

        rel_std = std / (abs(mean) + 1e-9)

        results.append((rel_std, name, mean, std, len(arr)))

    results.sort(key=lambda x: x[0])

    print("\nTop constant candidates:\n")

    for rel_std, name, mean, std, count in results[:8]:
        print(
            f"{name:28s} mean={mean:.6f}  std={std:.6f}  rel_std={rel_std:.6f}  n={count}"
        )

    best = results[0]

    print("\nMost stable fine-structure candidate:\n")
    print("name:", best[1])
    print("constant:", round(best[2], 6))
    print("std:", round(best[3], 6))
    print("rel_std:", round(best[0], 6))

    print("\nSuggested notation:\n")
    print(f"alpha_R ≈ {best[2]:.6f}")


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    search_fine_structure_constant(
        samples=2000,
        score_threshold=0.40
    )
