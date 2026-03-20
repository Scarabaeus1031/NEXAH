"""
NEXAH Multi-Agent Exploration System — Animated Version

This version extends the original demo by:
→ Adding animation
→ Exporting a GIF
→ Showing real navigation behavior

This is your "GitHub Hero Demo"
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# optional bridge (safe import)
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ENGINE')))
    from kernel_bridge import get_vortex_metrics, get_chimera_status, get_frustration_score
    BRIDGE_AVAILABLE = True
except:
    BRIDGE_AVAILABLE = False

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
# AGENTS
# --------------------------------------------------

def run_agent(landscape, role="climber", steps=50):
    size = landscape.shape[0]
    pos = (np.random.randint(0, size), np.random.randint(0, size))
    path = [pos]

    for _ in range(steps):
        neighbors = get_neighbors(pos, size)

        if role == "explorer":
            pos = neighbors[np.random.randint(len(neighbors))]
        else:
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
# RL AGENT
# --------------------------------------------------

def run_rl_agent(landscape, episodes=30):
    size = landscape.shape[0]
    Q = np.zeros((size, size, 4))
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

            Q[x, y, a] += 0.1 * (
                reward + 0.9 * np.max(Q[nx, ny]) - Q[x, y, a]
            )

            pos = (nx, ny)

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
# ANIMATION
# --------------------------------------------------

def animate_agents(landscape, paths, clusters, save_path="nexah_multi_agent.gif"):
    fig, ax = plt.subplots(figsize=(8,6))

    ax.imshow(landscape, cmap="viridis", origin="lower")
    ax.set_title("NEXAH Multi-Agent Navigation")

    lines = []
    points = []

    for _ in paths:
        line, = ax.plot([], [], linewidth=1)
        point = ax.scatter([], [], s=40)
        lines.append(line)
        points.append(point)

    max_steps = max(len(p) for p in paths)

    def update(frame):
        for i, path in enumerate(paths):
            if frame < len(path):
                xs = [p[0] for p in path[:frame+1]]
                ys = [p[1] for p in path[:frame+1]]

                lines[i].set_data(xs, ys)
                points[i].set_offsets([xs[-1], ys[-1]])

        # show clusters at end
        if frame == max_steps - 1:
            for c in clusters:
                cx, cy = c["center"]
                ax.scatter(cx, cy, s=120, marker="X", color="white")

        return lines + points

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=max_steps,
        interval=120,
        blit=True
    )

    ani.save(save_path, writer="pillow")
    print(f"GIF saved → {save_path}")

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("\n🚀 NEXAH Animated Multi-Agent Demo\n")

    landscape = generate_stability_landscape()

    paths = []
    final_positions = []

    roles = ["explorer", "climber"]

    for i in range(8):
        role = roles[i % 2]
        path = run_agent(landscape, role=role)
        paths.append(path)

        pos = path[-1]
        final_positions.append((pos, landscape[pos]))

        print(f"{role} → {pos} | {landscape[pos]:.3f}")

    rl_path = run_rl_agent(landscape)
    paths.append(rl_path)

    pos = rl_path[-1]
    final_positions.append((pos, landscape[pos]))

    print(f"RL → {pos} | {landscape[pos]:.3f}")

    endpoints = [p for p,_ in final_positions]
    clusters = cluster_endpoints(endpoints)

    print("\nClusters:")
    for i, c in enumerate(clusters):
        print(f"{i}: {c['center']} ({len(c['points'])})")

    # optional bridge
    if BRIDGE_AVAILABLE:
        try:
            history = np.load('output/phase_history.npy')
            phase_ring = history[-1] if history.ndim == 2 else history

            print("\nBridge Metrics:")
            print("Vortex:", get_vortex_metrics(phase_ring=phase_ring, history=history))
            print("Chimera:", get_chimera_status(phase_ring=phase_ring))
            print("Frustration:", get_frustration_score(N=50))
        except Exception as e:
            print("Bridge failed:", e)

    # 🎬 create GIF
    animate_agents(
        landscape,
        paths,
        clusters,
        save_path="BUILDER_LAB/visuals/nexah_multi_agent.gif"
    )

# --------------------------------------------------

if __name__ == "__main__":
    main()
