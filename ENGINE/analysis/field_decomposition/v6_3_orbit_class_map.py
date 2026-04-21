import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# NEXAH V6.3 — Orbit Class Map
# ------------------------------------------------------------
# Classifies initial conditions into:
#   0 = escape
#   1 = bounded / orbit-like
#   2 = captured in left basin
#   3 = captured in right basin
#
# This is a practical classification layer on top of the V6 physics model.
# ============================================================


# ============================================================
# FIELD SETUP
# ============================================================

x = np.linspace(6, 17, 220)
y = np.linspace(22, 31, 220)
X, Y = np.meshgrid(x, y)

dx = x[1] - x[0]
dy = y[1] - y[0]

def gauss(x0, y0, sx, sy, amp):
    return amp * np.exp(-(((X-x0)**2)/(2*sx**2) + ((Y-y0)**2)/(2*sy**2)))

V = (
    -2.0 * gauss(10.0, 25.0, 1.2, 1.0, 1.0)   # C0
    -2.3 * gauss(13.6, 26.0, 1.0, 1.0, 1.0)   # C2
    -1.0 * gauss(12.0, 24.0, 0.8, 0.9, 1.0)   # C1
    +2.0 * gauss(11.2, 28.5, 1.0, 1.0, 1.0)   # M0
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

Rx1, Ry1 = rotation((10.0, 25.0), 2.0)
Rx2, Ry2 = rotation((13.6, 26.0), -2.0)

Fx = Fx_grad + Rx1 + Rx2
Fy = Fy_grad + Ry1 + Ry2


# ============================================================
# HELPERS
# ============================================================

def sample(px, py, A):
    ix = np.argmin(np.abs(x - px))
    iy = np.argmin(np.abs(y - py))
    return A[iy, ix]

def inside(px, py):
    return (x.min() <= px <= x.max()) and (y.min() <= py <= y.max())

left_center = np.array([10.0, 25.0])
right_center = np.array([13.6, 26.0])

def dist_to_center(px, py, center):
    return np.sqrt((px-center[0])**2 + (py-center[1])**2)


# ============================================================
# PHYSICS SIMULATION
# ============================================================

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

        if not inside(px, py):
            break

    return np.array(xs), np.array(ys), np.array(energies)


# ============================================================
# CLASSIFICATION
# ============================================================

def classify(xs, ys):
    # escaped?
    if not inside(xs[-1], ys[-1]):
        return 0

    # captured?
    dL = dist_to_center(xs[-1], ys[-1], left_center)
    dR = dist_to_center(xs[-1], ys[-1], right_center)

    if dL < 0.45:
        return 2
    if dR < 0.45:
        return 3

    # bounded?
    span_x = xs.max() - xs.min()
    span_y = ys.max() - ys.min()

    if span_x < 3.5 and span_y < 3.5:
        return 1

    # default: bounded / transition-like
    return 1


# ============================================================
# SCAN INITIAL CONDITIONS
# ------------------------------------------------------------
# We launch from a ring around the central region with tangential velocity.
# ============================================================

n_theta = 80
n_r = 5

theta_vals = np.linspace(0, 2*np.pi, n_theta, endpoint=False)
r_vals = np.linspace(0.8, 1.5, n_r)

center = np.array([11.6, 25.5])

class_map = np.zeros((n_r, n_theta), dtype=int)
final_dist_map = np.zeros((n_r, n_theta), dtype=float)

representatives = {0: None, 1: None, 2: None, 3: None}

for i, r in enumerate(r_vals):
    for j, th in enumerate(theta_vals):
        x0 = center[0] + r*np.cos(th)
        y0 = center[1] + r*np.sin(th)

        # tangential launch
        vx0 = -0.55*np.sin(th)
        vy0 =  0.55*np.cos(th)

        xs, ys, E = simulate(x0, y0, vx0, vy0, steps=900, dt=0.02, damping=0.02)
        cls = classify(xs, ys)
        class_map[i, j] = cls

        final_dist_map[i, j] = np.sqrt((xs[-1]-center[0])**2 + (ys[-1]-center[1])**2)

        if representatives[cls] is None:
            representatives[cls] = (xs, ys)


# ============================================================
# PLOTS
# ============================================================

fig, axs = plt.subplots(2, 2, figsize=(14, 12))

# ------------------------------------------------------------
# Q1 — Class map in (r, theta) coordinates
# ------------------------------------------------------------
ax = axs[0, 0]
im = ax.imshow(class_map, aspect='auto', origin='lower', cmap='viridis')
ax.set_title("Orbit Class Map")
ax.set_xlabel("theta index")
ax.set_ylabel("radius index")
cbar = plt.colorbar(im, ax=ax)
cbar.set_label("0=escape, 1=orbit, 2=left capture, 3=right capture")

# ------------------------------------------------------------
# Q2 — Final distance map
# ------------------------------------------------------------
ax = axs[0, 1]
im = ax.imshow(final_dist_map, aspect='auto', origin='lower', cmap='magma')
ax.set_title("Final Distance Map")
ax.set_xlabel("theta index")
ax.set_ylabel("radius index")
cbar = plt.colorbar(im, ax=ax)
cbar.set_label("final distance from launch center")

# ------------------------------------------------------------
# Q3 — Class map projected into physical space
# ------------------------------------------------------------
ax = axs[1, 0]
cf = ax.contourf(X, Y, V, levels=50, cmap='cividis')

colors = {
    0: "orange",
    1: "cyan",
    2: "lime",
    3: "magenta",
}

for i, r in enumerate(r_vals):
    for j, th in enumerate(theta_vals):
        x0 = center[0] + r*np.cos(th)
        y0 = center[1] + r*np.sin(th)
        ax.scatter(x0, y0, s=18, color=colors[class_map[i, j]])

ax.scatter(*left_center, s=100, color="white", edgecolor="black")
ax.text(left_center[0]+0.12, left_center[1]+0.12, "C0", color="white")

ax.scatter(*right_center, s=100, color="white", edgecolor="black")
ax.text(right_center[0]+0.12, right_center[1]+0.12, "C2", color="white")

ax.scatter(11.2, 28.5, s=100, color="red", edgecolor="black")
ax.text(11.32, 28.62, "M0", color="white")

ax.set_title("Class Projection in Physical Space")
ax.set_xlabel("α")
ax.set_ylabel("β")
plt.colorbar(cf, ax=ax)

# ------------------------------------------------------------
# Q4 — Representative trajectories
# ------------------------------------------------------------
ax = axs[1, 1]
ax.set_title("Representative Trajectories")
ax.set_xlabel("x")
ax.set_ylabel("y")

for cls, tr in representatives.items():
    if tr is not None:
        xs, ys = tr
        ax.plot(xs, ys, color=colors[cls], linewidth=2, label=f"class {cls}")

ax.legend()

plt.suptitle("NEXAH V6.3 — Orbit Boundary / Class Map", fontsize=14)
plt.tight_layout()
plt.show()
