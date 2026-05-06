# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/transition_node_finder.py

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

ANGLE_THRESHOLD = 0.35     # radians (~20°)
MIN_DISTANCE = 5           # min index distance between nodes


# --------------------------------------------------
# CORE: ANGLE-BASED NODE DETECTION
# --------------------------------------------------

def compute_angles(trajectory):
    """
    Compute turning angle at each point
    """
    directions = np.diff(trajectory, axis=0)

    norms = np.linalg.norm(directions, axis=1, keepdims=True)
    directions = directions / (norms + 1e-8)

    angles = []

    for i in range(len(directions) - 1):
        v1 = directions[i]
        v2 = directions[i + 1]

        dot = np.clip(np.dot(v1, v2), -1.0, 1.0)
        angle = np.arccos(dot)

        angles.append(angle)

    return np.array(angles)


def detect_transition_nodes(trajectory):
    """
    Detect high-curvature points = transition nodes
    """
    angles = compute_angles(trajectory)

    nodes = []

    last_idx = -MIN_DISTANCE

    for i, angle in enumerate(angles):
        if angle > ANGLE_THRESHOLD:
            if i - last_idx >= MIN_DISTANCE:
                nodes.append(i)
                last_idx = i

    return np.array(nodes), angles


# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_nodes(trajectory, nodes):
    """
    Plot trajectory with detected nodes
    """
    plt.figure(figsize=(8, 8))

    plt.plot(trajectory[:, 0], trajectory[:, 1], alpha=0.3)

    if len(nodes) > 0:
        pts = trajectory[nodes]
        plt.scatter(pts[:, 0], pts[:, 1], c="red", s=50)

    plt.title("Detected Transition Nodes")
    plt.axis("equal")
    plt.show()


# --------------------------------------------------
# FULL PIPELINE
# --------------------------------------------------

def find_transition_nodes(trajectory):
    nodes, angles = detect_transition_nodes(trajectory)
    return nodes, angles


# --------------------------------------------------
# TEST RUN
# --------------------------------------------------

if __name__ == "__main__":
    t = np.linspace(0, 20, 1500)

    # test trajectory (spiral + distortion)
    x = np.cos(t) * (1 + 0.1 * t)
    y = np.sin(t) * (1 + 0.1 * t)

    # add slight deformation (to create nodes)
    x += 0.2 * np.sin(3 * t)

    trajectory = np.stack([x, y], axis=1)

    nodes, angles = find_transition_nodes(trajectory)

    plot_nodes(trajectory, nodes)
