# run_iota_angular_symmetry_test.py

import numpy as np
import matplotlib.pyplot as plt

# load your data
data = np.load("phase_data.npz")  # adjust
theta = data["theta"]
iota_mask = data["iota_mask"]

theta_iota = theta[iota_mask]

# normalize to [0, 2π]
theta_iota = (theta_iota + 2*np.pi) % (2*np.pi)

# histogram
bins = 36
hist, edges = np.histogram(theta_iota, bins=bins, density=True)

centers = (edges[:-1] + edges[1:]) / 2

plt.figure(figsize=(8,4))
plt.plot(centers, hist, label="IOTA distribution")
plt.xlabel("theta")
plt.ylabel("density")
plt.title("IOTA Angular Distribution")
plt.legend()
plt.grid()
plt.show()


# Fourier test
fft_vals = np.abs(np.fft.fft(hist))
freqs = np.fft.fftfreq(len(hist))

plt.figure(figsize=(8,4))
plt.stem(freqs[:len(freqs)//2], fft_vals[:len(freqs)//2])
plt.title("Angular Frequency Spectrum")
plt.xlabel("frequency")
plt.ylabel("amplitude")
plt.grid()
plt.show()


# print dominant modes
dominant = np.argsort(fft_vals)[-5:]
print("Top frequency indices:", dominant)
