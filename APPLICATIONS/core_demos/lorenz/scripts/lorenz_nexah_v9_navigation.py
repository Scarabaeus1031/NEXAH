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
coupling_strength = 0.08
distance_threshold = 6.0

navigation_strength = 0.15  # 🔥 NEW

# 🎯 Ziel (low-risk region approx)
target = np.array([0.0, 0.0, 25.0])

agents = [np.random.randn(3) * 2 for _ in range(n_agents)]

trajectories = [[] for _ in range(n_agents)]
coherences = [[] for _ in range(n_agents)]
distances = [[] for _ in range(n_agents)]


# ============================
# 3. Dynamic Network
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
# 4. Simulation
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

        # 🔥 NAVIGATION TERM
        nav = navigation_strength * (target - x)

        dx_total = dx_obs + interaction + nav

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

        # distance to target
        distances[i].append(np.linalg.norm(x_new - target))

    agents = new_agents


# ============================
# 5. Convert
# ============================

trajectories = [np.array(t) for t in trajectories]
coherences = [np.array(c) for c in coherences]
distances = [np.array(d) for d in distances]

mean_coherence = np.mean(np.array(coherences), axis=0)
mean_distance = np.mean(np.array(distances), axis=0)


# ============================
# 6. Visualization
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

# target markieren
ax1.scatter(target[0], target[1], target[2], color="red", s=100)

ax1.set_title("V9: Navigation in State Space")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("Z")


# --- Coherence ---
ax2 = fig.add_subplot(132)
ax2.plot(mean_coherence, color="cyan")
ax2.set_title("Mean Coherence")
ax2.set_xlabel("Step")


# --- Distance to target ---
ax3 = fig.add_subplot(133)
ax3.plot(mean_distance, color="orange")
ax3.set_title("Distance to Target")
ax3.set_xlabel("Step")

plt.tight_layout()
plt.savefig("APPLICATIONS/core_demos/lorenz_nexah_v9_navigation.png", dpi=150)
plt.show()


# ============================
# 7. Output
# ============================

print("Agents:", n_agents)
print("Navigation strength:", navigation_strength)
print("Mean coherence:", np.mean(mean_coherence))
print("Final distance:", mean_distance[-1])
