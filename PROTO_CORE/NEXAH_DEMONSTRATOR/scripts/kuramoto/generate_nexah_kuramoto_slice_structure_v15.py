# NEXAH v15 — Kuramoto Slice vs Structure
# Phase synchronization as projected structure:
# oscillators → order parameter → slice/channel → regime structure

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# KURAMOTO SIMULATION
# ============================================================

def simulate_kuramoto(n=48, steps=3000, dt=0.04, K=2.2, seed=7):
    rng = np.random.default_rng(seed)

    theta = rng.uniform(0, 2*np.pi, n)
    omega = rng.normal(0.0, 0.55, n)

    theta_history = np.zeros((steps, n))
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
        theta = theta + dt * theta_dot
        theta = np.mod(theta, 2*np.pi)

    return theta_history, r_history, psi_history


# ============================================================
# STRUCTURE EXTRACTION
# ============================================================

def density_field(x, y, grid_n=250):
    x = x + np.random.normal(0, 1e-6, size=len(x))
    y = y + np.random.normal(0, 1e-6, size=len(y))

    kde = gaussian_kde(np.vstack([x, y]))

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    X, Y = np.mgrid[xmin:xmax:complex(grid_n), ymin:ymax:complex(grid_n)]
    Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

    return X, Y, Z, [xmin, xmax, ymin, ymax]


def detect_gates(Z, percentile=18):
    return Z < np.percentile(Z, percentile)


# ============================================================
# RUN
# ============================================================

theta_hist, r, psi = simulate_kuramoto()

dr = np.gradient(r)

# NEXAH projection:
# x = synchronization order r(t)
# y = rate of synchronization change dr/dt
x_slice = r
y_slice = dr * 25.0

X, Y, Z, extent = density_field(x_slice, y_slice)

gate_mask = detect_gates(Z)

gx_idx, gy_idx = np.where(gate_mask)
gx = np.interp(gx_idx, [0, Z.shape[0]], [extent[0], extent[1]])
gy = np.interp(gy_idx, [0, Z.shape[1]], [extent[2], extent[3]])

# thin gates
if len(gx) > 800:
    idx = np.linspace(0, len(gx)-1, 800).astype(int)
    gx = gx[idx]
    gy = gy[idx]

# representative time slices
snapshots = [250, 900, 1700, 2600]

# ============================================================
# PLOT
# ============================================================

fig = plt.figure(figsize=(18, 10))

gs = fig.add_gridspec(2, 3, height_ratios=[1.0, 1.05])

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])
ax4 = fig.add_subplot(gs[1, 0])
ax5 = fig.add_subplot(gs[1, 1])
ax6 = fig.add_subplot(gs[1, 2])

# ------------------------------------------------------------
# 1. Raw oscillator view
# ------------------------------------------------------------
for i in range(theta_hist.shape[1]):
    ax1.plot(np.sin(theta_hist[:, i]), lw=0.35, alpha=0.45)

ax1.plot(r, color="black", lw=2.2, label="Order parameter r(t)")
ax1.set_title("Raw Kuramoto View\nmany oscillators + order parameter")
ax1.set_xticks([])
ax1.legend(fontsize=8)

# ------------------------------------------------------------
# 2. Order parameter
# ------------------------------------------------------------
ax2.plot(r, lw=2)
ax2.set_title("Synchronization Signal\nr(t)")
ax2.set_xlabel("time")
ax2.set_ylabel("r")

# ------------------------------------------------------------
# 3. Phase circle snapshots
# ------------------------------------------------------------
circle = np.linspace(0, 2*np.pi, 300)
ax3.plot(np.cos(circle), np.sin(circle), lw=1, alpha=0.5)

for t in snapshots:
    phases = theta_hist[t]
    ax3.scatter(
        np.cos(phases),
        np.sin(phases),
        s=18,
        alpha=0.7,
        label=f"t={t}",
    )

ax3.set_aspect("equal")
ax3.set_title("Structure View\nphase distribution on circle")
ax3.set_xticks([])
ax3.set_yticks([])
ax3.legend(fontsize=7)

# ------------------------------------------------------------
# 4. Slice projection
# ------------------------------------------------------------
ax4.plot(x_slice, y_slice, lw=0.65, color="steelblue", alpha=0.8)
ax4.scatter(x_slice[0], y_slice[0], s=80, color="green", label="start")
ax4.scatter(x_slice[-1], y_slice[-1], s=80, color="red", label="end")
ax4.set_title("NEXAH Slice Projection\nx = r(t), y = dr/dt")
ax4.set_xlabel("r")
ax4.set_ylabel("dr/dt")
ax4.legend(fontsize=8)

# ------------------------------------------------------------
# 5. Field reconstruction
# ------------------------------------------------------------
ax5.imshow(np.rot90(Z), cmap="viridis", extent=extent, aspect="auto")
ax5.plot(x_slice, y_slice, color="white", lw=1.0, alpha=0.75)
ax5.set_title("Reconstructed Field\nprojected synchronization dynamics")
ax5.set_xticks([])
ax5.set_yticks([])

# ------------------------------------------------------------
# 6. Gates / apertures
# ------------------------------------------------------------
ax6.imshow(np.rot90(Z), cmap="inferno", extent=extent, aspect="auto")
ax6.plot(x_slice, y_slice, color="white", lw=1.0, alpha=0.75)

# neon gates
ax6.scatter(gx, gy, s=90, c="cyan", alpha=0.13, edgecolors="none")
ax6.scatter(gx, gy, s=18, c="yellow", alpha=0.8, edgecolors="black", linewidths=0.25)

ax6.set_title("Kuramoto Gates\nlow-density apertures in projection")
ax6.set_xticks([])
ax6.set_yticks([])

fig.suptitle(
    "NEXAH v15 — Kuramoto Slice vs Structure\n"
    "Synchronization as projected field geometry: oscillators → order parameter → gates",
    fontsize=16,
)

plt.tight_layout(rect=[0, 0, 1, 0.93])

plt.savefig(
    "NEXAH_DEMONSTRATOR/visuals/nexah_kuramoto_slice_structure_v15.png",
    dpi=300,
    bbox_inches="tight",
)

plt.show()
