import numpy as np
import matplotlib.pyplot as plt
import os

# Constants for Lagrange Points with Prime Offsets
LAGRANGE_POINTS = {
    'L6': np.array([1.0, -0.5]),  # Approximate position of Lagrange 6 (Leading Earth)
    'L7': np.array([1.0, 0.5]),   # Approximate position of Lagrange 7 (Trailing Earth)
    'Earth': np.array([1.0, 0.0])  # Position of Earth (simplified)
}

# Function to simulate the transition geometry with Prime Offsets
def lagrange_point_prime_transition(lagrange_point, prime_offset):
    """
    Simulate the transition geometry for a given Lagrange point with a prime offset.
    Args:
    - lagrange_point: Coordinates of the Lagrange point.
    - prime_offset: Prime offset value to influence transition.
    Returns:
    - Transition path (simulated data)
    """
    phase = np.linspace(0, 2 * np.pi, 100)
    amplitude = np.sin(phase + prime_offset) * np.cos(lagrange_point[0] * phase)  # Adding phase shift and prime offset
    return phase, amplitude

# Simulate transitions for Lagrange 6 and Lagrange 7 with Prime Offsets
prime_offset_L6 = 0.5  # Prime offset for Lagrange 6
prime_offset_L7 = -0.5  # Prime offset for Lagrange 7

lagrange_6_x, lagrange_6_y = lagrange_point_prime_transition(LAGRANGE_POINTS['L6'], prime_offset_L6)
lagrange_7_x, lagrange_7_y = lagrange_point_prime_transition(LAGRANGE_POINTS['L7'], prime_offset_L7)

# Plot the Lagrange Point impact on transition geometry with Prime Offsets
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
output_dir = "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/janus_rope_operator/validation/outputs/EXP_07/"
os.makedirs(output_dir, exist_ok=True)

# Save the updated plot in the correct directory
output_file = f"{output_dir}lagrange_prime_transition_geometry.png"
plt.savefig(output_file)

# Show the plot
plt.show()

# Store results in a dictionary for further analysis
lagrange_prime_results = {
    'Lagrange 6 Impact (Prime Offsets)': {'x': lagrange_6_x, 'y': lagrange_6_y},
    'Lagrange 7 Impact (Prime Offsets)': {'x': lagrange_7_x, 'y': lagrange_7_y}
}

# Output file path for the results
lagrange_prime_results
