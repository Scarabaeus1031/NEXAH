import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from sklearn.cluster import DBSCAN

# -----------------------------
# 1. Lorenz System
# -----------------------------
def lorenz(x, y, z, s=10, r=28, b=2.667):
    dx = s * (y - x)
    dy = x * (r - z) - y
    dz = x * y - b * z
    return dx, dy, dz

dt = 0.01
num_steps = 15000

xs = np.empty(num_steps)
ys = np.empty(num_steps)
zs = np.empty(num_steps)

xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

for i in range(num_steps - 1):
    dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
    xs[i + 1] = xs[i] + dx * dt
    ys[i + 1] = ys[i] + dy * dt
    zs[i + 1] = zs[i] + dz * dt

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
# 3. Field Gradient (Flow)
# -----------------------------
dZdx, dZdy = np.gradient(Z)
mag = np.sqrt(dZdx**2 + dZdy**2) + 1e-8
Fx = dZdx / mag
Fy = dZdy / mag

# -----------------------------
# 4. Coherence
# -----------------------------
def sample_field(x, y):
    xi = np.clip(((x - xmin) / (xmax - xmin) * (X.shape[0]-1)).astype(int), 0, X.shape[0]-1)
    yi = np.clip(((y - ymin) / (ymax - ymin) * (Y.shape[1]-1)).astype(int), 0, Y.shape[1]-1)
    return Fx[xi, yi], Fy[xi, yi]

Fx_traj, Fy_traj = sample_field(xs, ys)

vel_mag = np.sqrt(vx**2 + vy**2) + 1e-8
field_mag = np.sqrt(Fx_traj**2 + Fy_traj**2) + 1e-8

C = (vx * Fx_traj + vy * Fy_traj) / (vel_mag * field_mag)

# -----------------------------
# 5. Basin Clustering
# -----------------------------
data = np.vstack([xs, ys]).T
clustering = DBSCAN(eps=1.5, min_samples=50).fit(data)
labels = clustering.labels_

# -----------------------------
# 6. Transition Probability Field (approx)
# -----------------------------
# low density = high transition probability
P_transition = 1 / (Z + 1e-6)

# normalize
P_transition = (P_transition - P_transition.min()) / (P_transition.max() - P_transition.min())

# -----------------------------
# 7. Gate Detection
# -----------------------------
coherence_threshold = 0.2
density_threshold = np.percentile(Z, 20)

gate_indices = np.where((C < coherence_threshold))[0]
gate_indices = gate_indices[::200]

gate_x = xs[gate_indices]
gate_y = ys[gate_indices]

# -----------------------------
# 8. Navigation Path Simulation
# -----------------------------
# follow gradient + avoid high transition probability
nav_x = [xs[0]]
nav_y = [ys[0]]

for i in range(2000):
    x = nav_x[-1]
    y = nav_y[-1]

    fx, fy = sample_field(np.array([x]), np.array([y]))
    fx, fy = fx[0], fy[0]

    # simple steering: follow field
    step = 0.1
    nav_x.append(x + fx * step)
    nav_y.append(y + fy * step)

nav_x = np.array(nav_x)
nav_y = np.array(nav_y)

# -----------------------------
# 9. Plot
# -----------------------------
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# -----------------------------
# LEFT: Basins
# -----------------------------
scatter = axes[0].scatter(xs, ys, c=labels, s=1, cmap='tab10')
axes[0].set_title("Basins (Regime Structure)")
axes[0].set_xticks([])
axes[0].set_yticks([])

# -----------------------------
# CENTER: Transition Field
# -----------------------------
axes[1].imshow(np.rot90(P_transition), extent=[xmin, xmax, ymin, ymax])
axes[1].set_title("Transition Probability Field")
axes[1].set_xticks([])
axes[1].set_yticks([])

# -----------------------------
# RIGHT: Full Structure
# -----------------------------
axes[2].imshow(np.rot90(Z), extent=[xmin, xmax, ymin, ymax], alpha=0.8)

# coherence coloring
axes[2].scatter(xs, ys, c=C, s=1, cmap='coolwarm')

# gates
axes[2].scatter(gate_x, gate_y, color='black', s=20, label='Gates')

# navigation path
axes[2].plot(nav_x, nav_y, color='yellow', lw=2, label='Navigation Path')

axes[2].set_title("Structure + Coherence + Navigation")
axes[2].set_xticks([])
axes[2].set_yticks([])
axes[2].legend()

# -----------------------------
# Title
# -----------------------------
fig.suptitle(
    "NEXAH — Basin Structure, Transition Field, and Navigation",
    fontsize=14
)

plt.tight_layout()

# -----------------------------
# Save
# -----------------------------
plt.savefig(
    "RESEARCH/visuals/nexah_hero_structure_pipeline_v3.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()
