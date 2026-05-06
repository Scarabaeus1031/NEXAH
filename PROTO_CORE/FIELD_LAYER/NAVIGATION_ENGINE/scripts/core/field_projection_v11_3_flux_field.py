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
# 4. EMPIRICAL FLUX FIELD
# =========================

def estimate_flux_field(alpha, beta, bins=180, sigma=2.0):
    """
    Build empirical density p and mean velocity field J/p on the alpha-beta plane.

    Returns:
        P      : smoothed density
        Vx, Vy : smoothed mean local velocity
        xedges, yedges
        xc, yc : bin centers
    """
    # local velocities from projected trajectory
    da = np.diff(alpha, prepend=alpha[0])
    db = np.diff(beta, prepend=beta[0])

    # occupancy / density
    P, xedges, yedges = np.histogram2d(alpha, beta, bins=bins)

    # accumulated velocity
    Fx, _, _ = np.histogram2d(alpha, beta, bins=[xedges, yedges], weights=da)
    Fy, _, _ = np.histogram2d(alpha, beta, bins=[xedges, yedges], weights=db)

    # smooth everything
    P = gaussian_filter(P, sigma=sigma)
    Fx = gaussian_filter(Fx, sigma=sigma)
    Fy = gaussian_filter(Fy, sigma=sigma)

    # avoid division by zero
    eps = 1e-8
    Vx = Fx / (P + eps)
    Vy = Fy / (P + eps)

    # optional mild smoothing on velocity field
    Vx = gaussian_filter(Vx, sigma=1.0)
    Vy = gaussian_filter(Vy, sigma=1.0)

    xc = 0.5 * (xedges[:-1] + xedges[1:])
    yc = 0.5 * (yedges[:-1] + yedges[1:])

    return P, Vx, Vy, xedges, yedges, xc, yc


# =========================
# 5. STREAMLINE INTEGRATION
# =========================

def interpolate_field(x, y, Vx, Vy, xedges, yedges):
    """
    Nearest-cell interpolation for velocity field.
    """
    ix = np.searchsorted(xedges, x) - 1
    iy = np.searchsorted(yedges, y) - 1

    if ix < 0 or iy < 0 or ix >= Vx.shape[0] or iy >= Vx.shape[1]:
        return None

    return np.array([Vx[ix, iy], Vy[ix, iy]], dtype=float)


def integrate_streamline(start, Vx, Vy, xedges, yedges, step_size=0.8, n_steps=60):
    """
    Forward integration in the empirical velocity field.
    """
    pos = np.array(start, dtype=float)
    path = [pos.copy()]

    for _ in range(n_steps):
        v = interpolate_field(pos[0], pos[1], Vx, Vy, xedges, yedges)
        if v is None:
            break

        n = np.linalg.norm(v)
        if n < 1e-7:
            break

        v = v / n
        pos = pos + step_size * v
        path.append(pos.copy())

    return np.array(path, dtype=float)


# =========================
# 6. MAIN
# =========================

def main():
    print("Running V11.3 Flux Field...")

    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    e1, e2, e3 = compute_basis(X)
    alpha, beta, gamma = project(X, e1, e2, e3)

    D = compute_deviation(beta, gamma)

    P, Vx, Vy, xedges, yedges, xc, yc = estimate_flux_field(
        alpha, beta,
        bins=180,
        sigma=2.0
    )

    # sample starts from later part of trajectory
    idxs = np.linspace(4500, 4999, 6).astype(int)
    starts = np.array([[alpha[i], beta[i]] for i in idxs], dtype=float)

    # quiver grid subsampling for readability
    step = 8
    Xg, Yg = np.meshgrid(xc, yc, indexing="ij")

    plt.figure(figsize=(10, 8))
    plt.imshow(
        P.T,
        origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto",
        cmap="viridis"
    )

    # vector field preview
    plt.quiver(
        Xg[::step, ::step],
        Yg[::step, ::step],
        Vx[::step, ::step],
        Vy[::step, ::step],
        color="white",
        alpha=0.35,
        scale=35,
        width=0.0025
    )

    # streamlines from selected starts
    for i, s in enumerate(starts):
        path = integrate_streamline(
            start=s,
            Vx=Vx,
            Vy=Vy,
            xedges=xedges,
            yedges=yedges,
            step_size=0.75,
            n_steps=75
        )

        plt.scatter(s[0], s[1], c="white", edgecolors="black", s=110, zorder=5)

        if len(path) > 1:
            plt.plot(path[:, 0], path[:, 1], linewidth=2.2, color="white", alpha=0.95)
            plt.scatter(path[:, 0], path[:, 1], s=10, color="white", alpha=0.8)

            p1 = path[-2]
            p2 = path[-1]
            d = p2 - p1
            n = np.linalg.norm(d)
            if n > 0:
                d = d / n
                plt.arrow(
                    p2[0], p2[1],
                    d[0] * 0.001, d[1] * 0.001,
                    color="white",
                    head_width=1.0,
                    head_length=1.4,
                    length_includes_head=True,
                    zorder=6
                )

        print(
            f"Sample {i} | start=({s[0]:.2f}, {s[1]:.2f}) | path_len={len(path)}"
        )

    plt.title("V11.3 Empirical Flux Field Trajectories")
    plt.xlabel("α")
    plt.ylabel("β")

    out_path = os.path.join(OUTPUT_DIR, "v11_3_flux_field.png")
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()

    print("Saved:", out_path)
    print(f"Density max: {np.max(P):.4f}")
    print(f"Mean |V|: {np.mean(np.sqrt(Vx**2 + Vy**2)):.6f}")


if __name__ == "__main__":
    main()
