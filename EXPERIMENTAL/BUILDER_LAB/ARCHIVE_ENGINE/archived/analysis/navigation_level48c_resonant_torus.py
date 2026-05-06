# ENGINE/analysis/navigation_level48c_resonant_torus.py

import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter, label, center_of_mass

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 80
SMOOTH_SIGMA = 1.2

NODE_THRESHOLD = 0.985
MIN_CLUSTER_SIZE = 3

TORUS_RADIUS = 12
TORUS_THICKNESS = 4

ENABLE_DRIFT = True   # kleiner Vorgeschmack auf Level 49


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def detect_nodes(score_map):
    threshold = np.quantile(score_map, NODE_THRESHOLD)
    mask = score_map > threshold

    labeled, num = label(mask)

    nodes = []
    for i in range(1, num + 1):
        region = (labeled == i)
        if np.sum(region) < MIN_CLUSTER_SIZE:
            continue

        cy, cx = center_of_mass(region)
        nodes.append((cx, cy))

    return nodes


# --------------------------------------------------
# TORUS BUILD
# --------------------------------------------------

def build_resonant_torus(nodes, size):

    lattice = np.zeros((size, size))

    if len(nodes) < 2:
        return lattice

    nodes = np.array(nodes)

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):

            x1, y1 = nodes[i]
            x2, y2 = nodes[j]

            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2

            dx = x2 - x1
            dy = y2 - y1
            dist = np.sqrt(dx**2 + dy**2)

            if dist < 5:
                continue

            # orthogonale Richtung
            nx = -dy
            ny = dx
            norm = np.sqrt(nx**2 + ny**2) + 1e-6
            nx /= norm
            ny /= norm

            for t in np.linspace(0, 2*np.pi, 160):

                # --- DRIFT (wichtig für dein Persistenz-Prinzip)
                drift = 0.0
                if ENABLE_DRIFT:
                    drift = 0.6 * np.sin(3 * t)

                r = TORUS_RADIUS + TORUS_THICKNESS * np.cos(2 * t)

                px = cx + (r + drift) * np.cos(t) + nx * 2 * np.sin(t)
                py = cy + (r + drift) * np.sin(t) + ny * 2 * np.sin(t)

                ix = int(np.clip(px, 0, size - 1))
                iy = int(np.clip(py, 0, size - 1))

                lattice[iy, ix] += 1.0

    lattice = gaussian_filter(lattice, sigma=1.5)

    max_val = np.max(lattice)
    if max_val > 0:
        lattice /= max_val

    return lattice


# --------------------------------------------------
# MIRROR FIELD (4774)
# --------------------------------------------------

def build_mirror_field(nodes, size):

    field = np.zeros((size, size))

    for (x, y) in nodes:
        mx = size - 1 - x  # Spiegelachse

        ix1, iy1 = int(x), int(y)
        ix2, iy2 = int(mx), int(y)

        field[iy1, ix1] += 1.0
        field[iy2, ix2] += 1.0

    field = gaussian_filter(field, sigma=1.0)

    max_val = np.max(field)
    if max_val > 0:
        field /= max_val

    return field


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def run():

    field = generate_stability_landscape(size=SIZE)

    # Gradient + Struktur
    gx, gy = np.gradient(field)
    grad = np.sqrt(gx**2 + gy**2)

    smooth = gaussian_filter(field, sigma=SMOOTH_SIGMA)

    node_score = grad * smooth

    # --------------------------------------------------
    # NODES
    # --------------------------------------------------

    nodes = detect_nodes(node_score)

    # --------------------------------------------------
    # STRUCTURES
    # --------------------------------------------------

    torus = build_resonant_torus(nodes, SIZE)
    mirror = build_mirror_field(nodes, SIZE)

    combined = 0.75 * torus + 0.25 * mirror

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    result = {
        "num_nodes": len(nodes),
        "nodes": [{"x": float(x), "y": float(y)} for (x, y) in nodes]
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    out_dir = "ENGINE/analysis/output_level48c"
    os.makedirs(out_dir, exist_ok=True)

    with open(f"{out_dir}/nodes_{ts}.json", "w") as f:
        json.dump(result, f, indent=2)

    # --------------------------------------------------
    # VISUAL
    # --------------------------------------------------

    fig, axs = plt.subplots(2, 2, figsize=(10, 10))

    axs[0, 0].imshow(field)
    axs[0, 0].set_title("Field")

    axs[0, 1].imshow(node_score)
    axs[0, 1].set_title("Node Score")

    node_map = np.zeros_like(field)
    for (x, y) in nodes:
        node_map[int(y), int(x)] = 1

    axs[1, 0].imshow(node_map)
    axs[1, 0].set_title("Detected Nodes")

    axs[1, 1].imshow(combined)
    axs[1, 1].set_title("Resonant Torus (Drifted)")

    plt.tight_layout()
    plt.savefig(f"{out_dir}/torus_{ts}.png")
    plt.close()

    print("Nodes:", nodes)


if __name__ == "__main__":
    run()
