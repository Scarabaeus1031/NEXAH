import numpy as np
import matplotlib.pyplot as plt
import os

# Constants for Lagrange Points (simplified positions)
LAGRANGE_POINTS = {
    'L6': np.array([1.0, -0.5]),  # Approximate position of Lagrange 6 (Leading Earth)
    'L7': np.array([1.0, 0.5]),   # Approximate position of Lagrange 7 (Trailing Earth)
    'Earth': np.array([1.0, 0.0])  # Position of Earth (simplified)
}

# Function to simulate the transition geometry
def lagrange_point_transition(lagrange_point):
    """
    Simulate the transition geometry for a given Lagrange point.
    Args:
    - lagrange_point: Coordinates of the Lagrange point.
    Returns:
    - Transition path (simulated data)
    """
    phase = np.linspace(0, 2 * np.pi, 100)
    amplitude = np.sin(phase) * np.cos(lagrange_point[0] * phase)  # Adding phase shift based on position
    return phase, amplitude

# Simulate transitions for Lagrange 6 and Lagrange 7
lagrange_6_x, lagrange_6_y = lagrange_point_transition(LAGRANGE_POINTS['L6'])
lagrange_7_x, lagrange_7_y = lagrange_point_transition(LAGRANGE_POINTS['L7'])

# Plot the Lagrange Point impact on transition geometry
plt.figure(figsize=(10, 6))
plt.plot(lagrange_6_x, lagrange_6_y, label='Lagrange 6', color='b')
plt.plot(lagrange_7_x, lagrange_7_y, label='Lagrange 7', color='r')
plt.title('Lagrange Point Impact on Transition Geometry with Real Positions')
plt.xlabel('Phase')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Output directory setup (adapted for your path)
output_dir = "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/janus_rope_operator/validation/outputs/EXP_05/"
os.makedirs(output_dir, exist_ok=True)

# Save the updated plot in the correct directory
output_file = f"{output_dir}lagrange_point_transition_geometry.png"
plt.savefig(output_file)

# Show the plot
plt.show()

# Store results in a dictionary for further analysis
lagrange_results_updated = {
    'Lagrange 6 Impact': {'x': lagrange_6_x, 'y': lagrange_6_y},
    'Lagrange 7 Impact': {'x': lagrange_7_x, 'y': lagrange_7_y}
}

# Output file path for the results
lagrange_results_updated
