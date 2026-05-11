import numpy as np
import matplotlib.pyplot as plt
import os

# Constants for Prime Offset and Vortex Coupling
LAGRANGE_POINTS = {
    'L6': np.array([1.0, -0.5]),  # Lagrange 6 Position
    'L7': np.array([1.0, 0.5]),   # Lagrange 7 Position
}

# Phase Drift and Prime Offsets Function
def prime_offset_modulation(phase, prime_offset=7):
    """
    Modulate the phase with a prime offset (drift).
    Args:
    - phase: Phase input (numpy array).
    - prime_offset: The prime number offset for the drift (default 7).
    Returns:
    - Modulated phase (numpy array).
    """
    return np.sin(phase + prime_offset * np.pi / 180)  # modulating by prime offset

# Vortex Coupling Simulation
def vortex_coupling(phase, coupling_strength=1.5):
    """
    Simulate the vortex coupling behavior by introducing nonlinearity.
    Args:
    - phase: Phase input (numpy array).
    - coupling_strength: Strength of the vortex coupling (default 1.5).
    Returns:
    - Coupled phase (numpy array).
    """
    return np.cos(coupling_strength * phase)  # non-linear vortex coupling

# Lagrange Points and Phase Drift Calculation
phase = np.linspace(0, 2 * np.pi, 100)
lagrange_6_phase = prime_offset_modulation(phase, 6)  # Modulate phase with prime offset for L6
lagrange_7_phase = prime_offset_modulation(phase, 7)  # Modulate phase with prime offset for L7

# Vortex Coupling on Lagrange Points
coupled_lagrange_6 = vortex_coupling(lagrange_6_phase)
coupled_lagrange_7 = vortex_coupling(lagrange_7_phase)

# Plot the results
plt.figure(figsize=(10, 6))

# Plot Lagrange 6 and Lagrange 7
plt.plot(phase, lagrange_6_phase, label='Lagrange 6 (Prime Offsets)', color='blue')
plt.plot(phase, lagrange_7_phase, label='Lagrange 7 (Prime Offsets)', color='red')

# Plot Vortex Coupled Lagrange Points
plt.plot(phase, coupled_lagrange_6, label='Coupled Lagrange 6', linestyle='--', color='purple')
plt.plot(phase, coupled_lagrange_7, label='Coupled Lagrange 7', linestyle='--', color='orange')

# Titles and Labels
plt.title('Vortex Coupling and Prime Offset Modulation at Lagrange Points')
plt.xlabel('Phase')
plt.ylabel('Amplitude')
plt.legend()

# Save the figure
output_dir = "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/janus_rope_operator/validation/outputs/EXP_11/"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'vortex_prime_modulation.png')
plt.savefig(output_file)

# Show the plot
plt.show()

# Numerical Results
modulated_phases = {
    'L6 Phase': lagrange_6_phase,
    'L7 Phase': lagrange_7_phase,
    'Coupled L6': coupled_lagrange_6,
    'Coupled L7': coupled_lagrange_7
}

print("Numerical Results:")
for key, value in modulated_phases.items():
    print(f"{key}: Mean = {np.mean(value):.3f}, Max = {np.max(value):.3f}, Min = {np.min(value):.3f}")
