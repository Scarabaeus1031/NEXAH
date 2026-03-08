import sys
import os
import random

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from FRAMEWORK.core.system_loader import load_system
from ENGINE.runtime.system_runner import build_regime_map
from FRAMEWORK.MESO.risk_geometry import compute_risk_geometry
from FRAMEWORK.NEXAH.navigation_policy import select_safest_transition


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


def simulate_from_state(start_state, graph, regime_map, risk_geometry, collapse_states, steps=20):

    state = start_state

    for _ in range(steps):

        next_state = select_safest_transition(
            state,
            regime_map,
            risk_geometry
        )

        state = next_state

        if state in collapse_states:
            return "collapse"

    return "stable"


def compute_phase_space():

    system = load_system(SYSTEM_PATH)

    regime_map = build_regime_map(system)

    risk_geometry = compute_risk_geometry(regime_map)

    graph = regime_map["graph"]

    collapse_states = regime_map["collapse_states"]

    states = list(graph.nodes())

    results = {}

    for state in states:

        outcome = simulate_from_state(
            state,
            graph,
            regime_map,
            risk_geometry,
            collapse_states
        )

        results[state] = outcome

    return graph, results


def visualize_phase_space(graph, results):

    pos = nx.spring_layout(graph, seed=42)

    node_colors = []

    for node in graph.nodes():

        if results[node] == "collapse":
            node_colors.append("red")
        else:
            node_colors.append("green")

    plt.figure(figsize=(10, 7))

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2500,
        font_size=10
    )

    for node in graph.nodes():

        x, y = pos[node]

        label = results[node]

        plt.text(
            x,
            y - 0.08,
            label,
            fontsize=9,
            ha="center"
        )

    plt.title("NEXAH Phase Space Map (Stability vs Collapse)")

    plt.show()


if __name__ == "__main__":

    graph, results = compute_phase_space()

    print("Phase space results:")
    for k, v in results.items():
        print(k, "->", v)

    visualize_phase_space(graph, results)
