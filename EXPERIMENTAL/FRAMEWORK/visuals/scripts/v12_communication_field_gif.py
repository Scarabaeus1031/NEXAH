import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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
# 2. Risk
# ----------------------------
def compute_risk(x):
    r = np.linalg.norm(x)
    base = np.tanh(r / 2.0)

    fx, fy = F(x[0], x[1])
    curvature = np.tanh(abs(fx * fy))

    return np.clip(0.7 * base + 0.3 * curvature, 0, 1)


# ----------------------------
# 3. Gradient of risk
# ----------------------------
def grad_risk(x, eps=1e-3):
    dx = np.array([eps, 0.0])
    dy = np.array([0.0, eps])

    dRx = (compute_risk(x + dx) - compute_risk(x - dx)) / (2 * eps)
    dRy = (compute_risk(x + dy) - compute_risk(x - dy)) / (2 * eps)

    return np.array([dRx, dRy])


# ----------------------------
# 4. Build field grid
# ----------------------------
def build_field():
    X, Y = np.meshgrid(np.linspace(-3, 3, 120), np.linspace(-3, 3, 120))
    R = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            R[i, j] = compute_risk(np.array([X[i, j], Y[i, j]]))

    return X, Y, R


# ----------------------------
# 5. Build dynamic edges
# ----------------------------
def build_edges(points, threshold=1.1):
    edges = []
    n = len(points)

    for i in range(n):
        for j in range(i + 1, n):
            d = np.linalg.norm(points[i] - points[j])
            if d < threshold:
                edges.append((i, j))
    return edges


# ----------------------------
# 6. Agents
# ----------------------------
np.random.seed(1)

agents = np.array([
    [-2.2, -1.5],
    [-1.8,  1.8],
    [ 2.0,  1.6],
    [ 2.2, -1.6],
    [-0.4,  2.2],
    [ 0.7, -2.2],
], dtype=float)

n_agents = len(agents)
trajectories = [[] for _ in range(n_agents)]

dt = 0.05

# ----------------------------
# 7. Field background
# ----------------------------
X, Y, R = build_field()

# ----------------------------
# 8. Plot setup
# ----------------------------
fig, ax = plt.subplots(figsize=(6, 6))
ax.contourf(X, Y, R, levels=50, cmap="plasma")

colors = plt.cm.tab10(np.linspace(0, 1, n_agents))

lines = [ax.plot([], [], color=colors[i], linewidth=1.8)[0] for i in range(n_agents)]
points = [ax.plot([], [], "o", color=colors[i], markersize=6)[0] for i in range(n_agents)]

# dynamic network edges
edge_lines = []

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_title("NEXAH V10 – Multi-Agent Network Dynamics")
ax.set_aspect("equal")
ax.set_xlabel("x")
ax.set_ylabel("y")


# ----------------------------
# 9. Animation update
# ----------------------------
def update(frame):
    global agents, edge_lines

    new_agents = agents.copy()

    # move agents
    for i in range(n_agents):
        x = agents[i]

        f = F(x[0], x[1])
        noise = np.random.normal(0, 0.1, 2)

        g = grad_risk(x)
        u = -0.8 * g

        x_next = x + dt * (f + noise + u)

        # clip to avoid runaway trajectories
        norm_x = np.linalg.norm(x_next)
        if norm_x > 4:
            x_next = x_next / norm_x * 4

        new_agents[i] = x_next
        trajectories[i].append(x_next)

    agents = new_agents

    # update trajectories + points
    for i in range(n_agents):
        traj = np.array(trajectories[i])

        if len(traj) > 1:
            lines[i].set_data(traj[:, 0], traj[:, 1])
            points[i].set_data([traj[-1, 0]], [traj[-1, 1]])

    # remove old network edges
    for line in edge_lines:
        line.remove()
    edge_lines = []

    # build new dynamic edges from current agent positions
    current_positions = agents.copy()
    edges = build_edges(current_positions, threshold=1.1)

    for i, j in edges:
        xi, yi = current_positions[i]
        xj, yj = current_positions[j]
        edge_line, = ax.plot(
            [xi, xj], [yi, yj],
            color="cyan",
            alpha=0.7,
            linewidth=1.2
        )
        edge_lines.append(edge_line)

    return lines + points + edge_lines


# ----------------------------
# 10. Run animation
# ----------------------------
anim = FuncAnimation(fig, update, frames=160, interval=50, blit=False)

# ----------------------------
# 11. Save GIF
# ----------------------------
output_dir = os.path.join(os.path.dirname(__file__), "../output")
os.makedirs(output_dir, exist_ok=True)

gif_path = os.path.join(output_dir, "v10_multi_agent_network.gif")
anim.save(gif_path, writer="pillow", fps=20)

print("Saved:", gif_path)
