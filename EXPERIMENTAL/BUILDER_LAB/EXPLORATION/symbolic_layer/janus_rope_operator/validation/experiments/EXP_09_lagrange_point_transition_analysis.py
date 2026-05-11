import numpy as np
import matplotlib.pyplot as plt
import os

# Constants for Lagrange Points (simplified positions)
LAGRANGE_POINTS = {
    'L6': np.array([1.0, -0.5]),  # Approximate position of Lagrange 6 (Leading Earth)
    'L7': np.array([1.0, 0.5]),   # Approximate position of Lagrange 7 (Trailing Earth)
    'Earth': np.array([1.0, 0.0])  # Position of Earth (simplified)
}

# Function to simulate the transition geometry with Lagrange points and prime offsets
def lagrange_point_transition_prime_offset(lagrange_point, prime_offset_factor):
    """
    Simulate transition geometry with Lagrange point influence and prime offset effects.
    Args:
    - lagrange_point: Coordinates of the Lagrange point.
    - prime_offset_factor: Offset factor for prime-based synchronization.
    Returns:
    - Phase and amplitude data for the transition geometry.
    """
    phase = np.linspace(0, 2 * np.pi, 100)
    amplitude = np.sin(phase + prime_offset_factor * lagrange_point[0]) * np.cos(phase)  # Prime offset effect
    return phase, amplitude

# Simulate transitions for Lagrange 6 and Lagrange 7 with prime offsets
lagrange_6_x, lagrange_6_y = lagrange_point_transition_prime_offset(LAGRANGE_POINTS['L6'], 0.5)
lagrange_7_x, lagrange_7_y = lagrange_point_transition_prime_offset(LAGRANGE_POINTS['L7'], -0.5)

# Plot the Lagrange Point impact on transition geometry with prime offsets
plt.figure(figsize=(10, 6))
plt.plot(lagrange_6_x, lagrange_6_y, label='Lagrange 6 (Prime Offsets)', color='b')
plt.plot(lagrange_7_x, lagrange_7_y, label='Lagrange 7 (Prime Offsets)', color='r')
plt.title('Lagrange Point Impact on Transition Geometry with Prime Offsets')
plt.xlabel('Phase')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Output directory setup (adapted for your path)
output_dir = "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/janus_rope_operator/validation/outputs/EXP_09/"
os.makedirs(output_dir, exist_ok=True)

# Save the updated plot in the correct directory
output_file = f"{output_dir}lagrange_point_transition_geometry_with_prime_offsets.png"
plt.savefig(output_file)

# Show the plot
plt.show()

# Store results in a dictionary for further analysis
lagrange_results_exp_09 = {
    'Lagrange 6 Impact with Prime Offsets': {'x': lagrange_6_x, 'y': lagrange_6_y},
    'Lagrange 7 Impact with Prime Offsets': {'x': lagrange_7_x, 'y': lagrange_7_y}
}

# Output file path for the results
lagrange_results_exp_09
