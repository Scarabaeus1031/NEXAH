import numpy as np
import matplotlib.pyplot as plt
import os

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 50
N_AGENTS = 200
STEPS = 140

CONTROL_STRENGTH = 0.3
NOISE = 0.15

FEEDBACK_STRENGTH = 0.25
DECAY = 0.98

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
# TORUS DELTA (WICHTIG!)
# --------------------------------------------------

def torus_delta(a, b):
    d = b - a
    if abs(d) > SIZE // 2:
        d -= np.sign(d) * SIZE
    return d

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

        # torus-aware direction
        tx, ty = target
        dir_vecs = np.array([
            [torus_delta(pos[0], nx), torus_delta(pos[1], ny)]
            for nx, ny in neighbors
        ])

        norms = np.linalg.norm(dir_vecs, axis=1) + 1e-6
        dir_vecs = dir_vecs / norms[:, None]

        target_vec = np.array([
            torus_delta(pos[0], tx),
            torus_delta(pos[1], ty)
        ])
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

        paths = []

        for _ in range(N_AGENTS):
            target = attractors[np.random.randint(len(attractors))]
            p = run_agent(field, target)
            paths.append(p)

        response = compute_response(paths)

        # update field
        field = DECAY * field + FEEDBACK_STRENGTH * response

        # normalize (wichtig!)
        field = field / (np.max(field) + 1e-6)

        history_fields.append(field.copy())
        all_paths_total.append(paths)

        print(f"Iteration {it+1} done")

    return base_field, history_fields, all_paths_total, attractors

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_results(base, history, paths_all, attractors):

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

    for path in final_paths[:60]:
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        plt.plot(xs, ys, alpha=0.12)

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
