# ============================================================
# NEXAH — Gate Graph Builder (Halvorsen System)
# ============================================================
#
# Purpose:
# Build a directed gate graph from detected Halvorsen gates.
#
# Pipeline:
# coarse matrix → gate detection → directed graph → graph plot
#
# Outputs:
# - gate_graph_*.txt
# - gate_graph_*.png
#
# ============================================================

import os
import glob
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# LOAD LATEST COARSE MATRIX
# ============================================================

def load_latest_matrix():
    files = sorted(glob.glob(
        "APPLICATIONS/dynamical_systems/halvorsen/outputs/coarse_matrix_*.npy"
    ))

    if not files:
        raise RuntimeError("No coarse_matrix_*.npy found. Run coarse_grain_halvorsen.py first.")

    latest = files[-1]
    print(f"→ loading matrix: {latest}")

    matrix = np.load(latest)
    print(f"matrix shape: {matrix.shape}")

    return matrix, latest


# ============================================================
# GATE DETECTION
# ============================================================

def detect_gates(matrix, alpha=0.2):
    gates = []
    n = matrix.shape[0]

    for i in range(n):
        diag = matrix[i, i]

        for j in range(n):
            if i == j:
                continue

            p = matrix[i, j]

            if diag > 0:
                rel = p / diag
                if rel > alpha:
                    gates.append({
                        "from": i,
                        "to": j,
                        "p": float(p),
                        "rel": float(rel)
                    })

    return gates


# ============================================================
# BUILD GRAPH OBJECT
# ============================================================

def build_gate_graph(matrix, gates):
    nodes = list(range(matrix.shape[0]))

    graph = {
        "nodes": nodes,
        "edges": gates
    }

    return graph


# ============================================================
# SAVE GRAPH TXT
# ============================================================

def save_graph_txt(graph, source_matrix, base_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_path = f"{base_path}/gate_graph_{timestamp}.txt"

    with open(txt_path, "w") as f:
        f.write("NEXAH — Halvorsen Gate Graph\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"Source matrix: {source_matrix}\n\n")

        f.write("NODES\n")
        f.write("-" * 50 + "\n")
        for node in graph["nodes"]:
            f.write(f"Cluster {node}\n")

        f.write("\nEDGES / GATES\n")
        f.write("-" * 50 + "\n")
        for edge in graph["edges"]:
            f.write(
                f"{edge['from']} -> {edge['to']} "
                f"| p={edge['p']:.4f} "
                f"| rel={edge['rel']:.3f}\n"
            )

    print(f"[✓] Gate graph TXT saved: {txt_path}")
    return txt_path


# ============================================================
# PLOT GATE GRAPH
# ============================================================

def plot_gate_graph(graph, base_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    png_path = f"{base_path}/gate_graph_{timestamp}.png"

    nodes = graph["nodes"]
    edges = graph["edges"]

    n = len(nodes)

    # Simple ordered channel layout:
    # clusters lie along x-axis, small sine curve adds readability.
    x = np.arange(n)
    y = np.sin(np.linspace(0, 2 * np.pi, n)) * 0.25

    fig, ax = plt.subplots(figsize=(11, 4))

    # nodes
    ax.scatter(x, y, s=250, zorder=3)

    for node in nodes:
        ax.text(
            x[node],
            y[node],
            str(node),
            ha="center",
            va="center",
            fontsize=9,
            zorder=4
        )

    # edges
    for edge in edges:
        i = edge["from"]
        j = edge["to"]
        p = edge["p"]

        dx = x[j] - x[i]
        dy = y[j] - y[i]

        ax.arrow(
            x[i],
            y[i],
            dx * 0.85,
            dy * 0.85,
            length_includes_head=True,
            head_width=0.06,
            head_length=0.18,
            linewidth=1.5 + 4 * p,
            alpha=0.75,
            zorder=2
        )

        mid_x = (x[i] + x[j]) / 2
        mid_y = (y[i] + y[j]) / 2

        ax.text(
            mid_x,
            mid_y + 0.10,
            f"{p:.2f}",
            fontsize=8,
            ha="center"
        )

    ax.set_title("NEXAH — Halvorsen Gate Graph")
    ax.set_xlabel("coarse cluster order")
    ax.set_yticks([])
    ax.grid(axis="x", alpha=0.2)

    plt.tight_layout()
    fig.savefig(png_path, dpi=300)
    plt.close(fig)

    print(f"[✓] Gate graph PNG saved: {png_path}")
    return png_path


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    base_path = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    os.makedirs(base_path, exist_ok=True)

    print("→ load coarse matrix")
    matrix, source_matrix = load_latest_matrix()

    print("→ detect gates")
    gates = detect_gates(matrix, alpha=0.2)
    print(f"found gates: {len(gates)}")

    for edge in gates:
        print(
            f"{edge['from']} -> {edge['to']} "
            f"| p={edge['p']:.4f} "
            f"| rel={edge['rel']:.3f}"
        )

    print("→ build graph")
    graph = build_gate_graph(matrix, gates)

    print("→ save graph")
    save_graph_txt(graph, source_matrix, base_path)
    plot_gate_graph(graph, base_path)

    print("✔ DONE")
