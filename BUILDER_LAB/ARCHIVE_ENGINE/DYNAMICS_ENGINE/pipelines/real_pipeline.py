# pipelines/real_pipeline.py

import os
import json
import numpy as np
import matplotlib.pyplot as plt

# --- IMPORTS AUS ANALYSIS ---
from analysis.loop_detector import detect_loops
from analysis.channel_extractor import extract_channels
from analysis.transition_node_finder import find_transition_nodes
from analysis.topology_builder import build_topology_from_components
from analysis.topology_metrics import compute_topology_metrics
from analysis.topology_signature import compute_topology_signature
from analysis.topology_classifier import classify_topology
from analysis.angle_field import analyze_angle_distribution


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

OUTPUT_DIR = "outputs"
VISUAL_DIR = os.path.join(OUTPUT_DIR, "visuals", "topology")
JSON_DIR = os.path.join(OUTPUT_DIR, "json")

os.makedirs(VISUAL_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)


# --------------------------------------------------
# JSON SAFETY
# --------------------------------------------------

def make_json_safe(obj):
    if isinstance(obj, dict):
        return {str(k): make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    else:
        return obj


# --------------------------------------------------
# 🔥 TRAJECTORY (UPGRADED)
# --------------------------------------------------

def generate_trajectory(params):
    t = np.linspace(0, 20, 2000)

    orbit = params.get("orbit", 0.2)
    helix = params.get("helix", 0.2)

    # Basis Spiral
    r = 1 + orbit * t
    x = r * np.cos(t)
    y = r * np.sin(t)

    # Helix Modulation (jet-like)
    x += helix * np.cos(3 * t)
    y += helix * np.sin(2 * t)

    return np.stack([x, y], axis=1)


# --------------------------------------------------
# 🔥 ROTATION DETECTION
# --------------------------------------------------

def compute_rotation(trajectory):
    """
    Estimate global rotation direction and strength
    """

    dx = np.diff(trajectory[:, 0])
    dy = np.diff(trajectory[:, 1])

    cross = trajectory[:-1, 0] * dy - trajectory[:-1, 1] * dx

    rotation_value = np.mean(cross)

    if rotation_value > 0:
        rotation = "CCW"
    elif rotation_value < 0:
        rotation = "CW"
    else:
        rotation = "NONE"

    strength = float(np.abs(rotation_value))

    return rotation, strength


# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_topology(trajectory, loops, channels, nodes, save_path=None):
    plt.figure(figsize=(8, 8))

    plt.plot(trajectory[:, 0], trajectory[:, 1], alpha=0.2)

    if loops is not None:
        _, points, labels = loops
        if points is not None and labels is not None:
            for label in set(labels):
                if label == -1:
                    continue
                cluster = points[labels == label]
                plt.scatter(cluster[:, 0], cluster[:, 1], s=20)

    if nodes is not None:
        plt.scatter(nodes[:, 0], nodes[:, 1], c='red', s=50)

    plt.title("Topology Detection")
    plt.axis("equal")

    if save_path:
        plt.savefig(save_path, dpi=150)
    else:
        plt.show()


# --------------------------------------------------
# CORE PIPELINE
# --------------------------------------------------

def run_pipeline(params, run_id="run_001", visualize=True):

    print("\n--- RUNNING PIPELINE ---")
    print("Params:", params)

    trajectory = generate_trajectory(params)

    # 🔥 ANGLE ANALYSIS
    angle_data = analyze_angle_distribution(trajectory)

    # 🔥 ROTATION
    rotation, rotation_strength = compute_rotation(trajectory)

    # 🔥 TOPOLOGY
    loops = detect_loops(trajectory)

    if loops is not None:
        recurrences, loop_points, loop_labels = loops
        channels = extract_channels(trajectory, loop_points, loop_labels)
    else:
        channels = []

    nodes = find_transition_nodes(trajectory)

    graph = build_topology_from_components(loops, channels, nodes)

    metrics = compute_topology_metrics(graph)
    signature = compute_topology_signature(metrics)
    classification = classify_topology(signature)

    print("\n--- RESULT ---")
    print("Classification:", classification)
    print("Rotation:", rotation, "| Strength:", round(rotation_strength, 6))

    json_path = os.path.join(JSON_DIR, f"{run_id}.json")
    visual_path = os.path.join(VISUAL_DIR, f"{run_id}.png")

    result = {
        "params": params,
        "classification": classification,
        "signature": signature,
        "metrics": metrics,
        "angle_data": angle_data,
        "rotation": rotation,
        "rotation_strength": rotation_strength
    }

    safe_result = make_json_safe(result)

    with open(json_path, "w") as f:
        json.dump(safe_result, f, indent=4)

    if visualize:
        plot_topology(trajectory, loops, channels, nodes, save_path=visual_path)

    print("\nSaved:")
    print("JSON:", json_path)
    print("IMG :", visual_path)

    return result


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    params = {
        "orbit": 0.3,
        "helix": 0.2
    }

    run_pipeline(params, run_id="test_run")
