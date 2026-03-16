# tools/resilience_topology_phase_transition_detector.py

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
# dataset
# --------------------------------------------------

def collect_dataset(system_path, samples=2000):

    base = load_json(system_path)

    dataset = []

    print("\nCollecting dataset\n")

    for i in range(samples):

        candidate = random_architecture(base)

        try:
            score = score_system(candidate)
        except:
            score = 0

        d = edge_density(candidate)

        dataset.append((d, score))

        if i % 50 == 0:
            print("sample", i, "score", score)

    return dataset


# --------------------------------------------------
# phase transition detection
# --------------------------------------------------

def detect_transition(dataset):

    densities = np.array([x[0] for x in dataset])
    scores = np.array([x[1] for x in dataset])

    bins = np.linspace(min(densities), max(densities), 20)

    avg_scores = []
    bin_centers = []

    for i in range(len(bins) - 1):

        mask = (densities >= bins[i]) & (densities < bins[i + 1])

        if np.sum(mask) > 5:

            avg = np.mean(scores[mask])

            avg_scores.append(avg)
            bin_centers.append((bins[i] + bins[i + 1]) / 2)

    avg_scores = np.array(avg_scores)
    bin_centers = np.array(bin_centers)

    gradient = np.gradient(avg_scores)

    idx = np.argmax(np.abs(gradient))

    critical_density = bin_centers[idx]

    return bin_centers, avg_scores, gradient, critical_density


# --------------------------------------------------
# visualization
# --------------------------------------------------

def plot_transition(bin_centers, avg_scores, gradient, critical_density):

    plt.figure(figsize=(8,6))

    plt.plot(bin_centers, avg_scores, label="Average Resilience")

    plt.axvline(
        critical_density,
        linestyle="--",
        label="Critical Density"
    )

    plt.xlabel("Edge Density")
    plt.ylabel("Average Resilience")

    plt.title("Resilience Phase Transition")

    plt.legend()

    plt.show()

    plt.figure(figsize=(8,6))

    plt.plot(bin_centers, gradient)

    plt.axvline(
        critical_density,
        linestyle="--",
        label="Critical Density"
    )

    plt.xlabel("Edge Density")
    plt.ylabel("Gradient")

    plt.title("Resilience Susceptibility")

    plt.legend()

    plt.show()


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    dataset = collect_dataset(BASE_SYSTEM, samples=2000)

    bin_centers, avg_scores, gradient, critical_density = detect_transition(dataset)

    print("\nPhase Transition")
    print("----------------")

    print("critical density:", critical_density)

    plot_transition(bin_centers, avg_scores, gradient, critical_density)
