# ieee_gate_detection_v19_detection_timing_validation.py

import numpy as np

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
# SWITCHING DENSITY
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
# VARIANCE (CORRECTED)
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
            return i

    return np.nan


# ------------------------
# MULTI-RUN VALIDATION
# ------------------------

runs = 50

switch_times = []
var_times = []
true_times = []

for seed in range(runs):

    t, x, true_transition = generate_signal(seed=seed)

    sd = compute_switching_density(x)
    var = compute_variance(x)

    # normalize (important for fair comparison)
    sd = sd / np.max(sd)
    var = var / np.max(var)

    t_switch = detect_time(sd)
    t_var = detect_time(var)

    switch_times.append(t_switch)
    var_times.append(t_var)
    true_times.append(true_transition)


# ------------------------
# RESULTS
# ------------------------

switch_times = np.array(switch_times)
var_times = np.array(var_times)
true_times = np.array(true_times)

print("\n--- V19 RESULTS (FIXED) ---")

print("\nTrue transition:", true_times[0])

print("\nSwitching detection:")
print(f"mean = {np.mean(switch_times):.2f}, std = {np.std(switch_times):.2f}")

print("\nVariance detection:")
print(f"mean = {np.mean(var_times):.2f}, std = {np.std(var_times):.2f}")

print("\nError vs true transition:")
print(f"Switching error = {np.mean(switch_times - true_times):.2f}")
print(f"Variance error  = {np.mean(var_times - true_times):.2f}")
