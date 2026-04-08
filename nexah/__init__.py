"""
NEXAH Public API

This module exposes the core structural components of the NEXAH Engine
for external users.
"""

# --- Core algebraic structures ---
from ENGINE.core.poset import FinitePoset as Poset
from ENGINE.core.lattice import LatticeOps as Lattice

# --- Operators ---
from ENGINE.core.closure_operator import ClosureOperator
from ENGINE.core.interior_operator import InteriorOperator
from ENGINE.core.monotone_operator import MonotoneOperator
from ENGINE.core.frame_operator import FrameOperator
from ENGINE.core.regime_operator import RegimeOperator

# --- High-level Engine Interface ---
class Engine:
    """
    High-level interface for the NEXAH framework.
    """
    def __init__(self):
        self.Poset = Poset
        self.Lattice = Lattice

    def create_poset(self, elements, order):
        return self.Poset(elements, order)

    def create_lattice(self, elements, order):
        return self.Lattice(elements, order)


# ================================================================
# === Spiral Coupling Layer (v9.0) ===
# ================================================================
from .spiral_coupling import SpiralCouplingLayer, SpiralCouplingKernel


# ================================================================
# === URF Axial Space Layer (v9.1) ===
# === 3D coordinate system for Matroschka + Switch Grid ===
# ================================================================
from .urf_axial_space.urf_axial_space_kernel import URFAxialSpaceKernel
from .urf_axial_space.switch_grid_mapper import SwitchGridMapper


# --- Public API export list ---
__all__ = [
    "Poset",
    "Lattice",
    "ClosureOperator",
    "InteriorOperator",
    "MonotoneOperator",
    "FrameOperator",
    "RegimeOperator",
    "Engine",
    # Spiral Coupling
    "SpiralCouplingLayer",
    "SpiralCouplingKernel",
    # URF Axial Space
    "URFAxialSpaceKernel",
    "SwitchGridMapper",
]

__version__ = "1.1"
