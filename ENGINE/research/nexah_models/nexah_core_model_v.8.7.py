import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# NEXAH v8.7 — Grid-Aware Elastic Lock
# ------------------------------------------------------------
# Main idea:
# - Lorenz-based projected field
# - 4 color regions: blue / green / red / grey
# - grey channel as transition axis
# - elastic axis like a "spanngurt"
# - integrated 3x3 grid in the middle field
# - angular resonance analysis
# ============================================================

# -----------------------------
# PARAMETERS
# -----------------------------
SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0

DT = 0.005
STEPS = 22000
SKIP = 2000

# channel / axis geometry
M = 0.62
B0 = 0.20
CHANNEL_WIDTH = 1.55

# soft regime cuts
LEFT_X = -5.0
RIGHT_X = 5.0

# 3x3 grid
GRID_N = 3
GRID_X = np.linspace(-2.4, 2.4, GRID_N)
GRID_Y = np.linspace(-2.4, 2.4, GRID_N)
GRID_LOCK_RADIUS = 0.90
GRID_LOCK_GAIN = 0.045

# elastic lock
ELASTIC_BASE = 0.008
ELASTIC_D_GAIN = 0.018
ELASTIC_THETA_GAIN = 0.008
ELASTIC_FAR_SCALE = 0.18

# plotting
POINT_SIZE = 5

# reproducibility
np.random.seed(7)


# ============================================================
# LORENZ STEP
# ============================================================
def lorenz_step(x, y, z, dt=DT, sigma=SIGMA, rho=RHO, beta=BETA):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return x + dt * dx, y + dt * dy, z + dt * dz


# ============================================================
# PROJECTION
# ------------------------------------------------------------
# Project Lorenz states into the NEXAH field plane
# ============================================================
def project_state(x, y, z):
    xp = 0.92 * x + 0.18 * y
    yp = 0.55 * y - 0.78 * z + 22.0
    return xp, yp


# ============================================================
# GEOMETRY HELPERS
# ============================================================
def line_y(x):
    return M * x + B0


def signed_distance_to_axis(x, y):
    return (y - (M * x + B0)) / np.sqrt(1.0 + M * M)


def closest_point_on_axis(x, y):
    # line: -M*x + y - B0 = 0
    a = -M
    b = 1.0
    c = -B0
    denom = a * a + b * b
    t = (a * x + b * y + c) / denom
    x0 = x - a * t
    y0 = y - b * t
    return x0, y0


def angle_of_point(x, y):
    th = np.degrees(np.arctan2(y, x))
    if th < 0:
        th += 360.0
    return th


def angular_velocity(theta_deg):
    th = np.unwrap(np.radians(theta_deg))
    dth = np.diff(th, prepend=th[0])
    return dth


def build_grid_points():
    pts = []
    for gx in GRID_X:
        for gy in GRID_Y:
            pts.append((gx, gy))
    return np.array(pts)


GRID_POINTS = build_grid_points()


def nearest_grid_point(x, y):
    d2 = (GRID_POINTS[:, 0] - x) ** 2 + (GRID_POINTS[:, 1] - y) ** 2
    idx = np.argmin(d2)
    return GRID_POINTS[idx], np.sqrt(d2[idx])


# ============================================================
# ELASTIC / GRID FORCES
# ============================================================
def adaptive_k(d, dtheta):
    if abs(d) < 1.5:
        k = ELASTIC_BASE + ELASTIC_D_GAIN * abs(d) + ELASTIC_THETA_GAIN * abs(dtheta)
    else:
        k = ELASTIC_BASE * ELASTIC_FAR_SCALE
    return k


def elastic_force(x, y, dtheta):
    d = signed_distance_to_axis(x, y)
    xa, ya = closest_point_on_axis(x, y)

    # base elastic attraction toward axis
    k = adaptive_k(d, dtheta)
    fx = k * (xa - x)
    fy = k * (ya - y)

    # grid attraction near channel center
    gp, gdist = nearest_grid_point(x, y)
    if abs(d) < CHANNEL_WIDTH and gdist < GRID_LOCK_RADIUS:
        lock_strength = GRID_LOCK_GAIN * (1.0 - gdist / GRID_LOCK_RADIUS)
        fx += lock_strength * (gp[0] - x)
        fy += lock_strength * (gp[1] - y)

    return fx, fy


# ============================================================
# REGION CLASSIFICATION
# ============================================================
def classify_region(x, y):
    d = signed_distance_to_axis(x, y)

    if abs(d) <= CHANNEL_WIDTH:
        return "grey"
    if x < LEFT_X:
        return "blue"
    if x > RIGHT_X:
        return "red"
    return "green"


# ============================================================
# SIMULATION
# ============================================================
def simulate():
    x, y, z = 0.1, 1.0, 1.05

    xs = []
    ys = []
    zs = []

    # raw Lorenz trajectory
    for _ in range(STEPS):
        x, y, z = lorenz_step(x, y, z)
        xs.append(x)
        ys.append(y)
        zs.append(z)

    xs = np.array(xs[SKIP:])
    ys = np.array(ys[SKIP:])
    zs = np.array(zs[SKIP:])

    # 2D projection
    xp = np.zeros_like(xs)
    yp = np.zeros_like(xs)
    for i in range(len(xs)):
        xp[i], yp[i] = project_state(xs[i], ys[i], zs[i])

    # first angular signal
    theta0 = np.array([angle_of_point(xp[i], yp[i]) for i in range(len(xp))])
    dtheta0 = angular_velocity(theta0)

    # apply elastic + grid correction
    xpc = xp.copy()
    ypc = yp.copy()

    for i in range(len(xpc)):
        fx, fy = elastic_force(xpc[i], ypc[i], dtheta0[i])
        xpc[i] += fx
        ypc[i] += fy

    # corrected angles
    theta = np.array([angle_of_point(xpc[i], ypc[i]) for i in range(len(xpc))])
    dtheta = angular_velocity(theta)

    # classify
    labels = np.array([classify_region(xpc[i], ypc[i]) for i in range(len(xpc))])

    return {
        "x": xs,
        "y": ys,
        "z": zs,
        "xp": xpc,
        "yp": ypc,
        "theta": theta,
        "dtheta": dtheta,
        "labels": labels,
    }


# ============================================================
# ANALYSIS
# ============================================================
def region_counts(labels):
    names = ["blue", "green", "red", "grey"]
    total = len(labels)
    out = {}
    for n in names:
        c = int(np.sum(labels == n))
        out[n] = (c, c / total)
    return out


# ============================================================
# PLOTTING
# ============================================================
def plot_main_field(data):
    xp = data["xp"]
    yp = data["yp"]
    labels = data["labels"]

    fig, ax = plt.subplots(figsize=(12, 9))

    mask_blue = labels == "blue"
    mask_green = labels == "green"
    mask_red = labels == "red"
    mask_grey = labels == "grey"

    ax.scatter(xp[mask_blue], yp[mask_blue], s=POINT_SIZE, c="tab:blue", label="blue", alpha=0.9, linewidths=0)
    ax.scatter(xp[mask_green], yp[mask_green], s=POINT_SIZE, c="orange", label="green", alpha=0.9, linewidths=0)
    ax.scatter(xp[mask_red], yp[mask_red], s=POINT_SIZE, c="tab:green", label="red", alpha=0.9, linewidths=0)
    ax.scatter(xp[mask_grey], yp[mask_grey], s=POINT_SIZE + 1, c="black", label="grey", alpha=0.95, linewidths=0)

    xx = np.linspace(np.min(xp) - 1.0, np.max(xp) + 1.0, 400)
    yy = line_y(xx)
    ax.plot(xx, yy, color="goldenrod", lw=2.2, label="elastic axis")

    ax.scatter(
        GRID_POINTS[:, 0],
        GRID_POINTS[:, 1],
        s=70,
        facecolors="none",
        edgecolors="magenta",
        linewidths=1.5,
        label="3x3 grid",
    )

    ax.set_title("NEXAH v8.7 — Grid-Aware Elastic Lock")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, alpha=0.35)
    ax.legend(loc="upper left")
    plt.tight_layout()
    plt.show()


def plot_grid_only(data):
    xp = data["xp"]
    yp = data["yp"]
    labels = data["labels"]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(xp, yp, s=4, c="lightsteelblue", alpha=0.08, linewidths=0)

    mask_grey = labels == "grey"
    ax.scatter(xp[mask_grey], yp[mask_grey], s=8, c="black", alpha=0.9, linewidths=0)

    ax.scatter(GRID_POINTS[:, 0], GRID_POINTS[:, 1], s=90, c="black", zorder=5)
    for i, (gx, gy) in enumerate(GRID_POINTS):
        ax.text(gx + 0.12, gy + 0.12, f"v{i}", fontsize=10, color="black")

    # connect neighbors in grid
    dx0 = GRID_X[1] - GRID_X[0]
    dy0 = GRID_Y[1] - GRID_Y[0]
    for i, (x1, y1) in enumerate(GRID_POINTS):
        for j, (x2, y2) in enumerate(GRID_POINTS):
            if j <= i:
                continue
            dx = abs(x1 - x2)
            dy = abs(y1 - y2)
            if dx <= dx0 + 1e-9 and dy <= dy0 + 1e-9:
                ax.plot([x1, x2], [y1, y2], color="gray", alpha=0.45, lw=1.3)

    ax.set_title("Grey Grid Nodes — Mycel Network")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, alpha=0.25)
    ax.set_aspect("equal", adjustable="box")
    plt.tight_layout()
    plt.show()


def plot_angular_analysis(data):
    theta = data["theta"]
    dtheta = data["dtheta"]
    labels = data["labels"]

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    axs[0, 0].hist(theta, bins=180, color="steelblue")
    axs[0, 0].axvline(135, color="tab:blue", linestyle="--")
    axs[0, 0].axvline(225, color="tab:blue", linestyle="--")
    axs[0, 0].axvline(45, color="tab:blue", linestyle="--")
    axs[0, 0].axvline(315, color="tab:blue", linestyle="--")
    axs[0, 0].set_title("Angular Distribution (Full Field)")
    axs[0, 0].set_xlabel("Degrees")
    axs[0, 0].set_ylabel("Count")

    grey_theta = theta[labels == "grey"]
    axs[0, 1].hist(grey_theta, bins=120, color="steelblue")
    axs[0, 1].axvline(135, color="tab:blue", linestyle="--")
    axs[0, 1].axvline(225, color="tab:blue", linestyle="--")
    axs[0, 1].axvline(45, color="tab:blue", linestyle="--")
    axs[0, 1].axvline(315, color="tab:blue", linestyle="--")
    axs[0, 1].set_title("Angular Distribution (Grey Channel)")
    axs[0, 1].set_xlabel("Degrees")
    axs[0, 1].set_ylabel("Count")

    axs[1, 0].plot(dtheta, lw=1.0)
    axs[1, 0].set_title("Angular Velocity dθ")
    axs[1, 0].set_xlabel("time step")

    axs[1, 1].plot(theta, lw=1.0)
    axs[1, 1].set_title("θ over time")
    axs[1, 1].set_xlabel("time step")

    plt.tight_layout()
    plt.show()


def plot_offset_overlay(data):
    xp = data["xp"]
    yp = data["yp"]
    labels = data["labels"]

    fig, ax = plt.subplots(figsize=(12, 8))

    mask_blue = labels == "blue"
    mask_green = labels == "green"
    mask_red = labels == "red"
    mask_grey = labels == "grey"

    ax.scatter(xp[mask_blue], yp[mask_blue], s=4, c="tab:blue", alpha=0.55, linewidths=0)
    ax.scatter(xp[mask_green], yp[mask_green], s=4, c="orange", alpha=0.55, linewidths=0)
    ax.scatter(xp[mask_red], yp[mask_red], s=4, c="tab:green", alpha=0.55, linewidths=0)
    ax.scatter(xp[mask_grey], yp[mask_grey], s=7, c="black", alpha=0.9, linewidths=0)

    # offset strap / spanngurt
    x1, y1 = -12.5, -14.0
    x2, y2 = 10.2, 15.4
    ax.plot([x1, x2], [y1, y2], color="goldenrod", lw=2.4)
    ax.scatter([x1, x2], [y1, y2], s=30, c=["royalblue", "lightskyblue"], edgecolors="white", linewidths=0.6, zorder=5)

    xx = np.linspace(np.min(xp) - 1.0, np.max(xp) + 1.0, 400)
    yy = line_y(xx)
    ax.plot(xx, yy, color="lightgray", lw=1.5, alpha=0.8)

    ax.set_title("NEXAH v8.7 — Offset Elastic Overlay")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, alpha=0.35)
    plt.tight_layout()
    plt.show()


# ============================================================
# MAIN
# ============================================================
def main():
    data = simulate()
    counts = region_counts(data["labels"])

    print("\n=== NEXAH v8.7 Summary ===")
    for name in ["blue", "green", "red", "grey"]:
        c, p = counts[name]
        print(f"{name}: {c} ({p:.3f})")

    print(f"\n3x3 grid nodes: {len(GRID_POINTS)}")

    plot_main_field(data)
    plot_grid_only(data)
    plot_angular_analysis(data)
    plot_offset_overlay(data)


if __name__ == "__main__":
    main()
