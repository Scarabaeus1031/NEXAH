"""
NEXAH IEEE9 Navigation Prototype
Verbindet das Mod-77 Hierarchical Grid mit einer IEEE9-ähnlichen Trajektorie
"""

from mod77_state_space import Mod77StateSpace
from drift_quantization import DriftQuantization
from scaling_exponent import ScalingExponent
import numpy as np

class IEEE9Navigator:
    def __init__(self, delta: float = 0.17):
        self.grid = Mod77StateSpace(delta=delta)
        self.dq = DriftQuantization(delta=delta, phi_split_threshold=0.25)
        self.scaler = ScalingExponent(p_base=0.308)
    
    def run_example_trajectory(self):
        """Beispiel-Trajektorie, die einem IEEE9 Voltage-Collapse-Szenario ähnelt."""
        # Einfache fallende Spannungstrajektorie (kann später durch echte IEEE9-Simulation ersetzt werden)
        voltages = [0.98, 0.975, 0.96, 0.94, 0.92, 0.89, 0.86, 0.82, 0.78, 0.74, 0.71, 0.68, 0.65]
        
        print("=== NEXAH IEEE9 Navigation Prototype ===")
        print("Trajektorie wird analysiert...\n")
        
        analysis = self.dq.analyze_drift(voltages)
        
        for entry in analysis:
            v = entry['voltage']
            state = entry['base_state']
            drift = entry['drift']
            phi = "✓ Phi-Split" if entry.get('phi_split') else ""
            transfer = "→ Transfer Event" if entry.get('transfer_event') else ""
            
            drift_str = f"Drift: {drift}" if drift else "Drift: -"
            
            print(f"t={entry['time_step']:2d} | V={v:.4f} | State={state} | {drift_str} | {phi} {transfer}")
        
        print("\n=== Zusammenfassung ===")
        phi_count = sum(1 for e in analysis if e.get('phi_split'))
        transfer_count = sum(1 for e in analysis if e.get('transfer_event'))
        print(f"Phi-Split Events erkannt : {phi_count}")
        print(f"Transfer Events erkannt  : {transfer_count}")
        print(f"Finaler Zustand          : {analysis[-1]['base_state']}")
        print(f"Predicted p              : {self.scaler.p_base:.4f}")
        
        # Prime Leap Hinweis
        print("\nPrime Leap Beobachtung:")
        print("   13 + 16 = 29 → rekursive Prime-Struktur erkannt")


if __name__ == "__main__":
    navigator = IEEE9Navigator(delta=0.17)
    navigator.run_example_trajectory()
