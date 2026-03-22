# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/topology_builder.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

NEIGHBOR_RADIUS = 2.5
MIN_NODE_CONNECTIONS = 3
MAX_POINTS = 1200  # safety


# --------------------------------------------------
# CORE
# --------------------------------------------------

def build_topology(points):
    """
    Build graph from spatial proximity
    """

    if points is None or len(points) == 0:
        return None, None

    # downsample (important!)
    if len(points) > MAX_POINTS:
        idx = np.random.choice(len(points), MAX_POINTS, replace=False)
        points = points[idx]

    tree = cKDTree(points)

    edges = []
    node_degree = np.zeros(len(points))

    for i, p in enumerate(points):
        neighbors = tree.query_ball_point(p, NEIGHBOR_RADIUS)

        for j in neighbors:
            if i == j:
                continue

            edges.append((i, j))
            node_degree[i] += 1

    return edges, node_degree


# --------------------------------------------------
# NODE DETECTION
# --------------------------------------------------

def detect_nodes(points, node_degree):
    """
    Nodes = high connectivity points
    """
    nodes = []

    for i, deg in enumerate(node_degree):
        if deg >= MIN_NODE_CONNECTIONS:
            nodes.append(points[i])

    if len(nodes) == 0:
        return None

    return np.array(nodes)


# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_topology(points, edges, nodes):
    plt.figure(figsize=(8, 8))

    # edges
    if edges is not None:
        for i, j in edges:
            x = [points[i][0], points[j][0]]
            y = [points[i][1], points[j][1]]
            plt.plot(x, y, alpha=0.1)

    # nodes
    if nodes is not None:
        plt.scatter(nodes[:, 0], nodes[:, 1], c="red", s=50)

    plt.title("Topology Graph (Loops + Channels + Nodes)")
    plt.axis("equal")
    plt.show()


# --------------------------------------------------
# FULL PIPELINE
# --------------------------------------------------

def build_topology_pipeline(points):
    edges, node_degree = build_topology(points)

    if edges is None:
        return None, None, None

    nodes = detect_nodes(points, node_degree)

    return edges, node_degree, nodes


# --------------------------------------------------
# TEST RUN
# --------------------------------------------------

if __name__ == "__main__":

    # synthetic example (spiral)
    t = np.linspace(0, 20, 1500)
    x = np.cos(t) * (1 + 0.1 * t)
    y = np.sin(t) * (1 + 0.1 * t)

    points = np.stack([x, y], axis=1)

    edges, node_degree, nodes = build_topology_pipeline(points)

    plot_topology(points, edges, nodes)
