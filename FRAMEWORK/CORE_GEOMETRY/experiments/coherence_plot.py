import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# COHERENCE CORE
# -----------------------------
def compute_coherence(x, window=20):
    dx = np.diff(x)

    # Glättung der Bewegung
    kernel = np.ones(window) / window
    dx_smooth = np.convolve(dx, kernel, mode='same')

    # Feldapproximation (zweite Glättung)
    F = np.convolve(dx_smooth, kernel, mode='same')

    dx_smooth = dx_smooth[:len(F)]

    C = (dx_smooth * F) / (np.abs(dx_smooth) * np.abs(F) + 1e-6)

    return C


# -----------------------------
# COHERENCE LEVEL (wichtig!)
# -----------------------------
def coherence_level(C, window=80):
    kernel = np.ones(window) / window
    return np.convolve(C, kernel, mode='same')


# -----------------------------
# TEST SIGNAL (später ersetzen!)
# -----------------------------
x = np.sin(np.linspace(0, 20, 2000)) + 0.2*np.random.randn(2000)

# -----------------------------
# COMPUTE
# -----------------------------
C = compute_coherence(x)
C_smooth = coherence_level(C)

# -----------------------------
# PLOT
# -----------------------------
plt.figure(figsize=(12,6))

# Rohsignal (leicht transparent)
plt.plot(C, alpha=0.15, label="Raw Coherence")

# Glatte Struktur (das ist wichtig!)
plt.plot(C_smooth, linewidth=2, label="Coherence (Smoothed)")

plt.axhline(0, linestyle="--", color="gray")

plt.title("NEXAH Coherence — v2")
plt.legend()

plt.savefig("FRAMEWORK/CORE_GEOMETRY/visuals/coherence_v2.png", dpi=300)

plt.show()
