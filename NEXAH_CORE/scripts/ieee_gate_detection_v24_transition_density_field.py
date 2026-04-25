# ieee_gate_detection_v24_transition_density_field.py

import numpy as np
import matplotlib.pyplot as plt

runs = 50
T = 1000
window = 30
pad = 40

theta_all = []
r_all = []

for seed in range(runs):
    np.random.seed(seed)
    t = np.arange(T)

    # SIGNAL
    x1 = np.sin(0.2 * t[:600])
    x2 = np.sin(0.2 * t[600:]) + 0.8 * np.random.randn(400)
    x = np.concatenate([x1, x2])

    dx = np.gradient(x)

    theta = np.arctan2(dx, x)
    theta = np.unwrap(theta)
    r = np.sqrt(x**2 + dx**2)

    # SWITCHING
    switching = np.zeros(T)
    for i in range(window, T):
        seg = theta[i-window:i]
        jumps = np.abs(np.diff(seg)) > 1.0
        switching[i] = np.sum(jumps) / window

    switch_idx = np.argmax(switching > 0.45)

    # VARIANCE
    var = np.zeros(T)
    for i in range(window, T):
        var[i] = np.var(x[i-window:i])

    var_idx = np.argmax(var > np.percentile(var, 90))

    # TRANSITION WINDOW
    start = max(0, switch_idx - pad)
    end   = min(T, var_idx + pad)

    theta_all.extend(theta[start:end])
    r_all.extend(r[start:end])


theta_all = np.array(theta_all)
r_all = np.array(r_all)

# -----------------------------
# 2D HISTOGRAM (DENSITY FIELD)
# -----------------------------
bins_theta = 120
bins_r = 80

H, xedges, yedges = np.histogram2d(
    theta_all,
    r_all,
    bins=[bins_theta, bins_r]
)

H = H.T  # correct orientation

# -----------------------------
# PLOT
# -----------------------------
plt.figure(figsize=(8, 6))

plt.imshow(
    H,
    extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
    aspect='auto',
    origin='lower'
)

plt.colorbar(label="transition density")

plt.xlabel("θ (unwrapped)")
plt.ylabel("r")
plt.title("V24 — Transition Density Field")

plt.grid(False)

out_path = "NEXAH_CORE/outputs/ieee_gates/v24_transition_density.png"
plt.savefig(out_path, dpi=150)
plt.show()

print("\n--- V24 ---")
print(f"Runs: {runs}")
print("Saved to:", out_path)
