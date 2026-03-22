# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/topology_builder.py

import numpy as np
from scipy.spatial import cKDTree


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

NEIGHBOR_RADIUS = 2.5
MIN_NODE_CONNECTIONS = 3
MAX_POINTS = 1200


# --------------------------------------------------
# CORE GRAPH FROM POINT CLOUD
# --------------------------------------------------

def build_topology(points):

    if points is None or len(points) == 0:
        return {}

    # downsample
    if len(points) > MAX_POINTS:
        idx = np.random.choice(len(points), MAX_POINTS, replace=False)
        points = points[idx]

    tree = cKDTree(points)

    graph = {i: [] for i in range(len(points))}

    for i, p in enumerate(points):
        neighbors = tree.query_ball_point(p, NEIGHBOR_RADIUS)

        for j in neighbors:
            if i == j:
                continue

            graph[i].append(j)

    return graph


# --------------------------------------------------
# NODE DETECTION
# --------------------------------------------------

def detect_nodes(points, graph):

    nodes = []

    for i, neighbors in graph.items():
        if len(neighbors) >= MIN_NODE_CONNECTIONS:
            nodes.append(points[i])

    if len(nodes) == 0:
        return None

    return np.array(nodes)


# --------------------------------------------------
# SAFE POINT HANDLING (🔥 KEY FIX)
# --------------------------------------------------

def safe_add_point(container, p):
    """
    Ensures point is always flattened to shape (2,)
    """
    try:
        p = np.array(p).reshape(-1)

        if len(p) >= 2:
            container.append(p[:2])

    except Exception:
        pass


# --------------------------------------------------
# 🔥 PIPELINE ADAPTER (FIXED)
# --------------------------------------------------

def build_topology_from_components(loops, channels, nodes):
    """
    Convert loops + channels + nodes → unified point cloud
    """

    all_points = []

    # loops
    if loops is not None:
        _, loop_points, _ = loops
        if loop_points is not None:
            for p in loop_points:
                safe_add_point(all_points, p)

    # channels
    if channels is not None:
        for ch in channels:
            for p in ch:
                safe_add_point(all_points, p)

    # nodes
    if nodes is not None:
        for p in nodes:
            safe_add_point(all_points, p)

    if len(all_points) == 0:
        return {}

    # guaranteed clean array
    all_points = np.array(all_points)

    return build_topology(all_points)


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":
    print("Topology Builder Ready")
