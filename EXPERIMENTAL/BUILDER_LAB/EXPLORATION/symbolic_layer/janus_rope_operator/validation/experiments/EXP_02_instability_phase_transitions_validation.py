import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Lorenz system equations
def lorenz(X, t, sigma, beta, rho):
    x, y, z = X
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# Rössler system equations
def rossler(X, t, a, b, c):
    x, y, z = X
    dxdt = -y - z
    dydt = x + a * y
    dzdt = b + z * (x - c)
    return [dxdt, dydt, dzdt]

# Parameters for Lorenz
sigma_lorenz = 10
beta_lorenz = 8/3
rho_lorenz = 28

# Parameters for Rössler
a_rossler = 0.2
b_rossler = 0.2
c_rossler = 5.7

# Time vector
t = np.linspace(0, 100, 10000)

# Initial conditions
X0_lorenz = [1.0, 0.0, 0.0]
X0_rossler = [1.0, 0.0, 0.0]

# Solve the ODEs
lorenz_solution = odeint(lorenz, X0_lorenz, t, args=(sigma_lorenz, beta_lorenz, rho_lorenz))
rossler_solution = odeint(rossler, X0_rossler, t, args=(a_rossler, b_rossler, c_rossler))

# Calculate phase (angle)
def calculate_phase(x, y):
    return np.arctan2(y, x)

# Calculate phases for both systems
phase_lorenz = calculate_phase(lorenz_solution[:, 0], lorenz_solution[:, 1])
phase_rossler = calculate_phase(rossler_solution[:, 0], rossler_solution[:, 1])

# Calculate phase mismatch
phase_mismatch = np.mean(np.abs(phase_lorenz - phase_rossler))

# Plot the phase plots for Lorenz and Rössler systems
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(t, phase_lorenz, color='blue')
plt.title('Lorenz System Phase')
plt.xlabel('Time')
plt.ylabel('Phase')

plt.subplot(1, 2, 2)
plt.plot(t, phase_rossler, color='red')
plt.title('Rössler System Phase')
plt.xlabel('Time')
plt.ylabel('Phase')

# Show plot
plt.tight_layout()


# Print phase mismatch
print(f"Phase Mismatch between Lorenz and Rössler systems: {phase_mismatch}")

# Save the plot
output_dir = './validation/outputs/EXP_02/'
plt.savefig(f"{output_dir}lorenz_rossler_phase_comparison.png")
