import numpy as np
import matplotlib.pyplot as plt

plt.style.use("dark_background")

# ============================
# 1. Lorenz
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
# 2. Coherence + Risk
# ============================

def coherence(x, dx_obs):
    dx_field = lorenz(x)
    num = np.dot(dx_obs, dx_field)
    denom = np.linalg.norm(dx_obs) * np.linalg.norm(dx_field) + 1e-8
    return num / denom

def risk(x, dx_obs):
    return 1 - coherence(x, dx_obs)


def grad_risk(x, dx_obs, eps=1e-3):
    g = np.zeros(3)

    for i in range(3):
        dx = np.zeros(3)
        dx[i] = eps

        r1 = risk(x + dx, dx_obs)
        r2 = risk(x - dx, dx_obs)

        g[i] = (r1 - r2) / (2 * eps)

    return g


# ============================
# 3. Simulation
# ============================

dt = 0.01
steps = 3000

noise_strength = 2.0
risk_strength = 0.4  # 🔥 key

n_agents = 8

agents = [np.random.randn(3) * 2 for _ in range(n_agents)]

trajectories = [[] for _ in range(n_agents)]
coherences = [[] for _ in range(n_agents)]
risks = [[] for _ in range(n_agents)]


for _ in range(steps):

    new_agents = []

    for i in range(n_agents):

        x = agents[i]

        dx = lorenz(x)
        noise = noise_strength * np.random.randn(3)

        dx_obs = dx + noise

        # 🔥 Risk-aware navigation
        g = grad_risk(x, dx_obs)
        control = -risk_strength * g

        dx_total = dx_obs + control

        c = coherence(x, dx_total)
        r = 1 - c

        x_new = x + dt * dx_total

        new_agents.append(x_new)
        trajectories[i].append(x_new.copy())
        coherences[i].append(c)
        risks[i].append(r)

    agents = new_agents


# ============================
# 4. Convert
# ============================

trajectories = [np.array(t) for t in trajectories]
coherences = [np.array(c) for c in coherences]
risks = [np.array(r) for r in risks]

mean_coh = np.mean(np.array(coherences), axis=0)
mean_risk = np.mean(np.array(risks), axis=0)


# ============================
# 5. Plot
# ============================

fig = plt.figure(figsize=(14,6))

# --- trajectories
ax1 = fig.add_subplot(121, projection='3d')

for i in range(n_agents):
    traj = trajectories[i]
    coh = coherences[i]

    for j in range(len(traj)-1):
        color = plt.cm.viridis((coh[j]+1)/2)
        ax1.plot(
            traj[j:j+2,0],
            traj[j:j+2,1],
            traj[j:j+2,2],
            color=color,
            linewidth=0.8
        )

ax1.set_title("V10: Risk-Aware Navigation")


# --- metrics
ax2 = fig.add_subplot(122)
ax2.plot(mean_coh, label="Coherence")
ax2.plot(mean_risk, label="Risk")

ax2.legend()
ax2.set_title("Coherence vs Risk")

plt.tight_layout()
plt.savefig("APPLICATIONS/core_demos/lorenz_nexah_v10_risk_navigation.png", dpi=150)
plt.show()


# ============================
# 6. Output
# ============================

print("Mean coherence:", np.mean(mean_coh))
print("Min coherence:", np.min(mean_coh))
print("Mean risk:", np.mean(mean_risk))
