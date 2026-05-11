import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os

# Systemparameter für Lorenz, Rössler und Halvorsen
sigma, rho, beta = 10, 28, 8 / 3
a, b, c = 0.2, 0.2, 5.7
p, q, r = 0.4, 0.4, 3.1

# Lorenz System
def lorenz_system(X, t, sigma, rho, beta):
    x, y, z = X
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# Rössler System
def rossler_system(X, t, a, b, c):
    x, y, z = X
    dxdt = -y - z
    dydt = x + a * y
    dzdt = b + z * (x - c)
    return [dxdt, dydt, dzdt]

# Halvorsen System
def halvorsen_system(X, t, p, q, r):
    x, y, z = X
    dxdt = p * (y - x)
    dydt = x * (r - z) - y
    dzdt = x * y - q * z
    return [dxdt, dydt, dzdt]

# Simulationszeitraum
t = np.linspace(0, 100, 10000)

# Anfangsbedingungen
X0 = [1, 0, 0]

# Systemintegration für Lorenz, Rössler und Halvorsen
lorenz_solution = odeint(lorenz_system, X0, t, args=(sigma, rho, beta))
rossler_solution = odeint(rossler_system, X0, t, args=(a, b, c))
halvorsen_solution = odeint(halvorsen_system, X0, t, args=(p, q, r))

# Berechnungen der Synchronisationseffekte
def calculate_sync(X1, X2):
    # Berechnung der Synchronisation als Korrelation der beiden Systeme
    return np.corrcoef(X1[:, 0], X2[:, 0])[0, 1]

# Berechnen der Synchronisation
lorenz_rossler_sync = calculate_sync(lorenz_solution, rossler_solution)
rossler_halvorsen_sync = calculate_sync(rossler_solution, halvorsen_solution)
lorenz_halvorsen_sync = calculate_sync(lorenz_solution, halvorsen_solution)

# Visualisierung der Synchronisation
fig, ax = plt.subplots(1, 3, figsize=(15, 6))

ax[0].plot(t, lorenz_solution[:, 0], label='Lorenz')
ax[0].plot(t, rossler_solution[:, 0], label='Rössler')
ax[0].set_title(f"Lorenz vs Rössler Sync: {lorenz_rossler_sync:.3f}")
ax[0].legend()

ax[1].plot(t, rossler_solution[:, 0], label='Rössler')
ax[1].plot(t, halvorsen_solution[:, 0], label='Halvorsen')
ax[1].set_title(f"Rössler vs Halvorsen Sync: {rossler_halvorsen_sync:.3f}")
ax[1].legend()

ax[2].plot(t, lorenz_solution[:, 0], label='Lorenz')
ax[2].plot(t, halvorsen_solution[:, 0], label='Halvorsen')
ax[2].set_title(f"Lorenz vs Halvorsen Sync: {lorenz_halvorsen_sync:.3f}")
ax[2].legend()

plt.tight_layout()

# Output directory setup
output_dir = "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/janus_rope_operator/experiments/EXP_20/"
os.makedirs(output_dir, exist_ok=True)

# Speichern der Visualisierungen
output_file = f"{output_dir}prime_modulation_sync.png"
plt.savefig(output_file)

# Anzeigen der Ergebnisse
plt.show()

# Ergebnisausgabe
sync_results = {
    'Lorenz vs Rössler Sync': lorenz_rossler_sync,
    'Rössler vs Halvorsen Sync': rossler_halvorsen_sync,
    'Lorenz vs Halvorsen Sync': lorenz_halvorsen_sync
}

sync_results
