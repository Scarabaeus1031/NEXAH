# tools/collapse_basin_map.py

import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import networkx as nx
import matplotlib.pyplot as plt

from FRAMEWORK.core.system_loader import load_system
from ENGINE.runtime.system_runner import build_regime_map
from FRAMEWORK.MESO.risk_geometry import compute_risk_geometry


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


def compute_collapse_basin(graph, collapse_states):

    collapse_basin = set(collapse_states)

    changed = True

    while changed:

        changed = False

        for node in graph.nodes():

            if node in collapse_basin:
                continue

            successors = list(graph.successors(node))

            if not successors:
                continue

            if all(s in collapse_basin for s in successors):

                collapse_basin.add(node)
                changed = True

    return collapse_basin


def visualize():

    system = load_system(SYSTEM_PATH)

    regime_map = build_regime_map(system)

    risk_geometry = compute_risk_geometry(regime_map)

    graph = regime_map["graph"]

    collapse_states = regime_map["collapse_states"]

    collapse_basin = compute_collapse_basin(graph, collapse_states)

    risk_gradient = risk_geometry["risk_gradient"]

    pos = nx.spring_layout(graph, seed=42)

    node_colors = []

    for node in graph.nodes():

        if node in collapse_states:
            node_colors.append("red")

        elif node in collapse_basin:
            node_colors.append("orange")

        else:
            node_colors.append("green")

    plt.figure(figsize=(11,8))

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2400,
        font_size=10
    )

    for node in graph.nodes():

        r = risk_gradient.get(node,0)

        x,y = pos[node]

        plt.text(
            x,
            y-0.08,
            f"risk={r:.2f}",
            fontsize=9,
            ha="center"
        )

    plt.title("NEXAH Collapse Basin Map")

    plt.show()


if __name__ == "__main__":

    visualize()
