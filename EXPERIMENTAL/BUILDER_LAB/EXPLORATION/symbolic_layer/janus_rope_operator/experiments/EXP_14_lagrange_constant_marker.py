import numpy as np
import matplotlib.pyplot as plt
import os

# Konstanten für Lagrange-Punkte (vereinfacht)
LAGRANGE_POINTS = {
    'L6': np.array([1.0, -0.5]),  # Lagrange 6 (Leading Earth)
    'L7': np.array([1.0, 0.5]),   # Lagrange 7 (Trailing Earth)
    'Earth': np.array([1.0, 0.0])  # Position der Erde
}

# Prime-Offsets als Faktoren für die Phasenverschiebung
PRIME_OFFSETS = {
    'L6': 0.1,
    'L7': 0.2
}

# Funktion zur Simulation der Phasenverschiebung an den Lagrange-Punkten mit Prime-Offsets
def lagrange_prime_drift(lagrange_point, prime_offset, phases=100):
    """
    Simuliert die Phasenverschiebung für Lagrange-Punkte mit Prime-Offsets.
    Args:
    - lagrange_point: Koordinaten des Lagrange-Punkts.
    - prime_offset: Offset zur Modulation der Phasenverschiebung.
    - phases: Anzahl der Punkte im Phasenraum.
    Returns:
    - x- und y-Koordinaten des Driftpfads.
    """
    phase = np.linspace(0, 2 * np.pi, phases)
    amplitude = np.sin(phase) * np.cos(lagrange_point[0] * phase + prime_offset)
    return phase, amplitude

# Simuliere die Lagrange-Punkte mit Prime-Offsets
lagrange_6_x, lagrange_6_y = lagrange_prime_drift(LAGRANGE_POINTS['L6'], PRIME_OFFSETS['L6'])
lagrange_7_x, lagrange_7_y = lagrange_prime_drift(LAGRANGE_POINTS['L7'], PRIME_OFFSETS['L7'])

# Simuliere die Interaktion zwischen Lagrange 6 und 7 (Kopplung)
coupled_lagrange_6_x = lagrange_6_x + 0.5  # Leichte Phasenverschiebung für Interaktion
coupled_lagrange_7_x = lagrange_7_x - 0.5  # Leichte Phasenverschiebung für Interaktion
coupled_lagrange_6_y = lagrange_6_y
coupled_lagrange_7_y = lagrange_7_y

# Plotte die Lagrange-Punkte und ihre Interaktionen
plt.figure(figsize=(12, 6))
plt.plot(lagrange_6_x, lagrange_6_y, label='Lagrange 6 (Prime Offsets)', color='b')
plt.plot(lagrange_7_x, lagrange_7_y, label='Lagrange 7 (Prime Offsets)', color='r')
plt.plot(coupled_lagrange_6_x, coupled_lagrange_6_y, '--', label='Coupled Lagrange 6', color='orange')
plt.plot(coupled_lagrange_7_x, coupled_lagrange_7_y, '--', label='Coupled Lagrange 7', color='purple')
plt.title('Vortex Coupling und Prime Offset Modulation an Lagrange-Punkten')
plt.xlabel('Phase')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Verzeichniseinstellungen für EXP_14
output_dir = "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/janus_rope_operator/experiments/EXP_14/"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(f"{output_dir}/vortex_prime_modulation_lagrange.png")

# Zeige das Plot
plt.show()

# Numerische Ergebnisse für Lagrange 6 und 7 (Mittelwert, Max, Min)
lagrange_results = {
    'L6 Phase': {'Mean': np.mean(lagrange_6_y), 'Max': np.max(lagrange_6_y), 'Min': np.min(lagrange_6_y)},
    'L7 Phase': {'Mean': np.mean(lagrange_7_y), 'Max': np.max(lagrange_7_y), 'Min': np.min(lagrange_7_y)},
    'Coupled L6': {'Mean': np.mean(coupled_lagrange_6_y), 'Max': np.max(coupled_lagrange_6_y), 'Min': np.min(coupled_lagrange_6_y)},
    'Coupled L7': {'Mean': np.mean(coupled_lagrange_7_y), 'Max': np.max(coupled_lagrange_7_y), 'Min': np.min(coupled_lagrange_7_y)},
}

lagrange_results
