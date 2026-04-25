# ieee_gate_detection_v22_transition_path.py

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# SIGNAL (same as v20/v21)
# -----------------------------
np.random.seed(0)

T = 1000
t = np.arange(T)

# pre-transition: clean oscillation
x1 = np.sin(0.2 * t[:600])

# post-transition: noisy regime
x2 = np.sin(0.2 * t[600:]) + 0.8 * np.random.randn(400)

x = np.concatenate([x1, x2])

true_transition = 600


# -----------------------------
# PHASE SPACE
# -----------------------------
dx = np.gradient(x)

theta = np.arctan2(dx, x)
r = np.sqrt(x**2 + dx**2)


# -----------------------------
# SWITCHING DENSITY (same idea)
# -----------------------------
window = 30
switching = np.zeros(T)

for i in range(window, T):
    segment = theta[i-window:i]
    jumps = np.abs(np.diff(segment)) > 1.0
    switching[i] = np.sum(jumps) / window

# detect switching event
switch_threshold = 0.45
switch_idx = np.argmax(switching > switch_threshold)


# -----------------------------
# VARIANCE DETECTION
# -----------------------------
var = np.zeros(T)

for i in range(window, T):
    var[i] = np.var(x[i-window:i])

var_threshold = np.percentile(var, 90)
var_idx = np.argmax(var > var_threshold)


# -----------------------------
# TRANSITION PATH WINDOW
# -----------------------------
pad = 80

start = max(0, switch_idx - pad)
end   = min(T, var_idx + pad)


# -----------------------------
# PLOT
# -----------------------------
plt.figure(figsize=(8, 6))

# full trajectory (faint)
plt.scatter(theta, r, s=5, alpha=0.1, color='gray')

# transition path (highlighted)
plt.plot(theta[start:end], r[start:end],
         color='blue', linewidth=2, label='transition path')

# markers
plt.scatter(theta[true_transition], r[true_transition],
            color='black', s=80, label='true')

plt.scatter(theta[switch_idx], r[switch_idx],
            color='blue', s=80, label='switch')

plt.scatter(theta[var_idx], r[var_idx],
            color='orange', s=80, label='variance')

# arrows (direction)
for i in range(start, end-1, 5):
    plt.arrow(theta[i], r[i],
              theta[i+1] - theta[i],
              r[i+1] - r[i],
              head_width=0.03,
              alpha=0.5,
              color='blue')

plt.xlabel("θ (phase)")
plt.ylabel("r (radius)")
plt.title("V22 — Transition Path in Phase Space")

plt.legend()
plt.grid(True)

# save
out_path = "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/v22_transition_path.png"
plt.savefig(out_path, dpi=150)
plt.show()

print("\n--- V22 ---")
print("True t:", true_transition)
print("Switch t:", switch_idx)
print("Variance t:", var_idx)
print("Saved to:", out_path)
