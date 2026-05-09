# ============================================================
# EXPERIMENT 06
# JANUS_FREQUENCY_DECOMPOSITION
# ============================================================
#
# Goal:
# Analyze whether JANUS coherence exhibits
# dominant frequency structure and harmonic organization.
#
# Focus:
# - FFT spectrum
# - power-law structure
# - dominant oscillation bands
# - coherence modulation frequencies
#
# Outputs:
# - janus_fft_spectrum.png
# - janus_power_spectrum.png
# - janus_frequency_peaks.png
#
# ============================================================

# file:
# scripts/janus_frequency_decomposition.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.signal import find_peaks
from scipy.fft import rfft, rfftfreq

plt.style.use("ggplot")

# ============================================================
# LORENZ SYSTEM
# ============================================================

sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0


def lorenz(t, state):
    x, y, z = state

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    return [dx, dy, dz]


# ============================================================
# SIMULATION
# ============================================================

dt = 0.01
T = 120.0

t_eval = np.arange(0, T, dt)

sol = solve_ivp(
    lorenz,
    [0, T],
    [1.0, 1.0, 1.0],
    t_eval=t_eval,
)

x = sol.y[0]
y = sol.y[1]
z = sol.y[2]

# ============================================================
# JANUS COHERENCE
# ============================================================

dx = np.gradient(x)
dy = np.gradient(y)

theta = np.arctan2(dy, dx)

janus = np.abs(np.cos(theta))

janus = (
    janus - np.min(janus)
) / (
    np.max(janus) - np.min(janus)
)

# ============================================================
# FFT
# ============================================================

N = len(janus)

freqs = rfftfreq(N, d=dt)
fft_vals = np.abs(rfft(janus))

power = fft_vals ** 2

# ============================================================
# PEAK DETECTION
# ============================================================

peak_idx, _ = find_peaks(
    power,
    prominence=np.max(power) * 0.05
)

peak_freqs = freqs[peak_idx]
peak_power = power[peak_idx]

# ============================================================
# VISUALIZATION
# ============================================================

# ------------------------------------------------------------
# FFT spectrum
# ------------------------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(freqs, fft_vals)

plt.xlim(0, 5)

plt.xlabel("frequency")
plt.ylabel("FFT amplitude")

plt.title("JANUS Frequency Spectrum")

plt.tight_layout()

plt.savefig(
    "outputs/janus_fft_spectrum.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Power spectrum
# ------------------------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(freqs, power)

plt.xlim(0, 5)

plt.xlabel("frequency")
plt.ylabel("power")

plt.title("JANUS Power Spectrum")

plt.tight_layout()

plt.savefig(
    "outputs/janus_power_spectrum.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Frequency peaks
# ------------------------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(freqs, power)

plt.scatter(
    peak_freqs,
    peak_power,
    color="red",
    s=40,
    label="dominant peaks"
)

for f, p in zip(peak_freqs, peak_power):
    plt.text(
        f,
        p,
        f"{f:.2f}",
        fontsize=8
    )

plt.xlim(0, 5)

plt.xlabel("frequency")
plt.ylabel("power")

plt.title("Dominant JANUS Frequencies")

plt.legend()

plt.tight_layout()

plt.savefig(
    "outputs/janus_frequency_peaks.png",
    dpi=300
)

plt.close()

# ============================================================
# RESULTS
# ============================================================

print("\n================================================")
print("JANUS FREQUENCY DECOMPOSITION")
print("================================================")

print(f"samples: {N}")
print(f"dominant peaks: {len(peak_freqs)}")

if len(peak_freqs) > 0:
    print("\nTop frequencies:")

    idx_sorted = np.argsort(peak_power)[::-1]

    for i in idx_sorted[:10]:
        print(
            f"freq = {peak_freqs[i]:.4f} "
            f"power = {peak_power[i]:.4f}"
        )

print("\noutputs saved to:")
print("outputs/")
print("================================================")
