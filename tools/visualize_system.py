# tools/visualize_system.py

import networkx as nx
import matplotlib.pyplot as plt

from FRAMEWORK.core.system_loader import load_system
from ENGINE.runtime.system_runner import build_regime_map
from FRAMEWORK.MESO.risk_geometry import compute_risk_geometry
from FRAMEWORK.NEXAH.navigation_policy import select_safest_transition
from FRAMEWORK.MEVA.execution_engine import ExecutionEngine


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid.json"
START_STATE = "stable"


def simulate(system_path, start_state):

    system = load_system(system_path)

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

    return system, regime_map, risk_geometry, trajectory


def visualize(system, regime_map, risk_geometry, trajectory):

    graph = regime_map["graph"]

    pos = nx.spring_layout(graph, seed=42)

    collapse_states = regime_map["collapse_states"]

    risk_gradient = risk_geometry["risk_gradient"]

    node_colors = []

    for node in graph.nodes():

        if node in collapse_states:
            node_colors.append("red")

        else:

            score = risk_gradient.get(node, 0)

            if score > 0.7:
                node_colors.append("green")

            elif score > 0.4:
                node_colors.append("orange")

            else:
                node_colors.append("yellow")

    plt.figure(figsize=(10, 7))

    nx.draw_networkx_nodes(
        graph,
        pos,
        node_color=node_colors,
        node_size=900
    )

    nx.draw_networkx_edges(
        graph,
        pos,
        arrows=True
    )

    nx.draw_networkx_labels(
        graph,
        pos,
        font_size=10
    )

    # draw trajectory path

    path_edges = []

    for i in range(len(trajectory) - 1):
        path_edges.append((trajectory[i], trajectory[i + 1]))

    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=path_edges,
        width=3,
        edge_color="blue"
    )

    plt.title("NEXAH System Visualization")
    plt.axis("off")
    plt.show()


def main():

    system, regime_map, risk_geometry, trajectory = simulate(
        SYSTEM_PATH,
        START_STATE
    )

    print("\nTrajectory:")
    print(trajectory)

    visualize(
        system,
        regime_map,
        risk_geometry,
        trajectory
    )


if __name__ == "__main__":

    main()
