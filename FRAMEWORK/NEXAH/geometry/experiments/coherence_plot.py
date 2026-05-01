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
# COHERENCE LEVEL (Envelope)
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
C_abs = np.abs(C)
C_env = coherence_level(C_abs)

# -----------------------------
# LINEAR PLOT (v2)
# -----------------------------
plt.figure(figsize=(12,6))

plt.plot(C_abs, alpha=0.1, label="|Coherence| raw")
plt.plot(C_env, linewidth=2, label="Coherence Envelope")

plt.axhline(0, linestyle="--", color="gray")
plt.title("NEXAH Coherence — Envelope")
plt.legend()

plt.savefig("FRAMEWORK/CORE_GEOMETRY/visuals/coherence_v3.png", dpi=300)
plt.show()


# -----------------------------
# POLAR PLOT (v4 🔥)
# -----------------------------
t = np.arange(len(C_env))
theta = 2 * np.pi * t / len(C_env)

plt.figure(figsize=(6,6))
ax = plt.subplot(111, projection='polar')

# Scatter für "Petals / Bloom"
sc = ax.scatter(theta, C_env, c=C_env, cmap='plasma', s=5)

ax.set_title("NEXAH Coherence — Polar")

plt.savefig("FRAMEWORK/CORE_GEOMETRY/visuals/coherence_polar.png", dpi=300)
plt.show()
