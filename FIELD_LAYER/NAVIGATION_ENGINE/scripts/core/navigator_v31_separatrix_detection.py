import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(42)

# ============================================================
# 1. CLUSTER CENTERS
# ============================================================

clusters = {
    "C0": np.array([10.0, 25.0]),
    "C1": np.array([12.0, 24.0]),
    "C2": np.array([13.5, 26.0]),
    "C3": np.array([11.0, 28.5]),
}

cluster_colors = {
    "C0": "#1f77b4",
    "C1": "#ff7f0e",
    "C2": "#2ca02c",
    "C3": "#d62728",
}

cluster_order = ["C0", "C1", "C2", "C3"]


# ============================================================
# 2. FIELD DEFINITION (same logic as V29)
# ============================================================

def gaussian(x, y, center, depth, sigma=1.2):
    return depth * np.exp(-((x - center[0]) ** 2 + (y - center[1]) ** 2) / (2 * sigma ** 2))


def envelope(t):
    return 1.0 + 0.4 * np.sin(0.03 * t)


def attractor_strengths(t):
    e = envelope(t)
    return {
        "C0": 1.5 * e,
        "C1": 2.0 * (1.0 + 0.4 * np.sin(0.03 * t + np.pi / 2)),
        "C2": 3.0 * (1.0 + 0.3 * np.sin(0.03 * t)),
        "C3": -2.0,
    }


def scalar_field(x, y, t):
    strengths = attractor_strengths(t)
    val = 0.0
    for c, pos in clusters.items():
        val += gaussian(x, y, pos, strengths[c])
    return val


def grad_scalar_field(x, y, t, eps=1e-3):
    dx = (scalar_field(x + eps, y, t) - scalar_field(x - eps, y, t)) / (2 * eps)
    dy = (scalar_field(x, y + eps, t) - scalar_field(x, y - eps, t)) / (2 * eps)
    return np.array([dx, dy])


def rotational_field(x, y):
    p = np.array([x, y], dtype=float)
    v = np.zeros(2, dtype=float)

    c2 = clusters["C2"]
    r2 = p - c2
    d2 = np.linalg.norm(r2) + 1e-9
    swirl2 = np.array([r2[1], -r2[0]]) * np.exp(-(d2 ** 2) / (2 * 1.4 ** 2))
    v += 0.85 * swirl2

    c3 = clusters["C3"]
    r3 = p - c3
    d3 = np.linalg.norm(r3) + 1e-9
    swirl3 = np.array([-r3[1], r3[0]]) * np.exp(-(d3 ** 2) / (2 * 1.1 ** 2))
    v += 1.15 * swirl3

    c1 = clusters["C1"]
    mid = 0.5 * (c1 + c2)
    rm = p - mid
    dm = np.linalg.norm(rm) + 1e-9
    shear = np.array([0.0, 1.0]) * np.exp(-(dm ** 2) / (2 * 1.8 ** 2))
    v += 0.35 * shear

    return v


def combined_field(x, y, t, alpha=1.0, beta=0.65):
    v_p = grad_scalar_field(x, y, t)
    v_r = rotational_field(x, y)
    return alpha * v_p + beta * v_r


# ============================================================
# 3. TRAJECTORY / BASIN ASSIGNMENT
# ============================================================

def nearest_cluster(point):
    dists = {k: np.linalg.norm(point - c) for k, c in clusters.items()}
    return min(dists, key=dists.get)


def simulate_endpoint(start, t0=0, steps=120, dt=0.08):
    x = np.array(start, dtype=float)

    for k in range(steps):
        t = t0 + k
        v = combined_field(x[0], x[1], t)
        mag = np.linalg.norm(v)
        if mag > 1e-9:
            v = v / mag
        x = x + dt * v

    return x


# ============================================================
# 4. GRID ANALYSIS
# ============================================================

def compute_background(t=200, nx=180, ny=180):
    xs = np.linspace(6, 17, nx)
    ys = np.linspace(22, 31, ny)
    X, Y = np.meshgrid(xs, ys)
    Z = scalar_field(X, Y, t)
    return X, Y, Z


def compute_vector_grid(t=200, nx=90, ny=90):
    xs = np.linspace(6, 17, nx)
    ys = np.linspace(22, 31, ny)
    X, Y = np.meshgrid(xs, ys)

    U = np.zeros_like(X)
    V = np.zeros_like(Y)
    M = np.zeros_like(X)

    for j in range(ny):
        for i in range(nx):
            v = combined_field(X[j, i], Y[j, i], t)
            U[j, i] = v[0]
            V[j, i] = v[1]
            M[j, i] = np.linalg.norm(v)

    return X, Y, U, V, M


def compute_basin_map(nx=120, ny=120):
    xs = np.linspace(6, 17, nx)
    ys = np.linspace(22, 31, ny)
    basin = np.zeros((ny, nx), dtype=int)

    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            end = simulate_endpoint([x, y])
            c = nearest_cluster(end)
            basin[j, i] = cluster_order.index(c)

    return xs, ys, basin


def compute_boundary_map(basin):
    ny, nx = basin.shape
    boundary = np.zeros_like(basin, dtype=float)

    for j in range(1, ny - 1):
        for i in range(1, nx - 1):
            neighborhood = basin[j-1:j+2, i-1:i+2]
            if np.any(neighborhood != basin[j, i]):
                boundary[j, i] = 1.0

    boundary = gaussian_filter(boundary, sigma=0.8)
    return boundary


# ============================================================
# 5. PLOTTING
# ============================================================

def plot_v31():
    print("Running V31 Separatrix Detection...")

    Xbg, Ybg, Zbg = compute_background(t=200)
    Xv, Yv, Uv, Vv, Mv = compute_vector_grid(t=200)
    xs, ys, basin = compute_basin_map()
    boundary = compute_boundary_map(basin)

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    ax1, ax2, ax3, ax4 = axes.flatten()

    # Q1 — field magnitude / slow zones
    im1 = ax1.contourf(Xv, Yv, Mv, levels=40, cmap="viridis_r")
    slow_mask = Mv < np.percentile(Mv, 12)
    ax1.scatter(Xv[slow_mask], Yv[slow_mask], s=5, c="white", alpha=0.8, label="slow zones")

    for k, c in clusters.items():
        ax1.scatter(c[0], c[1], s=180, c=cluster_colors[k], edgecolor="black", zorder=5)
        ax1.text(c[0], c[1] + 0.18, k, color="white", ha="center", va="bottom", fontsize=11)

    ax1.set_title("Q1 — Slow Zones / Decision Regions")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    ax1.legend(loc="upper right")
    fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

    # Q2 — basin map
    cmap = plt.get_cmap("tab10", 4)
    im2 = ax2.imshow(
        basin,
        origin="lower",
        extent=[xs.min(), xs.max(), ys.min(), ys.max()],
        aspect="auto",
        cmap=cmap,
        interpolation="nearest"
    )

    for k, c in clusters.items():
        ax2.scatter(c[0], c[1], s=180, c=cluster_colors[k], edgecolor="black", zorder=5)
        ax2.text(c[0], c[1] + 0.18, k, color="white", ha="center", va="bottom", fontsize=11)

    ax2.set_title("Q2 — Basin Map (Long-Term Destination)")
    ax2.set_xlabel("α")
    ax2.set_ylabel("β")
    fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

    # Q3 — boundary map / separatrix approximation
    im3 = ax3.contourf(
        xs, ys, boundary,
        levels=35,
        cmap="magma"
    )
    ax3.contour(
        xs, ys, boundary,
        levels=[0.35],
        colors="white",
        linewidths=1.6
    )

    for k, c in clusters.items():
        ax3.scatter(c[0], c[1], s=180, c=cluster_colors[k], edgecolor="black", zorder=5)
        ax3.text(c[0], c[1] + 0.18, k, color="white", ha="center", va="bottom", fontsize=11)

    ax3.set_title("Q3 — Separatrix / Decision Boundary")
    ax3.set_xlabel("α")
    ax3.set_ylabel("β")
    fig.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)

    # Q4 — overlay basin + boundaries + streamlines
    ax4.contourf(Xbg, Ybg, Zbg, levels=45, cmap="viridis", alpha=0.88)

    # normalize vectors for streamline clarity
    mag = np.sqrt(Uv**2 + Vv**2) + 1e-9
    Un = Uv / mag
    Vn = Vv / mag

    ax4.streamplot(
        Xv, Yv, Un, Vn,
        color="white",
        density=1.8,
        linewidth=1.0,
        arrowsize=1.1
    )

    ax4.contour(
        xs, ys, boundary,
        levels=[0.35],
        colors="magenta",
        linewidths=1.8
    )

    for k, c in clusters.items():
        ax4.scatter(c[0], c[1], s=180, c=cluster_colors[k], edgecolor="black", zorder=5)
        ax4.text(c[0], c[1] + 0.18, k, color="white", ha="center", va="bottom", fontsize=11)

    ax4.set_title("Q4 — Flow + Separatrix Overlay")
    ax4.set_xlabel("α")
    ax4.set_ylabel("β")

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "v31_separatrix_detection.png")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")
    print("\nInterpretation:")
    print("- Q1 marks slow regions where the net field weakens.")
    print("- Q2 shows the basin assignment of each initial point.")
    print("- Q3 extracts boundaries between different long-term destinations.")
    print("- Q4 overlays flow lines with separatrix structure.")


if __name__ == "__main__":
    plot_v31()
