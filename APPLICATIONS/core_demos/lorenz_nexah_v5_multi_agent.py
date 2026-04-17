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
# 2. Simulation parameters
# ============================

dt = 0.01
steps = 3000
noise_strength = 2.0

n_agents = 8  # 🔥 number of trajectories

# random initial states
agents = [np.random.randn(3) * 2 for _ in range(n_agents)]

trajectories = [[] for _ in range(n_agents)]
coherences = [[] for _ in range(n_agents)]


# ============================
# 3. Simulation loop
# ============================

for _ in range(steps):

    for i in range(n_agents):

        x = agents[i]

        dx = lorenz(x)
        noise = noise_strength * np.random.randn(3)
        dx_obs = dx + noise

        # coherence
        dx_field = lorenz(x)
        num = np.dot(dx_obs, dx_field)
        denom = np.linalg.norm(dx_obs) * np.linalg.norm(dx_field) + 1e-8
        c = num / denom

        # update
        x = x + dt * dx_obs

        agents[i] = x
        trajectories[i].append(x.copy())
        coherences[i].append(c)


# convert
trajectories = [np.array(traj) for traj in trajectories]
coherences = [np.array(c) for c in coherences]


# ============================
# 4. Visualization
# ============================

fig = plt.figure(figsize=(14, 6))

# --- Multi-agent trajectories ---
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

ax.set_title("V5: Multi-Agent Lorenz (Coherence)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")


# --- Mean coherence over agents ---
ax2 = fig.add_subplot(122)

mean_coherence = np.mean(np.array(coherences), axis=0)
ax2.plot(mean_coherence, color="cyan")

ax2.set_title("Mean Coherence (All Agents)")
ax2.set_xlabel("Step")
ax2.set_ylabel("C(x)")


plt.tight_layout()
plt.savefig("APPLICATIONS/core_demos/lorenz_nexah_v5_multi_agent.png", dpi=150)
plt.show()


# ============================
# 5. Output
# ============================

print("Agents:", n_agents)
print("Mean coherence:", np.mean(mean_coherence))
print("Min coherence:", np.min(mean_coherence))
