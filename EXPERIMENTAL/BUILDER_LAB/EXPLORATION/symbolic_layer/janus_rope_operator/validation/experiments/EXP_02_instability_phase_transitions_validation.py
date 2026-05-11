# EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/janus_rope_operator/validation/experiments/EXP_02_instability_phase_transitions_validation.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os

# Lorenz system differential equations
def lorenz(X, t, sigma, beta, rho):
    x, y, z = X
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# Rössler system differential equations
def rossler(X, t, a, b, c):
    x, y, z = X
    dxdt = -y - z
    dydt = x + a * y
    dzdt = b + z * (x - c)
    return [dxdt, dydt, dzdt]

# Define time vector
t = np.linspace(0, 100, 10000)

# Initial conditions
X0 = [1, 1, 1]

# Parameters for Lorenz system
sigma = 10
beta = 8/3
rho = 28

# Parameters for Rössler system
a = 0.2
b = 0.2
c = 5.7

# Solve the systems
lorenz_sol = odeint(lorenz, X0, t, args=(sigma, beta, rho))
rossler_sol = odeint(rossler, X0, t, args=(a, b, c))

# Compute phase
lorenz_phase = np.arctan2(lorenz_sol[:, 1], lorenz_sol[:, 0])  # phase for Lorenz system
rossler_phase = np.arctan2(rossler_sol[:, 1], rossler_sol[:, 0])  # phase for Rössler system

# Calculate phase mismatch (simple difference)
phase_mismatch = np.abs(np.mean(lorenz_phase - rossler_phase))

# Print phase mismatch
print(f"Phase Mismatch between Lorenz and Rössler systems: {phase_mismatch}")

# Create output directory if it doesn't exist
output_dir = './validation/outputs/EXP_02/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Plot the phase comparison for both systems
plt.figure(figsize=(12, 6))

# Plot Lorenz phase
plt.subplot(1, 2, 1)
plt.plot(t, lorenz_phase, color='blue')
plt.title("Lorenz System Phase")
plt.xlabel("Time")
plt.ylabel("Phase")

# Plot Rössler phase
plt.subplot(1, 2, 2)
plt.plot(t, rossler_phase, color='red')
plt.title("Rössler System Phase")
plt.xlabel("Time")
plt.ylabel("Phase")

# Save the plot
plt.savefig(f"{output_dir}lorenz_rossler_phase_comparison.png")

# Close the plot to avoid memory issues
plt.close()
