# mod7_fft_analysis.py

import numpy as np
from sympy import primerange
import matplotlib.pyplot as plt

mod = 7
primes = list(primerange(3, 10000))

# sequence
seq = np.array([p % mod for p in primes])

# normalize
seq = (seq - np.mean(seq)) / np.std(seq)

# FFT
fft_vals = np.fft.fft(seq)
freqs = np.fft.fftfreq(len(seq))

# power spectrum
power = np.abs(fft_vals)**2

plt.figure(figsize=(10,5))
plt.plot(freqs[:len(freqs)//2], power[:len(power)//2])
plt.title("FFT Spectrum (Prime mod 7)")
plt.xlabel("Frequency")
plt.ylabel("Power")
plt.show()


# ================= AUTO SAVE HOOK =================
import os
import matplotlib.pyplot as plt

if os.environ.get("AUTO_SAVE") == "1":

    figs = list(map(plt.figure, plt.get_fignums()))

    if not figs:
        print("[WARN] No figures to save.")

    for i, fig in enumerate(figs):
        filename = __file__.split("/")[-1].replace(".py", f"_{i}.png")
        fig.savefig(f"output/plots/{filename}", dpi=150, bbox_inches="tight")

    plt.close("all")

else:
    plt.show()

# =================================================
