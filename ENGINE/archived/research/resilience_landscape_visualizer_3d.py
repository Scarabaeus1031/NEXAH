"""
NEXAH 3D Resilience Landscape Visualizer
"""

from ENGINE.results_store import load_all_results

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def run_visualization():

    results = load_all_results()

    xs = []
    ys = []
    zs = []

    for r in results:

        graph = r.get("graph", {})
        resilience = r.get("resilience", {})

        nodes = len(graph.get("nodes", []))
        edges = len(graph.get("edges", []))
        score = resilience.get("resilience_score")

        if score is None:
            continue

        xs.append(nodes)
        ys.append(edges)
        zs.append(score)

    if not xs:
        print("No data available.")
        return

    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(xs, ys, zs)

    ax.set_xlabel("Nodes")
    ax.set_ylabel("Edges")
    ax.set_zlabel("Resilience")

    ax.set_title("NEXAH Resilience Landscape")

    plt.show()


if __name__ == "__main__":

    run_visualization()
