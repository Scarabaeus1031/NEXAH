import numpy as np
import matplotlib.pyplot as plt
import os

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 50
N_AGENTS = 250
STEPS = 180
NOISE = 0.12
CONTROL_STRENGTH = 0.28
SWITCH_PERIOD = 30   # alle N Schritte Zielwechsel

SAVE_DIR = "ENGINE/visuals/resonance_switching"
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

        if all(np.hypot(x - cx, y - cy) > 4 for cx, cy in coords):
            coords.append((x, y))

        if len(coords) >= n:
            break

    return coords

# --------------------------------------------------
# CONTROL STEP
# --------------------------------------------------

def controlled_step(pos, landscape, target):
    neighbors = get_neighbors(pos)

    vals = np.array([landscape[nx, ny] for nx, ny in neighbors])

    tx, ty = target

    scores = []

    for (nx, ny), val in zip(neighbors, vals):
        # directional pull
        dist_now = np.linalg.norm(np.array(pos) - np.array(target))
        dist_next = np.linalg.norm(np.array((nx, ny)) - np.array(target))

        directional = dist_now - dist_next

        score = val + CONTROL_STRENGTH * directional
        scores.append(score)

    if np.random.rand() < NOISE:
        return neighbors[np.random.randint(len(neighbors))]
    else:
        return neighbors[np.argmax(scores)]

# --------------------------------------------------
# RESONANCE SWITCHING AGENT
# --------------------------------------------------

def run_resonance_agent(landscape, attractors):
    pos = (np.random.randint(0, SIZE), np.random.randint(0, SIZE))
    path = [pos]

    for t in range(STEPS):

        # Phase-based switching
        phase = (t // SWITCH_PERIOD) % len(attractors)
        target = attractors[phase]

        pos = controlled_step(pos, landscape, target)
        path.append(pos)

    return path

# --------------------------------------------------
# RUN SIMULATION
# --------------------------------------------------

def run_simulation():
    landscape = generate_stability_landscape()

    attractors = find_top_attractors(landscape, n=3)

    if len(attractors) < 2:
        print("Not enough attractors found.")
        return landscape, attractors, []

    all_paths = []

    for _ in range(N_AGENTS):
        path = run_resonance_agent(landscape, attractors)
        all_paths.append(path)

    return landscape, attractors, all_paths

# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_results(landscape, attractors, paths):

    plt.figure(figsize=(7,7))
    plt.imshow(landscape, origin="lower", alpha=0.6)

    # draw paths
    for path in paths[:120]:
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        plt.plot(xs, ys, alpha=0.15)

    # attractors
    colors = ["red", "lime", "cyan"]

    for i, (x,y) in enumerate(attractors):
        plt.scatter(x, y, s=200, marker="*", color=colors[i % len(colors)], label=f"A{i}")

    plt.title("Resonance Switching Flow (Level 6)")
    plt.legend()
    plt.axis("off")

    path = os.path.join(SAVE_DIR, "resonance_switching.png")
    plt.savefig(path, dpi=220)

    print(f"\nSaved → {path}")

    plt.show()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    print("\n🚀 LEVEL 6 – RESONANCE SWITCHING\n")

    landscape, attractors, paths = run_simulation()

    if len(paths) > 0:
        plot_results(landscape, attractors, paths)
