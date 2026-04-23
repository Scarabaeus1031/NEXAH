# nexah/spiral_coupling/spiral_coupling_kernel.py
"""
Integration der dreifachen Spiralüberlagerung in NEXAH.
(ohne Abhängigkeit vom noch nicht existierenden Navigation Kernel)
"""

from .spiral_coupling_layer import SpiralCouplingLayer
import numpy as np
from typing import Dict

class SpiralCouplingKernel:
    """
    Einfacher Kernel für die dreifache Spiralüberlagerung.
    Kann später leicht in den Haupt-Navigation-Kernel eingebaut werden.
    """
    
    def __init__(self, coupling_strength: float = 0.85):
        self.layer = SpiralCouplingLayer(dt=0.01, coupling_strength=coupling_strength)

    def step(self, current_state: np.ndarray = None, external_input=None):
        """Ein Schritt der dreifachen Spirale"""
        if current_state is None:
            current_state = np.zeros(3)
        
        layer_state = self.layer.step(external_input)
        
        # Einfacher Flow-Vorschlag (Mittelwert der drei Schichten)
        flow_direction = (layer_state["water"] + layer_state["mercury"] + layer_state["ferro"]) / 3.0
        
        # Coherence = 1 - durchschnittliche Distanz zwischen den Schichten
        coherence = 1.0 - layer_state["avg_coupling_dist"]
        
        return {
            "layer_state": layer_state,
            "flow_direction": flow_direction,
            "coherence": coherence,
            "stability": "high" if coherence > 0.85 else "medium"
        }

    def get_state(self):
        """Aktueller Zustand"""
        return self.layer.get_state()
