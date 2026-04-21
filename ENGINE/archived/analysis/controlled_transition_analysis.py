import numpy as np
import matplotlib.pyplot as plt
import os

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 50
STEPS = 120
CONTROL_STRENGTH = 0.35   # wie stark wir "ziehen"
NOISE = 0.15              # Rest-Zufall

SAVE_DIR = "ENGINE/visuals/controlled_transition"
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
# FIND ATTRACTORS (simple peak detection)
# --------------------------------------------------

def find_top_attractors(landscape, n=3):
    flat_idx = np.argsort(landscape.flatten())[::-1]
    coords = []

    for idx in flat_idx:
        x = idx // SIZE
        y = idx % SIZE

        # avoid duplicates (distance filter)
        if all(np.hypot(x - cx, y - cy) > 4 for cx, cy in coords):
            coords.append((x, y))
        if len(coords) >= n:
            break

    return coords

# --------------------------------------------------
# CONTROLLED AGENT
# --------------------------------------------------

def run_controlled_agent(landscape, target):
    pos = (np.random.randint(0, SIZE), np.random.randint(0, SIZE))
    path = [pos]

    for _ in range(STEPS):
        neighbors = get_neighbors(pos)

        # gradient term (normal climbing)
        vals = np.array([landscape[nx, ny] for nx, ny in neighbors])

        # direction to target
        tx, ty = target
        dir_vecs = np.array([
            [(nx - pos[0]), (ny - pos[1])] for nx, ny in neighbors
        ])

        target_vec = np.array([tx - pos[0], ty - pos[1]])

        # normalize
        norms = np.linalg.norm(dir_vecs, axis=1) + 1e-6
        dir_vecs = dir_vecs / norms[:, None]

        target_norm = np.linalg.norm(target_vec) + 1e-6
        target_vec = target_vec / target_norm

        # alignment score
        alignment = dir_vecs @ target_vec

        # combined score
        score = vals + CONTROL_STRENGTH * alignment

        if np.random.rand() < NOISE:
            pos = neighbors[np.random.randint(len(neighbors))]
        else:
            pos = neighbors[np.argmax(score)]

        path.append(pos)

    return path

# --------------------------------------------------
# RUN SIMULATION
# --------------------------------------------------

def run_simulation():
    landscape = generate_stability_landscape()

    attractors = find_top_attractors(landscape, n=3)
    target = attractors[0]   # strongest peak

    all_paths = []

    for _ in range(300):
        path = run_controlled_agent(landscape, target)
        all_paths.append(path)

    return landscape, attractors, target, all_paths

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_results(landscape, attractors, target, paths):

    plt.figure(figsize=(6,6))
    plt.imshow(landscape, origin="lower", alpha=0.7)

    # draw trajectories
    for path in paths[:80]:
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        plt.plot(xs, ys, alpha=0.2)

    # mark attractors
    for i, (x,y) in enumerate(attractors):
        plt.scatter(x, y, s=120, label=f"A{i}")

    # highlight target
    tx, ty = target
    plt.scatter(tx, ty, s=200, marker="*", color="red", label="TARGET")

    plt.title("Controlled Transition Flow")
    plt.legend()
    plt.axis("off")

    path = os.path.join(SAVE_DIR, "controlled_transition.png")
    plt.savefig(path, dpi=200)
    print(f"\nSaved → {path}")

    plt.show()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    landscape, attractors, target, paths = run_simulation()
    plot_results(landscape, attractors, target, paths)
