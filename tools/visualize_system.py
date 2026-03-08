# tools/visualize_system.py

import sys
import os

# Add repository root to Python path
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


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid.json"

# Optional default start state (will be auto-corrected if not present)
START_STATE = "S0_normal"


def simulate(system_path, start_state):

    system = load_system(system_path)

    # Auto-fix start state if it does not exist
    if start_state not in system.nodes:
        start_state = system.nodes[0]

    regime_map = build_regime_map(system)

    risk_geometry = compute_risk_geometry(regime_map)

    engine = ExecutionEngine(regime_map, risk_geometry)

    engine.set_initial_state(start_state)

    def policy(state):
        return select_safest_transition(
            state,
            regime_map,
            risk_geometry
        )

    trajectory = engine.run(policy, max_steps=20)

    return system, regime_map, risk_geometry, trajectory, start_state


def visualize(system, regime_map, risk_geometry, trajectory):

    graph = regime_map["graph"]

    pos = nx.spring_layout(graph, seed=42)

    plt.figure(figsize=(10, 7))

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=2000,
        font_size=9
    )

    edges = list(zip(trajectory, trajectory[1:]))

    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=edges,
        edge_color="red",
        width=3
    )

    plt.title("NEXAH System Simulation")
    plt.show()


if __name__ == "__main__":

    system, regime_map, risk_geometry, trajectory, start_state = simulate(
        SYSTEM_PATH,
        START_STATE
    )

    print("Start state:", start_state)
    print("Trajectory:")
    print(trajectory)

    visualize(system, regime_map, risk_geometry, trajectory)        edge_color="red",
        width=3
    )

    plt.title("NEXAH System Simulation")
    plt.show()


if __name__ == "__main__":

    system, regime_map, risk_geometry, trajectory = simulate(
        SYSTEM_PATH,
        START_STATE
    )

    print("Trajectory:")
    print(trajectory)

    visualize(system, regime_map, risk_geometry, trajectory)
