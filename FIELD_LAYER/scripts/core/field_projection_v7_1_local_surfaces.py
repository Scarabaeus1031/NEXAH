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
# 6. LOCAL SURFACE MODEL
# =========================

def fit_quadratic_surface(alpha_b, beta_b, gamma_b):
    """
    gamma = c0 + c1*a + c2*b + c3*a^2 + c4*a*b + c5*b^2
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
    return (
        c0
        + c1 * alpha_grid
        + c2 * beta_grid
        + c3 * alpha_grid**2
        + c4 * alpha_grid * beta_grid
        + c5 * beta_grid**2
    )


def compute_r2(alpha_b, beta_b, gamma_b, coeffs):
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
# 7. SIMPLE LOCAL CLUSTERING
# =========================

def build_local_masks(alpha_b, beta_b):
    """
    Einfache, robuste Teilung in 4 lokale Regionen:
    oben links, oben rechts, unten links, unten rechts
    relativ zur Boundary-Wolke.
    """
    a_mid = np.median(alpha_b)
    b_mid = np.median(beta_b)

    masks = {
        "upper_left":  (alpha_b < a_mid) & (beta_b >= b_mid),
        "upper_right": (alpha_b >= a_mid) & (beta_b >= b_mid),
        "lower_left":  (alpha_b < a_mid) & (beta_b < b_mid),
        "lower_right": (alpha_b >= a_mid) & (beta_b < b_mid),
    }

    return masks, a_mid, b_mid


def make_local_grid(alpha_local, beta_local, padding=0.1, n=60):
    if len(alpha_local) < 10:
        return None, None

    a_min, a_max = np.min(alpha_local), np.max(alpha_local)
    b_min, b_max = np.min(beta_local), np.max(beta_local)

    da = a_max - a_min
    db = b_max - b_min

    a_min -= padding * da
    a_max += padding * da
    b_min -= padding * db
    b_max += padding * db

    a_lin = np.linspace(a_min, a_max, n)
    b_lin = np.linspace(b_min, b_max, n)
    return np.meshgrid(a_lin, b_lin)


# =========================
# 8. MAIN
# =========================

def main():
    print("Running Field Projection V7.1 Local Surfaces...")

    # --- Data ---
    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    components = compute_field_basis(X)
    alpha, beta, gamma = project_field(X, components)

    D = compute_deviation(beta, gamma)
    D_smooth, threshold, _ = detect_transitions(D)

    # Boundary cloud
    boundary_mask = D_smooth > threshold
    alpha_b = alpha[boundary_mask]
    beta_b = beta[boundary_mask]
    gamma_b = gamma[boundary_mask]
    D_b = D_smooth[boundary_mask]

    # Local regions
    local_masks, a_mid, b_mid = build_local_masks(alpha_b, beta_b)

    local_results = {}

    for name, mask in local_masks.items():
        a_loc = alpha_b[mask]
        b_loc = beta_b[mask]
        g_loc = gamma_b[mask]

        if len(a_loc) < 20:
            local_results[name] = None
            continue

        coeffs = fit_quadratic_surface(a_loc, b_loc, g_loc)
        r2 = compute_r2(a_loc, b_loc, g_loc, coeffs)
        grid = make_local_grid(a_loc, b_loc, padding=0.05, n=50)

        if grid[0] is None:
            local_results[name] = None
            continue

        A_grid, B_grid = grid
        G_grid = eval_quadratic_surface(A_grid, B_grid, coeffs)

        local_results[name] = {
            "alpha": a_loc,
            "beta": b_loc,
            "gamma": g_loc,
            "coeffs": coeffs,
            "r2": r2,
            "A_grid": A_grid,
            "B_grid": B_grid,
            "G_grid": G_grid,
        }

    # =========================
    # Q4 PANEL
    # =========================
    fig = plt.figure(figsize=(16, 12))

    # ---- Q1: 3D all local surfaces
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.scatter(alpha_b, beta_b, gamma_b, c=D_b, s=4, alpha=0.2)

    for name, result in local_results.items():
        if result is None:
            continue
        ax1.plot_surface(
            result["A_grid"],
            result["B_grid"],
            result["G_grid"],
            alpha=0.45,
            linewidth=0,
            antialiased=True
        )

    ax1.set_title("Q1 — Boundary Cloud + Local Surfaces")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    ax1.set_zlabel("γ")

    # ---- Q2: Top view
    ax2 = fig.add_subplot(222, projection='3d')
    ax2.scatter(alpha_b, beta_b, gamma_b, c=D_b, s=4, alpha=0.2)

    for name, result in local_results.items():
        if result is None:
            continue
        ax2.plot_surface(
            result["A_grid"],
            result["B_grid"],
            result["G_grid"],
            alpha=0.45,
            linewidth=0,
            antialiased=True
        )

    ax2.view_init(elev=90, azim=-90)
    ax2.set_title("Q2 — Top View")
    ax2.set_xlabel("α")
    ax2.set_ylabel("β")
    ax2.set_zlabel("γ")

    # ---- Q3: Frog view
    ax3 = fig.add_subplot(223, projection='3d')
    ax3.scatter(alpha_b, beta_b, gamma_b, c=D_b, s=4, alpha=0.2)

    for name, result in local_results.items():
        if result is None:
            continue
        ax3.plot_surface(
            result["A_grid"],
            result["B_grid"],
            result["G_grid"],
            alpha=0.45,
            linewidth=0,
            antialiased=True
        )

    ax3.view_init(elev=8, azim=35)
    ax3.set_title("Q3 — Frog View")
    ax3.set_xlabel("α")
    ax3.set_ylabel("β")
    ax3.set_zlabel("γ")

    # ---- Q4: α-β footprint + region split
    ax4 = fig.add_subplot(224)
    sc4 = ax4.scatter(alpha_b, beta_b, c=D_b, s=8, alpha=0.5)

    for name, result in local_results.items():
        if result is None:
            continue

        footprint = np.isfinite(result["G_grid"]).astype(float)
        ax4.contour(
            result["A_grid"],
            result["B_grid"],
            footprint,
            levels=[0.5],
            linewidths=2
        )

    ax4.axvline(a_mid, linestyle="--", alpha=0.5)
    ax4.axhline(b_mid, linestyle="--", alpha=0.5)
    ax4.set_title("Q4 — Local Surface Footprints")
    ax4.set_xlabel("α")
    ax4.set_ylabel("β")

    cbar = fig.colorbar(sc4, ax=[ax1, ax2, ax3, ax4], shrink=0.78, pad=0.08)
    cbar.set_label("D (boundary intensity)")

    plt.suptitle("FIELD_LAYER V7.1 — Local Boundary Surface Approximation", fontsize=18)

    out = os.path.join(OUTPUT_DIR, "v7_1_local_surfaces_q4.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()

    # =========================
    # METRICS
    # =========================
    print(f"Saved: {out}")
    print(f"Boundary points: {len(alpha_b)}")
    print("Local surface R^2 values:")

    for name, result in local_results.items():
        if result is None:
            print(f"  {name}: insufficient points")
        else:
            print(f"  {name}: R^2 = {result['r2']:.4f}, n = {len(result['alpha'])}")


if __name__ == "__main__":
    main()
