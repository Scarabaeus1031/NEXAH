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
    da = np.diff(alpha, prepend=alpha[0])
    db = np.diff(beta, prepend=beta[0])

    P, xedges, yedges = np.histogram2d(alpha, beta, bins=bins)

    Fx, _, _ = np.histogram2d(alpha, beta, bins=[xedges, yedges], weights=da)
    Fy, _, _ = np.histogram2d(alpha, beta, bins=[xedges, yedges], weights=db)

    P = gaussian_filter(P, sigma=sigma)
    Fx = gaussian_filter(Fx, sigma=sigma)
    Fy = gaussian_filter(Fy, sigma=sigma)

    eps = 1e-8
    Vx = Fx / (P + eps)
    Vy = Fy / (P + eps)

    Vx = gaussian_filter(Vx, sigma=1.0)
    Vy = gaussian_filter(Vy, sigma=1.0)

    xc = 0.5 * (xedges[:-1] + xedges[1:])
    yc = 0.5 * (yedges[:-1] + yedges[1:])

    return P, Vx, Vy, xedges, yedges, xc, yc


# =========================
# 5. FIELD DERIVATIVES
# =========================

def compute_field_derivatives(Vx, Vy):
    dVx_dx, dVx_dy = np.gradient(Vx)
    dVy_dx, dVy_dy = np.gradient(Vy)

    divergence = dVx_dx + dVy_dy
    curl_z = dVy_dx - dVx_dy

    return divergence, curl_z


# =========================
# 6. INTERPOLATION
# =========================

def interpolate_field(x, y, Vx, Vy, xedges, yedges):
    ix = np.searchsorted(xedges, x) - 1
    iy = np.searchsorted(yedges, y) - 1

    if ix < 0 or iy < 0 or ix >= Vx.shape[0] or iy >= Vy.shape[1]:
        return None

    return np.array([Vx[ix, iy], Vy[ix, iy]], dtype=float)


def interpolate_scalar(x, y, F, xedges, yedges):
    ix = np.searchsorted(xedges, x) - 1
    iy = np.searchsorted(yedges, y) - 1

    if ix < 0 or iy < 0 or ix >= F.shape[0] or iy >= F.shape[1]:
        return None

    return float(F[ix, iy])


# =========================
# 7. STREAMLINE INTEGRATION
# =========================

def integrate_streamline(start, Vx, Vy, xedges, yedges, step_size=0.75, n_steps=75):
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
# 8. CURVATURE
# =========================

def compute_signed_curvature(path):
    """
    Signed curvature for 2D path.
    Returns array with same length as path.
    Positive/negative ~ local turning direction.
    """
    n = len(path)
    if n < 3:
        return np.zeros(n, dtype=float)

    kappa = np.zeros(n, dtype=float)

    x = path[:, 0]
    y = path[:, 1]

    dx = np.gradient(x)
    dy = np.gradient(y)
    ddx = np.gradient(dx)
    ddy = np.gradient(dy)

    denom = (dx * dx + dy * dy) ** 1.5 + 1e-8
    num = dx * ddy - dy * ddx
    kappa = num / denom

    return kappa


def classify_path_topology(path, curl_z, divergence, xedges, yedges):
    """
    Very simple topology label from mean |curl| and |div|.
    """
    vals_curl = []
    vals_div = []

    for p in path:
        c = interpolate_scalar(p[0], p[1], curl_z, xedges, yedges)
        d = interpolate_scalar(p[0], p[1], divergence, xedges, yedges)
        if c is not None:
            vals_curl.append(c)
        if d is not None:
            vals_div.append(d)

    if len(vals_curl) == 0 or len(vals_div) == 0:
        return "unknown"

    mean_abs_curl = np.mean(np.abs(vals_curl))
    mean_abs_div = np.mean(np.abs(vals_div))

    if mean_abs_curl > mean_abs_div * 1.25:
        return "rotation"
    elif mean_abs_div > mean_abs_curl * 1.25:
        return "transport"
    else:
        return "transition"


# =========================
# 9. MAIN
# =========================

def main():
    print("Running V11.4 Curvature + Topology...")

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

    divergence, curl_z = compute_field_derivatives(Vx, Vy)

    idxs = np.linspace(4500, 4999, 6).astype(int)
    starts = np.array([[alpha[i], beta[i]] for i in idxs], dtype=float)

    # ---------- Figure ----------
    fig = plt.figure(figsize=(16, 12))

    # Q1: Flux field + streamlines
    ax1 = fig.add_subplot(221)
    ax1.imshow(
        P.T,
        origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto",
        cmap="viridis"
    )

    step = 8
    Xg, Yg = np.meshgrid(xc, yc, indexing="ij")
    ax1.quiver(
        Xg[::step, ::step],
        Yg[::step, ::step],
        Vx[::step, ::step],
        Vy[::step, ::step],
        color="white",
        alpha=0.35,
        scale=35,
        width=0.0025
    )

    all_paths = []
    topo_labels = []

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
        all_paths.append(path)

        label = classify_path_topology(path, curl_z, divergence, xedges, yedges)
        topo_labels.append(label)

        ax1.scatter(s[0], s[1], c="white", edgecolors="black", s=110, zorder=5)
        if len(path) > 1:
            ax1.plot(path[:, 0], path[:, 1], linewidth=2.0, color="white", alpha=0.95)

    ax1.set_title("Q1 — Flux Streamlines")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")

    # Q2: Signed curvature on streamlines
    ax2 = fig.add_subplot(222)
    ax2.imshow(
        P.T,
        origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto",
        cmap="viridis"
    )

    for path in all_paths:
        if len(path) < 3:
            continue

        kappa = compute_signed_curvature(path)
        sc = ax2.scatter(
            path[:, 0], path[:, 1],
            c=kappa,
            s=18,
            cmap="coolwarm",
            vmin=-0.25,
            vmax=0.25
        )

    ax2.set_title("Q2 — Signed Curvature (concave / convex)")
    ax2.set_xlabel("α")
    ax2.set_ylabel("β")
    cbar2 = fig.colorbar(sc, ax=ax2, shrink=0.85)
    cbar2.set_label("signed curvature")

    # Q3: Curl field
    ax3 = fig.add_subplot(223)
    im3 = ax3.imshow(
        curl_z.T,
        origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto",
        cmap="PuOr"
    )

    for path, label in zip(all_paths, topo_labels):
        if len(path) > 1:
            ax3.plot(path[:, 0], path[:, 1], linewidth=2.0, color="white", alpha=0.9)

    ax3.set_title("Q3 — Curl Field + Paths")
    ax3.set_xlabel("α")
    ax3.set_ylabel("β")
    cbar3 = fig.colorbar(im3, ax=ax3, shrink=0.85)
    cbar3.set_label("curl")

    # Q4: Topology summary
    ax4 = fig.add_subplot(224)
    colors = {
        "rotation": "orange",
        "transport": "cyan",
        "transition": "magenta",
        "unknown": "gray",
    }

    ax4.imshow(
        P.T,
        origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto",
        cmap="viridis"
    )

    for path, label, s in zip(all_paths, topo_labels, starts):
        if len(path) > 1:
            ax4.plot(path[:, 0], path[:, 1], linewidth=2.4, color=colors[label], alpha=0.95)
            ax4.scatter(s[0], s[1], c="white", edgecolors="black", s=110)

    # legend-like text
    summary = {}
    for label in topo_labels:
        summary[label] = summary.get(label, 0) + 1

    txt = "\n".join([f"{k}: {v}" for k, v in summary.items()])
    ax4.text(
        0.02, 0.98, txt,
        transform=ax4.transAxes,
        ha="left", va="top",
        fontsize=10,
        bbox=dict(facecolor="black", alpha=0.4, edgecolor="white")
    )

    ax4.set_title("Q4 — Topology Classes")
    ax4.set_xlabel("α")
    ax4.set_ylabel("β")

    fig.suptitle("V11.4 Curvature + Topology Layer", fontsize=22)
    out_path = os.path.join(OUTPUT_DIR, "v11_4_curvature_topology.png")
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()

    print("Saved:", out_path)
    print(f"Density max: {np.max(P):.4f}")
    print(f"Mean |V|: {np.mean(np.sqrt(Vx**2 + Vy**2)):.6f}")
    print("Topology classes:")
    for i, label in enumerate(topo_labels):
        print(f"  Sample {i}: {label}")


if __name__ == "__main__":
    main()
