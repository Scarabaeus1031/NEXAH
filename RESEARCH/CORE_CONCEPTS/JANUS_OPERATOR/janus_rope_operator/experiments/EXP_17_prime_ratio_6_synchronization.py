import numpy as np
import matplotlib.pyplot as plt

# Prime Ratios
def prime_ratio(amplitude, phase_shift, ratio):
    return amplitude * np.cos(phase_shift * ratio)

# Phase and Amplitude
phase = np.linspace(0, 2 * np.pi, 1000)
amplitude = np.sin(phase)

# Prime Ratios (3:5, 3:1, 3:3)
prime_ratio_6 = 3 / 5
prime_ratio_30 = 3 / 1
prime_ratio_10 = 3 / 3

# Apply Prime Ratios
y_6 = prime_ratio(amplitude, phase, prime_ratio_6)
y_30 = prime_ratio(amplitude, phase, prime_ratio_30)
y_10 = prime_ratio(amplitude, phase, prime_ratio_10)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(phase, y_6, label="Prime Ratio 6 (3:5)", color="blue")
plt.plot(phase, y_30, label="Prime Ratio 30 (3:1)", color="orange")
plt.plot(phase, y_10, label="Prime Ratio 10 (3:3)", color="green")

# Adding Vertical Lines (where crosses occur)
plt.axvline(x=np.pi, color='purple', linestyle='--', label="Synchronization Point (π)")
plt.axvline(x=9.7, color='magenta', linestyle='--', label="Prime Ratio 6 Sync Point")

# Labels
plt.title('Prime Modulation and Phase Synchronization (3:5, 3:1, 3:3)')
plt.xlabel('Phase')
plt.ylabel('Amplitude')
plt.legend()

# Show Plot
plt.show()
