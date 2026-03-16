# tools/catastrophe_detector.py

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


def detect_catastrophes(graph, collapse_states):
    """
    Detect catastrophic structures in the state graph.

    Returns:
        collapse_states:
            states already classified as collapse

        critical_states:
            states with at least one outgoing edge into collapse

        irreversible_edges:
            edges that directly enter collapse states

        safe_states:
            states not currently classified as critical/collapse
    """

    collapse_states = set(collapse_states)
    critical_states = set()
    irreversible_edges = []

    for node in graph.nodes():

        successors = list(graph.successors(node))

        for succ in successors:

            if succ in collapse_states:
                critical_states.add(node)
                irreversible_edges.append((node, succ))

    safe_states = set(graph.nodes()) - collapse_states - critical_states

    return {
        "collapse_states": collapse_states,
        "critical_states": critical_states,
        "irreversible_edges": irreversible_edges,
        "safe_states": safe_states,
    }


def visualize(graph, catastrophe_info, risk_geometry):
    """
    Visualize catastrophic structure of the graph.
    """

    pos = nx.spring_layout(graph, seed=42)

    collapse_states = catastrophe_info["collapse_states"]
    critical_states = catastrophe_info["critical_states"]
    irreversible_edges = catastrophe_info["irreversible_edges"]
    safe_states = catastrophe_info["safe_states"]

    risk_gradient = risk_geometry["risk_gradient"]

    node_colors = []
    for node in graph.nodes():

        if node in collapse_states:
            node_colors.append("red")
        elif node in critical_states:
            node_colors.append("orange")
        else:
            node_colors.append("green")

    plt.figure(figsize=(11, 8))

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2500,
        font_size=10
    )

    # Highlight dangerous edges
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=irreversible_edges,
        edge_color="red",
        width=3
    )

    # Add labels under nodes
    for node in graph.nodes():

        x, y = pos[node]
        risk = risk_gradient.get(node, 0)

        if node in collapse_states:
            label = f"collapse\nrisk={risk:.2f}"
        elif node in critical_states:
            label = f"critical\nrisk={risk:.2f}"
        else:
            label = f"safe\nrisk={risk:.2f}"

        plt.text(
            x,
            y - 0.09,
            label,
            fontsize=9,
            ha="center"
        )

    plt.title("NEXAH Catastrophe Detector")

    plt.show()


def main():
    system = load_system(SYSTEM_PATH)
    regime_map = build_regime_map(system)
    risk_geometry = compute_risk_geometry(regime_map)

    graph = regime_map["graph"]
    collapse_states = regime_map["collapse_states"]

    catastrophe_info = detect_catastrophes(graph, collapse_states)

    print("\nDetected Catastrophe Structure\n")

    print("Collapse states:")
    for s in sorted(catastrophe_info["collapse_states"]):
        print(" -", s)

    print("\nCritical states:")
    for s in sorted(catastrophe_info["critical_states"]):
        print(" -", s)

    print("\nIrreversible collapse edges:")
    for a, b in catastrophe_info["irreversible_edges"]:
        print(f" - {a} -> {b}")

    print("\nSafe states:")
    for s in sorted(catastrophe_info["safe_states"]):
        print(" -", s)

    visualize(graph, catastrophe_info, risk_geometry)


if __name__ == "__main__":
    main()
