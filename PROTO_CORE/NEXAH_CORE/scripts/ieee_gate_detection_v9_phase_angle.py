# NEXAH_CORE/scripts/ieee_gate_detection_v9_phase_angle.py
#
# v9: Phase-angle gate mapping
#
# Question:
# Do transition gates occur randomly,
# or do they concentrate at specific phase angles?
#
# Core idea:
# v8 showed WHERE gates live in phase space.
# v9 maps those gate points onto the phase angle:
#
#     theta(t) = atan2(dx/dt, x)
#
# Then we build:
# - Histogram of all phases
# - Histogram of gate phases
# - Density ratio (gate probability vs angle)

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from scipy.stats import entropy

np.random.seed(42)

OUTPUT_PATH = "NEXAH_CORE/outputs/ieee_gates/ieee_gate_detection_v9_phase_angle.png"


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

    return mask, C_thr, S_thr, G_thr


# --------------------------------------------------
# 6. PHASE ANGLE
# --------------------------------------------------
def compute_phase_angle(x, dx):
    theta = np.arctan2(dx, x)
    return theta


# --------------------------------------------------
# 7. MAIN
# --------------------------------------------------
t = np.linspace(0, 100, 1000)

x = generate_signal(t)
C = compute_coherence(x)
S = compute_entropy(x)
dx, G = compute_geometry(t, x)

mask, C_thr, S_thr, G_thr = compute_gate_mask(C, S, G)

theta = compute_phase_angle(x, dx)

# Filter valid indices
valid = (~np.isnan(theta)) & (np.abs(x) + np.abs(dx) > 1e-8)

theta_all = theta[valid]
theta_gates = theta[valid & mask]

# --------------------------------------------------
# 8. HISTOGRAMS
# --------------------------------------------------
bins = 60

hist_all, edges = np.histogram(theta_all, bins=bins, range=(-np.pi, np.pi), density=True)
hist_gates, _ = np.histogram(theta_gates, bins=bins, range=(-np.pi, np.pi), density=True)

centers = 0.5 * (edges[:-1] + edges[1:])

# Avoid division by zero
ratio = hist_gates / (hist_all + 1e-8)

# --------------------------------------------------
# 9. VISUALIZATION
# --------------------------------------------------
fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

# All phase distribution
axs[0].plot(centers, hist_all)
axs[0].set_title("Phase Distribution (All States)")
axs[0].set_ylabel("Density")

# Gate phase distribution
axs[1].plot(centers, hist_gates, color="orange")
axs[1].set_title("Gate Phase Distribution")
axs[1].set_ylabel("Density")

# Ratio (important!)
axs[2].plot(centers, ratio, color="red")
axs[2].set_title("Gate Probability vs Phase Angle")
axs[2].set_xlabel("Phase θ")
axs[2].set_ylabel("Relative Density")

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=150)


# --------------------------------------------------
# 10. POLAR VIEW (BONUS)
# --------------------------------------------------
fig2 = plt.figure(figsize=(6, 6))
ax2 = fig2.add_subplot(111, projection='polar')

ax2.plot(centers, ratio)
ax2.set_title("Gate Probability (Polar View)")

plt.tight_layout()


# --------------------------------------------------
# 11. LOGGING
# --------------------------------------------------
print("\n--- NEXAH IEEE Gate Detection v9 ---")
print(f"Coherence threshold: {C_thr:.3f}")
print(f"Entropy threshold:   {S_thr:.3f}")
print(f"Geometry threshold:  {G_thr:.3f}")
print(f"Total samples: {len(theta_all)}")
print(f"Gate samples:  {len(theta_gates)}")

print(f"\nSaved to: {OUTPUT_PATH}")

plt.show()
