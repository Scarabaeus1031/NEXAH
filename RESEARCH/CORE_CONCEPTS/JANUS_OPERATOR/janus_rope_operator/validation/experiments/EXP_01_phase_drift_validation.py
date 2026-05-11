import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Lorenz System
def lorenz(t, state, sigma=10, beta=8/3, rho=28):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# Rössler System
def rossler(t, state, a=0.2, b=0.2, c=5.7):
    x, y, z = state
    dxdt = -y - z
    dydt = x + a * y
    dzdt = b + z * (x - c)
    return [dxdt, dydt, dzdt]

# Phase Mismatch Calculation
def calculate_mismatch(phase1, phase2):
    return np.abs(phase1 - phase2)

# Function to simulate a system and extract phase information
def simulate_system(system_func, t_span, initial_conditions, t_eval):
    solution = solve_ivp(system_func, t_span, initial_conditions, t_eval=t_eval)
    x = solution.y[0]
    y = solution.y[1]
    z = solution.y[2]
    
    # Phase calculation (simplified)
    phase = np.arctan2(y, x)
    return phase

# Simulation Parameters
t_span = (0, 100)  # Time span
initial_conditions = [1.0, 1.0, 1.0]  # Initial conditions for both systems
t_eval = np.linspace(0, 100, 10000)  # Evaluation time points

# Simulate Lorenz and Rössler Systems
lorenz_phase = simulate_system(lorenz, t_span, initial_conditions, t_eval)
rossler_phase = simulate_system(rossler, t_span, initial_conditions, t_eval)

# Calculate Phase Mismatch
phase_mismatch = calculate_mismatch(lorenz_phase, rossler_phase)

# Plot Results
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(t_eval, lorenz_phase, label="Lorenz Phase")
plt.title("Lorenz System Phase")
plt.xlabel("Time")
plt.ylabel("Phase")

plt.subplot(1, 2, 2)
plt.plot(t_eval, rossler_phase, label="Rössler Phase", color='r')
plt.title("Rössler System Phase")
plt.xlabel("Time")
plt.ylabel("Phase")

plt.tight_layout()

# Save Results
output_dir = "validation/outputs/EXP_01/"
plt.savefig(output_dir + "lorenz_rossler_phase_comparison.png")

# Log mismatch value
print(f"Phase Mismatch between Lorenz and Rössler systems: {np.mean(phase_mismatch)}")
