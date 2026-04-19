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
# 6. SURFACE FIT
# =========================

def fit_quadratic_surface(alpha_b, beta_b, gamma_b):
    """
    Fit:
        gamma = c0
              + c1*alpha + c2*beta
              + c3*alpha^2 + c4*alpha*beta + c5*beta^2
    """
    A = np.column_stack([
        np.ones_like(alpha_b),
        alpha_b,
        beta_b,
        alpha_b**2,
        alpha_b * beta_b,
        beta_b**2
    ])

    coeffs, _, _, _ = np.linalg.lstsq(A, gamma_b, rcond=None)
    return coeffs


def eval_quadratic_surface(alpha_grid, beta_grid, coeffs):
    c0, c1, c2, c3, c4, c5 = coeffs
    gamma_grid = (
        c0
        + c1 * alpha_grid
        + c2 * beta_grid
        + c3 * alpha_grid**2
        + c4 * alpha_grid * beta_grid
        + c5 * beta_grid**2
    )
    return gamma_grid


def surface_r2(alpha_b, beta_b, gamma_b, coeffs):
    A = np.column_stack([
        np.ones_like(alpha_b),
        alpha_b,
        beta_b,
        alpha_b**2,
        alpha_b * beta_b,
        beta_b**2
    ])
    pred = A @ coeffs

    ss_res = np.sum((gamma_b - pred) ** 2)
    ss_tot = np.sum((gamma_b - np.mean(gamma_b)) ** 2)

    if ss_tot == 0:
        return np.nan

    return 1.0 - ss_res / ss_tot


# =========================
# 7. MAIN
# =========================

def main():
    print("Running Field Projection V7 Surface...")

    # --- Data ---
    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    components = compute_field_basis(X)
    alpha, beta, gamma = project_field(X, components)

    D = compute_deviation(beta, gamma)
    D_smooth, threshold, _ = detect_transitions(D)

    # Boundary points
    boundary_mask = D_smooth > threshold

    alpha_b = alpha[boundary_mask]
    beta_b = beta[boundary_mask]
    gamma_b = gamma[boundary_mask]
    D_b = D_smooth[boundary_mask]

    # --- Surface fit ---
    coeffs = fit_quadratic_surface(alpha_b, beta_b, gamma_b)
    r2 = surface_r2(alpha_b, beta_b, gamma_b, coeffs)

    # Grid for surface
    a_min, a_max = np.percentile(alpha_b, [2, 98])
    b_min, b_max = np.percentile(beta_b, [2, 98])

    a_lin = np.linspace(a_min, a_max, 120)
    b_lin = np.linspace(b_min, b_max, 120)

    A_grid, B_grid = np.meshgrid(a_lin, b_lin)
    G_grid = eval_quadratic_surface(A_grid, B_grid, coeffs)

    # Mask grid to convex-ish central support:
    # keep only region that is near actual boundary cloud in alpha-beta
    # simple bounding ellipse to avoid an oversized sheet
    a0 = np.mean(alpha_b)
    b0 = np.mean(beta_b)
    sa = np.std(alpha_b)
    sb = np.std(beta_b)

    support_mask = (((A_grid - a0) / (2.2 * sa)) ** 2 + ((B_grid - b0) / (2.2 * sb)) ** 2) < 1.0
    G_grid_masked = np.where(support_mask, G_grid, np.nan)

    # =========================
    # Q4 PANEL
    # =========================
    fig = plt.figure(figsize=(16, 12))

    # ---- Q1: Boundary cloud + surface
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.scatter(alpha_b, beta_b, gamma_b, c=D_b, s=4, alpha=0.25)
    ax1.plot_surface(A_grid, B_grid, G_grid_masked, alpha=0.55, linewidth=0, antialiased=True)
    ax1.set_title("Q1 — Boundary Cloud + Surface")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    ax1.set_zlabel("γ")

    # ---- Q2: Top view
    ax2 = fig.add_subplot(222, projection='3d')
    ax2.scatter(alpha_b, beta_b, gamma_b, c=D_b, s=4, alpha=0.25)
    ax2.plot_surface(A_grid, B_grid, G_grid_masked, alpha=0.55, linewidth=0, antialiased=True)
    ax2.view_init(elev=90, azim=-90)
    ax2.set_title("Q2 — Top View")
    ax2.set_xlabel("α")
    ax2.set_ylabel("β")
    ax2.set_zlabel("γ")

    # ---- Q3: Frog view
    ax3 = fig.add_subplot(223, projection='3d')
    ax3.scatter(alpha_b, beta_b, gamma_b, c=D_b, s=4, alpha=0.25)
    ax3.plot_surface(A_grid, B_grid, G_grid_masked, alpha=0.55, linewidth=0, antialiased=True)
    ax3.view_init(elev=8, azim=35)
    ax3.set_title("Q3 — Frog View")
    ax3.set_xlabel("α")
    ax3.set_ylabel("β")
    ax3.set_zlabel("γ")

    # ---- Q4: alpha-beta projection + surface footprint
    ax4 = fig.add_subplot(224)
    sc4 = ax4.scatter(alpha_b, beta_b, c=D_b, s=8, alpha=0.45)
    ax4.contour(
        A_grid,
        B_grid,
        np.where(np.isnan(G_grid_masked), 0.0, 1.0),
        levels=[0.5],
        linewidths=2
    )
    ax4.set_title("Q4 — Surface Footprint in α-β")
    ax4.set_xlabel("α")
    ax4.set_ylabel("β")

    cbar = fig.colorbar(sc4, ax=[ax1, ax2, ax3, ax4], shrink=0.78, pad=0.08)
    cbar.set_label("D (boundary intensity)")

    plt.suptitle("FIELD_LAYER V7 — Boundary Surface Approximation", fontsize=18)

    out = os.path.join(OUTPUT_DIR, "v7_surface_q4.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()

    # =========================
    # METRICS
    # =========================
    print(f"Saved: {out}")
    print(f"Boundary points: {len(alpha_b)}")
    print(f"Surface fit R^2: {r2:.4f}")
    print("Surface coefficients:")
    print(coeffs)


if __name__ == "__main__":
    main()
