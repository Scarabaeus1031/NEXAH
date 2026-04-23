# tools/resilience_phase_diagram.py

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
# phase classification
# --------------------------------------------------

def classify_phase(score):

    if score >= 0.40:
        return "stable"

    if score >= 0.25:
        return "critical"

    if score >= 0.12:
        return "fragile"

    return "collapse"


# --------------------------------------------------
# phase diagram builder
# --------------------------------------------------

def build_phase_diagram(system_path, samples=1500):

    base = load_json(system_path)

    cells = {}

    for i in range(samples):

        candidate = random_architecture(base)

        try:
            score = score_system(candidate)

        except:
            score = 0

        d = round(edge_density(candidate), 1)
        c = round(cycle_ratio(candidate), 1)

        key = (d, c)

        if key not in cells:
            cells[key] = []

        cells[key].append(score)

        if i % 50 == 0:
            print("sample", i, "score", score)

    densities = sorted(list(set(k[0] for k in cells.keys())))
    cycles = sorted(list(set(k[1] for k in cells.keys())))

    score_grid = np.zeros((len(cycles), len(densities)))
    phase_grid = np.zeros((len(cycles), len(densities)))

    phase_map = {
        "collapse": 0,
        "fragile": 1,
        "critical": 2,
        "stable": 3
    }

    for (d, c), values in cells.items():

        avg = np.mean(values)

        phase = classify_phase(avg)

        x = densities.index(d)
        y = cycles.index(c)

        score_grid[y][x] = avg
        phase_grid[y][x] = phase_map[phase]

    return densities, cycles, score_grid, phase_grid


# --------------------------------------------------
# plotting
# --------------------------------------------------

def plot_score_landscape(densities, cycles, score_grid):

    plt.figure(figsize=(8,6))

    plt.imshow(
        score_grid,
        origin="lower",
        aspect="auto",
        extent=[min(densities), max(densities), min(cycles), max(cycles)]
    )

    plt.colorbar(label="Resilience Score")

    plt.xlabel("Edge Density")
    plt.ylabel("Cycle Ratio")

    plt.title("Resilience Phase Landscape")

    plt.show()


def plot_phase_classes(densities, cycles, phase_grid):

    plt.figure(figsize=(8,6))

    plt.imshow(
        phase_grid,
        origin="lower",
        aspect="auto",
        extent=[min(densities), max(densities), min(cycles), max(cycles)],
        vmin=0,
        vmax=3
    )

    cbar = plt.colorbar()

    cbar.set_ticks([0,1,2,3])
    cbar.set_ticklabels(["collapse","fragile","critical","stable"])

    plt.xlabel("Edge Density")
    plt.ylabel("Cycle Ratio")

    plt.title("Resilience Phase Classes")

    plt.show()


# --------------------------------------------------
# summary
# --------------------------------------------------

def print_summary(densities, cycles, score_grid):

    max_idx = np.unravel_index(np.argmax(score_grid), score_grid.shape)

    best_cycle = cycles[max_idx[0]]
    best_density = densities[max_idx[1]]
    best_score = score_grid[max_idx]

    print("\nBest Region")
    print("-----------")

    print("density:", best_density)
    print("cycle:", best_cycle)
    print("score:", best_score)


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    densities, cycles, score_grid, phase_grid = build_phase_diagram(
        BASE_SYSTEM,
        samples=1500
    )

    print_summary(densities, cycles, score_grid)

    plot_score_landscape(densities, cycles, score_grid)

    plot_phase_classes(densities, cycles, phase_grid)
