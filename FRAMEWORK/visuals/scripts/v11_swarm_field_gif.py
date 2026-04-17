import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# ----------------------------
# Vector field
# ----------------------------
def F(x, y):
    return np.array([
        y + 0.2 * x,
        -x - 0.3 * y + 0.05 * np.tanh(x)
    ])

# ----------------------------
# Risk
# ----------------------------
def compute_risk(x):
    r = np.linalg.norm(x)
    base = np.tanh(r / 2.0)

    fx, fy = F(x[0], x[1])
    curvature = np.tanh(abs(fx * fy))

    return np.clip(0.7 * base + 0.3 * curvature, 0, 1)

# ----------------------------
# Gradient
# ----------------------------
def grad_risk(x, eps=1e-3):
    dx = np.array([eps, 0])
    dy = np.array([0, eps])

    dRx = (compute_risk(x + dx) - compute_risk(x - dx)) / (2 * eps)
    dRy = (compute_risk(x + dy) - compute_risk(x - dy)) / (2 * eps)

    return np.array([dRx, dRy])

# ----------------------------
# Swarm Forces
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

        # ----------------------------
        # Repulsion (strong at short distance)
        # ----------------------------
        if dist < 1.0:
            repulsion += diff / dist**2

        # ----------------------------
        # Attraction (weak at long distance)
        # ----------------------------
        if dist > 1.5 and dist < 3.0:
            attraction += -diff * 0.05

    return repulsion * 0.6 + attraction

# ----------------------------
# Field grid
# ----------------------------
def build_field():
    X, Y = np.meshgrid(np.linspace(-3, 3, 120), np.linspace(-3, 3, 120))
    R = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            R[i, j] = compute_risk(np.array([X[i, j], Y[i, j]]))

    return X, Y, R

X, Y, R = build_field()

# ----------------------------
# Agents
# ----------------------------
np.random.seed(2)

agents = np.array([
    [-2.2, -1.5],
    [-1.8,  1.8],
    [ 2.0,  1.6],
    [ 2.2, -1.6],
    [-0.4,  2.2],
    [ 0.7, -2.2],
])

n_agents = len(agents)
trajectories = [[] for _ in range(n_agents)]

dt = 0.05

# ----------------------------
# Plot setup
# ----------------------------
fig, ax = plt.subplots(figsize=(6, 6))
ax.contourf(X, Y, R, levels=50, cmap="plasma")

colors = plt.cm.tab10(np.linspace(0, 1, n_agents))
lines = [ax.plot([], [], color=colors[i])[0] for i in range(n_agents)]
points = [ax.plot([], [], 'o', color=colors[i])[0] for i in range(n_agents)]

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_title("NEXAH V11 – Swarm + Field Dynamics")
ax.set_aspect("equal")

# ----------------------------
# Animation step
# ----------------------------
def update(frame):
    global agents

    new_agents = agents.copy()

    for i in range(n_agents):
        x = agents[i]

        f = F(x[0], x[1])
        noise = np.random.normal(0, 0.05, 2)

        # Field control
        g = grad_risk(x)
        u_field = -0.8 * g

        # Swarm interaction
        u_swarm = swarm_forces(i, agents)

        # Total update
        x_next = x + dt * (f + u_field + u_swarm + noise)

        # Prevent explosion
        if np.linalg.norm(x_next) > 4:
            x_next = x_next / np.linalg.norm(x_next) * 4

        new_agents[i] = x_next
        trajectories[i].append(x_next)

    agents = new_agents

    # Update visuals
    for i in range(n_agents):
        traj = np.array(trajectories[i])

        if len(traj) > 1:
            lines[i].set_data(traj[:, 0], traj[:, 1])
            points[i].set_data([traj[-1, 0]], [traj[-1, 1]])

    return lines + points

# ----------------------------
# Run animation
# ----------------------------
anim = FuncAnimation(fig, update, frames=180, interval=50)

# ----------------------------
# Save GIF
# ----------------------------
output_dir = os.path.join(os.path.dirname(__file__), "../output")
os.makedirs(output_dir, exist_ok=True)

gif_path = os.path.join(output_dir, "v11_swarm_field.gif")
anim.save(gif_path, writer="pillow", fps=20)

print("Saved:", gif_path)
