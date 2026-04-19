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

    return D_smooth, threshold, peaks


# =========================
# 6. LOBE SWITCH DETECTION (V4.1 CORE)
# =========================

def detect_lobe_switches(alpha):
    sign_alpha = np.sign(alpha)

    switches = np.where(np.diff(sign_alpha) != 0)[0]

    directions = []

    for i in switches:
        if sign_alpha[i] < 0 and sign_alpha[i+1] > 0:
            directions.append(1)   # L → R
        elif sign_alpha[i] > 0 and sign_alpha[i+1] < 0:
            directions.append(-1)  # R → L
        else:
            directions.append(0)

    return switches, np.array(directions)


# =========================
# 7. MAIN
# =========================

def main():
    print("Running Field Projection V4.1...")

    # --- Data ---
    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    components = compute_field_basis(X)
    alpha, beta, gamma = project_field(X, components)

    D = compute_deviation(beta, gamma)

    # --- Peaks (Instability) ---
    D_smooth, threshold, peaks = detect_transitions(D)

    # --- True State Transitions ---
    switches, directions = detect_lobe_switches(alpha)

    t = np.arange(len(D))

    # Masks
    lr_mask = directions == 1
    rl_mask = directions == -1

    switches_lr = switches[lr_mask]
    switches_rl = switches[rl_mask]

    # =========================
    # PLOT 1: Phase Space (TRUE direction)
    # =========================
    plt.figure(figsize=(7, 7))
    plt.scatter(alpha, beta, c=D_smooth, s=2)

    plt.scatter(alpha[switches_lr], beta[switches_lr], s=40, label="L→R")
    plt.scatter(alpha[switches_rl], beta[switches_rl], s=40, label="R→L")

    plt.legend()
    plt.title("Phase Space: TRUE Lobe Transitions")

    out1 = os.path.join(OUTPUT_DIR, "v4_1_phase_switches.png")
    plt.savefig(out1, dpi=150)
    plt.close()

    # =========================
    # PLOT 2: Time Alignment (Peaks vs Switches)
    # =========================
    plt.figure(figsize=(10, 4))
    plt.plot(t, D_smooth, label="D(t)")
    plt.axhline(threshold, linestyle="--", label="threshold")

    plt.scatter(peaks, D_smooth[peaks], s=30, label="peaks (instability)")
    plt.scatter(switches, D_smooth[switches], s=30, label="switches (state)")

    plt.legend()
    plt.title("Peaks vs True Transitions")

    out2 = os.path.join(OUTPUT_DIR, "v4_1_peaks_vs_switches.png")
    plt.savefig(out2, dpi=150)
    plt.close()

    # =========================
    # PLOT 3: Direction Signal
    # =========================
    direction_series = np.zeros(len(alpha))

    for i, d in zip(switches, directions):
        direction_series[i] = d

    plt.figure(figsize=(10, 3))
    plt.plot(t, direction_series)
    plt.title("True Transition Direction Signal")

    out3 = os.path.join(OUTPUT_DIR, "v4_1_direction_signal.png")
    plt.savefig(out3, dpi=150)
    plt.close()

    # =========================
    # SUMMARY
    # =========================
    print(f"Saved: {out1}")
    print(f"Saved: {out2}")
    print(f"Saved: {out3}")

    print(f"Peaks (instability): {len(peaks)}")
    print(f"Switches (true transitions): {len(switches)}")
    print(f"L->R: {np.sum(directions == 1)}")
    print(f"R->L: {np.sum(directions == -1)}")


if __name__ == "__main__":
    main()
