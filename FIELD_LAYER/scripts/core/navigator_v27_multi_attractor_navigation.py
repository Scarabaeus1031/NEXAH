import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(42)

# ============================================================
# 1. CLUSTER / ATTRACTOR CENTERS
# ============================================================

cluster_centers = {
    "C0": np.array([10.0, 25.0]),   # fallback
    "C1": np.array([12.0, 24.0]),   # corridor / worker
    "C2": np.array([13.5, 26.0]),   # primary target
    "C3": np.array([11.0, 28.5]),   # high / risky
}

cluster_colors = {
    "C0": "#1f77b4",
    "C1": "#d62728",
    "C2": "#e377c2",
    "C3": "#17becf",
}

# ============================================================
# 2. MULTI-ATTRACTOR POTENTIAL
# ============================================================

def gaussian_well(x, center, sigma=1.0, depth=1.0):
    d2 = np.sum((x - center) ** 2)
    return -depth * np.exp(-d2 / (2 * sigma**2))

def gaussian_hill(x, center, sigma=1.0, height=1.0):
    d2 = np.sum((x - center) ** 2)
    return height * np.exp(-d2 / (2 * sigma**2))

def potential(x, mode="seek_C2"):
    """
    Multi-attractor landscape.
    Each mode reshapes preference among attractors.
    """
    c0 = cluster_centers["C0"]
    c1 = cluster_centers["C1"]
    c2 = cluster_centers["C2"]
    c3 = cluster_centers["C3"]

    V = 0.0

    # shared structure
    V += gaussian_well(x, c0, sigma=0.9, depth=0.8)
    V += gaussian_well(x, c1, sigma=0.8, depth=0.9)
    V += gaussian_well(x, c2, sigma=0.9, depth=1.0)

    # C3 is treated as risky hill in most modes
    V += gaussian_hill(x, c3, sigma=0.9, height=1.2)

    # mode-specific emphasis
    if mode == "seek_C2":
        V += gaussian_well(x, c2, sigma=0.8, depth=1.8)
        V += gaussian_hill(x, c3, sigma=0.8, height=0.6)

    elif mode == "seek_C1":
        V += gaussian_well(x, c1, sigma=0.8, depth=1.8)
        V += gaussian_hill(x, c3, sigma=0.8, height=0.4)

    elif mode == "fallback_C0":
        V += gaussian_well(x, c0, sigma=0.8, depth=2.0)
        V += gaussian_hill(x, c3, sigma=0.8, height=0.4)

    elif mode == "balanced":
        V += gaussian_well(x, c1, sigma=0.9, depth=0.8)
        V += gaussian_well(x, c2, sigma=0.9, depth=0.8)

    return V

def grad_potential(x, mode="seek_C2", eps=1e-3):
    """
    Finite-difference gradient of multi-attractor potential.
    """
    gx = (potential(np.array([x[0] + eps, x[1]]), mode) -
          potential(np.array([x[0] - eps, x[1]]), mode)) / (2 * eps)

    gy = (potential(np.array([x[0], x[1] + eps]), mode) -
          potential(np.array([x[0], x[1] - eps]), mode)) / (2 * eps)

    return np.array([gx, gy])

# ============================================================
# 3. FLOW CONTROL
# ============================================================

def flow_step(x, mode="seek_C2", dt=0.08, noise=0.025):
    grad = grad_potential(x, mode=mode)

    # downhill
    dx = -grad

    # small damping toward moderate motion
    dx *= 0.9

    # small noise to keep it dynamic
    dx += noise * np.random.randn(2)

    return x + dt * dx

def nearest_cluster(x):
    dists = {k: np.linalg.norm(x - v) for k, v in cluster_centers.items()}
    return min(dists, key=dists.get)

# ============================================================
# 4. SIMULATIONS
# ============================================================

def run_single_mode(mode="seek_C2", start=None, steps=220):
    if start is None:
        start = np.array([9.5, 25.0], dtype=float)

    x = start.copy()
    traj = [x.copy()]
    trace = [nearest_cluster(x)]

    for _ in range(steps):
        x = flow_step(x, mode=mode)
        traj.append(x.copy())
        trace.append(nearest_cluster(x))

    return np.array(traj), trace

def run_switching_navigation(schedule, start=None, dt=0.08, noise=0.025):
    """
    schedule = list of tuples (mode, n_steps)
    Example:
      [("fallback_C0", 50), ("seek_C1", 60), ("seek_C2", 100)]
    """
    if start is None:
        start = np.array([14.8, 28.8], dtype=float)

    x = start.copy()
    traj = [x.copy()]
    trace = [nearest_cluster(x)]
    mode_trace = []

    for mode, n_steps in schedule:
        for _ in range(n_steps):
            grad = grad_potential(x, mode=mode)
            dx = -0.9 * grad + noise * np.random.randn(2)
            x = x + dt * dx

            traj.append(x.copy())
            trace.append(nearest_cluster(x))
            mode_trace.append(mode)

    return np.array(traj), trace, mode_trace

# ============================================================
# 5. FIELD GRID
# ============================================================

def compute_field_grid(mode="seek_C2", xlim=(6,16.5), ylim=(21,31), n=55):
    xs = np.linspace(xlim[0], xlim[1], n)
    ys = np.linspace(ylim[0], ylim[1], n)
    X, Y = np.meshgrid(xs, ys)

    U = np.zeros_like(X)
    V = np.zeros_like(Y)
    P = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            p = np.array([X[i, j], Y[i, j]])
            g = grad_potential(p, mode=mode)
            U[i, j] = -g[0]
            V[i, j] = -g[1]
            P[i, j] = potential(p, mode=mode)

    return X, Y, U, V, P

# ============================================================
# 6. PLOTTING
# ============================================================

def plot_v27(schedule, traj_switch, trace_switch, mode_trace):
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    ax1, ax2, ax3, ax4 = axes.flatten()

    # Q1: field for final target mode
    X, Y, U, V, P = compute_field_grid(mode="seek_C2")

    im1 = ax1.imshow(
        P,
        origin="lower",
        extent=[X.min(), X.max(), Y.min(), Y.max()],
        aspect="auto",
        cmap="viridis"
    )
    ax1.quiver(X, Y, U, V, color="white", alpha=0.65, scale=40)

    for k, c in cluster_centers.items():
        ax1.scatter(c[0], c[1], s=220, c=cluster_colors[k], edgecolor="black", zorder=6)
        ax1.text(c[0], c[1] + 0.22, k, color="white", ha="center", va="bottom", fontsize=11)

    ax1.set_title("Q1 — Multi-Attractor Flow Field")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

    # Q2: switching trajectory
    ax2.imshow(
        P,
        origin="lower",
        extent=[X.min(), X.max(), Y.min(), Y.max()],
        aspect="auto",
        cmap="viridis"
    )

    ax2.plot(traj_switch[:, 0], traj_switch[:, 1], color="white", linewidth=2.0, alpha=0.95)
    ax2.scatter(traj_switch[0, 0], traj_switch[0, 1], c="lime", s=140, edgecolor="black", zorder=8)
    ax2.scatter(traj_switch[-1, 0], traj_switch[-1, 1], c="yellow", s=160, edgecolor="black", zorder=9)

    for k, c in cluster_centers.items():
        ax2.scatter(c[0], c[1], s=220, c=cluster_colors[k], edgecolor="black", zorder=6)
        ax2.text(c[0], c[1] + 0.22, k, color="white", ha="center", va="bottom", fontsize=11)

    ax2.set_title("Q2 — Switching Multi-Attractor Navigation")
    ax2.set_xlabel("α")
    ax2.set_ylabel("β")

    # Q3: cluster trace
    cluster_order = list(cluster_centers.keys())
    cluster_map = {c: i for i, c in enumerate(cluster_order)}
    trace_ids = [cluster_map[c] for c in trace_switch]

    ax3.plot(trace_ids, linewidth=1.4)
    ax3.set_yticks(range(len(cluster_order)))
    ax3.set_yticklabels(cluster_order)
    ax3.set_title("Q3 — Cluster Trace")
    ax3.set_xlabel("step")
    ax3.set_ylabel("nearest cluster")
    ax3.grid(True, alpha=0.3)

    # mark schedule boundaries
    pos = 0
    for mode, n_steps in schedule:
        pos += n_steps
        ax3.axvline(pos, color="red", alpha=0.3, linestyle="--")

    # Q4: visit counts
    counts = Counter(trace_switch)
    ax4.bar(counts.keys(), counts.values(),
            color=[cluster_colors[k] for k in counts.keys()])
    ax4.set_title("Q4 — Multi-Attractor Visit Counts")
    ax4.set_xlabel("cluster")
    ax4.set_ylabel("count")

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "v27_multi_attractor_navigation.png")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")

# ============================================================
# 7. MAIN
# ============================================================

def main():
    print("Running V27 Multi-Attractor Navigation...")

    schedule = [
        ("fallback_C0", 50),
        ("seek_C1", 70),
        ("seek_C2", 120),
    ]

    traj_switch, trace_switch, mode_trace = run_switching_navigation(schedule)

    counts = Counter(trace_switch)
    print("\nVisit Counts:")
    for k in sorted(counts.keys()):
        print(f"  {k}: {counts[k]}")

    print(f"\nFinal point: α={traj_switch[-1,0]:.4f}, β={traj_switch[-1,1]:.4f}")
    print(f"Final cluster: {trace_switch[-1]}")

    plot_v27(schedule, traj_switch, trace_switch, mode_trace)

if __name__ == "__main__":
    main()
