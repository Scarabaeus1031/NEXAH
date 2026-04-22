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
# 3. DEVIATION + DENSITY
# =========================

def compute_deviation(beta, gamma):
    return np.sqrt(beta**2 + gamma**2)


def density_field(alpha, beta, D, bins=220):
    H, xedges, yedges = np.histogram2d(alpha, beta, bins=bins, weights=D)
    H = gaussian_filter(H, sigma=2.0)
    return H, xedges, yedges


def extract_ridge(H, q=0.97):
    thresh = np.quantile(H, q)
    mask = H > thresh
    return np.argwhere(mask), thresh


# =========================
# 4. GRID -> COORDS
# =========================

def grid_to_coords(ridge_idx, xedges, yedges):
    xs = 0.5 * (xedges[:-1] + xedges[1:])
    ys = 0.5 * (yedges[:-1] + yedges[1:])

    coords = []
    for i, j in ridge_idx:
        coords.append([xs[i], ys[j]])

    return np.array(coords, dtype=float)


# =========================
# 5. PATH SPLIT + ORDERING
# =========================

def split_paths(coords):
    paths = {
        "left_upper": [],
        "left_lower": [],
        "right_upper": [],
        "right_lower": [],
    }

    for x, y in coords:
        if x < 0 and y > 0:
            paths["left_upper"].append([x, y])
        elif x < 0 and y <= 0:
            paths["left_lower"].append([x, y])
        elif x >= 0 and y > 0:
            paths["right_upper"].append([x, y])
        else:
            paths["right_lower"].append([x, y])

    for k in paths:
        if len(paths[k]) > 0:
            pts = np.array(paths[k], dtype=float)

            # adaptive ordering:
            # if path is mostly horizontal, sort by x
            # if mostly vertical, sort by y
            spread_x = np.std(pts[:, 0])
            spread_y = np.std(pts[:, 1])

            if spread_x >= spread_y:
                order = np.argsort(pts[:, 0])
            else:
                order = np.argsort(pts[:, 1])

            pts = pts[order]

            filtered = [pts[0]]
            for p in pts[1:]:
                if np.linalg.norm(p - filtered[-1]) > 0.2:
                    filtered.append(p)

            paths[k] = np.array(filtered, dtype=float)
        else:
            paths[k] = np.empty((0, 2), dtype=float)

    return paths


# =========================
# 6. RIDGE TANGENTS
# =========================

def compute_path_tangents(path):
    if len(path) < 2:
        return np.empty((0, 2), dtype=float)

    tangents = np.zeros_like(path)

    for i in range(len(path)):
        if i == 0:
            t = path[i + 1] - path[i]
        elif i == len(path) - 1:
            t = path[i] - path[i - 1]
        else:
            t = path[i + 1] - path[i - 1]

        n = np.linalg.norm(t)
        if n > 0:
            t = t / n

        tangents[i] = t

    return tangents


def build_tangent_field(paths):
    field = {}
    for name, path in paths.items():
        if len(path) >= 2:
            field[name] = {
                "points": path,
                "tangents": compute_path_tangents(path),
            }
        else:
            field[name] = {
                "points": np.empty((0, 2), dtype=float),
                "tangents": np.empty((0, 2), dtype=float),
            }
    return field


# =========================
# 7. DENSITY GRADIENT FIELD
# =========================

def compute_density_gradient(H):
    # H shape follows histogram2d: [xbin, ybin]
    gx, gy = np.gradient(H)
    return gx, gy


def interpolate_grid_vector(x, y, gx, gy, xedges, yedges):
    xi = np.searchsorted(xedges, x) - 1
    yi = np.searchsorted(yedges, y) - 1

    if xi < 0 or yi < 0 or xi >= gx.shape[0] or yi >= gx.shape[1]:
        return None

    return np.array([gx[xi, yi], gy[xi, yi]], dtype=float)


# =========================
# 8. HELPERS
# =========================

def nearest_index(points, p):
    if len(points) == 0:
        return None
    d = np.linalg.norm(points - p, axis=1)
    return int(np.argmin(d))


def choose_best_path(point, paths):
    best_key = None
    best_dist = np.inf

    for name, pts in paths.items():
        if len(pts) == 0:
            continue
        d = np.min(np.linalg.norm(pts - point, axis=1))
        if d < best_dist:
            best_dist = d
            best_key = name

    return best_key, best_dist


# =========================
# 9. HYBRID FLOW INTEGRATION
# =========================

def integrate_hybrid_flow(
    start,
    tangent_field,
    path_name,
    gx,
    gy,
    xedges,
    yedges,
    step_size=0.7,
    n_steps=35,
    w_ridge=0.55,
    w_attr=0.20,
    w_grad=0.25,
):
    if path_name is None:
        return np.array([start], dtype=float)

    points = tangent_field[path_name]["points"]
    tangents = tangent_field[path_name]["tangents"]

    if len(points) < 2:
        return np.array([start], dtype=float)

    pos = start.astype(float).copy()
    traj = [pos.copy()]

    for _ in range(n_steps):
        idx = nearest_index(points, pos)
        if idx is None:
            break

        # ridge tangent
        ridge_tangent = tangents[idx].copy()

        # attraction to nearest ridge point
        attract = points[idx] - pos
        a_norm = np.linalg.norm(attract)
        if a_norm > 0:
            attract = attract / a_norm
        else:
            attract = np.zeros(2)

        # density gradient
        grad = interpolate_grid_vector(pos[0], pos[1], gx, gy, xedges, yedges)
        if grad is None:
            break
        g_norm = np.linalg.norm(grad)
        if g_norm > 0:
            grad = grad / g_norm
        else:
            grad = np.zeros(2)

        # hybrid vector
        v = (
            w_ridge * ridge_tangent
            + w_attr * attract
            + w_grad * grad
        )

        v_norm = np.linalg.norm(v)
        if v_norm < 1e-9:
            break

        v = v / v_norm
        pos = pos + step_size * v
        traj.append(pos.copy())

    return np.array(traj, dtype=float)


# =========================
# 10. MAIN
# =========================

def main():
    print("Running V11.2 Hybrid Flow Field...")

    X = generate_lorenz()

    e1, e2, e3 = compute_basis(X)
    alpha, beta, gamma = project(X, e1, e2, e3)

    D = compute_deviation(beta, gamma)

    H, xedges, yedges = density_field(alpha, beta, D)
    gx, gy = compute_density_gradient(H)

    ridge_idx, ridge_thresh = extract_ridge(H, q=0.97)
    coords = grid_to_coords(ridge_idx, xedges, yedges)

    paths = split_paths(coords)
    tangent_field = build_tangent_field(paths)

    idxs = np.linspace(4500, 4999, 6).astype(int)
    starts = np.array([[alpha[i], beta[i]] for i in idxs], dtype=float)

    plt.figure(figsize=(10, 8))
    plt.imshow(
        H.T,
        origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto",
        cmap="viridis"
    )

    # ridge
    plt.scatter(coords[:, 0], coords[:, 1], s=5, c="red", label="ridge")

    colors = {
        "left_upper": "cyan",
        "left_lower": "blue",
        "right_upper": "orange",
        "right_lower": "yellow",
    }

    # path guides
    for name, pts in paths.items():
        if len(pts) > 1:
            plt.plot(pts[:, 0], pts[:, 1], color=colors[name], linewidth=1.8, alpha=0.85)

    # trajectories
    for i, s in enumerate(starts):
        best_path, best_dist = choose_best_path(s, paths)

        traj = integrate_hybrid_flow(
            start=s,
            tangent_field=tangent_field,
            path_name=best_path,
            gx=gx,
            gy=gy,
            xedges=xedges,
            yedges=yedges,
            step_size=0.7,
            n_steps=38,
            w_ridge=0.55,
            w_attr=0.20,
            w_grad=0.25,
        )

        plt.scatter(s[0], s[1], c="white", edgecolors="black", s=110, zorder=5)

        if len(traj) > 1:
            plt.plot(traj[:, 0], traj[:, 1], linewidth=2.2, color="white", alpha=0.95)
            plt.scatter(traj[:, 0], traj[:, 1], s=14, color="white", alpha=0.9)

            p1 = traj[-2]
            p2 = traj[-1]
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
            f"Sample {i} | path={best_path} | "
            f"start=({s[0]:.2f}, {s[1]:.2f}) | "
            f"dist={best_dist:.3f}"
        )

    plt.title("V11.2 Hybrid Flow Field Trajectories")
    plt.xlabel("α")
    plt.ylabel("β")
    plt.legend()

    out_path = os.path.join(OUTPUT_DIR, "v11_2_hybrid_flow.png")
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()

    print("Saved:", out_path)
    print(f"Ridge threshold: {ridge_thresh:.4f}")
    for name, pts in paths.items():
        print(f"{name}: {len(pts)} nodes")


if __name__ == "__main__":
    main()
