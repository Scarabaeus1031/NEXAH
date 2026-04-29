import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

# ============================================================
# SCENARIO
# ============================================================

def make_synthetic_scenario(kind="nonlinear", n=500):
    t = np.linspace(0, 100, n)
    V = 1.0 - 0.002 * t - 0.0005 * t**2

    if kind == "nonlinear":
        V += 0.015 * np.exp((t - 16) / 4.0) * (t < 25)
        V += 0.01 * np.sin(0.8 * t) * (t < 25)

    elif kind == "noisy":
        rng = np.random.default_rng(7)
        V += 0.01 * rng.normal(size=len(t))

    return t, V


# ============================================================
# CORE SIGNALS
# ============================================================

def compute_base_features(t, V):
    V_s = gaussian_filter1d(V, 2)
    dv = gaussian_filter1d(np.gradient(V_s, t), 2)
    ddv = gaussian_filter1d(np.gradient(dv, t), 2)
    return V_s, dv, ddv


# ============================================================
# EMBEDDINGS
# ============================================================

def embedding_standard(V, dv, ddv):
    return np.vstack([V, dv, ddv]).T


def embedding_koopman(V, dv, ddv):
    return np.vstack([
        V,
        dv,
        ddv,
        V**2,
        dv**2,
        V * dv
    ]).T


# ============================================================
# CURVATURE
# ============================================================

def compute_curvature(x):
    return gaussian_filter1d(
        np.linalg.norm(np.gradient(np.gradient(x, axis=0), axis=0), axis=1),
        2
    )


# ============================================================
# SHAPE EXTRACTION
# ============================================================

def extract_window_shapes(signal, window=30, step=2):
    shapes = []
    centers = []

    for i in range(0, len(signal) - window, step):
        seg = signal[i:i+window]

        seg_norm = seg / (np.max(seg) + 1e-8)
        shapes.append(seg_norm)
        centers.append(i + window//2)

    return np.array(shapes), np.array(centers)


# ============================================================
# PCA
# ============================================================

def compute_pca(X):
    X_mean = np.mean(X, axis=0)
    Xc = X - X_mean
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    coords = Xc @ Vt[:2].T
    return coords


# ============================================================
# SHAPE DRIFT
# ============================================================

def compute_shape_drift(coords):
    stable_idx = int(0.3 * len(coords))
    ref = np.mean(coords[:stable_idx], axis=0)
    dist = np.linalg.norm(coords - ref, axis=1)
    dist_n = dist / (np.max(dist) + 1e-8)
    return dist_n, stable_idx


# ============================================================
# DETECTION
# ============================================================

def sustained(mask, t, k=3):
    for i in range(len(mask)-k):
        if np.all(mask[i:i+k]):
            return t[i]
    return None


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("\n=== RUN 015 — KOOPMAN EMBEDDING PROBE ===\n")

    t, V = make_synthetic_scenario("nonlinear")

    V_s, dv, ddv = compute_base_features(t, V)

    # collapse
    t_collapse = t[np.argmax(V_s < 0.7)]

    # ============================================================
    # STANDARD PIPELINE
    # ============================================================

    x_std = embedding_standard(V_s, dv, ddv)
    k_std = compute_curvature(x_std)

    shapes_std, centers = extract_window_shapes(k_std)
    coords_std = compute_pca(shapes_std)
    drift_std, stable_idx = compute_shape_drift(coords_std)

    thresh_std = np.mean(drift_std[:stable_idx]) + 2*np.std(drift_std[:stable_idx])
    t_std = sustained(drift_std > thresh_std, centers)

    lead_std = t_collapse - t_std if t_std else None

    # ============================================================
    # KOOPMAN PIPELINE
    # ============================================================

    x_k = embedding_koopman(V_s, dv, ddv)
    k_k = compute_curvature(x_k)

    shapes_k, centers_k = extract_window_shapes(k_k)
    coords_k = compute_pca(shapes_k)
    drift_k, stable_idx_k = compute_shape_drift(coords_k)

    thresh_k = np.mean(drift_k[:stable_idx_k]) + 2*np.std(drift_k[:stable_idx_k])
    t_k = sustained(drift_k > thresh_k, centers_k)

    lead_k = t_collapse - t_k if t_k else None

    # ============================================================
    # RESULTS
    # ============================================================

    print("STANDARD lead:", lead_std)
    print("KOOPMAN  lead:", lead_k)

    # ============================================================
    # PLOT
    # ============================================================

    plt.figure(figsize=(10,5))

    plt.plot(centers, drift_std, label="Shape Drift (standard)", linewidth=2)
    plt.plot(centers_k, drift_k, label="Shape Drift (koopman)", linewidth=2)

    if t_std:
        plt.axvline(t_std, linestyle="--", label="standard detect")

    if t_k:
        plt.axvline(t_k, linestyle=":", label="koopman detect")

    plt.axvline(t_collapse, color="black", label="collapse")

    plt.title("Shape Drift — Standard vs Koopman Embedding")
    plt.xlabel("Time")
    plt.ylabel("Normalized drift")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
