import numpy as np
import matplotlib.pyplot as plt
import os

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 50
N_RUNS = 2000
STEPS = 80

SAVE_DIR = "ENGINE/visuals/monte_carlo"
os.makedirs(SAVE_DIR, exist_ok=True)

# --------------------------------------------------
# HARDER LANDSCAPE
# --------------------------------------------------

def generate_harder_landscape(size=50):
    x = np.linspace(0, size-1, size)
    y = np.linspace(0, size-1, size)
    X, Y = np.meshgrid(x, y)

    landscape = np.zeros((size, size))

    # mehrere Peaks
    for _ in range(6):
        cx, cy = np.random.randint(0, size, 2)
        amp = np.random.uniform(0.5, 1.5)
        sigma = np.random.uniform(3, 8)

        landscape += amp * np.exp(-((X-cx)**2 + (Y-cy)**2)/(2*sigma**2))

    # Noise
    landscape += 0.1 * np.random.randn(size, size)

    return landscape

# --------------------------------------------------
# MOVES (8-direction + periodic)
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
# AGENT (mit Temperatur)
# --------------------------------------------------

def run_agent(landscape, temperature=0.3):
    pos = (np.random.randint(0, SIZE), np.random.randint(0, SIZE))
    path = [pos]

    for _ in range(STEPS):
        neighbors = get_neighbors(pos)
        vals = np.array([landscape[nx, ny] for nx, ny in neighbors])

        if np.random.rand() < temperature:
            pos = neighbors[np.random.randint(len(neighbors))]
        else:
            pos = neighbors[np.argmax(vals)]

        path.append(pos)

    return path

# --------------------------------------------------
# MONTE CARLO + VECTOR FIELD
# --------------------------------------------------

def run_monte_carlo():
    landscape = generate_harder_landscape(SIZE)

    visit = np.zeros((SIZE, SIZE))
    endpoint = np.zeros((SIZE, SIZE))

    # vector field
    flow_x = np.zeros((SIZE, SIZE))
    flow_y = np.zeros((SIZE, SIZE))

    for _ in range(N_RUNS):
        path = run_agent(landscape)

        for i in range(len(path)-1):
            x1, y1 = path[i]
            x2, y2 = path[i+1]

            visit[x1, y1] += 1

            flow_x[x1, y1] += (x2 - x1)
            flow_y[x1, y1] += (y2 - y1)

        ex, ey = path[-1]
        endpoint[ex, ey] += 1

    return landscape, visit, endpoint, flow_x, flow_y

# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_all(landscape, visit, endpoint, flow_x, flow_y):
    visit_log = np.log1p(visit)
    endpoint_log = np.log1p(endpoint)

    fig, axs = plt.subplots(1, 3, figsize=(15,5))

    # Visit
    axs[0].imshow(visit_log, cmap="inferno", origin="lower")
    axs[0].set_title("Visit Density")

    # Endpoint
    axs[1].imshow(endpoint_log, cmap="inferno", origin="lower")
    axs[1].set_title("Endpoint Density")

    # Vector field
    axs[2].imshow(visit_log, cmap="gray", origin="lower")

    skip = 3
    axs[2].quiver(
        flow_x[::skip, ::skip],
        flow_y[::skip, ::skip],
        color="cyan"
    )

    axs[2].set_title("Flow Field")

    for ax in axs:
        ax.axis("off")

    plt.tight_layout()

    path = os.path.join(SAVE_DIR, "monte_carlo_vector_field.png")
    plt.savefig(path, dpi=200)

    print(f"\nSaved → {path}")
    plt.show()

# --------------------------------------------------

if __name__ == "__main__":
    data = run_monte_carlo()
    plot_all(*data)
