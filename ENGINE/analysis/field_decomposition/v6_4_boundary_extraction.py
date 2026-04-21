import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, gaussian_gradient_magnitude, label

# ============================================================
# NEXAH V6.4 — Boundary Extraction Engine
# ------------------------------------------------------------
# Goal:
#   Extract dynamical structure from orbit classification:
#   - robust orbit / capture / escape classes
#   - separatrix-like boundaries
#   - orbit bands
#   - gate sensitivity map
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
    return amp * np.exp(-(((X - x0)**2)/(2*sx**2) + ((Y - y0)**2)/(2*sy**2)))

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
source_center = np.array([11.2, 28.5])
launch_center = np.array([11.6, 25.5])

def dist(px, py, c):
    return np.sqrt((px - c[0])**2 + (py - c[1])**2)


# ============================================================
# SIMULATION
# ============================================================

def simulate(x0, y0, vx0, vy0, steps=1200, dt=0.02, damping=0.02):
    px, py = x0, y0
    vx, vy = vx0, vy0

    xs, ys = [px], [py]
    energies = []

    escaped = False

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

        E = 0.5 * (vx**2 + vy**2) + pot
        energies.append(E)

        if not inside(px, py):
            escaped = True
            break

    return np.array(xs), np.array(ys), np.array(energies), escaped


# ============================================================
# ROBUST CLASSIFICATION
# ------------------------------------------------------------
# 0 = escape
# 1 = orbit / bounded
# 2 = capture left
# 3 = capture right
# 4 = source / repelled upward region (optional)
# ============================================================

def classify(xs, ys, escaped):
    # Quick escape
    if escaped and len(xs) < 220:
        return 0

    x_end, y_end = xs[-1], ys[-1]

    dL = dist(x_end, y_end, left_center)
    dR = dist(x_end, y_end, right_center)
    dS = dist(x_end, y_end, source_center)

    # Capture if final state sits close to basin centers
    if dL < 0.42:
        return 2
    if dR < 0.42:
        return 3

    # Source-like / repelled region
    if dS < 0.55 and y_end > 27.8:
        return 4

    # Orbit / bounded class:
    # use span + mean radius from launch center + non-escape duration
    span_x = xs.max() - xs.min()
    span_y = ys.max() - ys.min()
    radial = np.sqrt((xs - launch_center[0])**2 + (ys - launch_center[1])**2)

    if (len(xs) > 300) and (span_x < 7.5) and (span_y < 7.5) and (radial.mean() < 4.0):
        return 1

    # Delayed escape counts as transition / orbit-like here
    if not escaped:
        return 1

    return 0


# ============================================================
# SCAN INITIAL CONDITIONS
# ============================================================

n_theta = 96
n_r = 8

theta_vals = np.linspace(0, 2*np.pi, n_theta, endpoint=False)
r_vals = np.linspace(0.65, 1.95, n_r)

class_map = np.zeros((n_r, n_theta), dtype=int)
final_dist_map = np.zeros((n_r, n_theta), dtype=float)
lifetime_map = np.zeros((n_r, n_theta), dtype=float)

representatives = {0: None, 1: None, 2: None, 3: None, 4: None}

for i, r in enumerate(r_vals):
    for j, th in enumerate(theta_vals):
        x0 = launch_center[0] + r * np.cos(th)
        y0 = launch_center[1] + r * np.sin(th)

        # tangential launch
        vx0 = -0.58 * np.sin(th)
        vy0 =  0.58 * np.cos(th)

        xs, ys, E, escaped = simulate(x0, y0, vx0, vy0)
        cls = classify(xs, ys, escaped)

        class_map[i, j] = cls
        final_dist_map[i, j] = np.sqrt((xs[-1] - launch_center[0])**2 + (ys[-1] - launch_center[1])**2)
        lifetime_map[i, j] = len(xs)

        if representatives[cls] is None:
            representatives[cls] = (xs, ys)


# ============================================================
# BOUNDARY / BAND EXTRACTION
# ============================================================

# 1) separatrix-like boundary:
# boundary where neighboring classes differ
boundary = np.zeros_like(class_map, dtype=float)

for i in range(n_r):
    for j in range(n_theta):
        c = class_map[i, j]
        nbrs = []
        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ii = np.clip(i + di, 0, n_r - 1)
            jj = (j + dj) % n_theta
            nbrs.append(class_map[ii, jj])
        if any(nn != c for nn in nbrs):
            boundary[i, j] = 1.0

boundary_s = gaussian_filter(boundary, sigma=1.0)

# 2) orbit band score from class=1 density
orbit_mask = (class_map == 1).astype(float)
orbit_band = gaussian_filter(orbit_mask, sigma=1.0)

# 3) gate sensitivity = gradient of final distance + gradient of lifetime
fd_grad = gaussian_gradient_magnitude(final_dist_map, sigma=1.0)
lt_grad = gaussian_gradient_magnitude(lifetime_map, sigma=1.0)
gate_sensitivity = fd_grad + 0.5 * lt_grad


# ============================================================
# PROJECT TO PHYSICAL SPACE
# ============================================================

PX = np.zeros_like(class_map, dtype=float)
PY = np.zeros_like(class_map, dtype=float)

for i, r in enumerate(r_vals):
    for j, th in enumerate(theta_vals):
        PX[i, j] = launch_center[0] + r * np.cos(th)
        PY[i, j] = launch_center[1] + r * np.sin(th)


# ============================================================
# PLOTTING
# ============================================================

fig, axs = plt.subplots(2, 3, figsize=(18, 12))

# ------------------------------------------------------------
# Q1 — Class map
# ------------------------------------------------------------
ax = axs[0, 0]
im = ax.imshow(class_map, aspect='auto', origin='lower', cmap='viridis')
ax.set_title("Q1 — Orbit / Capture Class Map")
ax.set_xlabel("theta index")
ax.set_ylabel("radius index")
cbar = plt.colorbar(im, ax=ax)
cbar.set_label("0=escape, 1=orbit, 2=left, 3=right, 4=source")

# ------------------------------------------------------------
# Q2 — Final distance map
# ------------------------------------------------------------
ax = axs[0, 1]
im = ax.imshow(final_dist_map, aspect='auto', origin='lower', cmap='magma')
ax.set_title("Q2 — Final Distance Map")
ax.set_xlabel("theta index")
ax.set_ylabel("radius index")
cbar = plt.colorbar(im, ax=ax)
cbar.set_label("final distance from launch center")

# ------------------------------------------------------------
# Q3 — Boundary extraction in scan space
# ------------------------------------------------------------
ax = axs[0, 2]
im = ax.imshow(boundary_s, aspect='auto', origin='lower', cmap='coolwarm')
ax.contour(boundary_s, levels=[0.25, 0.5, 0.75], colors='black', linewidths=0.8)
ax.set_title("Q3 — Boundary / Separatrix Score")
ax.set_xlabel("theta index")
ax.set_ylabel("radius index")
cbar = plt.colorbar(im, ax=ax)
cbar.set_label("boundary intensity")

# ------------------------------------------------------------
# Q4 — Class projection in physical space
# ------------------------------------------------------------
ax = axs[1, 0]
cf = ax.contourf(X, Y, V, levels=50, cmap='cividis')

colors = {
    0: "orange",
    1: "cyan",
    2: "lime",
    3: "magenta",
    4: "red",
}

for i in range(n_r):
    for j in range(n_theta):
        ax.scatter(PX[i, j], PY[i, j], s=20, color=colors[class_map[i, j]])

# overlay extracted boundary in physical space
ax.contour(PX, PY, boundary_s, levels=[0.45], colors='white', linewidths=2.0)
ax.contour(PX, PY, orbit_band, levels=[0.45, 0.65], colors='yellow', linewidths=1.2)

# centers
ax.scatter(*left_center, s=120, color="white", edgecolor="black")
ax.text(left_center[0] + 0.12, left_center[1] + 0.12, "C0", color="white")

ax.scatter(*right_center, s=120, color="white", edgecolor="black")
ax.text(right_center[0] + 0.12, right_center[1] + 0.12, "C2", color="white")

ax.scatter(*source_center, s=120, color="red", edgecolor="black")
ax.text(source_center[0] + 0.12, source_center[1] + 0.12, "M0", color="white")

ax.scatter(*launch_center, s=120, color="yellow", edgecolor="black")
ax.text(launch_center[0] + 0.12, launch_center[1] + 0.12, "launch", color="black")

ax.set_title("Q4 — Physical Projection + Extracted Boundaries")
ax.set_xlabel("α")
ax.set_ylabel("β")
plt.colorbar(cf, ax=ax)

# ------------------------------------------------------------
# Q5 — Gate sensitivity map
# ------------------------------------------------------------
ax = axs[1, 1]
cf = ax.contourf(PX, PY, gate_sensitivity, levels=40, cmap='plasma')
ax.contour(PX, PY, boundary_s, levels=[0.45], colors='cyan', linewidths=1.4)
ax.scatter(*launch_center, s=100, color='white', edgecolor='black')
ax.set_title("Q5 — Gate Sensitivity / Switching Zone")
ax.set_xlabel("α")
ax.set_ylabel("β")
plt.colorbar(cf, ax=ax)

# ------------------------------------------------------------
# Q6 — Representative trajectories
# ------------------------------------------------------------
ax = axs[1, 2]
ax.set_title("Q6 — Representative Trajectories")
ax.set_xlabel("x")
ax.set_ylabel("y")

for cls, tr in representatives.items():
    if tr is not None:
        xs, ys = tr
        ax.plot(xs, ys, color=colors[cls], linewidth=2, label=f"class {cls}")

ax.legend(loc='best')

plt.suptitle("NEXAH V6.4 — Boundary Extraction Engine", fontsize=15)
plt.tight_layout()
plt.show()
