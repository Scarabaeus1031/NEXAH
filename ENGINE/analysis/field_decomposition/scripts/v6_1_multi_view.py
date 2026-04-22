import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# GRID
# ============================================================
x = np.linspace(6, 17, 200)
y = np.linspace(22, 31, 200)
X, Y = np.meshgrid(x, y)

dx = x[1] - x[0]
dy = y[1] - y[0]

# ============================================================
# FIELD
# ============================================================
def gauss(x0, y0, sx, sy, amp):
    return amp * np.exp(-(((X-x0)**2)/(2*sx**2) + ((Y-y0)**2)/(2*sy**2)))

V = (
    -2.0 * gauss(10.0, 25.0, 1.2, 1.0, 1.0)
    -2.3 * gauss(13.6, 26.0, 1.0, 1.0, 1.0)
    -1.0 * gauss(12.0, 24.0, 0.8, 0.9, 1.0)
    +2.0 * gauss(11.2, 28.5, 1.0, 1.0, 1.0)
)

dV_dy, dV_dx = np.gradient(V, dy, dx)
Fx_grad = -dV_dx
Fy_grad = -dV_dy

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

# ============================================================
# SAMPLING
# ============================================================
def sample(px, py, A):
    ix = np.argmin(np.abs(x - px))
    iy = np.argmin(np.abs(y - py))
    return A[iy, ix]

# ============================================================
# SIMULATION
# ============================================================
def simulate(x0, y0, vx0, vy0, steps=800, dt=0.02, damping=0.02):
    px, py = x0, y0
    vx, vy = vx0, vy0

    xs, ys = [px], [py]
    vxs, vys = [vx], [vy]

    for _ in range(steps):
        fx = sample(px, py, Fx)
        fy = sample(px, py, Fy)

        vx += dt * (fx - damping * vx)
        vy += dt * (fy - damping * vy)

        px += dt * vx
        py += dt * vy

        xs.append(px)
        ys.append(py)
        vxs.append(vx)
        vys.append(vy)

    return np.array(xs), np.array(ys), np.array(vxs), np.array(vys)

starts = [
    (8.0, 29.0, 0.6, 0.0),
    (15.0, 29.0, -0.5, 0.0),
    (9.0, 23.0, 0.4, 0.5),
    (12.5, 27.0, 0.0, -0.7),
]

trajs = [simulate(*s) for s in starts]

# ============================================================
# PLOT
# ============================================================

fig = plt.figure(figsize=(16,12))

# Q1 FIELD
ax = fig.add_subplot(231)
cf = ax.contourf(X, Y, V, levels=50, cmap="viridis")
ax.streamplot(X, Y, Fx, Fy, color=(1,1,1,0.5), density=1.1)
ax.set_title("Field")

# Q2 TRAJECTORIES
ax = fig.add_subplot(232)
cf = ax.contourf(X, Y, V, levels=50, cmap="cividis")
colors = ["cyan","orange","lime","magenta"]
for i,(xs,ys,vxs,vys) in enumerate(trajs):
    ax.plot(xs, ys, color=colors[i])
ax.set_title("Trajectories")

# Q3 PHASE SPACE
ax = fig.add_subplot(233)
for i,(xs,ys,vxs,vys) in enumerate(trajs):
    ax.plot(vxs, vys, color=colors[i])
ax.set_title("Velocity Space (vx vs vy)")

# Q4 GATE ZOOM
ax = fig.add_subplot(234)
cf = ax.contourf(X, Y, V, levels=50, cmap="plasma")
ax.set_xlim(11,13)
ax.set_ylim(24,27)
ax.set_title("Gate Region (Zoom)")

# Q5 3D LANDSCAPE
ax = fig.add_subplot(235, projection='3d')
ax.plot_surface(X, Y, V, cmap='viridis', linewidth=0, antialiased=True)
ax.set_title("Potential Landscape 3D")

plt.tight_layout()
plt.show()
