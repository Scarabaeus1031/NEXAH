import numpy as np
import matplotlib.pyplot as plt
import os

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 50
N_AGENTS = 250
STEPS = 200

NOISE = 0.1
CONTROL_STRENGTH = 0.3

PHASE_SPEED = 0.08   # wie schnell Phase rotiert
SAVE_DIR = "ENGINE/visuals/resonance_steering"
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
# PHASE-DRIVEN TARGET SELECTION
# --------------------------------------------------

def get_phase_target(attractors, phase):
    # sinusoidal weighting → smooth switching
    weights = np.array([
        np.sin(phase),
        np.sin(phase + 2*np.pi/3),
        np.sin(phase + 4*np.pi/3)
    ])

    idx = np.argmax(weights)
    return attractors[idx]

# --------------------------------------------------
# CONTROLLED AGENT WITH PHASE
# --------------------------------------------------

def run_agent(landscape, attractors):

    pos = (np.random.randint(0, SIZE), np.random.randint(0, SIZE))
    path = [pos]

    phase = np.random.rand() * 2*np.pi

    for t in range(STEPS):

        # phase evolves
        phase += PHASE_SPEED

        target = get_phase_target(attractors, phase)

        neighbors = get_neighbors(pos)
        vals = np.array([landscape[nx, ny] for nx, ny in neighbors])

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
# RUN SIMULATION
# --------------------------------------------------

def run_simulation():

    landscape = generate_stability_landscape()
    attractors = find_top_attractors(landscape, 3)

    paths = []

    for _ in range(N_AGENTS):
        path = run_agent(landscape, attractors)
        paths.append(path)

    return landscape, attractors, paths

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_results(landscape, attractors, paths):

    plt.figure(figsize=(6,6))
    plt.imshow(landscape, origin="lower", alpha=0.7)

    # trajectories
    for path in paths[:100]:
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        plt.plot(xs, ys, alpha=0.15)

    # attractors
    for i, (x,y) in enumerate(attractors):
        plt.scatter(x, y, s=120, label=f"A{i}")

    plt.title("Resonance Steering Flow (Level 7)")
    plt.legend()
    plt.axis("off")

    path = os.path.join(SAVE_DIR, "resonance_steering.png")
    plt.savefig(path, dpi=200)
    print(f"\nSaved → {path}")

    plt.show()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    landscape, attractors, paths = run_simulation()
    plot_results(landscape, attractors, paths)
