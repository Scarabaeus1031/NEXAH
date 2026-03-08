# tools/risk_landscape.py

import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from FRAMEWORK.core.system_loader import load_system
from ENGINE.runtime.system_runner import build_regime_map
from FRAMEWORK.MESO.risk_geometry import compute_risk_geometry


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


def visualize_risk_landscape():

    system = load_system(SYSTEM_PATH)

    regime_map = build_regime_map(system)

    risk_geometry = compute_risk_geometry(regime_map)

    graph = regime_map["graph"]

    risk_gradient = risk_geometry["risk_gradient"]

    pos = nx.spring_layout(graph, seed=42)

    risks = [risk_gradient.get(n, 0) for n in graph.nodes()]

    cmap = cm.get_cmap("RdYlGn")

    node_colors = [cmap(r) for r in risks]

    plt.figure(figsize=(11,8))

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2500,
        font_size=10
    )

    for node in graph.nodes():

        x,y = pos[node]

        r = risk_gradient.get(node,0)

        plt.text(
            x,
            y-0.09,
            f"risk={r:.2f}",
            fontsize=9,
            ha="center"
        )

    sm = plt.cm.ScalarMappable(
        cmap=cmap,
        norm=plt.Normalize(vmin=0, vmax=1)
    )

    sm.set_array([])

    cbar = plt.colorbar(sm)
    cbar.set_label("Risk Level")

    plt.title("NEXAH Risk Landscape")

    plt.show()


if __name__ == "__main__":

    visualize_risk_landscape()
