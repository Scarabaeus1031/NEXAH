import numpy as np
import matplotlib.pyplot as plt
import os

# Constants for the dynamic system
LAGRANGE_POINTS = {
    'L6': np.array([1.0, -0.5]),  # Approximate position of Lagrange 6 (Leading Earth)
    'L7': np.array([1.0, 0.5]),   # Approximate position of Lagrange 7 (Trailing Earth)
}

# Function to simulate the interaction between the vortices (Wirbel)
def vortex_interaction(lagrange_point_1, lagrange_point_2):
    """
    Simulate the interaction between two vortices and their impact on transport dynamics.
    Args:
    - lagrange_point_1: Coordinates of the first Lagrange point.
    - lagrange_point_2: Coordinates of the second Lagrange point.
    Returns:
    - Interaction result (simulated data)
    """
    # Phase dynamics with varying offsets for each Lagrange point
    phase = np.linspace(0, 2 * np.pi, 100)
    amplitude_1 = np.sin(phase + lagrange_point_1[0]) * np.cos(phase)  # L6 effect
    amplitude_2 = np.sin(phase + lagrange_point_2[0]) * np.cos(phase)  # L7 effect

    # Calculate the interaction impact (cross-phase interactions)
    interaction = amplitude_1 + amplitude_2
    return phase, amplitude_1, amplitude_2, interaction

# Simulate interactions between Lagrange 6 and Lagrange 7
phase, amplitude_L6, amplitude_L7, interaction = vortex_interaction(LAGRANGE_POINTS['L6'], LAGRANGE_POINTS['L7'])

# Plot the interaction results
plt.figure(figsize=(10, 6))

# Plot for Lagrange 6
plt.plot(phase, amplitude_L6, label='Lagrange 6 (Leading)', color='b')

# Plot for Lagrange 7
plt.plot(phase, amplitude_L7, label='Lagrange 7 (Trailing)', color='r')

# Plot for the interaction between L6 and L7
plt.plot(phase, interaction, label='Interaction', color='purple', linestyle='--')

plt.title('Wirbelinteraktion und Phasenstabilität')
plt.xlabel('Phase')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Output directory setup (adapted for your path)
output_dir = "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/janus_rope_operator/experiments/EXP_10/"
os.makedirs(output_dir, exist_ok=True)

# Save the updated plot in the correct directory
output_file = f"{output_dir}vortex_interaction_phase_plot.png"
plt.savefig(output_file)

# Show the plot
plt.show()

# Store results in a dictionary for further analysis
vortex_interaction_results = {
    'Lagrange 6 Impact': {'x': phase, 'y': amplitude_L6},
    'Lagrange 7 Impact': {'x': phase, 'y': amplitude_L7},
    'Interaction Impact': {'x': phase, 'y': interaction}
}

# Output file path for the results
vortex_interaction_results
