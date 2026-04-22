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
    from scipy.ndimage import gaussian_filter1d

    D_smooth = gaussian_filter1d(D, sigma=smooth_sigma)
    threshold = np.mean(D_smooth) + k * np.std(D_smooth)

    peaks, _ = find_peaks(
        D_smooth,
        height=threshold,
        distance=min_distance
    )

    return D_smooth, threshold, peaks


# =========================
# 6. DENSITY
# =========================

def compute_density(alpha_b, beta_b, bins=140):
    H, a_edges, b_edges = np.histogram2d(alpha_b, beta_b, bins=bins)

    # smoothing
    H = gaussian_filter(H, sigma=1.5)

    a_centers = 0.5 * (a_edges[:-1] + a_edges[1:])
    b_centers = 0.5 * (b_edges[:-1] + b_edges[1:])

    return H.T, a_centers, b_centers


# =========================
# 7. RIDGE DETECTION
# =========================

def extract_ridges(H, threshold_percentile=90, neighborhood=3):
    """
    Find local maxima in density field.
    """

    # threshold
    thresh = np.percentile(H[H > 0], threshold_percentile)

    # local maxima
    local_max = maximum_filter(H, size=neighborhood) == H

    ridge_mask = (H >= thresh) & local_max

    return ridge_mask, thresh


# =========================
# 8. MAIN
# =========================

def main():
    print("Running Field Projection V7.3 Ridge Detection...")

    # --- Data ---
    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    components = compute_field_basis(X)
    alpha, beta, gamma = project_field(X, components)

    D = compute_deviation(beta, gamma)
    D_smooth, threshold, _ = detect_transitions(D)

    # Boundary points
    mask = D_smooth > threshold
    alpha_b = alpha[mask]
    beta_b = beta[mask]

    # Density
    H, a_centers, b_centers = compute_density(alpha_b, beta_b)

    # Ridge detection
    ridge_mask, ridge_thresh = extract_ridges(H, threshold_percentile=90, neighborhood=3)

    # Convert ridge indices to coordinates
    ridge_indices = np.where(ridge_mask)
    ridge_alpha = a_centers[ridge_indices[1]]
    ridge_beta = b_centers[ridge_indices[0]]

    # =========================
    # PLOTS
    # =========================
    fig = plt.figure(figsize=(14, 10))

    # ---- Q1 Density
    ax1 = fig.add_subplot(221)
    im1 = ax1.imshow(
        H,
        origin="lower",
        extent=[a_centers[0], a_centers[-1], b_centers[0], b_centers[-1]],
        aspect="auto"
    )
    ax1.set_title("Q1 — Density Field")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    plt.colorbar(im1, ax=ax1)

    # ---- Q2 Density + ridges
    ax2 = fig.add_subplot(222)
    im2 = ax2.imshow(
        H,
        origin="lower",
        extent=[a_centers[0], a_centers[-1], b_centers[0], b_centers[-1]],
        aspect="auto"
    )
    ax2.scatter(ridge_alpha, ridge_beta, c="red", s=12, label="ridge")
    ax2.set_title("Q2 — Ridge Detection")
    ax2.legend()
    plt.colorbar(im2, ax=ax2)

    # ---- Q3 Raw boundary
    ax3 = fig.add_subplot(223)
    ax3.scatter(alpha_b, beta_b, s=3, alpha=0.3)
    ax3.scatter(ridge_alpha, ridge_beta, c="red", s=10)
    ax3.set_title("Q3 — Boundary + Ridge Skeleton")
    ax3.set_xlabel("α")
    ax3.set_ylabel("β")

    # ---- Q4 Clean ridge only
    ax4 = fig.add_subplot(224)
    ax4.scatter(ridge_alpha, ridge_beta, c="red", s=12)
    ax4.set_title("Q4 — Extracted Transition Channels")
    ax4.set_xlabel("α")
    ax4.set_ylabel("β")

    plt.suptitle("FIELD_LAYER V7.3 — Ridge Detection (Transition Channels)", fontsize=16)

    out = os.path.join(OUTPUT_DIR, "v7_3_ridge_detection.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")
    print(f"Ridge threshold: {ridge_thresh:.4f}")
    print(f"Ridge points: {len(ridge_alpha)}")


if __name__ == "__main__":
    main()
