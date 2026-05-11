import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Parameter für das Rössler-System (oder anderes System)
a = 0.2
b = 0.2
c = 5.7

# Rössler-System
def rossler_system(X, t, a, b, c):
    x, y, z = X
    dxdt = -y - z
    dydt = x + a * y
    dzdt = b + z * (x - c)
    return [dxdt, dydt, dzdt]

# Simulationszeitraum
t = np.linspace(0, 100, 10000)

# Anfangsbedingungen
X0 = [1, 0, 0]

# Systemintegration
solution = odeint(rossler_system, X0, t, args=(a, b, c))

# Berechnung der Kohärenz
def calculate_coherence(system_solution):
    coherence = np.dot(system_solution[:, 0], system_solution[:, 1]) / (np.linalg.norm(system_solution[:, 0]) * np.linalg.norm(system_solution[:, 1]))
    return coherence

# Berechnung der Kohärenz für das Rössler-System
coherence_rossler = calculate_coherence(solution)

# Visualisierung
fig, ax = plt.subplots(1, 2, figsize=(15, 6))

# Rössler-System Phase-Diagramm
ax[0].plot(t, solution[:, 0], label='X')
ax[0].plot(t, solution[:, 1], label='Y')
ax[0].set_title('Rössler System Phase')
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Phase')
ax[0].legend()

# Kohärenz-Diagramm
ax[1].plot(t, coherence_rossler, color='g')
ax[1].set_title('Coherence in Rössler System')
ax[1].set_xlabel('Time')
ax[1].set_ylabel('Coherence')

plt.tight_layout()

# Speichern der Visualisierungen
output_dir = "output_directory_here/"
plt.savefig(f"{output_dir}rossler_system_coherence.png")

# Anzeigen der Ergebnisse
plt.show()

# Weitere Kontrolltests mit externen Steuermechanismen und deren Auswirkungen auf die Stabilisierung
