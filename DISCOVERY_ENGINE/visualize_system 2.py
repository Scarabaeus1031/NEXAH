# tools/visualize_system.py

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
from FRAMEWORK.NEXAH.navigation_policy import select_safest_transition
from FRAMEWORK.MEVA.execution_engine import ExecutionEngine

SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


def simulate(system_path):

    system = load_system(system_path)

    regime_map = build_regime_map(system)

    risk_geometry = compute_risk_geometry(regime_map)

    graph = regime_map["graph"]

    start_state = system.nodes[0]

    engine_safe = ExecutionEngine(regime_map, risk_geometry)
    engine_safe.set_initial_state(start_state)

    def safe_policy(state):
        return select_safest_transition(
            state,
            regime_map,
            risk_geometry
        )

    safe_traj = engine_safe.run(safe_policy, max_steps=20)

    engine_naive = ExecutionEngine(regime_map, risk_geometry)
    engine_naive.set_initial_state(start_state)

    def naive_policy(state):

        successors = list(graph.successors(state))

        if not successors:
            return state

        return successors[0]

    naive_traj = engine_naive.run(naive_policy, max_steps=20)

    return system, regime_map, risk_geometry, safe_traj, naive_traj, start_state


def visualize(system, regime_map, risk_geometry, safe_traj, naive_traj):

    graph = regime_map["graph"]

    pos = nx.spring_layout(graph, seed=42)

    risk_gradient = risk_geometry["risk_gradient"]

    node_colors = []

    for node in graph.nodes():

        r = risk_gradient.get(node, 0)

        if r > 0.66:
            node_colors.append("green")

        elif r > 0.33:
            node_colors.append("gold")

        else:
            node_colors.append("red")

    plt.figure(figsize=(11, 8))

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2200,
        font_size=10
    )

    safe_edges = list(zip(safe_traj, safe_traj[1:]))

    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=safe_edges,
        edge_color="blue",
        width=4
    )

    naive_edges = list(zip(naive_traj, naive_traj[1:]))

    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=naive_edges,
        edge_color="red",
        width=3,
        style="dashed"
    )

    plt.title("NEXAH Navigation in Risk Field — Blue: Stabilizing Policy | Red: Collapse Path")

    plt.show()


if __name__ == "__main__":

    system, regime_map, risk_geometry, safe_traj, naive_traj, start_state = simulate(SYSTEM_PATH)

    print("Start state:", start_state)
    print("Safe trajectory:", safe_traj)
    print("Naive trajectory:", naive_traj)

    visualize(system, regime_map, risk_geometry, safe_traj, naive_traj)
