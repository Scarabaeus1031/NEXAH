import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# 1. GENERATE LORENZ DATA
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
# 2. PCA FIELD AXIS
# =========================

def compute_field_basis(X):
    pca = PCA(n_components=3)
    pca.fit(X)
    return pca.components_


# =========================
# 3. PROJECTION
# =========================

def project_field(X, components):
    e1, e2, e3 = components
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
# 5. TRANSITIONS (V2)
# =========================

def detect_transitions(D, k=1.2, min_distance=50, smooth_sigma=2):
    D_smooth = gaussian_filter1d(D, sigma=smooth_sigma)

    threshold = np.mean(D_smooth) + k * np.std(D_smooth)

    peaks, _ = find_peaks(
        D_smooth,
        height=threshold,
        distance=min_distance
    )

    mask = D_smooth > threshold

    return D_smooth, threshold, peaks, mask


# =========================
# 6. PRE-TRANSITIONS (V3)
# =========================

def detect_pre_transitions(D_smooth, threshold, k=1.0):
    dD = np.gradient(D_smooth)

    dD_threshold = np.mean(dD) + k * np.std(dD)

    # wichtig: vor dem Peak bleiben
    pre_mask = (dD > dD_threshold) & (D_smooth < threshold)

    return dD, dD_threshold, pre_mask


# =========================
# 7. SIGNAL
# =========================

def build_signal(D_smooth, threshold):
    signal = D_smooth / threshold
    signal[signal < 1] = 0
    return signal


# =========================
# 8. MAIN
# =========================

def main():
    print("Running Field Projection V3...")

    # --- Data ---
    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    components = compute_field_basis(X)

    alpha, beta, gamma = project_field(X, components)
    D = compute_deviation(beta, gamma)

    # --- V2 ---
    D_smooth, threshold, peaks, mask = detect_transitions(D)

    # --- V3 ---
    dD, dD_thresh, pre_mask = detect_pre_transitions(D_smooth, threshold)

    signal = build_signal(D_smooth, threshold)

    t = np.arange(len(D))

    # =========================
    # PLOT 1: Deviation + Pre + Peaks
    # =========================
    plt.figure(figsize=(10,4))
    plt.plot(t, D_smooth, label="D(t)")
    plt.axhline(threshold, linestyle="--", label="threshold")

    plt.scatter(t[pre_mask], D_smooth[pre_mask], s=10, label="pre")
    plt.scatter(t[peaks], D_smooth[peaks], s=25, label="peak")

    plt.legend()
    plt.title("Deviation with Pre-Transitions")

    out1 = os.path.join(OUTPUT_DIR, "v3_deviation_pre.png")
    plt.savefig(out1, dpi=150)
    plt.close()

    # =========================
    # PLOT 2: dD/dt
    # =========================
    plt.figure(figsize=(10,3))
    plt.plot(t, dD, label="dD/dt")
    plt.axhline(dD_thresh, linestyle="--", label="threshold")

    plt.legend()
    plt.title("Growth Rate dD/dt")

    out2 = os.path.join(OUTPUT_DIR, "v3_derivative.png")
    plt.savefig(out2, dpi=150)
    plt.close()

    # =========================
    # PLOT 3: Phase Space
    # =========================
    plt.figure(figsize=(6,6))
    plt.scatter(alpha, beta, c=D_smooth, s=2)

    # pre-events
    plt.scatter(alpha[pre_mask], beta[pre_mask], s=10)

    # peak-events
    plt.scatter(alpha[peaks], beta[peaks], s=25)

    plt.title("Phase Space: Pre vs Transition")

    out3 = os.path.join(OUTPUT_DIR, "v3_phase.png")
    plt.savefig(out3, dpi=150)
    plt.close()

    print(f"Saved: {out1}")
    print(f"Saved: {out2}")
    print(f"Saved: {out3}")

    print(f"Transitions: {len(peaks)}")
    print(f"Pre-transitions: {np.sum(pre_mask)}")


if __name__ == "__main__":
    main()
