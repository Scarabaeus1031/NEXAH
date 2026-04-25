# ieee_gate_detection_v17_switching_metric.py

import numpy as np
import matplotlib.pyplot as plt

# ------------------------
# Example signal (replace with your own)
# ------------------------

np.random.seed(0)
t = np.linspace(0, 100, 1000)

# synthetic regime change
x = np.sin(t * 0.2)

# add instability later
x[600:] += 0.5 * np.random.randn(len(x[600:]))

dx = np.gradient(x)

# ------------------------
# Phase + sheet assignment
# ------------------------

theta = np.arctan2(dx, x)

# discretize phase into sheets
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
# Plot
# ------------------------

fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

# signal
axs[0].plot(t, x, color='purple')
axs[0].set_title("Signal")

# switching events
axs[1].plot(t, sheet, color='black', linewidth=1)
axs[1].scatter(t[switch == 1], sheet[switch == 1], color='red', s=10)
axs[1].set_title("Sheet Switching")

# switching density
axs[2].plot(t, switch_density, color='blue')
axs[2].set_title("Switching Density")

plt.tight_layout()
plt.show()
