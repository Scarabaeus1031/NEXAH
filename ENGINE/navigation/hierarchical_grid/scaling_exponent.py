"""
NEXAH Scaling Exponent Analysis
p ≈ 0.308 + Multiplikationskette + Resonanz-Paare
"""

class ScalingExponent:
    def __init__(self, p_base: float = 0.308):
        self.p_base = p_base
        self.chain = self._build_chain()
        self.resonance_pairs = self._build_resonance_pairs()
    
    def _build_chain(self):
        """Multiplikationskette der 0.308"""
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
        print("   • p ≈ 0.308 beschreibt den Übergang von zustands- zu fluss-dominiert")
        print("   • Multiplikation mit 2, 3, 4 erzeugt nächste harmonische Schwellen")
        print("   • Feine Zustände bilden Paare, die auf 8, 11, 13, 16 summieren")
        print("   • 13 = Prime-Verbinder, 16 = 2^4 → höhere Struktur")


if __name__ == "__main__":
    scaler = ScalingExponent(p_base=0.308)
    scaler.print_summary()
