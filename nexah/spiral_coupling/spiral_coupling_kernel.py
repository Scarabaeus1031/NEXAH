# nexah/spiral_coupling/spiral_coupling_kernel.py
"""
Integration der dreifachen Spiralüberlagerung in den NEXAH Navigation Kernel.
"""

from .spiral_coupling_layer import SpiralCouplingLayer
from nexah.navigation_kernel import NEXAHNavigationKernel  # falls schon vorhanden

class SpiralCouplingKernel:
    """
    Erweitert den Navigation Kernel um die dreifache Spiralüberlagerung.
    Der Ferro-Layer macht den magnetischen Flow sichtbar und koppelt alles.
    """
    
    def __init__(self, base_field=None):
        self.layer = SpiralCouplingLayer(dt=0.01, coupling_strength=0.85)
        self.base_field = base_field  # V69 Field oder anderes bestehendes Field

    def step(self, current_state: np.ndarray, external_input=None):
        """Ein voller Schritt: Layer + Navigation-Vorschlag"""
        layer_state = self.layer.step(external_input)
        
        # Einfache Navigation: Richtung des gekoppelten Flows
        flow_direction = (layer_state["water"] + layer_state["mercury"] + layer_state["ferro"]) / 3.0
        coherence = 1.0 - layer_state["avg_coupling_dist"]   # je kleiner Distanz, desto höher Kohärenz

        return {
            "layer_state": layer_state,
            "flow_direction": flow_direction,
            "coherence": coherence,
            "stability": "high" if coherence > 0.85 else "medium"
        }

    def propose_motion(self, current_state: np.ndarray, horizon: int = 10):
        """Vorschlag für coherence-guided Motion (wie im Navigation Kernel)"""
        motions = []
        for _ in range(horizon):
            step = self.step(current_state)
            motions.append(step["flow_direction"])
            current_state = current_state + step["flow_direction"] * 0.1
        return motions
