# ieee_gate_detection_v18_leading_indicator.py

import numpy as np
import matplotlib.pyplot as plt

# ------------------------
# Synthetic signal (replace later with real)
# ------------------------

np.random.seed(0)
t = np.linspace(0, 100, 1000)

x = np.sin(t * 0.2)

# add instability
x[600:] += 0.5 * np.random.randn(len(x[600:]))

dx = np.gradient(x)

# ------------------------
# Phase → sheets
# ------------------------

theta = np.arctan2(dx, x)

n_sheets = 6
sheet = np.floor((theta + np.pi) / (2 * np.pi) * n_sheets).astype(int)
sheet = np.clip(sheet, 0, n_sheets - 1)

# ------------------------
# Switching detection
# ------------------------

switch = np.zeros_like(sheet)
switch[1:] = (sheet[1:] != sheet[:-1]).astype(int)

# ------------------------
# Switching density
# ------------------------

window = 30
switch_density = np.convolve(switch, np.ones(window)/window, mode='same')

# ------------------------
# Collapse proxy (variance)
# ------------------------

var_window = 50
variance = np.convolve((x - np.mean(x))**2,
                       np.ones(var_window)/var_window,
                       mode='same')

# normalize
switch_density = switch_density / np.max(switch_density)
variance = variance / np.max(variance)

# ------------------------
# Plot (KEY VISUAL)
# ------------------------

plt.figure(figsize=(12,6))

plt.plot(t, switch_density, label="Switching Density", linewidth=2)
plt.plot(t, variance, label="Variance (collapse proxy)", linewidth=2)

plt.axvline(t[600], linestyle='--', alpha=0.3, label="true regime change")

plt.legend()
plt.title("v18 — Leading Indicator Test")
plt.xlabel("time")

# SAVE (important!)
plt.savefig("BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/v18_leading_indicator.png", dpi=150)

plt.close()
