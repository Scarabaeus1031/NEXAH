"""
URF Axial Space Kernel
======================

3D coordinate system for NEXAH Matroschka structures, Spiral Coupling and Switch Layer.
Maps the existing Dual-Strand Grey Channel + Elastic Axis into a clean 3D reference frame.

Axes:
    - Theta-Hertz Axis     (green) : frequency / oscillation / rotation
    - Magnet-Time Axis     (blue)  : magnetic flow / recall / duration
    - Beta Curvature       (orange): counter-rotation / restricted axis (√∫)
    - Memory Spin (M)      (red)   : vertical stability / spin (Ferro coupler)

Center: α (Potential)
"""

import numpy as np
from typing import Dict, Any


class URFAxialSpaceKernel:
    """
    Minimal 3D axial kernel for URF Axial Space (v9.1+).
    """

    def __init__(self):
        # Default scaling factors (can be tuned)
        self.theta_scale = 1.0      # frequency axis
        self.magnet_scale = 1.0     # time/flow axis
        self.beta_scale = 1.0       # curvature / restricted axis
        self.memory_scale = 1.0     # vertical spin

    def step(self, state: Dict[str, float]) -> Dict[str, Any]:
        """
        Takes current NEXAH state and returns 3D position in URF Axial Space.

        Expected keys in state:
            - coherence          (0..1)
            - coupling_dist      (pair coupling distance)
            - theta_hz           (current frequency component)
            - flow_direction     (from Spiral Coupling)
            - beta_curvature     (counter-rotation strength)
            - memory_spin        (Ferro / vertical stability)
        """
        # Extract components
        coherence = state.get("coherence", 0.0)
        coupling_dist = state.get("coupling_dist", 0.0)
        theta = state.get("theta_hz", 42.0)          # default Water ~42 Hz
        flow = state.get("flow_direction", 0.0)
        beta = state.get("beta_curvature", 0.0)
        memory = state.get("memory_spin", 1.0)

        # 3D coordinates in URF Axial Space
        x = self.theta_scale * theta * (1.0 - coupling_dist)          # Theta-Hertz
        y = self.magnet_scale * flow                                  # Magnet-Time
        z = self.beta_scale * beta                                    # Beta Curvature (√∫)

        # Vertical Memory Spin (red axis)
        m = self.memory_scale * memory * coherence

        # Restricted Axis (√∫) – the inner guidance line you mentioned
        restricted_axis = np.sqrt(np.abs(x * y * z)) * np.sign(coherence)

        return {
            "position_3d": np.array([x, y, z]),           # main URF coordinates
            "memory_spin": m,                             # vertical red axis
            "restricted_axis": restricted_axis,           # √∫ – your new frontier
            "coherence": coherence,
            "stability": "high" if coupling_dist < 0.1 else "medium",
            "matroschka_layer": self._get_matroschka_layer(z, beta),
            "switch_potential": abs(restricted_axis)      # strength for next switch
        }

    def _get_matroschka_layer(self, z: float, beta: float) -> str:
        """Simple layer classification for Matroschka nesting."""
        if abs(z) > 10 and beta > 0.7:
            return "Supra-Cosmos / Plasma"
        elif abs(z) > 5:
            return "Gas / High Energy"
        elif abs(z) > 2:
            return "Liquid / Flow"
        else:
            return "Solid / Core"

    def __repr__(self):
        return "URFAxialSpaceKernel (3D Matroschka + Restricted Axis √∫)"
