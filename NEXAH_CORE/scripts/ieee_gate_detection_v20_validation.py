# ieee_gate_detection_v20_final_validation.py

import numpy as np
import matplotlib.pyplot as plt

# ------------------------
# SIGNAL
# ------------------------

def generate_signal(n=1000, transition=600, noise_level=0.5, seed=0):
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
# VARIANCE (correct)
# ------------------------

def compute_variance(x, window=50):
    mean = np.convolve(x, np.ones(window)/window, mode='same')
    var = np.convolve((x - mean)**2, np.ones(window)/window, mode='same')
    return var


# ------------------------
# FAIR DETECTION
# ------------------------

def detect_time(signal, baseline_window=100, sensitivity=0.3):
    baseline = np.mean(signal[:baseline_window])
    max_val = np.max(signal)

    threshold = baseline + sensitivity * (max_val - baseline)

    for i, val in enumerate(signal):
        if val > threshold:
            return i, threshold

    return np.nan, threshold


# ==================================================
# PART 1 — MULTI-RUN VALIDATION
# ==================================================

runs = 50

switch_times = []
var_times = []

for seed in range(runs):

    t, x, true_transition = generate_signal(seed=seed)

    sd = compute_switching_density(x)
    var = compute_variance(x)

    # normalize
    sd = sd / np.max(sd)
    var = var / np.max(var)

    t_switch, _ = detect_time(sd)
    t_var, _ = detect_time(var)

    switch_times.append(t_switch)
    var_times.append(t_var)


switch_times = np.array(switch_times)
var_times = np.array(var_times)

print("\n--- V20 FINAL RESULTS ---")

print(f"\nTrue transition: {true_transition}")

print("\nSwitching detection:")
print(f"mean = {np.mean(switch_times):.2f}, std = {np.std(switch_times):.2f}")

print("\nVariance detection:")
print(f"mean = {np.mean(var_times):.2f}, std = {np.std(var_times):.2f}")

print("\nError vs true transition:")
print(f"Switching error = {np.mean(switch_times - true_transition):.2f}")
print(f"Variance error  = {np.mean(var_times - true_transition):.2f}")


# ==================================================
# PART 2 — VISUAL VALIDATION (ONE RUN)
# ==================================================

t, x, true_transition = generate_signal(seed=1)

sd = compute_switching_density(x)
var = compute_variance(x)

# normalize
sd = sd / np.max(sd)
var = var / np.max(var)

t_switch, th_switch = detect_time(sd)
t_var, th_var = detect_time(var)

# ------------------------
# PLOT
# ------------------------

fig, axs = plt.subplots(3, 1, figsize=(12, 9), sharex=True)

# SIGNAL
axs[0].plot(t, x, color="purple")
axs[0].axvline(true_transition, linestyle="--", label="True transition")
axs[0].set_title("Signal")
axs[0].legend()

# SWITCHING
axs[1].plot(t, sd, color="blue", label="Switching Density")
axs[1].axhline(th_switch, linestyle="--", alpha=0.5)
axs[1].axvline(t_switch, color="blue", linestyle="--", label="Detected (Switching)")
axs[1].axvline(true_transition, linestyle="--", color="black")
axs[1].set_title("Switching Detection")
axs[1].legend()

# VARIANCE
axs[2].plot(t, var, color="orange", label="Variance")
axs[2].axhline(th_var, linestyle="--", alpha=0.5)
axs[2].axvline(t_var, color="orange", linestyle="--", label="Detected (Variance)")
axs[2].axvline(true_transition, linestyle="--", color="black")
axs[2].set_title("Variance Detection")
axs[2].legend()

plt.tight_layout()

# SAVE
output_path = "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/v20_final_validation.png"
plt.savefig(output_path, dpi=150)

print("\nSaved visual to:", output_path)

plt.show()
