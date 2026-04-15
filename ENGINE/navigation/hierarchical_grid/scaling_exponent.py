"""
NEXAH Scaling Exponent - p ≈ 0.308 + Multiplikationskette + Resonanz-Paare
"""

import numpy as np

class ScalingExponent:
    def __init__(self, p_base: float = 0.308):
        self.p_base = p_base
        self.chain = self._build_chain()
        self.resonance_pairs = self._build_resonance_pairs()
    
    def _build_chain(self):
        return {
            1: round(self.p_base, 6),
            2: round(self.p_base * 2, 6),
            3: round(self.p_base * 3, 6),
            4: round(self.p_base * 4, 6),
        }
    
    def _build_resonance_pairs(self):
        """Beobachtete komplementäre Paare aus den feinen Zuständen"""
        return {
            '7.83 + 8.17': 16.00,
            '4.83 + 8.17': 13.00,
            '3.83 + 7.17': 11.00,
            '2.83 + 5.17': 8.00,
        }
    
    def print_summary(self):
        print("=== NEXAH Scaling Exponent Analysis ===")
        print(f"Base Exponent p          : {self.p_base:.6f}\n")
        
        print("Multiplikationskette:")
        for k, v in self.chain.items():
            print(f"   p × {k}  = {v:.6f}")
        
        print("\nResonanz-Paare aus feinen Zuständen:")
        for pair, sum_val in self.resonance_pairs.items():
            print(f"   {pair} = {sum_val}")
        
        print("\nInterpretation:")
        print("   • p ≈ 0.308 beschreibt Übergang zu fluss-dominiert")
        print("   • Multiplikation mit 2, 3, 4 erzeugt harmonische Schwellen")
        print("   • Feine Zustände bilden Paare, die auf 8, 11, 13, 16 summieren")
        print("   • 13 = Prime-Verbinder, 16 = 2^4 → höhere 2²-Erweiterung")

if __name__ == "__main__":
    scaler = ScalingExponent(p_base=0.308)
    scaler.print_summary()    print(f"Drift-Parameter δ  : {grid.delta}\n")
    
    test_voltages = [0.98, 0.92, 0.85, 0.71]
    
    print("Beispiel-Abbildung:")
    for v in test_voltages:
        state = grid.voltage_to_base_state(v)
        idx = grid.state_to_index(*state)
        fine = grid.get_fine_states(*state)
        print(f"Spannung {v:.3f} p.u. → Zustand {state} (Index {idx})")
        print(f"   Feinere Zustände: {fine}\n")
