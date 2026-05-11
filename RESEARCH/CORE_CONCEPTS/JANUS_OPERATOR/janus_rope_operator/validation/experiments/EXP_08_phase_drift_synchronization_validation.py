import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os

# Parameter für das Lorenz-System (oder ein anderes System für Vergleich)
sigma = 10
rho = 28
beta = 8/3

# Lorenz-System
def lorenz_system(X, t, sigma, rho, beta):
    x, y, z = X
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# Simulationszeitraum
t = np.linspace(0, 100, 10000)

# Anfangsbedingungen
X0 = [1, 0, 0]

# Systemintegration
solution = odeint(lorenz_system, X0, t, args=(sigma, rho, beta))

# Berechnung der Phasenverschiebung (Phase Drift)
def calculate_phase_drift(system_solution):
    phase = np.arctan2(system_solution[:, 1], system_solution[:, 0])
    phase_diff = np.diff(phase)
    return phase, phase_diff

# Berechnen der Phasenverschiebung für das Lorenz-System
phase_lorenz, phase_diff_lorenz = calculate_phase_drift(solution)

# Visualisierung
fig, ax = plt.subplots(1, 2, figsize=(15, 6))

# Lorenz-System Phase-Diagramm
ax[0].plot(t, phase_lorenz, label='Phase')
ax[0].set_title('Lorenz System Phase Drift')
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Phase')
ax[0].legend()

# Phase Drift-Diagramm
ax[1].plot(t[1:], phase_diff_lorenz, color='r')
ax[1].set_title('Phase Drift')
ax[1].set_xlabel('Time')
ax[1].set_ylabel('Phase Drift')

plt.tight_layout()

# Sicherstellen, dass der Ordner existiert
output_dir = "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/janus_rope_operator/validation/outputs/EXP_08/"
os.makedirs(output_dir, exist_ok=True)

# Speichern der Visualisierungen
output_file = f"{output_dir}lorenz_phase_drift_synchronization.png"
plt.savefig(output_file)

# Anzeigen der Ergebnisse
plt.show()

# Speichern der Ergebnisse für zukünftige Analysen
phase_drift_results = {
    'Lorenz Phase': phase_lorenz,
    'Lorenz Phase Drift': phase_diff_lorenz
}

# Ausgabe der Ergebnisse
phase_drift_results
