import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# -----------------------------
# 1. Lorenz System
# -----------------------------
def lorenz(x, y, z, s=10, r=28, b=2.667):
    dx = s * (y - x)
    dy = x * (r - z) - y
    dz = x * y - b * z
    return dx, dy, dz

dt = 0.01
num_steps = 12000

xs = np.empty(num_steps)
ys = np.empty(num_steps)
zs = np.empty(num_steps)

xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

for i in range(num_steps - 1):
    dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
    xs[i + 1] = xs[i] + dx * dt
    ys[i + 1] = ys[i] + dy * dt
    zs[i + 1] = zs[i] + dz * dt

# velocity
vx = np.gradient(xs)
vy = np.gradient(ys)

# -----------------------------
# 2. Density Field
# -----------------------------
points = np.vstack([xs, ys])
kde = gaussian_kde(points)

xmin, xmax = xs.min(), xs.max()
ymin, ymax = ys.min(), ys.max()

X, Y = np.mgrid[xmin:xmax:250j, ymin:ymax:250j]
positions = np.vstack([X.ravel(), Y.ravel()])
Z = np.reshape(kde(positions).T, X.shape)

# -----------------------------
# 3. Field Gradient (Flow Proxy)
# -----------------------------
dZdx, dZdy = np.gradient(Z)

# normalize field
mag = np.sqrt(dZdx**2 + dZdy**2) + 1e-8
Fx = dZdx / mag
Fy = dZdy / mag

# -----------------------------
# 4. Coherence (alignment)
# -----------------------------
# interpolate field to trajectory points
def sample_field(x, y):
    xi = np.clip(((x - xmin) / (xmax - xmin) * (X.shape[0]-1)).astype(int), 0, X.shape[0]-1)
    yi = np.clip(((y - ymin) / (ymax - ymin) * (Y.shape[1]-1)).astype(int), 0, Y.shape[1]-1)
    return Fx[xi, yi], Fy[xi, yi]

Fx_traj, Fy_traj = sample_field(xs, ys)

vel_mag = np.sqrt(vx**2 + vy**2) + 1e-8
field_mag = np.sqrt(Fx_traj**2 + Fy_traj**2) + 1e-8

C = (vx * Fx_traj + vy * Fy_traj) / (vel_mag * field_mag)

# -----------------------------
# 5. Gate Detection
# -----------------------------
# low density + low coherence
density_threshold = np.percentile(Z, 20)
coherence_threshold = 0.2

gate_indices = np.where((C < coherence_threshold))[0]
gate_indices = gate_indices[::200]  # subsample

gate_x = xs[gate_indices]
gate_y = ys[gate_indices]

# -----------------------------
# 6. Plot
# -----------------------------
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# -----------------------------
# LEFT: Trajectories
# -----------------------------
axes[0].plot(xs, ys, lw=0.4, alpha=0.6)
axes[0].set_title("Raw Dynamics")
axes[0].set_xticks([])
axes[0].set_yticks([])

# -----------------------------
# CENTER: Density + Flow
# -----------------------------
axes[1].imshow(np.rot90(Z), extent=[xmin, xmax, ymin, ymax])
axes[1].quiver(
    X[::15, ::15],
    Y[::15, ::15],
    Fx[::15, ::15],
    Fy[::15, ::15],
    scale=30,
    alpha=0.6
)
axes[1].set_title("Emergent Field (Density + Flow)")
axes[1].set_xticks([])
axes[1].set_yticks([])

# -----------------------------
# RIGHT: Structure + Gates + Path
# -----------------------------
axes[2].imshow(np.rot90(Z), extent=[xmin, xmax, ymin, ymax], alpha=0.8)

# trajectory colored by coherence
scatter = axes[2].scatter(
    xs, ys,
    c=C,
    s=1,
    cmap='coolwarm'
)

# gates
axes[2].scatter(gate_x, gate_y, color='black', s=20, label='Transition Gates')

axes[2].set_title("Structure + Coherence + Gates")
axes[2].set_xticks([])
axes[2].set_yticks([])
axes[2].legend()

# -----------------------------
# Global Title
# -----------------------------
fig.suptitle(
    "NEXAH — Structure, Coherence, and Transition Geometry",
    fontsize=14
)

plt.tight_layout()

# -----------------------------
# Save
# -----------------------------
plt.savefig(
    "RESEARCH/visuals/nexah_hero_structure_pipeline_v2.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()
