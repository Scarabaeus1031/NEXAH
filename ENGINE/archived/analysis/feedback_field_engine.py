import numpy as np
import matplotlib.pyplot as plt
import os

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 50
N_AGENTS = 220
STEPS = 180

NOISE = 0.1
CONTROL_STRENGTH = 0.25

FIELD_UPDATE_STRENGTH = 0.015   # wie stark Agenten das Feld verändern
FIELD_DECAY = 0.995            # Stabilisierung (verhindert Explosion)

SAVE_DIR = "ENGINE/visuals/self_modifying_field"
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
# FIND ATTRACTORS
# --------------------------------------------------

def find_top_attractors(landscape, n=3):
    flat_idx = np.argsort(landscape.flatten())[::-1]
    coords = []

    for idx in flat_idx:
        x = idx // SIZE
        y = idx % SIZE

        if all(np.hypot(x - cx, y - cy) > 5 for cx, cy in coords):
            coords.append((x, y))

        if len(coords) >= n:
            break

    return coords

# --------------------------------------------------
# AGENT WITH FEEDBACK
# --------------------------------------------------

def run_agent(landscape):

    pos = (np.random.randint(0, SIZE), np.random.randint(0, SIZE))
    path = [pos]

    for _ in range(STEPS):

        neighbors = get_neighbors(pos)
        vals = np.array([landscape[nx, ny] for nx, ny in neighbors])

        if np.random.rand() < NOISE:
            pos = neighbors[np.random.randint(len(neighbors))]
        else:
            pos = neighbors[np.argmax(vals)]

        path.append(pos)

        # 🔥 FEEDBACK: Agent verändert Feld
        x, y = pos

        landscape[x, y] += FIELD_UPDATE_STRENGTH

        # kleine Nachbarschaft verstärken (weicher Effekt)
        for nx, ny in get_neighbors(pos):
            landscape[nx, ny] += FIELD_UPDATE_STRENGTH * 0.3

    return path

# --------------------------------------------------
# RUN SIMULATION
# --------------------------------------------------

def run_simulation():

    base_landscape = generate_stability_landscape()
    landscape = base_landscape.copy()

    all_paths = []

    for _ in range(N_AGENTS):
        path = run_agent(landscape)
        all_paths.append(path)

        # Stabilisierung des Felds
        landscape *= FIELD_DECAY

    return base_landscape, landscape, all_paths

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_results(base, modified, paths):

    fig, axs = plt.subplots(1, 2, figsize=(12,5))

    # Original
    axs[0].imshow(base, origin="lower")
    axs[0].set_title("Original Landscape")
    axs[0].axis("off")

    # Modified
    axs[1].imshow(modified, origin="lower")
    axs[1].set_title("Self-Modified Landscape")

    # Trajectories
    for path in paths[:80]:
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        axs[1].plot(xs, ys, alpha=0.15)

    axs[1].axis("off")

    plt.tight_layout()

    path = os.path.join(SAVE_DIR, "self_modifying_field.png")
    plt.savefig(path, dpi=200)
    print(f"\nSaved → {path}")

    plt.show()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    base, modified, paths = run_simulation()
    plot_results(base, modified, paths)
