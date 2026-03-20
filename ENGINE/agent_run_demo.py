import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os

# --------------------------------------------------
# IMPORTS + Ordner sicherstellen
# --------------------------------------------------
try:
    from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape
except ImportError:
    print("⚠️  generate_stability_landscape konnte nicht importiert werden!")
    sys.exit(1)

# Optional Bridge
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from kernel_bridge import get_vortex_metrics, get_chimera_status, get_frustration_score
    BRIDGE_AVAILABLE = True
except:
    BRIDGE_AVAILABLE = False

# Ordner für Visuals sicherstellen
os.makedirs("BUILDER_LAB/visuals", exist_ok=True)

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
            Q[x, y, a] += 0.1 * (reward + 0.9 * np.max(Q[nx, ny]) - Q[x, y, a])
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
            clusters.append({"center": p, "points": [p]})
    return clusters

# --------------------------------------------------
# ANIMATION (GIF) → mit "test_" Prefix
# --------------------------------------------------
def animate_agents(landscape, paths, clusters, save_path="BUILDER_LAB/visuals/test_nexah_multi_agent.gif"):
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
        if frame == max_steps - 1:
            for c in clusters:
                cx, cy = c["center"]
                ax.scatter(cx, cy, s=120, marker="X", color="white")
        return lines + points
    ani = animation.FuncAnimation(fig, update, frames=max_steps, interval=120, blit=True)
    ani.save(save_path, writer="pillow")
    print(f"✅ TEST-GIF gespeichert → {save_path}")

# --------------------------------------------------
# TEMPORAL OVERLAY (GitHub-Desktop-Effekt) → mit "test_" Prefix
# --------------------------------------------------
def save_multi_frame_overlay(landscape, paths, clusters, save_path="BUILDER_LAB/visuals/test_nexah_all_paths_overlay.png"):
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.imshow(landscape, cmap="viridis", origin="lower")
    ax.set_title("NEXAH — Temporal Path Overlay (GitHub Desktop Style)")
    
    colors = ['red', 'magenta', 'cyan', 'lime', 'orange', 'purple', 'yellow', 'white']
    
    for i, path in enumerate(paths):
        color = colors[i % len(colors)]
        length = len(path)
        # 3 Zeitpunkte übereinanderlegen
        for stage, alpha in [(0, 0.25), (length//2, 0.55), (length-1, 0.95)]:
            xs = [p[0] for p in path[:stage+1]]
            ys = [p[1] for p in path[:stage+1]]
            ax.plot(xs, ys, color=color, linewidth=2.8, alpha=alpha)
            if stage > 0:
                ax.scatter(xs[-1], ys[-1], s=45, color=color, alpha=alpha, edgecolor='white')
    
    # Cluster
    for c in clusters:
        cx, cy = c["center"]
        ax.scatter(cx, cy, s=220, marker="X", color="white", edgecolor="black", linewidth=3, zorder=10)
        ax.text(cx+0.8, cy-0.8, f"{len(c['points'])}", color="black", fontsize=11, ha='center', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=250, bbox_inches='tight')
    print(f"✅ TEST-Overlay-PNG gespeichert → {save_path}")

# --------------------------------------------------
# MAIN
# --------------------------------------------------
def main():
    print("\n🚀 NEXAH Multi-Agent Demo gestartet (TEST-Version)\n")
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
        print(f"{role} → {pos} | Wert: {landscape[pos]:.3f}")
    
    rl_path = run_rl_agent(landscape)
    paths.append(rl_path)
    pos = rl_path[-1]
    final_positions.append((pos, landscape[pos]))
    print(f"RL-Agent → {pos} | Wert: {landscape[pos]:.3f}")
    
    endpoints = [p for p,_ in final_positions]
    clusters = cluster_endpoints(endpoints)
    
    print("\nClusters gefunden:")
    for i, c in enumerate(clusters):
        print(f"  {i}: {c['center']} ({len(c['points'])} Agenten)")
    
    # GIF (neuer Name)
    animate_agents(landscape, paths, clusters)
    
    # Temporal Overlay (neuer Name)
    save_multi_frame_overlay(landscape, paths, clusters)

if __name__ == "__main__":
    main()
