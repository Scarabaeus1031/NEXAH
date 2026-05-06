# ieee_gate_detection_v23_transition_path_overlay.py

import numpy as np
import matplotlib.pyplot as plt

runs = 20
T = 1000
window = 30
pad = 60

all_paths_theta = []
all_paths_r = []

true_transition = 600

for seed in range(runs):
    np.random.seed(seed)
    t = np.arange(T)

    # SIGNAL
    x1 = np.sin(0.2 * t[:600])
    x2 = np.sin(0.2 * t[600:]) + 0.8 * np.random.randn(400)
    x = np.concatenate([x1, x2])

    dx = np.gradient(x)

    theta = np.arctan2(dx, x)
    theta = np.unwrap(theta)   # 🔥 FIX

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

    # PATH WINDOW
    start = max(0, switch_idx - pad)
    end   = min(T, var_idx + pad)

    all_paths_theta.append(theta[start:end])
    all_paths_r.append(r[start:end])


# -----------------------------
# PLOT
# -----------------------------
plt.figure(figsize=(8, 6))

# background (single run for context)
plt.scatter(theta, r, s=5, alpha=0.05, color='gray')

# overlay paths
for th, rr in zip(all_paths_theta, all_paths_r):
    plt.plot(th, rr, alpha=0.4)

plt.xlabel("θ (unwrapped)")
plt.ylabel("r")
plt.title("V23 — Transition Path Overlay (Multi-Run)")

plt.grid(True)

out_path = "NEXAH_CORE/outputs/ieee_gates/v23_transition_overlay.png"
plt.savefig(out_path, dpi=150)
plt.show()

print("\n--- V23 ---")
print(f"Runs: {runs}")
print("Saved to:", out_path)
