"""
NEXAH Hierarchical Grid - Visualization
Erzeugt Plots für Trajektorien, Phi-Split und Resonanz-Strukturen
"""

import numpy as np
import matplotlib.pyplot as plt
from mod77_state_space import Mod77StateSpace
from drift_quantization import DriftQuantization

class GridVisualizer:
    def __init__(self, delta: float = 0.17):
        self.grid = Mod77StateSpace(delta=delta)
        self.dq = DriftQuantization(delta=delta)
    
    def plot_trajectory(self, voltages: list[float], title: str = "IEEE Trajectory in Mod-77 Grid"):
        """Visualisiert die Trajektorie mit Phi-Split-Markierungen."""
        analysis = self.dq.analyze_drift(voltages)
        
        times = [entry['time_step'] for entry in analysis]
        voltages = [entry['voltage'] for entry in analysis]
        phi_splits = [entry['phi_split'] for entry in analysis]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Spannungskurve
        ax.plot(times, voltages, 'b-', linewidth=2, label='Spannung (p.u.)')
        
        # Phi-Split Markierungen
        for i, is_split in enumerate(phi_splits):
            if is_split:
                ax.scatter(times[i], voltages[i], color='red', s=80, zorder=5, label='Phi-Split' if i == 0 else "")
        
        ax.set_xlabel('Zeitschritt')
        ax.set_ylabel('Spannung [p.u.]')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        plt.show()
        
        print(f"Plot erzeugt: {len(voltages)} Punkte, Phi-Splits markiert.")
    
    def simple_grid_view(self):
        """Einfache Übersicht über das Gitter."""
        print("Mod-77 Gitter Übersicht:")
        print(f"   Basis-Zustände : {self.grid.num_base_states}")
        print(f"   Feine Zustände : {self.grid.num_fine_states}")
        print(f"   Drift δ        : {self.grid.delta}")
        print("\nBeispiel-Fein-Zustände für (3,5):")
        print(self.grid.get_fine_states(3, 5))


# Demo
if __name__ == "__main__":
    # Beispiel-Trajektorie
    example_voltages = [0.98, 0.97, 0.95, 0.92, 0.88, 0.84, 0.79, 0.74, 0.71, 0.70, 0.68, 0.65]
    
    viz = GridVisualizer(delta=0.17)
    
    print("=== NEXAH Grid Visualization ===")
    viz.simple_grid_view()
    print("\nErzeuge Trajektorie-Plot mit Phi-Split-Markierungen...")
    viz.plot_trajectory(example_voltages, title="Beispiel-Trajektorie mit Phi-Split Events")
