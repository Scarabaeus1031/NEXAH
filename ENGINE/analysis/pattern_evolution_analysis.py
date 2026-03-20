import numpy as np
import matplotlib.pyplot as plt
import os

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape
from ENGINE.analysis.pattern_analysis import analyze_field

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 50
STEPS = 60
N_AGENTS = 200

SAVE_DIR = "ENGINE/visuals/evolution"
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
# AGENT STEP
# --------------------------------------------------

def step_agent(pos, landscape):
    neighbors = get_neighbors(pos)

    vals = [landscape[nx, ny] for nx, ny in neighbors]
    best_idx = np.argmax(vals)

    if np.random.rand() < 0.2:
        return neighbors[np.random.randint(len(neighbors))]
    else:
        return neighbors[best_idx]

# --------------------------------------------------
# EVOLUTION SIMULATION
# --------------------------------------------------

def run_evolution():
    landscape = generate_stability_landscape()

    agents = [
        (np.random.randint(0, SIZE), np.random.randint(0, SIZE))
        for _ in range(N_AGENTS)
    ]

    visit_history = []
    metrics_history = []

    visit_map = np.zeros((SIZE, SIZE))

    for t in range(STEPS):

        # reset per frame
        frame_map = np.zeros((SIZE, SIZE))

        new_agents = []

        for pos in agents:
            new_pos = step_agent(pos, landscape)
            new_agents.append(new_pos)

            x, y = new_pos
            frame_map[x, y] += 1
            visit_map[x, y] += 1

        agents = new_agents

        # store maps
        visit_history.append(frame_map.copy())

        # analyze current frame
        metrics = analyze_field(frame_map)
        metrics["time"] = t

        metrics_history.append(metrics)

    return landscape, visit_history, visit_map, metrics_history

# --------------------------------------------------
# PLOT METRICS OVER TIME
# --------------------------------------------------

def plot_metrics(metrics_history):

    times = [m["time"] for m in metrics_history]
    pairs = [m["pairs"] for m in metrics_history]
    hotspots = [m["hotspots"] for m in metrics_history]

    plt.figure(figsize=(10,5))

    plt.plot(times, pairs, label="Pairs (structure)")
    plt.plot(times, hotspots, label="Hotspots")

    plt.xlabel("Time")
    plt.ylabel("Metric Value")
    plt.title("Pattern Evolution Over Time")
    plt.legend()

    path = os.path.join(SAVE_DIR, "pattern_evolution_metrics.png")
    plt.savefig(path, dpi=200)

    print(f"\nSaved → {path}")
    plt.show()

# --------------------------------------------------
# VISUAL SNAPSHOTS
# --------------------------------------------------

def save_snapshots(visit_history):

    key_frames = [0, len(visit_history)//2, len(visit_history)-1]

    fig, axs = plt.subplots(1, 3, figsize=(12,4))

    for i, t in enumerate(key_frames):
        axs[i].imshow(visit_history[t], origin="lower")
        axs[i].set_title(f"t = {t}")
        axs[i].axis("off")

    plt.tight_layout()

    path = os.path.join(SAVE_DIR, "pattern_evolution_snapshots.png")
    plt.savefig(path, dpi=200)

    print(f"Saved → {path}")
    plt.show()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    landscape, visit_history, visit_map, metrics_history = run_evolution()

    save_snapshots(visit_history)
    plot_metrics(metrics_history)
