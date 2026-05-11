# EXP_14_vortex_prime_modulation_lagrange.py
import numpy as np
import matplotlib.pyplot as plt

# Lagrange points phase with prime offset modulation
def lagrange_vortex_interaction(phase, prime_offset, base_amplitude):
    return base_amplitude * np.cos(phase + prime_offset)

# Define the parameters
phase = np.linspace(0, 2 * np.pi, 1000)
lagrange_6_prime_offset = np.pi / 3
lagrange_7_prime_offset = -np.pi / 3
base_amplitude = 1

# Create the signals
lagrange_6_signal = lagrange_vortex_interaction(phase, lagrange_6_prime_offset, base_amplitude)
lagrange_7_signal = lagrange_vortex_interaction(phase, lagrange_7_prime_offset, base_amplitude)

# Plot the signals
plt.figure(figsize=(10, 6))
plt.plot(phase, lagrange_6_signal, label='Lagrange 6 (Prime Offsets)', color='blue')
plt.plot(phase, lagrange_7_signal, label='Lagrange 7 (Prime Offsets)', color='red')
plt.title('Vortex Coupling and Prime Offset Modulation at Lagrange Points')
plt.xlabel('Phase')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

# Save the plot
output_path = 'outputs/EXP_14_vortex_prime_modulation_lagrange.png'
plt.savefig(output_path)

# Show the plot
plt.show()

# Return numerical results for future analysis
results = {
    'Lagrange 6 Phase': {'Mean': np.mean(lagrange_6_signal), 'Max': np.max(lagrange_6_signal), 'Min': np.min(lagrange_6_signal)},
    'Lagrange 7 Phase': {'Mean': np.mean(lagrange_7_signal), 'Max': np.max(lagrange_7_signal), 'Min': np.min(lagrange_7_signal)},
}
results
