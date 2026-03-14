# tools/resilience_landscape.py

import sys
import os
import json
import copy
import random
import tempfile
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_analyzer import analyze_system


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


# -----------------------------
# utilities
# -----------------------------

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def write_temp_system(data):
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(data, tmp, indent=2)
    tmp.close()
    return tmp.name


def score_system(data):

    temp_path = write_temp_system(data)

    try:
        report = analyze_system(temp_path)
        return report["resilience_score"]

    finally:
        os.remove(temp_path)


def normalize_transitions(data):

    transitions = data.get("transitions", {})
    normalized = {}

    for state, targets in transitions.items():

        if isinstance(targets, list):
            normalized[state] = list(targets)
        else:
            normalized[state] = [targets]

    data["transitions"] = normalized

    return data


def rebuild_edges(data):

    edges = []

    for s, targets in data["transitions"].items():
        for t in targets:
            edges.append([s, t])

    data["edges"] = edges

    return data


# -----------------------------
# mutation helpers
# -----------------------------

def add_random_edge(data):

    nodes = data["nodes"]

    s = random.choice(nodes)
    t = random.choice(nodes)

    if s != t and t not in data["transitions"].get(s, []):
        data["transitions"].setdefault(s, []).append(t)

    return rebuild_edges(data)


def remove_random_edge(data):

    all_edges = []

    for s, targets in data["transitions"].items():
        for t in targets:
            all_edges.append((s, t))

    if not all_edges:
        return data

    s, t = random.choice(all_edges)

    if len(data["transitions"].get(s, [])) <= 1:
        return data

    data["transitions"][s] = [x for x in data["transitions"][s] if x != t]

    return rebuild_edges(data)


# -----------------------------
# SAFE density adjustment
# -----------------------------

def apply_density(data, target_density):

    data = copy.deepcopy(data)

    nodes = len(data["nodes"])
    max_edges = nodes * nodes

    for _ in range(200):  # prevents infinite loop

        current_edges = len(data["edges"])
        current_density = current_edges / max_edges

        if abs(current_density - target_density) < 0.02:
            break

        if current_density < target_density:
            data = add_random_edge(data)
        else:
            data = remove_random_edge(data)

    return data


# -----------------------------
# landscape computation
# -----------------------------

def compute_landscape(system_path):

    base = load_json(system_path)
    base = normalize_transitions(base)
    base = rebuild_edges(base)

    densities = np.linspace(0.1, 0.9, 12)
    noise_levels = np.linspace(0.0, 1.0, 12)

    landscape = np.zeros((len(noise_levels), len(densities)))

    for i, noise in enumerate(noise_levels):

        print(f"\nNoise layer: {noise:.2f}")

        for j, density in enumerate(densities):

            candidate = apply_density(base, density)

            try:
                score = score_system(candidate)

                # noise degrades stability
                score = score * (1 - noise * 0.4)

            except Exception:
                score = 0

            landscape[i, j] = score

            print(f"density={density:.2f} noise={noise:.2f} score={score:.3f}")

    return densities, noise_levels, landscape


# -----------------------------
# visualization
# -----------------------------

def visualize(densities, noise_levels, landscape):

    plt.figure(figsize=(8,6))

    plt.imshow(
        landscape,
        origin="lower",
        aspect="auto",
        extent=[
            densities[0],
            densities[-1],
            noise_levels[0],
            noise_levels[-1]
        ]
    )

    plt.colorbar(label="Resilience Score")

    plt.xlabel("Edge Density")
    plt.ylabel("Noise Level")

    plt.title("System Resilience Landscape")

    plt.show()


# -----------------------------
# main
# -----------------------------

if __name__ == "__main__":

    densities, noise_levels, landscape = compute_landscape(SYSTEM_PATH)

    visualize(densities, noise_levels, landscape)
