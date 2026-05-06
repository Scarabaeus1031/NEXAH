# navigator_v33_control_energy_field.py

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
# 2. FIELD DEFINITION
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
# 3. TRAJECTORY + BASIN
# ============================================================

def nearest_cluster(point):
    dists = {k: np.linalg.norm(point - c) for k, c in clusters.items()}
    return min(dists, key=dists.get)

def simulate_endpoint(start, control=None, t0=0, steps=120, dt=0.08):
    x = np.array(start, dtype=float)

    for k in range(steps):
        t = t0 + k
        v = combined_field(x[0], x[1], t)
        mag = np.linalg.norm(v)
        if mag > 1e-9:
            v = v / mag

        u = np.zeros(2)
        if control is not None:
            u = control(x, k)

        x = x + dt * (v + u)

    return x

def simulate_path(start, control=None, t0=0, steps=120, dt=0.08):
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

        x = x + dt * (v + u)
        traj.append(x.copy())

    return np.array(traj)

# ============================================================
# 4. CONTROL MODEL
# ============================================================

def make_constant_controller(direction, amp=0.2, duration=18):
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

def minimal_energy_to_target(start, target_cluster="C2",
                             amp_values=None,
                             duration_values=None):
    if amp_values is None:
        amp_values = np.linspace(0.0, 0.8, 17)
    if duration_values is None:
        duration_values = [4, 8, 12, 18, 24, 32]

    direction = clusters[target_cluster] - np.array(start, dtype=float)

    best_energy = None
    best_amp = None
    best_duration = None
    best_traj = None

    for duration in duration_values:
        for amp in amp_values:
            ctrl = make_constant_controller(direction, amp=amp, duration=duration)
            end = simulate_endpoint(start, control=ctrl)
            final_cluster = nearest_cluster(end)

            if final_cluster == target_cluster:
                energy = amp * amp * duration
                if best_energy is None or energy < best_energy:
                    best_energy = energy
                    best_amp = amp
                    best_duration = duration
                    best_traj = simulate_path(start, control=ctrl)

    return best_energy, best_amp, best_duration, best_traj

# ============================================================
# 5. ENERGY GRID
# ============================================================

def compute_background(t=200, nx=180, ny=180):
    xs = np.linspace(6, 17, nx)
    ys = np.linspace(22, 31, ny)
    X, Y = np.meshgrid(xs, ys)
    Z = scalar_field(X, Y, t)
    return X, Y, Z

def compute_energy_map(target_cluster="C2", nx=42, ny=42):
    xs = np.linspace(6, 17, nx)
    ys = np.linspace(22, 31, ny)

    E = np.full((ny, nx), np.nan)
    A = np.full((ny, nx), np.nan)
    D = np.full((ny, nx), np.nan)
    basin = np.zeros((ny, nx), dtype=int)

    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            start = np.array([x, y], dtype=float)
            basin[j, i] = cluster_order.index(nearest_cluster(simulate_endpoint(start)))

            best_energy, best_amp, best_duration, _ = minimal_energy_to_target(
                start, target_cluster=target_cluster
            )

            if best_energy is not None:
                E[j, i] = best_energy
                A[j, i] = best_amp
                D[j, i] = best_duration

    return xs, ys, E, A, D, basin

# ============================================================
# 6. REPRESENTATIVE TRAJECTORIES
# ============================================================

def choose_representative_points(xs, ys, E, num_points=6):
    pts = []
    ny, nx = E.shape

    valid = []
    for j in range(ny):
        for i in range(nx):
            if not np.isnan(E[j, i]):
                valid.append((xs[i], ys[j], E[j, i]))

    valid.sort(key=lambda p: p[2], reverse=True)

    min_dist = 1.2
    for x, y, e in valid:
        keep = True
        for sx, sy, _ in pts:
            if np.hypot(x - sx, y - sy) < min_dist:
                keep = False
                break
        if keep:
            pts.append((x, y, e))
        if len(pts) >= num_points:
            break

    return pts

# ============================================================
# 7. PLOTTING
# ============================================================

def plot_v33():
    print("Running V33 Control Energy Field...")

    Xbg, Ybg, Zbg = compute_background()
    xs, ys, E, A, D, basin = compute_energy_map(target_cluster="C2")

    # smooth only for display
    E_display = np.array(E, copy=True)
    valid_mask = ~np.isnan(E_display)
    if np.any(valid_mask):
        fill_val = np.nanmax(E_display[valid_mask])
        E_filled = np.where(valid_mask, E_display, fill_val)
        E_display = gaussian_filter(E_filled, sigma=0.8)
        E_display[~valid_mask] = np.nan

    reps = choose_representative_points(xs, ys, E, num_points=6)

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    ax1, ax2, ax3, ax4 = axes.flatten()

    # Q1 — energy field
    im1 = ax1.contourf(xs, ys, E_display, levels=35, cmap="magma")
    for k, c in clusters.items():
        ax1.scatter(c[0], c[1], s=180, c=cluster_colors[k], edgecolor="black", zorder=5)
        ax1.text(c[0], c[1] + 0.18, k, color="white", ha="center", va="bottom", fontsize=11)

    for x, y, e in reps:
        ax1.scatter(x, y, s=45, c="cyan", edgecolor="black", zorder=6)

    ax1.set_title("Q1 — Minimal Control Energy to Reach C2")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

    # Q2 — amplitude map
    im2 = ax2.contourf(xs, ys, A, levels=20, cmap="viridis")
    for k, c in clusters.items():
        ax2.scatter(c[0], c[1], s=180, c=cluster_colors[k], edgecolor="black", zorder=5)
        ax2.text(c[0], c[1] + 0.18, k, color="white", ha="center", va="bottom", fontsize=11)

    ax2.set_title("Q2 — Minimal Injection Amplitude")
    ax2.set_xlabel("α")
    ax2.set_ylabel("β")
    fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

    # Q3 — duration map
    im3 = ax3.contourf(xs, ys, D, levels=np.arange(0, 36, 4), cmap="cividis")
    for k, c in clusters.items():
        ax3.scatter(c[0], c[1], s=180, c=cluster_colors[k], edgecolor="black", zorder=5)
        ax3.text(c[0], c[1] + 0.18, k, color="white", ha="center", va="bottom", fontsize=11)

    ax3.set_title("Q3 — Minimal Injection Duration")
    ax3.set_xlabel("α")
    ax3.set_ylabel("β")
    fig.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)

    # Q4 — representative controlled paths
    ax4.contourf(Xbg, Ybg, Zbg, levels=45, cmap="viridis", alpha=0.9)

    for x, y, e in reps:
        best_energy, best_amp, best_duration, best_traj = minimal_energy_to_target(
            [x, y], target_cluster="C2"
        )
        if best_traj is not None:
            ax4.plot(best_traj[:, 0], best_traj[:, 1], color="cyan", lw=1.5, alpha=0.9)
            ax4.scatter(x, y, s=40, c="white", edgecolor="black", zorder=6)
            ax4.scatter(best_traj[-1, 0], best_traj[-1, 1], s=30, c="yellow", edgecolor="black", zorder=7)

    for k, c in clusters.items():
        ax4.scatter(c[0], c[1], s=180, c=cluster_colors[k], edgecolor="black", zorder=5)
        ax4.text(c[0], c[1] + 0.18, k, color="white", ha="center", va="bottom", fontsize=11)

    ax4.set_title("Q4 — Minimal-Energy Controlled Paths to C2")
    ax4.set_xlabel("α")
    ax4.set_ylabel("β")

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "v33_control_energy_field.png")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")
    print("\nRepresentative minimal-energy paths:")
    for i, (x, y, e) in enumerate(reps):
        best_energy, best_amp, best_duration, _ = minimal_energy_to_target(
            [x, y], target_cluster="C2"
        )
        print(
            f"  point {i:02d} @ ({x:.2f}, {y:.2f}) | "
            f"E={best_energy:.3f}, amp={best_amp:.3f}, duration={best_duration}"
        )

if __name__ == "__main__":
    plot_v33()
