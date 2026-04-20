import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 1. LORENZ + PROJECTION
# ============================================================

def generate_lorenz(n_steps=5000, dt=0.01):
    sigma = 10.0
    rho = 28.0
    beta = 8.0 / 3.0

    X = np.zeros((n_steps, 3), dtype=float)
    x, y, z = 1.0, 1.0, 1.0

    for i in range(n_steps):
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z

        x += dx * dt
        y += dy * dt
        z += dz * dt

        X[i] = [x, y, z]

    return X


def compute_basis(X):
    pca = PCA(n_components=3)
    pca.fit(X)
    return pca.components_


def project(X, e1, e2):
    alpha = X @ e1
    beta = X @ e2
    return alpha, beta


def density_field(alpha, beta, bins=180, sigma=2.0):
    H, xedges, yedges = np.histogram2d(alpha, beta, bins=bins)
    H = gaussian_filter(H, sigma=sigma)
    return H, xedges, yedges


# ============================================================
# 2. CLUSTER CENTERS
# ============================================================

def get_nodes():
    return np.array([
        [11.0, 26.0],  # N0
        [10.5, 25.5],  # N1
        [12.0, 24.8],  # N2
        [13.0, 26.0],  # N3
        [12.0, 23.5],  # N4
        [11.5, 24.0],  # N5
        [10.8, 27.8],  # N6
        [9.8, 25.2],   # N7
        [13.5, 25.5],  # N8
        [11.5, 28.5],  # N9
        [10.2, 24.2],  # N10
    ], dtype=float)


node_to_cluster = {
    0: 0, 1: 0, 7: 0, 10: 0,
    2: 1, 4: 1, 5: 1,
    3: 2, 8: 2,
    6: 3, 9: 3
}


def build_cluster_centroids(nodes, node_to_cluster):
    groups = {}
    for n_idx, c_idx in node_to_cluster.items():
        groups.setdefault(c_idx, []).append(nodes[n_idx])

    centroids = {}
    for c_idx, pts in groups.items():
        centroids[c_idx] = np.mean(np.array(pts), axis=0)

    return centroids, groups


# ============================================================
# 3. CONTINUOUS CONTROL FIELD
# ============================================================

def unit(v):
    n = np.linalg.norm(v)
    if n < 1e-9:
        return np.zeros_like(v)
    return v / n


def control_vector(point, centroids):
    """
    Continuous control field at point p in alpha-beta space.
    """
    p = np.array(point, dtype=float)

    c0 = centroids[0]
    c1 = centroids[1]
    c2 = centroids[2]
    c3 = centroids[3]

    # 1) attraction to target C2
    v_target = c2 - p
    d_target = np.linalg.norm(v_target)
    a_target = 1.2 * unit(v_target) / (1.0 + 0.15 * d_target)

    # 2) mild corridor attraction to segment C1-C2
    seg = c2 - c1
    seg_norm = np.dot(seg, seg) + 1e-12
    t = np.clip(np.dot(p - c1, seg) / seg_norm, 0.0, 1.0)
    proj = c1 + t * seg
    v_corridor = proj - p
    d_corr = np.linalg.norm(v_corridor)
    a_corr = 0.9 * unit(v_corridor) / (1.0 + 0.25 * d_corr)

    # 3) repulsion from C3
    v_bad = p - c3
    d_bad = np.linalg.norm(v_bad)
    a_bad = 1.8 * unit(v_bad) / (0.5 + d_bad**1.2)

    # 4) slight pull away from C0 if too close, otherwise neutral
    v_c0 = p - c0
    d_c0 = np.linalg.norm(v_c0)
    a_c0 = 0.4 * unit(v_c0) / (0.8 + d_c0**1.3)

    # 5) damping toward center band (avoid too much beta overshoot)
    center = 0.5 * (c1 + c2)
    v_center = center - p
    a_center = 0.25 * unit(v_center)

    v = a_target + a_corr + a_bad + a_c0 + a_center
    return v


def generate_control_field(centroids, xlim=(6.0, 16.5), ylim=(21.0, 30.8), resolution=35):
    xs = np.linspace(xlim[0], xlim[1], resolution)
    ys = np.linspace(ylim[0], ylim[1], resolution)

    Xg, Yg = np.meshgrid(xs, ys)
    U = np.zeros_like(Xg)
    V = np.zeros_like(Yg)

    for i in range(resolution):
        for j in range(resolution):
            p = np.array([Xg[i, j], Yg[i, j]])
            vec = control_vector(p, centroids)
            U[i, j] = vec[0]
            V[i, j] = vec[1]

    return Xg, Yg, U, V


# ============================================================
# 4. CONTINUOUS TRAJECTORY SIMULATION
# ============================================================

def assign_cluster(point, centroids):
    dists = {k: np.linalg.norm(point - c) for k, c in centroids.items()}
    return min(dists, key=dists.get)


def simulate_continuous(point0, centroids, n_steps=160, dt=0.12, noise=0.015):
    """
    Controlled continuous dynamics in alpha-beta space.
    """
    p = np.array(point0, dtype=float)
    traj = [p.copy()]
    clusters = [assign_cluster(p, centroids)]

    for _ in range(n_steps):
        v = control_vector(p, centroids)
        p = p + dt * v + np.random.normal(scale=noise, size=2)

        traj.append(p.copy())
        clusters.append(assign_cluster(p, centroids))

    return np.array(traj), clusters


def simulate_uncontrolled(point0, n_steps=160, dt=0.12, noise=0.04):
    """
    Simple baseline drift: weak downward / sideways drift + noise.
    """
    p = np.array(point0, dtype=float)
    traj = [p.copy()]

    drift = np.array([-0.05, -0.03], dtype=float)

    for _ in range(n_steps):
        p = p + dt * drift + np.random.normal(scale=noise, size=2)
        traj.append(p.copy())

    return np.array(traj)


# ============================================================
# 5. PLOTTING
# ============================================================

def plot_v26(H, xedges, yedges, nodes, groups, centroids,
             Xg, Yg, U, V,
             uncontrolled_traj, controlled_traj, controlled_clusters):
    cluster_colors = {
        0: "#1f77b4",  # blue
        1: "#d62728",  # red
        2: "#e377c2",  # magenta
        3: "#17becf",  # cyan
    }

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    ax1, ax2, ax3, ax4 = axes.flatten()

    # -------------------------
    # Q1 — control vector field
    # -------------------------
    ax1.imshow(
        H.T, origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto", cmap="viridis"
    )

    ax1.quiver(Xg, Yg, U, V, color="white", alpha=0.75, scale=45)

    for c_idx, node_list in groups.items():
        arr = np.array(node_list)
        ax1.scatter(arr[:, 0], arr[:, 1], s=220, c=cluster_colors[c_idx],
                    edgecolor="black", zorder=5)

    for c_idx, center in centroids.items():
        ax1.scatter(center[0], center[1], s=420, c=cluster_colors[c_idx],
                    marker="X", edgecolor="white", linewidth=1.8, zorder=7)
        ax1.text(center[0], center[1] + 0.35, f"C{c_idx}",
                 color="white", fontsize=11, ha="center", va="bottom", zorder=8)

    ax1.set_title("Q1 — Continuous Control Field")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")

    # -------------------------
    # Q2 — uncontrolled vs controlled
    # -------------------------
    ax2.imshow(
        H.T, origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto", cmap="viridis"
    )

    ax2.plot(uncontrolled_traj[:, 0], uncontrolled_traj[:, 1],
             color="orange", linewidth=1.8, alpha=0.85, label="uncontrolled")
    ax2.plot(controlled_traj[:, 0], controlled_traj[:, 1],
             color="white", linewidth=2.0, alpha=0.95, label="controlled")

    ax2.scatter(uncontrolled_traj[0, 0], uncontrolled_traj[0, 1],
                c="orange", s=140, edgecolor="black", zorder=8)
    ax2.scatter(controlled_traj[0, 0], controlled_traj[0, 1],
                c="lime", s=140, edgecolor="black", zorder=8)
    ax2.scatter(controlled_traj[-1, 0], controlled_traj[-1, 1],
                c="yellow", s=160, edgecolor="black", zorder=9)

    for c_idx, center in centroids.items():
        ax2.scatter(center[0], center[1], s=360, c=cluster_colors[c_idx],
                    marker="X", edgecolor="white", linewidth=1.8, zorder=7)

    ax2.set_title("Q2 — Controlled vs Uncontrolled Trajectory")
    ax2.set_xlabel("α")
    ax2.set_ylabel("β")
    ax2.legend(loc="lower left")

    # -------------------------
    # Q3 — controlled cluster occupancy over time
    # -------------------------
    ax3.plot(controlled_clusters, linewidth=1.3)
    ax3.set_yticks([0, 1, 2, 3])
    ax3.set_yticklabels(["C0", "C1", "C2", "C3"])
    ax3.set_title("Q3 — Controlled Cluster Trace")
    ax3.set_xlabel("step")
    ax3.set_ylabel("cluster")
    ax3.grid(True, alpha=0.3)

    # -------------------------
    # Q4 — visit counts under continuous control
    # -------------------------
    counts = Counter(controlled_clusters)
    ax4.bar(sorted(counts.keys()), [counts[k] for k in sorted(counts.keys())],
            color=["#1f77b4", "#d62728", "#e377c2", "#17becf"])
    ax4.set_xticks([0, 1, 2, 3])
    ax4.set_xticklabels(["C0", "C1", "C2", "C3"])
    ax4.set_title("Q4 — Controlled Continuous Visit Counts")
    ax4.set_xlabel("cluster")
    ax4.set_ylabel("count")

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "v26_continuous_field_control.png")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")


# ============================================================
# 6. MAIN
# ============================================================

def main():
    print("Running V26 Continuous Field Control...")

    X = generate_lorenz()
    e1, e2, _ = compute_basis(X)
    alpha, beta = project(X, e1, e2)
    H, xedges, yedges = density_field(alpha, beta)

    nodes = get_nodes()
    centroids, groups = build_cluster_centroids(nodes, node_to_cluster)

    Xg, Yg, U, V = generate_control_field(centroids)

    # choose a starting point near unstable side / upper-left-ish
    point0 = np.array([10.2, 27.6], dtype=float)

    uncontrolled_traj = simulate_uncontrolled(point0, n_steps=160, dt=0.12, noise=0.04)
    controlled_traj, controlled_clusters = simulate_continuous(
        point0, centroids,
        n_steps=160, dt=0.12, noise=0.015
    )

    counts = Counter(controlled_clusters)
    print("\nControlled Visit Counts:")
    for k in sorted(counts):
        print(f"  C{k}: {counts[k]}")

    print(f"\nFinal controlled point: α={controlled_traj[-1,0]:.3f}, β={controlled_traj[-1,1]:.3f}")
    print(f"Final cluster: C{controlled_clusters[-1]}")

    plot_v26(
        H, xedges, yedges, nodes, groups, centroids,
        Xg, Yg, U, V,
        uncontrolled_traj, controlled_traj, controlled_clusters
    )


if __name__ == "__main__":
    main()
