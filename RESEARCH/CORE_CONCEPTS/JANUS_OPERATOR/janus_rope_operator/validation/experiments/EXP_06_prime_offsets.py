import numpy as np
import matplotlib.pyplot as plt
import os

# Constants for Lagrange Points (simplified positions)
LAGRANGE_POINTS = {
    'L6': np.array([1.0, -0.5]),  # Approximate position of Lagrange 6 (Leading Earth)
    'L7': np.array([1.0, 0.5]),   # Approximate position of Lagrange 7 (Trailing Earth)
    'Earth': np.array([1.0, 0.0])  # Position of Earth (simplified)
}

# Prime offsets for Lagrange geometry (simplified hypothesis)
PRIME_OFFSETS = {
    'L6': [2, 3, 5],   # Example prime offsets for Lagrange 6
    'L7': [7, 11, 13]   # Example prime offsets for Lagrange 7
}

# Function to simulate the transition geometry with aperture and prime offsets
def lagrange_prime_transition(lagrange_point, prime_offsets):
    """
    Simulate the transition geometry for a given Lagrange point with prime offsets.
    Args:
    - lagrange_point: Coordinates of the Lagrange point.
    - prime_offsets: List of prime offsets influencing the transition geometry.
    Returns:
    - Transition path (simulated data)
    """
    phase = np.linspace(0, 2 * np.pi, 100)
    amplitude = np.sin(phase + np.sum(prime_offsets)) * np.cos(lagrange_point[0] * phase)  # Adjusting based on prime offsets
    return phase, amplitude

# Simulate transitions for Lagrange 6 and Lagrange 7 with prime offsets
lagrange_6_x, lagrange_6_y = lagrange_prime_transition(LAGRANGE_POINTS['L6'], PRIME_OFFSETS['L6'])
lagrange_7_x, lagrange_7_y = lagrange_prime_transition(LAGRANGE_POINTS['L7'], PRIME_OFFSETS['L7'])

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

# Output directory setup
output_dir = "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/janus_rope_operator/validation/outputs/EXP_06/"
os.makedirs(output_dir, exist_ok=True)

# Save the updated plot in the correct directory
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
