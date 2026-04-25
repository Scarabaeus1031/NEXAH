# ieee_gate_detection_v20_validation.py

import numpy as np

def generate_signal(seed):
    np.random.seed(seed)
    t = np.linspace(0, 100, 1000)

    x = np.sin(t * 0.2)
    x[600:] += 0.5 * np.random.randn(len(x[600:]))

    return t, x

def compute_switching_density(x):
    dx = np.gradient(x)
    theta = np.arctan2(dx, x)

    n_sheets = 6
    sheet = np.floor((theta + np.pi) / (2 * np.pi) * n_sheets).astype(int)
    sheet = np.clip(sheet, 0, n_sheets - 1)

    switch = np.zeros_like(sheet)
    switch[1:] = (sheet[1:] != sheet[:-1]).astype(int)

    window = 30
    density = np.convolve(switch, np.ones(window)/window, mode='same')

    return density

def compute_variance(x):
    window = 50
    var = np.convolve((x - np.mean(x))**2,
                      np.ones(window)/window,
                      mode='same')
    return var

# ------------------------
# Multi-run test
# ------------------------

runs = 30
results = []

for seed in range(runs):

    t, x = generate_signal(seed)

    switch_density = compute_switching_density(x)
    variance = compute_variance(x)

    # normalize
    switch_density /= np.max(switch_density)
    variance /= np.max(variance)

    # measure rise time (simple proxy)
    threshold = 0.5

    switch_time = np.argmax(switch_density > threshold)
    var_time = np.argmax(variance > threshold)

    results.append((switch_time, var_time))

# ------------------------
# Results
# ------------------------

results = np.array(results)

switch_times = results[:,0]
var_times = results[:,1]

print("Switching mean:", np.mean(switch_times))
print("Variance mean:", np.mean(var_times))

print("Switching std:", np.std(switch_times))
print("Variance std:", np.std(var_times))
