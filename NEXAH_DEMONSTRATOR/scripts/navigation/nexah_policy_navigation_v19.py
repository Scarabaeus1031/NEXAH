import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# SYSTEM (Lorenz only for clarity here)
# ============================================================

def lorenz(n=8000, dt=0.01):
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


# ============================================================
# POLICY (simple prototype)
# ============================================================

def policy_field(X, Y):
    # example:
    # push toward center + avoid origin instability

    cx = np.mean(X)
    cy = np.mean(Y)

    Ux = -(X - cx)
    Uy = -(Y - cy)

    mag = np.sqrt(Ux**2 + Uy**2) + 1e-9

    return Ux/mag, Uy/mag


# ============================================================
# SIMULATED NAVIGATION
# ============================================================

def simulate_path(start, X, Y, Fx, Fy, Ux, Uy, steps=200, alpha=0.7):
    path = [start]

    x, y = start

    for _ in range(steps):

        # find nearest grid index
        ix = np.abs(X[:,0] - x).argmin()
        iy = np.abs(Y[0,:] - y).argmin()

        f_vec = np.array([Fx[ix, iy], Fy[ix, iy]])
        u_vec = np.array([Ux[ix, iy], Uy[ix, iy]])

        v = f_vec + alpha * u_vec

        x += v[0] * 0.1
        y += v[1] * 0.1

        path.append((x, y))

    return np.array(path)


# ============================================================
# RUN
# ============================================================

x, y = lorenz()

X, Y, Z, extent = density_field(x, y)

Fx, Fy = navigation_field(Z)
Ux, Uy = policy_field(X, Y)

# simulate
path = simulate_path((x[0], y[0]), X, Y, Fx, Fy, Ux, Uy)

# ============================================================
# PLOT
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 1. Field
axes[0].imshow(np.rot90(Z), cmap='viridis', extent=extent)
axes[0].plot(x, y, color='white', lw=0.5)
axes[0].set_title("Field + Trajectory")
axes[0].axis("off")

# 2. Navigation + Policy
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

axes[1].set_title("Navigation + Policy")
axes[1].axis("off")

# 3. Guided path
axes[2].imshow(np.rot90(Z), cmap='inferno', extent=extent)
axes[2].plot(path[:,0], path[:,1], color='cyan', lw=2)

axes[2].scatter(path[0,0], path[0,1], color='green', s=50, label="start")
axes[2].scatter(path[-1,0], path[-1,1], color='red', s=50, label="end")

axes[2].legend()
axes[2].set_title("Controlled Navigation")
axes[2].axis("off")

fig.suptitle("NEXAH v19 — Policy-Guided Navigation", fontsize=14)

plt.tight_layout()

plt.savefig(
    "NEXAH_DEMONSTRATOR/visuals/nexah_policy_navigation_v19.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()
