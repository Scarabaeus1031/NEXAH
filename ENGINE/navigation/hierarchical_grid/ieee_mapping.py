"""
NEXAH IEEE Trajectory Mapping
Abbildet Spannungstrajektorien auf das Mod-77 Gitter + Scaling Analysis
"""

from mod77_state_space import Mod77StateSpace
from scaling_exponent import ScalingExponent
from typing import List, Dict

class IEEEMapping:
    def __init__(self, delta: float = 0.17, p_base: float = 0.308):
        self.grid = Mod77StateSpace(delta=delta)
        self.scaler = ScalingExponent(p_base=p_base)
    
    def map_trajectory(self, voltages: List[float]) -> List[Dict]:
        """Abbildet eine Liste von Spannungswerten auf das Mod-77 Gitter."""
        mapped = []
        prev_state = None
        
        for i, v in enumerate(voltages):
            current_state = self.grid.voltage_to_base_state(v)
            idx = self.grid.state_to_index(*current_state)
            
            drift = None
            if prev_state is not None:
                drift = self.grid.compute_drift(prev_state, current_state)
            
            # Einfache Schätzung der Systemgröße (später durch echte Bus-Anzahl ersetzen)
            system_size = max(9, len(voltages))
            
            result = {
                'time_step': i,
                'voltage': round(v, 4),
                'base_state': current_state,
                'state_index': idx,
                'drift': drift,
                'fine_states': self.grid.get_fine_states(*current_state),
                'predicted_p': round(self.scaler.predict_p_for_system_size(system_size), 4) if hasattr(self.scaler, 'predict_p_for_system_size') else self.scaler.p_base
            }
            mapped.append(result)
            prev_state = current_state
        
        return mapped
    
    def print_summary(self, voltages: List[float], max_steps: int = 8):
        """Übersichtliche Ausgabe der Mapping."""
        mapped = self.map_trajectory(voltages[:max_steps])
        
        print("=== IEEE Trajectory → Mod-77 Mapping ===")
        print(f"Verarbeitete Spannungswerte: {len(voltages)} (zeigt erste {max_steps})\n")
        
        for entry in mapped:
            v = entry['voltage']
            state = entry['base_state']
            idx = entry['state_index']
            drift = entry['drift']
            p = entry['predicted_p']
            
            drift_str = f"Drift: {drift}" if drift else "Drift: -"
            print(f"t={entry['time_step']:2d} | V={v:.4f} | State={state} (Idx {idx}) | {drift_str} | p≈{p}")
        
        print("\n→ Fertig. Das Gitter ist jetzt mit realen Trajektorien verbunden.")


# Demo
if __name__ == "__main__":
    # Beispiel-Trajektorie (kann später durch echte V20-Daten ersetzt werden)
    example_voltages = [0.98, 0.97, 0.95, 0.92, 0.88, 0.84, 0.79, 0.74, 0.71, 0.70]
    
    mapper = IEEEMapping(delta=0.17)
    mapper.print_summary(example_voltages, max_steps=10)
