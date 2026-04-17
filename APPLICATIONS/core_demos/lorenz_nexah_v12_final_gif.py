import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use("dark_background")

# ============================
# Lorenz
# ============================

sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

def lorenz(x):
    return np.array([
        sigma * (x[1] - x[0]),
        x[0] * (rho - x[2]) - x[1],
        x[0] * x[1] - beta * x[2]
    ])

def coherence(x, dx):
    dx_field = lorenz(x)
    num = np.dot(dx, dx_field)
    denom = np.linalg.norm(dx) * np.linalg.norm(dx_field) + 1e-8
    return num / denom

def risk(x, dx):
    return 1 - coherence(x, dx)

def grad_risk(x, dx, eps=1e-3):
    g = np.zeros(3)
    for i in range(3):
        shift = np.zeros(3)
        shift[i] = eps
        r1 = risk(x + shift, dx)
        r2 = risk(x - shift, dx)
        g[i] = (r1 - r2) / (2 * eps)
    return g


# ============================
# Parameters
# ============================

dt = 0.01
steps = 1500  # kürzer für GIF

noise_strength = 2.0
coupling_strength = 0.06
risk_strength = 0.35
distance_threshold = 6.0

n_agents = 8
agents = [np.random.randn(3) * 2 for _ in range(n_agents)]

trajectories = [[] for _ in range(n_agents)]
coherences = [[] for _ in range(n_agents)]


# ============================
# Network
# ============================

def dynamic_neighbors(states, threshold):
    neighbors = {i: [] for i in range(len(states))}
    for i in range(len(states)):
        for j in range(len(states)):
            if i == j:
                continue
            if np.linalg.norm(states[i] - states[j]) < threshold:
                neighbors[i].append(j)
    return neighbors


# ============================
# Simulation
# ============================

for _ in range(steps):

    neighbors = dynamic_neighbors(agents, distance_threshold)
    new_agents = []

    for i in range(n_agents):

        x = agents[i]

        dx = lorenz(x)
        noise = noise_strength * np.random.randn(3)
        dx_obs = dx + noise

        # interaction
        if neighbors[i]:
            mean_neighbor = np.mean([agents[j] for j in neighbors[i]], axis=0)
            interaction = coupling_strength * (mean_neighbor - x)
        else:
            interaction = 0

        # risk navigation
        g = grad_risk(x, dx_obs)
        control = -risk_strength * g

        dx_total = dx_obs + interaction + control

        c = coherence(x, dx_total)

        x_new = x + dt * dx_total

        new_agents.append(x_new)
        trajectories[i].append(x_new.copy())
        coherences[i].append(c)

    agents = new_agents


trajectories = [np.array(t) for t in trajectories]
coherences = [np.array(c) for c in coherences]


# ============================
# Animation
# ============================

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')

lines = [ax.plot([], [], [], lw=1)[0] for _ in range(n_agents)]

ax.set_xlim(-20, 20)
ax.set_ylim(-30, 30)
ax.set_zlim(0, 50)
ax.set_title("NEXAH V12 — Field Navigation")

def update(frame):

    for i in range(n_agents):
        traj = trajectories[i][:frame]
        coh = coherences[i][:frame]

        if len(traj) > 1:
            lines[i].set_data(traj[:,0], traj[:,1])
            lines[i].set_3d_properties(traj[:,2])

            color = plt.cm.viridis((coh[-1]+1)/2)
            lines[i].set_color(color)

    return lines

anim = FuncAnimation(fig, update, frames=steps, interval=20)

anim.save(
    "APPLICATIONS/core_demos/lorenz_nexah_v12_final.gif",
    writer="pillow",
    fps=20
)

plt.close()
