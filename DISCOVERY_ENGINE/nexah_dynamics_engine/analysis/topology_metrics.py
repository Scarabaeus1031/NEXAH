# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/topology_metrics.py

import numpy as np


# --------------------------------------------------
# NODE DEGREE ANALYSIS
# --------------------------------------------------

def compute_node_degrees(graph):
    degrees = {node: len(neighbors) for node, neighbors in graph.items()}
    return degrees


def degree_distribution(degrees):
    values = list(degrees.values())
    unique, counts = np.unique(values, return_counts=True)
    return dict(zip(unique, counts))


# --------------------------------------------------
# CHANNEL LENGTHS
# --------------------------------------------------

def compute_channel_lengths(channels):
    lengths = []

    for ch in channels:
        diffs = np.diff(ch, axis=0)
        dist = np.sum(np.linalg.norm(diffs, axis=1))
        lengths.append(dist)

    return lengths


# --------------------------------------------------
# LOOP SIZE
# --------------------------------------------------

def compute_loop_sizes(loops):
    sizes = []

    for loop in loops:
        diffs = np.diff(loop, axis=0)
        dist = np.sum(np.linalg.norm(diffs, axis=1))
        sizes.append(dist)

    return sizes


# --------------------------------------------------
# ANGLE ANALYSIS
# --------------------------------------------------

def compute_angles(points):
    angles = []

    for i in range(1, len(points) - 1):
        v1 = points[i] - points[i - 1]
        v2 = points[i + 1] - points[i]

        v1 = v1 / (np.linalg.norm(v1) + 1e-8)
        v2 = v2 / (np.linalg.norm(v2) + 1e-8)

        dot = np.clip(np.dot(v1, v2), -1.0, 1.0)
        angle = np.arccos(dot) * 180 / np.pi

        angles.append(angle)

    return angles


def detect_preferred_angles(angles, tolerance=5):
    targets = [30, 45, 60, 72, 90, 120, 137.5]
    hits = {t: 0 for t in targets}

    for a in angles:
        for t in targets:
            if abs(a - t) < tolerance:
                hits[t] += 1

    return hits


# --------------------------------------------------
# GRAPH CENTRALITY
# --------------------------------------------------

def find_hubs(degrees, threshold=5):
    return [node for node, deg in degrees.items() if deg >= threshold]


# --------------------------------------------------
# 🔥 MAIN API FUNCTION (FIX)
# --------------------------------------------------

def compute_topology_metrics(graph):
    """
    Main function used by pipeline
    """

    degrees = compute_node_degrees(graph)
    degree_dist = degree_distribution(degrees)
    hubs = find_hubs(degrees)

    metrics = {
        "num_nodes": len(graph),
        "num_edges": sum(len(v) for v in graph.values()) // 2,
        "degree_distribution": degree_dist,
        "num_hubs": len(hubs),
        "avg_degree": np.mean(list(degrees.values())) if degrees else 0
    }

    return metrics


# --------------------------------------------------
# OPTIONAL SUMMARY (KEEP)
# --------------------------------------------------

def summarize_topology(graph, loops=None, channels=None):
    degrees = compute_node_degrees(graph)
    degree_dist = degree_distribution(degrees)

    loop_sizes = compute_loop_sizes(loops) if loops else []
    channel_lengths = compute_channel_lengths(channels) if channels else []

    hubs = find_hubs(degrees)

    summary = {
        "degree_distribution": degree_dist,
        "num_hubs": len(hubs),
        "avg_loop_size": np.mean(loop_sizes) if loop_sizes else 0,
        "avg_channel_length": np.mean(channel_lengths) if channels else 0,
    }

    return summary


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":
    print("Topology Metrics Module Ready")
    Compute angles between consecutive segments
    """
    angles = []

    for i in range(1, len(points) - 1):
        v1 = points[i] - points[i - 1]
        v2 = points[i + 1] - points[i]

        # normalize
        v1 = v1 / (np.linalg.norm(v1) + 1e-8)
        v2 = v2 / (np.linalg.norm(v2) + 1e-8)

        dot = np.clip(np.dot(v1, v2), -1.0, 1.0)
        angle = np.arccos(dot) * 180 / np.pi

        angles.append(angle)

    return angles


def detect_preferred_angles(angles, tolerance=5):
    """
    Detect clustering near known geometric angles
    """
    targets = [30, 45, 60, 72, 90, 120, 137.5]
    hits = {t: 0 for t in targets}

    for a in angles:
        for t in targets:
            if abs(a - t) < tolerance:
                hits[t] += 1

    return hits


# --------------------------------------------------
# GRAPH CENTRALITY (simple)
# --------------------------------------------------

def find_hubs(degrees, threshold=5):
    """
    Find high-degree nodes
    """
    hubs = [node for node, deg in degrees.items() if deg >= threshold]
    return hubs


# --------------------------------------------------
# SUMMARY REPORT
# --------------------------------------------------

def summarize_topology(graph, loops, channels):
    degrees = compute_node_degrees(graph)
    degree_dist = degree_distribution(degrees)

    loop_sizes = compute_loop_sizes(loops) if loops else []
    channel_lengths = compute_channel_lengths(channels) if channels else []

    hubs = find_hubs(degrees)

    summary = {
        "degree_distribution": degree_dist,
        "num_hubs": len(hubs),
        "avg_loop_size": np.mean(loop_sizes) if loop_sizes else 0,
        "avg_channel_length": np.mean(channel_lengths) if channels else 0,
    }

    return summary


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":
    print("Topology Metrics Module Ready")
