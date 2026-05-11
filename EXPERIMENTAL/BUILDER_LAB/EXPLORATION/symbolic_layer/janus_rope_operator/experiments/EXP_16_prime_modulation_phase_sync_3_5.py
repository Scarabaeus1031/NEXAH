import os
import numpy as np
import matplotlib.pyplot as plt

# Define the phase offset modulation function
def prime_modulation_phase_sync(phase, prime_ratio, frequency=1):
    """Simulate prime modulation with phase synchronization."""
    # Phase modulation based on prime ratio (e.g., 3:5, 2:3, etc.)
    return np.sin(frequency * phase + prime_ratio * np.pi / 2)

# Define parameters
phase = np.linspace(0, 2 * np.pi, 1000)
prime_ratios = [3/5, 3/1, 3/3]  # Different prime ratios for the experiments
frequency = 1  # Base frequency for modulation

# Create a plot to visualize the different prime ratios
plt.figure(figsize=(10, 6))

# Plot each prime modulation
for prime_ratio in prime_ratios:
    modulated_wave = prime_modulation_phase_sync(phase, prime_ratio, frequency)
    label = f"Prime Ratio {int(prime_ratio*10)}"
    plt.plot(phase, modulated_wave, label=label)

# Add labels, legend, and title
plt.title("Prime Modulation and Phase Synchronization (3:5, 3:1, 3:3)")
plt.xlabel("Phase")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)

# Create output directory if it doesn't exist
output_dir = "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/janus_rope_operator/experiments/EXP_16/"
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Save the plot
output_file = f"{output_dir}vortex_prime_modulation_3_5.png"
plt.savefig(output_file)

# Show the plot
plt.show()

# Output results as a dictionary for analysis
modulation_results = {
    'prime_ratios': prime_ratios,
    'modulated_waves': [prime_modulation_phase_sync(phase, ratio, frequency) for ratio in prime_ratios]
}

# Return the results for further analysis
modulation_results
