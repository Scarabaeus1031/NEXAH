# nexah/spiral_coupling/spiral_coupling_layer.py
"""
Dreifache Spiralüberlagerung (Water - Mercury - Ferro)
Der neue Multi-Layer in NEXAH.
Magnetismus (Ferro) wirkt als aktiver Koppler zwischen den drei Schichten.
"""

import numpy as np
from typing import Dict, Tuple

class SpiralCouplingLayer:
    """
    Dreifache Schicht: Water (stabil/flüssig), Mercury (reaktiv), Ferro (magnetisch)
    Erzeugt die dreifache Spiralüberlagerung und koppelt die Schichten.
    """
    
    def __init__(self, dt: float = 0.01, coupling_strength: float = 0.85):
        self.dt = dt
        self.coupling_strength = coupling_strength
        
        # Initialzustände der drei Schichten
        self.water = np.zeros(3)      # blau  - träge, stabile Komponente
        self.mercury = np.zeros(3)    # rot   - reaktive, schnelle Komponente
        self.ferro = np.zeros(3)      # grün  - magnetischer Flow (Koppler)
        
        self.history = {"water": [], "mercury": [], "ferro": [], "coupling_dist": []}

    def step(self, external_input: np.ndarray = None) -> Dict[str, np.ndarray]:
        """Ein Zeitschritt der dreifachen Spiralüberlagerung."""
        if external_input is None:
            external_input = np.zeros(3)

        # Einfache Kopplungsdynamik (kann später erweitert werden)
        coupling_force = self.coupling_strength * (self.water + self.mercury + self.ferro)

        self.water   += self.dt * (external_input - 0.3 * self.water   + coupling_force)
        self.mercury += self.dt * (external_input - 0.1 * self.mercury + coupling_force * 1.6)
        self.ferro   += self.dt * (external_input - 0.6 * self.ferro   + coupling_force * 2.2)

        # Pair Coupling Distance (wie in deinen Visuals)
        dist_wm = np.linalg.norm(self.water - self.mercury)
        dist_mf = np.linalg.norm(self.mercury - self.ferro)
        dist_fw = np.linalg.norm(self.ferro - self.water)
        avg_dist = (dist_wm + dist_mf + dist_fw) / 3.0

        # History für Visuals
        self.history["water"].append(self.water.copy())
        self.history["mercury"].append(self.mercury.copy())
        self.history["ferro"].append(self.ferro.copy())
        self.history["coupling_dist"].append(avg_dist)

        return {
            "water": self.water,
            "mercury": self.mercury,
            "ferro": self.ferro,
            "avg_coupling_dist": avg_dist
        }

    def get_state(self) -> Dict:
        """Aktueller Zustand für den Navigation Kernel."""
        return {
            "positions": {"water": self.water, "mercury": self.mercury, "ferro": self.ferro},
            "coupling_strength": self.coupling_strength,
            "avg_coupling_dist": self.history["coupling_dist"][-1] if self.history["coupling_dist"] else 0.0
        }
