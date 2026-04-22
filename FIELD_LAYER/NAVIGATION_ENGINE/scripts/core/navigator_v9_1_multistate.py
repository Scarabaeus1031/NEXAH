import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# LORENZ
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
# BASIS
# =========================

def compute_basis(X):
    pca = PCA(n_components=3)
    pca.fit(X)
    return pca.components_


def project(X, e1, e2, e3):
    return X @ e1, X @ e2, X @ e3


def deviation(beta, gamma):
    return np.sqrt(beta**2 + gamma**2)


# =========================
# DENSITY
# =========================

def density_field(alpha, beta, D, bins=200):
    H, xedges, yedges = np.histogram2d(alpha, beta, bins=bins, weights=D)
    H = gaussian_filter(H, sigma=2)
    return H, xedges, yedges


def extract_ridge(H, q=0.97):
    thresh = np.quantile(H, q)
    idx = np.argwhere(H > thresh)
    return idx


# =========================
# NAVIGATION LOGIC
# =========================

def classify(D_val, dD_val, D_th=12, dD_th=0.5):
    if D_val < D_th:
        return "entry"
    elif dD_val > dD_th:
        return "core"
    else:
        return "exit"


def action(state):
    return {
        "entry": "PREPARE",
        "core": "INTERVENE",
        "exit": "STABILIZE"
    }[state]


# =========================
# MAIN
# =========================

def main():
    print("Running V9.1 Multi-State Navigation...")

    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    e1, e2, e3 = compute_basis(X)
    alpha, beta, gamma = project(X, e1, e2, e3)

    D = deviation(beta, gamma)
    dD = np.gradient(D)

    H, xedges, yedges = density_field(alpha, beta, D)
    ridge_idx = extract_ridge(H)

    ridge_alpha = xedges[ridge_idx[:, 0]]
    ridge_beta = yedges[ridge_idx[:, 1]]

    # =========================
    # MULTI STATES
    # =========================

    # sample multiple points
    indices = np.linspace(len(alpha)-500, len(alpha)-1, 8).astype(int)

    plt.figure(figsize=(8,6))

    plt.imshow(
        H.T,
        origin='lower',
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect='auto'
    )

    # ridge
    plt.scatter(ridge_alpha, ridge_beta, s=10, color='red')

    # states
    for t in indices:
        a0 = alpha[t]
        b0 = beta[t]
        D0 = D[t]
        dD0 = dD[t]

        s = classify(D0, dD0)
        act = action(s)

        color_map = {
            "entry": "blue",
            "core": "yellow",
            "exit": "green"
        }

        plt.scatter(a0, b0, s=80, color=color_map[s], edgecolors='black')

        # nearest ridge
        dist = np.sqrt((ridge_alpha - a0)**2 + (ridge_beta - b0)**2)
        i = np.argmin(dist)

        da = ridge_alpha[i] - a0
        db = ridge_beta[i] - b0

        norm = np.sqrt(da**2 + db**2)
        if norm > 0:
            da /= norm
            db /= norm

        plt.arrow(
            a0, b0,
            da*4, db*4,
            color='white',
            width=0.05,
            head_width=1.2,
            length_includes_head=True
        )

    plt.title("V9.1 Multi-State Navigation")
    plt.xlabel("α")
    plt.ylabel("β")

    out = os.path.join(OUTPUT_DIR, "v9_1_multistate.png")
    plt.savefig(out, dpi=150)
    plt.close()

    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
