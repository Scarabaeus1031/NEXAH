# exp_31_julia_navigation_coupling.py
# ============================================================
# EXP-31 — Julia Navigation Coupling
#
# Goal:
# Explore whether navigation trajectories inside a Julia field
# exhibit the same transition topology observed in JANUS routing:
#
# - basin locking
# - transition gates
# - neck regions
# - drift corridors
# - navigation sensitivity
#
# Exploratory only.
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_gradient_magnitude

# ------------------------------------------------------------
# Julia parameter
# ------------------------------------------------------------

C = complex(-0.750, 0.100)

# ------------------------------------------------------------
# Grid setup
# ------------------------------------------------------------

N = 700

x = np.linspace(-1.8, 1.8, N)
y = np.linspace(-1.8, 1.8, N)

X, Y = np.meshgrid(x, y)

Z0 = X + 1j * Y

# ------------------------------------------------------------
# Julia iteration
# ------------------------------------------------------------

max_iter = 120

Z = Z0.copy()

escape = np.zeros(Z.shape)

mask = np.ones(Z.shape, dtype=bool)

for i in range(max_iter):

    Z[mask] = Z[mask]**2 + C

    escaped = np.abs(Z) > 2.0

    newly_escaped = escaped & mask

    escape[newly_escaped] = i

    mask &= ~escaped

escape[escape == 0] = max_iter

# ------------------------------------------------------------
# Structural field
# ------------------------------------------------------------

field = gaussian_gradient_magnitude(escape, sigma=2.0)

# ------------------------------------------------------------
# Navigation field
# ------------------------------------------------------------

gy, gx = np.gradient(field)

# negative gradient = flow toward coherent basins
vx = -gx
vy = -gy

# normalize
norm = np.sqrt(vx**2 + vy**2) + 1e-9

vx /= norm
vy /= norm

# ------------------------------------------------------------
# Navigation trajectories
# ------------------------------------------------------------

def trace_path(x0, y0, steps=220, dt=0.015):

    px = [x0]
    py = [y0]

    x_curr = x0
    y_curr = y0

    for _ in range(steps):

        ix = np.argmin(np.abs(x - x_curr))
        iy = np.argmin(np.abs(y - y_curr))

        if ix <= 1 or ix >= N-2 or iy <= 1 or iy >= N-2:
            break

        dx = vx[iy, ix]
        dy = vy[iy, ix]

        x_curr += dx * dt
        y_curr += dy * dt

        px.append(x_curr)
        py.append(y_curr)

    return np.array(px), np.array(py)

# ------------------------------------------------------------
# Seed points
# ------------------------------------------------------------

seed_points = [
    (-1.2, -0.4),
    (-1.0,  0.2),
    (-0.7, -0.7),
    ( 0.3,  0.0),
    ( 0.7,  0.5),
    ( 1.1, -0.2),
]

# ------------------------------------------------------------
# Plot
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 12))

ax.imshow(
    escape,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="magma"
)

# ------------------------------------------------------------
# Overlay gradient structure
# ------------------------------------------------------------

levels = np.linspace(
    np.percentile(field, 70),
    np.percentile(field, 99),
    14
)

ax.contour(
    X,
    Y,
    field,
    levels=levels,
    colors="cyan",
    linewidths=0.8,
    alpha=0.7
)

# ------------------------------------------------------------
# Draw trajectories
# ------------------------------------------------------------

for sx, sy in seed_points:

    px, py = trace_path(sx, sy)

    ax.plot(
        px,
        py,
        linewidth=2.0,
        alpha=0.95
    )

    ax.scatter(px[0], py[0], s=60)
    ax.scatter(px[-1], py[-1], s=80)

# ------------------------------------------------------------
# Transition neck marker
# ------------------------------------------------------------

ax.axvline(
    0,
    linestyle="--",
    linewidth=1.5,
    alpha=0.7
)

# ------------------------------------------------------------
# Labels
# ------------------------------------------------------------

ax.set_title(
    "EXP-31 — Julia Navigation Coupling\n"
    f"c = {C.real:.3f} + {C.imag:.3f}i",
    fontsize=18
)

ax.set_xlabel("Re(z)")
ax.set_ylabel("Im(z)")

plt.tight_layout()

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

plt.savefig(
    "exp_31_julia_navigation_coupling.png",
    dpi=300
)

plt.show()

# ------------------------------------------------------------
# Notes
# ------------------------------------------------------------

print("\nEXP-31 — Julia Navigation Coupling")
print("--------------------------------------------------")
print("parameter c =", C)
print()
print("Interpretation:")
print("- trajectories converging into regions -> basin locking")
print("- narrow crossings -> transition gates")
print("- unstable rerouting -> drift sensitivity")
print("- coherent channels -> navigation corridors")
print()
print("Exploratory only.")
