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
# 5. PEAK TRANSITIONS
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
# 6. PRE-TRANSITIONS
# =========================

def detect_pre_transitions(D_smooth, threshold, k=1.0):
    dD = np.gradient(D_smooth)
    dD_threshold = np.mean(dD) + k * np.std(dD)

    pre_mask = (dD > dD_threshold) & (D_smooth < threshold)
    return dD, dD_threshold, pre_mask


# =========================
# 7. TRUE SWITCHES
# =========================

def detect_lobe_switches(alpha):
    sign_alpha = np.sign(alpha)
    switches = np.where(np.diff(sign_alpha) != 0)[0]

    directions = []
    for i in switches:
        if sign_alpha[i] < 0 and sign_alpha[i+1] > 0:
            directions.append(1)
        elif sign_alpha[i] > 0 and sign_alpha[i+1] < 0:
            directions.append(-1)
        else:
            directions.append(0)

    return switches, np.array(directions)


# =========================
# 8. COLLAPSE PRE REGIONS
# =========================

def collapse_pre_regions(pre_mask):
    idx = np.where(pre_mask)[0]
    if len(idx) == 0:
        return np.array([], dtype=int)

    anchors = [idx[0]]

    for i in range(1, len(idx)):
        if idx[i] != idx[i - 1] + 1:
            anchors.append(idx[i])

    return np.array(anchors, dtype=int)


# =========================
# 9. SELECT ONE PRE PER SWITCH (V5.1 CORE)
# =========================

def select_pre_for_each_switch(pre_events, switches):
    selected_pre = []
    lags = []

    for s in switches:
        candidates = pre_events[pre_events < s]

        if len(candidates) == 0:
            continue

        # entscheidend: letzter Pre vor Switch
        p = candidates[-1]

        selected_pre.append(p)
        lags.append(s - p)

    return np.array(selected_pre), np.array(lags)


# =========================
# 10. MAIN
# =========================

def main():
    print("Running Field Projection V5.1...")

    # --- Data ---
    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    components = compute_field_basis(X)
    alpha, beta, gamma = project_field(X, components)
    D = compute_deviation(beta, gamma)

    # --- V2 ---
    D_smooth, threshold, peaks = detect_transitions(D)

    # --- V3 ---
    dD, dD_thresh, pre_mask = detect_pre_transitions(D_smooth, threshold)
    pre_events = collapse_pre_regions(pre_mask)

    # --- V4 ---
    switches, directions = detect_lobe_switches(alpha)

    # --- V5.1 ---
    selected_pre, lags = select_pre_for_each_switch(pre_events, switches)

    t = np.arange(len(D))

    # =========================
    # PLOT 1: Mapping (1:1)
    # =========================
    plt.figure(figsize=(12, 5))
    plt.plot(t, D_smooth, label="D(t)")
    plt.axhline(threshold, linestyle="--", label="threshold")

    plt.scatter(selected_pre, D_smooth[selected_pre], s=40, label="selected pre")
    plt.scatter(switches, D_smooth[switches], s=40, label="switches")

    for p, s in zip(selected_pre, switches):
        plt.plot([p, s], [D_smooth[p], D_smooth[s]], linewidth=1)

    plt.legend()
    plt.title("1:1 Pre → Switch Mapping")

    out1 = os.path.join(OUTPUT_DIR, "v5_1_mapping.png")
    plt.savefig(out1, dpi=150)
    plt.close()

    # =========================
    # PLOT 2: Phase space
    # =========================
    plt.figure(figsize=(7, 7))
    plt.scatter(alpha, beta, c=D_smooth, s=2)

    plt.scatter(alpha[selected_pre], beta[selected_pre], s=40, label="decision points")
    plt.scatter(alpha[switches], beta[switches], s=40, label="switches")

    plt.legend()
    plt.title("Decision Points vs Switches")

    out2 = os.path.join(OUTPUT_DIR, "v5_1_phase.png")
    plt.savefig(out2, dpi=150)
    plt.close()

    # =========================
    # PLOT 3: Lag histogram
    # =========================
    plt.figure(figsize=(8, 4))
    if len(lags) > 0:
        plt.hist(lags, bins=15)

    plt.title("Decision Lead Time")
    plt.xlabel("steps before switch")
    plt.ylabel("count")

    out3 = os.path.join(OUTPUT_DIR, "v5_1_lag_hist.png")
    plt.savefig(out3, dpi=150)
    plt.close()

    # =========================
    # METRICS
    # =========================
    print(f"Saved: {out1}")
    print(f"Saved: {out2}")
    print(f"Saved: {out3}")
    print("")
    print(f"Switches: {len(switches)}")
    print(f"Decision points: {len(selected_pre)}")

    if len(lags) > 0:
        print(f"Mean decision lead time: {np.mean(lags):.2f}")
        print(f"Std: {np.std(lags):.2f}")
        print(f"Min: {np.min(lags)}")
        print(f"Max: {np.max(lags)}")


if __name__ == "__main__":
    main()
