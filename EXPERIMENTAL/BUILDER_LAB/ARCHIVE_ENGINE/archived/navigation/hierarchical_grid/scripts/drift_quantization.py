"""
NEXAH Drift Quantization & Phi-Split
Quantisiert Drift und erkennt Phi-Split / Transfer Events
"""

from mod77_state_space import Mod77StateSpace
from scaling_exponent import ScalingExponent
from typing import List, Dict, Tuple

class DriftQuantization:
    def __init__(self, delta: float = 0.17, phi_split_threshold: float = 0.25):
        self.grid = Mod77StateSpace(delta=delta)
        self.scaler = ScalingExponent(p_base=0.308)
        self.phi_split_threshold = phi_split_threshold
    
    def analyze_drift(self, voltages: List[float]) -> List[Dict]:
        """Analysiert Drift, Phi-Split und mögliche Transfer Events."""
        mapped = []
        prev_state = None
        
        for i, v in enumerate(voltages):
            current_state = self.grid.voltage_to_base_state(v)
            idx = self.grid.state_to_index(*current_state)
            
            drift = None
            is_phi_split = False
            transfer_event = False
            
            if prev_state is not None:
                drift = self.grid.compute_drift(prev_state, current_state)
                drift_magnitude = max(abs(drift[0]), abs(drift[1]))
                
                # Phi-Split Erkennung
                is_phi_split = drift_magnitude > self.phi_split_threshold
                
                # Einfacher Transfer Event (starker Drift)
                transfer_event = drift_magnitude > 0.7
            
            result = {
                'time_step': i,
                'voltage': round(v, 4),
                'base_state': current_state,
                'state_index': idx,
                'drift': drift,
                'phi_split': is_phi_split,
                'transfer_event': transfer_event,
                'fine_states': self.grid.get_fine_states(*current_state),
                'predicted_p': round(self.scaler.p_base, 4)
            }
            mapped.append(result)
            prev_state = current_state
        
        return mapped
    
    def print_analysis(self, voltages: List[float], max_steps: int = 12):
        mapped = self.analyze_drift(voltages[:max_steps])
        
        print("=== NEXAH Drift Quantization & Phi-Split ===")
        print(f"Analyse von {len(voltages)} Spannungswerten (zeigt erste {max_steps})\n")
        
        for entry in mapped:
            v = entry['voltage']
            state = entry['base_state']
            drift = entry['drift']
            phi = "✓ Phi-Split" if entry['phi_split'] else ""
            transfer = "→ Transfer" if entry['transfer_event'] else ""
            
            drift_str = f"Drift: {drift}" if drift else "Drift: -"
            
            print(f"t={entry['time_step']:2d} | V={v:.4f} | State={state} | {drift_str} | {phi} {transfer}")
        
        print("\n→ Phi-Split und Transfer Events erkannt.")


# Demo
if __name__ == "__main__":
    example_voltages = [0.98, 0.97, 0.95, 0.92, 0.88, 0.84, 0.79, 0.74, 0.71, 0.70, 0.68, 0.65]
    
    dq = DriftQuantization(delta=0.17, phi_split_threshold=0.25)
    dq.print_analysis(example_voltages, max_steps=12)
