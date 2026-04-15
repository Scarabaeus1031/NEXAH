"""
NEXAH Drift Quantization & Phi-Split
"""

import sys
import os
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from APPLICATIONS.navigation.core.mod77_state_space import Mod77StateSpace
from APPLICATIONS.navigation.core.scaling_exponent import ScalingExponent
from typing import List, Dict

class DriftQuantization:
    def __init__(self, delta: float = 0.17, phi_split_threshold: float = 0.25):
        self.grid = Mod77StateSpace(delta=delta)
        self.scaler = ScalingExponent(p_base=0.308)
        self.phi_split_threshold = phi_split_threshold
    
    def analyze_drift(self, voltages: List[float]) -> List[Dict]:
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
                
                is_phi_split = drift_magnitude > self.phi_split_threshold
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


if __name__ == "__main__":
    example_voltages = [0.98, 0.97, 0.95, 0.92, 0.88, 0.84, 0.79, 0.74, 0.71, 0.70, 0.68, 0.65]
    dq = DriftQuantization()
    analysis = dq.analyze_drift(example_voltages)
    print("DriftQuantization Test erfolgreich -", len(analysis), "Einträge")
