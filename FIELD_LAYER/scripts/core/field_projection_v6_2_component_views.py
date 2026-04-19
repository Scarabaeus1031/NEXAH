import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
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
# 5. MAIN
# =========================

def main():
    print("Running Field Projection V6.2 (Component Views)...")

    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    components = compute_field_basis(X)
    alpha, beta, gamma = project_field(X, components)

    D = compute_deviation(beta, gamma)
    D_smooth = gaussian_filter1d(D, sigma=2)

    # =========================
    # Q4 PANEL (2x2)
    # =========================

    fig = plt.figure(figsize=(14, 12))

    # ---- α
    ax1 = fig.add_subplot(221)
    sc1 = ax1.scatter(alpha, beta, c=alpha, s=5)
    ax1.set_title("Color = α (Flow Position)")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    fig.colorbar(sc1, ax=ax1)

    # ---- β
    ax2 = fig.add_subplot(222)
    sc2 = ax2.scatter(alpha, beta, c=beta, s=5)
    ax2.set_title("Color = β (Deviation Axis 1)")
    ax2.set_xlabel("α")
    ax2.set_ylabel("β")
    fig.colorbar(sc2, ax=ax2)

    # ---- γ
    ax3 = fig.add_subplot(223)
    sc3 = ax3.scatter(alpha, beta, c=gamma, s=5)
    ax3.set_title("Color = γ (Deviation Axis 2)")
    ax3.set_xlabel("α")
    ax3.set_ylabel("β")
    fig.colorbar(sc3, ax=ax3)

    # ---- D
    ax4 = fig.add_subplot(224)
    sc4 = ax4.scatter(alpha, beta, c=D_smooth, s=5)
    ax4.set_title("Color = D (Total Deviation)")
    ax4.set_xlabel("α")
    ax4.set_ylabel("β")
    fig.colorbar(sc4, ax=ax4)

    plt.suptitle("FIELD_LAYER V6.2 — Component Views", fontsize=18)

    out = os.path.join(OUTPUT_DIR, "v6_2_component_views.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
