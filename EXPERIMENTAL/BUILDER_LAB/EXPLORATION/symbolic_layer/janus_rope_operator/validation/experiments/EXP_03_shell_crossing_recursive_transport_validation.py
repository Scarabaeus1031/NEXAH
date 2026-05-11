import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

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

# Berechnung von Shell-Crossing (dynamisch) und rekursiven Transportmustern
# Beispiel: Finden der Übergangspunkte und Visualisierung der Strukturen

# Funktion zur Berechnung von Mismatch und Übergangspunkten
def calculate_mismatch(system_solution):
    # Berechne den Mismatch als Abweichung von den erwarteten Phasen
    phase = np.arctan2(system_solution[:, 1], system_solution[:, 0])
    mismatch = np.abs(np.diff(phase))
    return mismatch

# Berechnen des Mismatches für das Lorenz-System
mismatch_lorenz = calculate_mismatch(solution)

# Visualisierung
fig, ax = plt.subplots(1, 2, figsize=(15, 6))

# Lorenz-System Phase-Diagramm
ax[0].plot(t, solution[:, 0], label='X')
ax[0].plot(t, solution[:, 1], label='Y')
ax[0].set_title('Lorenz System Phase')
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Phase')
ax[0].legend()

# Mismatch-Diagramm
ax[1].plot(t[1:], mismatch_lorenz, color='r')
ax[1].set_title('Mismatch between Phases')
ax[1].set_xlabel('Time')
ax[1].set_ylabel('Mismatch')

plt.tight_layout()

# Speichern der Visualisierungen
output_dir = "output_directory_here/"
plt.savefig(f"{output_dir}lorenz_system_mismatch.png")

# Anzeigen der Ergebnisse
plt.show()

# Weitere Analysen und Tests auf rekursive Transportgeometrien etc.
