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
    dx = sigma * (x[1] - x[0])
    dy = x[0] * (rho - x[2]) - x[1]
    dz = x[0] * x[1] - beta * x[2]
    return np.array([dx, dy, dz])


# ============================
# 2. Parameters
# ============================

dt = 0.01
steps = 3000
noise_strength = 2.0

n_agents = 8
coupling_strength = 0.08  # etwas stärker als V6

# 🔗 Netzwerk (Adjacency List)
neighbors = {
    0: [1, 3],
    1: [0, 2],
    2: [1, 5],
    3: [0, 4],
    4: [3, 5, 6],
    5: [2, 4],
    6: [4, 7],
    7: [6]
}

agents = [np.random.randn(3) * 2 for _ in range(n_agents)]

trajectories = [[] for _ in range(n_agents)]
coherences = [[] for _ in range(n_agents)]


# ============================
# 3. Simulation
# ============================

for _ in range(steps):

    new_agents = []

    for i in range(n_agents):

        x = agents[i]

        dx = lorenz(x)
        noise = noise_strength * np.random.randn(3)
        dx_obs = dx + noise

        # 🔥 Netzwerk-Interaktion
        neighbor_states = [agents[j] for j in neighbors[i]]
        mean_neighbor = np.mean(neighbor_states, axis=0)

        interaction = coupling_strength * (mean_neighbor - x)

        dx_total = dx_obs + interaction

        # coherence
        dx_field = lorenz(x)
        num = np.dot(dx_total, dx_field)
        denom = np.linalg.norm(dx_total) * np.linalg.norm(dx_field) + 1e-8
        c = num / denom

        # update
        x_new = x + dt * dx_total

        new_agents.append(x_new)
        trajectories[i].append(x_new.copy())
        coherences[i].append(c)

    agents = new_agents


# convert
trajectories = [np.array(traj) for traj in trajectories]
coherences = [np.array(c) for c in coherences]


# ============================
# 4. Visualization
# ============================

fig = plt.figure(figsize=(14, 6))

# --- Trajectories ---
ax = fig.add_subplot(121, projection='3d')

for i in range(n_agents):
    traj = trajectories[i]
    coh = coherences[i]

    for j in range(len(traj) - 1):
        color = plt.cm.viridis((coh[j] + 1) / 2)
        ax.plot(
            traj[j:j+2, 0],
            traj[j:j+2, 1],
            traj[j:j+2, 2],
            color=color,
            linewidth=0.8
        )

ax.set_title("V7: Network-Coupled Lorenz")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")


# --- Mean coherence ---
ax2 = fig.add_subplot(122)

mean_coherence = np.mean(np.array(coherences), axis=0)
ax2.plot(mean_coherence, color="cyan")

ax2.set_title("Mean Coherence (Network)")
ax2.set_xlabel("Step")
ax2.set_ylabel("C(x)")


plt.tight_layout()
plt.savefig("APPLICATIONS/core_demos/lorenz_nexah_v7_network.png", dpi=150)
plt.show()


# ============================
# 5. Output
# ============================

print("Agents:", n_agents)
print("Coupling:", coupling_strength)
print("Mean coherence:", np.mean(mean_coherence))
print("Min coherence:", np.min(mean_coherence))
