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

    for k in paths:
        if len(paths[k]) > 0:
            pts = np.array(paths[k])
            # simple ordering by beta then alpha
            order = np.lexsort((pts[:, 0], pts[:, 1]))
            paths[k] = pts[order]
        else:
            paths[k] = np.empty((0, 2))

    return paths


# =========================
# 6. PATH SELECTION
# =========================

def choose_best_path(a0, b0, paths):
    best_key = None
    best_score = np.inf

    for key, pts in paths.items():
        if len(pts) == 0:
            continue

        dists = np.sqrt((pts[:, 0] - a0) ** 2 + (pts[:, 1] - b0) ** 2)
        score = np.mean(np.sort(dists)[: min(5, len(dists))])

        if score < best_score:
            best_score = score
            best_key = key

    return best_key


# =========================
# 7. PATH FOLLOWING
# =========================

def nearest_index_on_path(a, b, path):
    dists = np.sqrt((path[:, 0] - a) ** 2 + (path[:, 1] - b) ** 2)
    return int(np.argmin(dists))


def follow_path(a0, b0, path, step_size=1.5, n_steps=12):
    """
    Create a simple path-following trajectory:
    - project current point to nearest path node
    - advance node by node
    - interpolate step direction
    """
    if len(path) < 2:
        return np.array([[a0, b0]])

    idx = nearest_index_on_path(a0, b0, path)

    traj = [[a0, b0]]
    current = np.array([a0, b0], dtype=float)

    for _ in range(n_steps):
        next_idx = min(idx + 1, len(path) - 1)
        target = path[next_idx]

        direction = target - current
        norm = np.linalg.norm(direction)

        if norm < 1e-8:
            idx = next_idx
            if idx == len(path) - 1:
                break
            continue

        move = direction / norm * min(step_size, norm)
        current = current + move
        traj.append(current.copy())

        if np.linalg.norm(target - current) < 0.25 and idx < len(path) - 1:
            idx = next_idx

        if idx == len(path) - 1 and np.linalg.norm(path[-1] - current) < 0.25:
            break

    return np.array(traj)


# =========================
# 8. MAIN
# =========================

def main():
    print("Running V9.3 Continuous Path Following...")

    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    e1, e2, e3 = compute_basis(X)
    alpha, beta, gamma = project(X, e1, e2, e3)

    D = compute_deviation(beta, gamma)

    H, xedges, yedges = density_field(alpha, beta, D)
    ridge_idx, ridge_thresh = extract_ridge(H)

    ridge_alpha = xedges[ridge_idx[:, 0]]
    ridge_beta = yedges[ridge_idx[:, 1]]

    paths = split_paths(ridge_alpha, ridge_beta)

    # sample a few recent states
    indices = np.linspace(len(alpha) - 500, len(alpha) - 1, 6).astype(int)

    plt.figure(figsize=(9, 7))

    plt.imshow(
        H.T,
        origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto"
    )

    # plot ridge points
    plt.scatter(ridge_alpha, ridge_beta, s=8, color="red", label="ridge")

    # plot path groups
    colors = {
        "left_upper": "cyan",
        "left_lower": "blue",
        "right_upper": "orange",
        "right_lower": "yellow"
    }

    for key, pts in paths.items():
        if len(pts) > 1:
            plt.plot(pts[:, 0], pts[:, 1], linewidth=2, color=colors[key], alpha=0.8)

    # follow selected paths
    for t in indices:
        a0 = alpha[t]
        b0 = beta[t]

        key = choose_best_path(a0, b0, paths)
        if key is None:
            continue

        path = paths[key]
        traj = follow_path(a0, b0, path, step_size=1.5, n_steps=14)

        # current point
        plt.scatter(a0, b0, s=90, color="white", edgecolors="black", zorder=5)

        # trajectory
        if len(traj) > 1:
            plt.plot(traj[:, 0], traj[:, 1], color="white", linewidth=2.2, alpha=0.95)
            plt.scatter(traj[:, 0], traj[:, 1], s=18, color="white", alpha=0.95)

            # arrow at end segment
            p1 = traj[-2]
            p2 = traj[-1]
            d = p2 - p1
            n = np.linalg.norm(d)
            if n > 0:
                d = d / n
                plt.arrow(
                    p2[0], p2[1],
                    d[0] * 0.001, d[1] * 0.001,  # tiny shaft, head emphasized
                    color="white",
                    head_width=1.1,
                    head_length=1.5,
                    length_includes_head=True,
                    zorder=6
                )

    plt.title("V9.3 Continuous Path Following")
    plt.xlabel("α")
    plt.ylabel("β")
    plt.legend()

    out = os.path.join(OUTPUT_DIR, "v9_3_path_following.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")
    print(f"Ridge threshold: {ridge_thresh:.4f}")
    for key, pts in paths.items():
        print(f"{key}: {len(pts)} nodes")


if __name__ == "__main__":
    main()
