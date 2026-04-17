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
# 2. Risk + Gradient
# ============================

def compute_coherence(x, dx_obs):
    dx_field = lorenz(x)
    num = np.dot(dx_obs, dx_field)
    denom = np.linalg.norm(dx_obs) * np.linalg.norm(dx_field) + 1e-8
    return num / denom

def compute_risk(x, dx_obs):
    return 1 - compute_coherence(x, dx_obs)

def grad_risk(x, dx_obs, eps=1e-3):
    grad = np.zeros(3)
    for i in range(3):
        dx = np.zeros(3)
        dx[i] = eps

        r1 = compute_risk(x + dx, dx_obs)
        r2 = compute_risk(x - dx, dx_obs)

        grad[i] = (r1 - r2) / (2 * eps)
    return grad


# ============================
# 3. Simulation (NOISE + CONTROL)
# ============================

dt = 0.01
steps = 4000
noise_strength = 2.0
control_strength = 0.5  # 🔥 V4

x = np.array([1.0, 1.0, 1.0])

trajectory = []
coherence = []
risk = []

for _ in range(steps):

    dx = lorenz(x)
    noise = noise_strength * np.random.randn(3)

    # observed motion (with noise)
    dx_obs = dx + noise

    # compute metrics BEFORE update
    c = compute_coherence(x, dx_obs)
    r = 1 - c

    # 🔥 CONTROL: push against risk gradient
    g = grad_risk(x, dx_obs)
    u = -control_strength * g

    # update system
    x = x + dt * (dx_obs + u)

    trajectory.append(x.copy())
    coherence.append(c)
    risk.append(r)

trajectory = np.array(trajectory)
coherence = np.array(coherence)
risk = np.array(risk)


# ============================
# 4. 2D Risk Field Projection (V3)
# ============================

grid_size = 80
x_vals = np.linspace(-20, 20, grid_size)
y_vals = np.linspace(-30, 30, grid_size)

X, Y = np.meshgrid(x_vals, y_vals)
R_field = np.zeros_like(X)

z_fixed = 25  # projection slice

for i in range(grid_size):
    for j in range(grid_size):
        point = np.array([X[i, j], Y[i, j], z_fixed])
        dx = lorenz(point)
        R_field[i, j] = 1 - compute_coherence(point, dx)


# ============================
# 5. Visualization
# ============================

fig = plt.figure(figsize=(14, 6))

# --- V3: Risk Field ---
ax1 = fig.add_subplot(121)

cf = ax1.contourf(X, Y, R_field, levels=30, cmap="inferno")
plt.colorbar(cf, ax=ax1, label="Risk")

# project trajectory to XY
ax1.plot(trajectory[:,0], trajectory[:,1], color="cyan", linewidth=1)

ax1.set_title("V3: Risk Field (XY Projection)")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")


# --- V4: Coherence + Risk over time ---
ax2 = fig.add_subplot(122)

ax2.plot(coherence, label="Coherence")
ax2.plot(risk, label="Risk")

ax2.set_title("V4: Dynamics (with Control)")
ax2.set_xlabel("Step")
ax2.legend()


plt.tight_layout()
plt.savefig("APPLICATIONS/core_demos/lorenz_nexah_v3_v4.png", dpi=150)
plt.show()


# ============================
# 6. Output
# ============================

print("Mean coherence:", np.mean(coherence))
print("Min coherence:", np.min(coherence))
print("Mean risk:", np.mean(risk))
print("Max risk:", np.max(risk))
