"""
NEXAH Hierarchical Resonance Grid - Mod-77 State Space

Dieses Modul definiert den diskreten hierarchischen Zustandsraum für die NEXAH-Navigation.

- Basis: 77 Zustände aus Mod-7 × Mod-11
- Erweiterung: 2² → 308 feinere Zustände
- Enthält Mapping-Funktionen und Drift-Quantisierung
"""

import numpy as np
from typing import Tuple, List, Optional
import itertools

class Mod77StateSpace:
    """
    Repräsentiert den Mod-77 hierarchischen Zustandsraum.
    
    Attributes:
        num_states: Anzahl der Basis-Zustände (77)
        num_fine_states: Anzahl der feineren Zustände nach 2²-Erweiterung (308)
        delta: Drift-Parameter für die 2²-Verfeinerung (default ≈ 0.17)
    """
    
    def __init__(self, delta: float = 0.17):
        self.num_base_states = 77
        self.num_fine_states = 308
        self.delta = delta
        
        # Basis-Zustände: (r7, r11)
        self.base_states = list(itertools.product(range(7), range(11)))
        
        # Feinere Zustände mit ±delta (2²-Erweiterung)
        self.fine_offsets = list(itertools.product([-self.delta, 0, self.delta], repeat=2))
        # Wir nutzen nur 4 Kombinationen (±delta, ±delta) → echte 2²-Erweiterung
        self.fine_offsets = [off for off in self.fine_offsets if off != (0, 0)]  # ohne (0,0) falls gewünscht
    
    def get_base_state(self, idx: int) -> Tuple[int, int]:
        """Gibt den Basis-Zustand (r7, r11) für einen Index zurück."""
        return self.base_states[idx]
    
    def state_to_index(self, r7: int, r11: int) -> int:
        """Konvertiert (r7, r11) in einen flachen Index (0..76)."""
        return r7 * 11 + r11
    
    def index_to_state(self, idx: int) -> Tuple[int, int]:
        """Konvertiert flachen Index zurück in (r7, r11)."""
        r7 = idx // 11
        r11 = idx % 11
        return r7, r11
    
    def normalize_voltage(self, voltage: float, v_min: float = 0.65, v_max: float = 1.05) -> float:
        """Normalisiert eine Spannung (p.u.) auf [0, 1]."""
        return np.clip((voltage - v_min) / (v_max - v_min), 0.0, 1.0)
    
    def voltage_to_base_state(self, voltage: float) -> Tuple[int, int]:
        """Abbildet eine normierte Spannung auf einen Basis-Zustand (r7, r11)."""
        v_norm = self.normalize_voltage(voltage)
        r7 = int(round(v_norm * 6)) % 7      # 0..6
        r11 = int(round(v_norm * 10)) % 11   # 0..10
        return r7, r11
    
    def get_fine_states(self, r7: int, r11: int) -> List[Tuple[float, float]]:
        """Gibt die 4 feineren Zustände um (r7, r11) zurück (mit Drift-Offsets)."""
        fine = []
        for dr7, dr11 in itertools.product([-self.delta, self.delta], repeat=2):
            fine_r7 = (r7 + dr7) % 7
            fine_r11 = (r11 + dr11) % 11
            fine.append((fine_r7, fine_r11))
        return fine
    
    def compute_drift(self, state1: Tuple[int, int], state2: Tuple[int, int]) -> Tuple[float, float]:
        """Berechnet den Drift zwischen zwei Zuständen."""
        dr7 = (state2[0] - state1[0]) % 7
        dr11 = (state2[1] - state1[1]) % 11
        # Normalisierte Drift
        return dr7 / 7.0, dr11 / 11.0
    
    def get_state_info(self, idx: int) -> dict:
        """Gibt detaillierte Informationen zu einem Basis-Zustand."""
        r7, r11 = self.index_to_state(idx)
        return {
            'index': idx,
            'r7': r7,
            'r11': r11,
            'fine_states': self.get_fine_states(r7, r11),
            'description': f"Mod7={r7}, Mod11={r11}"
        }


# ============================
# Beispielnutzung / Test
# ============================

if __name__ == "__main__":
    grid = Mod77StateSpace(delta=0.17)
    
    print("=== NEXAH Mod-77 Hierarchical Grid ===")
    print(f"Basis-Zustände: {grid.num_base_states}")
    print(f"Feinere Zustände (2²): {grid.num_fine_states}")
    print(f"Drift-Parameter δ: {grid.delta}\n")
    
    # Beispiel: Spannung → Zustand
    test_voltages = [0.98, 0.92, 0.85, 0.71]
    for v in test_voltages:
        state = grid.voltage_to_base_state(v)
        idx = grid.state_to_index(*state)
        print(f"Spannung {v:.3f} p.u. → Zustand {state} (Index {idx})")
    
    # Beispiel: Feinere Zustände
    print("\nFeinere Zustände um (3, 5):")
    for fine in grid.get_fine_states(3, 5):
        print(f"  {fine}")
