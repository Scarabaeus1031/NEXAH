"""
NEXAH Lorenz Chaos Navigator (Graph Search Version)

This script searches a path through the Lorenz regime graph
to reach a desired regime.

Artifacts are saved in:

APPLICATIONS/outputs/lorenz_navigation/
"""

import os
import csv
from collections import deque
import matplotlib.pyplot as plt

from APPLICATIONS.adapters.examples.lorenz_adapter import LorenzAdapter


# ---------------------------------------------------
# Output directory
# ---------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------
# BFS search for target regime
# ---------------------------------------------------

def find_path_to_regime(adapter, start_state, target_regime):

    graph = adapter.to_state_graph()
    transitions = graph["transitions"]
    regimes = graph["regimes"]

    visited = set()
    queue = deque([[start_state]])

    while queue:

        path = queue.popleft()
        node = path[-1]

        if node in visited:
            continue

        visited.add(node)

        if regimes[node] == target_regime and node != start_state:
            return path

        for nxt in transitions.get(node, []):
            if nxt not in visited:
                new_path = list(path)
                new_path.append(nxt)
                queue.append(new_path)

    return None


# ---------------------------------------------------
# Save navigation CSV
# ---------------------------------------------------

def save_navigation_csv(adapter, path):

    regimes = adapter.regimes()
    node_states = adapter.node_states

    csv_path = os.path.join(OUTPUT_DIR, "lorenz_navigation_path.csv")

    with open(csv_path, "w", newline="") as f:

        writer = csv.writer(f)
        writer.writerow(["state", "regime", "x", "y", "z"])

        for s in path:
            x, y, z = node_states[s]
            writer.writerow([s, regimes[s], x, y, z])

    print("Saved:", csv_path)


# ---------------------------------------------------
# Save report
# ---------------------------------------------------

def save_report(lines):

    report_path = os.path.join(OUTPUT_DIR, "lorenz_navigation_report.txt")

    with open(report_path, "w") as f:
        for l in lines:
            f.write(l + "\n")

    print("Saved:", report_path)


# ---------------------------------------------------
# Plot navigation
# ---------------------------------------------------

def plot_navigation(adapter, path):

    node_states = adapter.node_states
    regimes = adapter.regimes()

    colors = {
        "LEFT_ATTRACTOR": "blue",
        "RIGHT_ATTRACTOR": "red",
        "TRANSITION": "gold",
        "ESCAPE": "black"
    }

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    xs, ys, zs = [], [], []

    for s in path:

        x, y, z = node_states[s]

        xs.append(x)
        ys.append(y)
        zs.append(z)

        ax.scatter(
            x,
            y,
            z,
            color=colors[regimes[s]],
            s=40
        )

    ax.plot(xs, ys, zs, linewidth=2)

    ax.set_title("Lorenz Regime Navigation Path")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    img = os.path.join(OUTPUT_DIR, "lorenz_navigation_path.png")

    plt.savefig(img, dpi=200)
    print("Saved:", img)

    plt.show()
    plt.close()


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():

    adapter = LorenzAdapter()

    graph = adapter.to_state_graph()

    start_state = graph["initial_state"]
    target_regime = "RIGHT_ATTRACTOR"

    print("\n==============================")
    print("NEXAH CHAOS NAVIGATOR (BFS)")
    print("==============================")

    print("Start state:", start_state)
    print("Target regime:", target_regime)

    path = find_path_to_regime(adapter, start_state, target_regime)

    report = []

    if path:

        print("\nFound path:\n")

        for s in path:

            regime = adapter.regimes()[s]
            line = f"{s} ({regime})"

            print(line)
            report.append(line)

    else:

        print("No path found")
        report.append("No path found")
        return

    save_navigation_csv(adapter, path)
    save_report(report)
    plot_navigation(adapter, path)

    print("\nNavigation finished.\n")


if __name__ == "__main__":
    main()
