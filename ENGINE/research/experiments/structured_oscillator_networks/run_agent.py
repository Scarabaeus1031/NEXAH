"""
NEXAH Multi-Agent Exploration System

T°Xx^^xx^^X
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
- Cluster detection of attractors

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
import sys
import os

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# Bridge importieren – Metriken holen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ENGINE')))
from kernel_bridge import get_vortex_metrics, get_chimera_status, get_frustration_score

# --------------------------------------------------
# NEIGHBORS
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
# ROLE-BASED AGENTS
# --------------------------------------------------

def run_agent(landscape, role="climber", steps=30):
    size = landscape.shape[0]

    pos = (np.random.randint(0, size), np.random.randint(0, size))
    path = [pos]

    for _ in range(steps):
        neighbors = get_neighbors(pos, size)

        if role == "explorer":
            pos = neighbors[np.random.randint(len(neighbors))]
            path.append(pos)
            continue

        x, y = pos
        current = landscape[x, y]

        best_pos = pos
        best_val = current

        for nx, ny in neighbors:
            val = landscape[nx, ny]
            if val > best_val:
                best_val = val
                best_pos = (nx, ny)

        if best_pos == pos:
            pos = neighbors[np.random.randint(len(neighbors))]
        else:
            pos = best_pos

        path.append(pos)

    return path

# --------------------------------------------------
# RL AGENT (Q-LEARNING LIGHT)
# --------------------------------------------------

def run_rl_agent(landscape, episodes=50, alpha=0.1, gamma=0.9):
    size = landscape.shape[0]

    Q = np.zeros((size, size, 4))  # 4 directions

    actions = [(-1,0),(1,0),(0,-1),(0,1)]

    for _ in range(episodes):
        pos = (np.random.randint(0, size), np.random.randint(0, size))

        for _ in range(30):
            x, y = pos

            a = np.argmax(Q[x, y])

            dx, dy = actions[a]
            nx, ny = x + dx, y + dy

            if not (0 <= nx < size and 0 <= ny < size):
                continue

            reward = landscape[nx, ny]

            Q[x, y, a] += alpha * (
                reward + gamma * np.max(Q[nx, ny]) - Q[x, y, a]
            )

            pos = (nx, ny)

    # run learned policy
    pos = (np.random.randint(0, size), np.random.randint(0, size))
    path = [pos]

    for _ in range(30):
        x, y = pos
        a = np.argmax(Q[x, y])
        dx, dy = actions[a]

        nx, ny = x + dx, y + dy

        if not (0 <= nx < size and 0 <= ny < size):
            break

        pos = (nx, ny)
        path.append(pos)

    return path

# --------------------------------------------------
# CLUSTERING (ATTRACTOR DETECTION)
# --------------------------------------------------

def cluster_endpoints(points, threshold=3):
    clusters = []

    for p in points:
        added = False

        for cluster in clusters:
            cx, cy = cluster["center"]

            if np.linalg.norm(np.array(p) - np.array((cx, cy))) < threshold:
                cluster["points"].append(p)

                xs = [pt[0] for pt in cluster["points"]]
                ys = [pt[1] for pt in cluster["points"]]
                cluster["center"] = (int(np.mean(xs)), int(np.mean(ys)))

                added = True
                break

        if not added:
            clusters.append({
                "center": p,
                "points": [p]
            })

    return clusters

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def visualize_agents(landscape, paths, clusters=None):
    plt.figure(figsize=(8, 6))

    plt.imshow(landscape, cmap="viridis", origin="lower")
    plt.colorbar(label="Stability")

    # paths
    for path in paths:
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        plt.plot(xs, ys, linewidth=1)
        plt.scatter(xs[-1], ys[-1], s=40)  # mark endpoint

    # cluster centers
    if clusters:
        for c in clusters:
            cx, cy = c["center"]
            plt.scatter(cx, cy, s=120, marker="X")

    plt.title("NEXAH Multi-Agent Navigation + Clusters")
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.show()

# --------------------------------------------------
# MAIN – mit Bridge-Integration
# --------------------------------------------------

def main():
    print("NEXAH Multi-Agent Demo mit Bridge-Integration")
    print("Initializing landscape...\n")

    landscape = generate_stability_landscape()

    paths = []
    final_positions = []

    # ROLE AGENTS
    roles = ["explorer", "climber"]

    for i in range(8):
        role = roles[i % 2]
        path = run_agent(landscape, role=role, steps=50)
        paths.append(path)

        pos = path[-1]
        final_positions.append((pos, landscape[pos]))

        print(f"{role} agent → {pos} | {landscape[pos]:.3f}")

    # RL AGENT
    rl_path = run_rl_agent(landscape, episodes=30)
    paths.append(rl_path)
    pos = rl_path[-1]
    final_positions.append((pos, landscape[pos]))

    print(f"RL agent → {pos} | {landscape[pos]:.3f}")

    # Cluster
    endpoints = [p for p,_ in final_positions]
    clusters = cluster_endpoints(endpoints)

    print("\n--- Cluster Analysis ---")
    for i, c in enumerate(clusters):
        print(f"Cluster {i}: center={c['center']} | size={len(c['points'])}")

    # Bridge-Metriken auf letztem Agent-Zustand
    print("\n--- Bridge-Metriken (letzter Zustand) ---")
    try:
        history = np.load('output/phase_history.npy')
        phase_ring = history[-1] if history.ndim == 2 else history
        print("Vortex Metrics:", get_vortex_metrics(phase_ring=phase_ring, history=history))
        print("Chimera Status:", get_chimera_status(phase_ring=phase_ring))
        print("Frustration Score:", get_frustration_score(N=50))
    except Exception as e:
        print("Bridge-Metriken fehlgeschlagen:", e)

    print("\nAgent finished.")

    # Visualization
    visualize_agents(landscape, paths, clusters)


# --------------------------------------------------

if __name__ == "__main__":
    main()# ROLE-BASED AGENTS
# --------------------------------------------------

def run_agent(landscape, role="climber", steps=30):
    size = landscape.shape[0]

    pos = (np.random.randint(0, size), np.random.randint(0, size))
    path = [pos]

    for _ in range(steps):
        neighbors = get_neighbors(pos, size)

        if role == "explorer":
            pos = neighbors[np.random.randint(len(neighbors))]
            path.append(pos)
            continue

        x, y = pos
        current = landscape[x, y]

        best_pos = pos
        best_val = current

        for nx, ny in neighbors:
            val = landscape[nx, ny]
            if val > best_val:
                best_val = val
                best_pos = (nx, ny)

        if best_pos == pos:
            pos = neighbors[np.random.randint(len(neighbors))]
        else:
            pos = best_pos

        path.append(pos)

    return path

# --------------------------------------------------
# RL AGENT (Q-LEARNING LIGHT)
# --------------------------------------------------

def run_rl_agent(landscape, episodes=50, alpha=0.1, gamma=0.9):
    size = landscape.shape[0]

    Q = np.zeros((size, size, 4))  # 4 directions

    actions = [(-1,0),(1,0),(0,-1),(0,1)]

    for _ in range(episodes):
        pos = (np.random.randint(0, size), np.random.randint(0, size))

        for _ in range(30):
            x, y = pos

            a = np.argmax(Q[x, y])

            dx, dy = actions[a]
            nx, ny = x + dx, y + dy

            if not (0 <= nx < size and 0 <= ny < size):
                continue

            reward = landscape[nx, ny]

            Q[x, y, a] += alpha * (
                reward + gamma * np.max(Q[nx, ny]) - Q[x, y, a]
            )

            pos = (nx, ny)

    # run learned policy
    pos = (np.random.randint(0, size), np.random.randint(0, size))
    path = [pos]

    for _ in range(30):
        x, y = pos
        a = np.argmax(Q[x, y])
        dx, dy = actions[a]

        nx, ny = x + dx, y + dy

        if not (0 <= nx < size and 0 <= ny < size):
            break

        pos = (nx, ny)
        path.append(pos)

    return path

# --------------------------------------------------
# CLUSTERING (ATTRACTOR DETECTION)
# --------------------------------------------------

def cluster_endpoints(points, threshold=3):
    clusters = []

    for p in points:
        added = False

        for cluster in clusters:
            cx, cy = cluster["center"]

            if np.linalg.norm(np.array(p) - np.array((cx, cy))) < threshold:
                cluster["points"].append(p)

                xs = [pt[0] for pt in cluster["points"]]
                ys = [pt[1] for pt in cluster["points"]]
                cluster["center"] = (int(np.mean(xs)), int(np.mean(ys)))

                added = True
                break

        if not added:
            clusters.append({
                "center": p,
                "points": [p]
            })

    return clusters

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def visualize_agents(landscape, paths, clusters=None):
    plt.figure(figsize=(8, 6))

    plt.imshow(landscape, cmap="viridis", origin="lower")
    plt.colorbar(label="Stability")

    # paths
    for path in paths:
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        plt.plot(xs, ys, linewidth=1)
        plt.scatter(xs[-1], ys[-1], s=40)  # mark endpoint

    # cluster centers
    if clusters:
        for c in clusters:
            cx, cy = c["center"]
            plt.scatter(cx, cy, s=120, marker="X")

    plt.title("NEXAH Multi-Agent Navigation + Clusters")
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.show()

# --------------------------------------------------
# MAIN – mit Bridge-Integration
# --------------------------------------------------^X

def main():
    print("NEXAH Multi-Agent Demo mit Bridge-Integration")
    print("Initializing landscape...\n")

    landscape = generate_stability_landscape()

    paths = []
    final_positions = []

    # ROLE AGENTS
    roles = ["explorer", "climber"]

    for i in range(8):
        role = roles[i % 2]
        path = run_agent(landscape, role=role, steps=50)
        paths.append(path)

        pos = path[-1]
        final_positions.append((pos, landscape[pos]))

        print(f"{role} agent → {pos} | {landscape[pos]:.3f}")

    # RL AGENT
    rl_path = run_rl_agent(landscape, episodes=30)
    paths.append(rl_path)
    pos = rl_path[-1]
    final_positions.append((pos, landscape[pos]))

    print(f"RL agent → {pos} | {landscape[pos]:.3f}")

    # Cluster
    endpoints = [p for p,_ in final_positions]
    clusters = cluster_endpoints(endpoints)

    print("\n--- Cluster Analysis ---")
    for i, c in enumerate(clusters):
        print(f"Cluster {i}: center={c['center']} | size={len(c['points'])}")

    # Bridge-Metriken auf letztem Agent-Zustand
    print("\n--- Bridge-Metriken (letzter Zustand) ---")
    try:
        history = np.load('output/phase_history.npy')
        phase_ring = history[-1] if history.ndim == 2 else history
        print("Vortex Metrics:", get_vortex_metrics(phase_ring=phase_ring, history=history))
        print("Chimera Status:", get_chimera_status(phase_ring=phase_ring))
        print("Frustration Score:", get_frustration_score(N=50))
    except Exception as e:
        print("Bridge-Metriken fehlgeschlagen:", e)

    print("\nAgent finished.")

    # Visualization
    visualize_agents(landscape, paths, clusters)


# --------------------------------------------------

if __name__ == "__main__":
    main()
