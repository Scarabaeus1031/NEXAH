import numpy as np
import matplotlib.pyplot as plt
import os

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape
from ENGINE.analysis.pattern_analysis import analyze_field, compare_with_random

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

N_RUNS = 2000
STEPS = 60
SIZE = 50

SAVE_DIR = "ENGINE/visuals/monte_carlo"
os.makedirs(SAVE_DIR, exist_ok=True)

# --------------------------------------------------
# MOVES (8-direction = weniger Artefakte)
# --------------------------------------------------

MOVES = [(-1,0),(1,0),(0,-1),(0,1),
         (-1,-1),(-1,1),(1,-1),(1,1)]

def get_neighbors(pos):
    x, y = pos
    neighbors = []

    for dx, dy in MOVES:
        nx = (x + dx) % SIZE   # periodic boundary!
        ny = (y + dy) % SIZE
        neighbors.append((nx, ny))

    return neighbors

# --------------------------------------------------
# AGENT
# --------------------------------------------------

def run_agent(landscape):
    pos = (np.random.randint(0, SIZE), np.random.randint(0, SIZE))
    path = [pos]

    for _ in range(STEPS):
        neighbors = get_neighbors(pos)

        # greedy climb with noise
        vals = [landscape[nx, ny] for nx, ny in neighbors]
        best_idx = np.argmax(vals)

        if np.random.rand() < 0.2:
            pos = neighbors[np.random.randint(len(neighbors))]
        else:
            pos = neighbors[best_idx]

        path.append(pos)

    return path

# --------------------------------------------------
# MONTE CARLO
# --------------------------------------------------

def run_monte_carlo():
    landscape = generate_stability_landscape()

    visit_map = np.zeros((SIZE, SIZE))
    endpoint_map = np.zeros((SIZE, SIZE))

    for _ in range(N_RUNS):
        path = run_agent(landscape)

        for x, y in path:
            visit_map[x, y] += 1

        ex, ey = path[-1]
        endpoint_map[ex, ey] += 1

    return landscape, visit_map, endpoint_map

# --------------------------------------------------
# PLOT + SAVE
# --------------------------------------------------

def plot_and_save(landscape, visit_map, endpoint_map):
    diff_map = visit_map - endpoint_map

    fig, axs = plt.subplots(1, 3, figsize=(15,5))

    axs[0].imshow(visit_map, origin="lower")
    axs[0].set_title("Visit Density")

    axs[1].imshow(endpoint_map, origin="lower")
    axs[1].set_title("Endpoint Density")

    axs[2].imshow(diff_map, origin="lower")
    axs[2].set_title("Flow Map (Visit - Endpoint)")

    for ax in axs:
        ax.axis("off")

    plt.tight_layout()

    # save
    path = os.path.join(SAVE_DIR, "monte_carlo_analysis.png")
    plt.savefig(path, dpi=200)

    print(f"\nSaved → {path}")
    plt.show()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    landscape, visit_map, endpoint_map = run_monte_carlo()
    plot_and_save(landscape, visit_map, endpoint_map)

    # --------------------------------------------------
    # PATTERN ANALYSIS
    # --------------------------------------------------

    print("\n--- PATTERN ANALYSIS ---")

    results = analyze_field(visit_map)

    for k, v in results.items():
        print(k, ":", v)

    # --------------------------------------------------
    # RANDOM COMPARISON
    # --------------------------------------------------

    print("\n--- COMPARISON WITH RANDOM ---")

    comparison = compare_with_random(visit_map)

    print("\nREAL:")
    for k, v in comparison["real"].items():
        print(k, ":", v)

    print("\nRANDOM:")
    for k, v in comparison["random"].items():
        print(k, ":", v)
