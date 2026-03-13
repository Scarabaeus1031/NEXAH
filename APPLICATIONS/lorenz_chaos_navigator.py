"""
NEXAH Lorenz Chaos Navigator

This script demonstrates regime-based navigation on the Lorenz system.

It uses the Lorenz adapter to:

1. load the sampled Lorenz regime graph
2. define a start state
3. define a target regime
4. navigate forward through the graph until the target regime is reached
5. save navigation evidence and visualize the path

Artifacts are stored in:

APPLICATIONS/outputs/lorenz_navigation/

Outputs:

- lorenz_navigation_path.csv
- lorenz_navigation_path.png
- lorenz_navigation_report.txt
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt

from APPLICATIONS.adapters.examples.lorenz_adapter import LorenzAdapter


# ---------------------------------------------------
# Output directory
# ---------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------
# Navigation policy
# ---------------------------------------------------

REGIME_SCORE = {
    "LEFT_ATTRACTOR": 3.0,
    "RIGHT_ATTRACTOR": 3.0,
    "TRANSITION": 1.5,
    "ESCAPE": -5.0,
}


def choose_next_state_toward_target(current_state, graph, target_regime):
    """
    Choose the next state that best moves toward the target regime
    while avoiding ESCAPE states.
    """
    transitions = graph.get("transitions", {})
    regimes = graph.get("regimes", {})
    possible = transitions.get(current_state, [])

    if not possible:
        return None

    candidates = []

    for nxt in possible:
        regime = regimes.get(nxt, "TRANSITION")

        score = REGIME_SCORE.get(regime, 0.0)

        if regime == target_regime:
            score += 100.0

        if regime == "ESCAPE":
            score -= 1000.0

        candidates.append((score, nxt))

    candidates.sort(key=lambda x: x[0], reverse=True)

    return candidates[0][1]


# ---------------------------------------------------
# Navigation loop
# ---------------------------------------------------

def navigate_to_target_regime(adapter, start_state=None, target_regime="RIGHT_ATTRACTOR", max_steps=50):
    """
    Navigate through the sampled Lorenz graph until the target regime is reached.
    """
    graph = adapter.to_state_graph()
    states = graph["states"]
    regimes = graph["regimes"]
    node_states = adapter.node_states

    if start_state is None:
        start_state = graph.get("initial_state", states[0])

    current = start_state
    path = [current]
    report_lines = []

    report_lines.append("NEXAH Lorenz Chaos Navigator")
    report_lines.append(f"Start state: {start_state}")
    report_lines.append(f"Start regime: {regimes.get(start_state)}")
    report_lines.append(f"Target regime: {target_regime}")
    report_lines.append("")

    print("\n==============================")
    print("NEXAH LORENZ CHAOS NAVIGATOR")
    print("==============================")
    print("Start state:", start_state)
    print("Start regime:", regimes.get(start_state))
    print("Target regime:", target_regime)
    print("")

    if regimes.get(current) == target_regime:
        print("Start state already in target regime.")
        report_lines.append("Start state already in target regime.")
        return path, report_lines

    for step in range(max_steps):
        nxt = choose_next_state_toward_target(current, graph, target_regime)

        if nxt is None:
            line = "No further transition available."
            print(line)
            report_lines.append(line)
            break

        current_regime = regimes.get(current)
        next_regime = regimes.get(nxt)

        line = f"Step {step+1}: {current} ({current_regime}) -> {nxt} ({next_regime})"
        print(line)
        report_lines.append(line)

        path.append(nxt)

        if next_regime == target_regime:
            line = f"Target regime reached at state {nxt}."
            print(line)
            report_lines.append(line)
            break

        if next_regime == "ESCAPE":
            line = f"Escape state encountered at {nxt}. Stopping."
            print(line)
            report_lines.append(line)
            break

        current = nxt

    return path, report_lines


# ---------------------------------------------------
# Save path CSV
# ---------------------------------------------------

def save_navigation_path_csv(adapter, path):
    """
    Save navigation path with regime labels and coordinates.
    """
    regimes = adapter.regimes()
    node_states = adapter.node_states

    csv_path = os.path.join(OUTPUT_DIR, "lorenz_navigation_path.csv")

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["state", "regime", "x", "y", "z"])

        for state in path:
            x, y, z = node_states[state]
            writer.writerow([state, regimes[state], x, y, z])

    print("Saved:", csv_path)


# ---------------------------------------------------
# Save report
# ---------------------------------------------------

def save_navigation_report(report_lines):
    """
    Save text report.
    """
    report_path = os.path.join(OUTPUT_DIR, "lorenz_navigation_report.txt")

    with open(report_path, "w") as f:
        for line in report_lines:
            f.write(line + "\n")

    print("Saved:", report_path)


# ---------------------------------------------------
# Plot path in 3D
# ---------------------------------------------------

def plot_navigation_path(adapter, path):
    """
    Plot the navigation path in Lorenz state space.
    """
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

    xs = []
    ys = []
    zs = []

    for state in path:
        x, y, z = node_states[state]
        xs.append(x)
        ys.append(y)
        zs.append(z)

        ax.scatter(x, y, z, color=colors[regimes[state]], s=30)

    ax.plot(xs, ys, zs, linewidth=1.5)

    ax.set_title("Lorenz Chaos Navigation Path")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    img_path = os.path.join(OUTPUT_DIR, "lorenz_navigation_path.png")

    plt.savefig(img_path, dpi=200)
    print("Saved:", img_path)

    plt.show()
    plt.close()


# ---------------------------------------------------
# Main pipeline
# ---------------------------------------------------

def main():
    adapter = LorenzAdapter()

    # You can change this manually for experiments
    start_state = "s0"
    target_regime = "RIGHT_ATTRACTOR"

    path, report_lines = navigate_to_target_regime(
        adapter=adapter,
        start_state=start_state,
        target_regime=target_regime,
        max_steps=50,
    )

    save_navigation_path_csv(adapter, path)
    save_navigation_report(report_lines)
    plot_navigation_path(adapter, path)

    print("\nNavigation pipeline finished.\n")


if __name__ == "__main__":
    main()
