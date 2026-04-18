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
coupling_strength = 0.10
distance_threshold = 8.0  # 🔥 controls connectivity

agents = [np.random.randn(3) * 2 for _ in range(n_agents)]

trajectories = [[] for _ in range(n_agents)]
coherences = [[] for _ in range(n_agents)]
edge_counts = []


# ============================
# 3. Dynamic neighbors
# ============================

def dynamic_neighbors(agent_states, threshold):
    neighbors = {i: [] for i in range(len(agent_states))}

    for i in range(len(agent_states)):
        for j in range(len(agent_states)):
            if i == j:
                continue

            d = np.linalg.norm(agent_states[i] - agent_states[j])

            if d < threshold:
                neighbors[i].append(j)

    return neighbors


# ============================
# 4. Simulation
# ============================

for _ in range(steps):

    neighbors = dynamic_neighbors(agents, distance_threshold)

    # count edges
    total_edges = sum(len(v) for v in neighbors.values()) / 2
    edge_counts.append(total_edges)

    new_agents = []

    for i in range(n_agents):

        x = agents[i]

        dx = lorenz(x)
        noise = noise_strength * np.random.randn(3)
        dx_obs = dx + noise

        # 🔥 dynamic interaction
        if len(neighbors[i]) > 0:
            neighbor_states = [agents[j] for j in neighbors[i]]
            mean_neighbor = np.mean(neighbor_states, axis=0)

            interaction = coupling_strength * (mean_neighbor - x)
        else:
            interaction = np.zeros(3)

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
trajectories = [np.array(t) for t in trajectories]
coherences = [np.array(c) for c in coherences]
edge_counts = np.array(edge_counts)


# ============================
# 5. Visualization
# ============================

fig = plt.figure(figsize=(15, 6))

# --- Trajectories ---
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

ax1.set_title("V8: Dynamic Network Lorenz")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("Z")


# --- Mean coherence ---
ax2 = fig.add_subplot(132)

mean_coherence = np.mean(np.array(coherences), axis=0)
ax2.plot(mean_coherence, color="cyan")

ax2.set_title("Mean Coherence (Dynamic)")
ax2.set_xlabel("Step")
ax2.set_ylabel("C(x)")


# --- Edge count ---
ax3 = fig.add_subplot(133)

ax3.plot(edge_counts, color="orange")

ax3.set_title("Network Connectivity (Edges)")
ax3.set_xlabel("Step")
ax3.set_ylabel("Edges")


plt.tight_layout()
plt.savefig("APPLICATIONS/core_demos/lorenz_nexah_v8_dynamic_network.png", dpi=150)
plt.show()


# ============================
# 6. Output
# ============================

print("Agents:", n_agents)
print("Coupling:", coupling_strength)
print("Distance threshold:", distance_threshold)
print("Mean coherence:", np.mean(mean_coherence))
print("Min coherence:", np.min(mean_coherence))
print("Mean edges:", np.mean(edge_counts))
