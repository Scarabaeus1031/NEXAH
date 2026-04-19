import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d

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
# 5. TRANSITIONS
# =========================

def detect_transitions(D, k=1.2, min_distance=50, smooth_sigma=2):
    D_smooth = gaussian_filter1d(D, sigma=smooth_sigma)
    threshold = np.mean(D_smooth) + k * np.std(D_smooth)

    peaks, _ = find_peaks(D_smooth, height=threshold, distance=min_distance)

    return D_smooth, threshold, peaks


# =========================
# 6. PRE
# =========================

def detect_pre_transitions(D_smooth, threshold, k=1.0):
    dD = np.gradient(D_smooth)
    dD_threshold = np.mean(dD) + k * np.std(dD)

    pre_mask = (dD > dD_threshold) & (D_smooth < threshold)
    return pre_mask


def collapse_pre_regions(pre_mask):
    idx = np.where(pre_mask)[0]
    if len(idx) == 0:
        return np.array([], dtype=int)

    anchors = [idx[0]]
    for i in range(1, len(idx)):
        if idx[i] != idx[i-1] + 1:
            anchors.append(idx[i])

    return np.array(anchors)


# =========================
# 7. SWITCHES
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
# 8. MATCH PRE → SWITCH
# =========================

def select_pre_for_each_switch(pre_events, switches):
    selected_pre = []
    mapping = []

    for s in switches:
        candidates = pre_events[pre_events < s]
        if len(candidates) == 0:
            continue

        p = candidates[-1]

        selected_pre.append(p)
        mapping.append((p, s))

    return np.array(selected_pre), mapping


# =========================
# 9. ASSIGN DIRECTION TO DECISION
# =========================

def assign_direction(mapping, switches, directions):
    decision_dir = []

    for (p, s) in mapping:
        idx = np.where(switches == s)[0][0]
        decision_dir.append(directions[idx])

    return np.array(decision_dir)


# =========================
# 10. MAIN
# =========================

def main():
    print("Running Field Projection V6...")

    X = generate_lorenz()
    X = X - np.mean(X, axis=0)

    components = compute_field_basis(X)
    alpha, beta, gamma = project_field(X, components)

    D = compute_deviation(beta, gamma)

    D_smooth, threshold, peaks = detect_transitions(D)

    pre_mask = detect_pre_transitions(D_smooth, threshold)
    pre_events = collapse_pre_regions(pre_mask)

    switches, directions = detect_lobe_switches(alpha)

    selected_pre, mapping = select_pre_for_each_switch(pre_events, switches)

    decision_dir = assign_direction(mapping, switches, directions)

    # masks
    left = decision_dir == -1
    right = decision_dir == 1

    # =========================
    # PLOT: PHASE DECISIONS
    # =========================
    plt.figure(figsize=(7,7))
    plt.scatter(alpha, beta, c=D_smooth, s=2)

    plt.scatter(alpha[selected_pre[left]], beta[selected_pre[left]], s=40, label="→ LEFT")
    plt.scatter(alpha[selected_pre[right]], beta[selected_pre[right]], s=40, label="→ RIGHT")

    plt.legend()
    plt.title("Decision Points with Direction")

    out = os.path.join(OUTPUT_DIR, "v6_decision_direction.png")
    plt.savefig(out, dpi=150)
    plt.close()

    print(f"Saved: {out}")
    print(f"Decisions: {len(selected_pre)}")
    print(f"Left: {np.sum(left)} | Right: {np.sum(right)}")


if __name__ == "__main__":
    main()
