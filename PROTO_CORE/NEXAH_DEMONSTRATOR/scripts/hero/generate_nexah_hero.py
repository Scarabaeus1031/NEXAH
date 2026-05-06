import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# -----------------------------
# 1. Generate Lorenz Trajectories
# -----------------------------
def lorenz(x, y, z, s=10, r=28, b=2.667):
    dx = s * (y - x)
    dy = x * (r - z) - y
    dz = x * y - b * z
    return dx, dy, dz

dt = 0.01
num_steps = 10000

xs = np.empty(num_steps)
ys = np.empty(num_steps)
zs = np.empty(num_steps)

xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

for i in range(num_steps - 1):
    dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
    xs[i + 1] = xs[i] + dx * dt
    ys[i + 1] = ys[i] + dy * dt
    zs[i + 1] = zs[i] + dz * dt

# Project to 2D
points = np.vstack([xs, ys])

# -----------------------------
# 2. Density Estimation
# -----------------------------
kde = gaussian_kde(points)
xmin, xmax = xs.min(), xs.max()
ymin, ymax = ys.min(), ys.max()

X, Y = np.mgrid[xmin:xmax:300j, ymin:ymax:300j]
positions = np.vstack([X.ravel(), Y.ravel()])
Z = np.reshape(kde(positions).T, X.shape)

# -----------------------------
# 3. Create Figure
# -----------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# -----------------------------
# LEFT: Trajectories
# -----------------------------
axes[0].plot(xs, ys, lw=0.5, color='blue', alpha=0.6)
axes[0].set_title("Raw Dynamics\n(Trajectories)")
axes[0].set_xticks([])
axes[0].set_yticks([])

# -----------------------------
# CENTER: Density Field
# -----------------------------
axes[1].imshow(np.rot90(Z), cmap='viridis',
               extent=[xmin, xmax, ymin, ymax])
axes[1].set_title("Emergent Structure\n(Density Field)")
axes[1].set_xticks([])
axes[1].set_yticks([])

# -----------------------------
# RIGHT: Structured Field + Path
# -----------------------------
axes[2].imshow(np.rot90(Z), cmap='viridis',
               extent=[xmin, xmax, ymin, ymax], alpha=0.7)

# overlay trajectory (highlighted)
axes[2].plot(xs, ys, color='white', lw=1.0)

# simple "gate" marker (low-density region)
gate_x, gate_y = xs[3000], ys[3000]
axes[2].scatter(gate_x, gate_y, color='red', s=50, label='Transition Region')

axes[2].set_title("Structured Field\n+ Navigation Path")
axes[2].set_xticks([])
axes[2].set_yticks([])
axes[2].legend(loc="upper right")

# -----------------------------
# Global Title
# -----------------------------
fig.suptitle(
    "NEXAH — From Dynamics to Structure to Navigation",
    fontsize=14
)

plt.tight_layout()

# -----------------------------
# Save
# -----------------------------
plt.savefig(
    "NEXAH_DEMONSTRATOR/visuals/nexah_hero_structure_pipeline_v1.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()
