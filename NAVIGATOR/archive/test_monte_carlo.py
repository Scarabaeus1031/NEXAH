import numpy as np
import matplotlib.pyplot as plt

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape
from ENGINE.analysis.monte_carlo_navigation import run_monte_carlo, compute_visit_density, compute_endpoint_density

# --- simple agent (reuse logic) ---
def get_neighbors(pos, size):
    x, y = pos
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    neighbors = []

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size:
            neighbors.append((nx, ny))

    return neighbors


def run_agent(landscape, steps=50):
    size = landscape.shape[0]
    pos = (np.random.randint(0, size), np.random.randint(0, size))
    path = [pos]

    for _ in range(steps):
        neighbors = get_neighbors(pos, size)

        x, y = pos
        current = landscape[x, y]

        best_pos = pos
        best_val = current

        for nx, ny in neighbors:
            val = landscape[nx, ny]
            if val > best_val:
                best_val = val
                best_pos = (nx, ny)

        pos = best_pos
        path.append(pos)

    return path


# --- run test ---
landscape = generate_stability_landscape()

paths = run_monte_carlo(
    landscape,
    agent_fn=run_agent,
    n_runs=300,
    steps=50
)

density = compute_visit_density(paths, size=landscape.shape[0])
endpoint_density = compute_endpoint_density(paths, size=landscape.shape[0])


# --- plot ---
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.imshow(density, cmap="hot", origin="lower")
plt.title("Visit Density")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(endpoint_density, cmap="hot", origin="lower")
plt.title("Endpoint Density")
plt.axis("off")

plt.tight_layout()
plt.show()
