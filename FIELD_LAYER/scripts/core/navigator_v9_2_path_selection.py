import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter

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

def compute_basis(X):
    pca = PCA(n_components=3)
    pca.fit(X)
    return pca.components_


def project(X, e1, e2, e3):
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
# 4. DENSITY FIELD
# =========================

def density_field(alpha, beta, D, bins=200):
    H, xedges, yedges = np.histogram2d(alpha, beta, bins=bins, weights=D)
    H = gaussian_filter(H, sigma=2)
    return H, xedges, yedges


def extract_ridge(H, q=0.97):
    thresh = np.quantile(H, q)
    mask = H > thresh
    return np.argwhere(mask), thresh


# =========================
# 5. RIDGE PATH GROUPS
# =========================

def split_paths(ridge_alpha, ridge_beta):
    """
    Split ridge into 4 regions (approximate paths)
    """
    paths = {
        "left_upper": [],
        "left_lower": [],
        "right_upper": [],
        "right_lower": []
    }

    for a, b in zip(ridge_alpha, ridge_beta):
        if a < 0 and b > 0:
            paths["left_upper"].append((a, b))
        elif a < 0 and b <= 0:
            paths["left_lower"].append((a, b))
        elif a >= 0 and b > 0:
            paths["right_upper"].append((a, b))
        else:
            paths["right_lower"].append((a, b))

    # convert to arrays
    for k in paths:
        if len(paths[k]) > 0:
            paths[k] = np.array(paths[k])
        else:
            paths[k] = np.empty((0,2))

    return paths


# =========================
# 6. PATH SELECTION
# =========================

def choose_best_path(a0, b0, paths):
    """
    Select path with minimal mean distance
    """
    best_key = None
    best_score = np.inf
    best_target = None

    for key, pts in paths.items():
        if len(pts) == 0:
            continue

        dists = np.sqrt((pts[:,0] - a0)**2 + (pts[:,1] - b0)**2)
        score = np.mean(np.sort(dists)[:5])  # use nearest 5 points

        if score < best_score:
            best_score = score
            best_key = key

            # closest point
            idx = np.argmin(dists)
            best_target = pts[idx]

    return best_key, best_target


# =========================
# 7. MAIN
# =========================

def main():
    print("Running V9.2 Path Selection...")

    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    e1, e2, e3 = compute_basis(X)
    alpha, beta, gamma = project(X, e1, e2, e3)

    D = compute_deviation(beta, gamma)

    H, xedges, yedges = density_field(alpha, beta, D)
    ridge_idx, _ = extract_ridge(H)

    ridge_alpha = xedges[ridge_idx[:, 0]]
    ridge_beta = yedges[ridge_idx[:, 1]]

    # split into paths
    paths = split_paths(ridge_alpha, ridge_beta)

    # =========================
    # MULTI STATES
    # =========================

    indices = np.linspace(len(alpha)-500, len(alpha)-1, 8).astype(int)

    plt.figure(figsize=(8,6))

    plt.imshow(
        H.T,
        origin='lower',
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect='auto'
    )

    # ridge
    plt.scatter(ridge_alpha, ridge_beta, s=10, color='red', label='ridge')

    colors = {
        "left_upper": "cyan",
        "left_lower": "blue",
        "right_upper": "orange",
        "right_lower": "yellow"
    }

    # plot paths
    for key, pts in paths.items():
        if len(pts) > 0:
            plt.scatter(pts[:,0], pts[:,1], s=5, color=colors[key], alpha=0.5)

    # =========================
    # DECISIONS
    # =========================

    for t in indices:
        a0 = alpha[t]
        b0 = beta[t]

        key, target = choose_best_path(a0, b0, paths)

        if target is None:
            continue

        # plot current
        plt.scatter(a0, b0, s=80, color='white', edgecolors='black')

        # direction
        da = target[0] - a0
        db = target[1] - b0

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

    plt.title("V9.2 Path Selection Navigation")
    plt.xlabel("α")
    plt.ylabel("β")
    plt.legend()

    out = os.path.join(OUTPUT_DIR, "v9_2_path_selection.png")
    plt.savefig(out, dpi=150)
    plt.close()

    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
