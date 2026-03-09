# tools/resilience_phase_transition_detector.py

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


# --------------------------------------------------
# architecture generator
# --------------------------------------------------

def generate_architecture(base, density):

    nodes = base["nodes"]

    data = copy.deepcopy(base)

    data["transitions"] = {}

    k = max(1, int(len(nodes) * density))

    for n in nodes:

        targets = random.sample(nodes, min(k, len(nodes)))

        data["transitions"][n] = targets

    return rebuild_edges(data)


# --------------------------------------------------
# phase scan
# --------------------------------------------------

def scan_phase_space(samples_per_density=30):

    base = load_json(BASE_SYSTEM)

    densities = np.linspace(0.05, 0.95, 20)

    avg_scores = []

    for d in densities:

        scores = []

        for _ in range(samples_per_density):

            candidate = generate_architecture(base, d)

            try:
                s = score_system(candidate)
            except:
                s = 0

            scores.append(s)

        avg = np.mean(scores)

        print("density", round(d,3), "avg_resilience", round(avg,3))

        avg_scores.append(avg)

    return densities, avg_scores


# --------------------------------------------------
# critical point detection
# --------------------------------------------------

def detect_critical_point(densities, scores):

    gradients = np.gradient(scores)

    idx = np.argmin(gradients)

    critical_density = densities[idx]

    return critical_density, gradients


# --------------------------------------------------
# plot
# --------------------------------------------------

def plot_transition(densities, scores, critical_density):

    plt.figure(figsize=(8,5))

    plt.plot(densities, scores, marker="o")

    plt.axvline(
        critical_density,
        linestyle="--"
    )

    plt.xlabel("Network Density")
    plt.ylabel("Resilience")

    plt.title("Resilience Phase Transition")

    plt.grid(True)

    plt.show()


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    densities, scores = scan_phase_space()

    critical_density, gradients = detect_critical_point(densities, scores)

    print("\nCritical Phase Transition")
    print("----------------------------")

    print("critical density ≈", critical_density)

    plot_transition(densities, scores, critical_density)

# ------------------------------------------------
# NEXAH ENGINE INTERFACE
# ------------------------------------------------

def detect_transitions(landscape):
    """
    Adapter for the NEXAH engine.

    The engine passes a landscape object. This adapter extracts
    transition candidates from it.
    """

    transitions = []

    # minimal heuristic for now
    if isinstance(landscape, dict):

        nodes = landscape.get("nodes", [])

        if len(nodes) > 1:
            transitions.append({
                "type": "potential_transition",
                "states": nodes[:2]
            })

    return transitions
