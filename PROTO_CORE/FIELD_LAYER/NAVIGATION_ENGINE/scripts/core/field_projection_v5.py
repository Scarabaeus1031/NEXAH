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
# 5. PEAK TRANSITIONS (V2)
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
# 6. PRE-TRANSITIONS (V3)
# =========================

def detect_pre_transitions(D_smooth, threshold, k=1.0):
    dD = np.gradient(D_smooth)
    dD_threshold = np.mean(dD) + k * np.std(dD)

    pre_mask = (dD > dD_threshold) & (D_smooth < threshold)
    pre_indices = np.where(pre_mask)[0]

    return dD, dD_threshold, pre_mask, pre_indices


# =========================
# 7. TRUE SWITCHES (V4.1)
# =========================

def detect_lobe_switches(alpha):
    sign_alpha = np.sign(alpha)
    switches = np.where(np.diff(sign_alpha) != 0)[0]

    directions = []
    for i in switches:
        if sign_alpha[i] < 0 and sign_alpha[i + 1] > 0:
            directions.append(1)   # L -> R
        elif sign_alpha[i] > 0 and sign_alpha[i + 1] < 0:
            directions.append(-1)  # R -> L
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
# 9. MAP PRE -> NEXT SWITCH
# =========================

def map_pre_to_switch(pre_events, switches, max_horizon=300):
    matches = []
    unmatched = []

    for p in pre_events:
        future_switches = switches[switches > p]

        if len(future_switches) == 0:
            unmatched.append(p)
            continue

        s = future_switches[0]
        lag = s - p

        if lag <= max_horizon:
            matches.append((p, s, lag))
        else:
            unmatched.append(p)

    return matches, unmatched


# =========================
# 10. MAIN
# =========================

def main():
    print("Running Field Projection V5...")

    # --- Data ---
    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    components = compute_field_basis(X)
    alpha, beta, gamma = project_field(X, components)
    D = compute_deviation(beta, gamma)

    # --- V2 ---
    D_smooth, threshold, peaks = detect_transitions(D)

    # --- V3 ---
    dD, dD_thresh, pre_mask, pre_indices = detect_pre_transitions(D_smooth, threshold)

    # Collapse contiguous pre regions into event anchors
    pre_events = collapse_pre_regions(pre_mask)

    # --- V4.1 ---
    switches, directions = detect_lobe_switches(alpha)

    # --- V5 ---
    matches, unmatched = map_pre_to_switch(pre_events, switches, max_horizon=300)

    matched_pre = np.array([m[0] for m in matches], dtype=int) if matches else np.array([], dtype=int)
    matched_switch = np.array([m[1] for m in matches], dtype=int) if matches else np.array([], dtype=int)
    lags = np.array([m[2] for m in matches], dtype=float) if matches else np.array([], dtype=float)

    t = np.arange(len(D))

    # =========================
    # PLOT 1: D(t) with pre->switch mapping
    # =========================
    plt.figure(figsize=(12, 5))
    plt.plot(t, D_smooth, label="D(t)")
    plt.axhline(threshold, linestyle="--", label="threshold")

    if len(pre_events) > 0:
        plt.scatter(pre_events, D_smooth[pre_events], s=35, label="pre-events")
    if len(switches) > 0:
        plt.scatter(switches, D_smooth[switches], s=35, label="true switches")

    # draw mapping lines
    for p, s, _ in matches:
        plt.plot([p, s], [D_smooth[p], D_smooth[s]], linewidth=1, alpha=0.6)

    plt.legend()
    plt.title("Pre-Events mapped to True Switches")

    out1 = os.path.join(OUTPUT_DIR, "v5_pre_to_switch_mapping.png")
    plt.savefig(out1, dpi=150)
    plt.close()

    # =========================
    # PLOT 2: Phase space with matched pre-events
    # =========================
    plt.figure(figsize=(7, 7))
    plt.scatter(alpha, beta, c=D_smooth, s=2)

    if len(matched_pre) > 0:
        plt.scatter(alpha[matched_pre], beta[matched_pre], s=35, label="matched pre")
    if len(switches) > 0:
        plt.scatter(alpha[switches], beta[switches], s=35, label="switches")

    plt.legend()
    plt.title("Phase Space: Pre-Events and True Switches")

    out2 = os.path.join(OUTPUT_DIR, "v5_phase_prediction.png")
    plt.savefig(out2, dpi=150)
    plt.close()

    # =========================
    # PLOT 3: Lag histogram
    # =========================
    plt.figure(figsize=(8, 4))
    if len(lags) > 0:
        plt.hist(lags, bins=15)
    plt.title("Lead Time: Pre-Event -> Switch")
    plt.xlabel("lag (steps)")
    plt.ylabel("count")

    out3 = os.path.join(OUTPUT_DIR, "v5_lag_histogram.png")
    plt.savefig(out3, dpi=150)
    plt.close()

    # =========================
    # PLOT 4: Lag over event index
    # =========================
    plt.figure(figsize=(10, 3))
    if len(lags) > 0:
        plt.plot(lags, marker="o")
    plt.title("Lead Time per Prediction Event")
    plt.xlabel("matched event index")
    plt.ylabel("lag (steps)")

    out4 = os.path.join(OUTPUT_DIR, "v5_lag_series.png")
    plt.savefig(out4, dpi=150)
    plt.close()

    # =========================
    # METRICS
    # =========================
    n_pre_raw = len(pre_indices)
    n_pre_events = len(pre_events)
    n_switches = len(switches)
    n_matches = len(matches)
    n_unmatched = len(unmatched)

    prediction_rate = n_matches / n_pre_events if n_pre_events > 0 else 0.0
    switch_coverage = len(np.unique(matched_switch)) / n_switches if n_switches > 0 else 0.0
    mean_lag = np.mean(lags) if len(lags) > 0 else np.nan
    std_lag = np.std(lags) if len(lags) > 0 else np.nan

    print(f"Saved: {out1}")
    print(f"Saved: {out2}")
    print(f"Saved: {out3}")
    print(f"Saved: {out4}")
    print("")
    print(f"Raw pre-points: {n_pre_raw}")
    print(f"Collapsed pre-events: {n_pre_events}")
    print(f"True switches: {n_switches}")
    print(f"Matched pre-events: {n_matches}")
    print(f"Unmatched pre-events: {n_unmatched}")
    print(f"Prediction rate: {prediction_rate:.3f}")
    print(f"Switch coverage: {switch_coverage:.3f}")

    if len(lags) > 0:
        print(f"Mean lead time: {mean_lag:.2f} steps")
        print(f"Std lead time: {std_lag:.2f} steps")
        print(f"Min lead time: {np.min(lags):.0f} steps")
        print(f"Max lead time: {np.max(lags):.0f} steps")


if __name__ == "__main__":
    main()
