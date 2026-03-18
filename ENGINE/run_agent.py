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
"""
NEXAH Multi-Agent System — Advanced Version

Includes:
- Role-based agents (Explorer / Climber)
- Reinforcement Learning agent (Q-learning)
- Cluster detection
- Metrics for system evaluation
"""

import numpy as np
import matplotlib.pyplot as plt

ffrom ENGINE.analysis.temporal_landscape import TemporalLandscape


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

        # EXPLORER → random biased
        if role == "explorer":
            pos = neighbors[np.random.randint(len(neighbors))]
            path.append(pos)
            continue

        # CLIMBER → greedy + escape
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

            # choose best action
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
# CLUSTERING
# --------------------------------------------------

def cluster_endpoints(points, threshold=3):
    clusters = []

    for p in points:
        added = False

        for c in clusters:
            if np.linalg.norm(np.array(p) - np.array(c["center"])) < threshold:
                c["points"].append(p)
                xs = [pt[0] for pt in c["points"]]
                ys = [pt[1] for pt in c["points"]]
                c["center"] = (int(np.mean(xs)), int(np.mean(ys)))
                added = True
                break

        if not added:
            clusters.append({"center": p, "points": [p]})

    return clusters


# --------------------------------------------------
# METRICS
# --------------------------------------------------

def compute_metrics(final_positions, clusters):
    values = [v for _, v in final_positions]

    dominant_cluster = max(clusters, key=lambda c: len(c["points"]))

    return {
        "max": max(values),
        "mean": np.mean(values),
        "num_clusters": len(clusters),
        "dominant_size": len(dominant_cluster["points"])
    }


# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def visualize(landscape, paths, clusters):
    plt.figure(figsize=(8,6))
    plt.imshow(landscape, cmap="viridis", origin="lower")
    plt.colorbar()

    for p in paths:
        xs = [x for x,_ in p]
        ys = [y for _,y in p]
        plt.plot(xs, ys)

    for c in clusters:
        cx, cy = c["center"]
        plt.scatter(cx, cy, s=150, marker="X")

    plt.title("NEXAH Advanced Multi-Agent System")
    plt.show()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    landscape = generate_stability_landscape()

    paths = []
    final_positions = []

    # ROLE AGENTS
    roles = ["explorer", "climber"]

    for i in range(8):
        role = roles[i % 2]
        path = run_agent(landscape, role=role)
        paths.append(path)

        pos = path[-1]
        final_positions.append((pos, landscape[pos]))

        print(f"{role} agent → {pos} | {landscape[pos]:.3f}")

    # RL AGENT
    rl_path = run_rl_agent(landscape)
    paths.append(rl_path)
    pos = rl_path[-1]
    final_positions.append((pos, landscape[pos]))

    print(f"RL agent → {pos} | {landscape[pos]:.3f}")

    # CLUSTER
    endpoints = [p for p,_ in final_positions]
    clusters = cluster_endpoints(endpoints)

    print("\nClusters:")
    for c in clusters:
        print(c)

    # METRICS
    metrics = compute_metrics(final_positions, clusters)

    print("\nMetrics:")
    print(metrics)

    # VISUALIZE
    visualize(landscape, paths, clusters)


if __name__ == "__main__":
    main()
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
# Clustering (attractor detection)
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
# Visualization
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
        plt.scatter(xs[-1], ys[-1], s=40)

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

    # --------------------------------------------
    # CLUSTER ANALYSIS
    # --------------------------------------------

    endpoints = [p for p, _ in final_positions]
    clusters = cluster_endpoints(endpoints)

    print("\n--- Cluster Analysis ---")

    for i, c in enumerate(clusters):
        print(f"Cluster {i}: center={c['center']} | size={len(c['points'])}")

    print("\nAgent finished.")

    # Visualization
    visualize_agents(landscape, paths, clusters)


# --------------------------------------------------

if __name__ == "__main__":
    main()
