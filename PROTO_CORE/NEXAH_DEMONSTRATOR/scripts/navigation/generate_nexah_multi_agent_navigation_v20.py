import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# SYSTEM (Lorenz)
# ============================================================

def lorenz(n=9000, dt=0.01):
    def f(x, y, z):
        return 10*(y-x), x*(28-z)-y, x*y - 2.667*z

    xs, ys, zs = np.zeros(n), np.zeros(n), np.zeros(n)
    xs[0], ys[0], zs[0] = 0.1, 0, 0

    for i in range(n-1):
        dx, dy, dz = f(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx*dt
        ys[i+1] = ys[i] + dy*dt
        zs[i+1] = zs[i] + dz*dt

    return xs[1000:], ys[1000:]


# ============================================================
# FIELD
# ============================================================

def density_field(x, y):
    kde = gaussian_kde(np.vstack([x, y]))

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    X, Y = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
    Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

    return X, Y, Z, [xmin, xmax, ymin, ymax]


def navigation_field(Z):
    dZdx, dZdy = np.gradient(Z)

    mag = np.sqrt(dZdx**2 + dZdy**2) + 1e-9

    Fx = dZdx / mag
    Fy = dZdy / mag

    return Fx, Fy


def policy_field(X, Y):
    cx = np.mean(X)
    cy = np.mean(Y)

    Ux = -(X - cx)
    Uy = -(Y - cy)

    mag = np.sqrt(Ux**2 + Uy**2) + 1e-9

    return Ux/mag, Uy/mag


# ============================================================
# MULTI-AGENT SIMULATION
# ============================================================

def simulate_agents(n_agents, X, Y, Fx, Fy, Ux, Uy,
                    steps=250, alpha=0.6):

    xmin, xmax = X.min(), X.max()
    ymin, ymax = Y.min(), Y.max()

    # random initial positions
    agents = np.zeros((n_agents, 2))
    agents[:,0] = np.random.uniform(xmin, xmax, n_agents)
    agents[:,1] = np.random.uniform(ymin, ymax, n_agents)

    trajectories = []

    for i in range(n_agents):
        traj = [agents[i].copy()]
        x, y = agents[i]

        for _ in range(steps):
            ix = np.abs(X[:,0] - x).argmin()
            iy = np.abs(Y[0,:] - y).argmin()

            f_vec = np.array([Fx[ix, iy], Fy[ix, iy]])
            u_vec = np.array([Ux[ix, iy], Uy[ix, iy]])

            v = f_vec + alpha * u_vec

            x += v[0] * 0.1
            y += v[1] * 0.1

            traj.append([x, y])

        trajectories.append(np.array(traj))

    return trajectories


# ============================================================
# RUN
# ============================================================

x, y = lorenz()

X, Y, Z, extent = density_field(x, y)
Fx, Fy = navigation_field(Z)
Ux, Uy = policy_field(X, Y)

trajectories = simulate_agents(
    n_agents=25,
    X=X, Y=Y,
    Fx=Fx, Fy=Fy,
    Ux=Ux, Uy=Uy
)

# ============================================================
# PLOT
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# ------------------------------------------------------------
# 1. Field
# ------------------------------------------------------------
axes[0].imshow(np.rot90(Z), cmap='viridis', extent=extent)
axes[0].plot(x, y, color='white', lw=0.5)
axes[0].set_title("Structure Field")
axes[0].axis("off")

# ------------------------------------------------------------
# 2. Vector fields
# ------------------------------------------------------------
axes[1].imshow(np.rot90(Z), cmap='inferno', extent=extent)

axes[1].quiver(
    X[::10,::10],
    Y[::10,::10],
    Fx[::10,::10],
    Fy[::10,::10],
    color='white',
    alpha=0.6
)

axes[1].quiver(
    X[::10,::10],
    Y[::10,::10],
    Ux[::10,::10],
    Uy[::10,::10],
    color='cyan',
    alpha=0.6
)

axes[1].set_title("Navigation + Policy Fields")
axes[1].axis("off")

# ------------------------------------------------------------
# 3. Multi-agent behavior
# ------------------------------------------------------------
axes[2].imshow(np.rot90(Z), cmap='inferno', extent=extent)

for traj in trajectories:
    axes[2].plot(traj[:,0], traj[:,1], alpha=0.7)

axes[2].set_title("Multi-Agent Navigation")
axes[2].axis("off")

fig.suptitle(
    "NEXAH v20 — Multi-Agent Field Navigation\n"
    "Emergent structure-guided swarm behavior",
    fontsize=14
)

plt.tight_layout()

plt.savefig(
    "NEXAH_DEMONSTRATOR/visuals/nexah_multi_agent_navigation_v20.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()
