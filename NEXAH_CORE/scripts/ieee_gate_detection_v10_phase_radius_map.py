# BUILDER_LAB/ZETA_EXPERIMENTS/scripts/ieee_gate_detection_v10_phase_radius_map.py
#
# v10: Phase + Radius Gate Map
#
# Goal:
# Build a 2D stability field:
#
#   P(gate | r, θ)
#
# This reveals where in phase space transitions occur.

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from scipy.stats import entropy

np.random.seed(42)

OUTPUT_PATH = "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/ieee_gate_detection_v10_phase_radius.png"


# --------------------------------------------------
# 1. SIGNAL
# --------------------------------------------------
def generate_signal(t):
    x = np.zeros_like(t)

    for i, ti in enumerate(t):
        if ti < 30:
            x[i] = 0.3 * np.sin(0.5 * ti)

        elif ti < 75:
            x[i] = (1 + 0.02 * ti) * np.sin(1.5 * ti)

        else:
            x[i] = np.random.normal(0, 1.0)

    return x


# --------------------------------------------------
# 2. COHERENCE
# --------------------------------------------------
def compute_coherence(x, window=20, max_lag=5):
    C = np.zeros(len(x))

    for i in range(window, len(x)):
        seg = x[i - window:i]
        vals = []

        for lag in range(1, max_lag + 1):
            a = seg[:-lag]
            b = seg[lag:]

            if np.std(a) > 1e-12 and np.std(b) > 1e-12:
                vals.append(abs(np.corrcoef(a, b)[0, 1]))

        C[i] = np.mean(vals) if vals else 0.0

    return C


# --------------------------------------------------
# 3. ENTROPY
# --------------------------------------------------
def compute_entropy(x, window=40):
    S = np.zeros(len(x))

    for i in range(window, len(x)):
        seg = x[i - window:i]
        _, pxx = welch(seg, nperseg=len(seg))

        pxx = pxx + 1e-12
        pxx = pxx / np.sum(pxx)

        S[i] = entropy(pxx)

    return S


# --------------------------------------------------
# 4. GEOMETRY
# --------------------------------------------------
def compute_geometry(t, x, window=30):
    dx = np.gradient(x, t)
    G = np.zeros(len(x))

    for i in range(window, len(x)):
        X = np.column_stack((x[i - window:i], dx[i - window:i]))
        cov = np.cov(X.T)

        eigvals = np.maximum(np.linalg.eigvalsh(cov), 1e-12)
        G[i] = np.sqrt(np.prod(eigvals))

    return dx, G


# --------------------------------------------------
# 5. GATE MASK
# --------------------------------------------------
def compute_gate_mask(C, S, G):
    C_thr = np.percentile(C[C > 0], 15)
    S_thr = np.percentile(S[S > 0], 80)
    G_thr = np.percentile(G[G > 0], 80)

    mask = (C < C_thr) & (S > S_thr) & (G > G_thr)

    return mask


# --------------------------------------------------
# 6. PHASE + RADIUS
# --------------------------------------------------
def compute_phase_radius(x, dx):
    theta = np.arctan2(dx, x)
    r = np.sqrt(x**2 + dx**2)
    return theta, r


# --------------------------------------------------
# 7. MAIN
# --------------------------------------------------
t = np.linspace(0, 100, 1000)

x = generate_signal(t)
C = compute_coherence(x)
S = compute_entropy(x)
dx, G = compute_geometry(t, x)

mask = compute_gate_mask(C, S, G)

theta, r = compute_phase_radius(x, dx)

valid = (~np.isnan(theta)) & (~np.isnan(r))

theta_all = theta[valid]
r_all = r[valid]

theta_g = theta[valid & mask]
r_g = r[valid & mask]


# --------------------------------------------------
# 8. 2D HISTOGRAM
# --------------------------------------------------
bins_theta = 60
bins_r = 40

theta_range = [-np.pi, np.pi]
r_range = [0, np.max(r_all)]

H_all, theta_edges, r_edges = np.histogram2d(
    theta_all, r_all,
    bins=[bins_theta, bins_r],
    range=[theta_range, r_range],
    density=True
)

H_gates, _, _ = np.histogram2d(
    theta_g, r_g,
    bins=[bins_theta, bins_r],
    range=[theta_range, r_range],
    density=True
)

# Gate probability
ratio = H_gates / (H_all + 1e-8)


# --------------------------------------------------
# 9. VISUALIZATION
# --------------------------------------------------
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# State density
im0 = axs[0].imshow(
    H_all.T,
    origin="lower",
    aspect="auto",
    extent=[theta_range[0], theta_range[1], r_range[0], r_range[1]]
)
axs[0].set_title("State Density f(r, θ)")
axs[0].set_xlabel("θ")
axs[0].set_ylabel("r")
plt.colorbar(im0, ax=axs[0])

# Gate density
im1 = axs[1].imshow(
    H_gates.T,
    origin="lower",
    aspect="auto",
    extent=[theta_range[0], theta_range[1], r_range[0], r_range[1]]
)
axs[1].set_title("Gate Density")
axs[1].set_xlabel("θ")
plt.colorbar(im1, ax=axs[1])

# Gate probability field
im2 = axs[2].imshow(
    ratio.T,
    origin="lower",
    aspect="auto",
    extent=[theta_range[0], theta_range[1], r_range[0], r_range[1]]
)
axs[2].set_title("Gate Probability f(r, θ)")
axs[2].set_xlabel("θ")
plt.colorbar(im2, ax=axs[2])

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=150)


# --------------------------------------------------
# 10. LOG
# --------------------------------------------------
print("\n--- NEXAH IEEE Gate Detection v10 ---")
print(f"Total samples: {len(theta_all)}")
print(f"Gate samples:  {len(theta_g)}")
print(f"Saved to: {OUTPUT_PATH}")

plt.show()
