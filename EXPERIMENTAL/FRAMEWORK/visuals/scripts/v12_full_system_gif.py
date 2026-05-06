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
# 3. Gradient
# ----------------------------
def grad_risk(x, eps=1e-3):
    dx = np.array([eps, 0])
    dy = np.array([0, eps])

    dRx = (compute_risk(x + dx) - compute_risk(x - dx)) / (2 * eps)
    dRy = (compute_risk(x + dy) - compute_risk(x - dy)) / (2 * eps)

    return np.array([dRx, dRy])

# ----------------------------
# 4. Swarm forces
# ----------------------------
def swarm_forces(i, agents):
    xi = agents[i]
    repulsion = np.zeros(2)
    attraction = np.zeros(2)

    for j in range(len(agents)):
        if i == j:
            continue

        xj = agents[j]
        diff = xi - xj
        dist = np.linalg.norm(diff) + 1e-6

        # repulsion (short range)
        if dist < 0.9:
            repulsion += diff / dist**2

        # attraction (mid range)
        if 1.4 < dist < 2.5:
            attraction += -0.04 * diff

    return 0.6 * repulsion + attraction

# ----------------------------
# 5. Communication
# ----------------------------
def communication_force(i, agents, risks, threshold=1.3):
    xi = agents[i]
    ri = risks[i]

    force = np.zeros(2)
    count = 0

    for j in range(len(agents)):
        if i == j:
            continue

        xj = agents[j]
        rj = risks[j]

        dist = np.linalg.norm(xj - xi)

        if dist < threshold:
            if rj < ri:  # only follow better agents
                force += (xj - xi)
                count += 1

    if count > 0:
        force = force / count

    return 0.2 * force

# ----------------------------
# 6. Field grid
# ----------------------------
def build_field():
    X, Y = np.meshgrid(np.linspace(-3, 3, 120), np.linspace(-3, 3, 120))
    R = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            R[i, j] = compute_risk(np.array([X[i, j], Y[i, j]]))

    return X, Y, R

# ----------------------------
# 7. Build edges
# ----------------------------
def build_edges(points, threshold=1.3):
    edges = []
    n = len(points)

    for i in range(n):
        for j in range(i + 1, n):
            if np.linalg.norm(points[i] - points[j]) < threshold:
                edges.append((i, j))
    return edges

# ----------------------------
# INIT
# ----------------------------
np.random.seed(4)

agents = np.array([
    [-2.2, -1.5],
    [-1.8,  1.8],
    [ 2.0,  1.6],
    [ 2.2, -1.6],
    [-0.4,  2.2],
    [ 0.7, -2.2],
    [-2.5,  0.3],
    [ 2.4,  0.1],
], dtype=float)

n_agents = len(agents)
trajectories = [[] for _ in range(n_agents)]

dt = 0.05

X, Y, R = build_field()

# ----------------------------
# Plot
# ----------------------------
fig, ax = plt.subplots(figsize=(6, 6))
ax.contourf(X, Y, R, levels=50, cmap="plasma")

colors = plt.cm.tab10(np.linspace(0, 1, n_agents))

lines = [ax.plot([], [], color=colors[i], lw=1.8)[0] for i in range(n_agents)]
points = [ax.plot([], [], "o", color=colors[i])[0] for i in range(n_agents)]

edge_lines = []

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_title("NEXAH V12 – Full System")
ax.set_aspect("equal")

# ----------------------------
# UPDATE
# ----------------------------
def update(frame):
    global agents, edge_lines

    for l in edge_lines:
        l.remove()
    edge_lines = []

    risks = np.array([compute_risk(a) for a in agents])
    new_agents = agents.copy()

    for i in range(n_agents):
        x = agents[i]

        f = F(x[0], x[1])
        noise = np.random.normal(0, 0.04, 2)

        u_field = -0.8 * grad_risk(x)
        u_swarm = swarm_forces(i, agents)
        u_comm = communication_force(i, agents, risks)

        x_next = x + dt * (f + u_field + u_swarm + u_comm + noise)

        # clip
        norm_x = np.linalg.norm(x_next)
        if norm_x > 4:
            x_next = x_next / norm_x * 4

        new_agents[i] = x_next
        trajectories[i].append(x_next)

    agents = new_agents

    # update visuals
    for i in range(n_agents):
        traj = np.array(trajectories[i])
        if len(traj) > 1:
            lines[i].set_data(traj[:, 0], traj[:, 1])
            points[i].set_data([traj[-1, 0]], [traj[-1, 1]])

    # network
    edges = build_edges(agents)

    for i, j in edges:
        ln, = ax.plot(
            [agents[i, 0], agents[j, 0]],
            [agents[i, 1], agents[j, 1]],
            color="cyan",
            alpha=0.4,
            lw=1.2
        )
        edge_lines.append(ln)

    return lines + points + edge_lines

# ----------------------------
# ANIMATION
# ----------------------------
anim = FuncAnimation(fig, update, frames=180, interval=50)

# ----------------------------
# SAVE
# ----------------------------
output_dir = os.path.join(os.path.dirname(__file__), "../output")
os.makedirs(output_dir, exist_ok=True)

gif_path = os.path.join(output_dir, "v12_full_system.gif")
anim.save(gif_path, writer="pillow", fps=20)

print("Saved:", gif_path)
