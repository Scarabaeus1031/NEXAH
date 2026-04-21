import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# NEXAH V6 — Physics Orbit Layer
# ------------------------------------------------------------
# This version uses a second-order dynamical system:
#
#   x'  = vx
#   y'  = vy
#   vx' = Fx(x,y) - damping * vx
#   vy' = Fy(x,y) - damping * vy
#
# where:
#   F = -∇V + rotational_component
#
# So this is no longer "pure falling in the field",
# but actual motion with momentum.
# ============================================================


# ============================================================
# GRID / FIELD SETUP
# ============================================================

x = np.linspace(6, 17, 260)
y = np.linspace(22, 31, 260)
X, Y = np.meshgrid(x, y)

dx = x[1] - x[0]
dy = y[1] - y[0]


def gauss(x0, y0, sx, sy, amp):
    return amp * np.exp(
        -(((X - x0) ** 2) / (2 * sx ** 2) + ((Y - y0) ** 2) / (2 * sy ** 2))
    )


# Potential field
# Negative = wells / basins
# Positive = source / hill
V = (
    -2.0 * gauss(10.0, 25.0, 1.2, 1.1, 1.0)   # C0
    -2.4 * gauss(13.6, 26.0, 1.0, 1.0, 1.0)   # C2
    -1.0 * gauss(12.0, 24.0, 0.9, 0.9, 1.0)   # C1
    +2.0 * gauss(11.2, 28.5, 1.0, 1.0, 1.0)   # M0 / source
)

# Gradient force: F = -∇V
dV_dy, dV_dx = np.gradient(V, dy, dx)
Fx_grad = -dV_dx
Fy_grad = -dV_dy


# ============================================================
# ROTATIONAL COMPONENT
# ------------------------------------------------------------
# Adds angular / orbital tendency around chosen centers.
# This is a NEXAH-style physics layer, not strict celestial mechanics.
# ============================================================

def rotational_field(X, Y, center, strength=1.0, eps=0.8):
    cx, cy = center
    dx_ = X - cx
    dy_ = Y - cy
    r2 = dx_**2 + dy_**2 + eps
    Rx = -strength * dy_ / r2
    Ry =  strength * dx_ / r2
    return Rx, Ry


Rx0, Ry0 = rotational_field(X, Y, (10.0, 25.0), strength=2.0)
Rx2, Ry2 = rotational_field(X, Y, (13.6, 26.0), strength=-2.2)

Fx_rot = Rx0 + Rx2
Fy_rot = Ry0 + Ry2

# Total force field
Fx = Fx_grad + Fx_rot
Fy = Fy_grad + Fy_rot


# ============================================================
# SIMULATION
# ============================================================

def sample_field(px, py, A):
    ix = np.argmin(np.abs(x - px))
    iy = np.argmin(np.abs(y - py))
    return A[iy, ix]


def simulate_orbit(x0, y0, vx0, vy0, steps=1200, dt=0.02, damping=0.01):
    px, py = x0, y0
    vx, vy = vx0, vy0

    xs, ys = [px], [py]
    vxs, vys = [vx], [vy]
    energies = []

    for _ in range(steps):
        fx = sample_field(px, py, Fx)
        fy = sample_field(px, py, Fy)
        pot = sample_field(px, py, V)

        # second-order update
        vx = vx + dt * (fx - damping * vx)
        vy = vy + dt * (fy - damping * vy)

        px = px + dt * vx
        py = py + dt * vy

        xs.append(px)
        ys.append(py)
        vxs.append(vx)
        vys.append(vy)

        kinetic = 0.5 * (vx**2 + vy**2)
        total_energy = kinetic + pot
        energies.append(total_energy)

        # stop if trajectory leaves the domain
        if px < x.min() or px > x.max() or py < y.min() or py > y.max():
            break

    return np.array(xs), np.array(ys), np.array(vxs), np.array(vys), np.array(energies)


# Example starts
starts = [
    (8.0, 29.0, 0.7, 0.0),
    (15.0, 29.0, -0.6, 0.0),
    (9.0, 23.0, 0.4, 0.6),
    (12.4, 27.0, 0.0, -0.8),
]

trajectories = [simulate_orbit(*s) for s in starts]


# ============================================================
# PLOT
# ============================================================

fig, axs = plt.subplots(2, 2, figsize=(14, 12))

# ------------------------------------------------------------
# Q1 — Potential + total force field
# ------------------------------------------------------------
ax = axs[0, 0]
cf = ax.contourf(X, Y, V, levels=50, cmap="viridis")
ax.streamplot(X, Y, Fx, Fy, color=(1, 1, 1, 0.6), density=1.1, linewidth=0.6)

centers = [
    (10.0, 25.0, "C0"),
    (12.0, 24.0, "C1"),
    (13.6, 26.0, "C2"),
    (11.2, 28.5, "M0"),
]
for px, py, label in centers:
    ax.scatter(px, py, s=110, edgecolor="black", linewidth=1.2)
    ax.text(px + 0.15, py + 0.15, label, color="white", fontsize=10, weight="bold")

ax.set_title("Q1 — Potential + Total Force Field")
ax.set_xlabel("α")
ax.set_ylabel("β")
fig.colorbar(cf, ax=ax)

# ------------------------------------------------------------
# Q2 — Gradient vs rotation comparison
# ------------------------------------------------------------
ax = axs[0, 1]
mag_grad = np.sqrt(Fx_grad**2 + Fy_grad**2)
mag_rot = np.sqrt(Fx_rot**2 + Fy_rot**2)
delta = mag_rot - mag_grad

cf = ax.contourf(X, Y, delta, levels=50, cmap="coolwarm")
ax.contour(X, Y, V, levels=20, colors="black", linewidths=0.4, alpha=0.35)

for px, py, label in centers:
    ax.scatter(px, py, s=90, edgecolor="black", linewidth=1.0)
    ax.text(px + 0.12, py + 0.12, label, color="black", fontsize=9, weight="bold")

ax.set_title("Q2 — Rotation minus Gradient")
ax.set_xlabel("α")
ax.set_ylabel("β")
fig.colorbar(cf, ax=ax)

# ------------------------------------------------------------
# Q3 — Trajectories in field
# ------------------------------------------------------------
ax = axs[1, 0]
cf = ax.contourf(X, Y, V, levels=50, cmap="cividis")
ax.streamplot(X, Y, Fx, Fy, color="white", density=1.1, linewidth=0.6, alpha=0.6)

colors = ["cyan", "orange", "lime", "magenta"]
for i, (xs, ys, vxs, vys, energies) in enumerate(trajectories):
    ax.plot(xs, ys, color=colors[i % len(colors)], linewidth=2.0)
    ax.scatter(xs[0], ys[0], color=colors[i % len(colors)], s=40)
    ax.scatter(xs[-1], ys[-1], color=colors[i % len(colors)], s=70, marker="x")

for px, py, label in centers:
    ax.scatter(px, py, s=110, edgecolor="black", linewidth=1.2)
    ax.text(px + 0.15, py + 0.15, label, color="white", fontsize=10, weight="bold")

ax.set_title("Q3 — Momentum Trajectories")
ax.set_xlabel("α")
ax.set_ylabel("β")
fig.colorbar(cf, ax=ax)

# ------------------------------------------------------------
# Q4 — Energy over time
# ------------------------------------------------------------
ax = axs[1, 1]
for i, (xs, ys, vxs, vys, energies) in enumerate(trajectories):
    if len(energies) > 0:
        ax.plot(energies, color=colors[i % len(colors)], linewidth=2, label=f"traj {i+1}")

ax.axhline(0, color="black", linewidth=0.8, alpha=0.5)
ax.set_title("Q4 — Total Energy Along Trajectories")
ax.set_xlabel("step")
ax.set_ylabel("E = kinetic + potential")
ax.legend()

plt.suptitle("NEXAH V6 — Physics Layer (Momentum + Field)", fontsize=15)
plt.tight_layout()
plt.show()
