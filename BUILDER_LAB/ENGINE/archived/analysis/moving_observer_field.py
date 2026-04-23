import numpy as np
import matplotlib.pyplot as plt
import os

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 50
N_AGENTS = 180
STEPS = 180

NOISE = 0.10
FIELD_FEEDBACK = 0.010
FIELD_DECAY = 0.997

OBSERVER_SPEED = 0.12
OBSERVER_RADIUS = 8.0

SAVE_DIR = "ENGINE/visuals/moving_observer_field"
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
# OBSERVER DYNAMICS
# --------------------------------------------------

def observer_position(t, center=(SIZE//2, SIZE//2), radius=OBSERVER_RADIUS, speed=OBSERVER_SPEED):
    cx, cy = center
    x = cx + radius * np.cos(speed * t)
    y = cy + radius * np.sin(speed * t)
    return np.array([x, y])

# --------------------------------------------------
# SHIFT FIELD RELATIVE TO X
# --------------------------------------------------

def shift_landscape(landscape, X):
    sx = int(round(X[0] - SIZE//2))
    sy = int(round(X[1] - SIZE//2))
    shifted = np.roll(landscape, shift=(-sx, -sy), axis=0)
    shifted = np.roll(shifted, shift=(-sy), axis=1)
    return shifted

# --------------------------------------------------
# FEEDBACK
# --------------------------------------------------

def apply_feedback(field, pos, amount=FIELD_FEEDBACK):
    x, y = pos
    field[x, y] += amount

    for nx, ny in get_neighbors(pos):
        field[nx, ny] += amount * 0.35

# --------------------------------------------------
# AGENT STEP ON SHIFTED FIELD
# --------------------------------------------------

def step_agent(pos, shifted_field):
    neighbors = get_neighbors(pos)
    vals = np.array([shifted_field[nx, ny] for nx, ny in neighbors])

    if np.random.rand() < NOISE:
        return neighbors[np.random.randint(len(neighbors))]
    else:
        return neighbors[np.argmax(vals)]

# --------------------------------------------------
# MAIN SIMULATION
# --------------------------------------------------

def run_simulation():
    base_field = generate_stability_landscape()
    dynamic_field = base_field.copy()

    agents = [
        (np.random.randint(0, SIZE), np.random.randint(0, SIZE))
        for _ in range(N_AGENTS)
    ]

    trajectories = [[] for _ in range(N_AGENTS)]
    observer_history = []
    com_history = []
    snapshots = []

    for t in range(STEPS):
        X = observer_position(t)
        observer_history.append(X.copy())

        shifted_field = shift_landscape(dynamic_field, X)

        new_agents = []

        for i, pos in enumerate(agents):
            new_pos = step_agent(pos, shifted_field)
            new_agents.append(new_pos)
            trajectories[i].append(new_pos)

            apply_feedback(dynamic_field, new_pos)

        agents = new_agents

        dynamic_field *= FIELD_DECAY

        xs = [p[0] for p in agents]
        ys = [p[1] for p in agents]
        com_history.append((np.mean(xs), np.mean(ys)))

        if t in [0, STEPS//3, 2*STEPS//3, STEPS-1]:
            snapshots.append((t, dynamic_field.copy(), shifted_field.copy(), X.copy()))

    return base_field, dynamic_field, trajectories, observer_history, com_history, snapshots

# --------------------------------------------------
# PLOTS
# --------------------------------------------------

def plot_overview(base_field, final_field):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    axs[0].imshow(base_field, origin="lower", cmap="viridis")
    axs[0].set_title("Base Field")
    axs[0].axis("off")

    axs[1].imshow(final_field, origin="lower", cmap="viridis")
    axs[1].set_title("Final Dynamic Field")
    axs[1].axis("off")

    plt.tight_layout()
    out_path = os.path.join(SAVE_DIR, "moving_observer_overview.png")
    plt.savefig(out_path, dpi=220)
    print(f"Saved → {out_path}")
    plt.show()

def plot_paths(final_field, trajectories, observer_history, com_history):
    plt.figure(figsize=(7, 7))
    plt.imshow(final_field, origin="lower", cmap="gray", alpha=0.75)

    for path in trajectories[:70]:
        xs = [p[1] for p in path]
        ys = [p[0] for p in path]
        plt.plot(xs, ys, alpha=0.15, linewidth=1)

    ox = [p[1] for p in observer_history]
    oy = [p[0] for p in observer_history]
    plt.plot(ox, oy, color="red", linewidth=2.2, label="observer X")

    cx = [p[1] for p in com_history]
    cy = [p[0] for p in com_history]
    plt.plot(cx, cy, color="cyan", linewidth=2.0, label="center of mass")

    plt.scatter(ox[0], oy[0], c="yellow", s=80, label="X start")
    plt.scatter(ox[-1], oy[-1], c="orange", s=80, label="X end")

    plt.title("Moving Observer Field")
    plt.axis("off")
    plt.legend(loc="upper right")

    out_path = os.path.join(SAVE_DIR, "moving_observer_paths.png")
    plt.savefig(out_path, dpi=220)
    print(f"Saved → {out_path}")
    plt.show()

def plot_snapshots(snapshots):
    fig, axs = plt.subplots(len(snapshots), 2, figsize=(10, 4 * len(snapshots)))

    if len(snapshots) == 1:
        axs = np.array([axs])

    for row, (t, dynamic_field, shifted_field, X) in enumerate(snapshots):
        axs[row, 0].imshow(dynamic_field, origin="lower", cmap="viridis")
        axs[row, 0].scatter(X[1], X[0], c="white", s=60, marker="x")
        axs[row, 0].set_title(f"Dynamic Field t={t}")
        axs[row, 0].axis("off")

        axs[row, 1].imshow(shifted_field, origin="lower", cmap="viridis")
        axs[row, 1].set_title(f"Field Relative to X (t={t})")
        axs[row, 1].axis("off")

    plt.tight_layout()
    out_path = os.path.join(SAVE_DIR, "moving_observer_snapshots.png")
    plt.savefig(out_path, dpi=220)
    print(f"Saved → {out_path}")
    plt.show()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    print("\n🚀 LEVEL 9 – MOVING OBSERVER FIELD\n")

    base_field, final_field, trajectories, observer_history, com_history, snapshots = run_simulation()

    plot_overview(base_field, final_field)
    plot_paths(final_field, trajectories, observer_history, com_history)
    plot_snapshots(snapshots)
