import numpy as np
import matplotlib.pyplot as plt
import os

# ----------------------------
# 1. Vector field
# ----------------------------
def F(x, y):
    return np.array([y, -x - 0.3*y])  # stabiler Spiral-Attraktor


# ----------------------------
# 2. Coherence
# ----------------------------
def coherence(v, f):
    denom = np.linalg.norm(v) * np.linalg.norm(f)
    if denom < 1e-8:
        return 1.0
    return np.dot(v, f) / denom


# ----------------------------
# 3. Simulation
# ----------------------------
dt = 0.05
steps = 200

x = np.array([-2.0, -1.5])
trajectory = []
coherences = []

for _ in range(steps):
    trajectory.append(x.copy())

    field = F(x[0], x[1])

    # 🔥 Noise → echte Dynamik
    noise = np.random.normal(0, 0.3, size=2)

    velocity = field + noise

    c = coherence(velocity, field)
    coherences.append(c)

    # 🔥 einfache Control
    if c < 0.3:
        u = np.array([0.0, 0.8])
    else:
        u = np.array([0.0, 0.0])

    x = x + dt * (velocity + u)

trajectory = np.array(trajectory)
coherences = np.array(coherences)

# ----------------------------
# 4. Output Folder
# ----------------------------
output_dir = os.path.join(os.path.dirname(__file__), "../output")
os.makedirs(output_dir, exist_ok=True)

# ----------------------------
# 5. Trajectory Plot (FARBE!)
# ----------------------------
fig, ax = plt.subplots()

for i in range(len(trajectory) - 1):
    ax.plot(
        trajectory[i:i+2, 0],
        trajectory[i:i+2, 1],
        color=plt.cm.viridis(coherences[i])
    )

# Startpunkt
ax.scatter(trajectory[0, 0], trajectory[0, 1], color="red", label="start")

ax.set_title("NEXAH V5: Trajectory colored by Coherence")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_aspect('equal', adjustable='box')

# 🔥 Colorbar FIX
sm = plt.cm.ScalarMappable(cmap='viridis')
sm.set_array(coherences)
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label("Coherence")

ax.legend()

traj_path = os.path.join(output_dir, "v5_colored_trajectory.png")
plt.savefig(traj_path)
print("Saved:", traj_path)

plt.close()

# ----------------------------
# 6. Coherence Plot
# ----------------------------
plt.figure()
plt.plot(coherences)

plt.title("Coherence over Time")
plt.xlabel("step")
plt.ylabel("C(x)")

coh_path = os.path.join(output_dir, "v5_coherence.png")
plt.savefig(coh_path)
print("Saved:", coh_path)

plt.close()
