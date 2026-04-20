# navigator_v38_capture_hook_navigation.py

import os
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(42)

# ============================================================
# 1. CLUSTERS
# ============================================================

clusters = {
    "C0": np.array([10.0, 25.0]),
    "C1": np.array([12.0, 24.0]),
    "C2": np.array([13.5, 26.0]),   # target
    "C3": np.array([11.0, 28.5]),
}

cluster_colors = {
    "C0": "#1f77b4",
    "C1": "#ff7f0e",
    "C2": "#2ca02c",
    "C3": "#d62728",
}

# ============================================================
# 2. FIELD
# ============================================================

def gaussian(x, y, center, strength, sigma=1.2):
    return strength * np.exp(-((x - center[0])**2 + (y - center[1])**2) / (2 * sigma**2))

def scalar_field(x, y):
    return (
        gaussian(x, y, clusters["C0"], 1.5)
        + gaussian(x, y, clusters["C1"], 2.0)
        + gaussian(x, y, clusters["C2"], 3.0)
        - gaussian(x, y, clusters["C3"], 2.0)
    )

def grad_field(x, y, eps=1e-3):
    dx = (scalar_field(x + eps, y) - scalar_field(x - eps, y)) / (2 * eps)
    dy = (scalar_field(x, y + eps) - scalar_field(x, y - eps)) / (2 * eps)
    return np.array([dx, dy])

def rotational_field(x, y):
    p = np.array([x, y], dtype=float)
    v = np.zeros(2, dtype=float)

    # around C2
    r2 = p - clusters["C2"]
    d2 = np.linalg.norm(r2) + 1e-9
    v += 0.60 * np.array([r2[1], -r2[0]]) * np.exp(-(d2**2) / (2 * 1.6**2))

    # around C3
    r3 = p - clusters["C3"]
    d3 = np.linalg.norm(r3) + 1e-9
    v += 0.55 * np.array([-r3[1], r3[0]]) * np.exp(-(d3**2) / (2 * 1.3**2))

    return v

def combined_field(x, y):
    return grad_field(x, y) + rotational_field(x, y)

# ============================================================
# 3. CAPTURE HOOK TERM
# ============================================================

def capture_hook_field(x, y, target, hook_radius=1.6, hook_strength=1.15):
    """
    Adds a hook-like capture term near the target.
    Outside the hook radius it is weak; inside, it bends the path
    into a tangential + inward capture arc.
    """
    p = np.array([x, y], dtype=float)
    r = p - target
    d = np.linalg.norm(r) + 1e-9

    # radial inward component
    inward = -r / d

    # tangential component to create hook / entry arc
    tangential = np.array([r[1], -r[0]]) / d

    # activate near target
    gate = np.exp(-(d**2) / (2 * hook_radius**2))

    # stronger tangential just outside center, inward near center
    tang_weight = hook_strength * gate
    in_weight = 0.9 * hook_strength * gate * (1.2 + 0.8 * np.exp(-d))

    return tang_weight * tangential + in_weight * inward

# ============================================================
# 4. NAVIGATION ENGINE
# ============================================================

def nearest_cluster(point):
    return min(clusters.keys(), key=lambda k: np.linalg.norm(point - clusters[k]))

def shortest_path(start_node, target_node):
    # fixed operational weights from V36
    edges = {
        ("C0", "C1"): 2.45,
        ("C0", "C2"): 3.64,
        ("C0", "C3"): 4.32,
        ("C1", "C2"): 2.28,
        ("C1", "C3"): 6.63,
        ("C2", "C3"): 5.65,
    }
    for (a, b), w in list(edges.items()):
        edges[(b, a)] = w

    nodes = list(clusters.keys())
    dist = {n: np.inf for n in nodes}
    prev = {n: None for n in nodes}
    dist[start_node] = 0
    Q = nodes.copy()

    while Q:
        u = min(Q, key=lambda n: dist[n])
        Q.remove(u)

        if u == target_node:
            break

        for v in nodes:
            if (u, v) in edges:
                alt = dist[u] + edges[(u, v)]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

    path = []
    u = target_node
    while u is not None:
        path.insert(0, u)
        u = prev[u]
    return path

def follow_segment(start, target, steps=220, step_size=0.075, hook=False):
    x = start.copy()
    traj = [x.copy()]

    for _ in range(steps):
        v = combined_field(x[0], x[1])

        # bias toward graph target
        bias = 0.35 * (target - x)

        # optional capture hook near final target
        if hook:
            hook_v = capture_hook_field(x[0], x[1], target)
        else:
            hook_v = np.zeros(2)

        direction = v + bias + hook_v
        direction = direction / (np.linalg.norm(direction) + 1e-9)

        x = x + step_size * direction
        traj.append(x.copy())

        if np.linalg.norm(x - target) < 0.18:
            break

    return np.array(traj)

def full_navigation(start_point, target_node="C2"):
    start_node = nearest_cluster(start_point)
    path_nodes = shortest_path(start_node, target_node)

    full_traj = []
    current = start_point.copy()

    for i, node in enumerate(path_nodes):
        target = clusters[node]
        is_final = (i == len(path_nodes) - 1)
        seg = follow_segment(current, target, hook=is_final)
        full_traj.extend(seg)
        current = seg[-1]

    return np.array(full_traj), path_nodes

# ============================================================
# 5. GRID FOR VISUALIZATION
# ============================================================

xv = np.linspace(6, 17, 220)
yv = np.linspace(22, 31, 220)
X, Y = np.meshgrid(xv, yv)
Z = scalar_field(X, Y)

# capture intensity map near C2
Hook = np.zeros_like(X)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        Hook[i, j] = np.linalg.norm(capture_hook_field(X[i, j], Y[i, j], clusters["C2"]))

# ============================================================
# 6. RUN
# ============================================================

start_point = np.array([8.0, 28.0], dtype=float)
traj, graph_path = full_navigation(start_point, target_node="C2")

print("Graph path:", graph_path)
print("Final point:", traj[-1])
print("Final cluster:", nearest_cluster(traj[-1]))

# ============================================================
# 7. PLOTTING
# ============================================================

fig, axs = plt.subplots(2, 2, figsize=(13, 11))

# Q1 — field + hook path
im1 = axs[0, 0].contourf(X, Y, Z, levels=40, cmap="viridis")
axs[0, 0].plot(traj[:, 0], traj[:, 1], color="cyan", lw=3, label="capture path")
axs[0, 0].scatter(start_point[0], start_point[1], color="white", s=110, label="start", zorder=6)

for c, p in clusters.items():
    axs[0, 0].scatter(p[0], p[1], color=cluster_colors[c], s=130, edgecolor="black", zorder=5)
    axs[0, 0].text(p[0] + 0.08, p[1] + 0.08, c, color="black")

axs[0, 0].set_title("Q1 — Capture Hook Navigation")
axs[0, 0].set_xlabel("α")
axs[0, 0].set_ylabel("β")
axs[0, 0].legend(loc="upper right")
fig.colorbar(im1, ax=axs[0, 0], fraction=0.046, pad=0.04)

# Q2 — hook field around C2
im2 = axs[0, 1].contourf(X, Y, Hook, levels=35, cmap="magma")
axs[0, 1].contour(X, Y, Hook, levels=8, colors="white", alpha=0.35, linewidths=0.7)
axs[0, 1].scatter(clusters["C2"][0], clusters["C2"][1], color=cluster_colors["C2"], s=150, edgecolor="black")
axs[0, 1].set_title("Q2 — Capture Intensity Around C2")
axs[0, 1].set_xlabel("α")
axs[0, 1].set_ylabel("β")
fig.colorbar(im2, ax=axs[0, 1], fraction=0.046, pad=0.04)

# Q3 — local zoom near C2
axs[1, 0].contourf(X, Y, Z, levels=40, cmap="viridis")
axs[1, 0].plot(traj[:, 0], traj[:, 1], color="cyan", lw=3)
axs[1, 0].scatter(traj[-1, 0], traj[-1, 1], color="yellow", s=90, edgecolor="black", zorder=7)
axs[1, 0].scatter(clusters["C2"][0], clusters["C2"][1], color=cluster_colors["C2"], s=150, edgecolor="black")
axs[1, 0].set_xlim(12.4, 14.4)
axs[1, 0].set_ylim(25.1, 26.8)
axs[1, 0].set_title("Q3 — Local Capture Geometry at C2")
axs[1, 0].set_xlabel("α")
axs[1, 0].set_ylabel("β")

# Q4 — abstract path nodes
axs[1, 1].axis("off")
axs[1, 1].set_title("Q4 — Graph Path")

y_positions = np.linspace(0.8, 0.2, len(graph_path))
for i, node in enumerate(graph_path):
    axs[1, 1].scatter(0.5, y_positions[i], s=900, color=cluster_colors[node], edgecolor="black")
    axs[1, 1].text(0.5, y_positions[i], node, color="white", ha="center", va="center", fontsize=14)
    if i < len(graph_path) - 1:
        axs[1, 1].annotate(
            "",
            xy=(0.5, y_positions[i+1] + 0.05),
            xytext=(0.5, y_positions[i] - 0.05),
            arrowprops=dict(arrowstyle="->", lw=2.0, color="gray")
        )
axs[1, 1].set_xlim(0, 1)
axs[1, 1].set_ylim(0, 1)

plt.tight_layout()

out_path = os.path.join(OUTPUT_DIR, "v38_capture_hook_navigation.png")
plt.savefig(out_path, dpi=180, bbox_inches="tight")
plt.close()

print("Saved:", out_path)
