# navigator_v32_boundary_crossing_control.py

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
# 2. FIELD DEFINITION (same family as V29/V31)
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
# 3. BASIN / BOUNDARY TOOLS
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


def boundary_points(xs, ys, boundary, threshold=0.35, max_points=12):
    pts = []
    ny, nx = boundary.shape
    for j in range(ny):
        for i in range(nx):
            if boundary[j, i] >= threshold:
                pts.append((xs[i], ys[j], boundary[j, i]))

    # sort by strength descending, then greedy spatial thinning
    pts.sort(key=lambda p: -p[2])

    selected = []
    min_dist = 0.7
    for x, y, val in pts:
        keep = True
        for sx, sy, _ in selected:
            if np.hypot(x - sx, y - sy) < min_dist:
                keep = False
                break
        if keep:
            selected.append((x, y, val))
        if len(selected) >= max_points:
            break

    return selected


# ============================================================
# 4. CONTROLLED CROSSING EXPERIMENT
# ============================================================

def simulate_path(start, control=None, t0=0, steps=140, dt=0.08, noise=0.0):
    x = np.array(start, dtype=float)
    traj = [x.copy()]

    for k in range(steps):
        t = t0 + k
        v = combined_field(x[0], x[1], t)
        mag = np.linalg.norm(v)
        if mag > 1e-9:
            v = v / mag

        u = np.zeros(2)
        if control is not None:
            u = control(x, k)

        x = x + dt * (v + u) + noise * np.random.randn(2)
        traj.append(x.copy())

    return np.array(traj)


def endpoint_cluster(traj):
    return nearest_cluster(traj[-1])


def make_crossing_controller(direction, amp=0.55, duration=18):
    direction = np.array(direction, dtype=float)
    n = np.linalg.norm(direction)
    if n < 1e-9:
        direction = np.array([1.0, 0.0])
    else:
        direction = direction / n

    def controller(x, k):
        if k < duration:
            return amp * direction
        return np.zeros(2)

    return controller


def run_crossing_experiments(boundary_pts):
    results = []

    target_dir = clusters["C2"] - clusters["C3"]
    fallback_dir = clusters["C0"] - clusters["C2"]

    ctrl_to_c2 = make_crossing_controller(target_dir, amp=0.55, duration=18)
    ctrl_to_c0 = make_crossing_controller(fallback_dir, amp=0.45, duration=18)

    for x, y, strength in boundary_pts:
        start = np.array([x, y])

        base_traj = simulate_path(start, control=None)
        c_base = endpoint_cluster(base_traj)

        c2_traj = simulate_path(start, control=ctrl_to_c2)
        c_c2 = endpoint_cluster(c2_traj)

        c0_traj = simulate_path(start, control=ctrl_to_c0)
        c_c0 = endpoint_cluster(c0_traj)

        results.append({
            "start": start,
            "strength": strength,
            "base_traj": base_traj,
            "base_cluster": c_base,
            "c2_traj": c2_traj,
            "c2_cluster": c_c2,
            "c0_traj": c0_traj,
            "c0_cluster": c_c0,
        })

    return results


# ============================================================
# 5. BACKGROUND GRID
# ============================================================

def compute_background(t=200, nx=180, ny=180):
    xs = np.linspace(6, 17, nx)
    ys = np.linspace(22, 31, ny)
    X, Y = np.meshgrid(xs, ys)
    Z = scalar_field(X, Y, t)
    return X, Y, Z


def compute_vector_grid(t=200, nx=80, ny=80):
    xs = np.linspace(6, 17, nx)
    ys = np.linspace(22, 31, ny)
    X, Y = np.meshgrid(xs, ys)

    U = np.zeros_like(X)
    V = np.zeros_like(Y)

    for j in range(ny):
        for i in range(nx):
            v = combined_field(X[j, i], Y[j, i], t)
            mag = np.linalg.norm(v)
            if mag > 1e-9:
                v = v / mag
            U[j, i] = v[0]
            V[j, i] = v[1]

    return X, Y, U, V


# ============================================================
# 6. PLOTTING
# ============================================================

def plot_v32():
    print("Running V32 Boundary Crossing Control...")

    Xbg, Ybg, Zbg = compute_background()
    Xv, Yv, Uv, Vv = compute_vector_grid()

    xs, ys, basin = compute_basin_map()
    boundary = compute_boundary_map(basin)
    bpts = boundary_points(xs, ys, boundary, threshold=0.35, max_points=10)

    results = run_crossing_experiments(bpts)

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    ax1, ax2, ax3, ax4 = axes.flatten()

    # Q1 — boundary seeds
    im1 = ax1.contourf(Xbg, Ybg, Zbg, levels=45, cmap="viridis")
    ax1.contour(xs, ys, boundary, levels=[0.35], colors="magenta", linewidths=1.8)

    for x, y, _ in bpts:
        ax1.scatter(x, y, s=55, c="yellow", edgecolor="black", zorder=6)

    for k, c in clusters.items():
        ax1.scatter(c[0], c[1], s=180, c=cluster_colors[k], edgecolor="black", zorder=5)
        ax1.text(c[0], c[1] + 0.18, k, color="white", ha="center", va="bottom", fontsize=11)

    ax1.set_title("Q1 — Boundary Seeds / Injection Points")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

    # Q2 — uncontrolled endpoints
    im2 = ax2.imshow(
        basin,
        origin="lower",
        extent=[xs.min(), xs.max(), ys.min(), ys.max()],
        aspect="auto",
        cmap=plt.get_cmap("tab10", 4),
        interpolation="nearest"
    )

    for r in results:
        s = r["start"]
        ax2.scatter(s[0], s[1], s=45, c="white", edgecolor="black", zorder=6)
        end = r["base_traj"][-1]
        ax2.plot(r["base_traj"][:, 0], r["base_traj"][:, 1], color="white", lw=1.4, alpha=0.9)
        ax2.scatter(end[0], end[1], s=30, c="yellow", edgecolor="black", zorder=7)

    for k, c in clusters.items():
        ax2.scatter(c[0], c[1], s=180, c=cluster_colors[k], edgecolor="black", zorder=5)
        ax2.text(c[0], c[1] + 0.18, k, color="white", ha="center", va="bottom", fontsize=11)

    ax2.set_title("Q2 — Uncontrolled Crossing Outcomes")
    ax2.set_xlabel("α")
    ax2.set_ylabel("β")
    fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

    # Q3 — controlled push toward C2
    im3 = ax3.contourf(Xbg, Ybg, Zbg, levels=45, cmap="viridis")
    ax3.contour(xs, ys, boundary, levels=[0.35], colors="magenta", linewidths=1.4)

    for r in results:
        s = r["start"]
        ax3.scatter(s[0], s[1], s=40, c="white", edgecolor="black", zorder=6)
        ax3.plot(r["c2_traj"][:, 0], r["c2_traj"][:, 1], color="cyan", lw=1.5, alpha=0.9)
        end = r["c2_traj"][-1]
        ax3.scatter(end[0], end[1], s=28, c="yellow", edgecolor="black", zorder=7)

    for k, c in clusters.items():
        ax3.scatter(c[0], c[1], s=180, c=cluster_colors[k], edgecolor="black", zorder=5)
        ax3.text(c[0], c[1] + 0.18, k, color="white", ha="center", va="bottom", fontsize=11)

    ax3.set_title("Q3 — Minimal Injection Toward C2")
    ax3.set_xlabel("α")
    ax3.set_ylabel("β")

    # Q4 — success histogram
    base_counts = {k: 0 for k in cluster_order}
    c2_counts = {k: 0 for k in cluster_order}
    c0_counts = {k: 0 for k in cluster_order}

    for r in results:
        base_counts[r["base_cluster"]] += 1
        c2_counts[r["c2_cluster"]] += 1
        c0_counts[r["c0_cluster"]] += 1

    idx = np.arange(len(cluster_order))
    w = 0.25

    ax4.bar(idx - w, [base_counts[k] for k in cluster_order], width=w, label="base")
    ax4.bar(idx,     [c2_counts[k] for k in cluster_order], width=w, label="push→C2")
    ax4.bar(idx + w, [c0_counts[k] for k in cluster_order], width=w, label="push→C0")

    ax4.set_xticks(idx)
    ax4.set_xticklabels(cluster_order)
    ax4.set_title("Q4 — Endpoint Basin Counts")
    ax4.set_xlabel("final basin")
    ax4.set_ylabel("count")
    ax4.legend()

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "v32_boundary_crossing_control.png")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")
    print("\nBoundary seed results:")
    for i, r in enumerate(results):
        s = r["start"]
        print(
            f"  seed {i:02d} @ ({s[0]:.2f}, {s[1]:.2f}) | "
            f"base={r['base_cluster']} | push→C2={r['c2_cluster']} | push→C0={r['c0_cluster']}"
        )


if __name__ == "__main__":
    plot_v32()
