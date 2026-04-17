import numpy as np
import matplotlib.pyplot as plt

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
# 2. Simulate trajectory
# ============================

dt = 0.01
steps = 4000

x = np.array([1.0, 1.0, 1.0])
trajectory = []

for _ in range(steps):
    trajectory.append(x.copy())
    dx = lorenz(x)
    x = x + dt * dx

trajectory = np.array(trajectory)


# ============================
# 3. Compute coherence
# ============================

coherence = []

for i in range(len(trajectory) - 1):
    x = trajectory[i]
    x_next = trajectory[i + 1]

    # observed movement
    dx_obs = (x_next - x) / dt

    # field prediction
    dx_field = lorenz(x)

    # coherence
    num = np.dot(dx_obs, dx_field)
    denom = np.linalg.norm(dx_obs) * np.linalg.norm(dx_field) + 1e-8

    c = num / denom
    coherence.append(c)

coherence = np.array(coherence)


# ============================
# 4. Risk
# ============================

risk = 1 - coherence


# ============================
# 5. Visualization
# ============================

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

fig = plt.figure(figsize=(12, 5))

# --- Trajectory colored by coherence ---
ax = fig.add_subplot(121, projection='3d')

for i in range(len(trajectory) - 1):
    color = plt.cm.viridis((coherence[i] + 1) / 2)
    ax.plot(
        trajectory[i:i+2, 0],
        trajectory[i:i+2, 1],
        trajectory[i:i+2, 2],
        color=color
    )

ax.set_title("Lorenz Attractor (colored by Coherence)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")


# --- Coherence over time ---
ax2 = fig.add_subplot(122)

ax2.plot(coherence)
ax2.set_title("Coherence over Time")
ax2.set_xlabel("Step")
ax2.set_ylabel("C(x)")

plt.tight_layout()
plt.show()


# ============================
# 5. Visualization
# ============================

plt.tight_layout()
plt.style.use("dark_background")
plt.savefig("APPLICATIONS/core_demos/lorenz_nexah_coherence.png", dpi=150)

plt.show()


# ============================
# 6. Print insight
# ============================

print("Mean coherence:", np.mean(coherence))
print("Min coherence:", np.min(coherence))
print("Max coherence:", np.max(coherence))
