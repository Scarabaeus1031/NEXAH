# tools/architecture_map.py

import sys
import os
import networkx as nx
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from FRAMEWORK.core.system_loader import load_system
from ENGINE.runtime.system_runner import build_regime_map


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


def detect_structure(graph, collapse_states):

    collapse_states = set(collapse_states)
    critical_states = set()

    for node in graph.nodes():

        successors = list(graph.successors(node))

        for succ in successors:
            if succ in collapse_states:
                critical_states.add(node)

    safe_states = set(graph.nodes()) - collapse_states - critical_states

    return safe_states, critical_states, collapse_states


def draw_architecture():

    system = load_system(SYSTEM_PATH)

    regime_map = build_regime_map(system)

    graph = regime_map["graph"]

    collapse_states = regime_map["collapse_states"]

    safe_states, critical_states, collapse_states = detect_structure(
        graph,
        collapse_states
    )

    pos = nx.spring_layout(graph, seed=42)

    node_colors = []

    for node in graph.nodes():

        if node in collapse_states:
            node_colors.append("red")

        elif node in critical_states:
            node_colors.append("orange")

        else:
            node_colors.append("green")

    plt.figure(figsize=(10,7))

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2200,
        font_size=10
    )

    plt.title("System Architecture Map\nGreen=Safe  Orange=Critical  Red=Collapse")

    plt.show()


if __name__ == "__main__":
    draw_architecture()
