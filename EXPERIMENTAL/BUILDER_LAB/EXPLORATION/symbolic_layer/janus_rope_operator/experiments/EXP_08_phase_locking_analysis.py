# ============================================================
# EXP_08 — Phase Locking Analysis
# JANUS Rope Operator / Phase Synchronization
#
# Goal:
# Analyze phase synchronization and locking behavior in modular transport systems.
#
# Outputs:
# 1. Phase Locking Visualization
# 2. Phase Drift and Synchronization Diagram
# 3. Phase Deviation Heatmap
#
# Author: NEXAH / JANUS Exploration
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from collections import defaultdict

# ============================================================
# PARAMETERS
# ============================================================

N = 32000  # Number of samples
DT = 0.0125  # Time step

MODULUS = 23  # Modulus for state space

# Phase locking and drift parameters
f1 = 2.0  # Frequency 1
f2 = 3.0  # Frequency 2
f3 = 5.0  # Frequency 3
f4 = 7.0  # Frequency 4

# ============================================================
# JANUS ROPE FIELD — Phase Drift and Synchronization
# ============================================================

# Generate the time series for the transport system
t = np.arange(N) * DT

# Layered frequency components for the x and y transport paths
x = (
    0.45*np.sin(f1*t) + 
    0.28*np.sin(f2*t + 0.6) + 
    0.15*np.sin(f3*t + 1.4)
)

y = (
    0.52*np.cos(f2*t) + 
    0.25*np.cos(f3*t + 0.3) + 
    0.14*np.sin(f4*t + 1.1)
)

# ============================================================
# PHASE SYNCHRONIZATION AND LOCKING
# ============================================================

# Calculate phase angles for the x and y transport paths
phase_x = np.angle(np.exp(1j * np.angle(np.cumsum(x))))  # Phase for x
phase_y = np.angle(np.exp(1j * np.angle(np.cumsum(y))))  # Phase for y

# Calculate the phase difference between x and y
phase_diff = np.unwrap(phase_x - phase_y)

# Measure the phase locking index (PLI) based on phase difference
PLI = np.abs(np.mean(np.exp(1j * phase_diff)))

# ============================================================
# VISUALIZATION 1 — Phase Locking
# ============================================================

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(t, phase_diff, color='blue', label="Phase Difference")
ax.set_title('EXP_08 — Phase Locking Analysis', fontsize=18)
ax.set_xlabel('Time (s)', fontsize=14)
ax.set_ylabel('Phase Difference (radians)', fontsize=14)
ax.legend()

# Save the figure
phase_locking_filepath = "outputs/EXP_08/exp08_phase_locking.png"
plt.tight_layout()
plt.savefig(phase_locking_filepath, dpi=300)

# ============================================================
# VISUALIZATION 2 — Phase Drift and Synchronization Diagram
# ============================================================

fig, ax = plt.subplots(figsize=(10, 10))

ax.scatter(x, y, c=phase_diff, cmap='plasma', alpha=0.75, s=10)
ax.set_title('EXP_08 — Phase Drift and Synchronization', fontsize=18)
ax.set_xlabel('X Transport', fontsize=14)
ax.set_ylabel('Y Transport', fontsize=14)

# Save the figure
phase_sync_filepath = "outputs/EXP_08/exp08_phase_drift_sync.png"
plt.tight_layout()
plt.savefig(phase_sync_filepath, dpi=300)

# ============================================================
# VISUALIZATION 3 — Phase Deviation Heatmap
# ============================================================

fig, ax = plt.subplots(figsize=(12, 4))

# Create a heatmap of phase differences across the system
heatmap = np.reshape(phase_diff, (int(np.sqrt(N)), int(np.sqrt(N))))

# Apply Gaussian filtering for smoothness
heatmap = gaussian_filter(heatmap, sigma=2)

ax.imshow(heatmap, cmap='magma', aspect='auto')
ax.set_title('EXP_08 — Phase Deviation Heatmap', fontsize=18)

# Save the figure
phase_deviation_filepath = "outputs/EXP_08/exp08_phase_deviation_heatmap.png"
plt.tight_layout()
plt.savefig(phase_deviation_filepath, dpi=300)

# ============================================================
# SUMMARY
# ============================================================

print("\n===================================")
print("EXP_08 — Phase Locking Analysis")
print("===================================\n")

print(f"Samples: {N}")
print(f"Modulus: {MODULUS}")
print(f"Phase Locking Index (PLI): {PLI:.5f}")

print("\nGenerated visuals:")
print("-----------------------------------")

files = [
    phase_locking_filepath,
    phase_sync_filepath,
    phase_deviation_filepath
]

for f in files:
    print(f)

print("\nDONE.\n")
