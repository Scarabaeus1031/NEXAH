import numpy as np
import matplotlib.pyplot as plt
import os

# Parameter
t = np.linspace(0, 2 * np.pi, 1000)  # Zeit oder Phase
A0 = 1  # Maximale Amplitude

# Prime Verhältnisse
P1 = 3 / 5
P2 = 3 / 1

# Wellenfunktionen
A1 = A0 * np.sin(P1 * t)
A2 = A0 * np.sin(P2 * t)

# Berechnung des Cross-Correlation (zur Bestimmung der Synchronisation)
correlation = np.correlate(A1, A2, mode='valid')

# Berechnung der Kreuzungspunkte
crossing_points = np.where(np.diff(np.sign(correlation)))[0]

# Visualisierung der Wellen
plt.figure(figsize=(10, 6))
plt.plot(t, A1, label='Prime Ratio 3:5')
plt.plot(t, A2, label='Prime Ratio 3:1')

# Sicherstellen, dass keine falschen Indizes verwendet werden
valid_crossing_points = np.clip(crossing_points, 0, len(t) - 1)
plt.scatter(t[valid_crossing_points], A1[valid_crossing_points], color='red', label='Kreuzungspunkte', zorder=5)

plt.title('Prime Modulation und Phase Synchronisation (3:5, 3:1)')
plt.xlabel('Phase')
plt.ylabel('Amplitude')
plt.legend()

# Setze den korrekten Output-Verzeichnispfad
output_dir = "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/janus_rope_operator/outputs/EXP_21/"
os.makedirs(output_dir, exist_ok=True)

# Speichern des Outputs im angegebenen Verzeichnis
output_file = f"{output_dir}prime_modulation_sync.png"
plt.savefig(output_file)

# Zeigen des Outputs
plt.show()
