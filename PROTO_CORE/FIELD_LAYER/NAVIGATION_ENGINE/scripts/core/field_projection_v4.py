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
# 8. DIRECTION CLASSIFICATION (V4)
# =========================

def classify_transitions(alpha, peaks, window=10):
    directions = []

    for p in peaks:
        left_idx = max(0, p - window)
        right_idx = min(len(alpha) - 1, p + window)

        before = np.mean(alpha[left_idx:p]) if p > left_idx else alpha[p]
        after = np.mean(alpha[p:right_idx]) if right_idx > p else alpha[p]

        if before < 0 and after > 0:
            directions.append(1)   # LEFT -> RIGHT
        elif before > 0 and after < 0:
            directions.append(-1)  # RIGHT -> LEFT
        else:
            directions.append(0)   # unclear / same side

    return np.array(directions)


def build_direction_series(n, peaks, directions):
    series = np.zeros(n)

    for p, d in zip(peaks, directions):
        series[p] = d

    return series


# =========================
# 9. MAIN
# =========================

def main():
    print("Running Field Projection V4...")

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

    # --- V4 ---
    directions = classify_transitions(alpha, peaks, window=10)
    direction_series = build_direction_series(len(alpha), peaks, directions)

    signal = build_signal(D_smooth, threshold)
    t = np.arange(len(D))

    lr_mask = directions == 1
    rl_mask = directions == -1
    un_mask = directions == 0

    peaks_lr = peaks[lr_mask]
    peaks_rl = peaks[rl_mask]
    peaks_un = peaks[un_mask]

    # =========================
    # PLOT 1: Deviation + Pre + Directed Peaks
    # =========================
    plt.figure(figsize=(10, 4))
    plt.plot(t, D_smooth, label="D(t)")
    plt.axhline(threshold, linestyle="--", label="threshold")

    plt.scatter(t[pre_mask], D_smooth[pre_mask], s=10, label="pre")
    plt.scatter(t[peaks_lr], D_smooth[peaks_lr], s=30, label="L→R")
    plt.scatter(t[peaks_rl], D_smooth[peaks_rl], s=30, label="R→L")

    if len(peaks_un) > 0:
        plt.scatter(t[peaks_un], D_smooth[peaks_un], s=30, label="unclear")

    plt.legend()
    plt.title("Deviation with Directed Transitions")

    out1 = os.path.join(OUTPUT_DIR, "v4_deviation_direction.png")
    plt.savefig(out1, dpi=150)
    plt.close()

    # =========================
    # PLOT 2: dD/dt
    # =========================
    plt.figure(figsize=(10, 3))
    plt.plot(t, dD, label="dD/dt")
    plt.axhline(dD_thresh, linestyle="--", label="threshold")
    plt.legend()
    plt.title("Growth Rate dD/dt")

    out2 = os.path.join(OUTPUT_DIR, "v4_derivative.png")
    plt.savefig(out2, dpi=150)
    plt.close()

    # =========================
    # PLOT 3: Phase Space with Directions
    # =========================
    plt.figure(figsize=(7, 7))
    plt.scatter(alpha, beta, c=D_smooth, s=2)

    # pre-events
    plt.scatter(alpha[pre_mask], beta[pre_mask], s=8, label="pre")

    # directed peaks
    plt.scatter(alpha[peaks_lr], beta[peaks_lr], s=40, label="L→R")
    plt.scatter(alpha[peaks_rl], beta[peaks_rl], s=40, label="R→L")

    if len(peaks_un) > 0:
        plt.scatter(alpha[peaks_un], beta[peaks_un], s=40, label="unclear")

    plt.legend()
    plt.title("Phase Space: Directed Transitions")

    out3 = os.path.join(OUTPUT_DIR, "v4_phase_direction.png")
    plt.savefig(out3, dpi=150)
    plt.close()

    # =========================
    # PLOT 4: Direction Series over Time
    # =========================
    plt.figure(figsize=(10, 3))
    plt.plot(t, direction_series, linewidth=1)
    plt.title("Transition Direction Signal")
    plt.xlabel("time")
    plt.ylabel("direction")

    out4 = os.path.join(OUTPUT_DIR, "v4_direction_signal.png")
    plt.savefig(out4, dpi=150)
    plt.close()

    # =========================
    # TEXT SUMMARY
    # =========================
    n_lr = np.sum(directions == 1)
    n_rl = np.sum(directions == -1)
    n_un = np.sum(directions == 0)

    print(f"Saved: {out1}")
    print(f"Saved: {out2}")
    print(f"Saved: {out3}")
    print(f"Saved: {out4}")
    print(f"Transitions total: {len(peaks)}")
    print(f"Pre-transitions: {np.sum(pre_mask)}")
    print(f"L->R transitions: {n_lr}")
    print(f"R->L transitions: {n_rl}")
    print(f"Unclear transitions: {n_un}")


if __name__ == "__main__":
    main()
