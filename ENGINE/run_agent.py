"""
NEXAH Multi-Agent Exploration System

This module demonstrates structural navigation on a stability landscape.

Concept:
--------
Agents operate on a generated stability landscape and attempt to move toward
higher stability regions.

Key Features:
-------------
- Multi-agent simulation
- Exploration vs exploitation strategy
- Gradient-based navigation (local)
- Escape from local minima via randomness
- Visualization of agent trajectories

Interpretation:
---------------
This is not just optimization.

This is:
→ Navigation in a dynamical stability field

Agents do not "solve a task"
They explore and discover stable regimes.

This forms the basis for:
- Reinforcement learning on landscapes
- Stability-driven decision systems
- Autonomous scientific exploration

Part of:
--------
NEXAH — Structural Navigation Framework
"""

import numpy as np
import matplotlib.pyplot as plt

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape


# --------------------------------------------------
# Neighborhood system
# --------------------------------------------------

def get_neighbors(pos, size):
    x, y = pos
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    neighbors = []

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size:
            neighbors.append((nx, ny))

    return neighbors


# --------------------------------------------------
# Agent logic (exploration + exploitation)
# --------------------------------------------------

def run_agent(landscape, steps=30, exploration_rate=0.2):
    size = landscape.shape[0]

    pos = (np.random.randint(0, size), np.random.randint(0, size))
    path = [pos]

    for _ in range(steps):

        x, y = pos
        current_value = landscape[x, y]

        neighbors = get_neighbors(pos, size)

        # Exploration (random move)
        if np.random.rand() < exploration_rate:
            pos = neighbors[np.random.randint(len(neighbors))]
            path.append(pos)
            continue

        # Exploitation (greedy climb)
        best_pos = pos
        best_value = current_value

        for nx, ny in neighbors:
            val = landscape[nx, ny]
            if val > best_value:
                best_value = val
                best_pos = (nx, ny)

        # Escape local minima
        if best_pos == pos:
            pos = neighbors[np.random.randint(len(neighbors))]
            path.append(pos)
            continue

        pos = best_pos
        path.append(pos)

    return path


# --------------------------------------------------
# Visualization
# --------------------------------------------------

def visualize_agents(landscape, paths):
    plt.figure(figsize=(8, 6))

    plt.imshow(landscape, cmap="viridis", origin="lower")
    plt.colorbar(label="Stability")

    for path in paths:
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]

        plt.plot(xs, ys, linewidth=1)
        plt.scatter(xs[-1], ys[-1], s=40)

    plt.title("NEXAH Multi-Agent Navigation")
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.show()


# --------------------------------------------------
# Main execution
# --------------------------------------------------

def main():
    print("NEXAH Multi-Agent System (Exploration Mode)")
    print("Initializing landscape...\n")

    landscape = generate_stability_landscape()

    num_agents = 10
    final_positions = []
    paths = []

    for i in range(num_agents):
        path = run_agent(landscape)
        paths.append(path)

        final_pos = path[-1]
        final_value = landscape[final_pos]

        final_positions.append((final_pos, final_value))

        print(f"Agent {i}: final position {final_pos} | stability {final_value:.3f}")

    print("\n--- Summary ---")

    values = [v for _, v in final_positions]

    print(f"Max stability found: {max(values):.3f}")
    print(f"Mean stability: {np.mean(values):.3f}")
    print(f"Unique end points: {len(set([p for p,_ in final_positions]))}")

    print("\nAgent finished.")

    # Visualization
    visualize_agents(landscape, paths)


# --------------------------------------------------

if __name__ == "__main__":
    main()
