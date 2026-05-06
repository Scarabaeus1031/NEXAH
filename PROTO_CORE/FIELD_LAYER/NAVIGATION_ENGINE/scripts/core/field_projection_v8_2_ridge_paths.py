import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter, maximum_filter

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# 1. LORENZ
# =========================

def generate_lorenz(n_steps=5000, dt=0.01):
    sigma = 10.0
    rho = 28.0
    beta = 8.0 / 3.0

    X = np.zeros((n_steps, 3))
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


# =========================
# 2. PCA + PROJECTION
# =========================

def compute_field_basis(X):
    pca = PCA(n_components=3)
    pca.fit(X)
    return pca.components_


def project_field(X, components):
    e1, e2, e3 = components
    alpha = X @ e1
    beta = X @ e2
    gamma = X @ e3
    return alpha, beta, gamma


# =========================
# 3. DEVIATION
# =========================

def compute_deviation(beta, gamma):
    return np.sqrt(beta**2 + gamma**2)


# =========================
# 4. TRANSITION DETECTION
# =========================

def detect_transitions(D):
    from scipy.ndimage import gaussian_filter1d
    D_smooth = gaussian_filter1d(D, sigma=2)
    threshold = np.mean(D_smooth) + 1.2 * np.std(D_smooth)
    peaks, _ = find_peaks(D_smooth, height=threshold, distance=50)
    return D_smooth, threshold


# =========================
# 5. DENSITY + RIDGE
# =========================

def compute_density(alpha_b, beta_b, bins=140):
    H, a_edges, b_edges = np.histogram2d(alpha_b, beta_b, bins=bins)
    H = gaussian_filter(H, sigma=1.5)

    a_centers = 0.5 * (a_edges[:-1] + a_edges[1:])
    b_centers = 0.5 * (b_edges[:-1] + b_edges[1:])

    return H.T, a_centers, b_centers


def extract_ridges(H, percentile=90, neighborhood=3):
    thresh = np.percentile(H[H > 0], percentile)
    local_max = maximum_filter(H, size=neighborhood) == H
    ridge_mask = (H >= thresh) & local_max
    return ridge_mask, thresh


# =========================
# 6. FLOW FIELD
# =========================

def compute_velocity(alpha, beta):
    d_alpha = np.diff(alpha, prepend=alpha[0])
    d_beta = np.diff(beta, prepend=beta[0])
    return d_alpha, d_beta


def estimate_flow_at_ridges(ridge_alpha, ridge_beta, alpha, beta, d_alpha, d_beta, radius=1.5):
    flow_vectors = []

    for ra, rb in zip(ridge_alpha, ridge_beta):
        dist = np.sqrt((alpha - ra)**2 + (beta - rb)**2)
        mask = dist < radius

        if np.sum(mask) < 5:
            flow_vectors.append((0.0, 0.0))
            continue

        vx = np.mean(d_alpha[mask])
        vy = np.mean(d_beta[mask])

        flow_vectors.append((vx, vy))

    return np.array(flow_vectors)


# =========================
# 7. SIMPLE PATH BUILDING
# =========================

def split_ridge_groups(ridge_alpha, ridge_beta):
    """
    Split ridge nodes into four simple groups:
    left-upper, left-lower, right-upper, right-lower
    """
    a_mid = np.median(ridge_alpha)
    b_mid = np.median(ridge_beta)

    groups = {
        "left_upper":  (ridge_alpha < a_mid) & (ridge_beta >= b_mid),
        "left_lower":  (ridge_alpha < a_mid) & (ridge_beta < b_mid),
        "right_upper": (ridge_alpha >= a_mid) & (ridge_beta >= b_mid),
        "right_lower": (ridge_alpha >= a_mid) & (ridge_beta < b_mid),
    }

    return groups, a_mid, b_mid


def build_ordered_path(x, y, side="left"):
    """
    Simple ordered path:
    sort by beta primarily, then alpha
    This is intentionally simple and robust.
    """
    if len(x) == 0:
        return np.array([]), np.array([])

    if side == "left":
        order = np.lexsort((x, y))
    else:
        order = np.lexsort((x, y))

    return x[order], y[order]


# =========================
# 8. MAIN
# =========================

def main():
    print("Running Field Projection V8.2 Ridge Paths...")

    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    components = compute_field_basis(X)
    alpha, beta, gamma = project_field(X, components)

    D = compute_deviation(beta, gamma)
    D_smooth, threshold = detect_transitions(D)

    # boundary points
    boundary_mask = D_smooth > threshold
    alpha_b = alpha[boundary_mask]
    beta_b = beta[boundary_mask]

    # density + ridges
    H, a_centers, b_centers = compute_density(alpha_b, beta_b)
    ridge_mask, ridge_thresh = extract_ridges(H, percentile=90, neighborhood=3)

    ridge_idx = np.where(ridge_mask)
    ridge_alpha = a_centers[ridge_idx[1]]
    ridge_beta = b_centers[ridge_idx[0]]

    # flow
    d_alpha, d_beta = compute_velocity(alpha, beta)
    flow = estimate_flow_at_ridges(
        ridge_alpha, ridge_beta,
        alpha, beta,
        d_alpha, d_beta,
        radius=1.5
    )

    # path groups
    groups, a_mid, b_mid = split_ridge_groups(ridge_alpha, ridge_beta)

    path_data = {}
    for name, mask in groups.items():
        xg = ridge_alpha[mask]
        yg = ridge_beta[mask]

        side = "left" if "left" in name else "right"
        xp, yp = build_ordered_path(xg, yg, side=side)

        path_data[name] = (xp, yp)

    # =========================
    # PLOT
    # =========================
    fig = plt.figure(figsize=(15, 11))

    # ---- Q1: density + ridges + flow
    ax1 = fig.add_subplot(221)
    im1 = ax1.imshow(
        H,
        origin="lower",
        extent=[a_centers[0], a_centers[-1], b_centers[0], b_centers[-1]],
        aspect="auto"
    )
    ax1.scatter(ridge_alpha, ridge_beta, c="red", s=16, label="ridge nodes")
    ax1.quiver(
        ridge_alpha, ridge_beta,
        flow[:, 0], flow[:, 1],
        color="white",
        scale=30,
        width=0.003
    )
    ax1.set_title("Q1 — Ridge Nodes + Flow")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    ax1.legend()
    plt.colorbar(im1, ax=ax1)

    # ---- Q2: path reconstruction
    ax2 = fig.add_subplot(222)
    im2 = ax2.imshow(
        H,
        origin="lower",
        extent=[a_centers[0], a_centers[-1], b_centers[0], b_centers[-1]],
        aspect="auto"
    )
    colors = {
        "left_upper": "cyan",
        "left_lower": "blue",
        "right_upper": "orange",
        "right_lower": "yellow"
    }

    for name, (xp, yp) in path_data.items():
        if len(xp) > 1:
            ax2.plot(xp, yp, linewidth=2.0, color=colors[name], label=name)
            ax2.scatter(xp, yp, s=16, color=colors[name])

    ax2.set_title("Q2 — Reconstructed Ridge Paths")
    ax2.set_xlabel("α")
    ax2.set_ylabel("β")
    ax2.legend()
    plt.colorbar(im2, ax=ax2)

    # ---- Q3: boundary + paths
    ax3 = fig.add_subplot(223)
    ax3.scatter(alpha_b, beta_b, s=4, alpha=0.15, label="boundary")
    for name, (xp, yp) in path_data.items():
        if len(xp) > 1:
            ax3.plot(xp, yp, linewidth=2.2, color=colors[name], label=name)
            ax3.scatter(xp, yp, s=18, color=colors[name])
    ax3.set_title("Q3 — Boundary + Ridge Paths")
    ax3.set_xlabel("α")
    ax3.set_ylabel("β")
    ax3.legend()

    # ---- Q4: clean paths only
    ax4 = fig.add_subplot(224)
    for name, (xp, yp) in path_data.items():
        if len(xp) > 1:
            ax4.plot(xp, yp, linewidth=2.5, color=colors[name], label=name)
            ax4.scatter(xp, yp, s=20, color=colors[name])
    ax4.axvline(a_mid, linestyle="--", alpha=0.4)
    ax4.axhline(b_mid, linestyle="--", alpha=0.4)
    ax4.set_title("Q4 — Transition Path Skeleton")
    ax4.set_xlabel("α")
    ax4.set_ylabel("β")
    ax4.legend()

    plt.suptitle("FIELD_LAYER V8.2 — Ridge Path Reconstruction", fontsize=17)

    out = os.path.join(OUTPUT_DIR, "v8_2_ridge_paths.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")
    print(f"Ridge threshold: {ridge_thresh:.4f}")
    print(f"Ridge points: {len(ridge_alpha)}")
    for name, (xp, yp) in path_data.items():
        print(f"{name}: {len(xp)} nodes")


if __name__ == "__main__":
    main()
