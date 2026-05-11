import numpy as np
import matplotlib.pyplot as plt

# Constants and initial setup for Lagrange Points
LAGRANGE_POINTS = {
    1: np.array([1.0, 0.0]),
    2: np.array([1.5, 0.0]),
    6: np.array([1.0, -0.5]),
    7: np.array([1.0, 0.5])
}

# Define a simple system for Lagrange points validation
def lagrange_point_impact(lagrange_point):
    """
    Simulate and track the influence of a Lagrange point on transition geometry.
    Args:
    - lagrange_point: Coordinates of the Lagrange point.
    Returns:
    - Transition paths (simulated data)
    """
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x) * np.cos(lagrange_point[0] * x)
    return x, y

# Simulate the Lagrange Point Impact for Lagrange 6 and 7
lagrange_6_x, lagrange_6_y = lagrange_point_impact(LAGRANGE_POINTS[6])
lagrange_7_x, lagrange_7_y = lagrange_point_impact(LAGRANGE_POINTS[7])

# Create visuals for the simulation
plt.figure(figsize=(10, 6))
plt.plot(lagrange_6_x, lagrange_6_y, label='Lagrange 6', color='b')
plt.plot(lagrange_7_x, lagrange_7_y, label='Lagrange 7', color='r')
plt.title('Lagrange Point Impact on Transition Geometry')
plt.xlabel('Phase')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save the output plot
plt.savefig('EXP_05_Lagrange_Point_Validation.png')
plt.close()

# Store relevant information
lagrange_results = {
    'Lagrange 6 Impact': {'x': lagrange_6_x, 'y': lagrange_6_y},
    'Lagrange 7 Impact': {'x': lagrange_7_x, 'y': lagrange_7_y}
}

lagrange_results
