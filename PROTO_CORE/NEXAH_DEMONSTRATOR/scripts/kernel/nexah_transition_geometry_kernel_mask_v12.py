import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import os

# ============================================================
# SYSTEM (Lorenz)
# ============================================================

def lorenz(x, y, z, s=10, r=28, b=2.667):
    return s*(y-x), x*(r-z)-y, x*y - b*z

def simulate(system, steps=10000, dt=0.01):
    xs, ys, zs = np.zeros(steps), np.zeros(steps), np.zeros(steps)
    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

    for i in range(steps - 1):
        dx, dy, dz = system(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx*dt
        ys[i+1] = ys[i] + dy*dt
        zs[i+1] = zs[i] + dz*dt

    return xs, ys

# ============================================================
# FIELD
# ============================================================

def density_field(xs, ys):
    kde = gaussian_kde(np.vstack([xs, ys]))

    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()

    X, Y = np.mgrid[xmin:xmax:250j, ymin:ymax:250j]
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
# INTERPOLATION
# ============================================================

def interp_field(X, Y, Z, x, y):
    xi = np.searchsorted(X[:,0], x) - 1
    yi = np.searchsorted(Y[0,:], y) - 1

    xi = np.clip(xi, 0, Z.shape[0]-1)
    yi = np.clip(yi, 0, Z.shape[1]-1)

    return Z[xi, yi]

# ============================================================
# MULTI-AGENT NAVIGATION
# ============================================================

def run_swarm(xs, ys, X, Y, Z, n_agents=25, steps=1500):

    dx, dy = compute_flow(xs, ys)
    gate_threshold = np.percentile(Z, 20)

    agents = []

    # initial positions (random samples from trajectory)
    for _ in range(n_agents):
        idx = np.random.randint(0, len(xs))
        agents.append([xs[idx], ys[idx]])

    trajectories = [[] for _ in range(n_agents)]

    for t in range(steps):
        for i in range(n_agents):

            x, y = agents[i]

            # local flow sample
            idx = np.random.randint(0, len(xs))
            fx, fy = dx[idx], dy[idx]

            density = interp_field(X, Y, Z, x, y)
            is_gate = density < gate_threshold

            # behavior
            if is_gate:
                # exploration in gate
                noise = np.random.randn(2) * 0.25
                step = np.array([fx, fy]) * 0.5 + noise
            else:
                # structured motion
                step = np.array([fx, fy]) * 0.9

            # update
            x += step[0] * 0.01
            y += step[1] * 0.01

            agents[i] = [x, y]
            trajectories[i].append((x, y))

    return trajectories

# ============================================================
# MAIN
# ============================================================

xs, ys = simulate(lorenz)
X, Y, Z = density_field(xs, ys)

swarm = run_swarm(xs, ys, X, Y, Z)

# ============================================================
# PLOT
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

extent = [xs.min(), xs.max(), ys.min(), ys.max()]

# RAW
axes[0].plot(xs, ys, lw=0.3, color='steelblue')
axes[0].set_title("System Dynamics")
axes[0].axis("off")

# FIELD + GATES
axes[1].imshow(np.rot90(Z), cmap="viridis", extent=extent)

gate_mask = detect_gates(Z)
gx, gy = np.where(gate_mask)

gx = np.interp(gx, [0, Z.shape[0]], [xs.min(), xs.max()])
gy = np.interp(gy, [0, Z.shape[1]], [ys.min(), ys.max()])

axes[1].scatter(gx, gy, color="cyan", s=2, alpha=0.4)
axes[1].set_title("Field + Gate Regions")
axes[1].axis("off")

# SWARM
axes[2].imshow(np.rot90(Z), cmap="inferno", extent=extent)

for traj in swarm:
    traj = np.array(traj)
    axes[2].plot(traj[:,0], traj[:,1], lw=0.8, alpha=0.7)

axes[2].scatter(gx, gy, color="cyan", s=3, alpha=0.4)

axes[2].set_title("Multi-Agent Navigation (Swarm)")
axes[2].axis("off")

plt.suptitle(
    "NEXAH v12 — Multi-Agent Kernel Navigation\n"
    "Emergent structure from gate-aware local dynamics",
    fontsize=14
)

plt.tight_layout()

output_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "visuals",
    "nexah_swarm_navigation_v12.png"
))

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches='tight'
)

plt.show()
