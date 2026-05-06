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
# 2. PCA Projection
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
# 3. Deviation + Density
# =========================

def compute_deviation(beta, gamma):
    return np.sqrt(beta**2 + gamma**2)


def density_field(alpha, beta, D, bins=200):
    H, xedges, yedges = np.histogram2d(alpha, beta, bins=bins, weights=D)
    H = gaussian_filter(H, sigma=2)
    return H, xedges, yedges


# =========================
# 4. VECTOR FIELD
# =========================

def compute_vector_field(H):
    gy, gx = np.gradient(H)  # important: numpy order
    return gx, gy


# =========================
# 5. INTERPOLATION
# =========================

def interpolate_vector(x, y, gx, gy, xedges, yedges):
    xi = np.searchsorted(xedges, x) - 1
    yi = np.searchsorted(yedges, y) - 1

    if xi < 0 or yi < 0 or xi >= gx.shape[0] or yi >= gx.shape[1]:
        return None

    return np.array([gx[xi, yi], gy[xi, yi]])


# =========================
# 6. TRAJECTORY INTEGRATION
# =========================

def integrate_path(start, gx, gy, xedges, yedges, steps=100, step_size=0.5):
    path = [start.copy()]
    pos = start.copy()

    for _ in range(steps):
        v = interpolate_vector(pos[0], pos[1], gx, gy, xedges, yedges)

        if v is None:
            break

        norm = np.linalg.norm(v)
        if norm < 1e-5:
            break

        v = v / norm  # normalize

        pos = pos + v * step_size
        path.append(pos.copy())

    return np.array(path)


# =========================
# 7. MAIN
# =========================

def main():
    print("Running V11 Flow Trajectories...")

    X = generate_lorenz()

    e1, e2, e3 = compute_basis(X)
    alpha, beta, gamma = project(X, e1, e2, e3)

    D = compute_deviation(beta, gamma)

    H, xedges, yedges = density_field(alpha, beta, D)

    gx, gy = compute_vector_field(H)

    # sample start points
    idxs = np.linspace(4500, 4999, 6).astype(int)
    starts = np.array([[alpha[i], beta[i]] for i in idxs])

    plt.figure(figsize=(10, 8))
    plt.imshow(H.T, origin="lower",
               extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
               aspect="auto", cmap="viridis")

    for i, s in enumerate(starts):
        path = integrate_path(s, gx, gy, xedges, yedges)

        plt.plot(path[:,0], path[:,1], linewidth=2)
        plt.scatter(s[0], s[1], c="white", edgecolors="black", s=100)

    plt.title("V11 Continuous Flow Trajectories")
    plt.xlabel("α")
    plt.ylabel("β")

    out_path = os.path.join(OUTPUT_DIR, "v11_flow_trajectories.png")
    plt.savefig(out_path, dpi=200)
    plt.close()

    print("Saved:", out_path)


if __name__ == "__main__":
    main()
