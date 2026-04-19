import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter, maximum_filter

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
# PCA + Projection
# =========================

def compute_field_basis(X):
    pca = PCA(n_components=3)
    pca.fit(X)
    return pca.components_


def project_field(X, components):
    e1, e2, e3 = components
    alpha = X @ e1
    beta = X @ e2
    gamma = X @ e3
    return alpha, beta, gamma


# =========================
# Deviation
# =========================

def compute_deviation(beta, gamma):
    return np.sqrt(beta**2 + gamma**2)


# =========================
# Transition detection
# =========================

def detect_transitions(D):
    from scipy.ndimage import gaussian_filter1d
    D_smooth = gaussian_filter1d(D, sigma=2)
    threshold = np.mean(D_smooth) + 1.2 * np.std(D_smooth)
    return D_smooth, threshold


# =========================
# Density + Ridge
# =========================

def compute_density(alpha_b, beta_b, bins=140):
    H, a_edges, b_edges = np.histogram2d(alpha_b, beta_b, bins=bins)
    H = gaussian_filter(H, sigma=1.5)

    a_centers = 0.5 * (a_edges[:-1] + a_edges[1:])
    b_centers = 0.5 * (b_edges[:-1] + b_edges[1:])

    return H.T, a_centers, b_centers


def extract_ridges(H, percentile=90):
    thresh = np.percentile(H[H > 0], percentile)
    local_max = maximum_filter(H, size=3) == H
    return (H >= thresh) & local_max


# =========================
# Flow computation
# =========================

def compute_velocity(alpha, beta):
    d_alpha = np.diff(alpha, prepend=alpha[0])
    d_beta = np.diff(beta, prepend=beta[0])
    return d_alpha, d_beta


def estimate_flow(ridge_alpha, ridge_beta, alpha, beta, d_alpha, d_beta, radius=1.5):
    flow = []

    for ra, rb in zip(ridge_alpha, ridge_beta):
        dist = np.sqrt((alpha - ra)**2 + (beta - rb)**2)
        mask = dist < radius

        if np.sum(mask) < 5:
            flow.append((0, 0))
            continue

        vx = np.mean(d_alpha[mask])
        vy = np.mean(d_beta[mask])

        flow.append((vx, vy))

    return np.array(flow)


# =========================
# SEGMENTATION
# =========================

def classify_segments(ridge_alpha, flow):
    segments = []

    for a, (vx, vy) in zip(ridge_alpha, flow):

        # Richtung entlang alpha-Achse
        if abs(vx) < 0.1:
            segments.append("core")

        elif (a > 0 and vx < 0) or (a < 0 and vx > 0):
            segments.append("entry")

        else:
            segments.append("exit")

    return np.array(segments)


# =========================
# MAIN
# =========================

def main():
    print("Running Field Projection V8.1 Flow Segmentation...")

    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    components = compute_field_basis(X)
    alpha, beta, gamma = project_field(X, components)

    D = compute_deviation(beta, gamma)
    D_smooth, threshold = detect_transitions(D)

    mask = D_smooth > threshold
    alpha_b = alpha[mask]
    beta_b = beta[mask]

    H, a_centers, b_centers = compute_density(alpha_b, beta_b)

    ridge_mask = extract_ridges(H)
    idx = np.where(ridge_mask)

    ridge_alpha = a_centers[idx[1]]
    ridge_beta = b_centers[idx[0]]

    d_alpha, d_beta = compute_velocity(alpha, beta)

    flow = estimate_flow(
        ridge_alpha, ridge_beta,
        alpha, beta,
        d_alpha, d_beta
    )

    segments = classify_segments(ridge_alpha, flow)

    # =========================
    # PLOT
    # =========================

    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111)

    im = ax.imshow(
        H,
        origin="lower",
        extent=[a_centers[0], a_centers[-1], b_centers[0], b_centers[-1]],
        aspect="auto"
    )

    colors = {
        "entry": "blue",
        "core": "yellow",
        "exit": "red"
    }

    for seg in ["entry", "core", "exit"]:
        mask_seg = segments == seg
        ax.scatter(
            ridge_alpha[mask_seg],
            ridge_beta[mask_seg],
            c=colors[seg],
            label=seg,
            s=20
        )

    ax.quiver(
        ridge_alpha, ridge_beta,
        flow[:, 0], flow[:, 1],
        color="white",
        scale=30,
        width=0.003
    )

    ax.legend()
    ax.set_title("V8.1 — Flow Segmentation (Entry / Core / Exit)")
    ax.set_xlabel("α")
    ax.set_ylabel("β")

    plt.colorbar(im)

    out = os.path.join(OUTPUT_DIR, "v8_1_flow_segmentation.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")
    print(f"Total ridge points: {len(ridge_alpha)}")


if __name__ == "__main__":
    main()
