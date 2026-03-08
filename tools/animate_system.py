# tools/animate_system.py

import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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


def animate(system, regime_map, risk_geometry, trajectory):

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

    fig, ax = plt.subplots(figsize=(11, 8))

    def draw_base():

        ax.clear()

        nx.draw(
            graph,
            pos,
            ax=ax,
            with_labels=True,
            node_color=node_colors,
            node_size=2200,
            font_size=10
        )

        ax.set_title("NEXAH System Navigation (Animated)")

    def update(frame):

        draw_base()

        if frame == 0:
            return

        edges = list(zip(trajectory[:frame], trajectory[1:frame+1]))

        nx.draw_networkx_edges(
            graph,
            pos,
            ax=ax,
            edgelist=edges,
            edge_color="blue",
            width=4
        )

        current_node = trajectory[frame]

        nx.draw_networkx_nodes(
            graph,
            pos,
            ax=ax,
            nodelist=[current_node],
            node_color="cyan",
            node_size=2600
        )

    anim = FuncAnimation(
        fig,
        update,
        frames=len(trajectory),
        interval=800,
        repeat=False
    )

    plt.show()


if __name__ == "__main__":

    system, regime_map, risk_geometry, trajectory = simulate(SYSTEM_PATH)

    print("Trajectory:", trajectory)

    animate(system, regime_map, risk_geometry, trajectory)
