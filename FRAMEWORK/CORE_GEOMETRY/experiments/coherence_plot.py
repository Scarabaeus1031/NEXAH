import numpy as np
import matplotlib.pyplot as plt

def compute_coherence(x, window=10):
    dx = np.diff(x)
    
    # Feldapproximation (glätten)
    kernel = np.ones(window) / window
    F = np.convolve(dx, kernel, mode='same')
    
    dx = dx[:len(F)]
    
    C = (dx * F) / (np.abs(dx) * np.abs(F) + 1e-8)
    
    return C

# Beispiel: ersetze x durch deine IEEE-Daten
x = np.load("your_ieee_signal.npy")

C = compute_coherence(x)

plt.figure(figsize=(10,5))
plt.plot(C, label="Coherence")
plt.axhline(0, linestyle="--", color="gray")
plt.title("NEXAH Coherence")
plt.legend()
plt.savefig("../visuals/coherence_example.png", dpi=300)
plt.show()
