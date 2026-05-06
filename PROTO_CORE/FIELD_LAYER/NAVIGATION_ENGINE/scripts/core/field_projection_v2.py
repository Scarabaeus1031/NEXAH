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

    components = pca.components_

    e1 = components[0]
    e2 = components[1]
    e3 = components[2]

    return e1, e2, e3


# =========================
# 3. PROJECTION
# =========================

def project_field(X, e1, e2, e3):
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
# 5. TRANSITION DETECTION
# =========================

def detect_transitions(D, k=1.2, min_distance=50, smooth_sigma=2):
    # Smooth
    D_smooth = gaussian_filter1d(D, sigma=smooth_sigma)

    # Adaptive threshold
    threshold = np.mean(D_smooth) + k * np.std(D_smooth)

    # Peaks
    peaks, properties = find_peaks(
        D_smooth,
        height=threshold,
        distance=min_distance
    )

    # Mask (continuous transitions)
    transition_mask = D_smooth > threshold

    return D_smooth, threshold, peaks, transition_mask


# =========================
# 6. SIGNAL
# =========================

def build_signal(D_smooth, threshold):
    signal = D_smooth / threshold
    signal[signal < 1] = 0
    return signal


# =========================
# 7. MAIN
# =========================

def main():
    print("Running Field Projection V2...")

    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    e1, e2, e3 = compute_field_basis(X)

    alpha, beta, gamma = project_field(X, e1, e2, e3)
    D = compute_deviation(beta, gamma)

    # =========================
    # TRANSITIONS
    # =========================
    D_smooth, threshold, peaks, mask = detect_transitions(D)
    signal = build_signal(D_smooth, threshold)

    t = np.arange(len(D))

    # =========================
    # PLOT 1: α vs β (colored)
    # =========================
    plt.figure(figsize=(6,6))
    plt.scatter(alpha, beta, c=D_smooth, s=2)
    plt.scatter(alpha[peaks], beta[peaks], s=20)
    plt.title("Field Projection (α vs β) with Transitions")

    out1 = os.path.join(OUTPUT_DIR, "v2_alpha_beta_transitions.png")
    plt.savefig(out1, dpi=150)
    plt.close()

    # =========================
    # PLOT 2: D(t) + Threshold + Peaks
    # =========================
    plt.figure(figsize=(10,4))
    plt.plot(t, D_smooth)
    plt.axhline(threshold, linestyle="--")

    plt.scatter(t[peaks], D_smooth[peaks])

    plt.title("Deviation with Transition Detection")

    out2 = os.path.join(OUTPUT_DIR, "v2_deviation_transitions.png")
    plt.savefig(out2, dpi=150)
    plt.close()

    # =========================
    # PLOT 3: Signal
    # =========================
    plt.figure(figsize=(10,3))
    plt.plot(t, signal)
    plt.title("Transition Signal")

    out3 = os.path.join(OUTPUT_DIR, "v2_signal.png")
    plt.savefig(out3, dpi=150)
    plt.close()

    print(f"Saved: {out1}")
    print(f"Saved: {out2}")
    print(f"Saved: {out3}")

    print(f"Detected transitions: {len(peaks)}")


if __name__ == "__main__":
    main()
