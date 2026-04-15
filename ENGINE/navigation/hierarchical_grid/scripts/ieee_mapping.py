"""
NEXAH IEEE Trajectory Mapping
Verbesserte Version – nutzt DriftQuantization + Scaling
"""

from mod77_state_space import Mod77StateSpace
from scaling_exponent import ScalingExponent
from drift_quantization import DriftQuantization
from typing import List

class IEEEMapping:
    def __init__(self, delta: float = 0.17):
        self.dq = DriftQuantization(delta=delta)
    
    def analyze(self, voltages: List[float]):
        """Vollständige Analyse einer Trajektorie"""
        analysis = self.dq.analyze_drift(voltages)
        
        print("=== NEXAH IEEE Trajectory Analysis ===")
        print(f"Spannungswerte analysiert: {len(voltages)}\n")
        
        for entry in analysis[:15]:   # erste 15 Schritte anzeigen
            v = entry['voltage']
            state = entry['base_state']
            drift = entry['drift']
            phi = "✓ Phi-Split" if entry.get('phi_split') else ""
            transfer = "→ Transfer" if entry.get('transfer_event') else ""
            
            drift_str = f"Drift: {drift}" if drift else "Drift: -"
            
            print(f"t={entry['time_step']:2d} | V={v:.4f} | State={state} | {drift_str} | {phi} {transfer}")
        
        print("\n→ Analyse abgeschlossen. Phi-Split und Transfer Events erkannt.")


# Demo
if __name__ == "__main__":
    # Beispiel-Trajektorie (später echte V20-Daten)
    example_voltages = [0.98, 0.97, 0.95, 0.92, 0.88, 0.84, 0.79, 0.74, 0.71, 0.70, 0.68, 0.65]
    
    mapper = IEEEMapping(delta=0.17)
    mapper.analyze(example_voltages)
