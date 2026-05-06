import numpy as np
import matplotlib.pyplot as plt
import os

# ----------------------------
# 1. Vector field
# ----------------------------
def F(x, y):
    return np.array([
        y + 0.2 * x,
        -x - 0.3 * y + 0.05 * np.tanh(x)
    ])


# ----------------------------
# 2. Coherence
# ----------------------------
def coherence(v, f):
    nv = np.linalg.norm(v)
    nf = np.linalg.norm(f)

    if nv < 1e-6 or nf < 1e-6:
        return 1.0

    return np.dot(v, f) / (nv * nf)


# ----------------------------
# 3. Structured risk
# ----------------------------
def compute_risk(x, c=1.0):
    r = np.linalg.norm(x)

    base = np.tanh(r / 2.0)

    fx, fy = F(x[0], x[1])
    curvature = np.abs(fx * fy)
    curvature = np.tanh(curvature)

    coherence_term = (1 - c)

    risk = 0.6 * base + 0.3 * curvature + 0.1 * coherence_term
    return np.clip(risk, 0, 1)


# ----------------------------
# 4. Gradient of risk
# ----------------------------
def grad_risk(x, eps=1e-3):
    dx = np.array([eps, 0.0])
    dy = np.array([0.0, eps])

    r_x1 = compute_risk(x + dx, 1.0)
    r_x2 = compute_risk(x - dx, 1.0)

    r_y1 = compute_risk(x + dy, 1.0)
    r_y2 = compute_risk(x - dy, 1.0)

    dRx = (r_x1 - r_x2) / (2 * eps)
    dRy = (r_y1 - r_y2) / (2 * eps)

    return np.array([dRx, dRy])


# ----------------------------
# 5. Compute risk field grid
# ----------------------------
def compute_field(x_range, y_range, res=140):
    X, Y = np.meshgrid(
        np.linspace(*x_range, res),
        np.linspace(*y_range, res)
    )

    R = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            pos = np.array([X[i, j], Y[i, j]])
            R[i, j] = compute_risk(pos, 1.0)

    return X, Y, R


# ----------------------------
# 6. Build agent network by distance
# ----------------------------
def build_edges(points, threshold=1.0):
    edges = []
    n = len(points)

    for i in range(n):
        for j in range(i + 1, n):
            d = np.linalg.norm(points[i] - points[j])
            if d < threshold:
                edges.append((i, j, d))
    return edges


# ----------------------------
# 7. Multi-agent simulation
# ----------------------------
np.random.seed(42)

dt = 0.05
steps = 220
n_agents = 8

agents = np.array([
    [-2.2, -1.5],
    [-1.8,  1.8],
    [ 2.0,  1.6],
    [ 2.2, -1.6],
    [-0.4,  2.2],
    [ 0.7, -2.2],
    [-2.5,  0.2],
    [ 2.4,  0.1],
], dtype=float)

trajectories = [[] for _ in range(n_agents)]
agent_risks = [[] for _ in range(n_agents)]
agent_coherences = [[] for _ in range(n_agents)]

for _ in range(steps):
    new_agents = agents.copy()

    for i in range(n_agents):
        x = agents[i].copy()

        f = F(x[0], x[1])
        noise = np.random.normal(0, 0.12, size=2)
        v = f + noise

        c = coherence(v, f)
        r = compute_risk(x, c)
        g = grad_risk(x)

        # Field-driven control
        u_field = -0.9 * g

        # Weak network cohesion: agents pull slightly toward nearby neighbors
        neighbor_pull = np.zeros(2)
        count = 0
        for j in range(n_agents):
            if i == j:
                continue
            d = np.linalg.norm(agents[j] - x)
            if d < 1.2:
                neighbor_pull += (agents[j] - x)
                count += 1

        if count > 0:
            neighbor_pull = 0.08 * (neighbor_pull / count)

        u = u_field + neighbor_pull

        x_next = x + dt * (v + u)

        # Safety clip
        norm_x = np.linalg.norm(x_next)
        if norm_x > 4.0:
            x_next = x_next / norm_x * 4.0

        new_agents[i] = x_next

        trajectories[i].append(x.copy())
        agent_risks[i].append(r)
        agent_coherences[i].append(c)

    agents = new_agents

trajectories = [np.array(t) for t in trajectories]
agent_risks = [np.array(r) for r in agent_risks]
agent_coherences = [np.array(c) for c in agent_coherences]

final_positions = np.array([traj[-1] for traj in trajectories])
edges = build_edges(final_positions, threshold=1.1)

# ----------------------------
# 8. Risk field background
# ----------------------------
X, Y, R = compute_field((-3, 3), (-3, 3))

# ----------------------------
# 9. Plot
# ----------------------------
fig, ax = plt.subplots(figsize=(8, 8))

im = ax.contourf(X, Y, R, levels=50, cmap="plasma")

# regime boundaries
ax.contour(X, Y, R, levels=[0.3], colors="white", linewidths=2)
ax.contour(X, Y, R, levels=[0.6], colors="red", linewidths=2)

# plot each agent trajectory
colors = plt.cm.tab10(np.linspace(0, 1, n_agents))

for i in range(n_agents):
    traj = trajectories[i]
    ax.plot(traj[:, 0], traj[:, 1], color=colors[i], alpha=0.9, linewidth=1.8)
    ax.scatter(traj[0, 0], traj[0, 1], color=colors[i], s=35, marker="o")
    ax.scatter(traj[-1, 0], traj[-1, 1], color=colors[i], s=60, marker="s")

# draw network edges between final positions
for i, j, d in edges:
    xi, yi = final_positions[i]
    xj, yj = final_positions[j]
    ax.plot([xi, xj], [yi, yj], color="cyan", alpha=0.7, linewidth=1.5)

# label final nodes
for i, p in enumerate(final_positions):
    ax.text(p[0] + 0.05, p[1] + 0.05, f"A{i}", fontsize=9)

ax.set_title("NEXAH V10: Multi-Agent Field Network")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_aspect("equal")

cbar = fig.colorbar(im, ax=ax)
cbar.set_label("Risk Field")

output_dir = os.path.join(os.path.dirname(__file__), "../output")
os.makedirs(output_dir, exist_ok=True)

path = os.path.join(output_dir, "v10_multi_agent_network.png")
plt.savefig(path, dpi=160, bbox_inches="tight")
print("Saved:", path)

plt.close()
