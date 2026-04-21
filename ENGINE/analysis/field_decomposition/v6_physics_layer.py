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
# NEXAH V6 — CLEAN PHYSICS LAYER
# ============================================================

# ------------------------------------------------------------
# GRID
# ------------------------------------------------------------
x = np.linspace(6, 17, 220)
y = np.linspace(22, 31, 220)
X, Y = np.meshgrid(x, y)

dx = x[1] - x[0]
dy = y[1] - y[0]

# ------------------------------------------------------------
# FIELD (Potential)
# ------------------------------------------------------------
def gauss(x0, y0, sx, sy, amp):
    return amp * np.exp(-(((X-x0)**2)/(2*sx**2) + ((Y-y0)**2)/(2*sy**2)))

V = (
    -2.0 * gauss(10.0, 25.0, 1.2, 1.0, 1.0)   # C0
    -2.3 * gauss(13.6, 26.0, 1.0, 1.0, 1.0)   # C2
    -1.0 * gauss(12.0, 24.0, 0.8, 0.9, 1.0)   # C1
    +2.0 * gauss(11.2, 28.5, 1.0, 1.0, 1.0)   # M0
)

# ------------------------------------------------------------
# GRADIENT FORCE
# ------------------------------------------------------------
dV_dy, dV_dx = np.gradient(V, dy, dx)
Fx_grad = -dV_dx
Fy_grad = -dV_dy

# ------------------------------------------------------------
# ROTATION FIELD
# ------------------------------------------------------------
def rotation(center, strength):
    cx, cy = center
    dx_ = X - cx
    dy_ = Y - cy
    r2 = dx_**2 + dy_**2 + 0.6
    return -strength * dy_ / r2, strength * dx_ / r2

Rx1, Ry1 = rotation((10,25), 2.0)
Rx2, Ry2 = rotation((13.6,26), -2.0)

Fx = Fx_grad + Rx1 + Rx2
Fy = Fy_grad + Ry1 + Ry2

# ------------------------------------------------------------
# SAMPLING
# ------------------------------------------------------------
def sample(px, py, A):
    ix = np.argmin(np.abs(x - px))
    iy = np.argmin(np.abs(y - py))
    return A[iy, ix]

# ------------------------------------------------------------
# SIMULATION
# ------------------------------------------------------------
def simulate(x0, y0, vx0, vy0, steps=1000, dt=0.02, damping=0.02):
    px, py = x0, y0
    vx, vy = vx0, vy0

    xs, ys = [px], [py]
    energies = []

    for _ in range(steps):

        fx = sample(px, py, Fx)
        fy = sample(px, py, Fy)
        pot = sample(px, py, V)

        vx += dt * (fx - damping * vx)
        vy += dt * (fy - damping * vy)

        px += dt * vx
        py += dt * vy

        xs.append(px)
        ys.append(py)

        E = 0.5*(vx**2 + vy**2) + pot
        energies.append(E)

        if px < x.min() or px > x.max() or py < y.min() or py > y.max():
            break

    return np.array(xs), np.array(ys), np.array(energies)

# ------------------------------------------------------------
# RUN TRAJECTORIES
# ------------------------------------------------------------
starts = [
    (8.0, 29.0, 0.6, 0.0),
    (15.0, 29.0, -0.5, 0.0),
    (9.0, 23.0, 0.4, 0.5),
    (12.5, 27.0, 0.0, -0.7),
]

trajs = [simulate(*s) for s in starts]

# ------------------------------------------------------------
# PLOTS
# ------------------------------------------------------------
fig, axs = plt.subplots(2,2, figsize=(14,12))

# Q1 FIELD
ax = axs[0,0]
cf = ax.contourf(X, Y, V, levels=50, cmap="viridis")
ax.streamplot(X, Y, Fx, Fy, color=(1,1,1,0.6), density=1.1, linewidth=0.6)
ax.set_title("Q1 — Field")

# Q2 FORCE MAGNITUDE
ax = axs[0,1]
mag = np.sqrt(Fx**2 + Fy**2)
cf = ax.contourf(X, Y, mag, levels=50, cmap="magma")
ax.set_title("Q2 — Force Magnitude")

# Q3 TRAJECTORIES
ax = axs[1,0]
cf = ax.contourf(X, Y, V, levels=50, cmap="cividis")

colors = ["cyan","orange","lime","magenta"]
for i,(xs,ys,E) in enumerate(trajs):
    ax.plot(xs, ys, color=colors[i], linewidth=2)
    ax.scatter(xs[0], ys[0], color=colors[i], s=40)
    ax.scatter(xs[-1], ys[-1], color=colors[i], s=70, marker="x")

ax.set_title("Q3 — Trajectories")

# Q4 ENERGY
ax = axs[1,1]
for i,(xs,ys,E) in enumerate(trajs):
    if len(E)>0:
        ax.plot(E, color=colors[i], label=f"T{i+1}")
ax.legend()
ax.set_title("Q4 — Energy")

plt.suptitle("NEXAH V6 — Physics Layer (Stable Build)")
plt.tight_layout()
plt.show()
