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
# 2. PCA
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


def density_field(alpha, beta, D, bins=200):
    H, xedges, yedges = np.histogram2d(alpha, beta, bins=bins, weights=D)
    H = gaussian_filter(H, sigma=2)
    return H, xedges, yedges


def extract_ridge(H, q=0.97):
    thresh = np.quantile(H, q)
    mask = H > thresh
    return np.argwhere(mask)


# =========================
# 4. GRID → COORDS
# =========================

def grid_to_coords(ridge_idx, xedges, yedges):
    xs = (xedges[:-1] + xedges[1:]) / 2
    ys = (yedges[:-1] + yedges[1:]) / 2

    coords = []
    for i, j in ridge_idx:
        coords.append([xs[i], ys[j]])

    return np.array(coords)


# =========================
# 5. PATH SPLIT
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
        paths[k] = np.array(paths[k]) if len(paths[k]) > 0 else np.empty((0,2))

    return paths


# =========================
# 6. DISTANCE HELPERS
# =========================

def nearest_point(path, point):
    if len(path) == 0:
        return None, np.inf

    dists = np.linalg.norm(path - point, axis=1)
    idx = np.argmin(dists)
    return path[idx], dists[idx]


def path_to_goal_distance(path, goal):
    if len(path) == 0:
        return np.inf

    dists = np.linalg.norm(path - goal, axis=1)
    return np.min(dists)


# =========================
# 7. GOAL-BASED DECISION
# =========================

def choose_best_path(point, paths, goal):
    best_path = None
    best_cost = np.inf
    best_target = None

    for name, path in paths.items():
        p_near, d1 = nearest_point(path, point)
        d2 = path_to_goal_distance(path, goal)

        cost = d1 + d2

        if cost < best_cost:
            best_cost = cost
            best_path = name
            best_target = p_near

    return best_path, best_target, best_cost


# =========================
# 8. MAIN
# =========================

def main():
    print("Running V10.1 Goal Navigation...")

    X = generate_lorenz()

    e1, e2, e3 = compute_basis(X)
    alpha, beta, gamma = project(X, e1, e2, e3)

    D = compute_deviation(beta, gamma)

    H, xedges, yedges = density_field(alpha, beta, D)

    ridge_idx = extract_ridge(H)
    coords = grid_to_coords(ridge_idx, xedges, yedges)

    paths = split_paths(coords)

    # 🎯 GOAL (right attractor)
    goal = np.array([10, 5])

    # sample states
    idxs = np.linspace(4500, 4999, 6).astype(int)
    points = np.array([[alpha[i], beta[i]] for i in idxs])

    plt.figure(figsize=(10, 8))
    plt.imshow(H.T, origin="lower",
               extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
               aspect="auto", cmap="viridis")

    # plot ridge
    plt.scatter(coords[:,0], coords[:,1], s=5, c="red", label="ridge")

    # goal
    plt.scatter(goal[0], goal[1], c="yellow", s=200, edgecolors="black", label="goal")

    for i, p in enumerate(points):
        path, target, cost = choose_best_path(p, paths, goal)

        plt.scatter(p[0], p[1], c="white", edgecolors="black", s=120)

        if target is not None:
            plt.arrow(p[0], p[1],
                      target[0]-p[0],
                      target[1]-p[1],
                      color="white",
                      head_width=1.0,
                      length_includes_head=True)

        print(f"Sample {i} | path={path} | cost={cost:.3f}")

    plt.title("V10.1 Goal-Directed Navigation")
    plt.xlabel("α")
    plt.ylabel("β")
    plt.legend()

    out_path = os.path.join(OUTPUT_DIR, "v10_1_goal_navigation.png")
    plt.savefig(out_path, dpi=200)
    plt.close()

    print("Saved:", out_path)


if __name__ == "__main__":
    main()
