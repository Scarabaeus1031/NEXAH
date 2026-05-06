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

def generate_lorenz(n_steps: int = 5000, dt: float = 0.01) -> np.ndarray:
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

def compute_basis(X: np.ndarray) -> np.ndarray:
    pca = PCA(n_components=3)
    pca.fit(X)
    return pca.components_


def project(X: np.ndarray, e1: np.ndarray, e2: np.ndarray, e3: np.ndarray):
    alpha = X @ e1
    beta = X @ e2
    gamma = X @ e3
    return alpha, beta, gamma


# =========================
# 3. DEVIATION
# =========================

def compute_deviation(beta: np.ndarray, gamma: np.ndarray) -> np.ndarray:
    return np.sqrt(beta**2 + gamma**2)


# =========================
# 4. DENSITY FIELD
# =========================

def density_field(alpha: np.ndarray, beta: np.ndarray, D: np.ndarray, bins: int = 200):
    H, xedges, yedges = np.histogram2d(alpha, beta, bins=bins, weights=D)
    H = gaussian_filter(H, sigma=2)
    return H, xedges, yedges


def extract_ridge(H: np.ndarray, q: float = 0.97):
    thresh = np.quantile(H, q)
    mask = H > thresh
    return np.argwhere(mask), thresh


# =========================
# 5. PATH GROUPS
# =========================

def split_paths(ridge_alpha: np.ndarray, ridge_beta: np.ndarray):
    paths = {
        "left_upper": [],
        "left_lower": [],
        "right_upper": [],
        "right_lower": [],
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

    for key in paths:
        if len(paths[key]) > 0:
            pts = np.array(paths[key], dtype=float)
            order = np.lexsort((pts[:, 0], pts[:, 1]))
            paths[key] = pts[order]
        else:
            paths[key] = np.empty((0, 2), dtype=float)

    return paths


# =========================
# 6. PATH COSTS
# =========================

def point_to_path_distance(a0: float, b0: float, path: np.ndarray) -> float:
    if len(path) == 0:
        return np.inf
    d = np.sqrt((path[:, 0] - a0) ** 2 + (path[:, 1] - b0) ** 2)
    return float(np.min(d))


def choose_best_path(a0: float, b0: float, paths: dict):
    best_key = None
    best_cost = np.inf

    for key, pts in paths.items():
        cost = point_to_path_distance(a0, b0, pts)
        if cost < best_cost:
            best_cost = cost
            best_key = key

    return best_key, best_cost


def choose_path_with_switching(
    a0: float,
    b0: float,
    paths: dict,
    current_path: str | None,
    switching_penalty: float = 2.0,
    switch_margin: float = 0.5,
):
    raw_costs = {}
    for key, pts in paths.items():
        raw_costs[key] = point_to_path_distance(a0, b0, pts)

    adjusted_costs = {}
    for key, cost in raw_costs.items():
        if current_path is not None and key != current_path:
            adjusted_costs[key] = cost + switching_penalty
        else:
            adjusted_costs[key] = cost

    best_key = min(adjusted_costs, key=adjusted_costs.get)
    best_cost = adjusted_costs[best_key]

    switched = False
    if current_path is not None and best_key != current_path:
        current_cost = adjusted_costs[current_path]
        if best_cost + switch_margin < current_cost:
            switched = True
        else:
            best_key = current_path
            best_cost = current_cost

    return best_key, best_cost, switched, raw_costs, adjusted_costs


# =========================
# 7. PATH FOLLOWING HELPERS
# =========================

def nearest_index_on_path(a: float, b: float, path: np.ndarray) -> int:
    d = np.sqrt((path[:, 0] - a) ** 2 + (path[:, 1] - b) ** 2)
    return int(np.argmin(d))


def follow_path(a0: float, b0: float, path: np.ndarray, step_size: float = 1.5, n_steps: int = 10):
    if len(path) < 2:
        return np.array([[a0, b0]], dtype=float)

    idx = nearest_index_on_path(a0, b0, path)
    current = np.array([a0, b0], dtype=float)
    traj = [current.copy()]

    for _ in range(n_steps):
        next_idx = min(idx + 1, len(path) - 1)
        target = path[next_idx]

        direction = target - current
        norm = np.linalg.norm(direction)

        if norm < 1e-9:
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

    return np.array(traj, dtype=float)


# =========================
# 8. MAIN
# =========================

def main():
    print("Running V10 Path Switching...")

    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    e1, e2, e3 = compute_basis(X)
    alpha, beta, gamma = project(X, e1, e2, e3)

    D = compute_deviation(beta, gamma)

    H, xedges, yedges = density_field(alpha, beta, D)
    ridge_idx, ridge_thresh = extract_ridge(H, q=0.97)

    ridge_alpha = xedges[ridge_idx[:, 0]]
    ridge_beta = yedges[ridge_idx[:, 1]]

    paths = split_paths(ridge_alpha, ridge_beta)

    path_colors = {
        "left_upper": "cyan",
        "left_lower": "blue",
        "right_upper": "orange",
        "right_lower": "yellow",
    }

    # Zustände aus jüngerer Trajektorie
    indices = np.linspace(len(alpha) - 500, len(alpha) - 1, 7).astype(int)

    # initialer "aktueller Pfad" aus erstem Punkt
    first_a = float(alpha[indices[0]])
    first_b = float(beta[indices[0]])
    current_path, _ = choose_best_path(first_a, first_b, paths)

    plt.figure(figsize=(9, 7))

    plt.imshow(
        H.T,
        origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto",
    )

    # Ridge
    plt.scatter(ridge_alpha, ridge_beta, s=8, color="red", label="ridge")

    # Pfade
    for key, pts in paths.items():
        if len(pts) > 1:
            plt.plot(pts[:, 0], pts[:, 1], linewidth=2.0, color=path_colors[key], alpha=0.9)

    summary = []

    for i, t in enumerate(indices):
        a0 = float(alpha[t])
        b0 = float(beta[t])

        chosen_path, chosen_cost, switched, raw_costs, adj_costs = choose_path_with_switching(
            a0,
            b0,
            paths,
            current_path=current_path,
            switching_penalty=2.0,
            switch_margin=0.5,
        )

        # falls Wechsel akzeptiert, aktueller Pfad aktualisieren
        if chosen_path != current_path:
            current_path = chosen_path

        path = paths[current_path]
        traj = follow_path(a0, b0, path, step_size=1.4, n_steps=10)

        # aktueller Zustand
        plt.scatter(a0, b0, s=95, color="white", edgecolors="black", zorder=6)

        # Trajektorie
        if len(traj) > 1:
            plt.plot(traj[:, 0], traj[:, 1], color="white", linewidth=2.1, alpha=0.95, zorder=5)
            plt.scatter(traj[:, 0], traj[:, 1], s=16, color="white", alpha=0.95, zorder=5)

            # Endpfeil
            p1 = traj[-2]
            p2 = traj[-1]
            d = p2 - p1
            n = np.linalg.norm(d)
            if n > 0:
                d = d / n
                plt.arrow(
                    p2[0],
                    p2[1],
                    d[0] * 0.001,
                    d[1] * 0.001,
                    color="white",
                    head_width=1.1,
                    head_length=1.5,
                    length_includes_head=True,
                    zorder=7,
                )

        # Marker, wenn Switch stattfand
        if switched:
            plt.scatter(a0, b0, s=180, facecolors="none", edgecolors="lime", linewidths=2.0, zorder=7)

        summary.append((i, t, a0, b0, current_path, switched, chosen_cost))

    plt.title("V10 Path Switching Navigation")
    plt.xlabel("α")
    plt.ylabel("β")
    plt.legend()

    out = os.path.join(OUTPUT_DIR, "v10_path_switching.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")
    print(f"Ridge threshold: {ridge_thresh:.4f}")
    for key, pts in paths.items():
        print(f"{key}: {len(pts)} nodes")

    print("\nDecisions:")
    for i, t, a0, b0, path_name, switched, cost in summary:
        tag = "SWITCH" if switched else "STAY"
        print(
            f"  Sample {i} | t={t} | α={a0:.2f}, β={b0:.2f} | "
            f"path={path_name} | {tag} | cost={cost:.3f}"
        )


if __name__ == "__main__":
    main()
