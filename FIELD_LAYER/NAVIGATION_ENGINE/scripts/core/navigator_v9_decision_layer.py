import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter


OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# 1. LORENZ SYSTEM
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
# 2. FIELD BASIS (PCA)
# =========================

def compute_basis(X):
    pca = PCA(n_components=3)
    pca.fit(X)
    return pca.components_


# =========================
# 3. PROJECTION
# =========================

def project(X, e1, e2, e3):
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
# 5. DENSITY FIELD
# =========================

def compute_density(alpha, beta, D, bins=200):
    H, xedges, yedges = np.histogram2d(alpha, beta, bins=bins, weights=D)
    H = gaussian_filter(H, sigma=2)
    return H, xedges, yedges


# =========================
# 6. RIDGE DETECTION
# =========================

def extract_ridge(H, threshold_quantile=0.97):
    thresh = np.quantile(H, threshold_quantile)
    ridge = np.argwhere(H > thresh)
    return ridge


# =========================
# 7. STATE CLASSIFICATION
# =========================

def classify_state(D_val, dD_val, D_thresh=12, dD_thresh=0.5):
    if D_val < D_thresh:
        return "entry"
    elif dD_val > dD_thresh:
        return "core"
    else:
        return "exit"


# =========================
# 8. ACTION POLICY
# =========================

def decide_action(state):
    if state == "entry":
        return "PREPARE"
    elif state == "core":
        return "INTERVENE"
    elif state == "exit":
        return "STABILIZE"
    return "UNKNOWN"


# =========================
# 9. MAIN
# =========================

def main():
    print("Running Navigator V9 (Visual Decision Layer)...")

    # Generate data
    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    # Basis + projection
    e1, e2, e3 = compute_basis(X)
    alpha, beta, gamma = project(X, e1, e2, e3)

    # Deviation + derivative
    D = compute_deviation(beta, gamma)
    dD = np.gradient(D)

    # Density field
    H, xedges, yedges = compute_density(alpha, beta, D)

    # Ridge
    ridge_idx = extract_ridge(H)

    # Convert ridge to coordinates
    ridge_alpha = xedges[ridge_idx[:, 0]]
    ridge_beta = yedges[ridge_idx[:, 1]]

    # =========================
    # SELECT CURRENT STATE
    # =========================

    t = -200  # sample point near end
    a0 = alpha[t]
    b0 = beta[t]
    D0 = D[t]
    dD0 = dD[t]

    state = classify_state(D0, dD0)
    action = decide_action(state)

    print(f"State: {state} | Action: {action}")
    print(f"Position: α={a0:.2f}, β={b0:.2f}")

    # =========================
    # DECISION DIRECTION
    # =========================

    # find nearest ridge point
    distances = np.sqrt((ridge_alpha - a0)**2 + (ridge_beta - b0)**2)
    idx = np.argmin(distances)

    target_a = ridge_alpha[idx]
    target_b = ridge_beta[idx]

    direction = np.array([target_a - a0, target_b - b0])

    # normalize arrow
    norm = np.linalg.norm(direction)
    if norm > 0:
        direction = direction / norm

    # =========================
    # PLOT
    # =========================

    plt.figure(figsize=(8,6))

    # density background
    plt.imshow(
        H.T,
        origin='lower',
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect='auto'
    )

    # ridge
    plt.scatter(ridge_alpha, ridge_beta, s=10, color='red', label='ridge')

    # current state
    color_map = {
        "entry": "blue",
        "core": "yellow",
        "exit": "green"
    }

    plt.scatter(a0, b0, s=100, color=color_map[state], edgecolors='black', label='current')

    # decision arrow
    plt.arrow(
        a0, b0,
        direction[0]*5, direction[1]*5,
        color='white',
        width=0.1,
        head_width=1.5,
        length_includes_head=True
    )

    plt.title(f"V9 Decision Layer — State: {state} | Action: {action}")
    plt.xlabel("α")
    plt.ylabel("β")
    plt.legend()

    out = os.path.join(OUTPUT_DIR, "v9_decision_layer.png")
    plt.savefig(out, dpi=150)
    plt.close()

    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
