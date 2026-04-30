import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# SYSTEM
# ============================================================

def lorenz(x, y, z, s=10, r=28, b=2.667):
    return s*(y-x), x*(r-z)-y, x*y - b*z

def simulate(system, steps=8000, dt=0.01):
    xs, ys, zs = np.zeros(steps), np.zeros(steps), np.zeros(steps)
    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

    for i in range(steps - 1):
        dx, dy, dz = system(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx*dt
        ys[i+1] = ys[i] + dy*dt
        zs[i+1] = zs[i] + dz*dt

    return xs, ys

# ============================================================
# FIELD + GATES
# ============================================================

def density_field(xs, ys):
    kde = gaussian_kde(np.vstack([xs, ys]))

    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()

    X, Y = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
    Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

    return X, Y, Z

def compute_flow(xs, ys):
    dx = np.gradient(xs)
    dy = np.gradient(ys)
    return dx, dy

def detect_gates(Z):
    threshold = np.percentile(Z, 20)
    return Z < threshold

# ============================================================
# INTERPOLATION HELPERS
# ============================================================

def interp_field(X, Y, Z, x, y):
    xi = np.searchsorted(X[:,0], x) - 1
    yi = np.searchsorted(Y[0,:], y) - 1

    xi = np.clip(xi, 0, Z.shape[0]-1)
    yi = np.clip(yi, 0, Z.shape[1]-1)

    return Z[xi, yi]

# ============================================================
# AGENT NAVIGATION
# ============================================================

def run_agent(xs, ys, X, Y, Z, steps=2000):

    dx, dy = compute_flow(xs, ys)

    # initial state
    x = xs[len(xs)//2]
    y = ys[len(ys)//2]

    traj_x = []
    traj_y = []

    gate_mask = detect_gates(Z)

    for _ in range(steps):

        # nearest field direction
        idx = np.random.randint(0, len(xs))
        fx = dx[idx]
        fy = dy[idx]

        # density at position
        density = interp_field(X, Y, Z, x, y)

        # gate check
        is_gate = density < np.percentile(Z, 20)

        # motion logic
        if is_gate:
            # allow exploration
            noise = np.random.randn(2) * 0.2
            step = np.array([fx, fy]) * 0.5 + noise
        else:
            # stay coherent
            step = np.array([fx, fy]) * 0.9

        x += step[0] * 0.01
        y += step[1] * 0.01

        traj_x.append(x)
        traj_y.append(y)

    return np.array(traj_x), np.array(traj_y)

# ============================================================
# MAIN PIPELINE
# ============================================================

xs, ys = simulate(lorenz)
X, Y, Z = density_field(xs, ys)

agent_x, agent_y = run_agent(xs, ys, X, Y, Z)

# ============================================================
# PLOT
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

extent = [xs.min(), xs.max(), ys.min(), ys.max()]

# RAW
axes[0].plot(xs, ys, lw=0.3)
axes[0].set_title("System Dynamics")
axes[0].axis("off")

# FIELD + GATES
axes[1].imshow(np.rot90(Z), cmap="viridis", extent=extent)
gate_mask = detect_gates(Z)

gx, gy = np.where(gate_mask)
gx = np.interp(gx, [0, Z.shape[0]], [xs.min(), xs.max()])
gy = np.interp(gy, [0, Z.shape[1]], [ys.min(), ys.max()])

axes[1].scatter(gx, gy, color="cyan", s=2, alpha=0.4)
axes[1].set_title("Field + Gates")
axes[1].axis("off")

# AGENT PATH
axes[2].imshow(np.rot90(Z), cmap="inferno", extent=extent)
axes[2].plot(agent_x, agent_y, color="white", lw=1.2)

axes[2].scatter(gx, gy, color="cyan", s=3, alpha=0.5)

axes[2].set_title("Kernel Navigation")
axes[2].axis("off")

plt.suptitle(
    "NEXAH v11 — Kernel Navigation Engine\n"
    "Agent moves through structure using gate-aware dynamics",
    fontsize=14
)

plt.tight_layout()

plt.savefig(
    "RESEARCH/visuals/nexah_kernel_navigation_v11.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()
