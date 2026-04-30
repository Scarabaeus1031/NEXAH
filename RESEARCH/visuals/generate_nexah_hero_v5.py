import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================
# SYSTEM DEFINITIONS
# ============================================

def lorenz_step(x, y, z, s=10, r=28, b=8/3):
    dx = s * (y - x)
    dy = x * (r - z) - y
    dz = x * y - b * z
    return dx, dy, dz


def halvorsen_step(x, y, z, a=1.4):
    dx = -a*x - 4*y - 4*z - y*y
    dy = -a*y - 4*z - 4*x - z*z
    dz = -a*z - 4*x - 4*y - x*x
    return dx, dy, dz


def rossler_step(x, y, z, a=0.2, b=0.2, c=5.7):
    dx = -y - z
    dy = x + a*y
    dz = b + z*(x - c)
    return dx, dy, dz


# ============================================
# SIMULATION (STABLE)
# ============================================

def simulate(system_func, steps=20000, dt=0.01, burn=2000, init=(0.1,0,0)):
    xs = np.empty(steps)
    ys = np.empty(steps)
    zs = np.empty(steps)

    xs[0], ys[0], zs[0] = init

    for i in range(steps - 1):
        dx, dy, dz = system_func(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx * dt
        ys[i+1] = ys[i] + dy * dt
        zs[i+1] = zs[i] + dz * dt

        # --- stability guard ---
        if not np.isfinite(xs[i+1]) or not np.isfinite(ys[i+1]):
            xs = xs[:i]
            ys = ys[:i]
            zs = zs[:i]
            break

    return xs[burn:], ys[burn:], zs[burn:]


# ============================================
# STRUCTURE EXTRACTION (ROBUST)
# ============================================

def extract_structure(xs, ys):

    # --- CLEAN ---
    mask = np.isfinite(xs) & np.isfinite(ys)
    xs = xs[mask]
    ys = ys[mask]

    # --- CLIP EXTREMES ---
    xs = np.clip(xs, -50, 50)
    ys = np.clip(ys, -50, 50)

    # --- KDE ---
    points = np.vstack([xs, ys])

    if points.shape[1] < 100:
        raise ValueError("Too few valid points for KDE")

    kde = gaussian_kde(points)

    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()

    X, Y = np.mgrid[xmin:xmax:250j, ymin:ymax:250j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    Z = np.reshape(kde(positions).T, X.shape)

    # gradient
    dZdx, dZdy = np.gradient(Z)

    return xs, ys, X, Y, Z, dZdx, dZdy


# ============================================
# RUN SYSTEMS
# ============================================

systems = [
    ("Lorenz", lorenz_step, 0.01),
    ("Halvorsen", halvorsen_step, 0.002),   # 🔥 key fix
    ("Rössler", rossler_step, 0.01),
]

results = []

for name, system, dt in systems:
    xs, ys, zs = simulate(system, dt=dt)

    if len(xs) < 1000:
        print(f"[WARN] {name} unstable, skipping")
        continue

    xs, ys, X, Y, Z, dZdx, dZdy = extract_structure(xs, ys)
    results.append((name, xs, ys, X, Y, Z, dZdx, dZdy))


# ============================================
# PLOTTING
# ============================================

fig, axes = plt.subplots(3, len(results), figsize=(5 * len(results), 14))

for i, (name, xs, ys, X, Y, Z, dZdx, dZdy) in enumerate(results):

    # --- Row 1: Trajectory ---
    axes[0, i].plot(xs, ys, lw=0.4, alpha=0.7)
    axes[0, i].set_title(f"{name}\nRaw Dynamics")
    axes[0, i].set_xticks([])
    axes[0, i].set_yticks([])

    # --- Row 2: Density ---
    axes[1, i].imshow(np.rot90(Z),
                      extent=[xs.min(), xs.max(), ys.min(), ys.max()])
    axes[1, i].set_title("Density Field")
    axes[1, i].set_xticks([])
    axes[1, i].set_yticks([])

    # --- Row 3: Structure ---
    axes[2, i].imshow(np.rot90(Z),
                      extent=[xs.min(), xs.max(), ys.min(), ys.max()],
                      alpha=0.7)

    skip = (slice(None, None, 12), slice(None, None, 12))

    axes[2, i].quiver(
        X[skip], Y[skip],
        dZdx[skip], dZdy[skip],
        alpha=0.6,
        scale=40
    )

    axes[2, i].plot(xs, ys, lw=0.6)

    # --- gate heuristic ---
    idx = np.argmin(Z.flatten())
    gx = X.flatten()[idx]
    gy = Y.flatten()[idx]

    axes[2, i].scatter(gx, gy, s=40)

    axes[2, i].set_title("Structure + Flow + Gate")
    axes[2, i].set_xticks([])
    axes[2, i].set_yticks([])


# ============================================
# TITLE
# ============================================

fig.suptitle(
    "NEXAH v5 (Clean) — Cross-System Structure Extraction",
    fontsize=16
)

plt.tight_layout()

# ============================================
# SAVE
# ============================================

out_path = "RESEARCH/visuals/nexah_structure_cross_system_v5_clean.png"

plt.savefig(out_path, dpi=300, bbox_inches='tight')

print(f"Saved to: {out_path}")

plt.show()
