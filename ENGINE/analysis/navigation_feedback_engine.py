import numpy as np
import matplotlib.pyplot as plt
import os

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 60
N_AGENTS = 200
STEPS = 140

CONTROL_STRENGTH = 0.3
NOISE = 0.15

FEEDBACK_STRENGTH = 0.25   # wie stark Pfade Feld verändern
DECAY = 0.98              # Feld-Gedächtnis

SAVE_DIR = "ENGINE/visuals/navigation_feedback"
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

def find_attractors(field, n=3):
    flat_idx = np.argsort(field.flatten())[::-1]
    coords = []

    for idx in flat_idx:
        x = idx // SIZE
        y = idx % SIZE

        if all(np.hypot(x - cx, y - cy) > 6 for cx, cy in coords):
            coords.append((x, y))

        if len(coords) >= n:
            break

    return coords

# --------------------------------------------------
# AGENT NAVIGATION
# --------------------------------------------------

def run_agent(field, target):
    pos = (np.random.randint(0, SIZE), np.random.randint(0, SIZE))
    path = [pos]

    for _ in range(STEPS):
        neighbors = get_neighbors(pos)

        vals = np.array([field[nx, ny] for nx, ny in neighbors])

        # Richtung zum Ziel
        tx, ty = target
        dir_vecs = np.array([
            [(nx - pos[0]), (ny - pos[1])] for nx, ny in neighbors
        ])

        norms = np.linalg.norm(dir_vecs, axis=1) + 1e-6
        dir_vecs = dir_vecs / norms[:, None]

        target_vec = np.array([tx - pos[0], ty - pos[1]])
        target_vec = target_vec / (np.linalg.norm(target_vec) + 1e-6)

        alignment = dir_vecs @ target_vec

        score = vals + CONTROL_STRENGTH * alignment

        if np.random.rand() < NOISE:
            pos = neighbors[np.random.randint(len(neighbors))]
        else:
            pos = neighbors[np.argmax(score)]

        path.append(pos)

    return path

# --------------------------------------------------
# FIELD RESPONSE (Y)
# --------------------------------------------------

def compute_response(paths):
    response = np.zeros((SIZE, SIZE))

    for path in paths:
        for x, y in path:
            response[x, y] += 1

    # normalize
    response = response / (np.max(response) + 1e-6)

    return response

# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

def run_simulation(iterations=5):

    base_field = generate_stability_landscape()
    field = base_field.copy()

    history_fields = []
    all_paths_total = []

    for it in range(iterations):

        attractors = find_attractors(field, n=3)
        target = attractors[0]

        paths = []

        for _ in range(N_AGENTS):
            p = run_agent(field, target)
            paths.append(p)

        # FIELD RESPONSE
        response = compute_response(paths)

        # UPDATE FIELD
        field = DECAY * field + FEEDBACK_STRENGTH * response

        history_fields.append(field.copy())
        all_paths_total.append(paths)

        print(f"Iteration {it+1} done")

    return base_field, history_fields, all_paths_total, attractors

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_results(base, history, paths_all, attractors):

    # FINAL FIELD
    final_field = history[-1]
    final_paths = paths_all[-1]

    plt.figure(figsize=(10,5))

    plt.subplot(1,2,1)
    plt.title("Base Field")
    plt.imshow(base, origin="lower")
    plt.axis("off")

    plt.subplot(1,2,2)
    plt.title("Learned Navigation Field")
    plt.imshow(final_field, origin="lower")

    # overlay paths
    for path in final_paths[:60]:
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        plt.plot(xs, ys, alpha=0.15)

    for i,(x,y) in enumerate(attractors):
        plt.scatter(x,y,s=120,label=f"A{i}")

    plt.legend()
    plt.axis("off")

    path = os.path.join(SAVE_DIR, "navigation_feedback.png")
    plt.savefig(path, dpi=200)
    print(f"\nSaved → {path}")

    plt.show()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    base, history, paths, attractors = run_simulation(iterations=6)
    plot_results(base, history, paths, attractors)
