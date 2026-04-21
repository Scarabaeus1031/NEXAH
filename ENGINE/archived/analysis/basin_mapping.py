import numpy as np
import matplotlib.pyplot as plt
import os

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 50
STEPS = 80

SAVE_DIR = "ENGINE/visuals/basin_mapping"
os.makedirs(SAVE_DIR, exist_ok=True)

# --------------------------------------------------
# MOVES
# --------------------------------------------------

MOVES = [(-1,0),(1,0),(0,-1),(0,1),
         (-1,-1),(-1,1),(1,-1),(1,1)]

def get_neighbors(pos):
    x, y = pos
    neighbors = []

    for dx, dy in MOVES:
        nx = (x + dx) % SIZE
        ny = (y + dy) % SIZE
        neighbors.append((nx, ny))

    return neighbors

# --------------------------------------------------
# DETERMINISTIC AGENT (NO NOISE!)
# --------------------------------------------------

def run_to_attractor(start, landscape):
    pos = start

    for _ in range(STEPS):
        neighbors = get_neighbors(pos)

        vals = [landscape[nx, ny] for nx, ny in neighbors]
        best_idx = np.argmax(vals)

        pos = neighbors[best_idx]

    return pos  # final attractor

# --------------------------------------------------
# CLUSTER ATTRACTORS
# --------------------------------------------------

def cluster_attractors(endpoints, threshold=2):
    clusters = []
    labels = {}

    for idx, p in enumerate(endpoints):
        assigned = False

        for cid, c in enumerate(clusters):
            cx, cy = c

            if np.linalg.norm(np.array(p) - np.array((cx, cy))) < threshold:
                labels[idx] = cid
                assigned = True
                break

        if not assigned:
            clusters.append(p)
            labels[idx] = len(clusters) - 1

    return clusters, labels

# --------------------------------------------------
# BASIN MAPPING
# --------------------------------------------------

def compute_basin_map(landscape):
    endpoints = []
    positions = []

    for x in range(SIZE):
        for y in range(SIZE):
            final = run_to_attractor((x, y), landscape)
            endpoints.append(final)
            positions.append((x, y))

    clusters, labels = cluster_attractors(endpoints)

    basin_map = np.zeros((SIZE, SIZE))

    for i, (x, y) in enumerate(positions):
        basin_map[x, y] = labels[i]

    return basin_map, clusters

# --------------------------------------------------
# SEPARATRIX DETECTION
# --------------------------------------------------

def compute_separatrix(basin_map):
    sep = np.zeros_like(basin_map)

    for x in range(SIZE):
        for y in range(SIZE):
            current = basin_map[x, y]

            neighbors = get_neighbors((x, y))

            for nx, ny in neighbors:
                if basin_map[nx, ny] != current:
                    sep[x, y] = 1
                    break

    return sep

# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_all(landscape, basin_map, separatrix, clusters):

    fig, axs = plt.subplots(1, 3, figsize=(18,6))

    # 1) landscape
    axs[0].imshow(landscape, origin="lower")
    axs[0].set_title("Stability Landscape")
    axs[0].axis("off")

    # 2) basin map
    im = axs[1].imshow(basin_map, origin="lower", cmap="tab10")
    axs[1].set_title("Attractor Basins")
    axs[1].axis("off")

    # plot attractors
    for i, (x, y) in enumerate(clusters):
        axs[1].scatter(y, x, c="white", s=80)
        axs[1].text(y, x, str(i), color="black")

    # 3) separatrix
    axs[2].imshow(separatrix, origin="lower", cmap="gray")
    axs[2].set_title("Separatrix (Flip Boundaries)")
    axs[2].axis("off")

    plt.tight_layout()

    path = os.path.join(SAVE_DIR, "basin_mapping.png")
    plt.savefig(path, dpi=200)

    print(f"\nSaved → {path}")
    plt.show()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    print("\n🚀 LEVEL 4 – BASIN MAPPING\n")

    landscape = generate_stability_landscape()

    basin_map, clusters = compute_basin_map(landscape)
    separatrix = compute_separatrix(basin_map)

    plot_all(landscape, basin_map, separatrix, clusters)
