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

def coherence(x, dx_obs):
    dx_field = lorenz(x)
    num = np.dot(dx_obs, dx_field)
    denom = np.linalg.norm(dx_obs) * np.linalg.norm(dx_field) + 1e-8
    return num / denom

def risk(x, dx_obs):
    return 1 - coherence(x, dx_obs)


# ============================
# 3. Parameters
# ============================

dt = 0.01
steps = 2500   # 🔧 etwas reduziert für Stabilität

noise_strength = 2.0
coupling_strength = 0.06
goal_strength = 0.08
distance_threshold = 6.0

n_agents = 8
agents = [np.random.randn(3) * 2 for _ in range(n_agents)]

trajectories = [[] for _ in range(n_agents)]
coherences = [[] for _ in range(n_agents)]
risks = [[] for _ in range(n_agents)]
goal_history = []


# ============================
# 4. Dynamic neighbors
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
# 5. Emergent Goal (robust)
# ============================

def emergent_goal(states, local_risks, local_coherences):

    weights = []

    for r, c in zip(local_risks, local_coherences):
        # 🔧 stabilisierte Gewichtung
        w = max(c, 0.0) * max(1 - r, 0.0)
        weights.append(w)

    weights = np.array(weights)

    # fallback falls degeneriert
    if np.sum(weights) < 1e-6:
        return np.mean(states, axis=0)

    weights = weights / np.sum(weights)

    goal = np.zeros(3)
    for w, s in zip(weights, states):
        goal += w * s

    return goal


# ============================
# 6. Simulation
# ============================

for _ in range(steps):

    neighbors = dynamic_neighbors(agents, distance_threshold)

    # --- Pre-pass für Goal ---
    current_coh = []
    current_risk = []

    for i in range(n_agents):
        x = agents[i]
        dx = lorenz(x)
        noise = noise_strength * np.random.randn(3)
        dx_obs = dx + noise

        c = coherence(x, dx_obs)
        r = 1 - c

        current_coh.append(c)
        current_risk.append(r)

    current_coh = np.array(current_coh)
    current_risk = np.array(current_risk)

    # 🔥 emergent goal
    goal = emergent_goal(agents, current_risk, current_coh)
    goal_history.append(goal.copy())

    new_agents = []

    for i in range(n_agents):

        x = agents[i]

        dx = lorenz(x)
        noise = noise_strength * np.random.randn(3)
        dx_obs = dx + noise

        # --- Netzwerk ---
        if len(neighbors[i]) > 0:
            neighbor_states = [agents[j] for j in neighbors[i]]
            mean_neighbor = np.mean(neighbor_states, axis=0)
            interaction = coupling_strength * (mean_neighbor - x)
        else:
            interaction = np.zeros(3)

        # --- emergent navigation ---
        nav = goal_strength * (goal - x)

        dx_total = dx_obs + interaction + nav

        c = coherence(x, dx_total)
        r = 1 - c

        x_new = x + dt * dx_total

        new_agents.append(x_new)
        trajectories[i].append(x_new.copy())
        coherences[i].append(c)
        risks[i].append(r)

    agents = new_agents


# ============================
# 7. Convert
# ============================

trajectories = [np.array(t) for t in trajectories]
coherences = [np.array(c) for c in coherences]
risks = [np.array(r) for r in risks]
goal_history = np.array(goal_history)

mean_coh = np.mean(np.array(coherences), axis=0)
mean_risk = np.mean(np.array(risks), axis=0)


# ============================
# 8. Visualization
# ============================

fig = plt.figure(figsize=(16, 6))

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

# emergent goal path
ax1.plot(
    goal_history[:, 0],
    goal_history[:, 1],
    goal_history[:, 2],
    color="red",
    linewidth=2,
    label="Emergent goal"
)

ax1.set_title("V11: Emergent Goal")
ax1.legend()


# --- Coherence ---
ax2 = fig.add_subplot(132)
ax2.plot(mean_coh, color="cyan")
ax2.set_title("Mean Coherence")


# --- Risk ---
ax3 = fig.add_subplot(133)
ax3.plot(mean_risk, color="orange")
ax3.set_title("Mean Risk")


plt.tight_layout()
plt.savefig("APPLICATIONS/core_demos/lorenz_nexah_v11_emergent_goal.png", dpi=150)
plt.show()


# ============================
# 9. Output
# ============================

print("Mean coherence:", np.mean(mean_coh))
print("Min coherence:", np.min(mean_coh))
print("Mean risk:", np.mean(mean_risk))
