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
# 6. PRE / SWITCHES
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
        if idx[i] != idx[i - 1] + 1:
            anchors.append(idx[i])
    return np.array(anchors, dtype=int)


def detect_lobe_switches(alpha):
    sign_alpha = np.sign(alpha)
    switches = np.where(np.diff(sign_alpha) != 0)[0]

    directions = []
    for i in switches:
        if sign_alpha[i] < 0 and sign_alpha[i + 1] > 0:
            directions.append(1)
        elif sign_alpha[i] > 0 and sign_alpha[i + 1] < 0:
            directions.append(-1)
        else:
            directions.append(0)

    return switches, np.array(directions)


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

    return np.array(selected_pre, dtype=int), mapping


def assign_direction(mapping, switches, directions):
    decision_dir = []

    for _, s in mapping:
        idx = np.where(switches == s)[0][0]
        decision_dir.append(directions[idx])

    return np.array(decision_dir, dtype=int)


# =========================
# 7. TIME TO NEXT SWITCH
# =========================

def compute_time_to_next_switch(n, switches):
    time_to_switch = np.full(n, np.nan)

    if len(switches) == 0:
        return time_to_switch

    switch_ptr = 0
    for i in range(n):
        while switch_ptr < len(switches) and switches[switch_ptr] < i:
            switch_ptr += 1

        if switch_ptr < len(switches):
            time_to_switch[i] = switches[switch_ptr] - i

    return time_to_switch


# =========================
# 8. MAIN
# =========================

def main():
    print("Running Field Projection V6.1 3D Colored...")

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

    # Boundary = instabile Schicht
    boundary_mask = D_smooth > threshold

    # Zeit bis nächster Switch
    time_to_switch = compute_time_to_next_switch(len(alpha), switches)

    # nur Boundary-Punkte mit definierter future time
    valid_mask = boundary_mask & np.isfinite(time_to_switch)

    a_b = alpha[valid_mask]
    b_b = beta[valid_mask]
    g_b = gamma[valid_mask]
    t_b = time_to_switch[valid_mask]

    # Decision Richtung
    left_mask = decision_dir == -1
    right_mask = decision_dir == 1

    # =========================
    # Q4 PANEL
    # =========================
    fig = plt.figure(figsize=(16, 12))

    # ---- PANEL 1: Standard 3D
    ax1 = fig.add_subplot(221, projection='3d')
    sc1 = ax1.scatter(a_b, b_b, g_b, c=t_b, s=5, alpha=0.35)
    ax1.scatter(
        alpha[selected_pre[left_mask]],
        beta[selected_pre[left_mask]],
        gamma[selected_pre[left_mask]],
        s=50,
        label="→ LEFT"
    )
    ax1.scatter(
        alpha[selected_pre[right_mask]],
        beta[selected_pre[right_mask]],
        gamma[selected_pre[right_mask]],
        s=50,
        label="→ RIGHT"
    )
    ax1.set_title("Q1 — 3D Boundary (time to switch)")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    ax1.set_zlabel("γ")
    ax1.legend()

    # ---- PANEL 2: Top View
    ax2 = fig.add_subplot(222, projection='3d')
    ax2.scatter(a_b, b_b, g_b, c=t_b, s=5, alpha=0.35)
    ax2.scatter(
        alpha[selected_pre[left_mask]],
        beta[selected_pre[left_mask]],
        gamma[selected_pre[left_mask]],
        s=50
    )
    ax2.scatter(
        alpha[selected_pre[right_mask]],
        beta[selected_pre[right_mask]],
        gamma[selected_pre[right_mask]],
        s=50
    )
    ax2.view_init(elev=90, azim=-90)
    ax2.set_title("Q2 — Top View")
    ax2.set_xlabel("α")
    ax2.set_ylabel("β")
    ax2.set_zlabel("γ")

    # ---- PANEL 3: Frog View
    ax3 = fig.add_subplot(223, projection='3d')
    ax3.scatter(a_b, b_b, g_b, c=t_b, s=5, alpha=0.35)
    ax3.scatter(
        alpha[selected_pre[left_mask]],
        beta[selected_pre[left_mask]],
        gamma[selected_pre[left_mask]],
        s=50
    )
    ax3.scatter(
        alpha[selected_pre[right_mask]],
        beta[selected_pre[right_mask]],
        gamma[selected_pre[right_mask]],
        s=50
    )
    ax3.view_init(elev=10, azim=35)
    ax3.set_title("Q3 — Frog View")
    ax3.set_xlabel("α")
    ax3.set_ylabel("β")
    ax3.set_zlabel("γ")

    # ---- PANEL 4: 2D α-β Projection
    ax4 = fig.add_subplot(224)
    sc4 = ax4.scatter(a_b, b_b, c=t_b, s=8, alpha=0.45)
    ax4.scatter(
        alpha[selected_pre[left_mask]],
        beta[selected_pre[left_mask]],
        s=70,
        label="→ LEFT"
    )
    ax4.scatter(
        alpha[selected_pre[right_mask]],
        beta[selected_pre[right_mask]],
        s=70,
        label="→ RIGHT"
    )
    ax4.set_title("Q4 — α-β Projection")
    ax4.set_xlabel("α")
    ax4.set_ylabel("β")
    ax4.legend()

    # gemeinsame colorbar
    cbar = fig.colorbar(sc4, ax=[ax1, ax2, ax3, ax4], shrink=0.75, pad=0.08)
    cbar.set_label("time to next switch (steps)")

    plt.suptitle("FIELD_LAYER V6.1 — Transition Boundary Perspectives", fontsize=18)

    out = os.path.join(OUTPUT_DIR, "v6_1_q4_boundary_views.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")
    print(f"Boundary points: {len(a_b)}")
    print(f"Decision points: {len(selected_pre)}")
    if len(t_b) > 0:
        print(f"Boundary lead-time range: {np.nanmin(t_b):.0f} .. {np.nanmax(t_b):.0f} steps")


if __name__ == "__main__":
    main()
