import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# COHERENCE CORE
# -----------------------------
def compute_coherence(x, window=20):
    dx = np.diff(x)

    kernel = np.ones(window) / window
    dx_smooth = np.convolve(dx, kernel, mode='same')
    F = np.convolve(dx_smooth, kernel, mode='same')

    dx_smooth = dx_smooth[:len(F)]

    C = (dx_smooth * F) / (np.abs(dx_smooth) * np.abs(F) + 1e-6)
    return C


# -----------------------------
# ENVELOPE
# -----------------------------
def coherence_level(C, window=80):
    kernel = np.ones(window) / window
    return np.convolve(C, kernel, mode='same')


# -----------------------------
# TEST SIGNAL (replace later!)
# -----------------------------
x = np.sin(np.linspace(0, 20, 2000)) + 0.2*np.random.randn(2000)

# -----------------------------
# COMPUTE
# -----------------------------
C = compute_coherence(x)
C_abs = np.abs(C)
C_env = coherence_level(C_abs)

# 🔥 DROPS (NEW)
drops = 1 - C_abs
drops_env = coherence_level(drops)

# -----------------------------
# PLOT 1 — COHERENCE
# -----------------------------
plt.figure(figsize=(12,6))

plt.plot(C_abs, alpha=0.1, label="|Coherence| raw")
plt.plot(C_env, linewidth=2, label="Coherence Envelope")

plt.title("NEXAH Coherence — Envelope")
plt.legend()

plt.savefig("FRAMEWORK/CORE_GEOMETRY/visuals/coherence_v4.png", dpi=300)
plt.show()


# -----------------------------
# PLOT 2 — DROPS 🔥
# -----------------------------
plt.figure(figsize=(12,4))

plt.plot(drops, alpha=0.2, label="Drops (raw)")
plt.plot(drops_env, linewidth=2, label="Drop Intensity")

plt.title("NEXAH Coherence Drops")
plt.legend()

plt.savefig("FRAMEWORK/CORE_GEOMETRY/visuals/coherence_drops.png", dpi=300)
plt.show()


# -----------------------------
# POLAR — COHERENCE
# -----------------------------
t = np.arange(len(C_env))
theta = 2 * np.pi * t / len(C_env)

plt.figure(figsize=(6,6))
ax = plt.subplot(111, projection='polar')

ax.scatter(theta, C_env, c=C_env, cmap='plasma', s=5)

ax.set_title("Coherence Polar")

plt.savefig("FRAMEWORK/CORE_GEOMETRY/visuals/coherence_polar_v4.png", dpi=300)
plt.show()


# -----------------------------
# POLAR — DROPS 🔥🔥
# -----------------------------
plt.figure(figsize=(6,6))
ax = plt.subplot(111, projection='polar')

ax.scatter(theta, drops_env, c=drops_env, cmap='inferno', s=5)

ax.set_title("Drop Intensity Polar")

plt.savefig("FRAMEWORK/CORE_GEOMETRY/visuals/coherence_drops_polar.png", dpi=300)
plt.show()
