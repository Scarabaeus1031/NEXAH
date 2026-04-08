import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# NEXAH v8.8 — Dual Core Grid (2x2) + 3x3 Field
# ============================================================

SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0

DT = 0.005
STEPS = 22000
SKIP = 2000

# axis
M = 0.62
B0 = 0.20
CHANNEL_WIDTH = 1.5

LEFT_X = -5
RIGHT_X = 5

# -----------------------------
# GRID SYSTEMS
# -----------------------------

# 3x3 (field stabilizer)
GRID3_X = np.linspace(-2.4, 2.4, 3)
GRID3_Y = np.linspace(-2.4, 2.4, 3)

# 2x2 (core kernel)
GRID2_X = np.linspace(-1.0, 1.0, 2)
GRID2_Y = np.linspace(-1.0, 1.0, 2)

GRID3 = np.array([(x, y) for x in GRID3_X for y in GRID3_Y])
GRID2 = np.array([(x, y) for x in GRID2_X for y in GRID2_Y])

# strengths
GRID3_GAIN = 0.03
GRID2_GAIN = 0.08   # much stronger
GRID_RADIUS = 1.2

# elastic
ELASTIC_BASE = 0.008
ELASTIC_GAIN = 0.02

np.random.seed(8)

# ============================================================
# LORENZ
# ============================================================
def lorenz_step(x, y, z):
    dx = SIGMA * (y - x)
    dy = x * (RHO - z) - y
    dz = x * y - BETA * z
    return x + DT * dx, y + DT * dy, z + DT * dz


def project(x, y, z):
    xp = 0.92 * x + 0.18 * y
    yp = 0.55 * y - 0.78 * z + 22
    return xp, yp


# ============================================================
# GEOMETRY
# ============================================================
def axis_y(x):
    return M * x + B0


def dist_axis(x, y):
    return (y - (M * x + B0)) / np.sqrt(1 + M**2)


def closest_axis(x, y):
    a = -M
    b = 1
    c = -B0
    t = (a*x + b*y + c) / (a*a + b*b)
    return x - a*t, y - b*t


def nearest(pt, grid):
    d = np.sum((grid - pt)**2, axis=1)
    i = np.argmin(d)
    return grid[i], np.sqrt(d[i])


# ============================================================
# FORCES
# ============================================================
def elastic_force(x, y):
    xa, ya = closest_axis(x, y)
    d = dist_axis(x, y)
    k = ELASTIC_BASE + ELASTIC_GAIN * abs(d)
    return k * (xa - x), k * (ya - y)


def grid_force(x, y):
    fx, fy = 0, 0

    # 3x3 (soft field)
    g3, d3 = nearest((x, y), GRID3)
    if d3 < GRID_RADIUS:
        w = GRID3_GAIN * (1 - d3/GRID_RADIUS)
        fx += w * (g3[0] - x)
        fy += w * (g3[1] - y)

    # 2x2 (core lock)
    g2, d2 = nearest((x, y), GRID2)
    if d2 < GRID_RADIUS:
        w = GRID2_GAIN * (1 - d2/GRID_RADIUS)
        fx += w * (g2[0] - x)
        fy += w * (g2[1] - y)

    return fx, fy


# ============================================================
# CLASSIFY
# ============================================================
def region(x, y):
    d = dist_axis(x, y)

    if abs(d) < CHANNEL_WIDTH:
        return "grey"
    if x < LEFT_X:
        return "blue"
    if x > RIGHT_X:
        return "red"
    return "green"


# ============================================================
# SIM
# ============================================================
def simulate():
    x, y, z = 0.1, 1.0, 1.05

    pts = []

    for _ in range(STEPS):
        x, y, z = lorenz_step(x, y, z)
        pts.append((x, y, z))

    pts = pts[SKIP:]

    xp, yp = [], []

    for x, y, z in pts:
        px, py = project(x, y, z)

        fx1, fy1 = elastic_force(px, py)
        fx2, fy2 = grid_force(px, py)

        px += fx1 + fx2
        py += fy1 + fy2

        xp.append(px)
        yp.append(py)

    xp = np.array(xp)
    yp = np.array(yp)

    labels = np.array([region(xp[i], yp[i]) for i in range(len(xp))])

    return xp, yp, labels


# ============================================================
# PLOT
# ============================================================
def plot(xp, yp, labels):
    fig, ax = plt.subplots(figsize=(12, 9))

    for name, col in [("blue","tab:blue"),("green","orange"),
                      ("red","tab:green"),("grey","black")]:
        m = labels == name
        ax.scatter(xp[m], yp[m], s=5, c=col, label=name, alpha=0.9)

    # axis
    xx = np.linspace(min(xp), max(xp), 400)
    ax.plot(xx, axis_y(xx), color="goldenrod", lw=2, label="axis")

    # grids
    ax.scatter(GRID3[:,0], GRID3[:,1], s=80,
               facecolors="none", edgecolors="magenta", label="3x3")

    ax.scatter(GRID2[:,0], GRID2[:,1], s=120,
               c="cyan", label="2x2 core")

    ax.set_title("NEXAH v8.8 — Dual Core Grid (2x2 + 3x3)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.show()


# ============================================================
# MAIN
# ============================================================
def main():
    xp, yp, labels = simulate()

    total = len(labels)
    print("\n=== NEXAH v8.8 Summary ===")
    for k in ["blue","green","red","grey"]:
        c = np.sum(labels == k)
        print(f"{k}: {c} ({c/total:.3f})")

    plot(xp, yp, labels)


if __name__ == "__main__":
    main()
