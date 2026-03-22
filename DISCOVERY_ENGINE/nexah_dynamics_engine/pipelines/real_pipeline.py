# pipelines/real_pipeline.py

import os
import json
import numpy as np
import matplotlib.pyplot as plt

# --- IMPORTS AUS ANALYSIS ---
from analysis.loop_detector import detect_loops
from analysis.channel_extractor import extract_channels
from analysis.transition_node_finder import find_transition_nodes
from analysis.topology_builder import build_topology_graph
from analysis.topology_metrics import compute_topology_metrics
from analysis.topology_signature import compute_topology_signature
from analysis.topology_classifier import classify_topology


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

OUTPUT_DIR = "outputs"
VISUAL_DIR = os.path.join(OUTPUT_DIR, "visuals", "topology")
JSON_DIR = os.path.join(OUTPUT_DIR, "json")

os.makedirs(VISUAL_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)


# --------------------------------------------------
# TRAJECTORY GENERATOR (TEST / später ersetzen)
# --------------------------------------------------

def generate_trajectory(params):
    t = np.linspace(0, 20, 2000)

    orbit = params.get("orbit", 0.2)
    helix = params.get("helix", 0.2)

    x = np.cos(t) * (1 + orbit * t)
    y = np.sin(t) * (1 + orbit * t)

    # asymmetry / drift
    y += helix * np.sin(2 * t)

    return np.stack([x, y], axis=1)


# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_topology(trajectory, loops, channels, nodes, save_path=None):
    plt.figure(figsize=(8, 8))

    # trajectory
    plt.plot(trajectory[:, 0], trajectory[:, 1], alpha=0.2)

    # loops
    if loops is not None:
        _, points, labels = loops
        if points is not None and labels is not None:
            for label in set(labels):
                if label == -1:
                    continue
                cluster = points[labels == label]
                plt.scatter(cluster[:, 0], cluster[:, 1], s=20)

    # nodes
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

    # 1. generate trajectory
    trajectory = generate_trajectory(params)

    # 2. detect loops
    loops = detect_loops(trajectory)

    # 3. extract channels
    channels = extract_channels(trajectory)

    # 4. detect transition nodes
    nodes = find_transition_nodes(trajectory)

    # 5. build topology graph
    graph = build_topology_graph(loops, channels, nodes)

    # 6. metrics
    metrics = compute_topology_metrics(graph)

    # 7. signature
    signature = compute_topology_signature(metrics)

    # 8. classification
    classification = classify_topology(signature)

    print("\n--- RESULT ---")
    print("Classification:", classification)
    print("Signature:", signature)

    # --------------------------------------------------
    # SAVE OUTPUT
    # --------------------------------------------------

    json_path = os.path.join(JSON_DIR, f"{run_id}.json")
    visual_path = os.path.join(VISUAL_DIR, f"{run_id}.png")

    result = {
        "params": params,
        "classification": classification,
        "signature": signature,
        "metrics": metrics
    }

    with open(json_path, "w") as f:
        json.dump(result, f, indent=4)

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
