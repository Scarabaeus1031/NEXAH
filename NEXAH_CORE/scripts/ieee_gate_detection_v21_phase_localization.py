# ieee_gate_detection_v21_phase_localization.py

import numpy as np
import matplotlib.pyplot as plt

# ------------------------
# SIGNAL
# ------------------------

def generate_signal(n=1000, transition=600, noise_level=0.5, seed=1):
    np.random.seed(seed)
    t = np.arange(n)

    x = np.sin(0.2 * t)
    x[transition:] += noise_level * np.random.randn(n - transition)

    return t, x, transition


# ------------------------
# SWITCHING
# ------------------------

def compute_switching_density(x, window=30):
    dx = np.gradient(x)
    theta = np.arctan2(dx, x)

    n_sheets = 6
    sheet = np.floor((theta + np.pi) / (2 * np.pi) * n_sheets).astype(int)
    sheet = np.clip(sheet, 0, n_sheets - 1)

    switch = np.zeros_like(sheet)
    switch[1:] = (sheet[1:] != sheet[:-1]).astype(int)

    density = np.convolve(switch, np.ones(window)/window, mode='same')
    return density


# ------------------------
# VARIANCE
# ------------------------

def compute_variance(x, window=50):
    mean = np.convolve(x, np.ones(window)/window, mode='same')
    var = np.convolve((x - mean)**2, np.ones(window)/window, mode='same')
    return var


# ------------------------
# DETECTION
# ------------------------

def detect_time(signal, baseline_window=100, sensitivity=0.3):
    baseline = np.mean(signal[:baseline_window])
    max_val = np.max(signal)

    threshold = baseline + sensitivity * (max_val - baseline)

    for i, val in enumerate(signal):
        if val > threshold:
            return i

    return np.nan


# ------------------------
# RUN
# ------------------------

t, x, true_t = generate_signal()

dx = np.gradient(x)

# phase space
theta = np.arctan2(dx, x)
r = np.sqrt(x**2 + dx**2)

# signals
sd = compute_switching_density(x)
var = compute_variance(x)

# normalize
sd /= np.max(sd)
var /= np.max(var)

# detections
t_switch = detect_time(sd)
t_var = detect_time(var)

# ------------------------
# PLOT
# ------------------------

plt.figure(figsize=(8, 6))

# full trajectory
plt.scatter(theta, r, s=5, alpha=0.2, label="trajectory")

# mark points
plt.scatter(theta[true_t], r[true_t], color="black", s=80, label="true transition")
plt.scatter(theta[t_switch], r[t_switch], color="blue", s=80, label="switching detect")
plt.scatter(theta[t_var], r[t_var], color="orange", s=80, label="variance detect")

plt.xlabel("θ (phase)")
plt.ylabel("r (radius)")
plt.title("V21 — Phase Space Localization of Transition")
plt.legend()

plt.tight_layout()

output_path = "NEXAH_CORE/outputs/ieee_gates/v21_phase_localization.png"
plt.savefig(output_path, dpi=150)

print("\n--- V21 ---")
print(f"True t: {true_t}")
print(f"Switching t: {t_switch}")
print(f"Variance t: {t_var}")
print("Saved to:", output_path)

plt.show()
