import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# LOAD
# ----------------------------
df = pd.read_csv("v34_physical_coupling.csv")
df["theta"] = 2 * np.pi * df["t"] / 24.0

# sortieren
df = df.sort_values("theta")

# Signal = C oder loops
signal = df["C"].values

# ----------------------------
# FOURIER
# ----------------------------
fft = np.fft.fft(signal)
freqs = np.fft.fftfreq(len(signal), d=1)

power = np.abs(fft)

# nur positive Frequenzen
mask = freqs > 0
freqs = freqs[mask]
power = power[mask]

# ----------------------------
# TOP MODES
# ----------------------------
top_idx = np.argsort(power)[-5:]

print("\n--- DOMINANT MODES ---")
for i in top_idx:
    print(f"freq={freqs[i]:.3f} | power={power[i]:.4f}")

# ----------------------------
# PLOT
# ----------------------------
plt.figure(figsize=(10,4))
plt.stem(freqs, power, basefmt=" ")
plt.xlabel("frequency")
plt.ylabel("power")
plt.title("Fourier Spectrum (C vs θ)")
plt.show()
