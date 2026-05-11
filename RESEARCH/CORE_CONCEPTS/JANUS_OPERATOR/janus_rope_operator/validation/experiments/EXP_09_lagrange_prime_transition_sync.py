import numpy as np
import matplotlib.pyplot as plt
import os

# Constants for Lagrange Points (simplified positions)
LAGRANGE_POINTS = {
    'L6': np.array([1.0, -0.5]),  # Approximate position of Lagrange 6 (Leading Earth)
    'L7': np.array([1.0, 0.5]),   # Approximate position of Lagrange 7 (Trailing Earth)
    'Earth': np.array([1.0, 0.0])  # Position of Earth (simplified)
}

# Function to simulate the transition geometry with prime offsets
def lagrange_point_transition_with_offsets(lagrange_point, offset_factor):
    """
    Simulate the transition geometry for a given Lagrange point with prime offsets.
    Args:
    - lagrange_point: Coordinates of the Lagrange point.
    - offset_factor: Factor to apply prime offset to the phase and amplitude.
    Returns:
    - Transition path (simulated data)
    """
    phase = np.linspace(0, 2 * np.pi, 100)
    amplitude = np.sin(phase + lagrange_point[0] * offset_factor) * np.cos(lagrange_point[0] * phase)  # Adding prime offset to phase
    return phase, amplitude

# Simulate transitions for Lagrange 6 and Lagrange 7 with Prime Offsets
lagrange_6_x, lagrange_6_y = lagrange_point_transition_with_offsets(LAGRANGE_POINTS['L6'], 0.3)
lagrange_7_x, lagrange_7_y = lagrange_point_transition_with_offsets(LAGRANGE_POINTS['L7'], 0.3)

# Plot the Lagrange Point impact on transition geometry with Prime Offsets
plt.figure(figsize=(10, 6))
plt.plot(lagrange_6_x, lagrange_6_y, label='Lagrange 6 (Prime Offsets)', color='blue')
plt.plot(lagrange_7_x, lagrange_7_y, label='Lagrange 7 (Prime Offsets)', color='red')
plt.title('Lagrange Point Impact on Transition Geometry with Prime Offsets')
plt.xlabel('Phase')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Output directory setup (adapted for your path)
output_dir = "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/janus_rope_operator/validation/outputs/EXP_09/"
os.makedirs(output_dir, exist_ok=True)

# Save the plot in the correct directory
output_file = f"{output_dir}lagrange_prime_transition_geometry.png"
plt.savefig(output_file)

# Show the plot
plt.show()

# Store results in a dictionary for further analysis
lagrange_prime_results = {
    'Lagrange 6 Impact': {'x': lagrange_6_x, 'y': lagrange_6_y},
    'Lagrange 7 Impact': {'x': lagrange_7_x, 'y': lagrange_7_y}
}

# Output file path for the results
lagrange_prime_results
