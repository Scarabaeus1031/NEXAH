# NEXAH v21 — Kuramoto as a NEXAH Field
#
# Kuramoto → Order Parameter → Field → Gates → Navigation

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


# ============================================================
# 1. KURAMOTO SIMULATION
# ============================================================

def simulate_kuramoto(n_agents=64, steps=4500, dt=0.04, K=2.05, seed=7):
    rng = np.random.default_rng(seed)

    theta = rng.uniform(0, 2*np.pi, n_agents)
    omega = rng.normal(0.0, 0.65, n_agents)

    theta_history = np.zeros((steps, n_agents))
    r_history = np.zeros(steps)
    psi_history = np.zeros(steps)

    for t in range(steps):
        order = np.mean(np.exp(1j * theta))
        r = np.abs(order)
        psi = np.angle(order)

        theta_history[t] = theta
        r_history[t] = r
        psi_history[t] = psi

        theta_dot = omega + K * r * np.sin(psi - theta)
        theta = np.mod(theta + dt * theta_dot, 2*np.pi)

    return theta_history, r_history, np.unwrap(psi_history)


# ============================================================
# 2. FIELD CONSTRUCTION
# ============================================================

def density_field(x, y, grid_n=250):
    x = np.asarray(x)
    y = np.asarray(y)

    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]

    # jitter gegen KDE Probleme
    x = x + np.random.normal(0, 1e-7, len(x))
    y = y + np.random.normal(0, 1e-7, len(y))

    kde = gaussian_kde(np.vstack([x, y]))

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    X, Y = np.mgrid[xmin:xmax:complex(grid_n), ymin:ymax:complex(grid_n)]
    Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

    return X, Y, Z, [xmin, xmax, ymin, ymax]


def navigation_field(Z):
    dZdx, dZdy = np.gradient(Z)

    mag = np.sqrt(dZdx**2 + dZdy**2) + 1e-9

    Fx = dZdx / mag
    Fy = dZdy / mag

    return Fx, Fy


def detect_gates(Z, percentile=15):
    return Z < np.percentile(Z, percentile)


def grid_to_points(mask, extent, shape, max_points=800):
    gx, gy = np.where(mask)

    gx = np.interp(gx, [0, shape[0]], [extent[0], extent[1]])
    gy = np.interp(gy, [0, shape[1]], [extent[2], extent[3]])

    if len(gx) > max_points:
        idx = np.linspace(0, len(gx) - 1, max_points).astype(int)
        gx = gx[idx]
        gy = gy[idx]

    return gx, gy


# ============================================================
# 3. RUN
# ============================================================

theta_hist, r_hist, psi_hist = simulate_kuramoto()

# NEXAH Projection:
# x = r(t)
# y = dr/dt
r = r_hist
dr = np.gradient(r)

# optional smoothing
dr = np.convolve(dr, np.ones(5)/5, mode='same')

X, Y, Z, extent = density_field(r, dr)
Fx, Fy = navigation_field(Z)

gates = detect_gates(Z)
gx, gy = grid_to_points(gates, extent, Z.shape)


# ============================================================
# 4. PLOT
# ============================================================

fig, axes = plt.subplots(1, 4, figsize=(20, 5))

# ------------------------------------------------------------
# 1. Kuramoto Raw
# ------------------------------------------------------------
axes[0].plot(theta_hist[:600], alpha=0.4)
axes[0].plot(r, color='black', lw=2, label='r(t)')
axes[0].set_title("Kuramoto Oscillators + Order Parameter")
axes[0].legend()
axes[0].axis("off")

# ------------------------------------------------------------
# 2. Projection (Slice)
# ------------------------------------------------------------
axes[1].plot(r, dr, color='blue', lw=1)
axes[1].scatter(r[0], dr[0], color='green', label='start')
axes[1].scatter(r[-1], dr[-1], color='red', label='end')
axes[1].set_title("NEXAH Projection (r, dr/dt)")
axes[1].legend()
axes[1].axis("off")

# ------------------------------------------------------------
# 3. Field
# ------------------------------------------------------------
axes[2].imshow(np.rot90(Z), cmap='viridis', extent=extent)
axes[2].plot(r, dr, color='white', lw=1)
axes[2].set_title("Reconstructed Field")
axes[2].axis("off")

# ------------------------------------------------------------
# 4. Gates + Navigation
# ------------------------------------------------------------
axes[3].imshow(np.rot90(Z), cmap='inferno', extent=extent)

# Neon Gates
axes[3].scatter(gx, gy, s=120, c='cyan', alpha=0.15)
axes[3].scatter(gx, gy, s=20, c='yellow', edgecolors='black')

# Path
axes[3].plot(r, dr, color='white', lw=1)

# Flow vectors
axes[3].quiver(
    X[::12,::12],
    Y[::12,::12],
    Fx[::12,::12],
    Fy[::12,::12],
    color='white',
    alpha=0.5
)

axes[3].set_title("Gates + Navigation Field")
axes[3].axis("off")

# ------------------------------------------------------------
# Global
# ------------------------------------------------------------
fig.suptitle(
    "NEXAH v21 — Kuramoto → Field → Gates → Navigation",
    fontsize=14
)

plt.tight_layout()

plt.savefig(
    "NEXAH_DEMONSTRATOR/visuals/nexah_kuramoto_field_v21.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()
