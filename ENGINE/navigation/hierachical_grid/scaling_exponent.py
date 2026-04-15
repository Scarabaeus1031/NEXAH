"""
NEXAH Hierarchical Grid - Scaling Exponent Analysis
===================================================

Berechnet und verwaltet den emergenten kritischen Exponenten p ≈ 0.308
sowie dessen Multiplikationskette und Winkel-Verbindung.
"""

import numpy as np
from typing import Dict, List, Tuple

class ScalingExponent:
    """
    Verwaltet den kritischen Exponenten p ≈ 0.308 und verwandte Skalierungsbeziehungen.
    """
    
    def __init__(self, p_base: float = 0.308):
        self.p_base = p_base
        self.multiplication_chain = self._compute_multiplication_chain()
        self.angle_relation = self._compute_angle_relation()
    
    def _compute_multiplication_chain(self) -> Dict[int, float]:
        """Berechnet die Multiplikationskette: p × 2, p × 3, p × 4"""
        return {
            1: round(self.p_base, 6),
            2: round(self.p_base * 2, 6),
            3: round(self.p_base * 3, 6),
            4: round(self.p_base * 4, 6),
        }
    
    def _compute_angle_relation(self) -> Dict[str, float]:
        """Berechnet die Winkel-Verbindung: 27.692° / 90° ≈ 0.308"""
        theta_critical_deg = 27.692
        f_axis_deg = 90.0
        ratio = theta_critical_deg / f_axis_deg
        
        return {
            'theta_critical_deg': theta_critical_deg,
            'theta_critical_approx': 28.0,
            'f_axis_deg': f_axis_deg,
            'ratio': round(ratio, 6),
            'description': f"p ≈ {ratio:.6f} = {theta_critical_deg}° / 90°"
        }
    
    def get_multiplication_chain(self) -> Dict[int, float]:
        """Gibt die Multiplikationskette zurück."""
        return self.multiplication_chain
    
    def get_angle_relation(self) -> Dict[str, float]:
        """Gibt die Winkel-Beziehung zurück."""
        return self.angle_relation
    
    def predict_p_for_system_size(self, system_size: float) -> float:
        """
        Einfaches heuristisches Modell: p nimmt mit Systemgröße ab 
        (von zustands-dominiert zu fluss-dominiert).
        """
        # Beispiel: Bei kleinen Systemen p näher an 0.5, bei großen → 0.308
        return max(0.308, 0.55 - 0.12 * np.log10(system_size))
    
    def print_summary(self):
        """Gibt eine übersichtliche Zusammenfassung aus."""
        print("=== NEXAH Scaling Exponent Analysis ===")
        print(f"Base Exponent p          : {self.p_base:.6f}\n")
        
        print("Multiplikationskette:")
        for k, v in self.multiplication_chain.items():
            print(f"   p × {k}  = {v:.6f}")
        
        print("\nWinkel-Verbindung:")
        angle = self.angle_relation
        print(f"   Critical Angle       : {angle['theta_critical_deg']}° ≈ {angle['theta_critical_approx']}° = 4×7°")
        print(f"   F-Axis               : {angle['f_axis_deg']}°")
        print(f"   Ratio                : {angle['ratio']:.6f}")
        print(f"   → {angle['description']}")
        
        print("\nInterpretation:")
        print("   • p ≈ 0.308 beschreibt den Übergang von zustands- zu fluss-dominiert")
        print("   • Multiplikation mit 2, 3, 4 erzeugt nächste harmonische Schwellen")
        print("   • 28° = 4×7° verbindet den Exponenten mit dem Mod-7-Zyklus")


# ============================
# Beispielnutzung
# ============================

if __name__ == "__main__":
    scaler = ScalingExponent(p_base=0.308)
    scaler.print_summary()
    
    # Beispiel: Vorhersage für unterschiedliche Systemgrößen
    print("\nVorhergesagter p für verschiedene Systemgrößen:")
    for size in [9, 118, 300, 1354, 9241]:
        p_pred = scaler.predict_p_for_system_size(size)
        print(f"   IEEE{size:4d} → p ≈ {p_pred:.4f}")
