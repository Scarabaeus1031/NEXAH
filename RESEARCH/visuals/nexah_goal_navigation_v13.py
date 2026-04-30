import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# SYSTEM
# ============================================================

def lorenz(x, y, z, s=10, r=28, b=2.667):
    return s*(y-x), x*(r-z)-y, x*y - b*z

def simulate(steps=10000, dt=0.01):
    xs, ys, zs = np.zeros(steps), np.zeros(steps), np.zeros(steps)
    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

    for i in range(steps - 1):
        dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
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

def detect_gates(Z):
    return Z < np.percentile(Z, 20)

def interp(X, Y, Z, x, y):
    xi = np.searchsorted(X[:,0], x) - 1
    yi = np.searchsorted(Y[0,:], y) - 1

    xi = np.clip(xi, 0, Z.shape[0]-1)
    yi = np.clip(yi, 0, Z.shape[1]-1)

    return Z[xi, yi]

# ============================================================
# GOAL NAVIGATION
# ============================================================

def run_agent(xs, ys, X, Y, Z, start, goal, steps=2000):

    gate_thresh = np.percentile(Z, 20)

    x, y = start
    traj = []

    for _ in range(steps):

        # random local flow sample
        idx = np.random.randint(0, len(xs))
        fx = xs[idx+1] - xs[idx]
        fy = ys[idx+1] - ys[idx]

        density = interp(X, Y, Z, x, y)
        is_gate = density < gate_thresh

        # goal direction
        gx, gy = goal
        goal_vec = np.array([gx - x, gy - y])
        goal_vec /= (np.linalg.norm(goal_vec) + 1e-8)

        flow_vec = np.array([fx, fy])
        flow_vec /= (np.linalg.norm(flow_vec) + 1e-8)

        if is_gate:
            # gate: allow direction change
            step = 0.5*flow_vec + 0.8*goal_vec + 0.2*np.random.randn(2)
        else:
            # basin: follow structure
            step = 0.9*flow_vec + 0.2*goal_vec

        x += step[0] * 0.01
        y += step[1] * 0.01

        traj.append((x, y))

    return np.array(traj)

# ============================================================
# MAIN
# ============================================================

xs, ys = simulate()
X, Y, Z = density_field(xs, ys)

start = (xs[100], ys[100])
goal = (xs[5000], ys[5000])

traj = run_agent(xs, ys, X, Y, Z, start, goal)

# ============================================================
# PLOT
# ============================================================

fig, ax = plt.subplots(figsize=(6,6))

extent = [xs.min(), xs.max(), ys.min(), ys.max()]

ax.imshow(np.rot90(Z), cmap='inferno', extent=extent)

# gates
mask = detect_gates(Z)
gx, gy = np.where(mask)
gx = np.interp(gx, [0, Z.shape[0]], [xs.min(), xs.max()])
gy = np.interp(gy, [0, Z.shape[1]], [ys.min(), ys.max()])
ax.scatter(gx, gy, color='cyan', s=2, alpha=0.3)

# trajectory
ax.plot(traj[:,0], traj[:,1], color='white', lw=2)

# start & goal
ax.scatter(*start, color='green', s=100, label='Start')
ax.scatter(*goal, color='red', s=100, label='Goal')

ax.set_title("NEXAH v13 — Goal Navigation via Structure")
ax.axis('off')
ax.legend()

plt.tight_layout()

plt.savefig(
    "RESEARCH/visuals/nexah_goal_navigation_v13.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()
