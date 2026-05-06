import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d

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
# 2. PCA
# =========================

def compute_field_basis(X):
    pca = PCA(n_components=3)
    pca.fit(X)
    return pca.components_


# =========================
# 3. PROJECTION
# =========================

def project_field(X, components):
    e1, e2, e3 = components
    alpha = X @ e1
    beta = X @ e2
    gamma = X @ e3
    return alpha, beta, gamma


# =========================
# 4. DEVIATION
# =========================

def compute_deviation(beta, gamma):
    return np.sqrt(beta**2 + gamma**2)


# =========================
# 5. TRANSITIONS
# =========================

def detect_transitions(D, k=1.2, min_distance=50, smooth_sigma=2):
    D_smooth = gaussian_filter1d(D, sigma=smooth_sigma)
    threshold = np.mean(D_smooth) + k * np.std(D_smooth)

    peaks, _ = find_peaks(
        D_smooth,
        height=threshold,
        distance=min_distance
    )

    return D_smooth, threshold, peaks


# =========================
# 6. DENSITY HELPERS
# =========================

def compute_2d_density(alpha_b, beta_b, bins=120, smooth_sigma=1.5):
    H, a_edges, b_edges = np.histogram2d(alpha_b, beta_b, bins=bins)
    H = gaussian_filter1d(H, sigma=smooth_sigma, axis=0)
    H = gaussian_filter1d(H, sigma=smooth_sigma, axis=1)

    a_centers = 0.5 * (a_edges[:-1] + a_edges[1:])
    b_centers = 0.5 * (b_edges[:-1] + b_edges[1:])

    return H.T, a_centers, b_centers


def compute_3d_density(alpha_b, beta_b, gamma_b, bins=40, smooth_sigma=1.0):
    H, edges = np.histogramdd(
        np.column_stack([alpha_b, beta_b, gamma_b]),
        bins=bins
    )

    H = gaussian_filter1d(H, sigma=smooth_sigma, axis=0)
    H = gaussian_filter1d(H, sigma=smooth_sigma, axis=1)
    H = gaussian_filter1d(H, sigma=smooth_sigma, axis=2)

    a_edges, b_edges, g_edges = edges
    a_centers = 0.5 * (a_edges[:-1] + a_edges[1:])
    b_centers = 0.5 * (b_edges[:-1] + b_edges[1:])
    g_centers = 0.5 * (g_edges[:-1] + g_edges[1:])

    return H, a_centers, b_centers, g_centers


def top_density_voxels(H, a_centers, b_centers, g_centers, percentile=97):
    threshold = np.percentile(H[H > 0], percentile) if np.any(H > 0) else 0.0
    idx = np.where(H >= threshold)

    a = a_centers[idx[0]]
    b = b_centers[idx[1]]
    g = g_centers[idx[2]]
    d = H[idx]

    return a, b, g, d, threshold


# =========================
# 7. MAIN
# =========================

def main():
    print("Running Field Projection V7.2 Density Field...")

    # --- Data ---
    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    components = compute_field_basis(X)
    alpha, beta, gamma = project_field(X, components)

    D = compute_deviation(beta, gamma)
    D_smooth, threshold, _ = detect_transitions(D)

    # Boundary points only
    boundary_mask = D_smooth > threshold
    alpha_b = alpha[boundary_mask]
    beta_b = beta[boundary_mask]
    gamma_b = gamma[boundary_mask]
    D_b = D_smooth[boundary_mask]

    # 2D density in alpha-beta
    H2, a2, b2 = compute_2d_density(alpha_b, beta_b, bins=140, smooth_sigma=1.6)

    # 3D density in alpha-beta-gamma
    H3, a3, b3, g3 = compute_3d_density(alpha_b, beta_b, gamma_b, bins=42, smooth_sigma=1.0)

    # strongest 3D density voxels
    a_top, b_top, g_top, d_top, dens_thresh = top_density_voxels(H3, a3, b3, g3, percentile=97)

    # =========================
    # Q4 PANEL
    # =========================
    fig = plt.figure(figsize=(16, 12))

    # ---- Q1: 2D density heatmap
    ax1 = fig.add_subplot(221)
    im1 = ax1.imshow(
        H2,
        origin="lower",
        aspect="auto",
        extent=[a2[0], a2[-1], b2[0], b2[-1]]
    )
    ax1.set_title("Q1 — Boundary Density in α-β")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    fig.colorbar(im1, ax=ax1)

    # ---- Q2: 2D heatmap + raw boundary
    ax2 = fig.add_subplot(222)
    im2 = ax2.imshow(
        H2,
        origin="lower",
        aspect="auto",
        extent=[a2[0], a2[-1], b2[0], b2[-1]]
    )
    ax2.scatter(alpha_b, beta_b, s=4, alpha=0.15)
    ax2.set_title("Q2 — Density + Boundary Points")
    ax2.set_xlabel("α")
    ax2.set_ylabel("β")
    fig.colorbar(im2, ax=ax2)

    # ---- Q3: 3D strongest density voxels
    ax3 = fig.add_subplot(223, projection='3d')
    sc3 = ax3.scatter(a_top, b_top, g_top, c=d_top, s=18, alpha=0.85)
    ax3.set_title("Q3 — Strongest 3D Density Voxels")
    ax3.set_xlabel("α")
    ax3.set_ylabel("β")
    ax3.set_zlabel("γ")
    fig.colorbar(sc3, ax=ax3, shrink=0.7)

    # ---- Q4: Frog-style 3D density view
    ax4 = fig.add_subplot(224, projection='3d')
    sc4 = ax4.scatter(a_top, b_top, g_top, c=d_top, s=18, alpha=0.85)
    ax4.view_init(elev=8, azim=35)
    ax4.set_title("Q4 — Frog View of Density Field")
    ax4.set_xlabel("α")
    ax4.set_ylabel("β")
    ax4.set_zlabel("γ")
    fig.colorbar(sc4, ax=ax4, shrink=0.7)

    plt.suptitle("FIELD_LAYER V7.2 — Boundary Density Field", fontsize=18)

    out = os.path.join(OUTPUT_DIR, "v7_2_density_field_q4.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")
    print(f"Boundary points: {len(alpha_b)}")
    print(f"3D density threshold (97th percentile): {dens_thresh:.4f}")
    print(f"Strong voxels kept: {len(a_top)}")


if __name__ == "__main__":
    main()
