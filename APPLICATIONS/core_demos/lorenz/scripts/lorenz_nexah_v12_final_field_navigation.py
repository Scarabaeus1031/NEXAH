import numpy as np
import matplotlib.pyplot as plt

plt.style.use("dark_background")

# ============================
# 1. Lorenz System
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


# ============================
# 2. Coherence / Risk
# ============================

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
# 3. Parameters
# ============================

dt = 0.01
steps = 2500

noise_strength = 2.0
coupling_strength = 0.06
risk_strength = 0.35   # 🔥 KEY

distance_threshold = 6.0
n_agents = 8

agents = [np.random.randn(3) * 2 for _ in range(n_agents)]

trajectories = [[] for _ in range(n_agents)]
coherences = [[] for _ in range(n_agents)]
risks = [[] for _ in range(n_agents)]


# ============================
# 4. Dynamic Network
# ============================

def dynamic_neighbors(states, threshold):
    neighbors = {i: [] for i in range(len(states))}

    for i in range(len(states)):
        for j in range(len(states)):
            if i == j:
                continue

            d = np.linalg.norm(states[i] - states[j])
            if d < threshold:
                neighbors[i].append(j)

    return neighbors


# ============================
# 5. Simulation
# ============================

for _ in range(steps):

    neighbors = dynamic_neighbors(agents, distance_threshold)
    new_agents = []

    for i in range(n_agents):

        x = agents[i]

        # base dynamics
        dx = lorenz(x)
        noise = noise_strength * np.random.randn(3)
        dx_obs = dx + noise

        # network interaction
        if len(neighbors[i]) > 0:
            neighbor_states = [agents[j] for j in neighbors[i]]
            mean_neighbor = np.mean(neighbor_states, axis=0)
            interaction = coupling_strength * (mean_neighbor - x)
        else:
            interaction = np.zeros(3)

        # 🔥 PURE FIELD NAVIGATION
        g = grad_risk(x, dx_obs)
        control = -risk_strength * g

        dx_total = dx_obs + interaction + control

        c = coherence(x, dx_total)
        r = 1 - c

        x_new = x + dt * dx_total

        new_agents.append(x_new)
        trajectories[i].append(x_new.copy())
        coherences[i].append(c)
        risks[i].append(r)

    agents = new_agents


# ============================
# 6. Convert
# ============================

trajectories = [np.array(t) for t in trajectories]
coherences = [np.array(c) for c in coherences]
risks = [np.array(r) for r in risks]

mean_coh = np.mean(np.array(coherences), axis=0)
mean_risk = np.mean(np.array(risks), axis=0)


# ============================
# 7. Visualization
# ============================

fig = plt.figure(figsize=(16, 6))

# --- 3D trajectories ---
ax1 = fig.add_subplot(131, projection='3d')

for i in range(n_agents):
    traj = trajectories[i]
    coh = coherences[i]

    for j in range(len(traj) - 1):
        color = plt.cm.viridis((coh[j] + 1) / 2)
        ax1.plot(
            traj[j:j+2, 0],
            traj[j:j+2, 1],
            traj[j:j+2, 2],
            color=color,
            linewidth=0.8
        )

ax1.set_title("V12: Field-Level Navigation")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("Z")


# --- Mean Coherence ---
ax2 = fig.add_subplot(132)
ax2.plot(mean_coh, color="cyan")
ax2.set_title("Mean Coherence")
ax2.set_xlabel("Step")


# --- Mean Risk ---
ax3 = fig.add_subplot(133)
ax3.plot(mean_risk, color="orange")
ax3.set_title("Mean Risk")
ax3.set_xlabel("Step")


plt.tight_layout()
plt.savefig("APPLICATIONS/core_demos/lorenz_nexah_v12_final.png", dpi=150)
plt.show()


# ============================
# 8. Output
# ============================

print("Agents:", n_agents)
print("Risk strength:", risk_strength)
print("Mean coherence:", np.mean(mean_coh))
print("Min coherence:", np.min(mean_coh))
print("Mean risk:", np.mean(mean_risk))
