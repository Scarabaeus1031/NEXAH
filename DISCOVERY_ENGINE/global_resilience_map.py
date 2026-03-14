# tools/global_resilience_map.py

import sys
import os
import json
import matplotlib.pyplot as plt
import networkx as nx

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_analyzer import analyze_system


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"
BEST_PATH = "APPLICATIONS/examples/energy_grid_global_best.json"


def load_system(path):
    with open(path, "r") as f:
        return json.load(f)


def build_graph(system):

    G = nx.DiGraph()

    nodes = system.get("nodes", [])
    edges = system.get("edges", [])

    for n in nodes:
        G.add_node(n)

    for s, t in edges:
        G.add_edge(s, t)

    return G


def classify_states(report):

    safe = set(report["safe_states"])
    critical = set(report["critical_states"])
    collapse = set(report["collapse_states"])

    return safe, critical, collapse


def draw_system(ax, system, report, title):

    G = build_graph(system)

    safe, critical, collapse = classify_states(report)

    pos = nx.spring_layout(G, seed=42)

    node_colors = []

    for n in G.nodes():

        if n in collapse:
            node_colors.append("red")

        elif n in critical:
            node_colors.append("orange")

        else:
            node_colors.append("green")

    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color=node_colors,
        node_size=2000,
        font_size=9
    )

    ax.set_title(title)


def main():

    base_system = load_system(SYSTEM_PATH)
    best_system = load_system(BEST_PATH)

    base_report = analyze_system(SYSTEM_PATH)
    best_report = analyze_system(BEST_PATH)

    fig, axes = plt.subplots(1, 2, figsize=(12,6))

    draw_system(
        axes[0],
        base_system,
        base_report,
        f"Base System\nScore={base_report['resilience_score']:.3f}"
    )

    draw_system(
        axes[1],
        best_system,
        best_report,
        f"Best Found System\nScore={best_report['resilience_score']:.3f}"
    )

    plt.suptitle("Global Resilience Architecture Comparison")

    plt.show()


if __name__ == "__main__":
    main()
