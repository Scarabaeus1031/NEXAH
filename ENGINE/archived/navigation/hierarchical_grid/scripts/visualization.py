"""
NEXAH Hierarchical Grid - Improved Visualization
"""

import numpy as np
import matplotlib.pyplot as plt
from mod77_state_space import Mod77StateSpace
from drift_quantization import DriftQuantization

class GridVisualizer:
    def __init__(self, delta: float = 0.17):
        self.grid = Mod77StateSpace(delta=delta)
        self.dq = DriftQuantization(delta=delta, phi_split_threshold=0.25)
    
    def plot_trajectory(self, voltages: list[float], title: str = "NEXAH Trajectory with Phi-Split", save_as=None):
        analysis = self.dq.analyze_drift(voltages)
        
        times = [e['time_step'] for e in analysis]
        volts = [e['voltage'] for e in analysis]
        phi_splits = [e['phi_split'] for e in analysis]
        drifts = [max(abs(e['drift'][0]), abs(e['drift'][1])) if e['drift'] else 0 for e in analysis]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), height_ratios=[3, 1], sharex=True)
        
        # Obere Plot: Spannung + Phi-Split
        ax1.plot(times, volts, 'b-', linewidth=2.5, label='Spannung (p.u.)')
        for i, is_split in enumerate(phi_splits):
            if is_split:
                ax1.scatter(times[i], volts[i], color='red', s=120, zorder=5, label='Phi-Split' if i == 0 else "")
        
        ax1.set_ylabel('Spannung [p.u.]')
        ax1.set_title(title)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Untere Plot: Drift-Magnitude
        ax2.plot(times, drifts, 'orange', linewidth=2, label='Drift Magnitude')
        ax2.axhline(y=0.25, color='red', linestyle='--', alpha=0.7, label='Phi-Split Threshold')
        ax2.set_ylabel('Drift Magnitude')
        ax2.set_xlabel('Zeitschritt')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        
        if save_as:
            plt.savefig(save_as, dpi=200, bbox_inches='tight')
            print(f"Plot gespeichert als: {save_as}")
        
        plt.show()
    
    def simple_grid_view(self):
        print("Mod-77 Gitter Übersicht:")
        print(f"   Basis-Zustände : {self.grid.num_base_states}")
        print(f"   Feine Zustände : {self.grid.num_fine_states}")
        print(f"   Drift δ        : {self.grid.delta}\n")


# Demo
if __name__ == "__main__":
    example_voltages = [0.98, 0.97, 0.95, 0.92, 0.88, 0.84, 0.79, 0.74, 0.71, 0.70, 0.68, 0.65]
    
    viz = GridVisualizer(delta=0.17)
    viz.simple_grid_view()
    viz.plot_trajectory(example_voltages, 
                        title="NEXAH IEEE Trajectory with Phi-Split Events",
                        save_as="nexah_phi_split_trajectory.png")
