# run_iota_angular_symmetry_test.py

import numpy as np
import matplotlib.pyplot as plt

# 👉 IMPORT aus deinem bestehenden Script
from RESEARCH.validation.causality.phase_dynamics_analysis import run_phase_analysis

# oder falls du keine Funktion hast → copy/paste die Berechnung hier rein


# ================================
# RUN PHASE ANALYSIS
# ================================
results = run_phase_analysis()  # <- du musst das ggf. anpassen

theta = results["theta"]
iota_mask = results["iota_mask"]


# ================================
# ANGULAR DISTRIBUTION
# ================================
theta_iota = theta[iota_mask]

# normalize
theta_iota = (theta_iota + 2*np.pi) % (2*np.pi)

bins = 36
hist, edges = np.histogram(theta_iota, bins=bins, density=True)
centers = (edges[:-1] + edges[1:]) / 2

plt.figure(figsize=(8,4))
plt.plot(centers, hist)
plt.title("IOTA Angular Distribution")
plt.xlabel("theta")
plt.ylabel("density")
plt.grid()
plt.show()


# ================================
# FOURIER ANALYSIS
# ================================
fft_vals = np.abs(np.fft.fft(hist))

plt.figure(figsize=(8,4))
plt.plot(fft_vals[:len(fft_vals)//2])
plt.title("Angular Frequency Spectrum")
plt.xlabel("mode k")
plt.ylabel("amplitude")
plt.grid()
plt.show()


# ================================
# DOMINANT MODES
# ================================
dominant = np.argsort(fft_vals)[-5:]
print("Top modes:", dominant)
