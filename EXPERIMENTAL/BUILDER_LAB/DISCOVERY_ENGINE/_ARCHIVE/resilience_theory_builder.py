# tools/resilience_theory_builder.py

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
# random architecture
# --------------------------------------------------

def random_architecture(base):

    nodes = base["nodes"]

    data = copy.deepcopy(base)

    data["transitions"] = {}

    for n in nodes:

        targets = []

        k = random.randint(1, len(nodes))

        for _ in range(k):

            t = random.choice(nodes)

            if t != n and t not in targets:
                targets.append(t)

        data["transitions"][n] = targets

    return rebuild_edges(data)


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
# theory builder
# --------------------------------------------------

def build_theory(system_path, samples=1000):

    base = load_json(system_path)

    densities = []
    cycles = []
    scores = []

    for i in range(samples):

        candidate = random_architecture(base)

        try:
            score = score_system(candidate)
        except:
            score = 0

        d = edge_density(candidate)
        c = cycle_ratio(candidate)

        densities.append(d)
        cycles.append(c)
        scores.append(score)

        if i % 50 == 0:
            print(f"sample {i} score={score:.3f}")

    densities = np.array(densities)
    cycles = np.array(cycles)
    scores = np.array(scores)

    # --------------------------------------------------
    # critical points
    # --------------------------------------------------

    best_index = np.argmax(scores)

    best_density = densities[best_index]
    best_cycle = cycles[best_index]
    best_score = scores[best_index]

    print("\nResilience Theory Summary")
    print("---------------------------")

    print(f"Best resilience score: {best_score:.3f}")
    print(f"Optimal density: {best_density:.3f}")
    print(f"Optimal cycle ratio: {best_cycle:.3f}")

    # --------------------------------------------------
    # average trends
    # --------------------------------------------------

    avg_density = np.mean(densities)
    avg_cycle = np.mean(cycles)

    print("\nAverage architecture")

    print(f"mean density: {avg_density:.3f}")
    print(f"mean cycle ratio: {avg_cycle:.3f}")

    # --------------------------------------------------
    # phase transition detection
    # --------------------------------------------------

    density_bins = np.linspace(0, 1, 10)

    phase_scores = []

    for i in range(len(density_bins) - 1):

        mask = (densities >= density_bins[i]) & (densities < density_bins[i + 1])

        if np.sum(mask) > 0:

            phase_scores.append(np.mean(scores[mask]))

        else:

            phase_scores.append(0)

    print("\nPhase regions (density → avg resilience)")

    for i, val in enumerate(phase_scores):

        print(f"{density_bins[i]:.2f} - {density_bins[i+1]:.2f}  ->  {val:.3f}")

    # --------------------------------------------------
    # theoretical law guess
    # --------------------------------------------------

    print("\nEmergent hypothesis")

    if best_density < avg_density:
        print("Lower density architectures appear more resilient.")

    if best_cycle > avg_cycle:
        print("Feedback cycles increase stability.")

    if best_cycle < avg_cycle:
        print("Too many cycles may destabilize the system.")


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    build_theory(BASE_SYSTEM, samples=1000)
