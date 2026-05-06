"""
NEXAH Hierarchical Resonance Grid - Mod-77 State Space
FINAL VERSION with compute_drift
"""

import numpy as np
from typing import Tuple, List
import itertools

class Mod77StateSpace:
    """Diskreter hierarchischer Zustandsraum für NEXAH-Navigation."""
    
    def __init__(self, delta: float = 0.17):
        self.delta = delta
        self.num_base_states = 77
        self.num_fine_states = 308
    
    def state_to_index(self, r7: int, r11: int) -> int:
        return r7 * 11 + r11
    
    def index_to_state(self, idx: int) -> Tuple[int, int]:
        r7 = idx // 11
        r11 = idx % 11
        return r7, r11
    
    def normalize_voltage(self, voltage: float, v_min: float = 0.65, v_max: float = 1.05) -> float:
        return np.clip((voltage - v_min) / (v_max - v_min), 0.0, 1.0)
    
    def voltage_to_base_state(self, voltage: float) -> Tuple[int, int]:
        v_norm = self.normalize_voltage(voltage)
        r7 = int(round(v_norm * 6)) % 7
        r11 = int(round(v_norm * 10)) % 11
        return r7, r11
    
    def get_fine_states(self, r7: int, r11: int) -> List[Tuple[float, float]]:
        """Gibt die 4 feineren Zustände (±delta) – garantiert im gültigen Bereich."""
        fine_states = []
        for dr7, dr11 in itertools.product([-self.delta, self.delta], repeat=2):
            fine_r7 = (r7 + dr7) % 7
            fine_r11 = (r11 + dr11) % 11
            if fine_r7 < 0:
                fine_r7 += 7
            if fine_r11 < 0:
                fine_r11 += 11
            fine_states.append((round(fine_r7, 4), round(fine_r11, 4)))
        return fine_states
    
    def compute_drift(self, state1: Tuple[int, int], state2: Tuple[int, int]) -> Tuple[float, float]:
        """Berechnet den Drift zwischen zwei Basis-Zuständen."""
        dr7 = (state2[0] - state1[0]) % 7
        dr11 = (state2[1] - state1[1]) % 11
        return round(dr7 / 7.0, 4), round(dr11 / 11.0, 4)

# Demo
if __name__ == "__main__":
    grid = Mod77StateSpace(delta=0.17)
    
    print("=== NEXAH Mod-77 Hierarchical Grid ===")
    print(f"Basis-Zustände     : {grid.num_base_states}")
    print(f"Feinere Zustände   : {grid.num_fine_states}")
    print(f"Drift-Parameter δ  : {grid.delta}\n")
    
    test_voltages = [0.98, 0.92, 0.85, 0.71]
    
    print("Beispiel-Abbildung:")
    for v in test_voltages:
        state = grid.voltage_to_base_state(v)
        idx = grid.state_to_index(*state)
        fine = grid.get_fine_states(*state)
        
        print(f"Spannung {v:.3f} p.u. → Zustand {state} (Index {idx})")
        print(f"   Feinere Zustände: {fine}\n")
