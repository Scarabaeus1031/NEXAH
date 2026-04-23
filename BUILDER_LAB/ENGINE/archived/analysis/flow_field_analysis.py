import numpy as np
import matplotlib.pyplot as plt
import os

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 50
N_AGENTS = 400
STEPS = 80
TEMPERATURE = 0.2   # noise level

SAVE_DIR = "ENGINE/visuals/flow_field"
os.makedirs(SAVE_DIR, exist_ok=True)

# --------------------------------------------------
# MOVES (8-directional)
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
# AGENT SIMULATION
# --------------------------------------------------

def run_agents(landscape):
    flow_x = np.zeros((SIZE, SIZE))
    flow_y = np.zeros((SIZE, SIZE))

    for _ in range(N_AGENTS):
        pos = (np.random.randint(0, SIZE), np.random.randint(0, SIZE))

        for _ in range(STEPS):
            neighbors = get_neighbors(pos)

            vals = np.array([landscape[nx, ny] for nx, ny in neighbors])
            best_idx = np.argmax(vals)

            # noise (temperature)
            if np.random.rand() < TEMPERATURE:
                next_pos = neighbors[np.random.randint(len(neighbors))]
            else:
                next_pos = neighbors[best_idx]

            # flow vector
            dx = next_pos[0] - pos[0]
            dy = next_pos[1] - pos[1]

            flow_x[pos] += dx
            flow_y[pos] += dy

            pos = next_pos

    return flow_x, flow_y

# --------------------------------------------------
# GRADIENT FIELD (REFERENCE)
# --------------------------------------------------

def compute_gradient(landscape):
    gx, gy = np.gradient(landscape)
    return gx, gy

# --------------------------------------------------
# VORTEX DETECTION (curl)
# --------------------------------------------------

def compute_curl(flow_x, flow_y):
    dFy_dx = np.gradient(flow_y, axis=0)
    dFx_dy = np.gradient(flow_x, axis=1)
    curl = dFy_dx - dFx_dy
    return curl

# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_all(landscape, flow_x, flow_y, gx, gy, curl):

    fig, axs = plt.subplots(1, 3, figsize=(18,6))

    # --- 1. FLOW FIELD ---
    axs[0].imshow(landscape, origin="lower", alpha=0.6)

    step = 2
    axs[0].quiver(
        flow_x[::step, ::step],
        flow_y[::step, ::step],
        color="cyan",
        scale=50
    )

    axs[0].set_title("Agent Flow Field")

    # --- 2. GRADIENT FIELD ---
    axs[1].imshow(landscape, origin="lower", alpha=0.6)

    axs[1].quiver(
        gx[::step, ::step],
        gy[::step, ::step],
        color="white",
        scale=20
    )

    axs[1].set_title("Gradient Field (Ground Truth)")

    # --- 3. CURL (ROTATION / FLIP ZONES) ---
    im = axs[2].imshow(curl, origin="lower", cmap="bwr")
    axs[2].set_title("Curl (Rotation / Flip Zones)")

    plt.colorbar(im, ax=axs[2])

    for ax in axs:
        ax.axis("off")

    plt.tight_layout()

    path = os.path.join(SAVE_DIR, "flow_field_analysis.png")
    plt.savefig(path, dpi=200)

    print(f"\nSaved → {path}")
    plt.show()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    print("\n🚀 FLOW FIELD ANALYSIS (Level 3)\n")

    landscape = generate_stability_landscape()

    flow_x, flow_y = run_agents(landscape)
    gx, gy = compute_gradient(landscape)
    curl = compute_curl(flow_x, flow_y)

    plot_all(landscape, flow_x, flow_y, gx, gy, curl)
