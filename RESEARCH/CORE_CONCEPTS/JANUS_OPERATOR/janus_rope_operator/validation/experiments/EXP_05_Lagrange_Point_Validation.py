import numpy as np
import matplotlib.pyplot as plt
import os

# Konstanten für die Lagrange-Punkte
LAGRANGE_POINTS = {
    'L6': np.array([1.0, -0.5]),  # Ungefähre Position des Lagrange 6 (Leading Earth)
    'L7': np.array([1.0, 0.5]),   # Ungefähre Position des Lagrange 7 (Trailing Earth)
    'Earth': np.array([1.0, 0.0])  # Position der Erde (vereinfacht)
}

# Funktion, um die Übergangsgeometrie zu simulieren
def lagrange_point_transition(lagrange_point):
    """
    Simuliere die Übergangsgeometrie für einen gegebenen Lagrange-Punkt.
    Args:
    - lagrange_point: Koordinaten des Lagrange-Punkts.
    Returns:
    - Übergangsweg (simulierte Daten)
    """
    phase = np.linspace(0, 2 * np.pi, 100)
    amplitude = np.sin(phase) * np.cos(lagrange_point[0] * phase)  # Phasenverschiebung basierend auf Position hinzufügen
    return phase, amplitude

# Lagrange 6 und Lagrange 7 Übergänge simulieren
lagrange_6_x, lagrange_6_y = lagrange_point_transition(LAGRANGE_POINTS['L6'])
lagrange_7_x, lagrange_7_y = lagrange_point_transition(LAGRANGE_POINTS['L7'])

# Visualisierung der Auswirkungen der Lagrange-Punkte auf die Übergangsgeometrie
plt.figure(figsize=(10, 6))
plt.plot(lagrange_6_x, lagrange_6_y, label='Lagrange 6', color='b')
plt.plot(lagrange_7_x, lagrange_7_y, label='Lagrange 7', color='r')
plt.title('Einfluss der Lagrange-Punkte auf die Übergangsgeometrie')
plt.xlabel('Phase')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Ausgabeordner einrichten
output_dir = "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/janus_rope_operator/validation/outputs/EXP_05/"
os.makedirs(output_dir, exist_ok=True)

# Speichern der Visualisierung im richtigen Ordner
output_file = f"{output_dir}lagrange_point_transition_geometry.png"
plt.savefig(output_file)

# Visualisierung anzeigen
plt.show()

# Ergebnisse für die weitere Analyse speichern
lagrange_results = {
    'Lagrange 6 Impact': {'x': lagrange_6_x, 'y': lagrange_6_y},
    'Lagrange 7 Impact': {'x': lagrange_7_x, 'y': lagrange_7_y}
}

# Ergebnisdateipfad für die Ergebnisse
lagrange_results
